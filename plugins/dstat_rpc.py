global string
import string

class dstat_rpc(dstat):
    def __init__(self):
        self.name = 'rpc client'
        self.format = ('d', 5, 1000)
        self.open('/proc/net/rpc/nfs')
        self.vars = ('calls', 'retransmits', 'autorefreshes')
        self.nick = ('call', 'retr', 'refr')
        self.init(self.vars, 1)

    def extract(self):
        for line in self.readlines():
            l = line.split()
            if not l or l[0] != 'rpc': continue
            for i, name in enumerate(self.vars):
                self.cn2[name] = long(l[i+1])
        for name in self.vars:
            self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick
        if step == op.delay:
            self.cn1.update(self.cn2)

# vim:ts=4:sw=4:et
