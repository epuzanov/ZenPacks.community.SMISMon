################################################################################
#
# This program is part of the SNIAMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAFanMap

SNIAFanMap maps CIM_Fan class to Fan class.

$Id: SNIAFanMap.py,v 1.0 2011/09/20 20:30:48 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SMISMon.SMISPlugin import SMISPlugin

class SNIAFanMap(SMISPlugin):
    """Map SNIA_Fan class to Fan class"""

    maptype = "FanMap"
    modname = "ZenPacks.community.SMISMon.SNIA_Fan"
    relname = "fans"
    compname = "hw"


    def queries(self, device):
        return {
            "SNIA_Fan":
                (
                    "SELECT __PATH,__NAMESPACE,ActiveCooling,DeviceID FROM SNIA_Fan",
                    None,
                    self.prepareCS(device),
                    {
                        '__PATH':'setCimPath',
                        'ActiveCooling':'type',
                        'DeviceID':'id',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect SMI-S information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("SNIA_Fan", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            if str(getattr(om, 'type', 'true')).lower() == 'true':
                om.type = 'Active Cooling'
            else:
                om.type = 'Passive Cooling'
            rm.append(om)
        if len(rm.maps) > 0: return rm
        return
