### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global cpunr

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'most waiting for'
        self.vars = ('child process',)
        self.type = 's'
        self.width = 16
        self.scale = 0

    def extract(self):
        self.set2 = {}
        self.val['max'] = 0.0
        for pid in proc_pidlist():
            try:
                ### Using dopen() will cause too many open files
                l = proc_splitline('/proc/%s/stat' % pid)
            except IOError:
                continue

            if len(l) < 15: continue

            ### Reset previous value if it doesn't exist
            if pid not in self.set1:
                self.set1[pid] = 0

            self.set2[pid] = int(l[15]) + int(l[16])
            usage = (self.set2[pid] - self.set1[pid]) * 1.0 / elapsed / cpunr

            ### Is it a new topper ?
            if usage <= self.val['max']: continue

            self.val['max'] = usage
            self.val['name'] = getnamebypid(pid, l[1][1:-1])
            self.val['pid'] = pid

        ### Debug (show PID)
#       self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            self.set1 = self.set2

    def show(self):
        if self.val['max'] == 0.0:
            return '%-*s' % (self.width, '')
        else:
            return '%s%-*s%s' % (theme['default'], self.width-3, self.val['name'][0:self.width-3], cprint(self.val['max'], 'p', 3, 34))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
