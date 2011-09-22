################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_ConsistencySet

SNIA_ConsistencySet is an abstraction of a CIM_ConsistencySet

$Id: SNIA_ConsistencySet.py,v 1.0 2011/09/04 22:40:34 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.SNIA_ManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.SNIA_ConsistencySet")


def manage_addConsistencySet(context, id, userCreated, REQUEST=None):
    """make ConsistencySet"""
    svid = prepId(id)
    sv = SNIA_ConsistencySet(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class SNIA_ConsistencySet(OSComponent, SNIA_ManagedSystemElement):
    """ConsistencySet object"""

    portal_type = meta_type = 'SNIA_ConsistencySet'

    caption = ""
    failSafe = ""
    hostAccessMode = ""
    participationType = ""
    remoteCellName = ""
    suspendMode = ""
    writeMode = ""

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'failSafe', 'type':'string', 'mode':'w'},
                 {'id':'hostAccessMode', 'type':'string', 'mode':'w'},
                 {'id':'participationType', 'type':'string', 'mode':'w'},
                 {'id':'remoteCellName', 'type':'string', 'mode':'w'},
                 {'id':'suspendMode', 'type':'string', 'mode':'w'},
                 {'id':'writeMode', 'type':'string', 'mode':'w'},
                ) + SNIA_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.SMISMon.SNIA_Device.SNIA_DeviceOS",
            "drgroups")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.SMISMon.SNIA_StoragePool",
            "drgroups")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIA_StorageVolume",
            "drgroup")),
        )

    factory_type_information = (
        {
            'id'             : 'ConsistencySet',
            'meta_type'      : 'ConsistencySet',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ConsistencySet_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addConsistencySet',
            'immediate_view' : 'viewSNIAConsistencySet',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAConsistencySet'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'members'
                , 'name'          : 'Members'
                , 'action'        : 'viewSNIAConsistencySetMembers'
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
        strpool = getattr(self.os().storagepools, str(spid), None)
        if strpool: self.storagepool.addRelation(strpool)
        else: log.warn("storage pool id:%s not found", spid)


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()


    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    def getCurrentPercentLogLevel(self):
        return "%s%%"%self.cacheRRDValue('CurrentPercentLogLevel', 0)


    def getLogDiskReservedCapacity(self):
        return convToUnits(self.cacheRRDValue('LogDiskReservedCapacity', 0)*512)


    def getRRDNames(self):
        """
        Return the datapoint name of this ConsistencySet
        """
        return ['ConsistencySet_CurrentPercentLogLevel',
                'ConsistencySet_LogDiskReservedCapacity',
                ]

InitializeClass(SNIA_ConsistencySet)
