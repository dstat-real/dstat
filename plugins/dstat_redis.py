### Author: Jihyun Yu <yjh0502@gmail.com>

global redis_host 
redis_host = os.getenv('DSTAT_REDIS_HOST') or "127.0.0.1"

global redis_port
redis_port = os.getenv('DSTAT_REDIS_PORT') or "6379"

class dstat_plugin(dstat):
    def __init__(self):
        self.type = 'd'
        self.width = 7
        self.scale = 10000
        self.name = 'redis'
        self.nick = ('tps',)
        self.vars = ('tps',)
        self.cmdInfo = '*1\r\n$4\r\ninfo\r\n'

    def get_info(self):
        global socket
        import socket

        global redis_host
        global redis_port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(0.1)
            s.connect((redis_host, int(redis_port)))
            s.send(self.cmdInfo)
            dict = {};
            for line in s.recv(1024*1024).split('\r\n'):
                if line == "" or line[0] == '#' or line[0] == '*' or line[0] == '$':
                    continue
                pair = line.split(':', 2)
                dict[pair[0]] = pair[1]
            return dict
        except:
            return {}
        finally:
            try:
                s.close()
            except:
                pass

    def extract(self):
        key = "instantaneous_ops_per_sec"
        dic = self.get_info()
        if key in dic:
            self.val['tps'] = int(dic[key])

# vim:ts=4:sw=4:et
