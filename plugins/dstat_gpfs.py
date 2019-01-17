### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Total amount of read and write throughput (in bytes) on a GPFS filesystem.
    """

    def __init__(self):
        self.name = 'gpfs i/o'
        self.nick = ('read', 'write')
        self.vars = ('_br_', '_bw_')

    def check(self):
        if os.access('/usr/lpp/mmfs/bin/mmpmon', os.X_OK):
            try:
                self.stdin, self.stdout, self.stderr = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
                self.stdin.write('reset\n')
                readpipe(self.stdout)
            except IOError:
                raise Exception('Cannot interface with gpfs mmpmon binary')
            return True
        raise Exception('Needs GPFS mmpmon binary')

    def extract(self):
        try:
            self.stdin.write('io_s\n')
#           readpipe(self.stderr)
            for line in readpipe(self.stdout):
                if not line: continue
                l = line.split()
                for name in self.vars:
                    self.set2[name] = int(l[l.index(name)+1])
            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed
        except IOError as e:
            if op.debug > 1: print('%s: lost pipe to mmpmon, %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1
        except Exception as e:
            if op.debug > 1: print('%s: exception %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
