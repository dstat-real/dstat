global string
import string

class dstat_thermal(dstat):
	def __init__(self):
		self.name = 'thermal'
		self.format = ('d', 4, 20)
		self.vars = os.listdir('/proc/acpi/thermal_zone/')
#		self.nick = [string.lower(name) for name in self.vars]
		self.nick = []
		for name in self.vars:
			self.nick.append(string.lower(name))
		self.init(self.vars, 1)

	def extract(self):
		for zone in self.vars:
			for line in dopen('/proc/acpi/thermal_zone/'+zone+'/temperature').readlines():
				l = string.split(line)
				self.val[zone] = int(l[1])

# vim:ts=4:sw=4
