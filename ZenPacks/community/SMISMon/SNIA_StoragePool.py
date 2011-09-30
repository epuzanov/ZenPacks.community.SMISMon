################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_StoragePool

SNIA_StoragePool is an abstraction of a CIM_StoragePool

$Id: SNIA_StoragePool.py,v 1.2 2011/09/30 18:39:17 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.SNIA_ManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits

class SNIA_StoragePool(OSComponent, SNIA_ManagedSystemElement):
    """SNIA StoragePool object"""

    portal_type = meta_type = 'SNIA_StoragePool'

    caption = ""
    totalManagedSpace = 0
    poolId = ""
    usage = 0

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'totalManagedSpace', 'type':'int', 'mode':'w'},
                 {'id':'poolId', 'type':'string', 'mode':'w'},
                 {'id':'usage', 'type':'int', 'mode':'w'},
                ) + SNIA_ManagedSystemElement._properties


    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "ZenPacks.community.SMISMon.SNIA_Device.SNIA_DeviceOS",
            "storagepools")),
        ("harddisks", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIA_DiskDrive",
            "storagepool")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIA_StorageVolume",
            "storagepool")),
        ("collections", ToMany(
            ToOne,
            "ZenPacks.community.SMISMon.SNIA_ReplicationGroup",
            "storagepool")),
        )

    factory_type_information = ( 
        {
            'id'             : 'StoragePool',
            'meta_type'      : 'StoragePool',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StoragePool_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStoragePool',
            'immediate_view' : 'viewSNIAStoragePool',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAStoragePool'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewSNIAStoragePoolDisks'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'volumes'
                , 'name'          : 'Volumes'
                , 'action'        : 'viewSNIAStoragePoolVolumes'
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


    def totalBytes(self):
        return self.totalManagedSpace or 0


    def usedBytes(self):
        return self.totalBytes() - self.cacheRRDValue('RemainingManagedSpace',0)


    def totalBytesString(self):
        return convToUnits(self.totalBytes(), divby=1024)


    def usedBytesString(self):
        return convToUnits(self.usedBytes(), divby=1024)


    def availBytesString(self):
        return convToUnits((self.totalBytes() - self.usedBytes()), divby=1024)


    def capacity(self):
        """
        Return the percentage capacity of a filesystems using its rrd file
        """
        __pychecker__='no-returnvalues'
        if self.totalBytes() is not 0:
            return int(100.0 * self.usedBytes() / self.totalBytes())
        return 'unknown'


    def totalDisks(self):
        """
        Return total disks number
        """
        return len(self.harddisks())


    def getRRDNames(self):
        """
        Return the datapoint name of this StoragePool
        """
        return ['StoragePool_RemainingManagedSpace',
                'StoragePool_TotalManagedSpace']


InitializeClass(SNIA_StoragePool)
