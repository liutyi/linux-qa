#!/usr/bin/env python
from argparse import ArgumentParser
from socket import gethostname;
from collections import OrderedDict
import platform
import time
import os

def Options ():
   scriptName = 'LQApy Script'
   scriptVer  = '0.1'
   scriptBuild = '010'
   scriptDate  = '2015-04-13'
   developedBy = 'Oleksandr Liutyi'
   scriptDesc  = 'Linux Server QA Script'
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

def list (msg):
    print NEUTRAL + msg + DEFAULT

def positive(msg):
    print GOOD + msg + DEFAULT

def warning(msg):
    print WARNING + msg + DEFAULT

def error(msg):
    print CRITICAL + msg + DEFAULT

def title(msg):
    longtitle="==========["+msg+"]==================================================="
    shorttitle=longtitle[0:61]
    print TITLE + shorttitle

def row(msg,info):
    shortrow=msg[0:6]+':\t'
    print TITLE + shortrow + DEFAULT + str(info)

def countuptime():
    try:
      f = open( "/proc/uptime" )
      contents = f.read().split()
      f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"
    total_seconds = float(contents[0])
    # Helper vars:
    MINUTE = 60; HOUR = MINUTE * 60; DAY = HOUR * 24
    # Get the days, hours, etc:
    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )
    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if days > 0:
       string += str(days) + " " + (days == 1 and "day" or "days" )
    else:
         string += str(hours).zfill(2) + ":"
         string += str(minutes).zfill(2)
 
    return string;

def meminfo ():
    meminfo=OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    num = int (meminfo [ 'MemTotal' ].split(' ')[0].strip())
    for unit in ['KB','MB','GB','TB','PB','EB','ZB']:
        if abs(num) < 1024.0:
            memhr = "%3.1f %s" % (num, unit)
	    break
        num /= 1024.0
        humanread = "%.1f %s" % (num, 'Yi')
    row('MEM',memhr)
    


def cpuinfo ():
        f = open( "/proc/cpuinfo" );
        for line in f:
            if line.strip():
               if line.rstrip('\n').startswith('model name'):
                  model_name = line.rstrip('\n').split(':')[1].strip()
        f.close()
	row ("CPU", model_name)

def dmidecode():
    try:
        f = open( "/sys/class/dmi/id/sys_vendor" ); vendor=f.read(); f.close()
        f = open( "/sys/class/dmi/id/product_name" ); product=f.read(); f.close()
        f = open( "/sys/class/dmi/id/product_serial" ); serialn=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_vendor" ); biosven=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_version" ); biosver=f.read(); f.close()
        f = open( "/sys/class/dmi/id/bios_date" ); biosdate=f.read(); f.close()
	f = open( "/proc/meminfo" ); meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in f.readlines()); mem_total_kib = meminfo['MemTotal']; f.close()
	f = open( "/proc/cpuinfo" );
    except:
        return "File not exist"
    server = str( vendor.rstrip('\n')) + " " + str(product.rstrip('\n'))
    bios   = str(biosven.rstrip('\n')) + " " + str(biosver.rstrip('\n')) + " (" + str(biosdate.rstrip('\n')) + ")"
    serial = str(serialn.rstrip('\n'))
    row('SERVER',server)
    row('BIOS',bios)
    row('SERIAL',serial)

def main():
   args =  Options ()
   ColorScheme (args.color)
   sections=args.section
   if ( len(sections) == 0 ):
     sections = ['header', 'hw', 'load', 'net' , 'netsrv', 'security', 'agents']
   print TITLE + "=============================================================" + DEFAULT
   print('{:^61}'.format(version))
   print TITLE + "=============================================================" + DEFAULT
   for i in range(len(sections)):
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
        if ( sections[i] == 'hw' ):
           title('HARDWARE')
           dmidecode()
           cpuinfo()
           meminfo()





if __name__ == '__main__':
    main()

