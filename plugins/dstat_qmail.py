### Author: Tom Van Looy <tom$ctors,net>

class dstat_plugin(dstat):
    """
    port of qmail_qstat to dstat
    """
    def __init__(self):
        self.name = 'qmail'
        self.nick = ('in_queue', 'not_prep')
        self.vars = ('mess', 'todo')
        self.type = 'd'
        self.width = 4
        self.scale = 100

    def check(self):
        for item in self.vars:
            if not os.access('/var/qmail/queue/'+item, os.R_OK):
                raise Exception('Cannot access qmail queues')

    def extract(self):
        for item in self.vars:
            self.val[item] = len(glob.glob('/var/qmail/queue/'+item+'/*/*'))

# vim:ts=4:sw=4:et
