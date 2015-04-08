#!/usr/bin/env python
from argparse import ArgumentParser
import subprocess

def Options ():
   scriptName = 'LQApy Script'
   scriptVer  = '0.1'
   scriptUpd  = '001'
   scriptDate  = '2015-04-08'
   developedBy = 'Oleksandr Liutyi'
   version = scriptName+" "+scriptVer+"-"+scriptUpd+" ("+scriptDate+")"
   description = 'Linux Server QA Script'
   parser = ArgumentParser(description=description)
   parser.add_argument("-V", "--version", action='version', version=version)
   parser.add_argument("-q", "--quick", action="store_true", help="do not ubdate locate db")
   parser.add_argument("-w", "--write",    action="store_true", help="write errors to syslog")
   parser.add_argument('-s', '--scheme',   action='store', dest='color', choices=['black', 'white', 'text'], help="Color scheme selection\r\nblack, white, text ")
   parser.add_argument("section",nargs='*', help="optional section(s) name(s) for example: header, hw, san, net, netsrv, security, ntp, agents")
   args = parser.parse_args()
   print(args.color)
   print(args.section)

def bashCmd (cmd):
    x = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = x.stdout.read().strip()
    return out

def main():
	Options ()

if __name__ == '__main__':
    main()

