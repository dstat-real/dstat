### Dstat NTP plugin
### Displays time from an NTP server
###
### Authority: dag@wieers.com

global socket
import socket
global struct
import struct

### FIXME: Implement millisecond granularity as well

class dstat_ntp(dstat):
    def __init__(self):
        self.name = 'ntp'
        self.timefmt = os.getenv('DSTAT_TIMEFMT') or '%d-%m %H:%M:%S'
        self.ntpserver = os.getenv('DSTAT_NTPSERVER') or '0.fedora.pool.ntp.org'
        self.format = ('s', len(time.strftime(self.timefmt, time.localtime())), 0)
        self.nick = ('date/time',)
        self.vars = ('time',)
        self.epoch = 2208988800L
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.init(self.vars, 1)

    def gettime(self):
        self.socket.sendto( '\x1b' + 47 * '\0', ( self.ntpserver, 123 ))
        data, address = self.socket.recvfrom( 1024 )

        if data:
            return (struct.unpack( '!12I', data )[10] - self.epoch)
        else:
            return 0

    def check(self):
        try:
            self.gettime()
        except gaierror:
            raise Exception, 'Failed to connect to NTP server.'
        except error:
            raise Exception, 'Error connecting to NTP server.'
        return True

    def extract(self):
        starttime = self.gettime()
        self.val['time'] = time.strftime(self.timefmt, time.localtime(starttime))

    def show(self):
        if step == op.delay:
            color = 'silver'
        else:
            color = 'gray'
        return ansi[color] + self.val['time']

# vim:ts=4:sw=4:et
