### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

class dstat_topoom(dstat):
    def __init__(self):
        self.name = 'out of memory'
        self.type = 's'
        self.width = 18
        self.scale = 0
        self.vars = ('kill score',)
        self.pid = str(os.getpid())

    def check(self):
        if not os.access('/proc/self/oom_score', os.R_OK):
            raise Exception, 'Kernel does not support /proc/pid/oom_score, use at least 2.6.11.'

    def extract(self):
        self.val['max'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
                l = open('/proc/%s/oom_score' % pid).read().split()
                if len(l) < 1: continue
                oom_score = int(l[0])

                ### Is it a new topper ?
                if oom_score < self.val['max']: continue

                ### Extract name
                l = open('/proc/%s/stat' % pid).read().split()
                name = l[1][1:-1]

            except ValueError:
                continue
            except IOError:
                continue

            self.val['max'] = oom_score
            self.val['name'] = name
            self.val['pid'] = pid

        if self.val['max'] == 0.0:
            self.val['process'] = ''
        else:
            self.val['process'] = self.val['name']

        ### Debug (show PID)
#       self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if self.val['max'] == 0.0:
            self.val['kill score'] = ''
        else:
            self.val['kill score'] = '%-*s%s' % (self.width-4, self.val['process'][0:self.width-4], cprint(self.val['max'], 'f', 4, 1000))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
