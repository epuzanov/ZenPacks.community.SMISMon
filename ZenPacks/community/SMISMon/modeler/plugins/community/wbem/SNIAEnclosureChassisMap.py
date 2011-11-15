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

SNIAEnclosureChassisMap maps CIM_Chassis class to SNIAEnclosureChassis class.

$Id: SNIAEnclosureChassisMap.py,v 1.5 2011/11/13 23:13:36 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class SNIAEnclosureChassisMap(SMISPlugin):
    """Map CIM_Chassis class to Storage Enclosure"""

    maptype = "EnclosureChassisMap"
    modname = "ZenPacks.community.SMISMon.SNIAEnclosureChassis"
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
                        "ElementName":"caption",
                        "Manufacturer":"_manuf",
                        "Model":"setProductKey",
                        "SerialNumber":"serialNumber",
                        "PartNumber":"_pn",
                        "Tag":"id",
                    },
                ),
            }


    def _enclosureLayout(self, instance):
        return None


    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        for instance in results.get("CIM_Chassis", []):
            if sysname not in instance["id"]: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if not om._manuf: om._manuf = "Unknown"
                if om.setProductKey:
                    om.setProductKey = MultiArgs(om.setProductKey, om._manuf)
                enclosureLayout = self._enclosureLayout(instance)
                if enclosureLayout:
                    om.enclosureLayout, om.diskFF = enclosureLayout
            except AttributeError:
                continue
            rm.append(om)
        return rm
