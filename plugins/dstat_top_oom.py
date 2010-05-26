### Author: Dag Wieers <dag@wieers.com>

### Dstat most expensive process plugin
### Displays the name of the most expensive process

### More information:
###    http://lwn.net/Articles/317814/

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'out of memory'
        self.vars = ('kill score',)
        self.type = 's'
        self.width = 18
        self.scale = 0

    def check(self):
        if not os.access('/proc/self/oom_score', os.R_OK):
            raise Exception, 'Kernel does not support /proc/pid/oom_score, use at least 2.6.11.'

    def extract(self):
        self.output = ''
        self.val['max'] = 0.0
        for pid in proc_pidlist():
            try:
                ### Extract name
                name = proc_splitline('/proc/%s/stat' % pid)[1][1:-1]

                ### Using dopen() will cause too many open files
                l = proc_splitline('/proc/%s/oom_score' % pid)
            except IOError:
                continue
            except IndexError:
                continue

            if len(l) < 1: continue
            oom_score = int(l[0])

            ### Is it a new topper ?
            if oom_score <= self.val['max']: continue

            self.val['max'] = oom_score
            self.val['name'] = getnamebypid(pid, name)
            self.val['pid'] = pid

        if self.val['max'] != 0.0:
            self.output = '%-*s%s' % (self.width-4, self.val['name'][0:self.width-4], cprint(self.val['max'], 'f', 4, 1000))

        ### Debug (show PID)
#       self.output = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
