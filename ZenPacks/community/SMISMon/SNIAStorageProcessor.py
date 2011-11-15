################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStorageProcessor

SNIAStorageProcessor is an abstraction of a CIM_StorageProcessor

$Id: SNIAStorageProcessor.py,v 1.1 2011/11/13 22:59:47 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ExpansionCard import ExpansionCard
from Products.ZenRelations.RelSchema import ToOne, ToMany
from ZenPacks.community.SMISMon.CIMManagedSystemElement import *

class SNIAStorageProcessor(ExpansionCard, CIMManagedSystemElement):
    """SNIA StorageProcessor object"""

    portal_type = meta_type = 'StorageProcessor'


    caption = ""
    FWRev = 0

    monitor = True

    _properties = ExpansionCard._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                ) + CIMManagedSystemElement._properties

    _relations = ExpansionCard._relations + (
        ("ports", ToMany(ToOne,
                    "ZenPacks.community.SMISMon.SNIANetworkPort",
                    "controller")),
        )

    factory_type_information = (
        {
            'id'             : 'SNIAStorageProcessor',
            'meta_type'      : 'SNIAStorageProcessor',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageProcessor_icon.gif',
            'product'        : 'SMISMon',
            'factory'        : 'manage_addExpansion',
            'immediate_view' : 'viewSNIAStorageProcessor',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIAStorageProcessor'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'fcports'
                , 'name'          : 'FC Ports'
                , 'action'        : 'viewSNIAStorageProcessorPorts'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    security = ClassSecurityInfo()


    getRRDTemplates = CIMManagedSystemElement.getRRDTemplates


    security.declareProtected(ZEN_VIEW, 'getManufacturerLink')
    def getManufacturerLink(self, target=None):
        if self.productClass():
            url = self.productClass().manufacturer.getPrimaryLink()
            if target: url = url.replace(">", " target='%s'>" % target, 1)
            return url
        return ""


    security.declareProtected(ZEN_VIEW, 'getProductLink')
    def getProductLink(self, target=None):
        url = self.productClass.getPrimaryLink()
        if target: url = url.replace(">", " target='%s'>" % target, 1)
        return url


    def sysUpTime(self):
        """
        Return the controllers UpTime
        """
        cpuUpTime = round(self.cacheRRDValue('cpuUpTime', -1))
        if cpuUpTime == -1: return -1
        return cpuUpTime / 10


    def uptimeString(self):
        """
        Return the controllers uptime string

        @rtype: string
        @permission: ZEN_VIEW
        """
        ut = self.sysUpTime()
        if ut < 0:
            return "Unknown"
        elif ut == 0:
            return "0d:0h:0m:0s"
        ut = float(ut)/100.
        days = ut/86400
        hour = (ut%86400)/3600
        mins = (ut%3600)/60
        secs = ut%60
        return "%02dd:%02dh:%02dm:%02ds" % (
            days, hour, mins, secs)


    def getRRDNames(self):
        """
        Return the datapoint name of this StorageProcessor
        """
        return ['StorageProcessor_cpuUpTime']


    def viewName(self): return self.caption


InitializeClass(SNIAStorageProcessor)
