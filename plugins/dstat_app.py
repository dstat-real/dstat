### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

### FIXME: The val, cn1 and cn2 will only grow and consume more memory.

global string
import string

class dstat_app(dstat):
	def __init__(self):
		self.name = 'most expensive'
		self.format = ('s', 15, 0)
		self.nick = ('process',)
		self.vars = self.nick
		self.cn1 = {}; self.cn2 = {}; self.val = {}

	def extract(self):
		max = 0
		for pid in os.listdir('/proc/'):
			try: int(pid)
			except: continue
			if os.path.exists('/proc/%s/stat' % pid):
				if not self.cn1.has_key(pid):
					self.cn1[pid] = 0

				for line in dopen('/proc/%s/stat' % pid).readlines():
					l = string.split(line)
					if len(l) < 15: continue
					self.cn2[pid] = int(l[13]) + int(l[14])
				self.val[pid] = (self.cn2[pid] - self.cn1[pid]) * 1.0 / tick

				### Get the process that spends the most jiffies
				if self.val[pid] > max:
					max = self.val[pid]
					self.val['process'] = l[1][1:-1]

					### Debug
#					self.val['process'] = self.val['process'] + ' ' + str(max)
#					self.val['process'] = self.val['process'] + ' ' + l[13] + ':' + l[14]

				### Garbage collect sort off
#				if self.val[pid] == 0:
#					del(self.cn1[pid]); del(self.cn2[pid]); del(self.val[pid])

				### If the name is a known interpreter, take the second argument from the cmdline
				if self.val['process'] in ('perl', 'python', 'sh', 'bash'):
					for line in dopen('/proc/%s/cmdline' % pid).readlines():
						l = string.split(line, '\0')
						self.val['process'] = os.path.basename(l[1])

		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
