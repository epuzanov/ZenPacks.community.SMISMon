################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStorageVolumeMap

SNIAStorageVolumeMap maps CIM_StorageVolume class to SNIA_StorageVolume class.

$Id: SNIAStorageVolumeMap.py,v 1.3 2011/10/04 19:45:56 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIAStorageVolumeMap(SMISPlugin):
    """Map CIM_StorageVolume class to SNIA_StorageVolume"""

    maptype = "StorageVolumeMap"
    modname = "ZenPacks.community.SMISMon.SNIA_StorageVolume"
    relname = "virtualdisks"
    compname = "os"


    def queries(self, device):
        return {
            "CIM_StorageVolume":
                (
                    "SELECT * FROM CIM_StorageVolume",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "Access":"accessType",
                        "Caption":"caption",
                        "BlockSize":"blockSize",
                        'DataRedundancy':'_dr',
                        'DeviceID':'id',
                        'PackageRedundancy':'_pr',
                        "SystemName":"_sname",
                    },
                ),
            "CIM_AllocatedFromStoragePool":
                (
                    "SELECT Antecedent,Dependent FROM CIM_AllocatedFromStoragePool",
                    None,
                    self.prepareCS(device),
                    {
                        "Antecedent":"ant",
                        "Dependent":"dep",
                    },
                ),
            "CIM_MemberOfCollection":
                (
                    "SELECT Collection,Member FROM CIM_MemberOfCollection",
                    None,
                    self.prepareCS(device),
                    {
                        "Collection":"coll", # Collection
                        "Member":"me", # StorageVolume
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

    accessTypes = {
        0: "Unknown",
        1: "Readable",
        2: "Writable",
        3: "Read/Write Supported",
        4: "Write Once",
    }

    raidLevels = {
        (0, 1): 'RAID0',
        (1, 1): 'RAID5',
        (1, 2): 'RAID1+0',
        (2, 1): 'RAID6',
        (2, 2): 'RAID5+1',
    }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        afp = dict([(a["dep"], a["ant"]
                    ) for a in results.get("CIM_AllocatedFromStoragePool", [])])
        rgroup = dict([(a["me"], a["coll"]
                    ) for a in results.get("CIM_MemberOfCollection",[])])
        stats = dict([(s["me"], s["stats"]
                    ) for s in results.get("CIM_ElementStatisticalData", [])])
        for instance in results.get("CIM_StorageVolume", []):
            if sysname not in instance["_sname"]: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om._pr = int(getattr(om, '_pr', 0) or 0)
                om._dr = int(getattr(om, '_dr', 0) or 0)
                if om._dr > 2: om._dr = 2
                om.diskType = self.raidLevels.get((om._pr, om._dr), 'unknown')
                om.accessType = self.accessTypes.get(getattr(om, "accessType",
                                                                0), "Unknown")
                om.setStoragePool = afp.get(om.snmpindex, 'None')
                om.setReplicationGroup = rgroup.get(om.snmpindex, 'None')
                om.statindex = stats.get(om.snmpindex, 'None')
            except AttributeError:
                continue
            rm.append(om)
        return rm
