### Authority: dag@wieers.com

### For more information, see:
###     http://eaglet.rain.com/rick/linux/schedstat/

class dstat_plugin(dstat):
    """
    Name and average amount of CPU time consumed in milliseconds of the process
    that has the highest average amount of cputime for the different slices for
    the measured timeframe.

    On a system with one CPU and one core, the total cputime is 1000ms. On a
    system with two cores the total cputime is 2000ms.
    """

    def __init__(self):
        self.name = 'highest average'
        self.vars = ('cputime process',)
        self.type = 's'
        self.width = 17
        self.scale = 0
        self.pidset1 = {}

    def check(self):
        if not os.access('/proc/self/schedstat', os.R_OK):
            raise Exception, 'Kernel has no scheduler statistics [CONFIG_SCHEDSTATS], use at least 2.6.12'

    def extract(self):
        self.output = ''
        self.pidset2 = {}
        self.val['result'] = 0
        for pid in proc_pidlist():
            try:
                ### Reset values
                if not self.pidset1.has_key(pid):
                    self.pidset1[pid] = {'run_ticks': 0, 'ran': 0}

                ### Extract name
                name = proc_splitline('/proc/%s/stat' % pid)[1][1:-1]

                ### Extract counters
                l = proc_splitline('/proc/%s/schedstat' % pid)
            except IOError:
                continue
            except IndexError:
                continue

            if len(l) != 3: continue

            self.pidset2[pid] = {'run_ticks': long(l[0]), 'ran': long(l[2])}

            if self.pidset2[pid]['ran'] - self.pidset1[pid]['ran'] > 0:
                avgrun = (self.pidset2[pid]['run_ticks'] - self.pidset1[pid]['run_ticks']) * 1.0 / (self.pidset2[pid]['ran'] - self.pidset1[pid]['ran']) / elapsed
            else:
                avgrun = 0

            ### Get the process that spends the most jiffies
            if avgrun > self.val['result']:
                self.val['result'] = avgrun
                self.val['pid'] = pid
                self.val['name'] = getnamebypid(pid, name)

        if step == op.delay:
            self.pidset1 = self.pidset2

        if self.val['result'] != 0.0:
            self.output = '%-*s%s' % (self.width-4, self.val['name'][0:self.width-4], cprint(self.val['result'], 'f', 4, 100))

        ### Debug (show PID)
#       self.output = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

    def showcsv(self):
        return '%s / %.4f' % (self.val['name'], self.val['result'])

# vim:ts=4:sw=4:et
