### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'memory usage'
        self.nick = ('used', 'buff', 'cach', 'free')
        self.vars = ('MemUsed', 'Buffers', 'Cached', 'MemFree')
        self.server = os.getenv('DSTAT_SNMPSERVER') or '192.168.1.1'
        self.community = os.getenv('DSTAT_SNMPCOMMUNITY') or 'public'

    def check(self):
        try:
            global cmdgen
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except:
            raise Exception('Needs pysnmp and pyasn1 modules')

    def extract(self):
        self.val['MemTotal'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,4,5,0))) * 1024
        self.val['MemFree'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,4,11,0))) * 1024
#        self.val['Shared'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,4,13,0))) * 1024
        self.val['Buffers'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,4,14,0))) * 1024
        self.val['Cached'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,4,15,0))) * 1024

        self.val['MemUsed'] = self.val['MemTotal'] - self.val['MemFree']

# vim:ts=4:sw=4:et
