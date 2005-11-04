class dstat_clock(dstat):
	def __init__(self):
		self.name = 'human clock'
		self.format = ('t', 14, 0)
		self.nick = ('date/time',)
		self.vars = self.nick
		self.init(self.vars, 1)

	def extract(self):
		pass
#		self.val['epoch'] = time.date('M d H:i', time.time())

	def show(self):
		return time.strftime('%d-%m %H:%M:%S', time.gmtime())

# vim:ts=4:sw=4
