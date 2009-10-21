class dstat_fan(dstat):
    def __init__(self):
        self.name = 'fan'
        self.type = 'd'
        self.width = 4
        self.scale = 500
        if os.path.exists('/proc/acpi/ibm/fan'):
            for line in dopen('/proc/acpi/ibm/fan'):
                l = line.split()
                if l[0] == 'speed:':
                    self.vars = ('speed',)
            self.nick = self.vars
        else:
            raise Exception, 'Needs kernel IBM-ACPI support'
        self.init(self.vars, 1)

    def extract(self):
        if os.path.exists('/proc/acpi/ibm/fan'):
            for line in dopen('/proc/acpi/ibm/fan'):
                l = line.split()
                if l[0] == 'speed:':
                    self.val['speed'] = int(l[1])

# vim:ts=4:sw=4:et
