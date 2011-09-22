################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIADeviceMap

SNIADeviceMap maps CIM_StorageSystem class to hw and
os products.

$Id: SNIADeviceMap.py,v 1.0 2011/09/04 22:49:18 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIADeviceMap(SMISPlugin):
    """SNIADeviceMap maps CIM_StorageSystem class to hw and
       os products.
    """

    maptype = "DeviceMap"
    modname = "ZenPacks.community.SMISMon.SNIA_Device" 

    def queries(self, device):
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    self.prepareCS(device),
                    {
                        "CreationClassName":"snmpOid",
                        "Description":"snmpDescr",
                        "Name":"snmpSysName",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        try:
            cs = None
            for cs in results.get("CIM_ComputerSystem", [{}]):
                sysname = device.snmpSysName or device.id.replace("-","")
                if sysname == cs.get('snmpSysName', ''): break
            if not cs: return
            maps = []
            om = self.objectMap(cs)
            maps.append(om)
        except:
            log.warning("processing error")
            return
        return maps
