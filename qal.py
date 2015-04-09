#!/usr/bin/env python
from argparse import ArgumentParser
from socket import gethostname;
import platform
import time
import os

def Options ():
   scriptName = 'LQApy Script'
   scriptVer  = '0.1'
   scriptBuild = '002'
   scriptDate  = '2015-04-09'
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
			 action='store', dest='color', choices=['grey', 'white', 'text'],\
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
   if ( scheme == None ):
	TITLE=FDEF; NEUTRAL=FWHITE; CRITICAL=FRED; WARNING=FBROWN; GOOD=FGREEN; TIPS=FLCYAN; DEFAULT=FDEF
   if ( scheme == "white" ):
	TITLE=FBLACK; NEUTRAL=FDEF; CRITICAL=FRED; WARNING=FBROWN; GOOD=FGREEN; TIPS=FLCYAN; DEFAULT=FDEF
   if ( scheme == "grey" ):
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
    print shortrow + str(info)

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
      if  len(string) > 0 or hours > 0:
         string += ", " + str(hours) + ":"
      if len(string) > 0 or minutes > 0:
         string += str(minutes) 
 
    return string;


def main():
   args =  Options ()
   ColorScheme (args.color)
   sections=args.section
   if ( len(sections) == 0 ):
     sections = ['header', 'hw', 'net' , 'netsrv', 'security', 'agents']
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
           title('HW')

if __name__ == '__main__':
    main()

