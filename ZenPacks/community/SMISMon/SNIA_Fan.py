################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_Fan

SNIA_Fan is an abstraction of a Fan.

$Id: SNIA_Fan.py,v 1.0 2011/09/04 22:46:46 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import Fan
from ZenPacks.community.SMISMon.SNIA_ManagedSystemElement import *

class SNIA_Fan(Fan, SNIA_ManagedSystemElement):
    """SNIA_Fan object"""

    _properties = Fan._properties + SNIA_ManagedSystemElement._properties

    def rpmString(self, default=None):
        """
        Return a string representation of the RPM
        """
        return self.getStatus() == 0 and 'Normal' or 'unknown'

    getRRDTemplates = SNIA_ManagedSystemElement.getRRDTemplates

InitializeClass(SNIA_Fan)
