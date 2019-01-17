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

    stats  = self.db.command("listDatabases")
    self.dbList = []
    for db in stats.get('databases'):
      self.dbList.append(db.get('name'))

    line = self.db.command("serverStatus")
    if 'storageEngine' in line:
      self.storageEngine = line.get('storageEngine').get('name')
    else:
      self.storageEngine = 'mmapv1'

    self.name    = 'mongodb stats'
    self.nick    = ('dsize', 'isize', 'ssize')
    self.vars    = ('dataSize', 'indexSize', 'storageSize')
    self.type    = 'b'
    self.width   = 5
    self.scale   = 2
    self.count   = 1

    if self.storageEngine == 'mmapv1':
      self.nick  = self.nick + ('fsize',)
      self.vars  = self.vars + ('fileSize',)


  def extract(self):
    self.set = {}

    # refresh the database list every 10 iterations
    if (self.count % 10) == 0:
      stats  = self.m.admin.command("listDatabases")
      self.dbList = []
      for db in stats.get('databases'):
        self.dbList.append(db.get('name'))
    self.count += 1

    for name in self.vars:
      self.set[name] = 0

    for db in self.dbList:
      self.db = self.m.get_database(db)
      stats = self.db.command("dbStats")
      for name in self.vars:
        self.set[name] += int(stats.get(name)) / (1024 * 1024)
    self.val = self.set
