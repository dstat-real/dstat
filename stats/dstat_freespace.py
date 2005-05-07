import dstat, os

### FIXME: This module needs infrastructure to provide a list of mountpoints

class dstat_freespace(dstat.dstat):
	def __init__(self):
		self.format = ('f', 5, 1024)
		self.open('/etc/mtab')
		self.vars = self.vars()
		self.name = ['/' + os.path.basename(name) for name in self.vars]
		self.nick = ('avail', 'free')
		self.init(self.vars, 2)

	def vars(self):
		ret = []
		if self.fd:
			self.fd.seek(0)
			for line in self.fd.readlines():
				l = line.split()
				if len(l) < 6: continue
				if l[0] in ('none', 'usbfs', 'sunrpc'): continue
				name = l[1] 
				ret.append(name)
		return ret

	def extract(self):
		for name in self.vars:
			res = os.statvfs(name)
			self.val[name] = ( long(res[3]) * long(res[0]), long(res[2]) * long(res[0]) )

# vim:ts=4:sw=4
