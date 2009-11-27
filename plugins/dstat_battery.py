### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Percentage of remaining battery power as reported by ACPI.
    """
    def __init__(self):
        self.name = 'battery'
        self.type = 'p'
        self.width = 4
        self.scale = 34

    def check(self):
        if not os.path.exists('/proc/acpi/battery/'):
            raise Exception, "No ACPI battery information found."

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
            for line in dopen('/proc/acpi/battery/'+battery+'/info').readlines():
                l = line.split()
                if len(l) < 4: continue
                if l[0] == 'last':
                    full = int(l[3])
                    break
            for line in dopen('/proc/acpi/battery/'+battery+'/state').readlines():
                l = line.split()
                if len(l) < 3: continue
                if l[0] == 'remaining':
                    current = int(l[2])
                    break
            if current:
                self.val[battery] = current * 100.0 / full
            else:
                self.val[battery] = -1

# vim:ts=4:sw=4:et
