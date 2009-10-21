#!/usr/bin/python

### Example 1: Direct accessing stats
### This is a quick example showing how you can access dstat data
### If you're interested in this functionality, contact me at dag@wieers.com
import sys
sys.path.insert(0, '/usr/share/dstat/')
import dstat

### Set default theme
dstat.theme = dstat.set_theme()

clear = dstat.ansi['reset']
dstat.tick = dstat.ticks()

c = dstat.dstat_cpu()
print c.title() + '\n' + c.subtitle()
c.extract()
print c.show(), clear
print 'Percentage:', c.val['total']
print 'Raw:', c.cn2['total']
print

m = dstat.dstat_mem()
print m.title() + '\n' + m.subtitle()
m.extract()
print m.show(), clear
print 'Raw:', m.val
print

l = dstat.dstat_load()
print l.title() + '\n' + l.subtitle()
l.extract()
print l.show(), clear
print 'Raw:', l.val
print

d = dstat.dstat_disk()
print d.title() + '\n' + d.subtitle()
d.extract()
print d.show(), clear
print 'Raw:', d.val['total']
print
