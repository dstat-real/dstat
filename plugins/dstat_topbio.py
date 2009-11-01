### Dstat most expensive block I/O process plugin
### Displays the name of the most expensive block I/O process
###
### Authority: dag@wieers.com

class dstat_topbio(dstat):
    def __init__(self):
        self.name = 'most expensive'
        self.type = 's'
        self.width = 22
        self.scale = 0
        self.nick = ('block i/o process',)
        self.vars = self.nick
        self.pid = str(os.getpid())
        self.pidset1 = {}; self.pidset2 = {}

    def check(self):
        if not os.access('/proc/self/io', os.R_OK):
            raise Exception, 'Kernel has no I/O accounting, use at least 2.6.20'

    def extract(self):
        self.val['usage'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Reset values
                if not self.pidset2.has_key(pid):
                    self.pidset2[pid] = {'read_bytes:': 0, 'write_bytes:': 0}
                if not self.pidset1.has_key(pid):
                    self.pidset1[pid] = {'read_bytes:': 0, 'write_bytes:': 0}

                ### Extract name
                name = open('/proc/%s/stat' % pid).read().split()[1][1:-1]

                ### Extract counters
                for line in open('/proc/%s/io' % pid).readlines():
                    l = line.split()
                    if len(l) != 2: continue
                    self.pidset2[pid][l[0]] = int(l[1])

            except ValueError:
                continue
            except IOError:
                continue

            read_usage = (self.pidset2[pid]['read_bytes:'] - self.pidset1[pid]['read_bytes:']) * 1.0 / tick
            write_usage = (self.pidset2[pid]['write_bytes:'] - self.pidset1[pid]['write_bytes:']) * 1.0 / tick
            usage = read_usage + write_usage

            ### Get the process that spends the most jiffies
            if usage > self.val['usage']:
                self.val['usage'] = usage
                self.val['read_usage'] = read_usage
                self.val['write_usage'] = write_usage
                self.val['pid'] = pid
                self.val['name'] = name
#                st = os.stat("/proc/%s" % pid)

        if self.val['usage'] == 0.0:
            self.val['process'] = ''
        else:
            self.val['process'] = os.path.basename(self.val['name'])

        ### Debug (show PID)
#       self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            for pid in self.pidset2.keys():
                self.pidset1[pid].update(self.pidset2[pid])

    def show(self):
        if self.val['usage'] == 0.0:
            return '%-*s' % (self.width, '')
        else:
            return '%s%-*s%s:%s' % (ansi['default'], self.width-11, self.val['process'][0:self.width-11], cprint(self.val['read_usage'], 'f', 5, 1024), cprint(self.val['write_usage'], 'f', 5, 1024))

    def showcsv(self):
        return '%s / %d:%d' % (self.val['name'], self.val['read_usage'], self.val['write_usage'])

# vim:ts=4:sw=4:et
