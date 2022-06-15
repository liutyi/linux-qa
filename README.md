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
curl https://raw.githubusercontent.com/oliut/linux-qa/master/qal.py 2>/dev/null |python
```
or 
```
curl https://raw.githubusercontent.com/oliut/linux-qa/master/qal.py 2>/dev/null |python3
```

```    
======================================================================
                     qal.py 0.2-020 (2022-06-15)
======================================================================
NAME:   server2
DATE:   2022-06-15 15:27 (EEST)
UPTIME: 4 days (0.0, 0.02, 0.03)
OS:     Ubuntu 16.04 xenial
KERNEL: Linux-4.4.0-210-generic-x86_64-with-Ubuntu-16.04-xenial
========[HARDWARE]====================================================
SERVER:
BIOS:   Intel Corp. WYLPT10H.86A.0046.2017.1219.2136 (12/19/2017)
SERIAL:
CPU:    2(1)xIntel(R) Core(TM) i5-4250U CPU @ 1.30GHz
MEM:    14.6 GB
SWAP:   15.0 GB
DISK:   sda 447.1 GB
NET:    eno1 1000/full(up) TX: 26.5 GB RX: 76.0 GB

```

```
======================================================================
                     qal.py 0.2-020 (2022-06-15)
======================================================================
NAME:   server1
DATE:   2022-06-15 12:29 (UTC)
UPTIME: 00:07 (0.35, 0.88, 0.64)
OS:     Ubuntu 18.04 bionic
KERNEL: Linux-4.15.0-184-generic-x86_64-with-Ubuntu-18.04-bionic
========[HARDWARE]====================================================
SERVER: GIGABYTE GB-BXi7-5500
BIOS:   American Megatrends Inc. F2 (12/05/2014)
SERIAL: To be filled by O.E.M.
CPU:    2(1)xIntel(R) Core(TM) i7-5500U CPU @ 2.40GHz
MEM:    15.5 GB
SWAP:   4.0 GB
DISK:   sda 931.5 GB
NET:    enp3s0 1000/full(up) TX: 541.5 KB RX: 27.8 MB
```

```
======================================================================
                     qal.py 0.2-020 (2022-06-15)
======================================================================
NAME:   server3
DATE:   2022-06-15 15:04 (EEST)
UPTIME: 13:01 (0.0, 0.0, 0.0)
OS:     Ubuntu 22.04 jammy
KERNEL: Linux-5.15.0-37-generic-x86_64-with-glibc2.35
========[HARDWARE]====================================================
SERVER: Intel(R) Client Systems NUC10i7FNK
BIOS:   Intel Corp. FNCML357.0056.2022.0223.1614 (02/23/2022)
SERIAL: G6FN20400EMY
CPU:    6(1)xIntel(R) Core(TM) i7-10710U CPU @ 1.10GHz
MEM:    62.5 GB
SWAP:   8.0 GB
DISK:   nvme0n1 1.8 TB
NET:    eno1 1000/full(up) TX: 2.9 GB RX: 556.7 MB

```

