### Author: Bert de Bruijn <bert+dstat$debruijn,be>

### VMware cpu stats
### Displays CPU stats coming from the hypervisor inside VMware VMs.
### The vmGuestLib API from VMware Tools needs to be installed

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'vm cpu'
        self.vars = ('used', 'stolen', 'elapsed')
        self.nick = ('usd', 'stl')
        self.type = 'p'
        self.width = 3
        self.scale = 100
        self.cpunr = getcpunr()

    def check(self):
        try:
            global vmguestlib
            import vmguestlib

            self.gl = vmguestlib.VMGuestLib()
        except:
            raise Exception, 'Needs python-vmguestlib module'

    def extract(self):
        self.gl.UpdateInfo()
        self.set2['elapsed'] = self.gl.GetElapsedMs()
        self.set2['stolen'] = self.gl.GetCpuStolenMs()
        self.set2['used'] = self.gl.GetCpuUsedMs()

        for name in ('stolen', 'used'):
            self.val[name] = (self.set2[name] - self.set1[name]) * 100 / (self.set2['elapsed'] - self.set1['elapsed']) / self.cpunr

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4