# Author: Roberto Polli <rpolli@redhat.com>
#
# NOTE: Edit the jcmd location according to your path or use update-alternatives.
global BIN_JCMD
BIN_JCMD = '/usr/bin/jcmd'


class dstat_plugin(dstat):
    """
    This plugin gathers jvm stats via jcmd.

    Usage:
       JVM_PID=15123 dstat --jvm-full 

    Minimize the impacts of jcmd and consider using:

        dstat --noupdate

    For full informations on jcmd see:

      - http://docs.oracle.com/javase/7/docs/technotes/tools/solaris/jcmd.html
      - https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr006.html

    This requires the presence of /tmp/hsperfdata_* directory, so
     it WON'T WORK if you add -XX:-UsePerfData or -XX:+PerfDisableSharedMem.

    """

    def __init__(self):
        self.name = 'jvm_full'
        self.vars = ('clsL', 'clsU', 'fgc', 'heap', 'heap%',
                     'heapmax', 'perm', 'perm%', 'permmax')
        self.type = 'f'
        self.width = 5
        self.scale = 1000

    def check(self):
        """Preliminar checks. If no pid is passed, defaults to 0.
        """
        if not os.access(BIN_JCMD, os.X_OK):
            raise Exception('Needs jstat binary')

        try:
            self.jvm_pid = int(os.environ.get('JVM_PID',0))
        except Exception as e:
            self.jvm_pid = 0

        return True

    @staticmethod
    def _to_stat(k, v):
        try:
            return k, int(v)
        except (KeyError, ValueError, AttributeError):
            return k, v

    @staticmethod
    def _cmd_splitlines(cmd):
        """Splits a txt output of lines like key=value.
        """
        for l in os.popen(cmd):
            yield l.strip().split("=", 1)

    def extract(self):
        try:
            lines = self._cmd_splitlines(
                '%s %s PerfCounter.print ' % (BIN_JCMD, self.jvm_pid))
            table = dict(self._to_stat(*l) for l in lines
                         if len(l) > 1)
            if table:
                # Number of loaded classes.
                self.set2['clsL'] = table['java.cls.loadedClasses']
                self.set2['clsU'] = table['java.cls.unloadedClasses']
                # Number of Full Garbage Collection events.
                self.set2['fgc'] = table['sun.gc.collector.1.invocations']
                # The heap space is made up of Old Generation and Young
                # Generation (which is divided in Eden, Survivor0 and
                # Survivor1)
                self.set2['heap'] = table['sun.gc.generation.1.capacity'] + table[
                    'sun.gc.generation.0.capacity']
                # Usage is hidden in the nested spaces.
                self.set2['heapu'] = sum(table[k] for k in table
                                         if 'sun.gc.generation.' in k
                                         and 'used' in k)
                self.set2['heapmax'] = table['sun.gc.generation.1.maxCapacity'] + table[
                    'sun.gc.generation.0.maxCapacity']

                # Use PermGen on jdk7 and the new metaspace on jdk8
                try:
                    self.set2['perm'] = table['sun.gc.generation.2.capacity']
                    self.set2['permu'] = sum(table[k] for k in table
                                             if 'sun.gc.generation.2.' in k
                                             and 'used' in k)
                    self.set2['permmax'] = table[
                        'sun.gc.generation.2.maxCapacity']
                except KeyError:
                    self.set2['perm'] = table['sun.gc.metaspace.capacity']
                    self.set2['permu'] = table['sun.gc.metaspace.used']
                    self.set2['permmax'] = table[
                        'sun.gc.metaspace.maxCapacity']

            # Evaluate statistics on memory usage.
            for name in ('heap', 'perm'):
                self.set2[name + '%'] = 100 * self.set2[
                    name + 'u'] / self.set2[name]

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
