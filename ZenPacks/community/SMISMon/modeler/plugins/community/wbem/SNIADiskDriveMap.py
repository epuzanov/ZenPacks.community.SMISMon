################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIADiskDriveMap

SNIADiskDriveMap maps CIM_DiskDrive class to HardDisk class.

$Id: SNAIDiskDriveMap.py,v 1.4 2011/10/04 22:12:54 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs

class SNIADiskDriveMap(SMISPlugin):
    """Map CIM_DiskDrive class to HardDisk"""

    maptype = "HardDiskMap"
    modname = "ZenPacks.community.SMISMon.SNIA_DiskDrive"
    relname = "harddisks"
    compname = "hw"


    def queries(self, device):
        return {
            "CIM_DiskDrive":
                (
                    "SELECT * FROM CIM_DiskDrive",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "DeviceID":"id",
                        "MaxMediaSize":"size",
                        "Name":"_name",
                        "SystemName":"_sname",
                    },
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT * FROM CIM_PhysicalPackage",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"_path",
                        "Manufacturer":"_manuf",
                        "Model":"setProductKey",
                        "Name":"description",
                        "Replaceable":"replaceable",
                        "SerialNumber":"serialNumber",
                        "Version":"FWRev",
                    },
                ),
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"_path",
                        "Primordial":"_primordial",
                    },
                ),
            "CIM_Realizes":
                (
                    "SELECT Antecedent,Dependent FROM CIM_Realizes",
                    None,
                    self.prepareCS(device),
                    {
                        "Antecedent":"ant", # PhysicalPackage
                        "Dependent":"dep", # DiskDrive
                    },
                ),
            "CIM_PackageInChassis":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_PackageInChassis",
                    None,
                    self.prepareCS(device),
                    {
                        "GroupComponent":"gc", # Enclosure
                        "PartComponent":"pc", # PhysicalPackage
                    },
                ),
            "CIM_ConcreteComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_ConcreteComponent",
                    None,
                    self.prepareCS(device),
                    {
                        "GroupComponent":"gc", # StoragePool
                        "PartComponent":"pc", # DiskExtent
                    },
                ),
            "CIM_MediaPresent":
                (
                    "SELECT Antecedent,Dependent FROM CIM_MediaPresent",
                    None,
                    self.prepareCS(device),
                    {
                        "Antecedent":"ant", # DiskDrive
                        "Dependent":"dep", # DiskExtent
                    },
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT ManagedElement,Stats FROM CIM_ElementStatisticalData",
                    None,
                    self.prepareCS(device),
                    {
                        "ManagedElement":"me",
                        "Stats":"stats",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        pp=dict([(p["_path"],p) for p in results.get("CIM_PhysicalPackage",[])])
        packages = dict([(a["dep"], pp.get(a["ant"], {})) for a in results.get(
                                                            "CIM_Realizes",[])])
        enclosures = dict([(a["pc"], a["gc"]) for a in results.get(
                                                    "CIM_PackageInChassis",[])])
        ppools = [a["_path"] for a in results.get("CIM_StoragePool", []
                    ) if a.get("_primordial",True) or "rimordial" in a["_path"]]
        cc=dict([(a["pc"],a["gc"]) for a in results.get("CIM_ConcreteComponent",
                                        []) if a["gc"] not in ppools])
        spools = dict([(a["ant"], cc.get(a["dep"], {})
                        ) for a in results.get("CIM_MediaPresent", [])])
        stats = dict([(s["me"], s["stats"]
                    ) for s in results.get("CIM_ElementStatisticalData", [])])
        for instance in results.get("CIM_DiskDrive", []):
            if sysname not in instance["_sname"]: continue
            try:
                instance.update(packages.get(instance["snmpindex"], {}))
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om.size = int(getattr(om, 'size', 0)) * 1000
                om._manuf = getattr(om, '_manuf', '') or 'Unknown'
                om.setProductKey = MultiArgs(
                    getattr(om, 'setProductKey', '') or 'Unknown', om._manuf)
                om.setEnclosure = enclosures.get(getattr(om, '_path', 'None'))
                om.setStoragePool = spools.get(getattr(om, 'snmpindex', 'None'))
                om.statindex = stats.get(om.snmpindex, 'None')
            except AttributeError:
                raise
            rm.append(om)
        return rm
