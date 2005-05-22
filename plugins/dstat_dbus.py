class dstat_dbus(dstat):
	def __init__(self):
		self.name = 'dbus'
		self.format = ('d', 3, 100)
		self.nick = ('sys', 'ses')
		self.vars = ('system', 'session')
		self.init(self.vars, 1)

	def check(self): 
#		dstat.info(1, 'The dbus module is an EXPERIMENTAL module.')
		try:
			global dbus
			import dbus
			try:
				self.sysbus = dbus.Bus(dbus.Bus.TYPE_SYSTEM).get_service('org.freedesktop.DBus').get_object('/org/freedesktop/DBus', 'org.freedesktop.DBus')
				try:
					self.sesbus = dbus.Bus(dbus.Bus.TYPE_SESSION).get_service('org.freedesktop.DBus').get_object('/org/freedesktop/DBus', 'org.freedesktop.DBus')
				except:
					self.sesbus = None
			except:
				raise Exception, 'Module is unable to connect to dbus message bus.'
				return False
			return True
		except:
			raise Exception, 'Module needs the python-dbus module.'
			return False

	def extract(self):
		self.val['system'] = len(self.sysbus.ListServices()) - 1
		try:
			self.val['session'] = len(self.sesbus.ListServices()) - 1
		except:
			self.val['session'] = -1
#		print dir(b); print dir(s); print dir(d); print d.ListServices()
#		print dir(d)
#		print d.ListServices()

# vim:ts=4:sw=4
