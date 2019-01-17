### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'load avg'
        self.nick = ('1m', '5m', '15m')
        self.vars = ('load1', 'load5', 'load15')
        self.type = 'f'
        self.width = 4
        self.scale = 0.5
        self.server = os.getenv('DSTAT_SNMPSERVER') or '192.168.1.1'
        self.community = os.getenv('DSTAT_SNMPCOMMUNITY') or 'public'

    def check(self):
        try:
            global cmdgen
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except:
            raise Exception('Needs pysnmp and pyasn1 modules')

    def extract(self):
        list(map(lambda x, y: self.val.update({x: float(y)}), self.vars, snmpwalk(self.server, self.community, (1,3,6,1,4,1,2021,10,1,3))))

# vim:ts=4:sw=4:et
