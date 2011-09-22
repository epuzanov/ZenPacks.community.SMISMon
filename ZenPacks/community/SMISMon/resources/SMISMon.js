/*
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.SNIA_DiskDrivePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_DiskDrive',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'enclosure'},
                {name: 'storagePool'},
                {name: 'bay'},
                {name: 'diskType'},
                {name: 'size'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'enclosure',
                dataIndex: 'enclosure',
                header: _t('Enclosure'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Type'),
                width: 160
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                width: 60
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_DiskDrivePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_DiskDrivePanel', ZC.SNIA_DiskDrivePanel);
ZC.registerName('SNIA_DiskDrive', _t('Hard Disk'), _t('Hard Disks'));

ZC.SNIA_NetworkPortPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_NetworkPort',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'controller'},
                {name: 'mac'},
                {name: 'networkAddresses'},
                {name: 'linkTechnology'},
                {name: 'type'},
                {name: 'speed'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'controller',
                dataIndex: 'controller',
                header: _t('Controller'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Interface Name'),
                sortable: true
            },{
                id: 'mac',
                dataIndex: 'mac',
                header: _t('MAC'),
                sortable: true,
                width: 160
            },{
                id: 'networkAddresses',
                dataIndex: 'networkAddresses',
                sortable: true,
                header: _t('Network')
            },{
                id: 'linkTechnology',
                dataIndex: 'linkTechnology',
                header: _t('Link Technology')
            },{
                id: 'type',
                dataIndex: 'type',
                header: _t('Type')
            },{
                id: 'speed',
                dataIndex: 'speed',
                header: _t('Speed')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_NetworkPortPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_NetworkPortPanel', ZC.SNIA_NetworkPortPanel);
ZC.registerName('SNIA_NetworkPort', _t('Port'), _t('Ports'));

ZC.SNIA_EnclosureChassisPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_EnclosureChassis',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('ID'),
                width: 20,
                sortable: true
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_EnclosureChassisPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_EnclosureChassisPanel', ZC.SNIA_EnclosureChassisPanel);
ZC.registerName('SNIA_EnclosureChassis', _t('Storage Enclosure'), _t('Storage Enclosures'));

ZC.SNIA_StoragePoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_StoragePool',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'totalDisks'},
                {name: 'totalBytesString'},
                {name: 'usedBytesString'},
                {name: 'availBytesString'},
                {name: 'capacity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'totalDisks',
                dataIndex: 'totalDisks',
                header: _t('Total Disks')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Total bytes')
            },{
                id: 'usedBytesString',
                dataIndex: 'usedBytesString',
                header: _t('Used bytes')
            },{
                id: 'availBytesString',
                dataIndex: 'availBytesString',
                header: _t('Free bytes')
            },{
                id: 'capacity',
                dataIndex: 'capacity',
                header: _t('Utilization')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_StoragePoolPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_StoragePoolPanel', ZC.SNIA_StoragePoolPanel);
ZC.registerName('SNIA_StoragePool', _t('Disk Group'), _t('Disk Groups'));

ZC.SNIA_StorageProcessorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_StorageProcessor',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'slot'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'uptime'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'slot',
                dataIndex: 'slot',
                header: _t('Slot'),
                sortable: true
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'serialNumber',
                dataIndex: 'serialNumber',
                header: _t('Serial #'),
                width: 120
            },{
                id: 'uptime',
                dataIndex: 'uptime',
                header: _t('Uptime')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_StorageProcessorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_StorageProcessorPanel', ZC.SNIA_StorageProcessorPanel);
ZC.registerName('SNIA_StorageProcessor', _t('Controller'), _t('Controllers'));

ZC.SNIA_StorageVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_StorageVolume',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'storagePool'},
                {name: 'diskType'},
                {name: 'accessType'},
                {name: 'totalBytesString'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Disk Type')
            },{
                id: 'accessType',
                dataIndex: 'accessType',
                header: _t('Access')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Size')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_StorageVolumePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_StorageVolumePanel', ZC.SNIA_StorageVolumePanel);
ZC.registerName('SNIA_StorageVolume', _t('Virtual Disk'), _t('Virtual Disks'));

ZC.SNIA_ConsistencySetPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'SNIA_ConsistencySet',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'participationType'},
                {name: 'writeMode'},
                {name: 'remoteCellName'},
                {name: 'storagePool'},
                {name: 'currentPercentLogLevel'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'participationType',
                dataIndex: 'participationType',
                header: _t('Role')
            },{
                id: 'writeMode',
                dataIndex: 'writeMode',
                header: _t('Write Mode'),
                width: 150
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Log Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'currentPercentLogLevel',
                dataIndex: 'currentPercentLogLevel',
                header: _t('Log Usage'),
                width: 60
            },{
                id: 'remoteCellName',
                dataIndex: 'remoteCellName',
                header: _t('Remote System')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.SNIA_ConsistencySetPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('SNIA_ConsistencySetPanel', ZC.SNIA_ConsistencySetPanel);
ZC.registerName('SNIA_ConsistencySet', _t('Data Replication'), _t('Data Replication'));
})();
