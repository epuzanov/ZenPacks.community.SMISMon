################################################################################
#
# This program is part of the ZenSMIS Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SMISPlugin

wrapper for PythonPlugin

$Id: SMISPlugin.py,v 1.0 2011/09/04 22:20:29 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class SMISPlugin(SQLPlugin):

    deviceProperties = SQLPlugin.deviceProperties + ('snmpSysName',
                                                    'zWbemProxy',
                                                    'zWinUser',
                                                    'zWinPassword',
                                                    'zSNIAConnectionString',
                                                    )


    def prepareCS(self, device):
        args = [getattr(device, 'zSNIAConnectionString',
                                        "'pywbemdb',scheme='https',port=5989")]
        kwargs = eval('(lambda *argsl,**kwargs:kwargs)(%s)'%args[0].lower())
        if 'host' not in kwargs:
            args.append("host='%s'"%getattr(device, 'zWbemProxy', 'localhost'))
        if 'user' not in kwargs:
            args.append("user='%s'"%getattr(device, 'zWinUser', ''))
        if 'password' not in kwargs:
            args.append("password='%s'"%getattr(device, 'zWinPassword', ''))
        return ','.join(args)
