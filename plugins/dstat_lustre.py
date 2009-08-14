global os
import os

class dstat_lustre(dstat):
    def __init__(self):
        self.name = []
        self.vars = []
        if os.path.exists('/proc/fs/lustre/llite'):
            for mount in os.listdir('/proc/fs/lustre/llite'):
                self.vars.append(mount)
                self.name.append(mount[:mount.rfind('-')])
        self.format = ('f', 5, 1024)
        self.nick = ('read', 'write')
        self.init(self.vars, 2)
        info(1, 'Module dstat_lustre is still experimental.')

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
            self.cn2[name] = (read, write)
            self.val[name] = ( (self.cn2[name][0] - self.cn1[name][0]) * 1.0 / tick,\
                               (self.cn2[name][1] - self.cn1[name][1]) * 1.0 / tick ) 
            if step == op.delay:
                self.cn1.update(self.cn2)

# vim:ts=4:sw=4
# Authors
# Brock Palen brockp@mlds-networks.com
# Kilian Vavalotti kilian@stanford.edu
