
#Version: 2.2
#VEID   user    nice    system   uptime     idle             strv   uptime          used           maxlat  totlat  numsched
#302    142926  0       10252    152896388  852779112954062  0      427034187248480 1048603937010  0       0       0
#301    27188   0       7896     152899846  853267000490282  0      427043845492614 701812592320   0       0       0

class dstat_vzcpu(dstat):
    def __init__(self):
        self.type = 'p'
        self.width = 3
        self.scale = 34
        self.open('/proc/vz/vestat')
        self.nick = ('usr', 'sys', 'idl', 'nic')
        self.discover = self.discover()
        self.vars = self.vars()
        self.name = self.name()
        self.init(self.vars + ['total'], 4)
        info(1, 'Module dstat_vzcpu is still experimental.')

    def discover(self, *list):
        ret = []
        for l in self.splitlines():
            if len(l) < 6 or l[0] == 'VEID': continue
            ret.append(l[0])
        ret.sort()
        for item in list: ret.append(item)
        return ret

    def name(self):
        ret = []
        for name in self.vars:
            if name == 'total':
                ret.append('total ve usage')
            else:
                ret.append('ve ' + name + ' usage')
        return ret

    def vars(self):
        ret = []
        if not op.full:
            list = ('total', )
        else: 
            list = self.discover
        for name in list: 
            if name in self.discover + ['total']:
                ret.append(name)
        return ret

    def extract(self):
        self.cn2['total'] = [0, 0, 0, 0]
        for line in self.splitlines():
            if len(l) < 6 or l[0] == 'VEID': continue
            name = l[0]
            self.cn2[name] = ( long(l[1]), long(l[3]), long(l[4]) - long(l[1]) - long(l[2]) - long(l[3]), long(l[2]) )
            self.cn2['total'] = ( self.cn2['total'][0] + long(l[1]), self.cn2['total'][1] + long(l[3]), self.cn2['total'][2] + long(l[4]) - long(l[1]) - long(l[2]) - long(l[3]), self.cn2['total'][3] + long(l[2]) )
        for name in self.vars:
            for i in range(4):
                self.val[name][i] = 100.0 * (self.cn2[name][i] - self.cn1[name][i]) / (sum(self.cn2[name]) - sum(self.cn1[name]))
        if step == op.delay:
            self.cn1.update(self.cn2)

# vim:ts=4:sw=4:et
