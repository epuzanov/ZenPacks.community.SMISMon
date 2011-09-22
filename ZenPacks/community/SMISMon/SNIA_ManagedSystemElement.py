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

$Id: SNIA_ManagedSystemElement.py,v 1.0 2011/09/04 22:35:14 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenossSecurity import *

class SNIA_ManagedSystemElement(object):

    cimNamespace = 'root/cimv2'
    cimClassName = ''
    cimKeybindings = ''
    cimStatClassName = ''
    cimStatKeybindings = ''
    state = 'OK'

    _properties = (
                 {'id':'cimNamespace', 'type':'string', 'mode':'w'},
                 {'id':'cimClassName', 'type':'string', 'mode':'w'},
                 {'id':'cimKeybindings', 'type':'string', 'mode':'w'},
                 {'id':'cimStatClassName', 'type':'string', 'mode':'w'},
                 {'id':'cimStatKeybindings', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )

    security = ClassSecurityInfo()


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setCimPath')
    def setCimPath(self, path):
        """
        Set cimClassName and cimKeybindings attributes
        """
        self.cimClassName, self.cimKeybindings = path.split('.', 1)


    security.declareProtected(ZEN_VIEW, 'getCimPath')
    def getCimPath(self):
        """
        Return CIM instance __PATH attribute
        """
        return '.'.join((self.cimClassName, self.cimKeybindings))


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setCimStatPath')
    def setCimStatPath(self, path):
        """
        Set cimStatClassName and cimStatKeybindings attributes
        """
        self.cimStatClassName, self.cimStatKeybindings = path.split('.', 1)


    security.declareProtected(ZEN_VIEW, 'getCimStatPath')
    def getCimStatPath(self):
        """
        Return CIM_StatisticalData instance __PATH attribute
        """
        return '.'.join((self.cimStatClassName, self.cimStatKeybindings))


    def cimInstanceName(self):
        """
        Return the CIM Instance Name
        """
        return '%s WHERE %s' % (self.cimClassName,
                                self.cimKeybindings.replace(',',' AND '))


    def cimStatInstanceName(self):
        """
        Return the CIM_StatisticalData Instance Name
        """
        return '%s WHERE %s' % (self.cimStatClassName,
                                self.cimStatKeybindings.replace(',',' AND '))


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
        templates = [self.__class__.__name__]
        if self.cimClassName and self.cimClassName != self.__class__.__name__:
            templates.append(self.cimClassName)
        for i in range(len(templates)):
            templ = self.getRRDTemplateByName(templates.pop(0))
            if templ: templates.append(templ)
        return templates
