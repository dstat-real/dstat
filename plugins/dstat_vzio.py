### Example content for /proc/bc/<veid>/ioacct
#       read                         2773011640320
#       write                        2095707136000
#       dirty                        4500342390784
#       cancel                       4080624041984
#       missed                                   0
#       syncs_total                              2
#       fsyncs_total                       1730732
#       fdatasyncs_total                      3266
#       range_syncs_total                        0
#       syncs_active                             0
#       fsyncs_active                            0
#       fdatasyncs_active                        0
#       range_syncs_active                       0
#       vfs_reads                       3717331387
#       vfs_read_chars         3559144863185798078
#       vfs_writes                       901216138
#       vfs_write_chars          23864660931174682
#       io_pbs                                  16

class dstat_vzio(dstat):
    def __init__(self):
        self.nick = ['read', 'write']
        self.cols = 2
        info(1, 'Module dstat_vzio is still experimental.')

    def name(self):
        return ['ve/'+name for name in self.vars]

    def vars(self):
        ret = []
        if not op.full:
            varlist = ['total',]
        else:
            varlist = [os.path.basename(veid) for veid in glob.glob('/proc/vz/*')]
        ret = varlist
        return ret

    def extract(self):
        global update
        for veid in self.vars:
            self.set2['total'] = {}
            for line in dopen('/proc/bc/%s/ioacct' % veid).readlines():
#            for line in dopen('ioacct.%d' % (update % 3)).readlines():
                l = line.split()
                if len(l) != 2: continue
                if l[0] not in self.nick: continue
                index = self.nick.index(l[0])
                self.set2[veid][index] = long(l[1])
                self.set2['total'][index] = self.set2['total'][index] + long(l[1])
#            print veid, self.val[veid], self.set2[veid][0], self.set2[veid][1]
#            print veid, self.val[veid], self.set1[veid][0], self.set1[veid][1]
            self.val[veid] = (
                (self.set2[veid][0] - self.set1[veid][0]) / tick,
                (self.set2[veid][1] - self.set1[veid][1]) / tick,
            )
        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
