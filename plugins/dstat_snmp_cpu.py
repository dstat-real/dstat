### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'total cpu'
        self.vars = ( 'usr', 'sys', 'idl' )
        self.type = 'p'
        self.width = 3
        self.scale = 34
        self.server = os.getenv('DSTAT_SNMPSERVER') or '192.168.1.1'
        self.community = os.getenv('DSTAT_SNMPCOMMUNITY') or 'public'

    def check(self):
        try:
            global cmdgen
            from pysnmp.entity.rfc3413.oneliner import cmdgen
        except:
            raise Exception('Needs pysnmp and pyasn1 modules')

    def extract(self):
        self.set2['usr'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,11,50,0)))
        self.set2['sys'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,11,52,0)))
        self.set2['idl'] = int(snmpget(self.server, self.community, (1,3,6,1,4,1,2021,11,53,0)))
#        self.set2['usr'] = int(snmpget(self.server, self.community, (('UCD-SNMP-MIB', 'ssCpuRawUser'), 0)))
#        self.set2['sys'] = int(snmpget(self.server, self.community, (('UCD-SNMP-MIB', 'ssCpuRawSystem'), 0)))
#        self.set2['idl'] = int(snmpget(self.server, self.community, (('UCD-SNMP-MIB', 'ssCpuRawIdle'), 0)))

        if update:
            for name in self.vars:
                if sum(self.set2.values()) > sum(self.set1.values()):
                    self.val[name] = 100.0 * (self.set2[name] - self.set1[name]) / (sum(self.set2.values()) - sum(self.set1.values()))
                else:
                    self.val[name] = 0

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
