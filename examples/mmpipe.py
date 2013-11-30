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
        try:
            import subprocess
            p = subprocess.Popen(cmd, shell=False, bufsize=0, close_fds=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pipes[cmd] = (p.stdin, p.stdout, p.stderr)
        except ImportError:
            pipes[cmd] = os.popen3(cmd, 't', 0)
    return pipes[cmd]

### Unbuffered sys.stdout
sys.stdout = os.fdopen(1, 'w', 0)

### Main entrance
if __name__ == '__main__':
    try:
#        stdin, stdout, stderr = dpopen('/usr/lpp/mmfs/bin/mmpmon -p -s')
#        stdin.write('reset\n')
        stdin, stdout, stderr = dpopen('/bin/bash')
        stdin.write('uname -a\n')
        readpipe(stdout)

        while True:
#            stdin.write('io_s\n')
            stdin.write('cat /proc/stat\n')
            for line in readpipe(stdout):
                print line

    except KeyboardInterrupt, e:
        print

# vim:ts=4:sw=4
