### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global string
import string

class dstat_topoom(dstat):
    def __init__(self):
        self.name = 'kill score'
        self.format = ('s', 20, 34)
        self.nick = ('oom process',)
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.cn1 = {}; self.cn2 = {}; self.val = {}

    def check(self):
        if not os.access('/proc/1/oom_score', os.R_OK):
            raise Exception, 'Kernel does not support /proc/pid/oom_score interface.'
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
#               l = string.split(dopen('/proc/%s/stat' % pid).read())
                l = string.split(open('/proc/%s/oom_score' % pid).read())
                if len(l) < 1: continue
                oom_score = int(l[0])

                if  oom_score < self.val['max']: continue

                ### Extract name
                l = string.split(open('/proc/%s/stat' % pid).read())
                name = l[1][1:-1]

                ### Get commandline
                m = string.split(open('/proc/%s/cmdline' % pid).read(), '\0')
                if len(m) > 1:
                    cmd = os.path.basename(m[1])

            except ValueError:
                continue
            except IOError:
                continue

            ### Get the process that spends the most jiffies
            if  oom_score >= self.val['max']:

                self.val['max'] = oom_score
                self.val['name'] = name
                self.val['pid'] = pid
                self.val['cmd'] = cmd
#                st = os.stat("/proc/%s" % pid)
#                if st:
#                    pw = pwd.getpwuid(st.st_uid)
#                    if pw:
#                        self.val['user'] = pw[0]
#                    else:
#                        self.val['user'] = stat.st_uid
#                else:
#                    self.val['user'] = 'none'

        if self.val['max'] == 0.0:
            self.val['process'] = ''
        else:
            ### If the name is a known interpreter, take the second argument from the cmdline
            if self.val['name'] in ('bash', 'csh', 'ksh', 'perl', 'python', 'sh'):
                self.val['process'] = os.path.basename(cmd)
            else:
                self.val['process'] = self.val['name']

#               l = l.reverse()
#               for x in l:
#                   print x
#                   if x[0] != '-':
#                       self.val['name'] = os.path.basename(x)
#                       break

            ### Debug (show PID)
#           self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.format[1]-6, self.val['name'])

    def show(self):
        if self.val['max'] == 0.0:
            return '%-*s' % (self.format[1], '')
        else:
            return '%s%-*s%s' % (ansi['default'], self.format[1]-6, self.val['process'][0:self.format[1]-6], cprint(self.val['max'], ('p', 6, 34)))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
