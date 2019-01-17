### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.nick = ('fcnt', )
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/user_beancounters')
        self.cols = 1 ### Is this correct ?

    def check(self):
        info(1, 'Module %s is still experimental.' % self.filename)

    def discover(self, *list):
        ret = []
        for l in self.splitlines():
            if len(l) < 7 or l[0] in ('uid', '0:'): continue
            ret.append(l[0][0:-1])
        ret.sort()
        for item in list: ret.append(item)
        return ret

    def name(self):
        ret = []
        for name in self.vars:
            if name == 'total':
                ret.append('total failcnt')
            else:
                ret.append(name)
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
        for name in self.vars + ['total']:
            self.set2[name] = 0
        for l in self.splitlines():
            if len(l) < 6 or l[0] == 'uid':
                continue
            elif len(l) == 7:
                name = l[0][0:-1]
                if name in self.vars:
                    self.set2[name] = self.set2[name] + int(l[6])
                self.set2['total'] = self.set2['total'] + int(l[6])
            elif name == '0':
                continue
            else:
                if name in self.vars:
                    self.set2[name] = self.set2[name] + int(l[5])
                self.set2['total'] = self.set2['total'] + int(l[5])

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
