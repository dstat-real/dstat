### Author: <gianfranco@mongodb.com>

global mongodb_user
mongodb_user = os.getenv('DSTAT_MONGODB_USER') or os.getenv('USER')

global mongodb_pwd
mongodb_pwd = os.getenv('DSTAT_MONGODB_PWD')

global mongodb_host
mongodb_host = os.getenv('DSTAT_MONGODB_HOST') or '127.0.0.1:27017'

class dstat_plugin(dstat):
  """
  Plugin for MongoDB.
  """
  def __init__(self):
    global pymongo
    import pymongo

    try:
      self.m = pymongo.MongoClient(mongodb_host)
      if mongodb_pwd:
        self.m.admin.authenticate(mongodb_user, mongodb_pwd)
      self.db = self.m.admin
    except Exception as e:
      raise Exception('Cannot interface with MongoDB server: %s' % e)

    self.name    = 'mongodb counts'
    self.nick    = ('qry', 'ins', 'upd', 'del', 'gtm', 'cmd')
    self.vars    = ('query', 'insert','update','delete','getmore','command')
    self.type    = 'd'
    self.width   = 5
    self.scale   = 2
    self.lastVal = {}

  def extract(self):
    status = self.db.command("serverStatus")
    opct = status['opcounters']

    for name in self.vars:
      if name in opct.iterkeys():
        if not name in self.lastVal:
          self.lastVal[name] = opct.get(name)

        self.val[name]     = (int(opct.get(name)) - self.lastVal[name]) / elapsed
        self.lastVal[name] = opct.get(name)
