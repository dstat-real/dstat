### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Provide memory information related to the dstat process.

    The various values provide information about the memory usage of the
    dstat process. This plugin gives you the possibility to follow memory
    usage changes of dstat over time.
    """
    def __init__(self):
        self.name = 'contxt sw'
        self.vars = ('voluntary', 'involuntary', 'total')
        self.type = 'd'
        self.width = 3
        self.scale = 100

    def extract(self):
        res = resource.getrusage(resource.RUSAGE_SELF)

        self.set2['voluntary'] = float(res.ru_nvcsw)
        self.set2['involuntary'] = float(res.ru_nivcsw)
        self.set2['total'] = (float(res.ru_nvcsw) + float(res.ru_nivcsw))

        for name in self.vars:
            self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
