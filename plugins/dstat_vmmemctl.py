### VMware vmmemctl stats
### Displays ballooning status inside VMware VMs. 
### The vmmemctl from the VMware Tools needs to be loaded.
### This plugin has been tested on a VM running CentOS5 with the open-vm-tools, on ESX3.5
###
### Authority: bert+dstat@debruijn.be

# NB Data comes from /proc/vmmemctl

class dstat_vmmemctl(dstat):
    def __init__(self):
        self.name = 'memctl'
        self.type = 'f'
        self.width = 6
        self.scale = 1024
        self.open('/proc/vmmemctl')
        self.nick = ('size',)
        self.vars = ('balloon',)

    def check(self): 
        try:
            os.stat('/proc/vmmemctl')
        except:
            raise Exception, 'Needs VMware Tools (modprobe vmmemctl)'

    def extract(self):
        for l in self.splitlines():
            if len(l) < 3: continue
            if l[0] != 'current:': continue
            if l[2] != 'pages': continue
            self.val['balloon'] = int(l[1]) * 4096.0
            break
# vim:ts=4:sw=4
