### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Remaining battery time.

    Calculated from power drain and remaining battery power. Information is
    retrieved from ACPI.
    """

    def __init__(self):
        self.name = 'remain'
        self.type = 't'
        self.width = 5
        self.scale = 0

    def vars(self):
        ret = []
        for battery in os.listdir('/proc/acpi/battery/'):
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = line.split()
                if len(l) < 2: continue
                if l[0] == 'present:' and l[1] == 'yes':
                    ret.append(battery)
        ret.sort()
        return ret

    def nick(self):
        return [name.lower() for name in self.vars]

    def extract(self):
        for battery in self.vars:
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = line.split()
                if len(l) < 3: continue
                if l[0:2] == ['remaining', 'capacity:']:
                    remaining = int(l[2])
                    continue
                elif l[0:2] == ['present', 'rate:']:
                    rate = int(l[2])
                    continue

            if rate and remaining:
                self.val[battery] = remaining * 60 / rate
            else:
                self.val[battery] = -1

# vim:ts=4:sw=4:et
