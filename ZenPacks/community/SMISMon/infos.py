################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""infos.py

Representation of SNIA components.

$Id: infos.py,v 1.1 2011/11/13 23:33:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits


class DiskDriveInfo(ComponentInfo):

    serialNumber = ProxyProperty("serialNumber")
    diskType = ProxyProperty("diskType")
    FWRev = ProxyProperty("FWRev")
    bay = ProxyProperty("bay")

    @property
    def size(self):
        return convToUnits(self._object.size, divby=1000)

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    @info
    def enclosure(self):
        return self._object.getEnclosure()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def name(self):
        return self._object.viewName()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class NetworkPortInfo(ComponentInfo):

    fullDuplex = ProxyProperty("fullDuplex")
    linkTechnology = ProxyProperty("linkTechnology")
    networkAddresses = ProxyProperty("networkAddresses")
    type = ProxyProperty("type")
    description = ProxyProperty("description")
    mtu = ProxyProperty("mtu")

    @property
    def mac(self):
        if not self._object.mac: return ''
        else: return '-'.join([self._object.mac[s*4:s*4+4] for s in range(4)])

    @property
    def name(self):
        return self._object.interfaceName

    @property
    def speed(self):
        return self._object.speedString()

    @property
    @info
    def controller(self):
        return self._object.getController()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class EnclosureChassisInfo(ComponentInfo):

    enclosureLayout = ProxyProperty("enclosureLayout")
    diskFF = ProxyProperty("diskFF")

    @property
    def name(self):
        return self._object.viewName()

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class StoragePoolInfo(ComponentInfo):

    @property
    def name(self):
        return self._object.viewName()

    @property
    def totalDisks(self):
        return self._object.totalDisks()

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    def usedBytesString(self):
        return self._object.usedBytesString()

    @property
    def availBytesString(self):
        return self._object.availBytesString()

    @property
    def capacity(self):
        capacity = self._object.capacity()
        if str(capacity).isdigit():
            capacity = '%s%%'%capacity
        return capacity

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class StorageProcessorInfo(ComponentInfo):

    slot = ProxyProperty("slot")
    serialNumber = ProxyProperty("serialNumber")
    FWRev = ProxyProperty("FWRev")

    @property
    def name(self):
        return self._object.viewName()

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def uptime(self):
        return self._object.uptimeString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class StorageVolumeInfo(ComponentInfo):

    accessType = ProxyProperty("accessType")
    diskType = ProxyProperty("diskType")

    @property
    def name(self):
        return self._object.viewName()

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class ReplicationGroupInfo(ComponentInfo):

    @property
    def name(self):
        return self._object.viewName()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()
