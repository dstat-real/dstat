global string
import string

class dstat_cpufreq(dstat):
	def __init__(self):
		self.name = 'frequency'
		self.format = ('p', 4, 34)
		self.vars = os.listdir('/sys/devices/system/cpu/')
		self.nick = [string.lower(name) for name in self.vars]
		self.init(self.vars, 1)

	def check(self): 
		if self.vars:
			for cpu in self.vars:
				if not os.access('/sys/devices/system/cpu/'+cpu+'/cpufreq/cpuinfo_cur_freq', os.R_OK):
					raise Exception, 'Module cannot access acpi cpu frequency information'
					return False
			return True
		return false

	def extract(self):
		for cpu in self.vars:
			for line in dopen('/sys/devices/system/cpu/'+cpu+'/cpufreq/cpuinfo_max_freq').readlines():
				l = string.split(line)
				max = int(l[0])
			for line in dopen('/sys/devices/system/cpu/'+cpu+'/cpufreq/cpuinfo_cur_freq').readlines():
				l = string.split(line)
				cur = int(l[0])
			### Need to close because of bug in sysfs (?)
			dclose('/sys/devices/system/cpu/'+cpu+'/cpufreq/cpuinfo_cur_freq')
			self.val[cpu] = cur * 100.0 / max

# vim:ts=4:sw=4
