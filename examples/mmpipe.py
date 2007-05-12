#!/usr/bin/python
import select, sys, os

def readpipe(file, tmout = 0.001):
    "Read available data from pipe"
    ret = ''
    while not select.select([file.fileno()], [], [], tmout)[0]:
        pass
    while select.select([file.fileno()], [], [], tmout)[0]:
        ret = ret + file.read(1)
        return ret.split('\n')

def dpopen(cmd):
    "Open a pipe for reuse, if already opened, return pipes"
    global pipes
    if 'pipes' not in globals().keys(): pipes = {}
    if cmd not in pipes.keys():
        pipes[cmd] = os.popen3(cmd, 't', 0)
    return pipes[cmd]

### Unbuffered sys.stdout
sys.stdout = os.fdopen(1, 'w', 0)

### Main entrance
if __name__ == '__main__':
    try:
        stdin, stdout, stderr = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
        stdin.write('reset\n')
        readpipe(stdout)

        while True:
            stdin.write('io_s\n')
            for line in readpipe(stdout):
                print line

    except KeyboardInterrupt, e:
        print

# vim:ts=4:sw=4
