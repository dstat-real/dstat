global iwlibs
import iwlibs

class dstat_wifi(dstat):
	def __init__(self):
		self.name = 'wifi'
		self.format = ('d', 3, 33)
		self.vars = iwlibs.getNICnames()
		self.name = self.vars
		self.nick = ('lnk', 's/n')
		self.init(self.vars, 2)

	def check(self): 
		try:
			global iwlibs
			import iwlibs
		except:
			raise Exception, 'Module needs the python-wifi module.'
		return True

	def extract(self):
		for name in self.vars:
			wifi = iwlibs.Wireless(name)
			stat, qual, discard, missed_beacon = wifi.getStatistics()
#			print qual.quality, qual.signallevel, qual.noiselevel
			if qual.quality == 0 and qual.signallevel == qual.noiselevel == -101:
				self.val[name] = ( -1, -1 )
			else:
				self.val[name][0] = qual.quality * 100 / 160
				self.val[name][1] = qual.signallevel * 100 / qual.noiselevel

# vim:ts=4:sw=4
