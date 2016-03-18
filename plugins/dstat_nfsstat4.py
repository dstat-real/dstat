### Author: Adam Michel <elfurbe@furbism.com>
### Based on work by: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'nfs4 client'
        # this vars/nick pair is the ones I considered relevant. Any set of the full list would work.
        self.vars = ('read', 'write', 'readdir', 'commit', 'getattr', 'create', 'link','remove')
        self.nick = ('read', 'writ', 'rdir', 'cmmt', 'gatr','crt','link','rmv')
        # this is every possible variable if you're into that
        #self.vars = ("read", "write", "commit", "open", "open_conf", "open_noat", "open_dgrd", "close", 
        #        "setattr", "fsinfo", "renew", "setclntid", "confirm", "lock", "lockt", "locku", 
        #        "access", "getattr", "lookup", "lookup_root", "remove", "rename", "link", "symlink", 
        #        "create", "pathconf", "statfs", "readlink", "readdir", "server_caps", "delegreturn", 
        #        "getacl", "setacl", "fs_locations", "rel_lkowner", "secinfo")
        # these are terrible shortnames for every possible variable
        #self.nick = ("read", "writ", "comt", "open", "opnc", "opnn", "opnd", "clse", "seta", "fnfo", 
        #        "renw", "stcd", "cnfm", "lock", "lckt", "lcku", "accs", "gatr", "lkup", "lkp_r", 
        #        "rem", "ren", "lnk", "slnk", "crte", "pthc", "stfs", "rdlk", "rdir", "scps", "delr", 
        #        "gacl", "sacl", "fslo", "relo", "seco")
        self.type = 'd'
        self.width = 5
        self.scale = 1000
        self.open('/proc/net/rpc/nfs')

    def check(self):
        # other NFS modules had this, so I left it. It seems to work.
        info(1, 'Module %s is still experimental.' % self.filename)

    def extract(self):
        # list of fields from nfsstat, in order of output from cat /proc/net/rpc/nfs 
        nfs4_names = ("version", "fieldcount", "null", "read", "write", "commit", "open", "open_conf",
                "open_noat", "open_dgrd", "close", "setattr", "fsinfo", "renew", "setclntid",
                "confirm", "lock", "lockt", "locku", "access", "getattr", "lookup", "lookup_root",
                "remove", "rename", "link", "symlink", "create", "pathconf", "statfs", "readlink",
                "readdir", "server_caps", "delegreturn", "getacl", "setacl", "fs_locations",
                "rel_lkowner", "secinfo")
        for line in self.splitlines():

            fields = line.split()
            if fields[0] == "proc4": # just grab NFSv4 stats
                assert int(fields[1]) == len(fields[2:]), ("reported field count (%d) does not match actual field count (%d)" % (int(fields[1]), len(fields[2:])))
                for var in self.vars:
                    self.set2[var] = fields[nfs4_names.index(var)]

        for name in self.vars:
            self.val[name] = (int(self.set2[name]) - int(self.set1[name])) * 1.0 / elapsed

        if step == op.delay:
            self.set1.update(self.set2)

# vim:ts=4:sw=4:et
