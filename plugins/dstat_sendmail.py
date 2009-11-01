### FIXME: Should read /var/log/mail/statistics or /etc/mail/statistics (format ?)
global glob
import glob

class dstat_sendmail(dstat):
    def __init__(self):
        self.name = 'sendmail'
        self.type = 'd'
        self.width = 4
        self.scale = 100
        self.vars = ('queue',)
        self.nick = ('queu',)

    def check(self):
        if not os.access('/var/spool/mqueue', os.R_OK):
            raise Exception, 'Cannot access sendmail queue'

    def extract(self):
        self.val['queue'] = len(glob.glob('/var/spool/mqueue/qf*'))

# vim:ts=4:sw=4:et
