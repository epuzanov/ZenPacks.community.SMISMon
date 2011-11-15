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

SNIADeviceMap maps CIM_ComputerSystem class to hw and os products.

$Id: SNIADeviceMap.py,v 1.2 2011/11/13 23:10:22 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIADeviceMap(SMISPlugin):
    """SNIADeviceMap maps CIM_ComputerSystem class to hw and
       os products.
    """

    maptype = "DeviceMap"
    modname = "ZenPacks.community.SMISMon.SNIADevice" 

    def queries(self, device):
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "Description":"snmpDescr",
                        "Name":"snmpSysName",
                    },
                ),
            "CIM_ComponentCS":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_ComponentCS",
                    None,
                    self.prepareCS(device),
                    {
                        "GroupComponent":"gc", # StorageSystem
                        "PartComponent":"pc", # StorageProcessor
                    },
                ),
            }


    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        sysname = getattr(device,"snmpindex","") or device.id.replace("-","")
        cards = [i.get('pc', '') for i in results.get("CIM_ComponentCS", [])]
        try:
            for cs in results.get("CIM_ComputerSystem", [{}]):
                curSysName = cs.get("snmpindex", "notFound")
                if curSysName in cards: continue
                if sysname in curSysName: return [self.objectMap(cs)]
        except:
            log.warning("processing error")
        return
