################################################################################
#
# This program is part of the SNIAMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAReplicationGroupMap

SNIAReplicationGroupMap maps SNIA_ReplicationGroup class to
SNIAReplicationGroup class.

$Id: SNIA_ReplicationGroupMap.py,v 1.0 2011/09/30 18:43:17 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class SNIAReplicationGroupMap(SMISPlugin):
    """Map SNIA_ReplicationGroup class to ReplicationGroup"""

    maptype = "ReplicationGroupMap"
    modname = "ZenPacks.community.SNIAMon.SNIAReplicationGroup"
    relname = "collections"
    compname = "os"

    def queries(self, device):
        return {
            "CIM_SystemSpecificCollection":
                (
                    "SELECT * FROM CIM_SystemSpecificCollection",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "ElementName":"caption",
                    },
                ),
            "CIM_HostedCollection":
                (
                    "SELECT Antecedent,Dependent FROM CIM_HostedCollection",
                    None,
                    self.prepareCS(device),
                    {
                        "Antecedent":"ant", # System
                        "Dependent":"dep", # Collection
                    },
                ),
            }


    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpindex","") or device.id.replace("-","")
        colls = [c.get('dep', '') for c in results.get("CIM_HostedCollection",[]
                                                ) if sysname in i.get('ant','')]
        for instance in results.get("CIM_SystemSpecificCollection", []):
            if instance["snmpindex"] not in colls: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.caption)
            except AttributeError:
                continue
            rm.append(om)
        return rm
