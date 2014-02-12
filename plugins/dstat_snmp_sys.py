### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'system'
        self.nick = ('int', 'csw')
        self.vars = ('intr', 'ctxt')
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.server = os.getenv('DSTAT_SNMPSERVER') or '192.168.1.1'
        self.community = os.getenv('DSTAT_SNMPCOMMUNITY') or 'public'

    def check(self):
        try:
            global cmdgen
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except:
            raise Exception, 'Needs pysnmp and pyasn1 modules'

    def extract(self):
        self.set2['intr'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,11,59,0)))
        self.set2['ctxt'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,11,60,0)))

        if update:
            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
