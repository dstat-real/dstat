### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'nfs3 server'
        self.nick = ('read', 'writ', 'rdir', 'inod', 'fs', 'cmmt')
        self.vars = ('read', 'write', 'readdir', 'inode', 'filesystem', 'commit')
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/net/rpc/nfsd')

    def check(self):
        info(1, 'Module %s is still experimental.' % self.filename)

    def extract(self):
        for l in self.splitlines():
            if not l or l[0] != 'proc3': continue
            self.set2['read'] = long(l[8])
            self.set2['write'] = long(l[9])
            self.set2['readdir'] = long(l[18]) + long(l[19])
            self.set2['inode'] = long(l[3]) + long(l[4]) + long(l[5]) + long(l[6]) + long(l[7]) + long(l[10]) + long(l[11]) + long(l[12]) + long(l[13]) + long(l[14]) + long(l[15]) + long(l[16]) + long(l[17])
            self.set2['filesystem'] = long(l[20]) + long(l[21]) + long(l[22])
            self.set2['commit'] = long(l[23])

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
