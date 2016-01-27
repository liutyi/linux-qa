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

TESTED ON:

Centos 7
Ubuntu 14.04


USAGE:

root@testmachine:~# linux-qa/qal.py
```    
=============================================================
LQApy Script 0.1-013 (2015-06-14)
=============================================================
NAME:   testmachine
DATE:   2016-01-27 12:51 (EET)
UPTIME: 4 days (0.0, 0.01, 0.05)
OS:     CentOS Linux 7.1.1503 Core
KERNEL: Linux-3.10.0-229.20.1.el7.x86_64-x86_64-with-centos-7.1.1503-Core
==========[HARDWARE]=========================================
SERVER: Dell Inc. OptiPlex 3010
BIOS:   Dell Inc. A05 (09/18/2012)
SERIAL: 8QBYG5J
CPU:    4(1)xIntel(R) Core(TM) i5-3470 CPU @ 3.20GHz
MEM:    15.4 GB
SWAP:   16.0 GB
DISK:   sda 931.5 GB
DISK:   sdb 167.7 GB

```
    

