class dstat_net_packets(dstat):
    def __init__(self):
        self.format = ('f', 5, 1000)
        self.open('/proc/net/dev')
        self.nick = ('#recv', '#send')
        self.totalfilter = re.compile('^(lo|bond[0-9]+|face|.+\.[0-9]+)$')
        self.discover = self.discover()
        self.vars = self.vars()
        self.name = ['pkt/'+name for name in self.vars]
        self.init(self.vars + ['total',], 2)

    def discover(self, *objlist):
        ret = []
        for l in self.splitlines(replace=':'):
            if len(l) < 17: continue
            if l[2] == '0' and l[10] == '0': continue
            name = l[0]
            if name not in ('lo', 'face'):
                ret.append(name)
        ret.sort()
        for item in objlist: ret.append(item)
        return ret

    def vars(self):
        ret = []
        if op.netlist:
            varlist = op.netlist
        elif not op.full:
            varlist = ('total',)
        else:
            varlist = self.discover
#           if len(varlist) > 2: varlist = varlist[0:2]
            varlist.sort()
        for name in varlist:
            if name in self.discover + ['total', 'lo']:
                ret.append(name)
        if not ret:
            raise Exception, "No suitable network interfaces found to monitor"
        return ret

    def extract(self):
        self.cn2['total'] = [0, 0]
        for l in self.splitlines(replace=':'):
            if len(l) < 17: continue
            if l[2] == '0' and l[10] == '0': continue
            name = l[0]
            if name in self.vars :
                self.cn2[name] = ( long(l[2]), long(l[10]) )
            if not self.totalfilter.match(name):
                self.cn2['total'] = ( self.cn2['total'][0] + long(l[2]), self.cn2['total'][1] + long(l[10]))
        if update:
            for name in self.cn2.keys():
                self.val[name] = (
                    (self.cn2[name][0] - self.cn1[name][0]) * 1.0 / tick,
                    (self.cn2[name][1] - self.cn1[name][1]) * 1.0 / tick,
                 )
        if step == op.delay:
            self.cn1.update(self.cn2)
