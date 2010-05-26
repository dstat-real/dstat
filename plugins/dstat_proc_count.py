### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    """
    Total Number of processes on this system.
    """
    def __init__(self):
        self.name = 'procs'
        self.vars = ('total',)
        self.type = 'd'
        self.width = 4
        self.scale = 10

    def extract(self):
        self.val['total'] = len([pid for pid in proc_pidlist()])
