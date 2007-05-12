### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global string
import string

class dstat_app(dstat):
    def __init__(self):
        self.name = 'most expensive'
        self.format = ('s', 18, 0)
        self.nick = ('process',)
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.cn1 = {}; self.cn2 = {}; self.val = {}

    def extract(self):
        max = 0.0
        for pid in os.listdir('/proc/'):
            try: int(pid)
            except: continue
            if os.path.exists('/proc/%s/stat' % pid):
                if pid == self.pid: continue
                if not self.cn1.has_key(pid):
                    self.cn1[pid] = 0

                ### Using dopen() will cause too many open files
#               l = string.split(dopen('/proc/%s/stat' % pid).read())
                l = string.split(open('/proc/%s/stat' % pid).read())
                if len(l) < 15: continue
                self.cn2[pid] = int(l[13]) + int(l[14])
                usage = (self.cn2[pid] - self.cn1[pid]) * 1.0 / tick

                ### Get the process that spends the most jiffies
                if usage > max:
                    max = usage
                    self.val['name'] = l[1][1:-1]
                    self.val['pid'] = pid

        if max == 0.0:
            self.val['process'] = ''
        else:
            ### If the name is a known interpreter, take the second argument from the cmdline
            if self.val['name'] in ('bash', 'csh', 'ksh', 'perl', 'python', 'sh'):
                ### Using dopen() will cause too many open files
#               l = string.split(dopen('/proc/%s/cmdline' % self.val['pid']).read(), '\0')
                l = string.split(open('/proc/%s/cmdline' % self.val['pid']).read(), '\0')
                if len(l) > 2:
                    self.val['name'] = os.path.basename(l[1])

#               l = l.reverse()
#               for x in l:
#                   print x
#                   if x[0] != '-':
#                       self.val['name'] = os.path.basename(x)
#                       break

            ### Show yellow usage
            self.val['process'] = '%-*s%s%3d' % (self.format[1]-3, self.val['name'], ansi['yellow'], round(max))

            ### Debug (show PID)
#           self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.format[1]-6, self.val['name'])

        if step == op.delay:
            self.cn1.update(self.cn2)

# vim:ts=4:sw=4:et
