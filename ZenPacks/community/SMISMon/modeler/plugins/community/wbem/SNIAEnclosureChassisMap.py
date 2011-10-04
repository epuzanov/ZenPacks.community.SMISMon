################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAEnclosureChassisMap

SNIAEnclosureChassisMap maps CIM_Chassis class to SNIA_EnclosureChassis class.

$Id: SNIAEnclosureChassisMap.py,v 1.3 2011/10/04 19:44:15 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class SNIAEnclosureChassisMap(SMISPlugin):
    """Map CIM_Chassis class to Storage Enclosure"""

    maptype = "EnclosureChassisMap"
    modname = "ZenPacks.community.SMISMon.SNIA_EnclosureChassis"
    relname = "enclosures"
    compname = "hw"


    def queries(self, device):
        return {
            "CIM_Chassis":
                (
                    "SELECT * FROM CIM_Chassis",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "ChassisPackageType":"_cptype",
                        "Manufacturer":"_manuf",
                        "Model":"setProductKey",
                        "SerialNumber":"serialNumber",
                        "Tag":"id",
                    },
                ),
            "CIM_ComputerSystemPackage":
                (
                    "SELECT Antecedent,Dependent FROM CIM_ComputerSystemPackage",
                    None,
                    self.prepareCS(device),
                    {
                        "Antecedent":"ant", # Chassis
                        "Dependent":"dep", # System
                    },
                ),
            }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpindex","") or device.id.replace("-","")
        localchassis = [d["ant"] for d in results.get(
                        "CIM_ComputerSystemPackage",[]) if sysname in d["dep"]]
        for instance in results.get("CIM_Chassis", []):
            if instance["snmpindex"] not in localchassis: continue
#            if str(instance["_cptype"]) != '22': continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if not om._manuf: om._manuf = "Unknown"
                if om.setProductKey:
                    om.setProductKey = MultiArgs(om.setProductKey, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
