### Dstat Hello World plugin
### Displays hello world
###
### Authority: dag@wieers.com

class dstat_helloworld(dstat):
    def __init__(self):
        self.name = 'plugin title'
        self.format = ('s', 12, 0)
        self.nick = ('counter',)
        self.vars = ('text',)
        self.init(self.vars, 1)

    def extract(self):
        self.val['text'] = 'Hello world!'

# vim:ts=4:sw=4:et
