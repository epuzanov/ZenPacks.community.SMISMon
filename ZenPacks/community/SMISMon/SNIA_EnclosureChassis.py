################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_EnclosureChassis

SNIA_EnclosureChassis is an abstraction of a CIM_EnclosureChassis

$Id: SNIA_EnclosureChassis.py,v 1.0 2011/09/04 22:45:15 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.SNIA_ManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits

LINKTMPLT='<a href="%s" target="_top"><img src="/zport/dmd/%s_%s_%s.png" /></a>'

class SNIA_EnclosureChassis(HWComponent, SNIA_ManagedSystemElement):
    """ SNIA EnclosureChassis object"""

    portal_type = meta_type = 'SNIA_EnclosureChassis'

    #enclosureLayout = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
    #diskFF = 'sniadisk_lff_v'
    #enclosureLayout = '1 3 5 7 9,2 4 6 8 10'
    enclosureLayout = '0 0 0 0,0 0 0 0,0 0 0 0'
    diskFF = 'sniadisk_lff_h'

    _properties = HWComponent._properties + (
                 {'id':'enclosureLayout', 'type':'string', 'mode':'w'},
                 {'id':'diskFF', 'type':'boolean', 'mode':'w'},
                ) + SNIA_ManagedSystemElement._properties

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                    "ZenPacks.community.SMISMon.SNIA_DeviceHW",
                    "enclosures")),
        ("harddisks", ToMany(ToOne,
                    "ZenPacks.community.SMISMon.SNIA_DiskDrive",
                    "enclosure")),
        )

    factory_type_information = (
        {
            'id'             : 'SNIA_EnclosureChassis',
            'meta_type'      : 'SNIA_EnclosureChassis',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'EnclosureChassis_icon.gif',
            'product'        : 'SMISMon',
            'factory'        : 'manage_addEnclosureChassis',
            'immediate_view' : 'viewSNIAEnclosureChassis',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAEnclosureChassis'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'layout'
                , 'name'          : 'Layout'
                , 'action'        : 'viewSNIAEnclosureChassisLayout'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewSNIAEnclosureChassisDisks'
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

    def isUserCreated(self):
        """
        Return True if layout not detected
        """
        return self.enclosureLayout=='0 0 0 0,0 0 0 0,0 0 0 0' and True or False


    def getStatus(self):
        """
        Return the components status
        """
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))


    def layout(self):
        """
        Build Disk Enclosure layout
        """
        bays = {}
        for disk in self.harddisks() or []:
            bays[str(disk.bay)] = LINKTMPLT % ( disk.getPrimaryUrlPath(),
                                self.diskFF, disk.diskType, disk.statusDot())
        return '<table border="0">\n<tr>\n<td>%s\n</td>\n</tr>\n</table>\n'%(
            '</td>\n</tr>\n<tr>\n<td>'.join(['</td>\n<td>'.join([bays.get(b,
            '<img src="/zport/dmd/%s_blank.png" />'%self.diskFF) \
            for b in l.split(' ')]) for l in self.enclosureLayout.split(',')]))

    def getRRDNames(self):
        """
        Return the datapoint name of this EnclosureChassis
        """
        return ['EnclosureChassis_OperationalStatus']


InitializeClass(SNIA_EnclosureChassis)
