### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Provide CPU information related to the dstat process.

    This plugin shows the CPU utilization for the dstat process itself,
    including the user-space and system-space (kernel) utilization and
    a total of both. On a system with one cpu and one core, the total
    cputime is 1000ms. On a system with 2 cores the total is 2000ms.
    It may help to vizualise the performance of Dstat and its selection
    of plugins.
    """
    def __init__(self):
        self.name = 'dstat cpu'
        self.vars = ('user', 'system', 'total')
        self.nick = ('usr', 'sys', 'tot')
        self.type = 'p'
        self.width = 3
        self.scale = 100

    def extract(self):
        res = resource.getrusage(resource.RUSAGE_SELF)

        self.set2['user'] = float(res.ru_utime)
        self.set2['system'] = float(res.ru_stime)
        self.set2['total'] = float(res.ru_utime) + float(res.ru_stime)

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 100.0 / elapsed / cpunr

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
