### Author: Dag Wieers <dag$wieers,com>

### FIXME: This module needs infrastructure to provide a list of mountpoints
### FIXME: Would be nice to have a total by default (half implemented)

class dstat_plugin(dstat):
    """
    Amount of used and free space per mountpoint.
    """

    def __init__(self):
        self.nick = ('used', 'free')
        self.open('/etc/mtab')
        self.cols = 2

    def vars(self):
        ret = []
        for l in self.splitlines():
            if len(l) < 6: continue
            if l[2] in ('binfmt_misc', 'devpts', 'iso9660', 'none', 'proc', 'sysfs', 'usbfs', 'cgroup', 'tmpfs', 'devtmpfs', 'debugfs', 'mqueue', 'systemd-1', 'rootfs', 'autofs'): continue
            ### FIXME: Excluding 'none' here may not be what people want (/dev/shm)
            if l[0] in ('devpts', 'none', 'proc', 'sunrpc', 'usbfs', 'securityfs', 'hugetlbfs', 'configfs', 'selinuxfs', 'pstore', 'nfsd'): continue
            name = l[1]
            res = os.statvfs(name)
            if res[0] == 0: continue ### Skip zero block filesystems
            ret.append(name)

            #print(l[0] + " / " + name + " / " + l[2])
        return ret

    def name(self):
        return ['/' + os.path.basename(name) for name in self.vars]

    def extract(self):
        self.val['total'] = (0, 0)
        for name in self.vars:
            res = os.statvfs(name)
            self.val[name] = ( (float(res.f_blocks) - float(res.f_bavail)) * int(res.f_frsize), float(res.f_bavail) * float(res.f_frsize) )
            self.val['total'] = (self.val['total'][0] + self.val[name][0], self.val['total'][1] + self.val[name][1])

# vim:ts=4:sw=4:et
