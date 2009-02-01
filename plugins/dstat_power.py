### Dstat power usage plugin
### Displays power usage information from ACPI
###
### Authority: dag@wieers.com

global string
import string

class dstat_power(dstat):
    def __init__(self):
        self.name = 'power'
        self.format = ('f', 5, 1)
        self.vars = ( 'rate', )
        self.nick = ( 'usage', )
        self.batteries = []
        self.rate = 0
        for battery in os.listdir('/proc/acpi/battery/'):
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = string.split(line)
                if len(l) < 2: continue
                self.batteries.append(battery)
                break
        self.init(self.vars, 1)

    def extract(self):
        amperes_drawn = 0
        voltage = 0
        watts_drawn = 0
        for battery in self.batteries:
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = string.split(line)
                if len(l) < 3: continue
                if l[0] == 'present:' and l[1] != 'yes': continue
                if l[0:2] == ['charging','state:'] and l[2] != 'discharging':
                    voltage = 0
                    break
                if l[0:2] == ['present','voltage:']:
                    voltage = int(l[2]) / 1000.0
                elif l[0:2] == ['present','rate:'] and l[3] == 'mW':
                    watts_drawn = int(l[2]) / 1000.0
                elif l[0:2] == ['present','rate:'] and l[3] == 'mA':
                    amperes_drawn = int(l[2]) / 1000.0

            self.rate = self.rate + watts_drawn + voltage * amperes_drawn

        if op.update:
            self.val['rate'] = self.rate / tick
        else:
            self.val['rate'] = self.rate

        if step == op.delay:
            self.rate = 0

# vim:ts=4:sw=4:et
