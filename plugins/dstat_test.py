### Author: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    '''
    Provides a test playground to test syntax and structure.
    '''
    def __init__(self):
        self.name = 'test'
        self.nick = ( 'f1', 'f2' )
        self.vars = ( 'f1', 'f2' )
#        self.type = 'd'
#        self.width = 4
#        self.scale = 20
        self.type = 's'
        self.width = 4
        self.scale = 0

    def extract(self):
#        Self.val = { 'f1': -1, 'f2': -1 }
        self.val = { 'f1': 'test', 'f2': 'test' }

# vim:ts=4:sw=4:et
