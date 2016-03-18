### Author: Adam Michel <elfurbe@furbism.com>
### Based on work by: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'nfs4 server'
        # this vars/nick pair is the ones I considered relevant. Any set of the full list would work.
        self.vars = ('read','write','readdir','getattr','setattr','commit','getfh','putfh',
                'savefh','restorefh','open','open_conf','close','access','lookup','remove')
        self.nick = ('read', 'writ', 'rdir', 'gatr','satr','cmmt','gfh','pfh','sfh','rfh',
                'open','opnc','clse','accs','lkup','rem')
        # this is every possible variable for NFSv4 server if you're into that
        #self.vars4 = ('op0-unused', 'op1-unused', 'op2-future' , 'access',
        #        'close', 'commit', 'create', 'delegpurge', 'delegreturn', 'getattr', 'getfh',
        #        'link', 'lock', 'lockt', 'locku', 'lookup', 'lookup_root', 'nverify', 'open',
        #        'openattr', 'open_conf', 'open_dgrd','putfh', 'putpubfh', 'putrootfh',
        #        'read', 'readdir', 'readlink', 'remove', 'rename','renew', 'restorefh',
        #        'savefh', 'secinfo', 'setattr', 'setcltid', 'setcltidconf', 'verify', 'write',
        #        'rellockowner')
        # I separated the NFSv41 ops cause you know, completeness.
        #self.vars41 = ('bc_ctl', 'bind_conn', 'exchange_id', 'create_ses',
        #        'destroy_ses', 'free_stateid', 'getdirdeleg', 'getdevinfo', 'getdevlist',
        #        'layoutcommit', 'layoutget', 'layoutreturn', 'secinfononam', 'sequence',
        #        'set_ssv', 'test_stateid', 'want_deleg', 'destroy_clid', 'reclaim_comp')
        # Just catin' the tuples together to make the full list.
        #self.vars = self.vars4 + self.vars41
        # these are terrible shortnames for every possible variable
        #self.nick4 = ('unsd','unsd','unsd','accs','clse','comm','crt','delp','delr','gatr','gfh',
        #        'link','lock','lckt','lcku','lkup','lkpr','nver','open','opna','opnc','opnd',
        #        'pfh','ppfh','prfh','read','rdir','rlnk','rmv','ren','rnw','rfh','sfh','snfo',
        #        'satr','scid','scic','ver','wrt','rlko')
        #self.nick41 = ('bctl','bcon','eid','cses','dses','fsid',
        #        'gdd','gdi','gdl','lcmt','lget','lrtn','sinn','seq','sets','tsts','wdel','dcid',
        #        'rcmp')
        #self.nick = self.nick4 + self.nick41
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open("/proc/net/rpc/nfsd")

    def check(self):
        # other NFS modules had this, so I left it. It seems to work.
        info(1, 'Module %s is still experimental.' % self.filename)

    def extract(self):
        # list of fields from /proc/net/rpc/nfsd, in order of output 
        # taken from include/linux/nfs4.h in kernel source
        nfsd4_names = ('label', 'fieldcount', 'op0-unused', 'op1-unused', 'op2-future' , 'access',
                'close', 'commit', 'create', 'delegpurge', 'delegreturn', 'getattr', 'getfh',
                'link', 'lock', 'lockt', 'locku', 'lookup', 'lookup_root', 'nverify', 'open',
                'openattr', 'open_conf', 'open_dgrd','putfh', 'putpubfh', 'putrootfh',
                'read', 'readdir', 'readlink', 'remove', 'rename','renew', 'restorefh',
                'savefh', 'secinfo', 'setattr', 'setcltid', 'setcltidconf', 'verify', 'write',
                'rellockowner', 'bc_ctl', 'bind_conn', 'exchange_id', 'create_ses',
                'destroy_ses', 'free_stateid', 'getdirdeleg', 'getdevinfo', 'getdevlist',
                'layoutcommit', 'layoutget', 'layoutreturn', 'secinfononam', 'sequence',
                'set_ssv', 'test_stateid', 'want_deleg', 'destroy_clid', 'reclaim_comp'
                )

        for line in self.splitlines():
            fields = line.split()

            if fields[0] == "proc4ops": # just grab NFSv4 stats
                assert int(fields[1]) == len(fields[2:]), ("reported field count (%d) does not match actual field count (%d)" % (int(fields[1]), len(fields[2:])))
                for var in self.vars:
                    self.set2[var] = fields[nfsd4_names.index(var)]

        for name in self.vars:
            self.val[name] = (int(self.set2[name]) - int(self.set1[name])) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
