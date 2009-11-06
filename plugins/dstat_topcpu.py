### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global cpunr

class dstat_topcpu(dstat):
    def __init__(self):
        self.name = 'most expensive'
        self.type = 's'
        self.width = 16
        self.scale = 0
        self.vars = ('cpu process',)
        self.pid = str(os.getpid())
        self.pidset1 = {}; self.pidset2 = {}

    def extract(self):
        self.val['max'] = 0.0
        self.val['cpu process'] = ''
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
                l = open('/proc/%s/stat' % pid).read().split()

            except ValueError:
                continue
            except IOError:
                continue

            if len(l) < 15: continue

            ### Reset previous value if it doesn't exist
            if not self.pidset1.has_key(pid):
                self.pidset1[pid] = 0

            self.pidset2[pid] = int(l[13]) + int(l[14])
            usage = (self.pidset2[pid] - self.pidset1[pid]) * 1.0 / tick / cpunr

            ### Is it a new topper ?
            if usage < self.val['max']: continue

            name = l[1][1:-1]

            self.val['max'] = usage
            self.val['pid'] = pid
            self.val['name'] = getnamebypid(pid, name)

        if self.val['max'] != 0.0:
            self.val['cpu process'] = '%-*s%s' % (self.width-3, self.val['name'][0:self.width-3], cprint(self.val['max'], 'p', 3, 34))

        ### Debug (show PID)
#        self.val['cpu process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            self.pidset1.update(self.pidset2)

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
