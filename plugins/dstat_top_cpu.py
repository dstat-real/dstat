### Authority: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    """
    Most expensive CPU process.

    Displays the process that uses the CPU the most during the monitored
    interval. The value displayed is the percentage of CPU time for the total
    amount of CPU processing power. Based on per process CPU information.
    """
    def __init__(self):
        self.name = 'most expensive'
        self.vars = ('cpu process',)
        self.type = 's'
        self.width = 16
        self.scale = 0
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
#                l = open('/proc/%s/stat' % pid).read().split()
                l = linecache.getline('/proc/%s/stat' % pid, 1).split()

            except ValueError:
                continue
            except IOError:
                continue

            if len(l) < 15: continue

            ### Reset previous value if it doesn't exist
            if not self.pidset1.has_key(pid):
                self.pidset1[pid] = 0

            self.pidset2[pid] = long(l[13]) + long(l[14])
            usage = (self.pidset2[pid] - self.pidset1[pid]) * 1.0 / elapsed / cpunr

            ### Is it a new topper ?
            if usage < self.val['max']: continue

            name = l[1][1:-1]

            self.val['max'] = usage
            self.val['pid'] = pid
#            self.val['name'] = getnamebypid(pid, name)
            self.val['name'] = name

        if self.val['max'] != 0.0:
            self.val['cpu process'] = '%-*s%s' % (self.width-3, self.val['name'][0:self.width-3], cprint(self.val['max'], 'f', 3, 34))

        ### Debug (show PID)
#        self.val['cpu process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            self.pidset1.update(self.pidset2)

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
