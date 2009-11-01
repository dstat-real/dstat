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
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
                l = open('/proc/%s/stat' % pid).read().split()
                if len(l) < 15: continue

                ### Reset previous value if it doesn't exist
                if not self.pidset1.has_key(pid):
                    self.pidset1[pid] = 0

                self.pidset2[pid] = int(l[13]) + int(l[14])
                usage = (self.pidset2[pid] - self.pidset1[pid]) * 1.0 / tick / cpunr

                ### Is it a new topper ?
                if usage < self.val['max']: continue

                ### Extract name
                name = l[1][1:-1]

            except ValueError:
                continue
            except IOError:
                continue

            self.val['max'] = usage
            self.val['name'] = name
            self.val['pid'] = pid
#            st = os.stat("/proc/%s" % pid)
#            if st:
#                pw = pwd.getpwuid(st.st_uid)
#                if pw:
#                    self.val['user'] = pw[0]
#                else:
#                    self.val['user'] = stat.st_uid
#            else:
#                self.val['user'] = 'none'

        if self.val['max'] == 0.0:
            self.val['process'] = ''
        else:
            self.val['process'] = self.val['name']

#               l = l.reverse()
#               for x in l:
#                   print x
#                   if x[0] != '-':
#                       self.val['name'] = os.path.basename(x)
#                       break

        ### Debug (show PID)
#       self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            self.pidset1.update(self.pidset2)

        if self.val['max'] == 0.0:
            self.val['cpu process'] = ''
        else:
            self.val['cpu process'] = '%-*s%s' % (self.width-3, self.val['process'][0:self.width-3], cprint(self.val['max'], 'p', 3, 34))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
