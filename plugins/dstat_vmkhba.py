### VMware ESX kernel vmhba stats
### Displays kernel vmhba statistics on VMware ESX servers
###
### Authority: bert+dstat@debruijn.be

# NOTE TO USERS: command-line plugin configuration is not yet possible, so I've
# "borrowed" the -D argument. 
# EXAMPLES:
# # dstat -M vmkhba -D vmhba1,vmhba2,total
# # dstat -M vmkhba -D vmhba0
# You can even combine the Linux and VMkernel diskstats (but the "total" argument
# will be used by both).
# # dstat -M vmkhba -d -D sda,vmhba1

class dstat_vmkhba(dstat):
	def __init__(self):
		self.name = 'vmkhba'
		self.discover = self.discover()
		self.format = ('f', 5, 1024)
		self.nick = ('read', 'writ')
		self.vars = self.vars()
		self.name = self.vars
		self.init(self.vars + ['total'], 2)

	def discover(self, *list):
	# discover will list all vmhba's found.
	# we might want to filter out the unused vmhba's (read stats, compare with ['0', ] * 13)
		ret = []
		try:
			list = os.listdir('/proc/vmware/scsi/')
		except:
			raise Exception, 'Needs VMware ESX'
		for name in list:
			for line in dopen('/proc/vmware/scsi/%s/stats' % name).readlines():
				l = line.split()
				if len(l) < 13: continue
				if l[0] == 'cmds': continue
				if l == ['0', ] * 13: continue
				ret.append(name)
		return ret

	def vars(self):
	# vars will take the argument list - when implemented - , use total, or will use discover + total
		ret = []
		if op.disklist:
			list = op.disklist
		#elif not op.full:
		#	list = ('total', )
		else:
			list = self.discover
			list.sort()
		for name in list:
			if name in self.discover + ['total']:
				ret.append(name)
		return ret

	def check(self): 
		info(1, 'The vmkhba module is an EXPERIMENTAL module.')
		ret = True
		try:
			os.listdir('/proc/vmware')
		except:
			raise Exception, 'Needs VMware ESX'
		return ret

	def extract(self):
		self.cn2['total'] = (0, 0)
		for name in self.vars:
			self.cn2[name] = (0, 0)
		for name in os.listdir('/proc/vmware/scsi/'):
			for line in dopen('/proc/vmware/scsi/%s/stats' % name).readlines():
				l = line.split()
				if len(l) < 13: continue
				if l[0] == 'cmds': continue
				if l[2] == '0' and l[4] == '0': continue
				if l == ['0', ] * 13: continue
				self.cn2['total'] = ( self.cn2['total'][0] + long(l[2]), self.cn2['total'][1] + long(l[4]) )
				if name in self.vars and name != 'total':
					self.cn2[name] = ( long(l[2]), long(l[4]) )
			for name in self.cn2.keys():
				self.val[name] = (
					(self.cn2[name][0] - self.cn1[name][0]) * 1024.0 / tick,
					(self.cn2[name][1] - self.cn1[name][1]) * 1024.0 / tick
				)
		if step == op.delay:
			self.cn1.update(self.cn2)
