class dstat_plugin(dstat):
    """
    ZFS on Linux ARC (Adjustable Replacement Cache)

    Data is extracted from /proc/spl/kstat/zfs/arcstats
    """
    def __init__(self):
        self.name = 'ZFS ARC'
        self.nick = ('mem', 'hit', 'miss', 'reads', 'hit%')
        self.vars = ('size', 'hits', 'misses', 'total', 'hit_rate')
        self.types = ('b', 'd', 'd', 'd', 'p')
        self.scales = (1024, 1000, 1000, 1000, 1000)
        self.counter = (False, True, True, False, False)
        self.open('/proc/spl/kstat/zfs/arcstats')

    def extract(self):
        for l in self.splitlines():
            if len(l) < 2: continue
            l[0].split()
            name = l[0]
            if name in self.vars:
                self.set2[name] = int(l[2])

        for i, name in enumerate (self.vars):
            if self.counter[i]:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed
            else:
                self.val[name] = self.set2[name]

        self.val['total'] = self.val['hits'] + self.val['misses']

        if self.val['total'] > 0 :
            self.val['hit_rate'] = self.val['hits'] / self.val['total'] * 100.0
        else:
            self.val['hit_rate'] = 0

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
