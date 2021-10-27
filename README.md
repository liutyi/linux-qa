# qal.py

Python script that should give some first quick overview on Linux server status/health/configuration

FEATURES:

v 0.1: 

- OS Version, uptime, load average, kernel version
- Server Manufacturer, Type, Bios version and date, HW Serial

v 0.2: 
- openVZ info
- disk and ethernet
- some python 3 compatibility

TODO:

rest hardware info, net info, net services (SMTP,NTP,SYSLOG) info, security info, all kind of monitoring agents status

DEPENDENCIES:

yum install python-argparse

TESTED ON:

- Centos 7
- Ubuntu 20.04 Python 2.7
- Ubuntu 20.04 Python 3.8


USAGE:

```
curl https://raw.githubusercontent.com/oliut/linux-qa/master/qal.py 2>/dev/null |python
```

```    
root@oliut-vm:~# curl https://raw.githubusercontent.com/oliut/linux-qa/master/qal.py 2>/dev/null |python3
======================================================================
                     qal.py 0.1-016 (2021-10-04)
======================================================================
NAME:   oliut-vm
DATE:   2021-10-27 12:42 (EEST)
UPTIME: 10:33 (0.1, 0.03, 0.01)
OS:     Ubuntu 20.04 focal
KERNEL: Linux-5.11.0-38-generic-x86_64-with-glibc2.29
========[HARDWARE]====================================================
SERVER: innotek GmbH VirtualBox
BIOS:   innotek GmbH VirtualBox (12/01/2006)
SERIAL: 0
CPU:    1(1)xIntel(R) Core(TM) i5-10210U CPU @ 1.60GHz
MEM:    3.8 GB
SWAP:   1.7 GB
DISK:   sda 36.3 GB
NET:    enp0s3 1000/full(up) TX: 54.8 MB RX: 78.7 MB


```
    

