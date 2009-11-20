### VMware ESX kernel vmknic stats
### Displays VMkernel port statistics on VMware ESX servers
###
### Authority: bert+dstat@debruijn.be

# NOTE TO USERS: command-line plugin configuration is not yet possible, so I've
# "borrowed" the -N argument.
# EXAMPLES:
# # dstat -M vmknic -N vmk1
# You can even combine the Linux and VMkernel network stats (just don't just "total").
# # dstat -M vmknic -n -N vmk0,vswif0
# NB Data comes from /proc/vmware/net/tcpip/ifconfig

class dstat_vmknic(dstat):
    def __init__(self):
        self.name = 'vmknic'
        self.open('/proc/vmware/net/tcpip/ifconfig')
        self.nick = ('recv', 'send')
        self.cols = 2
        info(1, 'The vmknic module is an EXPERIMENTAL module.')

    def discover(self, *list):
        ret = []
        for l in self.fd[0].splitlines(replace=' /', delim='/'):
            if len(l) != 12: continue
            if l[2][:5] == '<Link': continue
            if ','.join(l) == 'Name,Mtu/TSO,Network,Address,Ipkts,Ierrs,Ibytes,Opkts,Oerrs,Obytes,Coll,Time': continue
            if l[0] == 'lo0': continue
            if l[0] == 'Usage:': continue
            ret.append(l[0])
        ret.sort()
        for item in list: ret.append(item)
        return ret

    def vars(self):
        ret = []
        if op.netlist:
            list = op.netlist
        else:
            list = self.discover
            list.sort()
        for name in list:
            if name in self.discover + ['total']:
                ret.append(name)
        return ret

    def name(self):
        return ['net/'+name for name in self.vars]

    def check(self): 
        try:
            os.listdir('/proc/vmware')
        except:
            raise Exception, 'Needs VMware ESX'

    def extract(self):
        self.set2['total'] = [0, 0]
        for line in self.readlines():
            l = line.replace(' /','/').split()
            if len(l) != 12: continue
            if l[2][:5] == '<Link': continue
            if ','.join(l) == 'Name,Mtu/TSO,Network,Address,Ipkts,Ierrs,Ibytes,Opkts,Oerrs,Obytes,Coll,Time': continue
            if l[0] == 'Usage:': continue
            name = l[0]
            if name in self.vars:
                self.set2[name] = ( long(l[6]), long(l[9]) )
            if name != 'lo0':
                self.set2['total'] = ( self.set2['total'][0] + long(l[6]), self.set2['total'][1] + long(l[9]) )
        if update:
            for name in self.set2.keys():
                self.val[name] = (
                    (self.set2[name][0] - self.set1[name][0]) * 1.0 / elapsed,
                    (self.set2[name][1] - self.set1[name][1]) * 1.0 / elapsed,
                )
        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4
