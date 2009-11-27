### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'wifi'
        self.nick = ('lnk', 's/n')
        self.type = 'd'
        self.width = 3
        self.scale = 34
        self.cols = 2

    def check(self):
        global iwlibs
        from pythonwifi import iwlibs

    def vars(self):
        return iwlibs.getNICnames()

    def extract(self):
        for name in self.vars:
            wifi = iwlibs.Wireless(name)
            stat, qual, discard, missed_beacon = wifi.getStatistics()
#           print qual.quality, qual.signallevel, qual.noiselevel
            if qual.quality == 0 or qual.signallevel == -101 or qual.noiselevel == -101 or qual.signallevel == -256 or qual.noiselevel == -256:
                self.val[name] = ( -1, -1 )
            else:
                self.val[name] = ( qual.quality, qual.signallevel * 100 / qual.noiselevel )

# vim:ts=4:sw=4:et
