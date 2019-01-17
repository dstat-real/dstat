### Author: Bert de Bruijn <bert+dstat$debruijn,be>

### VMware ESX kernel vmhba stats
### Displays kernel vmhba statistics on VMware ESX servers

# NOTE TO USERS: command-line plugin configuration is not yet possible, so I've
# "borrowed" the -D argument. 
# EXAMPLES:
# # dstat --vmkhba -D vmhba1,vmhba2,total
# # dstat --vmkhba -D vmhba0
# You can even combine the Linux and VMkernel diskstats (but the "total" argument
# will be used by both).
# # dstat --vmkhba -d -D sda,vmhba1

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'vmkhba'
        self.nick = ('read', 'writ')
        self.cols = 2

    def discover(self, *list):
    # discover will list all vmhba's found.
    # we might want to filter out the unused vmhba's (read stats, compare with ['0', ] * 13)
        ret = []
        try:
            list = os.listdir('/proc/vmware/scsi/')
        except:
            raise Exception('Needs VMware ESX')
        for name in list:
            for line in dopen('/proc/vmware/scsi/%s/stats' % name).readlines():
                l = line.split()
                if len(l) < 13: continue
                if l[0] == 'cmds': continue
                if l == ['0', ] * 13: continue
                ret.append(name)
        return ret

    def vars(self):
    # vars will take the argument list - when implemented - , use total, or will use discover + total
        ret = []
        if op.disklist:
            list = op.disklist
        #elif not op.full:
        #   list = ('total', )
        else:
            list = self.discover
            list.sort()
        for name in list:
            if name in self.discover + ['total']:
                ret.append(name)
        return ret

    def check(self): 
        try:
            os.listdir('/proc/vmware')
        except:
            raise Exception('Needs VMware ESX')
        info(1, 'The vmkhba module is an EXPERIMENTAL module.')

    def extract(self):
        self.set2['total'] = (0, 0)
        for name in self.vars:
            self.set2[name] = (0, 0)
        for name in os.listdir('/proc/vmware/scsi/'):
            for line in dopen('/proc/vmware/scsi/%s/stats' % name).readlines():
                l = line.split()
                if len(l) < 13: continue
                if l[0] == 'cmds': continue
                if l[2] == '0' and l[4] == '0': continue
                if l == ['0', ] * 13: continue
                self.set2['total'] = ( self.set2['total'][0] + int(l[2]), self.set2['total'][1] + int(l[4]) )
                if name in self.vars and name != 'total':
                    self.set2[name] = ( int(l[2]), int(l[4]) )

            for name in self.set2:
                self.val[name] = list(map(lambda x, y: (y - x) * 1024.0 / elapsed, self.set1[name], self.set2[name]))

        if step == op.delay:
            self.set1.update(self.set2)
