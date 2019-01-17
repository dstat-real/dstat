### Author: Vikas Gorur (http://github.com/vikasgorur)

class dstat_plugin(dstat):
    """
    Waiting calls on mounted FUSE filesystems

    Displays the number of waiting calls on all mounted FUSE filesystems.
    """

    def __init__(self):
        self.name = 'fuse'
        self.type = 'd'
        self.fusectl_path = "/sys/fs/fuse/connections/"
        self.dirs = []

    def check(self):
        info(1, "Module %s is still experimental." % self.filename)

        if not os.path.exists(self.fusectl_path):
            raise Exception('%s not mounted' % self.fusectl_path)
        if len(os.listdir(self.fusectl_path)) == 0:
            raise Exception('No fuse filesystems mounted')

    def vars(self):
        self.dirs = os.listdir(self.fusectl_path)

        atleast_one_ok = False
        for d in self.dirs:
            if os.access(self.fusectl_path + d + "/waiting", os.R_OK):
                atleast_one_ok = True

        if not atleast_one_ok:
            raise Exception('User is not root or no fuse filesystems mounted')

        return self.dirs

    def extract(self):
        for d in self.dirs:
            path = self.fusectl_path + d + "/waiting"
            if os.path.exists(path):
                line = dopen(path).readline()
                self.val[d] = int(line)
            else:
                self.val[d] = 0

# vim:ts=4:sw=4:et
