################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIADevice

SNIADevice is an abstraction of a SMI-S Device

$Id: SNIADevice.py,v 1.3 2011/11/13 22:51:45 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import InitializeClass
from distutils.version import StrictVersion
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_DEVICE
from Products.ZenModel.Device import Device
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenStatus import ZenStatus
from Products.ZenModel.ZVersion import VERSION
from ZenPacks.community.SMISMon.SNIADeviceHW import SNIADeviceHW
from ZenPacks.community.SMISMon.SNIADeviceOS import SNIADeviceOS

IMM_VIEW = StrictVersion(VERSION) < '2.6' and 'deviceStatus' or 'devicedetail'

class SNIADevice(Device):

    def __init__(self, id, buildRelations=True):
        ManagedEntity.__init__(self, id, buildRelations=buildRelations)
        os = SNIADeviceOS()
        self._setObject(os.id, os)
        hw = SNIADeviceHW()
        self._setObject(hw.id, hw)
        self._lastPollSnmpUpTime = ZenStatus(0)
        self._snmpLastCollection = 0
        self._lastChange = 0
        self.buildRelations()

    factory_type_information = (
        {
            'immediate_view': IMM_VIEW,
            'actions'       :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'deviceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'sniaDeviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'sniaDeviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfServer'
                , 'name'          : 'Perf'
                , 'action'        : 'viewDevicePerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit'
                , 'action'        : 'editDevice'
                , 'permissions'   : (ZEN_CHANGE_DEVICE,)
                },
            )
         },
        )

    def cimInstanceName(self):
        """
        Return the CIM Instance Name
        """
        return self.snmpindex.replace('.', ' WHERE ', 1).replace(',', ' AND ')

InitializeClass(SNIADevice)

