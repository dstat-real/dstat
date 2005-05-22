#!/usr/bin/python

### Example 1: Direct accessing stats
### This is a quick example showing how you can access dstat data
### If you're interested in this functionality, contact me at dag@wieers.com
import sys
sys.path.insert(0, '/usr/share/dstat/')
import dstat

clear = dstat.ansi['reset']

c = dstat.dstat_cpu()
print c.title1() + '\n' + c.title2()
c.extract()
print c.show(), clear
print 'Percentage:', c.val['']
print 'Raw:', c.cn2['']
print

m = dstat.dstat_mem()
print m.title1() + '\n' + m.title2()
m.extract()
print m.show(), clear
print 'Raw:', m.val
print

l = dstat.dstat_load()
print l.title1() + '\n' + l.title2()
l.extract()
print l.show(), clear
print 'Raw:', l.val
print

d = dstat.dstat_disk()
print d.title1() + '\n' + d.title2()
d.extract()
print d.show(), clear
print 'Raw:', d.val['total']
print
