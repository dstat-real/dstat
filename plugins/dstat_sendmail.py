### Author: Dag Wieers <dag@wieers.com>

### FIXME: Should read /var/log/mail/statistics or /etc/mail/statistics (format ?)

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'sendmail'
        self.vars = ('queue',)
        self.type = 'd'
        self.width = 4
        self.scale = 100

    def check(self):
        if not os.access('/var/spool/mqueue', os.R_OK):
            raise Exception('Cannot access sendmail queue')

    def extract(self):
        self.val['queue'] = len(glob.glob('/var/spool/mqueue/qf*'))

# vim:ts=4:sw=4:et
