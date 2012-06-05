class dstat_plugin(dstat):
    """
    Detailed memory usage

    Displays memory usage similarly to the internal plugin but with added total and reclaimable counters.
    Additionally, reclaimable memory is subtracted from the used memory counter.
    """
    def __init__(self):
        self.name = 'detailed memory usage'
        self.nick = ('total', 'used', 'buff', 'cach', 'free', 'recl')
        self.vars = ('MemTotal', 'MemUsed', 'Buffers', 'Cached', 'MemFree', 'SReclaimable')
        self.open('/proc/meminfo')

    def extract(self):
        for l in self.splitlines():
            if len(l) < 2: continue
            name = l[0].split(':')[0]
            if name in self.vars:
                self.val[name] = long(l[1]) * 1024.0
        self.val['MemUsed'] = self.val['MemTotal'] - self.val['MemFree'] - self.val['Buffers'] - self.val['Cached'] - self.val['SReclaimable']

# vim:ts=4:sw=4:et
