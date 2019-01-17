### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'thermal'
        self.type = 'd'
        self.width = 3
        self.scale = 20

        if os.path.exists('/sys/devices/virtual/thermal/'):
            self.nick = []
            self.vars = []
            for zone in os.listdir('/sys/devices/virtual/thermal/'):
                zone_split=zone.split("thermal_zone")
                if len(zone_split) == 2:
                    self.vars.append(zone)
                    name="".join(["tz",zone_split[1]])
                    self.nick.append(name)

        elif os.path.exists('/sys/bus/acpi/devices/LNXTHERM:01/thermal_zone/'):
            self.vars = os.listdir('/sys/bus/acpi/devices/LNXTHERM:01/thermal_zone/')
            self.nick = []
            for name in self.vars:
                self.nick.append(name.lower())

        elif os.path.exists('/proc/acpi/ibm/thermal'):
            self.namelist = ['cpu', 'pci', 'hdd', 'cpu', 'ba0', 'unk', 'ba1', 'unk']
            self.nick = []
            for line in dopen('/proc/acpi/ibm/thermal'):
                l = line.split()
                for i, name in enumerate(self.namelist):
                    if int(l[i+1]) > 0:
                        self.nick.append(name)
            self.vars = self.nick

        elif os.path.exists('/proc/acpi/thermal_zone/'):
            self.vars = os.listdir('/proc/acpi/thermal_zone/')
#           self.nick = [name.lower() for name in self.vars]
            self.nick = []
            for name in self.vars:
                self.nick.append(name.lower())

        else:
            raise Exception('Needs kernel thermal, ACPI or IBM-ACPI support')

    def check(self):
        if not os.path.exists('/proc/acpi/ibm/thermal') and \
           not os.path.exists('/proc/acpi/thermal_zone/') and \
           not os.path.exists('/sys/devices/virtual/thermal/') and \
           not os.path.exists('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/'):
            raise Exception('Needs kernel thermal, ACPI or IBM-ACPI support')

    def extract(self):
        if os.path.exists('/sys/devices/virtual/thermal/'):
            for zone in self.vars:
                for line in dopen('/sys/devices/virtual/thermal/'+zone+'/temp').readlines():
                    l = line.split()
                    self.val[zone] = int(l[0])
        elif os.path.exists('/sys/bus/acpi/devices/LNXTHERM:01/thermal_zone/'):
            for zone in self.vars:
                if os.path.isdir('/sys/bus/acpi/devices/LNXTHERM:01/thermal_zone/'+zone) == False:
                    for line in dopen('/sys/bus/acpi/devices/LNXTHERM:01/thermal_zone/'+zone).readlines():
                        l = line.split()
                        if l[0].isdigit() == True:
                            self.val[zone] = int(l[0])
                        else:
                            self.val[zone] = 0
        elif os.path.exists('/proc/acpi/ibm/thermal'):
            for line in dopen('/proc/acpi/ibm/thermal'):
                l = line.split()
                for i, name in enumerate(self.namelist):
                    if int(l[i+1]) > 0:
                        self.val[name] = int(l[i+1])
        elif os.path.exists('/proc/acpi/thermal_zone/'):
            for zone in self.vars:
                for line in dopen('/proc/acpi/thermal_zone/'+zone+'/temperature').readlines():
                    l = line.split()
                    self.val[zone] = int(l[1])

# vim:ts=4:sw=4:et
