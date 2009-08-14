### Dstat cpu frequency plugin
### Displays CPU frequency information (from ACPI)
###
### Authority: dag@wieers.com

global glob
import glob

class dstat_cpufreq(dstat):
    def __init__(self):
        self.name = 'frequency'
        self.format = ('p', 4, 34)
#       self.vars = os.listdir('/sys/devices/system/cpu/')
#       self.nick = [name.lower() for name in self.vars]
        self.vars = []
        self.nick = []
        for name in glob.glob('/sys/devices/system/cpu/cpu[0-9]*'):
            name = os.path.basename(name)
            self.vars.append(name)
            self.nick.append(name.lower())
        self.nick.sort()
        self.init(self.vars, 1)

    def check(self): 
        if self.vars:
            for cpu in self.vars:
                if not os.access('/sys/devices/system/cpu/'+cpu+'/cpufreq/scaling_cur_freq', os.R_OK):
                    raise Exception, 'Cannot access acpi '+cpu+' frequency information'
            return True
        raise Exception, 'No statistics found'

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
            self.cn1[cpu] = self.cn1[cpu] + cur * 100.0 / max

            if op.update:
                self.val[cpu] = self.cn1[cpu] / tick
            else:
                self.val[cpu] = self.cn1[cpu]

            if step == op.delay:
                self.cn1[cpu] = 0

# vim:ts=4:sw=4:et
