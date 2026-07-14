#!/usr/bin/env bash
#
# qal.sh - Linux Server Brief Status Script
# Bash port of qal.py by Oleksandr Liutyi
#
# License: GPLv3
# http://www.gnu.org/licenses/gpl.html
#

SCRIPT_NAME='qal.sh'
SCRIPT_VER='0.2'
SCRIPT_BUILD='020'
SCRIPT_DATE='2022-06-15'
SCRIPT_DESC='Linux Server Brief Status Script'
VERSION="${SCRIPT_NAME} ${SCRIPT_VER}-${SCRIPT_BUILD} (${SCRIPT_DATE})"

# ---------------------------------------------------------------- options ---
usage() {
    cat <<EOF
usage: ${SCRIPT_NAME} [-h] [-V] [-q] [-w] [-s {calm,inverse,default,text}] [section ...]

${SCRIPT_DESC}

positional arguments:
  section               optional section(s) name(s) for example:
                        header, hw, net, netsrv, security, agents

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -q, --quick           do not update locate db
  -w, --write           write errors to syslog
  -s SCHEME, --scheme SCHEME
                        Color scheme selection: calm, inverse, default, text
EOF
}

OPT_QUICK=0
OPT_WRITE=0
OPT_SCHEME='default'
SECTIONS=()

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)    usage; exit 0 ;;
        -V|--version) echo "$VERSION"; exit 0 ;;
        -q|--quick)   OPT_QUICK=1 ;;
        -w|--write)   OPT_WRITE=1 ;;
        -s|--scheme)
            shift
            OPT_SCHEME="$1"
            ;;
        -s=*|--scheme=*)
            OPT_SCHEME="${1#*=}"
            ;;
        -*)
            echo "${SCRIPT_NAME}: error: unrecognized argument: $1" >&2
            exit 2 ;;
        *)
            SECTIONS+=("$1") ;;
    esac
    shift
done

case "$OPT_SCHEME" in
    calm|inverse|default|text) ;;
    *) echo "${SCRIPT_NAME}: error: argument -s/--scheme: invalid choice: '${OPT_SCHEME}' (choose from 'calm', 'inverse', 'default', 'text')" >&2
       exit 2 ;;
esac

# ----------------------------------------------------------- color scheme ---
color_scheme() {
    # Foreground color definitions
    local FBLACK='\033[0;30m' FRED='\033[0;31m'   FGREEN='\033[0;32m'
    local FBROWN='\033[0;33m' FDEF='\033[0;39m'   FLCYAN='\033[1;36m'
    local FWHITE='\033[1;37m'

    case "$1" in
        calm)
            TITLE=$FDEF;   NEUTRAL=$FWHITE; CRITICAL=$FRED; WARNING=$FBROWN
            GOOD=$FGREEN;  TIPS=$FLCYAN;    DEFAULT=$FDEF ;;
        inverse)
            TITLE=$FBLACK; NEUTRAL=$FDEF;   CRITICAL=$FRED; WARNING=$FBROWN
            GOOD=$FGREEN;  TIPS=$FLCYAN;    DEFAULT=$FDEF ;;
        default)
            TITLE=$FWHITE; NEUTRAL=$FDEF;   CRITICAL=$FRED; WARNING=$FBROWN
            GOOD=$FGREEN;  TIPS=$FLCYAN;    DEFAULT=$FDEF ;;
        text)
            TITLE=''; NEUTRAL=''; CRITICAL=''; WARNING=''
            GOOD='';  TIPS='';    DEFAULT='' ;;
    esac
}

# --------------------------------------------------------- print helpers ----
list()     { printf '%b%s%b\n' "$NEUTRAL"  "$1" "$DEFAULT"; }
positive() { printf '%b%s%b\n' "$GOOD"     "$1" "$DEFAULT"; }
warning()  { printf '%b%s%b\n' "$WARNING"  "$1" "$DEFAULT"; }
error()    { printf '%b%s%b\n' "$CRITICAL" "$1" "$DEFAULT"; }

title() {
    local longtitle="========[$1]============================================================"
    printf '%b%s%b\n' "$TITLE" "${longtitle:0:70}" "$DEFAULT"
}

# Row with row TITLE: + information
row() {
    printf '%b%s:\t%b%s\n' "$TITLE" "${1:0:6}" "$DEFAULT" "$2"
}

# ---------------------------------------------------------------- helpers ---
# humanize <number> <start_unit>   start_unit: B or KB
humanize() {
    awk -v n="$1" -v start="$2" 'BEGIN{
        split("B KB MB GB TB PB EB ZB", u, " ")
        i = (start == "KB") ? 2 : 1
        while ((n >= 1024 || n <= -1024) && i < 8) { n /= 1024; i++ }
        printf "%3.1f %s", n, u[i]
    }'
}

