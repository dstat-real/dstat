### Author: Dag Wieers <dag@wieers.com>

global socket
import socket

global struct
import struct

### FIXME: Implement millisecond granularity as well
### FIXME: Interrupts socket if data is overdue (more than 250ms ?)

class dstat_plugin(dstat):
    """
    Time from an NTP server.

    BEWARE: this dstat plugin typically takes a lot longer to run than
    system plugins and for that reason it is important to use an NTP server
    located nearby as well as make sure that it does not impact your other
    counters too much.
    """

    def __init__(self):
        self.name = 'ntp'
        self.nick = ('date/time',)
        self.vars = ('time',)
        self.timefmt = os.getenv('DSTAT_TIMEFMT') or '%d-%m %H:%M:%S'
        self.ntpserver = os.getenv('DSTAT_NTPSERVER') or '0.fedora.pool.ntp.org'
        self.type = 's'
        self.width = len(time.strftime(self.timefmt, time.localtime()))
        self.scale = 0
        self.epoch = 2208988800L
#        socket.setdefaulttimeout(0.25)
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.settimeout(0.25)

    def gettime(self):
        self.socket.sendto( '\x1b' + 47 * '\0', ( self.ntpserver, 123 ))
        data, address = self.socket.recvfrom(1024)
        return struct.unpack( '!12I', data )[10] - self.epoch

    def check(self):
        try:
            self.gettime()
        except socket.gaierror:
            raise Exception, 'Failed to connect to NTP server %s.' % self.ntpserver
        except socket.error:
            raise Exception, 'Error connecting to NTP server %s.' % self.ntpserver

    def extract(self):
        try:
            self.val['time'] = time.strftime(self.timefmt, time.localtime(self.gettime()))
        except:
            self.val['time'] = theme['error'] + '-'.rjust(self.width-1) + ' '

    def showcsv(self):
        return time.strftime(self.timefmt, time.localtime(self.gettime()))

# vim:ts=4:sw=4:et
