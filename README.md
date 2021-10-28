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

- Centos 7
- Ubuntu 18.04
- Ubuntu 20.04 Python 2.7
- Ubuntu 20.04 Python 3.8


USAGE:

```
curl https://raw.githubusercontent.com/liutyi/linux-qa/master/qal.py 2>/dev/null |python
```

```    
======================================================================
                     qal.py 0.2-019 (2021-10-27)
======================================================================
NAME:   server1
DATE:   2021-10-28 11:44 (UTC)
UPTIME: 152 days (0.85, 0.66, 0.42)
OS:     Ubuntu 18.04 bionic
KERNEL: Linux-4.15.0-143-generic-x86_64-with-Ubuntu-18.04-bionic
========[HARDWARE]====================================================
SERVER: GIGABYTE GB-BXi7-5500
BIOS:   American Megatrends Inc. F2 (12/05/2014)
SERIAL: To be filled by O.E.M.
CPU:    2(1)xIntel(R) Core(TM) i7-5500U CPU @ 2.40GHz
MEM:    15.5 GB
SWAP:   4.0 GB
DISK:   sda 931.5 GB
NET:    enp3s0 1000/full(up) TX: 3.0 GB RX: 22.8 GB
```
    

