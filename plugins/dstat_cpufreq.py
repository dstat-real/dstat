### Author: dag@wieers.com

class dstat_plugin(dstat):
    """
    CPU frequency in percentage as reported by ACPI.
    """

    def __init__(self):
        self.name = 'frequency'
        self.type = 'p'
        self.width = 4
        self.scale = 34

    def check(self): 
        for cpu in glob.glob('/sys/devices/system/cpu/cpu[0-9]*'):
            if not os.access(cpu+'/cpufreq/scaling_cur_freq', os.R_OK):
                raise Exception('Cannot access acpi %s frequency information' % os.path.basename(cpu))

    def vars(self):
        ret = []
        for name in glob.glob('/sys/devices/system/cpu/cpu[0-9]*'):
            ret.append(os.path.basename(name))
        ret.sort()
        return ret
#       return os.listdir('/sys/devices/system/cpu/')

    def nick(self):
        return [name.lower() for name in self.vars]

    def extract(self):
        for cpu in self.vars:
            for line in dopen('/sys/devices/system/cpu/'+cpu+'/cpufreq/scaling_max_freq').readlines():
                l = line.split()
                max = int(l[0])
            for line in dopen('/sys/devices/system/cpu/'+cpu+'/cpufreq/scaling_cur_freq').readlines():
                l = line.split()
                cur = int(l[0])
            ### Need to close because of bug in sysfs (?)
            dclose('/sys/devices/system/cpu/'+cpu+'/cpufreq/scaling_cur_freq')
            self.set1[cpu] = self.set1[cpu] + cur * 100.0 / max

            if op.update:
                self.val[cpu] = self.set1[cpu] / elapsed
            else:
                self.val[cpu] = self.set1[cpu]

            if step == op.delay:
                self.set1[cpu] = 0

# vim:ts=4:sw=4:et
