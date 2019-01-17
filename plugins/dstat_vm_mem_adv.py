### Author: Bert de Bruijn <bert+dstat$debruijn,be>

### VMware advanced memory stats
### Displays memory stats coming from the hypervisor inside VMware VMs.
### The vmGuestLib API from VMware Tools needs to be installed

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'vmware advanced memory'
        self.vars = ('active', 'ballooned', 'mapped', 'overhead', 'saved', 'shared', 'swapped', 'targetsize', 'used')
        self.nick = ('active', 'balln', 'mappd', 'ovrhd', 'saved', 'shard', 'swapd', 'targt', 'used')
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
        self.val['overhead'] = self.gl.GetMemOverheadMB() * 1024 ** 2
        self.val['saved'] = self.gl.GetMemSharedSavedMB() * 1024 ** 2
        self.val['shared'] = self.gl.GetMemSharedMB() * 1024 ** 2
        self.val['swapped'] = self.gl.GetMemSwappedMB() * 1024 ** 2
        self.val['targetsize'] = self.gl.GetMemTargetSizeMB() * 1024 ** 2
        self.val['used'] = self.gl.GetMemUsedMB() * 1024 ** 2

# vim:ts=4:sw=4
