### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    The average size (in sectors) of the requests that were issued
    to the device.
    """

    def __init__(self):
        self.version = 2
        self.nick = ('avgrq',)
        self.type = 'f'
        self.width = 4
        self.scale = 10
        self.diskfilter = re.compile('^([hsv]d[a-z]+\d+|cciss/c\d+d\d+p\d+|dm-\d+|md\d+|mmcblk\d+p\d0|VxVM\d+)$')
        self.open('/proc/diskstats')
        self.cols = 1
        self.struct = dict( nr_ios=0, rd_sect=0, wr_sect=0 )

    def discover(self, *objlist):
        ret = []
        for l in self.splitlines():
            if len(l) < 13: continue
            if l[3:] == ['0',] * 11: continue
            name = l[2]
            ret.append(name)
        for item in objlist: ret.append(item)
        if not ret:
            raise Exception, "No suitable block devices found to monitor"
        return ret

    def vars(self):
        ret = []
        if op.disklist:
            varlist = op.disklist
        else:
            varlist = []
            blockdevices = [os.path.basename(filename) for filename in glob.glob('/sys/block/*')]
            for name in self.discover:
                if self.diskfilter.match(name): continue
                if name not in blockdevices: continue
                varlist.append(name)
            varlist.sort()
        for name in varlist:
            if name in self.discover:
                ret.append(name)
        return ret

    def name(self):
        return self.vars

    def extract(self):
        for l in self.splitlines():
            if len(l) < 13: continue
            if l[3:] == ['0',] * 11: continue
            if l[3] == '0' and l[7] == '0': continue
            name = l[2]
            if name not in self.vars or name == 'total': continue
            self.set2[name] = dict(
                nr_ios = long(l[3])+long(l[7]),
                rd_sect = long(l[9]),
                wr_sect = long(l[11]),
            )

        for name in self.vars:
            tput = ( self.set2[name]['nr_ios'] - self.set1[name]['nr_ios'] )
            if tput:
                ticks = self.set2[name]['rd_sect'] - self.set1[name]['rd_sect'] + \
                        self.set2[name]['wr_sect'] - self.set1[name]['wr_sect']
                self.val[name] = ( ticks * 1.0 / tput, )
            else:
                self.val[name] = ( 0.0, )

        if step == op.delay:
            self.set1.update(self.set2)
