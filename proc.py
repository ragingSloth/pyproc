#/proc/[PID]/statm
#    1st entry is virtual
#    2nd entry is physical
import os
import time
from resource import getpagesize
from re import search
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
        times = stat.read().split(' ')
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

graph_cpu(nsamples=10, PID=2061)
