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

ZC.DiskDrivePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'DiskDrive',
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
        ZC.DiskDrivePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DiskDrivePanel', ZC.DiskDrivePanel);
ZC.registerName('DiskDrive', _t('Hard Disk'), _t('Hard Disks'));

ZC.NetworkPortPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetworkPort',
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
        ZC.NetworkPortPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('NetworkPortPanel', ZC.NetworkPortPanel);
ZC.registerName('NetworkPort', _t('FC Port'), _t('FC Ports'));

ZC.EnclosureChassisPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'EnclosureChassis',
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
        ZC.EnclosureChassisPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('EnclosureChassisPanel', ZC.EnclosureChassisPanel);
ZC.registerName('EnclosureChassis', _t('Storage Enclosure'), _t('Storage Enclosures'));

ZC.StoragePoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'StoragePool',
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
        ZC.StoragePoolPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('StoragePoolPanel', ZC.StoragePoolPanel);
ZC.registerName('StoragePool', _t('Disk Group'), _t('Disk Groups'));

ZC.StorageProcessorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'StorageProcessor',
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
        ZC.StorageProcessorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('StorageProcessorPanel', ZC.StorageProcessorPanel);
ZC.registerName('StorageProcessor', _t('Storage Controller'), _t('Storage Controllers'));

ZC.StorageVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'StorageVolume',
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
        ZC.StorageVolumePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('StorageVolumePanel', ZC.StorageVolumePanel);
ZC.registerName('StorageVolume', _t('Virtual Disk'), _t('Virtual Disks'));

ZC.ReplicationGroupPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ReplicationGroup',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
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
        ZC.ReplicationGroupPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ReplicationGroupPanel', ZC.ReplicationGroupPanel);
ZC.registerName('ReplicationGroup', _t('Replication Group'), _t('Replication Groups'));
})();
