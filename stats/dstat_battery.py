import dstat, string, os

class dstat_battery(dstat.dstat):
	def __init__(self):
		self.name = 'battery'
		self.format = ('f', 4, 34)
		self.vars = os.listdir('/proc/acpi/battery/')
		self.nick = [string.lower(name) for name in self.vars]
		self.init(self.vars, 1)

	def extract(self):
		for battery in self.vars:
			for line in dstat.dopen('/proc/acpi/battery/'+battery+'/info').readlines():
				l = string.split(line)
				if len(l) < 4: continue
				if l[0] == 'last':
					full = int(l[3])
			for line in dstat.dopen('/proc/acpi/battery/'+battery+'/state').readlines():
				l = string.split(line)
				if len(l) < 3: continue
				if l[0] == 'remaining':
					current = int(l[2])
			self.val[battery] = current * 100.0 / full

# vim:ts=4:sw=4
