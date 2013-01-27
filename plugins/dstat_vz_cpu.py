### Author: Dag Wieers <dag@wieers.com>

#Version: 2.2
#VEID   user    nice    system   uptime     idle             strv   uptime          used           maxlat  totlat  numsched
#302    142926  0       10252    152896388  852779112954062  0      427034187248480 1048603937010  0       0       0
#301    27188   0       7896     152899846  853267000490282  0      427043845492614 701812592320   0       0       0

class dstat_plugin(dstat):
    def __init__(self):
        self.nick = ('usr', 'sys', 'idl', 'nic')
        self.type = 'p'
        self.width = 3
        self.scale = 34
        self.open('/proc/vz/vestat')
        self.cols = 4

    def check(self):
        info(1, 'Module %s is still experimental.' % self.filename)

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
        self.set2['total'] = [0, 0, 0, 0]
        for l in self.splitlines():
            if len(l) < 6 or l[0] == 'VEID': continue
            name = l[0]
            self.set2[name] = ( long(l[1]), long(l[3]), long(l[4]) - long(l[1]) - long(l[2]) - long(l[3]), long(l[2]) )
            self.set2['total'] = ( self.set2['total'][0] + long(l[1]), self.set2['total'][1] + long(l[3]), self.set2['total'][2] + long(l[4]) - long(l[1]) - long(l[2]) - long(l[3]), self.set2['total'][3] + long(l[2]) )

        for name in self.vars:
            for i in range(self.cols):
                self.val[name][i] = 100.0 * (self.set2[name][i] - self.set1[name][i]) / (sum(self.set2[name]) - sum(self.set1[name]))

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
