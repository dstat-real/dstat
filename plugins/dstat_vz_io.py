### Author: Dag Wieers <dag@wieers.com>

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

class dstat_plugin(dstat):
    def __init__(self):
        self.nick = ['read', 'write', 'dirty', 'cancel', 'missed']
        self.cols = len(self.nick)

    def check(self):
        if not os.path.exists('/proc/vz'):
            raise Exception('System does not have OpenVZ support')
        elif not os.path.exists('/proc/bc'):
            raise Exception('System does not have (new) OpenVZ beancounter support')
        elif not glob.glob('/proc/bc/*/ioacct'):
            raise Exception('System does not have any OpenVZ containers')
        info(1, 'Module %s is still experimental.' % self.filename)

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
        for name in self.vars:
            self.set2['total'] = {}
            for line in dopen('/proc/bc/%s/ioacct' % name).readlines():
                l = line.split()
                if len(l) != 2: continue
                if l[0] not in self.nick: continue
                index = self.nick.index(l[0])
                self.set2[name][index] = int(l[1])
                self.set2['total'][index] = self.set2['total'][index] + int(l[1])
#            print(name, self.val[name], self.set2[name][0], self.set2[name][1])
#            print(name, self.val[name], self.set1[name][0], self.set1[name][1])

            self.val[name] = list(map(lambda x, y: (y - x) / elapsed, self.set1[name], self.set2[name]))

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
