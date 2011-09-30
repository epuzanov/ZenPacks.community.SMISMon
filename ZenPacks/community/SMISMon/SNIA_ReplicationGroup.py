################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_ReplicationGroup

SNIA_ReplicationGroup is an abstraction of a CIM_Collection

$Id: SNIA_ReplicationGroup.py,v 1.0 2011/09/30 18:38:33 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.SNIA_ManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.SNIA_ReplicationGroup")


def manage_addReplicationGroup(context, id, userCreated, REQUEST=None):
    """make ReplicationGroup"""
    svid = prepId(id)
    sv = SNIA_ReplicationGroup(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class SNIA_ReplicationGroup(OSComponent, SNIA_ManagedSystemElement):
    """ReplicationGroup object"""

    portal_type = meta_type = 'SNIA_ReplicationGroup'

    caption = ""

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                ) + SNIA_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.SMISMon.SNIA_Device.SNIA_DeviceOS",
            "collections")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.SMISMon.SNIA_StoragePool",
            "collections")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIA_StorageVolume",
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

    getRRDTemplates = SNIA_ManagedSystemElement.getRRDTemplates

    security = ClassSecurityInfo()


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

InitializeClass(SNIA_ReplicationGroup)
