### Author: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Number of operations performed on a GPFS filesystem.
    """

    def __init__(self):
        self.name = 'gpfs file operations'
        self.nick = ('open', 'clos', 'read', 'writ', 'rdir', 'inod')
        self.vars = ('_oc_', '_cc_', '_rdc_', '_wc_', '_dir_', '_iu_')
        self.type = 'd'
        self.width = 5
        self.scale = 1000

    def check(self): 
        if os.access('/usr/lpp/mmfs/bin/mmpmon', os.X_OK):
            try:
                self.stdin, self.stdout, self.stderr = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
                self.stdin.write('reset\n')
                readpipe(self.stdout)
            except IOError:
                raise Exception, 'Cannot interface with gpfs mmpmon binary'
            return True
        raise Exception, 'Needs GPFS mmpmon binary'

    def extract(self):
        try:
            self.stdin.write('io_s\n')
#           readpipe(self.stderr)
            for line in readpipe(self.stdout):
                if not line: continue
                l = line.split()
                for name in self.vars:
                    self.set2[name] = long(l[l.index(name)+1])
            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed
        except IOError, e:
            if op.debug > 1: print '%s: lost pipe to mmpmon, %s' % (self.filename, e)
            for name in self.vars: self.val[name] = -1
        except Exception, e:
            if op.debug > 1: print '%s: exception %s' % (self.filename, e)
            for name in self.vars: self.val[name] = -1

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
