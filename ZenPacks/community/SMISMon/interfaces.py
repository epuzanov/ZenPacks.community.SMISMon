################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.4 2011/11/13 23:08:52 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IDiskDriveInfo(IComponentInfo):
    """
    Info adapter for SNIA Disk Drive components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    name = schema.Text(title=u"Name", readonly=True, group='Details')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    size = schema.Text(title=u"Size", readonly=True, group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    enclosure = schema.Entity(title=u"Enclosure", readonly=True,group='Details')
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    bay = schema.Int(title=u"Bay", readonly=False, group='Details')

class INetworkPortInfo(IComponentInfo):
    """
    Info adapter for SNIA Network Port components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    name = schema.Text(title=u"Interface Name", readonly=True, group='Overview')
    controller = schema.Entity(title=u"Storage Controller", readonly=True,
                                                                group='Details')
    fullDuplex = schema.Bool(title=u"Duplex", readonly=True, group='Details')
    linkTechnology = schema.Text(title=u"Link Technology", readonly=True,
                                                                group='Details')
    networkAddresses = schema.List(title=u"Network", readonly=True,
                                                                group='Details')
    type = schema.Text(title=u"Type", readonly=True, group='Details')
    speed = schema.Text(title=u"Speed", readonly=True, group='Details')
    mtu = schema.Int(title=u"MTU", readonly=True, group='Details')
    mac = schema.Text(title=u"MAC", readonly=True, group='Details')

class IEnclosureChassisInfo(IComponentInfo):
    """
    Info adapter for SNIA Enclosure Chassis components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    enclosureLayout = schema.Text(title=u"Layout String", readonly=False,
                                                                group='Details')
    diskFF = schema.Text(title=u"Disks form factor", readonly=False,
                                                                group='Details')

class IStoragePoolInfo(IComponentInfo):
    """
    Info adapter for SNIA Storage Pool components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    totalDisks = schema.Int(title=u"Total Disk", readonly=True, group="Details")
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")
    usedBytesString = schema.Text(title=u"Used Bytes", readonly=True,
                                                                group="Details")
    availBytesString = schema.Text(title=u"Available Bytes", readonly=True,
                                                                group="Details")
    capacity = schema.Text(title=u"Utilization", readonly=True, group="Details")

class IStorageProcessorInfo(IComponentInfo):
    """
    Info adapter for SNIA Storage Processor components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    uptime = schema.Text(title=u"Uptime", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,
                                                                group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')

class IStorageVolumeInfo(IComponentInfo):
    """
    Info adapter for SNIA Storage Volume components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    accessType = schema.Text(title=u"Access Type", readonly=True,
                                                                group='Details')
    diskType = schema.Text(title=u"Disk Type", readonly=True, group='Details')
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")

class IReplicationGroupInfo(IComponentInfo):
    """
    Info adapter for SNIA Replication Group components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
