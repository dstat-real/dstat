### Author: Bert de Bruijn <bert+dstat$debruijn,be>

### VMware ESX kernel interrupt stats
### Displays kernel interrupt statistics on VMware ESX servers

# NOTE TO USERS: command-line plugin configuration is not yet possible, so I've
# "borrowed" the -I argument. 
# EXAMPLES:
# # dstat --vmkint -I 0x46,0x5a
# You can even combine the Linux and VMkernel interrupt stats
# # dstat --vmkint -i -I 14,0x5a
# Look at /proc/vmware/interrupts to see which interrupt is linked to which function

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'vmkint'
        self.type = 'd'
        self.width = 4
        self.scale = 1000
        self.open('/proc/vmware/interrupts')
#       self.intmap = self.intmap()

#   def intmap(self):
#       ret = {}
#       for line in dopen('/proc/vmware/interrupts').readlines():
#           l = line.split()
#           if len(l) <= self.vmkcpunr: continue
#           l1 = l[0].split(':')[0]
#           l2 = ' '.join(l[vmkcpunr()+1:]).split(',')
#           ret[l1] = l1
#           for name in l2:
#               ret[name.strip().lower()] = l1
#           return ret

    def vmkcpunr(self):
        #the service console sees only one CPU, so cpunr == 1, only the vmkernel sees all CPUs
        ret = []
        # default cpu number is 2
        ret = 2
        for l in self.fd[0].splitlines():
            if l[0] == 'Vector': 
                ret = int( int( l[-1] ) + 1 )
        return ret

    def discover(self):
        #interrupt names are not decimal numbers, but rather hexadecimal numbers like 0x7e
        ret = []
        self.fd[0].seek(0)
        for line in self.fd[0].readlines():
            l = line.split()
            if l[0] == 'Vector': continue
            if len(l) < self.vmkcpunr()+1: continue
            name = l[0].split(':')[0]
            amount = 0
            for i in l[1:1+self.vmkcpunr()]:
                amount = amount + long(i)
            if amount > 20: ret.append(str(name))
        return ret

    def vars(self):
        ret = []
        if op.intlist:
            list = op.intlist
        else:
            list = self.discover
#           len(list) > 5: list = list[-5:]
        for name in list:
            if name in self.discover:
                ret.append(name)
#           elif name.lower() in self.intmap.keys():
#               ret.append(self.intmap[name.lower()])
        return ret

    def check(self): 
        try:
            os.listdir('/proc/vmware')
        except:
            raise Exception, 'Needs VMware ESX'
        info(1, 'The vmkint module is an EXPERIMENTAL module.')

    def extract(self):
        self.fd[0].seek(0)
        for line in self.fd[0].readlines():
            l = line.split()
            if len(l) < self.vmkcpunr()+1: continue
            name = l[0].split(':')[0]
            if name in self.vars:
                self.set2[name] = 0
                for i in l[1:1+self.vmkcpunr()]:
                    self.set2[name] = self.set2[name] + long(i)

        for name in self.set2.keys():
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4
