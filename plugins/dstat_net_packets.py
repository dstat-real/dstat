class dstat_net_packets(dstat):
    def __init__(self):
        self.format = ('f', 5, 1000)
        self.open('/proc/net/dev')
        self.nick = ('#recv', '#send')
        self.discover = self.discover()
        self.vars = self.vars()
        self.name = ['pkt/'+name for name in self.vars]
        self.init(self.vars + ['total',], 2)

    def discover(self, *list):
        ret = []
        for line in self.readlines():
            l = line.replace(':', ' ').split()
            if len(l) < 17: continue
            if l[2] == '0' and l[10] == '0': continue
            name = l[0]
            if name not in ('lo', 'face'):
                ret.append(name)
        ret.sort()
        for item in list: ret.append(item)
        return ret

    def vars(self):
        ret = []
        if op.netlist:
            list = op.netlist
        elif not op.full:
            list = ('total',)
        else:
            list = self.discover
#           if len(list) > 2: list = list[0:2]
            list.sort()
        for name in list:
            if name in self.discover + ['total', 'lo']:
                ret.append(name)
        return ret

    def extract(self):
        self.cn2['total'] = [0, 0]
        for line in self.readlines():
            l = line.replace(':', ' ').split()
            if len(l) < 17: continue
            if l[2] == '0' and l[10] == '0': continue
            name = l[0]
            if name in self.vars :
                self.cn2[name] = ( long(l[2]), long(l[10]) )
            if name not in ('lo','face'):
                self.cn2['total'] = ( self.cn2['total'][0] + long(l[2]), self.cn2['total'][1] + long(l[10]))
        if update:
            for name in self.cn2.keys():
                self.val[name] = (
                    (self.cn2[name][0] - self.cn1[name][0]) * 1.0 / tick,
                    (self.cn2[name][1] - self.cn1[name][1]) * 1.0 / tick,
                 )
        if step == op.delay:
            self.cn1.update(self.cn2)
