### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

global string
import string

class dstat_topmem(dstat):
    def __init__(self):
        self.name = 'most expensive'
        self.format = ('s', 16, 0)
        self.nick = ('memory process',)
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.cn1 = {}; self.cn2 = {}; self.val = {}

    def extract(self):
        self.val['usage'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
#               l = string.split(dopen('/proc/%s/stat' % pid).read())
                l = string.split(open('/proc/%s/stat' % pid).read())

                if len(l) < 23: continue
                usage = int(l[23]) * pagesize

            except ValueError:
                continue

            ### Get the process that uses the most memory
            if usage >= self.val['usage']:
                self.val['usage'] = usage
                self.val['name'] = l[1][1:-1]
                self.val['pid'] = pid

        if self.val['usage'] == 0.0:
            self.val['process'] = ''
        else:
            ### If the name is a known interpreter, take the second argument from the cmdline
            if self.val['name'] in ('bash', 'csh', 'ksh', 'perl', 'python', 'sh'):
                ### Using dopen() will cause too many open files
#               l = string.split(dopen('/proc/%s/cmdline' % self.val['pid']).read(), '\0')
                l = string.split(open('/proc/%s/cmdline' % self.val['pid']).read(), '\0')
                if len(l) > 2:
                    self.val['process'] = os.path.basename(l[1])
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
        return '%s%-*s%s' % (ansi['default'], self.format[1]-4, self.val['process'][0:self.format[1]-4], cprint(self.val['usage'], ('f', 4, 1024)))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['usage'])

# vim:ts=4:sw=4:et
