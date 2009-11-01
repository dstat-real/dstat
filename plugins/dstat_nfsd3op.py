class dstat_nfsd3op(dstat):
    def __init__(self):
        self.name = 'extended nfs3 server operations'
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/net/rpc/nfsd')
        self.vars = ('null', 'getattr', 'setattr', 'lookup', 'access', 'readlink', 'read', 'write', 'create', 'mkdir', 'symlink', 'mknod', 'remove', 'rmdir', 'rename', 'link', 'readdir', 'readdirplus', 'fsstat', 'fsinfo', 'pathconf', 'commit')
        self.nick = ('null', 'gatr', 'satr', 'look', 'aces', 'rdln', 'read', 'writ', 'crea', 'mkdr', 'syml', 'mknd', 'rm', 'rmdr', 'ren', 'link', 'rdir', 'rdr+', 'fstt', 'fsnf', 'path', 'cmmt')
        info(1, 'Module dstat_nfsd3op is still experimental.')

    def extract(self):
        for l in self.splitlines():
            if not l or l[0] != 'proc3': continue
            for i, name in enumerate(self.vars):
                self.set2[name] = long(l[i+2])
        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / tick
        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
