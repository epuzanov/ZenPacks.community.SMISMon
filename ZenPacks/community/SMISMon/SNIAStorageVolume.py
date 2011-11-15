################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStorageVolume

SNIAStorageVolume is an abstraction of a CIM_StorageVolume

$Id: SNIAStorageVolume.py,v 1.3 2011/11/13 23:00:31 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId
from ZenPacks.community.SMISMon.CIMManagedSystemElement import *

import logging
log = logging.getLogger("zen.SNIAStorageVolume")


def manage_addStorageVolume(context, id, userCreated, REQUEST=None):
    """make StorageVolume"""
    svid = prepId(id)
    sv = SNIAStorageVolume(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class SNIAStorageVolume(OSComponent, CIMManagedSystemElement):
    """HPStorageVolume object"""

    portal_type = meta_type = 'StorageVolume'

    accessType = ""
    caption = ""
    blockSize = 0
    diskType = ""

    _properties = OSComponent._properties + (
                 {'id':'accessType', 'type':'string', 'mode':'w'},
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'blockSize', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                ) + CIMManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.SMISMon.SNIADevice.SNIADeviceOS",
            "virtualdisks")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.SMISMon.SNIAStoragePool",
            "virtualdisks")),
        ("collection", ToOne(ToMany,
            "ZenPacks.community.SMISMon.SNIAReplicationGroup",
            "virtualdisks")),
        )

    factory_type_information = (
        {
            'id'             : 'StorageVolume',
            'meta_type'      : 'StorageVolume',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageVolume_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStorageVolume',
            'immediate_view' : 'viewSNIAStorageVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAStorageVolume'
                , 'permissions'   : (ZEN_VIEW,)
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
        return getattr(self.getStoragePool(), 'poolId', 'Unknown')


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setReplicationGroup')
    def setReplicationGroup(self, cid):
        """
        Set the drgroup relationship to the ReplicationGroup specified by the given id
        """
        for coll in self.os().collections() or []:
            if coll.snmpindex != cid: continue
            self.collection.addRelation(coll)
            break


    security.declareProtected(ZEN_VIEW, 'getReplicationGroup')
    def getReplicationGroup(self):
        return self.collection()


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('NumberOfBlocks', 0) * self.blockSize


    def totalBytesString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.totalBytes(), divby=1024)


    def getRRDNames(self):
        """
        Return the datapoint name of this StorageVolume
        """
        return ['StorageVolume_NumberOfBlocks']


    def viewName(self): return self.caption


InitializeClass(SNIAStorageVolume)
