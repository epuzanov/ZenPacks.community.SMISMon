################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_DeviceHW

SNIA_DeviceHW is an abstraction of a SMI-S Hardware

$Id: SNIA_DeviceHW.py,v 1.1 2011/09/23 15:52:04 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenModel.Hardware import Hardware
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class SNIA_DeviceHW(DeviceHW):

    # Define new relationships
    _relations = Hardware._relations + (
        ("cpus", ToManyCont(ToOne, "Products.ZenModel.CPU", "hw")),
        ("cards", ToManyCont(ToOne, "Products.ZenModel.ExpansionCard", "hw")),
        ("harddisks", ToManyCont(ToOne, "ZenPacks.community.SMISMon.SNIA_DiskDrive", "hw")),
        ("fans", ToManyCont(ToOne, "Products.ZenModel.Fan", "hw")),
        ("powersupplies", ToManyCont(ToOne, "Products.ZenModel.PowerSupply",
            "hw")),
        ("temperaturesensors", ToManyCont(ToOne,
            "Products.ZenModel.TemperatureSensor", "hw")),
        ("enclosures", ToManyCont(ToOne,
            "ZenPacks.community.SMISMon.SNIA_EnclosureChassis", "hw")),
        ("ports", ToManyCont(ToOne,
            "ZenPacks.community.SMISMon.SNIA_NetworkPort", "hw")),
    )

    factory_type_information = (
        {
            'id'             : 'Device',
            'meta_type'      : 'Device',
            'description'    : """Base class for all devices""",
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDevice',
            'immediate_view' : 'sniaDeviceHardwareDetail',
            'actions'        : ()
         },
        )

    def __init__(self):
        id = "hw"
        Hardware.__init__(self, id)

InitializeClass(SNIA_DeviceHW)
