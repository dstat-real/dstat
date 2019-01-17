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

    self.name    = 'mongodb queues'
    self.nick    = ('ar', 'aw', 'qt', 'qw')
    self.vars    = ('ar', 'aw', 'qt', 'qw')
    self.type    = 'd'
    self.width   = 5
    self.scale   = 2
    self.lastVal = {}

  def extract(self):
    status = self.db.command("serverStatus")
    glock = status['globalLock']
    alock = glock['activeClients']
    qlock = glock['currentQueue']

    self.val['ar'] = int(alock['readers'])
    self.val['aw'] = int(alock['writers'])
    self.val['qr'] = int(qlock['readers'])
    self.val['qw'] = int(qlock['writers'])
