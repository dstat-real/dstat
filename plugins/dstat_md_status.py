### Author: Bert de Bruijn <bert+dstat@debruijn.be>

class dstat_plugin(dstat):
    """
    Recovery state of software RAID rebuild.

    Prints completed recovery percentage and rebuild speed of the md device
    that is actively being recovered or resynced.

    If no devices are being rebuilt, it displays 100%, 0B. If instead
    multiple devices are being rebuilt, it displays the total progress
    and total throughput.
    """

    def __init__(self):
        self.name = 'sw raid'
        self.type = 's'
        self.scale = 0
        self.nick = ('pct speed', )
        self.width = 9
        self.vars = ('text', )
        self.open('/proc/mdstat')

    def check(self):
        if not os.path.exists('/proc/mdstat'):
            raise Exception('Needs kernel md support')

    def extract(self):
        pct = 0
        speed = 0
        nr = 0
        for l in self.splitlines():
            if len(l) < 2: continue
            if l[1] in ('recovery', 'reshape', 'resync'):
                nr += 1
                pct += int(l[3][0:2].strip('.%'))
                speed += int(l[6].strip('sped=K/sc')) * 1024
        if nr:
            pct = pct / nr
        else:
            pct = 100
        self.val['text'] = '%s %s' % (cprint(pct, 'p', 3, 34), cprint(speed, 'd', 5, 1024))

# vim:ts=4:sw=4:et
