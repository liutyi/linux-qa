#!/usr/bin/env python
#
# License: GPLv3
# http://www.gnu.org/licenses/gpl.html
#
from argparse import ArgumentParser
from socket import gethostname;
from collections import OrderedDict
#import psutil
import platform
import time
import os

# Parse command line options
def Options ():
   scriptName = 'qal.py'
   scriptVer  = '0.1'
   scriptBuild = '016'
   scriptDate  = '2021-10-04'
   developedBy = 'Oleksandr Liutyi'
   scriptDesc  = 'Linux Server Brief Status Script'
   global version; version = scriptName+" "+scriptVer+"-"+scriptBuild+" ("+scriptDate+")"
   parser = ArgumentParser(description=scriptDesc)
   parser.add_argument("-V", "--version",\
                         action='version', version=version)
   parser.add_argument("-q", "--quick",\
                         action="store_true",\
                         help="do not ubdate locate db")
   parser.add_argument("-w", "--write",\
                         action="store_true",\
                         help="write errors to syslog")
   parser.add_argument('-s', '--scheme',\
                         action='store', dest='color', choices=['calm', 'inverse', 'default', 'text'],\
                         default='default',\
                         help="Color scheme selection\r\nblack, white, text ")
   parser.add_argument("section",nargs='*',\
                         help="optional section(s) name(s) for example: header, hw, net, netsrv, security, agents")
   args = parser.parse_args()
   return args

# Define color scheme
def ColorScheme (scheme):
   # Background color definitions
   BBLACK='\033[40m'; BRED='\033[41m'; BGREEN='\033[42m'
   BBROWN='\033[43m'; BBLUE='\033[44m'; BMAGENTA='\033[45m'
   BCYAN='\033[46m'; BGRAY='\033[47m'; BDEF='\033[49m'
   # Foreground color definitions
   FBLACK='\033[0;30m'; FRED='\033[0;31m'; FGREEN='\033[0;32m'
   FBROWN='\033[0;33m'; FBLUE='\033[0;34m'; FMAGENTA='\033[0;35m'
   FCYAN='\033[0;36m'; FGRAY='\033[0;37m'; FDEF='\033[0;39m'
   FDGRAY='\033[1;30m'; FLRED='\033[1;31m'; FLGREEN='\033[1;32m'
   FYELLOW='\033[1;33m'; FLBLUE='\033[1;34m'; FLMAGENTA='\033[1;35m'
   FLCYAN='\033[1;36m'; FWHITE='\033[1;37m'
   # Special color definitions
   SBOLD='\033[1m'; SUNDERLINE='\033[4m'; SBLINK='\033[5m'; SINVERSE='\033[7m'; SDEF='\033[m'
   # Assign color
   global TITLE; global NEUTRAL; global CRITICAL; global WARNING; global GOOD; global TIPS; global DEFAULT
   if ( scheme == 'calm' ):
        TITLE=FDEF; NEUTRAL=FWHITE; CRITICAL=FRED; WARNING=FBROWN; GOOD=FGREEN; TIPS=FLCYAN; DEFAULT=FDEF
   if ( scheme == "inverse" ):
        TITLE=FBLACK; NEUTRAL=FDEF; CRITICAL=FRED; WARNING=FBROWN; GOOD=FGREEN; TIPS=FLCYAN; DEFAULT=FDEF
   if ( scheme == "default" ):
        TITLE=FWHITE; NEUTRAL=FDEF; CRITICAL=FRED; WARNING=FBROWN; GOOD=FGREEN; TIPS=FLCYAN; DEFAULT=FDEF
   if ( scheme == "text" ):
        TITLE=""; NEUTRAL=""; CRITICAL=""; WARNING=""; GOOD=""; TIPS=""; DEFAULT=""

# Print in neutral colors
def list (msg):
    print NEUTRAL + msg + DEFAULT

# Print with POSITIVE colors
def positive(msg):
    print GOOD + msg + DEFAULT

# Print in WARNING colors
def warning(msg):
    print WARNING + msg + DEFAULT

