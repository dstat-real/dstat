#!/usr/bin/python

import sys
sys.path.insert(0, '/usr/share/dstat/')
import dstat, time

devices = ( 
    (  1,   0, 'ram0'),
    (  1,   1, 'ram1'),
    (  3,   1, 'hda1'),
    ( 33,   0, 'hde'),
    (  7,   0, 'loop0'),
    (  7,   1, 'loop1'),
    (  8,   0, '/dev/sda'),
    (  8,   1, '/dev/sda1'),
    (  8,  18, '/dev/sdb2'),
    (  8,  37, '/dev/sdc5'),
    (  9,   0, 'md0'),
    (  9,   1, 'md1'),
    (  9,   2, 'md2'),
    ( 74,  16, '/dev/ida/c2d1'),
    ( 77, 241, '/dev/ida/c5d15p1'),
    ( 98,   0, 'ubd/disc0/disc'),
    ( 98,  16, 'ubd/disc1/disc'),
    (104,   0, 'cciss/c0d0'),
    (104,   2, 'cciss/c0d0p2'),
    (253,   0, 'dm-0'),
    (253,   1, 'dm-1'),
)

for maj, min, device in devices:
    print device, '->', dstat.dev(maj, min)
