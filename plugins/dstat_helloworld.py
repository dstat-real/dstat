### Dstat Hello World plugin
### Displays hello world
###
### Authority: dag@wieers.com

class dstat_plugin(dstat):
    def __init__(self):
        self.type = 's'
        self.width = 12
        self.scale = 0
        self.name = 'plugin title'
        self.nick = ('counter',)
        self.vars = ('text',)

    def extract(self):
        self.val['text'] = 'Hello world!'

# vim:ts=4:sw=4:et
