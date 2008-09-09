### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global string
import string

class dstat_topoom(dstat):
    def __init__(self):
        self.name = 'out of memory'
        self.format = ('s', 18, 0)
        self.nick = ('kill score',)
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.cn1 = {}; self.cn2 = {}; self.val = {}

    def check(self):
        if not os.access('/proc/self/oom_score', os.R_OK):
            raise Exception, 'Kernel does not support /proc/pid/oom_score, use at least 2.6.11.'
        return True

    def extract(self):
        self.val['max'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
                l = string.split(open('/proc/%s/oom_score' % pid).read())
                if len(l) < 1: continue
                oom_score = int(l[0])

                ### Is it a new topper ?
                if oom_score < self.val['max']: continue

                ### Extract name
                l = string.split(open('/proc/%s/stat' % pid).read())
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
#           self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.format[1]-6, self.val['name'])

    def show(self):
        if self.val['max'] == 0.0:
            return '%-*s' % (self.format[1], '')
        else:
            return '%s%-*s%s' % (ansi['default'], self.format[1]-4, self.val['process'][0:self.format[1]-4], cprint(self.val['max'], ('f', 4, 1000)))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
