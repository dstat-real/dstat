global string, popen2
import string, popen2

class dstat_gpfs(dstat):
	def __init__(self):
		self.name = 'gpfs i/o'
		self.format = ('f', 5, 1024)
		self.vars = ('read', 'write')
		self.nick = self.vars
		self.init(self.vars, 1)

	def check(self): 
		if os.access('/usr/lpp/mmfs/bin/mmpmon', os.X_OK):
			try:
				self.stdout, self.stdin, self.stderr = popen2.popen3('/usr/lpp/mmfs/bin/mmpmon', 0)
			except IOError:
				raise Exception, 'Module can not interface with gpfs mmpmon binary'
			return True
		raise Exception, 'Module needs gpfs mmpmon binary'
		return false

	def extract(self):
		try:
			self.stdout.flush()
			self.stdin.write('io_s\n'); size = 290
#			self.stdin.write('fs_io_s\n'); size = 370
			for line in self.stdout.read(size).split('\n'):
				l = line.split()
				if len(l) != 3: continue
#				print l
				name = l[0:2]
				if name == ['bytes','read:']:
					self.cn2['read'] = long(l[2])
				elif name == ['bytes','written:']:
					self.cn2['write'] = long(l[2])
		except IOError, e:
			print e
		for name in self.vars:
			self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick
		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
