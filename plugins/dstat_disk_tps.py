### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Percentage of bandwidth utilization for block devices.

    Displays percentage of CPU time during which I/O requests were issued
    to the device (bandwidth utilization for the device). Device saturation
    occurs when this value is close to 100%.
    """

    def __init__(self):
        self.nick = ('reads', 'writs' )
        self.type = 'd'
        self.scale = 1000
        self.diskfilter = re.compile('^(dm-[0-9]+|md[0-9]+|[hsv]d[a-z]+[0-9]+)$')
        self.open('/proc/diskstats')
        self.cols = 2

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
        elif not op.full:
            varlist = ('total',)
        else:
            varlist = []
            blockdevices = [os.path.basename(filename) for filename in glob.glob('/sys/block/*')]
            for name in self.discover:
                if self.diskfilter.match(name): continue
                if name not in blockdevices: continue
                varlist.append(name)
#           if len(varlist) > 2: varlist = varlist[0:2]
            varlist.sort()
        for name in varlist:
            if name in self.discover + ['total'] + op.diskset.keys():
                ret.append(name)
        return ret

    def name(self):
        return ['dsk/'+name for name in self.vars]

    def extract(self):
        for name in self.vars: self.set2[name] = (0, 0)
        for l in self.splitlines():
            if len(l) < 13: continue
            if l[3] == '0' and l[7] == '0': continue
            name = l[2]
            if l[3:] == ['0',] * 11: continue
            if not self.diskfilter.match(name):
                self.set2['total'] = ( self.set2['total'][0] + long(l[3]), self.set2['total'][1] + long(l[7]) )
            if name in self.vars and name != 'total':
                self.set2[name] = ( self.set2[name][0] + long(l[3]), self.set2[name][1] + long(l[7]))
            for diskset in self.vars:
                if diskset in op.diskset.keys():
                    for disk in op.diskset[diskset]:
                        if re.match('^'+disk+'$', name):
                            self.set2[diskset] = ( self.set2[diskset][0] + long(l[3]), self.set2[diskset][1] + long(l[7]) )
        for name in self.set2.keys():
            self.val[name] = (
                (self.set2[name][0] - self.set1[name][0]) / elapsed,
                (self.set2[name][1] - self.set1[name][1]) / elapsed,
            )
        if step == op.delay:
            self.set1.update(self.set2)

# S_VALUE(ioj->rd_ios, ioi->rd_ios, itv),
# S_VALUE(ioj->wr_ios, ioi->wr_ios, itv),

