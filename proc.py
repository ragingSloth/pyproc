#/proc/[PID]/statm
#    1st entry is virtual
#    2nd entry is physical
import os
import time
import subprocess
from datetime import datetime, timedelta
from resource import getpagesize
from re import search, match
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

def graph_cpu(nsamples=1000,PID=None):
    data = []
    for i in xrange(nsamples):
        uptime = float(open('/proc/uptime').read().split(' ')[0])
        hertz = os.sysconf('SC_CLK_TCK')
        stat = open('/proc/'+str(PID)+'/stat','rt')
        times = stat.read().split(' ')
        stat.close
        total_time = sum(map(int,times[13:17]))
        time.sleep(.1)
        stat = open('/proc/'+str(PID)+'/stat','rt')
        times = stat.read().split()
        stat.close
        total_time2 = sum(map(int,times[13:17]))
        cpu = (total_time2-total_time)/10.0
        data.append(cpu)
    plt.plot(gaussian_filter1d(data,.68))
    plt.show()

def memory(PID = None):
    if PID == None:
        PID = os.getpid()
    page_size = getpagesize()
    mem = open('/proc/'+str(PID)+'/statm','r').read().split(' ')
    meminfo = open('/proc/meminfo').read()
    mem_total = int(search('^MemTotal:\s+(\d+)',meminfo).groups()[0])*1024.0
    return int(mem[1])*page_size/mem_total*100

def start_time(PID):
    system_start = subprocess.Popen(['who', '-b'], stdout=subprocess.PIPE).stdout.read()
    system_start = ' '.join(system_start.split()[2:])
    system_start = datetime.strptime(system_start, '%Y-%m-%d %H:%M')
    stat = open('/proc/'+str(PID)+'/stat','rt')
    start = stat.read().split()[21]
    hertz = os.sysconf('SC_CLK_TCK')
    return system_start + timedelta(0, float(start)/hertz)
#    start = filter(lambda x: match('[0-9]+', x) is not None and len(x) < 6, start)
#    return map(datetime.fromtimestamp, map(int, start))#(int(start))

def ps(args):
    return subprocess.Popen(['ps', '-'+args], stdout=subprocess.PIPE).stdout.read()

print start_time(26658)
