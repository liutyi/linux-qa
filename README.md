# qal.py

Python script that should give some first quick overview on Linux server status/health/configuration

FEATURES:

v 0.1: 

OS Version, uptime, load average, kernel version
Server Manufacturer, Type, Bios version and date, HW Serial
disk and ethernet

TODO:

rest hardware info, net info, net services (SMTP,NTP,SYSLOG) info, security info, all kind of monitoring agents status

DEPENDENCIES:

yum install python-argparse

TESTED ON:

Centos 7
Ubuntu 14.04
Ubuntu 20.04


USAGE:

root@oliut-vm:~# python qal.py
```    
=============================================================
                 qal.py 0.1-014 (2021-09-10)
=============================================================
NAME:   oliut-vm
DATE:   2021-09-10 17:48 (EEST)
UPTIME: 16:02 (0.03, 0.01, 0.0)
OS:     Ubuntu 20.04 focal
KERNEL: Linux-5.11.0-27-generic-x86_64-with-Ubuntu-20.04-focal
==========[HARDWARE]=========================================
SERVER: innotek GmbH VirtualBox
BIOS:   innotek GmbH VirtualBox (12/01/2006)
SERIAL: 0
CPU:    1(1)xIntel(R) Core(TM) i5-10210U CPU @ 1.60GHz
MEM:    3.8 GB
SWAP:   1.7 GB
DISK:   sda 36.3 GB
NET:    enp0s3 1000/full(up) TX: 64.8 MB RX: 140.5 MB

```
    

