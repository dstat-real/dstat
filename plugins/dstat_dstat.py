### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Provide more information related to the dstat process.

    The dstat cputime is the total cputime dstat requires per second. On a
    system with one cpu and one core, the total cputime is 1000ms. On a system
    with 2 cores the total is 2000ms.
    """
    def __init__(self):
        self.name = 'dstat'
        self.vars = ('cputime', 'latency')
        self.type = 'd'
        self.width = 4
        self.scale = 100
        self.pid = str(os.getpid())

    def extract(self):
        ### Extract counters
        l = dopen('/proc/%s/schedstat' % self.pid).read().split()
#        l = linecache.getline('/proc/%s/schedstat' % self.pid, 1).split()

        self.set2['cputime'] = long(l[0])
        self.set2['latency'] = long(l[1])

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
