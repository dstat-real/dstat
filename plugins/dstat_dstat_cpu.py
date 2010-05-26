### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Provide memory information related to the dstat process.

    The various values provide information about the memory usage of the
    dstat process. This plugin gives you the possibility to follow memory
    usage changes of dstat over time.
    """
    def __init__(self):
        self.name = 'dstat cputime'
        self.vars = ('system', 'user', 'total')
        self.type = 'd'
        self.width = 4
        self.scale = 100

    def extract(self):
        ### Extract counters
        l = resource.getrusage(resource.RUSAGE_SELF)

        self.set2['system'] = float(l[0])
        self.set2['user'] = float(l[1])
        self.set2['total'] = (float(l[0]) + float(l[1]))

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1000.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
