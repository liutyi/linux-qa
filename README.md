# qal.py

Python script that should give some first quick overview on Linux server status/health/configuration

FEATURES:

v 0.1: 

- OS Version, uptime, load average, kernel version
- Server Manufacturer, Type, Bios version and date, HW Serial

v 0.2: 
- openVZ info
- disk and ethernet
- add cpu core/threads info
- python 3 compatibility

TODO:

rest hardware info, net info, net services (SMTP,NTP,SYSLOG) info, security info, all kind of monitoring agents status

DEPENDENCIES:

yum install python-argparse

TESTED ON:

- Centos 6 Python 3.4
- Centos 7 Python 2.7
- Centos 7 Python 3.6
- AlmaLinux 8.6 Python 3.6
- Ubuntu 16.04 Python 2.7
- Ubuntu 16.04 Python 3.5
- Ubuntu 18.04 Python 2.7
- Ubuntu 18.04 Python 3.6
- Ubuntu 20.04 Python 2.7
- Ubuntu 20.04 Python 3.8
- Ubuntu 22.04 Python 3.10


USAGE:

```
curl https://raw.githubusercontent.com/liutyi/linux-qa/master/qal.py 2>/dev/null |python
```
or 
```
curl https://raw.githubusercontent.com/liutyi/linux-qa/master/qal.py 2>/dev/null |python3
```

```    
======================================================================
                     qal.py 0.2-020 (2022-06-15)
======================================================================
NAME:   server3
DATE:   2022-06-15 15:49 (EEST)
UPTIME: 13:47 (0.0, 0.0, 0.0)
OS:     Ubuntu 22.04 jammy
KERNEL: Linux-5.15.0-37-generic-x86_64-with-glibc2.35
========[HARDWARE]====================================================
SERVER: Intel(R) Client Systems NUC10i7FNK
BIOS:   Intel Corp. FNCML357.0056.2022.0223.1614 (02/23/2022)
SERIAL: G6FN20400EMY
CPU:    1xIntel(R) Core(TM) i7-10710U CPU @ 1.10GHz [ C:6 / T:12 ]
MEM:    62.5 GB
SWAP:   8.0 GB
DISK:   nvme0n1 1.8 TB
NET:    eno1 1000/full(up) TX: 2.9 GB RX: 557.9 MB

```
```
======================================================================
                     qal.py 0.2-020 (2022-06-15)
======================================================================
NAME:   server22
DATE:   2022-06-15 15:52 (IDT)
UPTIME: 1937 days (0.1, 0.61, 0.87)
OS:     CentOS 6.10 Final
KERNEL: Linux-2.6.32-431.29.2.el6.x86_64-x86_64-with-centos-6.10-Final
========[HARDWARE]====================================================
SERVER: Supermicro X9SCL/X9SCM
BIOS:   American Megatrends Inc. 2.0b (09/17/2012)
SERIAL: 0123456789
CPU:    1xIntel(R) Xeon(R) CPU E3-1230 V2 @ 3.30GHz [ C:4 / T:4 ]
MEM:    31.3 GB
SWAP:   16.0 GB
DISKS:  3 disks 2.2 TB in total
NET:    eth0 1000/full(up) TX: 1.0 PB RX: 660.4 TB
NET:    eth1 1000/full(up) TX: 81.4 TB RX: 127.5 TB
```

