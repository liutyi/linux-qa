# qal.py

Python script that should give some first quick overview on Linux server status/health/configuration

FEATURES:

v 0.1: 

OS Version, uptime, load average, kernel version
Server Manufacturer, Type, Bios version and date, HW Serial

TODO:

rest hardware info, net info, net services (SMTP,NTP,SYSLOG) info, security info, all kind of monitoring agents status

DEPENDENCIES:

yum install python-argparse

USAGE:

root@wordpress-0yvs:~# linux-qa/qal.py

=============================================================
              LQApy Script 0.1-010 (2015-04-13)
=============================================================
NAME:   wordpress-0yvs
DATE:   2015-04-24 22:16 (EEST)
UPTIME: 7 days (0.0, 0.01, 0.05)
OS:     debian 7.8
KERNEL: Linux-3.2.0-4-amd64-x86_64-with-debian-7.8
==========[HARDWARE]=========================================
SERVER: Google Google
BIOS:   Google Google (01/01/2011)
SERIAL: GoogleCloud-78402E1B290C15E9106CA7DE44591E72


