### FIXME: This module needs infrastructure to provide a list of mountpoints
### FIXME: Would be nice to have a total by default (half implemented)

### FIXME: Apparently needs python 2.0, possibly python 2.2
global string
import string

class dstat_freespace(dstat):
    def __init__(self):
        self.format = ('f', 5, 1024)
        self.open('/etc/mtab')
        self.vars = self.vars()
#       self.name = ['/' + os.path.basename(name) for name in self.vars]
        self.name = []
        for name in self.vars:
            self.name.append('/' + os.path.basename(name))
        self.nick = ('used', 'free')
        self.init(self.vars + ['total',], 2)

    def vars(self):
        ret = []
        for line in self.readlines():
            l = string.split(line)
            if len(l) < 6: continue
            if l[2] in ('binfmt_misc', 'devpts', 'iso9660', 'none', 'proc', 'sysfs', 'usbfs'): continue
            ### FIXME: Excluding 'none' here may not be what people want (/dev/shm)
            if l[0] in ('devpts', 'none', 'proc', 'sunrpc', 'usbfs'): continue
            name = l[1] 
            res = os.statvfs(name)
            if res[0] == 0: continue ### Skip zero block filesystems
            ret.append(name)
        return ret

    def extract(self):
        self.val['total'] = (0, 0)
        for name in self.vars:
            res = os.statvfs(name)
            self.val[name] = ( (float(res.f_blocks) - float(res.f_bavail)) * long(res.f_frsize), float(res.f_bavail) * float(res.f_frsize) )
            self.val['total'] = (self.val['total'][0] + self.val[name][0], self.val['total'][1] + self.val[name][1])

# vim:ts=4:sw=4:et
