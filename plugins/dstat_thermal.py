global string
import string

class dstat_thermal(dstat):
	def __init__(self):
		self.name = 'thermal'
		self.format = ('d', 4, 20)
		if os.path.exists('/proc/acpi/ibm/thermal'):
			self.namelist = ['cpu', 'pci', 'hdd', 'cpu', 'bat0', 'unk', 'bat1', 'unk']
			self.nick = []
			for line in dopen('/proc/acpi/ibm/thermal'):
				l = string.split(line)
				for i, name in enumerate(self.namelist):
					if int(l[i+1]) > 0:
						self.nick.append(name)
			self.vars = self.nick
		elif os.path.exists('/proc/acpi/thermal_zone/'):
			self.vars = os.listdir('/proc/acpi/thermal_zone/')
#			self.nick = [string.lower(name) for name in self.vars]
			self.nick = []
			for name in self.vars:
				self.nick.append(string.lower(name))
		else:
			raise Exception, 'Needs kernel ACPI or IBM-ACPI support'
		self.init(self.vars, 1)

	def extract(self):
		if os.path.exists('/proc/acpi/ibm/thermal'):
			for line in dopen('/proc/acpi/ibm/thermal'):
				l = string.split(line)
				for i, name in enumerate(self.namelist):
					if int(l[i+1]) > 0:
						self.val[name] = int(l[i+1])
		elif os.path.exists('/proc/acpi/thermal_zone/'):
			for zone in self.vars:
				for line in dopen('/proc/acpi/thermal_zone/'+zone+'/temperature').readlines():
					l = string.split(line)
					self.val[zone] = int(l[1])

# vim:ts=4:sw=4
