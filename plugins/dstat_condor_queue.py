### Author: <krikava$gmail,com>

### Condor queue plugin
### Display information about jobs in queue (using condor_q(1))
###
### WARNING: with many jobs in the queue, the condor_q might take quite
### some time to execute and use quite a bit of resources. Consider
### using a longer delay.

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

    global CONDOR_Q_STAT_PATTER
    CONDOR_Q_STAT_PATTER = re.compile(r'(\d+) jobs; (\d+) idle, (\d+) running, (\d+) held')

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

        self.condor_status_cmd = os.path.join(bin_dir, 'condor_q')

        if not os.access(self.condor_status_cmd, os.X_OK):
            raise Exception, 'Needs %s in the path' % self.condor_status_cmd
        else:
            try:
                p = os.popen(self.condor_status_cmd+' 2>&1 /dev/null')
                ret = p.close()
                if ret:
                    raise Exception, 'Cannot interface with Condor - condor_q returned != 0?'
            except IOError:
                raise Exception, 'Unable to execute %s' % self.condor_status_cmd
            return True

    def extract(self):
        last_line = None

        try:
	    for repeats in range(3):
                for last_line in cmd_readlines(self.condor_status_cmd):
                    pass

                m = CONDOR_Q_STAT_PATTER.match(last_line)
                if m == None:
                    raise Exception, 'Invalid output from %s. Got: %s' % (cmd, last_line)

                stats = [int(s.strip()) for s in m.groups()]
                for i,j in enumerate(self.vars):
                    self.val[j] = stats[i]
        except Exception:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