# Print in ERROR colors
def error(msg):
    print CRITICAL + msg + DEFAULT

# Print section title
def title(msg):
    longtitle="========["+msg+"]============================================================"
    shorttitle=longtitle[0:70]
    print TITLE + shorttitle

# Add row with row TITLE: + information
def row(msg,info):
    shortrow=msg[0:6]+':\t'
    print TITLE + shortrow + DEFAULT + str(info)

# Get human readable uptime
def countuptime():
    try:
      f = open( "/proc/uptime" )
      contents = f.read().split()
      f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"
    total_seconds = float(contents[0])
    MINUTE = 60; HOUR = MINUTE * 60; DAY = HOUR * 24
    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )
    string = ""
    if days > 0:
       string += str(days) + " " + (days == 1 and "day" or "days" )
    else:
         string += str(hours).zfill(2) + ":"
         string += str(minutes).zfill(2)

    return string;

# Memory, Swap, Disk sizes in human readable formats
def humanizeKB (number):
    for unit in ['KB','MB','GB','TB','PB','EB','ZB']:
        if abs(number) < 1024.0:
            humanrnum = "%3.1f %s" % (number, unit)
            break
        number /= 1024.0
        humanrnum = "%.1f %s" % (number, 'Yi')
    return humanrnum;

def humanizeB (number):
    for unit in ['B','KB','MB','GB','TB','PB','EB','ZB']:
        if abs(number) < 1024.0:
            humanrnum = "%3.1f %s" % (number, unit)
            break
        number /= 1024.0
        humanrnum = "%.1f %s" % (number, 'Yi')
    return humanrnum;

# Get human readable memory info
def meminfo ():
    meminfo=OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    f.close()
    memt = int (meminfo [ 'MemTotal' ].split(' ')[0].strip())
    swpt = int (meminfo [ 'SwapTotal' ].split(' ')[0].strip())
#    swpt = psutil.swap_memory().total
#    memt = psutil.virtual_memory().total
    memth = humanizeKB (memt)
    swpth = humanizeKB (swpt)

    row('MEM',memth)
    row('SWAP',swpth)


# Get CPU Information
def cpuinfo ():
        cpucore = []; oscpucore = []
        f = open( "/proc/cpuinfo" );
        for line in f:
            if line.strip():
               if line.rstrip('\n').startswith('model name'):
                  model_name = line.rstrip('\n').split(':')[1].strip()
               if line.rstrip('\n').startswith('physical id'):
                  coreid = line.rstrip('\n').split(':')[1].strip()
                  if coreid not in cpucore:
                     cpucore.append(coreid)
               if line.rstrip('\n').startswith('core id'):
                  coreid = line.rstrip('\n').split(':')[1].strip()
                  if coreid not in oscpucore:
                     oscpucore.append(coreid)
        f.close()
        model_name = str (len(oscpucore)) + "(" + str (len(cpucore)) + ")" + "x" + model_name
        row ("CPU", model_name)

# Get BIOS/HW information
def dmidecode():
    try:
        f = open( "/sys/class/dmi/id/sys_vendor" ); vendor=f.read(); f.close()
        f = open( "/sys/class/dmi/id/product_name" ); product=f.read(); f.close()
        f = open( "/sys/class/dmi/id/product_serial" ); serialn=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_vendor" ); biosven=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_version" ); biosver=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_date" ); biosdate=f.read(); f.close()
    except:
        return "File not exist"
    server = str( vendor.rstrip('\n')) + " " + str(product.rstrip('\n'))
    bios   = str(biosven.rstrip('\n')) + " " + str(biosver.rstrip('\n')) + " (" + str(biosdate.rstrip('\n')) + ")"
    serial = str(serialn.rstrip('\n'))
    row('SERVER',server)
    row('BIOS',bios)
    row('SERIAL',serial)

