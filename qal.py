#!/usr/bin/env python
from argparse import ArgumentParser

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

def title (msg):
    longtitle="=========["+msg+"]================================================="
    shorttitle=longtitle[0:61]
    print TITLE + shorttitle
	
def main():
   args =  Options ()
   ColorScheme (args.color)
   sections=args.section
   if ( len(sections) == 0 ):
     sections = ['header', 'hw', 'net' , 'netsrv', 'security', 'agents']
   print TITLE + "==============================================================" + DEFAULT
   print('{:^62}'.format(version))
   print TITLE + "==============================================================" + DEFAULT
   for i in range(len(sections)):
        if ( sections[i] == 'header' ):
           print TITLE + "==============================================================" + DEFAULT            
        if ( sections[i] == 'hw' ):
           title('HW')

if __name__ == '__main__':
    main()

