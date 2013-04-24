### Authority: Damon Snyder <drsnyder$gmail,com>

class dstat_plugin(dstat):
    """
    Advanced memory statistics

    Displays various advanced memory counters from /proc/meminfo.
    """

    def __init__(self):
        self.name = 'advanced memory usage'
        self.nick = ('used', 'buff', 'cach', 'free', 'dirty')
        self.vars = ('MemUsed', 'Buffers', 'Cached', 'MemFree', 'Dirty', 'MemTotal')
        self.open('/proc/meminfo')

    def extract(self):
        for l in self.splitlines():
            if len(l) < 2: continue
            name = l[0].split(':')[0]
            if name in self.vars:
                self.val[name] = long(l[1]) * 1024.0
        self.val['MemUsed'] = self.val['MemTotal'] - self.val['MemFree'] - self.val['Buffers'] - self.val['Cached']
