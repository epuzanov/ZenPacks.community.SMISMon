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

$Id: info.py,v 1.3 2011/10/12 22:02:10 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from zope.interface import implements
from ZenPacks.community.SMISMon import interfaces
from ZenPacks.community.SMISMon.infos import *


class SNIA_DiskDriveInfo(DiskDriveInfo):
    implements(interfaces.IDiskDriveInfo)


class SNIA_NetworkPortInfo(NetworkPortInfo):
    implements(interfaces.INetworkPortInfo)


class SNIA_EnclosureChassisInfo(EnclosureChassisInfo):
    implements(interfaces.IEnclosureChassisInfo)


class SNIA_StoragePoolInfo(StoragePoolInfo):
    implements(interfaces.IStoragePoolInfo)


class SNIA_StorageProcessorInfo(StorageProcessorInfo):
    implements(interfaces.IStorageProcessorInfo)


class SNIA_StorageVolumeInfo(StorageVolumeInfo):
    implements(interfaces.IStorageVolumeInfo)


class SNIA_ReplicationGroupInfo(ReplicationGroupInfo):
    implements(interfaces.IReplicationGroupInfo)
