### Author: <krikava$gmail,com>

### Condor queue plugin
### Display information about jobs in queue (using condor_q(1))
import os
import re

global condor_classad

class condor_classad:
    """
    Utility class to work with Condor ClassAds
    """

    global ATTR_VAR_PATTERN
    ATTR_VAR_PATTERN = re.compile(r'\$\((\w+)\)')

    def __init__(self, file=None, config=None):
        if file != None:
            self.attributes = condor_classad._read_from_file(file)
        elif config != None:
            self.attributes = condor_classad._parse(config)

        if self.attributes == None:
            raise Exception, 'condor_config must be initialized either using a file or config text'

        local_config_file = self['LOCAL_CONFIG_FILE']

        if local_config_file != None:
            for k,v in condor_classad._read_from_file(local_config_file).items():
                self.attributes[k] = v

    def __getitem__(self, name):
        if name in self.attributes:
            self._expand(name)
        return self.attributes[name]

    def _expand(self, var):
        if not var in self.attributes:
            return

        while True:
            m = ATTR_VAR_PATTERN.match(self.attributes[var])
            if m == None:
                break
            var_name = m.group(1)
            self.attributes[var] = ATTR_VAR_PATTERN.sub(self.attributes[var_name],
                                                          self.attributes[var])

    @staticmethod
    def _parse(text):
        attributes = {}
        for l in [l for l in text.split('\n') if not l.strip().startswith('#')]:
            l = l.split('=')
            if len(l) <= 1 or len(l[0]) == 0:
                continue
            attributes[l[0].strip()] = ''.join(l[1:]).strip()
        return attributes

    @staticmethod
    def _read_from_file(filename):
        if not os.access(filename, os.R_OK):
            raise Exception, 'Unable to read file %s' % filename
        try:
            f = open(filename)
            return condor_classad._parse((f.read()))
        finally:
            f.close()

class dstat_plugin(dstat):
    """
    Plugin for Condor queue stats
    """

    global CONDOR_STATUS
    CONDOR_STATUS = 'condor_status'
    global CONDOR_STATUS_ARGS
    CONDOR_STATUS_ARGS = r' -schedd -format "%d:" TotalIdleJobs -format "%d:" TotalRunningJobs -format "%d\n" TotalHeldJobs'

    def __init__(self):
        self.name = 'condor queue'
        self.vars = ('jobs', 'idle', 'running', 'held')
        self.type = 'd'
        self.width = 5
        self.scale = 1
        self.condor_config = None

    def check(self):
        config_file = os.environ['CONDOR_CONFIG']
        if config_file == None:
            raise Exception, 'Environment varibale CONDOR_CONFIG is missing'
        self.condor_config = condor_classad(config_file)

        bin_dir = self.condor_config['BIN']
        if bin_dir == None:
            raise Exception, 'Unable to find BIN directory in condor config file %s' % config_file

        self.condor_status_cmd = os.path.join(bin_dir, CONDOR_STATUS)

        if not os.access(self.condor_status_cmd, os.X_OK):
            raise Exception, 'Needs %s in the path' % self.condor_status_cmd
        cmd_test(self.condor_status_cmd)
        return True

    def extract(self):
        cmd = self.condor_status_cmd+CONDOR_STATUS_ARGS
        stats = cmd_splitlines(cmd,':').next()
        if len(stats) != 3:
           raise Exception, 'Invalid output from %s. Expected: \d+:\d+\d+, got: %s' % (cmd, stats)

        stats = [int(s.strip()) for s in stats]
        for i,j in enumerate(self.vars[1:]):
            self.val[j] = stats[i]

        self.val['jobs'] = sum(stats)

# vim:ts=4:sw=4:et
