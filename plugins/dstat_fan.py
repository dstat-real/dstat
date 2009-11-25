### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Fan speed in RPM (rotations per minute) as reported by ACPI.
    """

    def __init__(self):
        self.name = 'fan'
        self.type = 'd'
        self.width = 4
        self.scale = 500

    def vars(self):
        ret = None
        for line in dopen('/proc/acpi/ibm/fan'):
            l = line.split()
            if l[0] == 'speed:':
                ret = ('speed',)
        return ret

    def check(self):
        if not os.path.exists('/proc/acpi/ibm/fan'):
            raise Exception, 'Needs kernel IBM-ACPI support'

    def extract(self):
        if os.path.exists('/proc/acpi/ibm/fan'):
            for line in dopen('/proc/acpi/ibm/fan'):
                l = line.split()
                if l[0] == 'speed:':
                    self.val['speed'] = int(l[1])

# vim:ts=4:sw=4:et
