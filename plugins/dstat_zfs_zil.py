class dstat_plugin(dstat):
    """
    ZFS on Linux ZIL (ZFS Intent Log)

    Data is extracted from /proc/spl/kstat/zfs/zil
    """
    def __init__(self):
        self.name = 'ZFS ZIL'
        self.nick = ('count', 'bytes')
        self.vars = ('zil_itx_metaslab_slog_count', 'zil_itx_metaslab_slog_bytes')
        self.types = ('d', 'b')
        self.scales = (1000, 1024)
        self.counter = (True, True)
        self.open('/proc/spl/kstat/zfs/zil')

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

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
