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
            self.set2['read'] = int(l[8])
            self.set2['write'] = int(l[9])
            self.set2['readdir'] = int(l[18]) + int(l[19])
            self.set2['inode'] = int(l[3]) + int(l[4]) + int(l[5]) + int(l[6]) + int(l[7]) + int(l[10]) + int(l[11]) + int(l[12]) + int(l[13]) + int(l[14]) + int(l[15]) + int(l[16]) + int(l[17])
            self.set2['filesystem'] = int(l[20]) + int(l[21]) + int(l[22])
            self.set2['commit'] = int(l[23])

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
