global string, select
import string, select

class dstat_gpfs(dstat):
	def __init__(self):
		self.name = 'gpfs i/o'
		self.format = ('f', 5, 1024)
		self.vars = ('_br_', '_bw_')
		self.nick = ('read', 'write')
		self.init(self.vars, 1)

	def check(self): 
		if os.access('/usr/lpp/mmfs/bin/mmpmon', os.X_OK):
			try:
				self.stdin, self.stdout, self.stderr = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
				self.stdin.write('reset\n')
				readpipe(self.stdout)
			except IOError:
				raise Exception, 'Module can not interface with gpfs mmpmon binary'
			return True
		raise Exception, 'Module needs gpfs mmpmon binary'

	def extract(self):
		try:
			self.stdin.write('io_s\n')
#			readpipe(self.stderr)
			for line in readpipe(self.stdout):
				if not line: continue
				l = line.split()
				for name in self.vars:
					self.cn2[name] = long(l[l.index(name)+1])
			for name in self.vars:
				self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick
		except IOError, e:
			for name in self.vars: self.val[name] = -1
#			print 'dstat_gpfs: lost pipe to mmpmon,', e
		except Exception, e:
			for name in self.vars: self.val[name] = -1
#			print 'dstat_gpfs: exception', e

		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
