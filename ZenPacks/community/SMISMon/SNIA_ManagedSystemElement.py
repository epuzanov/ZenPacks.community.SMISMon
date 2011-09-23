################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIA_ManagedSystemElement

SNIA_ManagedSystemElement is an abstraction for SNIA_ManagedSystemElement class.

$Id: SNIA_ManagedSystemElement.py,v 1.1 2011/09/23 15:53:31 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenossSecurity import *

class SNIA_ManagedSystemElement(object):

    snmpindex = ''
    statindex = ''
    state = 'OK'

    _properties=(
                {'id':'statindex', 'type':'string', 'mode':'w'},
                {'id':'state', 'type':'string', 'mode':'w'},
                )


    def cimInstanceName(self):
        """
        Return the CIM Instance Name
        """
        return self.snmpindex.replace('.', ' WHERE ', 1).replace(',', ' AND ')


    def cimStatInstanceName(self):
        """
        Return the CIM_StatisticalData Instance Name
        """
        return self.statindex.replace('.', ' WHERE ', 1).replace(',', ' AND ')


    def cimClassName(self):
        """
        Return the CIM Class Name
        """
        return self.snmpindex.split('.', 1)[0]


    def cimStatClassName(self):
        """
        Return the CIM_StatisticalData Class Name
        """
        return self.statindex.split('.', 1)[0]


    def cimKeybindings(self):
        """
        Return the CIM Instance Keybindings
        """
        return eval('(lambda **kws:kws)(%s)'%self.snmpindex.split('.', 1)[-1])


    def cimStatKeybindings(self):
        """
        Return the CIM_StatisticalData Instance Keybindings
        """
        return eval('(lambda **kws:kws)(%s)'%self.statindex.split('.', 1)[-1])


    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
        colors = {0:'green',1:'purple',2:'blue',3:'yellow',4:'orange',5:'red'}
        if not self.monitor: return 'grey'
        severity = self.ZenEventManager.getMaxSeverity(self)
        return colors.get(severity, 'grey')


    def statusString(self, status=None):
        """
        Return the status string
        """
        return self.state or 'Unknown'


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        cn = self.cimClassName()
        templates = [self.__class__.__name__]
        if cn and cn != self.__class__.__name__:
            templates.append(cn)
        for i in range(len(templates)):
            templ = self.getRRDTemplateByName(templates.pop(0))
            if templ: templates.append(templ)
        return templates
