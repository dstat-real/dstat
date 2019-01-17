### Author: Bert de Bruijn <bert+dstat$debruijn,be>

### VMware memory stats
### Displays memory stats coming from the hypervisor inside VMware VMs.
### The vmGuestLib API from VMware Tools needs to be installed

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'vmware memory'
        self.vars = ('active', 'ballooned', 'mapped',  'swapped', 'used')
        self.nick = ('active', 'balln', 'mappd', 'swapd', 'used')
        self.type = 'd'
        self.width = 5
        self.scale = 1024

    def check(self):
        try:
            global vmguestlib
            import vmguestlib

            self.gl = vmguestlib.VMGuestLib()
        except:
            raise Exception('Needs python-vmguestlib module')

    def extract(self):
        self.gl.UpdateInfo()
        self.val['active'] = self.gl.GetMemActiveMB() * 1024 ** 2
        self.val['ballooned'] = self.gl.GetMemBalloonedMB() * 1024 ** 2
        self.val['mapped'] = self.gl.GetMemMappedMB() * 1024 ** 2
        self.val['swapped'] = self.gl.GetMemSwappedMB() * 1024 ** 2
        self.val['used'] = self.gl.GetMemUsedMB() * 1024 ** 2

# vim:ts=4:sw=4
