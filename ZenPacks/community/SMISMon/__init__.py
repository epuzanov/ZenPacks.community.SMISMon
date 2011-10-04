
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass


class ZenPack(ZenPackBase):
    """ SMISMon loader
    """

    packZProperties = [(
        'zSNIAConnectionString',
        "'pywbemdb',scheme='https',port=5989,host='localhost',namespace='root/eva'",
        'string')]

    dcProperties = {
        '/Storage/SMI-S': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.wbem.SNIADeviceMap',
                'community.wbem.SNIAEnclosureChassisMap',
                'community.wbem.SNIAStorageProcessorMap',
                'community.wbem.SNIAStoragePoolMap',
                'community.wbem.SNIAReplicationGroupMap',
                'community.wbem.SNIANetworkPortMap',
                'community.wbem.SNIADiskDriveMap',
                'community.wbem.SNIAStorageVolumeMap',
                ),
                'lines',
            ),
            'zPythonClass': ('ZenPacks.community.SMISMon.SNIA_Device', 'string'),
            'zSnmpMonitorIgnore': (True, 'boolean'),
        },
    }

    def addDeviceClass(self, app, dcp, properties):
        try:
            dc = app.zport.dmd.Devices.getOrganizer(dcp)
        except:
            dcp, newdcp = dcp.rsplit('/', 1)
            dc = self.addDeviceClass(app, dcp, self.dcProperties.get(dcp, {}))
            manage_addDeviceClass(dc, newdcp)
            dc = app.zport.dmd.Devices.getOrganizer("%s/%s"%(dcp, newdcp))
            dc.description = ''
        for prop, value in properties.iteritems():
            if not hasattr(aq_base(dc), prop):
                dc._setProperty(prop, value[0], type = value[1])
        return dc

    def install(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
            if not hasattr(devReports, 'SMI-S Reports'):
                dc = rClass('SMI-S Reports', None)
                devReports._setObject('SMI-S Reports', dc)
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
            if not hasattr(devReports, 'SMI-S Reports'):
                dc = rClass('SMI-S Reports', None)
                devReports._setObject('SMI-S Reports', dc)
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
                dc._delProperty('zPythonClass')
                dc._delProperty('zSnmpMonitorIgnore')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            if hasattr(devReports, 'SMI-S Reports'):
                devReports._delObject('SMI-S Reports')
