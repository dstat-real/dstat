### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    """
    Power usage information from ACPI.

    Displays the power usage in watt per hour of your system's battery using
    ACPI information. This information is only available when the battery is
    being used (or being charged).
    """

    def __init__(self):
        self.name = 'power'
        self.nick = ( 'usage', )
        self.vars = ( 'rate', )
        self.type = 'f'
        self.width = 5
        self.scale = 1
        self.rate = 0
        self.batteries = []
        for battery in os.listdir('/proc/acpi/battery/'):
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = line.split()
                if len(l) < 2: continue
                self.batteries.append(battery)
                break

    def check(self):
        if not self.batteries:
            raise Exception, 'No battery information found, no power usage statistics'

    def extract(self):
        amperes_drawn = 0
        voltage = 0
        watts_drawn = 0
        for battery in self.batteries:
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = line.split()
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

        ### Return error if we found no information
        if self.rate == 0:
            self.rate = -1

        if op.update:
            self.val['rate'] = self.rate / elapsed
        else:
            self.val['rate'] = self.rate

        if step == op.delay:
            self.rate = 0

# vim:ts=4:sw=4:et
