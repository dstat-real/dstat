class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'snooze'
        self.vars = ('snooze',)
        self.type = 's'
        self.width = 6
        self.scale = 0
        self.before = time.time()

    def extract(self):
        now = time.time()
        if loop != 0:
            self.val['snooze'] = now - self.before
        else:
            self.val['snooze'] = self.before
        if step == op.delay:
            self.before = now

    def show(self):
        if self.val['snooze'] > step + 1:
            return ansi['default'] + '     -'

        if op.blackonwhite:
            textcolor = 'black'
            if step != op.delay:
                textcolor = 'darkgray'
        else:
            textcolor = 'white'
            if step != op.delay:
                textcolor = 'gray'

        snoze, c = fchg(self.val['snooze'], 6, 1000)

        return color[textcolor] + snoze
