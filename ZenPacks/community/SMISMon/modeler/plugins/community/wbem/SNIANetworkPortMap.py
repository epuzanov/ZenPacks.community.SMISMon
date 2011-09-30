################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIANetworkPortMap

SNIANetworkPortMap maps CIM_NetworkPort class to SNIA_NetworkPort class.

$Id: SNIANetworkPortMap.py,v 1.2 2011/09/30 18:42:47 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class SNIANetworkPortMap(SMISPlugin):
    """Map CIM_NetworkPort class to NetworkPort"""

    maptype = "NetworkPortMap"
    modname = "ZenPacks.community.SMISMon.SNIA_NetworkPort"
    relname = "ports"
    compname = "hw"


    def queries(self, device):
        return {
            "CIM_NetworkPort":
                (
                    "SELECT * FROM CIM_NetworkPort",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"snmpindex",
                        "Description":"description",
                        "DeviceID":"id",
                        "Caption":"interfaceName",
                        "FullDuplex":"fullDuplex",
                        "LinkTechnology":"linkTechnology",
                        "NetworkAddresses":"networkAddresses",
                        "PermanentAddress":"mac",
                        "PortType":"type",
                        "Speed":"speed",
                        "SupportedMaximumTransmissionUnit":"mtu",
                        "SystemName":"_sname",
                    },
                ),
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    self.prepareCS(device),
                    {
                        "__PATH":"i",
                        "Name":"n",
                    }
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

    linkTypes = {
        0:'Unknown',
        1: 'Other',
        2: 'Ethernet',
        3: 'IB',
        4: 'FC',
        5: 'FDDI',
        6: 'ATM',
        7: 'Token Ring',
        8: 'Frame Relay',
        9: 'Infrared',
        10: 'Bluetooth',
        11: 'Wireless LAN',
    }

    portTypes = {
        0: "Unknown",
        1: "Other",
        10: "N",
        11: "NL",
        12: "F/NL",
        13: "Nx",
        14: "E",
        15: "F",
        16: "FL",
        17: "B",
        18: "G",
        94: "SAS",
    }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        cs=dict([(c['n'],c['i']) for c in results.get("CIM_ComputerSystem",[])])
        stats = dict([(s["me"], s["stats"]
                    ) for s in results.get("CIM_ElementStatisticalData", [])])
        for instance in results.get("CIM_NetworkPort", []):
            if sysname not in instance["_sname"]: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if om._sname: om.setController = cs.get(om._sname, 'None')
                if om.interfaceName:om.interfaceName=om.interfaceName.split()[-1]
                om.type = self.portTypes.get(getattr(om, "type", 0), "Unknown")
                om.linkTechnology = self.linkTypes.get(getattr(om,
                                            "linkTechnology", 0), "Unknown")
                om.statindex = stats.get(om.snmpindex, 'None')
            except AttributeError:
                continue
            rm.append(om)
        return rm