# Get human readable uptime
countuptime() {
    local total_seconds days hours minutes
    if [ ! -r /proc/uptime ]; then
        echo "Cannot open uptime file: /proc/uptime"
        return
    fi
    read -r total_seconds _ < /proc/uptime
    total_seconds=${total_seconds%.*}
    days=$((   total_seconds / 86400 ))
    hours=$((  (total_seconds % 86400) / 3600 ))
    minutes=$(( (total_seconds % 3600) / 60 ))
    if [ "$days" -gt 0 ]; then
        if [ "$days" -eq 1 ]; then echo "$days day"; else echo "$days days"; fi
    else
        printf '%02d:%02d\n' "$hours" "$minutes"
    fi
}

# ---------------------------------------------------------------- sections --
sec_header() {
    row 'NAME' "$(hostname)"
    row 'DATE' "$(date '+%Y-%m-%d %H:%M (%Z)')"

    local l1 l5 l15
    read -r l1 l5 l15 _ < /proc/loadavg
    row 'UPTIME' "$(countuptime) ($l1, $l5, $l15)"

    # OS  (equivalent of distro.name() + version + codename)
    local platf
    platf=$(
        if [ -r /etc/os-release ]; then
            . /etc/os-release
            codename="${VERSION_CODENAME:-}"
            if [ -z "$codename" ]; then
                codename=$(printf '%s\n' "${VERSION:-}" | sed -n 's/.*(\(.*\)).*/\1/p')
            fi
            echo "${NAME:-} ${VERSION_ID:-} ${codename}"
        else
            uname -s
        fi
    )
    row 'OS' "$platf"

    # KERNEL (equivalent of platform.platform())
    local glibc
    glibc=$(getconf GNU_LIBC_VERSION 2>/dev/null | awk '{print $2}')
    if [ -n "$glibc" ]; then
        row 'KERNEL' "Linux-$(uname -r)-$(uname -m)-with-glibc${glibc}"
    else
        row 'KERNEL' "Linux-$(uname -r)-$(uname -m)"
    fi
}

# Get BIOS/HW information
dmidecode_info() {
    local d=/sys/class/dmi/id
    [ -r "$d/sys_vendor" ] || return
    local vendor product biosven biosver biosdate
    vendor=$(<"$d/sys_vendor");     product=$(<"$d/product_name")
    biosven=$(<"$d/bios_vendor");   biosver=$(<"$d/bios_version")
    biosdate=$(<"$d/bios_date")
    row 'SERVER' "$vendor $product"
    row 'BIOS'   "$biosven $biosver ($biosdate)"
    if [ -r "$d/product_serial" ]; then
        row 'SERIAL' "$(<"$d/product_serial")"
    fi
}

checkvz() {
    [ -r /proc/vz/veinfo ] || return
    local ovz
    ovz=$(sed 's/^[[:space:]]*//' /proc/vz/veinfo)
    row 'OPENVZ' "$ovz"
}

# Get CPU Information
cpuinfo() {
    local model sockets cores threads
    model=$(awk -F': *' '/^model name/{print $2; exit}' /proc/cpuinfo)
    sockets=$(awk -F': *' '/^physical id/{print $2}' /proc/cpuinfo | sort -u | wc -l)
    cores=$(awk -F': *'   '/^core id/{print $2}'     /proc/cpuinfo | sort -u | wc -l)
    threads=$(grep -c '^processor' /proc/cpuinfo)
    [ "$sockets" -eq 0 ] && sockets=1
    row 'CPU' "${sockets}x${model} [ C:${cores} / T:${threads} ]"
}

# Get human readable memory info
memory_info() {
    local memkb swpkb
    memkb=$(awk '/^MemTotal:/{print $2}'  /proc/meminfo)
    swpkb=$(awk '/^SwapTotal:/{print $2}' /proc/meminfo)
    row 'MEM'  "$(humanize "$memkb" KB)"
    row 'SWAP' "$(humanize "$swpkb" KB)"
}

# Get disks sizes
disk_info() {
    local disks=() dev blocks block_size dev_size total=0
    for dev in /sys/block/*; do
        dev=${dev##*/}
        case "$dev" in
            md*|sd*|hd*|xvd*|vd*|nvme*|ploop*) disks+=("$dev") ;;
        esac
    done
    if [ ${#disks[@]} -lt 3 ]; then
        for dev in "${disks[@]}"; do
            blocks=$(<"/sys/block/$dev/size")
            block_size=$(cat "/sys/block/$dev/queue/logical_block_size" 2>/dev/null || echo 512)
            dev_size=$(( blocks * block_size ))
            row 'DISK' "$dev $(humanize "$dev_size" B)"
        done
    else
        for dev in "${disks[@]}"; do
            blocks=$(<"/sys/block/$dev/size")
            block_size=$(cat "/sys/block/$dev/queue/logical_block_size" 2>/dev/null || echo 512)
            total=$(( total + blocks * block_size ))
        done
        row 'DISKS' "${#disks[@]} disks $(humanize "$total" B) in total"
    fi
}
