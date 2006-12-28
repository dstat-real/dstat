global string
import string

class dstat_vzubc(dstat):
	def __init__(self):
		self.format = ('d', 5, 1000)
		self.open('/proc/user_beancounters')
		self.nick = ('fcnt', )
		self.discover = self.discover()
		self.vars = self.vars()
		self.name = self.name()
		self.init(self.vars + ['total'], 1)
		info(1, 'Module dstat_vzubc is still experimental.')

	def discover(self, *list):
		ret = []
		for line in self.readlines():
			l = line.split()
			if len(l) < 7 or l[0] in ('uid', '0:'): continue
			ret.append(l[0][0:-1])
		ret.sort()
		for item in list: ret.append(item)
		return ret

	def name(self):
		ret = []
		for name in self.vars:
			if name == 'total':
				ret.append('total failcnt')
			else:
				ret.append(name)
		return ret

	def vars(self):
		ret = []
		if not op.full:
			list = ('total', )
		else: 
			list = self.discover
		for name in list: 
			if name in self.discover + ['total']:
				ret.append(name)
		return ret

	def extract(self):
		for name in self.vars + ['total']:
			self.cn2[name] = 0
		for line in self.readlines():
			l = line.split() 
			if len(l) < 6 or l[0] == 'uid':
				continue
			elif len(l) == 7:
				name = l[0][0:-1]
				if name in self.vars:
					self.cn2[name] = self.cn2[name] + long(l[6])
				self.cn2['total'] = self.cn2['total'] + long(l[6])
			elif name == '0':
				continue
			else:
				if name in self.vars:
					self.cn2[name] = self.cn2[name] + long(l[5])
				self.cn2['total'] = self.cn2['total'] + long(l[5])
		for name in self.vars:
			self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick
		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
