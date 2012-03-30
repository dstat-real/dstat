### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Percentage of bandwidth utilization for block devices.

    Displays percentage of CPU time during which I/O requests were issued
    to the device (bandwidth utilization for the device). Device saturation
    occurs when this value is close to 100%.
    """

    def __init__(self):
        self.nick = ('util', )
        self.type = 'f'
        self.width = 4
        self.scale = 34
        self.diskfilter = re.compile('^(dm-\d+|md\d+|[hsv]d[a-z]+\d+)$')
        self.open('/proc/diskstats')
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

    def basename(self, disk):
        "Strip /dev/ and convert symbolic link"
        if disk[:5] == '/dev/':
            # file or symlink
            if os.path.exists(disk):
                # e.g. /dev/disk/by-uuid/15e40cc5-85de-40ea-b8fb-cb3a2eaf872
                if os.path.islink(disk):
                    target = os.readlink(disk)
                    # convert relative pathname to absolute
                    if target[0] != '/':
                        target = os.path.join(os.path.dirname(disk), target)
                        target = os.path.normpath(target)
                    print 'dstat: symlink %s -> %s' % (disk, target)
                    disk = target
                # trim leading /dev/
                return disk[5:]
            else:
                print 'dstat: %s does not exist' % disk
        else:
            return disk

    def vars(self):
        ret = []
        if op.disklist:
            varlist = map(self.basename, op.disklist)
        else:
            varlist = []
            for name in self.discover:
                if self.diskfilter.match(name): continue
                if name not in blockdevices(): continue
                varlist.append(name)
#           if len(varlist) > 2: varlist = varlist[0:2]
            varlist.sort()
        for name in varlist:
            if name in self.discover:
                ret.append(name)
        return ret

    def name(self):
        return [sysfs_dev(name) for name in self.vars]

    def extract(self):
        for name in self.vars: self.set2[name] = (0, )
        for l in self.splitlines():
            if len(l) < 13: continue
            if l[5] == '0' and l[9] == '0': continue
            name = l[2]
            if l[3:] == ['0',] * 11: continue
            if name in self.vars:
                self.set2[name] = ( self.set2[name][0] + long(l[12]), )
        for name in self.set2.keys():
            self.val[name] = (
                (self.set2[name][0] - self.set1[name][0]) * 1.0 * hz / elapsed / 1000,
            )
        if step == op.delay:
            self.set1.update(self.set2)
