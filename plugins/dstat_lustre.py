global os
import os

class dstat_lustre(dstat):
    def __init__(self):
        self.nick = ('read', 'write')
        info(1, 'Module dstat_lustre is still experimental.')

    def name(self):
        ret = []
        for mount in os.listdir('/proc/fs/lustre/llite'):
            ret.append(mount[:mount.rfind('-')])
        return ret

    def vars(self):
        ret = []
        for mount in os.listdir('/proc/fs/lustre/llite'):
            ret.append(mount)
        return ret

    def check(self):
        if not os.path.exists('/proc/fs/lustre/llite'):
            raise Exception, 'Lustre filesystem not found'

    def extract(self):
        for name in self.vars:
            f = open('/'.join(['/proc/fs/lustre/llite',name,'stats']))
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if not l or l[0] != 'read_bytes': continue
                read = long(l[6])
            for line in lines:
                l = line.split()
                if not l or l[0] != 'write_bytes': continue
                write = long(l[6])
            self.set2[name] = (read, write)
            self.val[name] = ( (self.set2[name][0] - self.set1[name][0]) * 1.0 / tick,\
                               (self.set2[name][1] - self.set1[name][1]) * 1.0 / tick ) 
            if step == op.delay:
                self.set1.update(self.set2)

# vim:ts=4:sw=4
# Authors
# Brock Palen brockp@mlds-networks.com
# Kilian Vavalotti kilian@stanford.edu
