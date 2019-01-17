### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    def __init__(self):
        self.nick = ('recv', 'send')
        self.type = 'b'
        self.cols = 2
        self.server = os.getenv('DSTAT_SNMPSERVER') or '192.168.1.1'
        self.community = os.getenv('DSTAT_SNMPCOMMUNITY') or 'public'

    def check(self):
        try:
            global cmdgen
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except:
            raise Exception('Needs pysnmp and pyasn1 modules')

    def name(self):
        return self.vars

    def vars(self):
        return [ str(x) for x in snmpwalk(self.server, self.community, (1,3,6,1,2,1,2,2,1,2)) ]

    def extract(self):
        list(map(lambda x, y, z: self.set2.update({x: (int(y), int(z))}), self.vars, snmpwalk(self.server, self.community, (1,3,6,1,2,1,2,2,1,10)), snmpwalk(self.server, self.community, (1,3,6,1,2,1,2,2,1,16))))

        if update:
            for name in self.set2:
                self.val[name] = list(map(lambda x, y: (y - x) * 1.0 / elapsed, self.set1[name], self.set2[name]))

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
