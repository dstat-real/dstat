### Author: Dean Wilson <dean.wilson@gmail.com>

class dstat_plugin(dstat):
    """
    Memcache hit count plugin.

    Displays the number of memcache get_hits and get_misses.
    """
    def __init__(self):
        self.name = 'Memcache Hits'
        self.nick = ('Hit', 'Miss')
        self.vars = ('get_hits', 'get_misses')
        self.type = 'd'
        self.width = 6
        self.scale = 50

    def check(self):
        try:
            global memcache
            import memcache
            self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        except:
            raise Exception, 'Plugin needs the memcache module'

    def extract(self):
        stats = self.mc.get_stats()
        for key in self.vars:
            self.val[key] = long(stats[0][1][key])
