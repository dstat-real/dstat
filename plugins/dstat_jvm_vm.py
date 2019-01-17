# Author: Roberto Polli <rpolli@redhat.com>
#
# This plugin shows jvm stats using the JVM_PID environment variable.
# Requires the presence of the /tmp/hsperfdata_* directory and
#  files created when running java with the profiler enabled.
#


class dstat_plugin(dstat):

    def __init__(self):
        self.name = 'jvm mem ops '
        self.vars = ('fgc', 'heap', 'heap%', 'perm', 'perm%')
        self.type = 'f'
        self.width = 5
        self.scale = 1000

    def check(self):
        if not os.access('/usr/bin/jstat', os.X_OK):
            raise Exception('Needs jstat binary')
        try:
            self.jvm_pid = int(os.environ.get('JVM_PID', 0))
        except Exception:
            self.jvm_pid = 0

        return True

    @staticmethod
    def _to_float(s):
        return float(s.replace(",", "."))

    @staticmethod
    def _cmd_splitlines(cmd):
        for l in os.popen(cmd):
            yield l.strip().split()

    def extract(self):
        from collections import namedtuple
        try:
            lines = self._cmd_splitlines(
                '/usr/bin/jstat -gc %s' % self.jvm_pid)
            headers = next(lines)
            DStatParser = namedtuple('DStatParser', headers)
            line = next(lines)
            if line:
                stats = DStatParser(*[self._to_float(x) for x in line])
                # print(stats)
                self.set2['cls'] = 0
                self.set2['fgc'] = int(stats.FGC)
                self.set2['heap'] = (
                    stats.S0C + stats.S1C + stats.EC + stats.OC)
                self.set2['heapu'] = (
                    stats.S0U + stats.S1U + stats.EU + stats.OU)

                # Use MetaSpace on jdk8
                try:
                    self.set2['perm'] = stats.PC
                    self.set2['permu'] = stats.PU
                except AttributeError:
                    self.set2['perm'] = stats.MC
                    self.set2['permu'] = stats.MU

            # Evaluate statistics on memory usage.
            for name in ('heap', 'perm'):
                self.set2[name + '%'] = 100 * self.set2[
                    name + 'u'] / self.set2[name]
                self.set2[name] /= 1024

            for name in self.vars:
                self.val[name] = self.set2[name]

            if step == op.delay:
                self.set1.update(self.set2)

        except IOError as e:
            if op.debug > 1:
                print('%s: lost pipe to jstat, %s' % (self.filename, e))
            for name in self.vars:
                self.val[name] = -1

        except Exception as e:
            if op.debug > 1:
                print('%s: exception' % e)
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
