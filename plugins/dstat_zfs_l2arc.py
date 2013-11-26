class dstat_plugin(dstat):
    """
    ZFS on Linux L2ARC (Level 2 Adjustable Replacement Cache)

    Data is extracted from /proc/spl/kstat/zfs/arcstats
    """
    def __init__(self):
        self.name = 'ZFS L2ARC'
        self.nick = ('size', 'hit', 'miss', 'hit%', 'read', 'write')
        self.vars = ('l2_size', 'l2_hits', 'l2_misses', 'hit_rate', 'l2_read_bytes', 'l2_write_bytes')
        self.types = ('b', 'd', 'd', 'p', 'b', 'b')
        self.scales = (1024, 1000, 1000, 1000, 1024, 1024)
        self.counter = (False, True, True, False, True, True)
        self.open('/proc/spl/kstat/zfs/arcstats')

    def extract(self):
        for l in self.splitlines():
            if len(l) < 2: continue
            l[0].split()
            name = l[0]
            if name in self.vars:
                self.set2[name] = long(l[2])

        for i, name in enumerate (self.vars):
            if self.counter[i]:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed
            else:
                self.val[name] = self.set2[name]

        probes = self.val['l2_hits'] + self.val['l2_misses']

	if probes > 0 :
            self.val['hit_rate'] = self.val['l2_hits'] / probes * 100.0
	else:
            self.val['hit_rate'] = 0

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
