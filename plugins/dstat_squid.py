### Authority: Jason Friedland <thesuperjason@gmail.com>

# This plugin has been tested with:
# - Dstat 0.6.7
# - CentOS release 5.4 (Final)
# - Python 2.4.3
# - Squid 2.6 and 2.7
 
global squidclient_options
squidclient_options = os.getenv('DSTAT_SQUID_OPTS') # -p 8080
 
class dstat_plugin(dstat):
    '''
    Provides various Squid statistics.
    '''
    def __init__(self):
        self.name = 'squid status'
        self.type = 's'
        self.width = 5
        self.scale = 1000
        self.vars = ('Number of file desc currently in use',
            'CPU Usage, 5 minute avg',
            'Total accounted',
            'Number of clients accessing cache',
            'Mean Object Size')
        self.nick = ('fdesc',
            'cpu5',
            'mem',
            'clnts',
            'objsz')

    def check(self):
        if not os.access('/usr/sbin/squidclient', os.X_OK):
            raise Exception('Needs squidclient binary')
        cmd_test('/usr/sbin/squidclient %s mgr:info' % squidclient_options)
        return True
 
    def extract(self):
        try:
            for l in cmd_splitlines('/usr/sbin/squidclient %s mgr:info' % squidclient_options, ':'):
                if l[0].strip() in self.vars:
                    self.val[l[0].strip()] = l[1].strip()
                    break
        except IOError as e:
            if op.debug > 1: print('%s: lost pipe to squidclient, %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1
        except Exception as e:
            if op.debug > 1: print('%s: exception' (self.filename, e))
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et