# Get disks sizes
def disk():
    devicesall = os.listdir('/sys/block/')
    disks = []; blocks = 0; dev_size =  0; block_size = 1024
    for dev in devicesall:
        if dev.startswith('md') or dev.startswith('sd') or dev.startswith('hd') or dev.startswith('xvd') or dev.startswith('vd') or dev.startswith('nvme'):
               disks.append(dev)
    disks = sorted(disks)
    if len (disks) < 3:
       for dev in disks:
               blocks = open('/sys/block/%s/size' % dev).readline().strip()
               block_size = open('/sys/block/%s/queue/logical_block_size' % dev).readline().strip()
               dev_size = int (blocks) * int (block_size)
               info = dev + " " + humanizeB (dev_size)
               row ('DISK', info)
    else:
       for dev in disks:
               blocks = open('/sys/block/%s/size' % dev).readline().strip()
               block_size = open('/sys/block/%s/queue/logical_block_size' % dev).readline().strip()
               newdev_size = int (blocks) * int (block_size)
               dev_size += newdev_size
       info = str(len (disks)) + " disks " + humanizeB(dev_size) + " in total"
       row ('DISKS', info)

def netcards():
    devicesall = os.listdir('/sys/class/net')
    netcards = [];
    for dev in devicesall:
        if dev.startswith('eno') or dev.startswith('enp') or dev.startswith('em') or dev.startswith('eth') or dev.startswith('wan') or dev.startswith('pxe'):
               netcards.append(dev)
    netcards = sorted(netcards)
    for dev in netcards:
            state = open('/sys/class/net/%s/operstate' % dev).readline().strip()
            speed = open('/sys/class/net/%s/speed' % dev).readline().strip()
            duplex = open('/sys/class/net/%s/duplex' % dev).readline().strip()
            rx_bytes = int (open('/sys/class/net/%s/statistics/rx_bytes' % dev).readline().strip())
            tx_bytes = int (open('/sys/class/net/%s/statistics/tx_bytes' % dev).readline().strip())
            if ( state == 'up' ):
                 info = dev + " " + speed + "/" + duplex + "(" + state  +  ")" + " TX: " + humanizeB (tx_bytes) + " RX: " + humanizeB (rx_bytes)
                 row ('NET', info)


# MAIN part of the script
def main():
   args =  Options ()
   ColorScheme (args.color)
   sections=args.section
   if ( len(sections) == 0 ):
     sections = ['header', 'hw', 'load', 'net' , 'netsrv', 'security', 'agents']
   print TITLE + "======================================================================" + DEFAULT
   print('{:^70}'.format(version))
   print TITLE + "======================================================================" + DEFAULT
   for i in range(len(sections)):
# HEADER
        if ( sections[i] == 'header' ):
           hostname=gethostname()
           row('NAME', hostname)
           now=time.strftime("%Y-%m-%d %H:%M (%Z)")
           row('DATE',now)
           loadavg=os.getloadavg()
           uptime=countuptime() + " " + str(os.getloadavg())
           row('UPTIME', uptime)
           platf=' '.join(platform.linux_distribution())
           row('OS', platf)
           kernelv=platform.platform()
           row('KERNEL',kernelv)
# HARDWARE
        if ( sections[i] == 'hw' ):
           title('HARDWARE')
           dmidecode()
           cpuinfo()
           meminfo()
           disk()
           netcards()

# HEALTH
#
# Memory usage
# Load Avg per core
# root FS disk usage
# root FS inodes usage check
# ipc resources availability
# pids availability
#
# PERFORMANCE
#
# count disk IOPS and transfer rate in MB/s
# count available MIPS in some way
#
# VIRTUAL
#
# Vmware addition and other type of guest services check
#
# NETWORK
#
# IP addresses
# Routings/Gateways
#
#
# NETWORK SERVICES
#
# SMTP status check
# NTP status check
# DNS setup check
#
# AGENTS
#
# Zabbix agent status and version
# Nagios agent status and version
# ..
#
# SECURITY
#
# ssh password access for root
# Qemu/Xen VENOM
# Bash ShellShock
# SSL HeartBleed
#
#
#







if __name__ == '__main__':
    main()
