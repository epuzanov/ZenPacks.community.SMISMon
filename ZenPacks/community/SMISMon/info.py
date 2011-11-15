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

$Id: info.py,v 1.4 2011/11/13 23:02:47 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from ZenPacks.community.SMISMon import interfaces
from ZenPacks.community.SMISMon.infos import *


class SNIADiskDriveInfo(DiskDriveInfo):
    implements(interfaces.IDiskDriveInfo)


class SNIANetworkPortInfo(NetworkPortInfo):
    implements(interfaces.INetworkPortInfo)


class SNIAEnclosureChassisInfo(EnclosureChassisInfo):
    implements(interfaces.IEnclosureChassisInfo)


class SNIAStoragePoolInfo(StoragePoolInfo):
    implements(interfaces.IStoragePoolInfo)


class SNIAStorageProcessorInfo(StorageProcessorInfo):
    implements(interfaces.IStorageProcessorInfo)


class SNIAStorageVolumeInfo(StorageVolumeInfo):
    implements(interfaces.IStorageVolumeInfo)


class SNIAReplicationGroupInfo(ReplicationGroupInfo):
    implements(interfaces.IReplicationGroupInfo)
