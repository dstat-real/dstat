### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'rpc server'
        self.nick = ('call', 'erca', 'erau', 'ercl', 'xdrc')
        self.vars = ('calls', 'badcalls', 'badauth', 'badclnt', 'xdrcall')
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/net/rpc/nfsd')

    def extract(self):
        for l in self.splitlines():
            if not l or l[0] != 'rpc': continue
            for i, name in enumerate(self.vars):
                self.set2[name] = int(l[i+1])

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
