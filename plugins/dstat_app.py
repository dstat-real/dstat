### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

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

				l = string.split(dopen('/proc/%s/stat' % pid).read())
				if len(l) < 15: continue
				self.cn2[pid] = int(l[13]) + int(l[14])
				usage = (self.cn2[pid] - self.cn1[pid]) * 1.0 / tick

				### Get the process that spends the most jiffies
				if usage > max:
					max = usage
					self.val['process'] = l[1][1:-1]

					### If the name is a known interpreter, take the second argument from the cmdline
					if self.val['process'] in ('bash', 'csh', 'ksh', 'perl', 'python', 'sh'):
						for line in dopen('/proc/%s/cmdline' % pid).readlines():
							self.val['process'] = os.path.basename(string.split(line, '\0')[1])

					### Debug (show PID)
#					self.val['process'] = '%s %s' % (pid, self.val['process'])

					### Debug (show CPU usage)
#					self.val['process'] = '%s %d' % (self.val['process'], usage)

					### Debug (show CPU kernel/user values)
#					self.val['process'] = '%s %d:%d' % (self.val['process'], int(l[13]) / tick, int(l[14]) / tick)

				### Garbage collect sort off
#				if value == 0:
#					del(self.cn1[pid]); del(self.cn2[pid])

		if step == op.delay:
			self.cn1.update(self.cn2)

# vim:ts=4:sw=4
