### Author: David Nicklay <david-d$nicklay,com>
### Modified from disk-util: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Read and Write average wait times of block devices.

    Displays the average read and write wait times of block devices
    """

    def __init__(self):
        self.type = 'f'
        self.width = 6
        self.scale = 34
        self.diskfilter = re.compile('^(dm-\d+|md\d+|[hsv]d[a-z]+\d+)$')
        self.open('/proc/diskstats')
        self.nick = ('rawait','wawait' )
        self.cols = 1

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
        for name in self.vars:
            self.set2[name] = (0, 0, 0, 0 )
        for l in self.splitlines():
            if len(l) < 13: continue
            if l[5] == '0' and l[9] == '0': continue
            name = l[2]
            if l[3:] == ['0',] * 11: continue
            if name in self.vars:
                self.set2[name] = (
                    0 + long(l[3]),
                    0 + long(l[6]),
                    0 + long(l[7]),
                    0 + long(l[10])
                )
        for name in self.set2.keys():
            try:
                self.val[name] = (
                    ( (self.set2[name][1] - self.set1[name][1]) * 1.0 )
                    /
                    ( (self.set2[name][0] - self.set1[name][0]) * 1.0 )
                    ,
                    ( (self.set2[name][3] - self.set1[name][3]) * 1.0 )
                    /
                    ( (self.set2[name][2] - self.set1[name][2]) * 1.0 )
                )
            except IndexError:
                self.val[name] = (0,0)
                pass
            except ZeroDivisionError:
                self.val[name] = (0,0)
                pass
        if step == op.delay:
            self.set1.update(self.set2)

