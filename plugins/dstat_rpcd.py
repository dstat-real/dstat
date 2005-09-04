global string
import string

class dstat_rpcd(dstat):
	def __init__(self):
		self.name = 'rpc server'
		self.format = ('d', 4, 1000)
		self.open('/proc/net/rpc/nfsd')
		self.vars = ('calls', 'badcalls', 'badauth', 'badclnt', 'xdrcall')
		self.nick = ('call', 'erca', 'erau', 'ercl', 'xdrc')
		self.init(self.vars, 1)

	def extract(self):
		self.fd.seek(0)
		for line in self.fd.readlines():
			l = line.split()
			if not l or l[0] != 'rpc': continue
			for i, name in enumerate(self.vars):
				self.cn2[name] = long(l[i+1])
		for name in self.vars:
			self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick
		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
