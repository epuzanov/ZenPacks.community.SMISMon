################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAReplicationGroup

SNIAReplicationGroup is an abstraction of a CIM_Collection

$Id: SNIAReplicationGroup.py,v 1.1 2011/11/13 22:53:44 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.CIMManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.SNIAReplicationGroup")


def manage_addReplicationGroup(context, id, userCreated, REQUEST=None):
    """make ReplicationGroup"""
    svid = prepId(id)
    sv = SNIAReplicationGroup(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class SNIAReplicationGroup(OSComponent, CIMManagedSystemElement):
    """ReplicationGroup object"""

    portal_type = meta_type = 'ReplicationGroup'

    caption = ""

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                ) + CIMManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.SMISMon.SNIADevice.SNIADeviceOS",
            "collections")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.SMISMon.SNIAStoragePool",
            "collections")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIAStorageVolume",
            "collection")),
        )

    factory_type_information = (
        {
            'id'             : 'ReplicationGroup',
            'meta_type'      : 'ReplicationGroup',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ReplicationGroup_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addReplicationGroup',
            'immediate_view' : 'viewSNIAReplicationGroup',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAReplicationGroup'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'members'
                , 'name'          : 'Members'
                , 'action'        : 'viewSNIAReplicationGroupMembers'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    security = ClassSecurityInfo()


    getRRDTemplates = CIMManagedSystemElement.getRRDTemplates


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        for sp in self.os().storagepools() or []:
            if sp.snmpindex != spid: continue
            self.storagepool.addRelation(sp)
            break


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()


    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    def viewName(self): return self.caption


InitializeClass(SNIAReplicationGroup)
