################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIANetworkPort

SNIANetworkPort is an abstraction of a CIM_NetworkPort

$Id: SNIANetworkPort.py,v 1.2 2011/11/13 22:55:26 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.SMISMon.CIMManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits

import logging
log = logging.getLogger("zen.SNIANetworkPort")

class SNIANetworkPort(HWComponent, CIMManagedSystemElement):
    """SNIA NetworkPort object"""

    portal_type = meta_type = 'NetworkPort'

    interfaceName = ""
    fullDuplex = True
    linkTechnology = ""
    networkAddresses = []
    type = ""
    description = ""
    speed = 0
    mtu = 0
    mac = ""

    _properties = HWComponent._properties + (
                 {'id':'interfaceName', 'type':'string', 'mode':'w'},
                 {'id':'fullDuplex', 'type':'boolean', 'mode':'w'},
                 {'id':'linkTechnology', 'type':'string', 'mode':'w'},
                 {'id':'networkAddresses', 'type':'lines', 'mode':'w'},
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'speed', 'type':'int', 'mode':'w'},
                 {'id':'mtu', 'type':'int', 'mode':'w'},
                 {'id':'mac', 'type':'string', 'mode':'w'},
                ) + CIMManagedSystemElement._properties


    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                    "ZenPacks.community.SMISMon.SNIADeviceHW",
                    "ports")),
        ("controller", ToOne(ToMany,
                    "ZenPacks.community.SMISMon.SNIAStorageProcessor",
                    "ports")),
        )


    factory_type_information = (
        {
            'id'             : 'NetworkPort',
            'meta_type'      : 'NetworkPort',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'NetworkPort_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addNetworkPort',
            'immediate_view' : 'viewSNIANetworkPort',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSNIANetworkPort'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
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


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setController')
    def setController(self, cid):
        """
        Set the controller relationship to the Controller specified by the given
        id.
        """
        for cntrl in self.hw().cards() or []:
            if cntrl.snmpindex != cid: continue
            self.controller.addRelation(cntrl)
            break


    security.declareProtected(ZEN_VIEW, 'getController')
    def getController(self):
        return self.controller()


    def speedString(self):
        """
        Return the speed in human readable form ie 10MB
        """
        return convToUnits(self.speed, divby=1024)


    def networkString(self):
        """
        Return the networks string
        """
        if self.networkAddresses: return '<br>'.join(self.networkAddresses)
        else: return 'Unknown'


    def macString(self):
        """
        Return the mac string
        """
        if len(str(self.mac)) < 15: return ''
        return '-'.join([self.mac[s*4:s*4+4] for s in range(4)])


    def viewName(self): return self.caption


InitializeClass(SNIANetworkPort)
