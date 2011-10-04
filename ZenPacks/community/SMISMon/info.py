################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of SNIA components.

$Id: info.py,v 1.2 2011/10/04 22:09:38 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.SMISMon import interfaces


class SNIA_DiskDriveInfo(ComponentInfo):
    implements(interfaces.ISNIA_DiskDriveInfo)

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
        return self._object.description

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class SNIA_NetworkPortInfo(ComponentInfo):
    implements(interfaces.ISNIA_NetworkPortInfo)

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

class SNIA_EnclosureChassisInfo(ComponentInfo):
    implements(interfaces.ISNIA_EnclosureChassisInfo)

    enclosureLayout = ProxyProperty("enclosureLayout")
    diskFF = ProxyProperty("diskFF")

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

class SNIA_StoragePoolInfo(ComponentInfo):
    implements(interfaces.ISNIA_StoragePoolInfo)

    @property
    def name(self):
        return self._object.caption

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

class SNIA_StorageProcessorInfo(ComponentInfo):
    implements(interfaces.ISNIA_StorageProcessorInfo)

    slot = ProxyProperty("slot")
    serialNumber = ProxyProperty("serialNumber")
    FWRev = ProxyProperty("FWRev")

    @property
    def name(self):
        return self._object.caption

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

class SNIA_StorageVolumeInfo(ComponentInfo):
    implements(interfaces.ISNIA_StorageVolumeInfo)

    accessType = ProxyProperty("accessType")
    diskType = ProxyProperty("diskType")

    @property
    def name(self):
        return self._object.caption

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

class SNIA_ReplicationGroupInfo(ComponentInfo):
    implements(interfaces.ISNIA_ReplicationGroupInfo)

    @property
    def name(self):
        return self._object.caption

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

