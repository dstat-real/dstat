### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    """
    Top interrupt

    Displays the name of the most frequent interrupt
    """
    def __init__(self):
        self.name = 'most frequent'
        self.vars = ('interrupts',)
        self.type = 's'
        self.width = 20
        self.scale = 0
        self.intset1 = [ 0 ] * 256
        self.open('/proc/stat')
        self.names = self.names()

    def names(self):
        ret = {}
        for line in dopen('/proc/interrupts'):
            l = line.split()
            if len(l) <= cpunr: continue
            l1 = l[0].split(':')[0]
            ### Cleanup possible names
            l2 = ' '.join(l[cpunr+2:])
            l2 = l2.replace('_hcd:', '/')
            l2 = re.sub('@pci[:\d+\.]+', '', l2)
            ret[l1] = l2
        return ret

    def extract(self):
        self.output = ''
        self.val['total'] = 0.0
        for line in self.splitlines():
            if line[0] == 'intr':
                self.intset2 = [ long(int) for int in line[3:] ]

        for i in range(len(self.intset2)):
            total = (self.intset2[i] - self.intset1[i]) * 1.0 / elapsed

            ### Get the process that spends the most jiffies
            if total > self.val['total']:
                self.val['name'] = self.names[str(i+1)]
                self.val['total'] = total

        if step == op.delay:
            self.intset1 = self.intset2

        if self.val['total'] != 0.0:
            self.output = '%-15s%s' % (self.val['name'], cprint(self.val['total'], 'd', 5, 1000))

        ### Debug (show PID)
#        self.output = '%*s %-*s%s %s' % (5, self.val['pid'], self.width-17, self.val['name'][0:self.width-17], cprint(self.val['read_usage'], 'd', 5, 1024), cprint(self.val['write_usage'], 'd', 5, 1024))

    def showcsv(self):
        return '%s / %f' % (self.val['name'], self.val['total'])

# vim:ts=4:sw=4:et
