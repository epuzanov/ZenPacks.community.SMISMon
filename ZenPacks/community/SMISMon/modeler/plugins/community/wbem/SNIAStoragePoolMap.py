################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStoragePoolMap

SNIAStoragePoolMap maps CIM_StoragePool class to SNIA_StoragePool class.

$Id: SNIAStoragePoolMap.py,v 1.1 2011/09/23 15:59:48 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIAStoragePoolMap(SMISPlugin):
    """Map CIM_StoragePool class to StoragePool"""

    maptype = "SNIAStoragePoolMap"
    modname = "ZenPacks.community.SMISMon.SNIA_StoragePool"
    relname = "storagepools"
    compname = "os"


    def queries(self, device):
        return {
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "InstanceID":"id",
                        "Name":"caption",
                        "PoolID":"poolId",
                        "TotalManagedSpace":"totalManagedSpace",
                        "Usage":"usage",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        for instance in results.get("CIM_StoragePool", []):
            if not instance["id"].startswith(sysname): continue
            if instance["id"].endswith('.Allocated Disks'): continue
            if instance["id"].endswith('.Ungrouped Disks'): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
            except AttributeError:
                continue
            rm.append(om)
        return rm
