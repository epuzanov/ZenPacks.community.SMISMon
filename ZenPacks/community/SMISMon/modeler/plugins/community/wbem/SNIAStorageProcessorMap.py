################################################################################
#
# This program is part of the SNIAMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStorageProcessorMap

SNIAStorageProcessorMap maps SNIA_StorageProcessor class to
SNIAStorageProcessor class.

$Id: SNIA_StorageProcessorMap.py,v 1.1 2011/10/04 19:45:14 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class SNIAStorageProcessorMap(SMISPlugin):
    """Map SNIA_StorageProcessor class to StorageProcessor"""

    maptype = "ExpansionCardMap"
    modname = "ZenPacks.community.SMISMon.SNIA_StorageProcessor"
    relname = "cards"
    compname = "hw"

    def queries(self, device):
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "Name":"caption",
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
        rm = self.relMap()
        sysname = getattr(device,"snmpindex","") or device.id.replace("-","")
        cards = [i.get('pc', '') for i in results.get("CIM_ComponentCS", []
                                                ) if sysname in i.get('gc', '')]
        for instance in results.get("CIM_ComputerSystem", []):
            if instance["snmpindex"] not in cards: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.caption)
            except AttributeError:
                continue
            rm.append(om)
        return rm
