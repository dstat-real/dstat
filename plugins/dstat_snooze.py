class dstat_snooze(dstat):
    def __init__(self):
        self.name = 'snooze'
        self.format = ('s', 6, 0)
        self.nick = ('snooze',)
        self.vars = self.nick
        self.init(self.vars, 1)

    def extract(self):
        self.val['snooze'] = tick

    def show(self):
        if self.val['snooze'] > step + 1:
            return ansi['default'] + '     -'
        color = 'white'
        if step != op.delay:
            color = 'gray'
        snoze, c = fchg(self.val['snooze'], 7, 1000)
        return ansi[color] + snoze
