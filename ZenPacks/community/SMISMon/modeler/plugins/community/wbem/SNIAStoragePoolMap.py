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

$Id: SNIAStoragePoolMap.py,v 1.2 2011/09/30 18:43:45 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIAStoragePoolMap(SMISPlugin):
    """Map CIM_StoragePool class to StoragePool"""

    maptype = "StoragePoolMap"
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
                        "Primordial":"_primordial",
                        "TotalManagedSpace":"totalManagedSpace",
                        "Usage":"usage",
                    },
                ),
            "CIM_HostedStoragePool":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_HostedStoragePool",
                    None,
                    self.prepareCS(device),
                    {
                        "GroupComponent":"gc", # SysName
                        "PartComponent":"pc", # StoragePool
                    },
                ),
            }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpindex","") or device.id.replace("-","")
        localpools = [p["pc"] for p in results.get("CIM_HostedStoragePool",
                                                    []) if sysname in p["gc"]]
        for instance in results.get("CIM_StoragePool", []):
            if instance["snmpindex"] not in localpools: continue
            if 'rimordial' in instance["snmpindex"]: continue
            if instance.get("_primordial", False): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
            except AttributeError:
                continue
            rm.append(om)
        return rm
