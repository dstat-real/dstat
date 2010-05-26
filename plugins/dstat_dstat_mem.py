### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Provide memory information related to the dstat process.

    The various values provide information about the memory usage of the
    dstat process. This plugin gives you the possibility to follow memory
    usage changes of dstat over time.
    """
    def __init__(self):
        self.name = 'dstat memory usage'
        self.vars = ('virtual', 'resident', 'shared', 'data')
        self.type = 'd'

    def extract(self):
        ### Extract counters
        l = dopen('/proc/%s/statm' % ownpid).read().split()
#        l = linecache.getline('/proc/%s/schedstat' % self.pid, 1).split()
        self.val['virtual'] = long(l[0]) * pagesize / 1024
        self.val['resident'] = long(l[1]) * pagesize / 1024
        self.val['shared'] = long(l[2]) * pagesize / 1024
#        self.val['text'] = long(l[3]) * pagesize / 1024
#        self.val['library'] = long(l[4]) * pagesize / 1024
        self.val['data'] = long(l[5]) * pagesize / 1024

# vim:ts=4:sw=4:et
