### Dstat Display Process Count plugin
### Displays the number of processes on a machine

class dstat_plugin(dstat):
    def __init__(self):
        self.name   = 'procs'
        self.type = 'd'
        self.width = 4
        self.scale = 10
        self.vars   = ('total',)

    def extract(self):
        self.val['total'] = len(glob.glob('/proc/[0-9]*'))
