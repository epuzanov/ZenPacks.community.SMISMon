################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIADiskDrive

SNIADiskDrive is an abstraction of a harddisk.

$Id: SNIADiskDrive.py,v 1.2 2011/11/13 22:53:15 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import DTMLFile
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.SMISMon.CIMManagedSystemElement import *

import logging
log = logging.getLogger("zen.SNIADiskDrive")

addHardDisk = DTMLFile('dtml/addHardDisk', globals())

class SNIADiskDrive(HWComponent, CIMManagedSystemElement):
    """SNIA DiskDrive object"""

    portal_type = meta_type = 'DiskDrive'

    manage_editHardDiskForm = DTMLFile('dtml/manageEditHardDisk', globals())

    caption = ""
    size = 0
    diskType = "sas"
    replaceable = True
    bay = -1
    FWRev = ""

    _properties = HWComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'replaceable', 'type':'boolean', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                ) + CIMManagedSystemElement._properties

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                            "ZenPacks.community.SMISMon.SNIADeviceHW",
                            "harddisks")),
        ("enclosure", ToOne(ToMany,
                            "ZenPacks.community.SMISMon.SNIAEnclosureChassis",
                            "harddisks")),
        ("storagepool", ToOne(ToMany,
                            "ZenPacks.community.SMISMon.SNIAStoragePool",
                            "harddisks")),
        )


    factory_type_information = ( 
        { 
            'id'             : 'DiskDrive',
            'meta_type'      : 'DiskDrive',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'DiskDrive_icon.gif',
            'product'        : 'SMISMon',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewSNIADiskDrive',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIADiskDrive'
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


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setEnclosure')
    def setEnclosure(self, enclid):
        """
        Set the enclosure relationship to the enclosure specified by the given
        id.
        """
        for encl in self.hw().enclosures() or []:
            if encl.snmpindex != enclid: continue
            self.enclosure.addRelation(encl)
            break


    security.declareProtected(ZEN_VIEW, 'getEnclosure')
    def getEnclosure(self):
        """
        Return enclosure object
        """
        return self.enclosure()


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the
        given caption.
        """
        for sp in getattr(self.device().os, 'storagepools', (lambda:[]))():
            if sp.snmpindex != spid: continue
            self.storagepool.addRelation(sp)
            break


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        """
        Return Disk Group object
        """
        return self.storagepool()


    def getEnclosureName(self):
        """
        Return enclosure id
        """
        return getattr(self.getEnclosure(), 'caption', 'Unknown')


    def getStoragePoolName(self):
        """
        Return Disk Group name
        """
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    security.declareProtected(ZEN_VIEW, 'getManufacturerLink')
    def getManufacturerLink(self, target=None):
        """
        Return Manufacturer Link
        """
        if self.productClass():
            url = self.productClass().manufacturer.getPrimaryLink()
            if target: url = url.replace(">", " target='%s'>" % target, 1)
            return url
        return ""


    security.declareProtected(ZEN_VIEW, 'getProductLink')
    def getProductLink(self, target=None):
        """
        Return Product Link
        """
        url = self.productClass.getPrimaryLink()
        if target: url = url.replace(">", " target='%s'>" % target, 1)
        return url


    def isUserCreated(self):
        """
        Return True it bay == 0
        """
        return self.bay == -1 and True or False


    def diskImg(self):
        """
        Return disk image filename.
        """
        return '/zport/dmd/smisdisk_%s_%s'%(self.diskType, self.statusDot())


    def bayString(self):
        """
        Return enclosure and bay numbers
        """
        return '%s bay %02d'%(self.getEnclosureName(), int(self.bay))


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size, divby=1000)


    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        return 'Unknown'


    def replaceableString(self):
        """
        Return the HotPlug Status
        """
        return self.replaceable and 'Hot Swappable' or 'Non-Hot Swappable'


    def viewName(self): return self.caption


InitializeClass(SNIADiskDrive)
