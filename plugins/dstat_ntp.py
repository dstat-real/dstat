### Dstat NTP plugin
### Displays time from an NTP server
###
### Authority: dag@wieers.com

### Beware that this dstat plugin typically takes a lot longer to run than
### system plugins and for that reason it is important to use an NTP server
### located nearby as well as make sure that it does not impact your other
### counters too much.

global socket
import socket

global struct
import struct

### FIXME: Implement millisecond granularity as well
### FIXME: Interrupts socket if data is overdue (more than 250ms ?)

class dstat_ntp(dstat):
    def __init__(self):
        self.name = 'ntp'
        self.timefmt = os.getenv('DSTAT_TIMEFMT') or '%d-%m %H:%M:%S'
        self.ntpserver = os.getenv('DSTAT_NTPSERVER') or '0.fedora.pool.ntp.org'
        self.format = ('s', len(time.strftime(self.timefmt, time.localtime())), 0)
        self.nick = ('date/time',)
        self.vars = ('time',)
        self.epoch = 2208988800L
#        socket.setdefaulttimeout(0.25)
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.socket.settimeout(0.25)
        self.init(self.vars, 1)

    def gettime(self):
        try:
            self.socket.sendto( '\x1b' + 47 * '\0', ( self.ntpserver, 123 ))
            data, address = self.socket.recvfrom(1024)
        except socket.timeout:
            return 0
        return struct.unpack( '!12I', data )[10] - self.epoch

    def check(self):
        try:
            t = self.gettime()
        except socket.gaierror:
            raise Exception, 'Failed to connect to NTP server.'
        except socket.error:
            raise Exception, 'Error connecting to NTP server.'
        return True

    def extract(self):
        self.val['time'] = self.gettime()

    def show(self):
        if step == op.delay:
            color = 'silver'
        else:
            color = 'gray'
        if self.val['time']:
            return ansi[color] + time.strftime(self.timefmt, time.localtime(self.val['time']))
        else:
            return ansi['white'] + ansi['redbg'] + '-'.rjust(self.format[1]-1) + ' ' + ansi['default']

# vim:ts=4:sw=4:et
