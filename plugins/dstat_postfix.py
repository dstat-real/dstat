### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'postfix'
        self.nick = ('inco', 'actv', 'dfrd', 'bnce', 'defr')
        self.vars = ('incoming', 'active', 'deferred', 'bounce', 'defer')
        self.type = 'd'
        self.width = 4
        self.scale = 100

    def check(self):
        if not os.access('/var/spool/postfix/active', os.R_OK):
            raise Exception, 'Cannot access postfix queues'

    def extract(self):
        for item in self.vars:
            self.val[item] = len(glob.glob('/var/spool/postfix/'+item+'/*/*'))

# vim:ts=4:sw=4:et
