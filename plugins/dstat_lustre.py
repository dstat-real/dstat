# Author: Brock Palen <brockp@mlds-networks.com>, Kilian Vavalotti <kilian@stanford.edu>

class dstat_plugin(dstat):
    def __init__(self):
        self.nick = ('read', 'write')
        self.cols = 2 

    def check(self):
        if not os.path.exists('/proc/fs/lustre/llite'):
            raise Exception('Lustre filesystem not found')
        info(1, 'Module %s is still experimental.' % self.filename)

    def name(self):
        return [mount for mount in os.listdir('/proc/fs/lustre/llite')]

    def vars(self):
        return [mount for mount in os.listdir('/proc/fs/lustre/llite')]

    def extract(self):
        for name in self.vars:
            for line in dopen(os.path.join('/proc/fs/lustre/llite', name, 'stats')).readlines():
                l = line.split()
                if len(l) < 6: continue
                if l[0] == 'read_bytes':
                    read = int(l[6])
                elif l[0] == 'write_bytes':
                    write = int(l[6])
            self.set2[name] = (read, write)

            self.val[name] = list(map(lambda x, y: (y - x) * 1.0 / elapsed, self.set1[name], self.set2[name]))

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4
