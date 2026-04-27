# Chapter 13: Managing Linux Networking – Complete Professional Guide

## Table of Contents

- [Chapter 13: Managing Linux Networking – Complete Professional Guide](#chapter-13-managing-linux-networking--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Network Troubleshooting Commands](#1-network-troubleshooting-commands)
    - [1.1 `ifconfig` (legacy)](#11-ifconfig-legacy)
    - [1.2 `ip` – Modern Replacement](#12-ip--modern-replacement)
    - [1.3 `ping`](#13-ping)
    - [1.4 `tracepath` / `traceroute`](#14-tracepath--traceroute)
    - [1.5 `arp`](#15-arp)
    - [1.6 `netstat` (legacy)](#16-netstat-legacy)
    - [1.7 `ss` – Socket Statistics (modern netstat)](#17-ss--socket-statistics-modern-netstat)
    - [1.8 `dig` – DNS lookup](#18-dig--dns-lookup)
    - [1.9 `nc` (netcat) – Swiss Army knife for networking](#19-nc-netcat--swiss-army-knife-for-networking)
    - [1.10 `curl` – Transfer data from/to server](#110-curl--transfer-data-fromto-server)
  - [2. Network Interface Naming in Linux](#2-network-interface-naming-in-linux)
    - [Old naming scheme (traditional)](#old-naming-scheme-traditional)
    - [New naming scheme (systemd/udev)](#new-naming-scheme-systemdudev)
  - [3. Managing Network Interfaces with NetworkManager](#3-managing-network-interfaces-with-networkmanager)
    - [3.1 `nmcli` – Command‑line client](#31-nmcli--commandline-client)
    - [3.2 `nmtui` – Text user interface](#32-nmtui--text-user-interface)
  - [4. Network Configuration Files](#4-network-configuration-files)
    - [4.1 Old (legacy) locations (ifcfg style)](#41-old-legacy-locations-ifcfg-style)
    - [4.2 New (NetworkManager) locations](#42-new-networkmanager-locations)
  - [5. Important Network Ports to Know](#5-important-network-ports-to-know)
  - [6. Common Network Problems and Troubleshooting](#6-common-network-problems-and-troubleshooting)
    - [Problem 1: No network connectivity](#problem-1-no-network-connectivity)
    - [Problem 2: DNS resolution fails (can ping IP but not domain)](#problem-2-dns-resolution-fails-can-ping-ip-but-not-domain)
    - [Problem 3: Slow network or high latency](#problem-3-slow-network-or-high-latency)
    - [Problem 4: Cannot reach a specific service (port filtered)](#problem-4-cannot-reach-a-specific-service-port-filtered)
    - [Problem 5: Duplicate IP address](#problem-5-duplicate-ip-address)
    - [Problem 6: Interface naming changed after kernel update](#problem-6-interface-naming-changed-after-kernel-update)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [Practice Lab – Verify Your Understanding](#practice-lab--verify-your-understanding)
  - [Real‑World Scenario – Setting Up and Troubleshooting a New Production Server’s Network](#realworld-scenario--setting-up-and-troubleshooting-a-new-production-servers-network)
    - [Background](#background)
    - [Step 1: Initial Inspection](#step-1-initial-inspection)
    - [Step 2: Configure a Static IP with `nmcli`](#step-2-configure-a-static-ip-with-nmcli)
    - [Step 3: Basic Connectivity Testing](#step-3-basic-connectivity-testing)
    - [Step 4: Socket and Service Inspection](#step-4-socket-and-service-inspection)
    - [Step 5: Temporary Network Changes (Alias and Route)](#step-5-temporary-network-changes-alias-and-route)
    - [Step 6: Firewall Configuration (firewalld)](#step-6-firewall-configuration-firewalld)
    - [Step 7: Deliberate DNS Problem and Recovery](#step-7-deliberate-dns-problem-and-recovery)
    - [Step 8: ARP and Neighbor Table](#step-8-arp-and-neighbor-table)
    - [Step 9: Monitoring and Error Checking](#step-9-monitoring-and-error-checking)
    - [Step 10: Document the Setup](#step-10-document-the-setup)
    - [Final Verification Checklist](#final-verification-checklist)

---

## 1. Network Troubleshooting Commands

### 1.1 `ifconfig` (legacy)

**Explanation:** Displays or configures network interfaces. Deprecated on many modern distributions; replaced by `ip`.

**Syntax:** `ifconfig [interface] [options]`

**Example output:**
```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fe3a:1234  prefixlen 64  scopeid 0x20
        ether 00:0c:29:3a:12:34  txqueuelen 1000  (Ethernet)
        RX packets 1234  bytes 123456 (120.5 KiB)
        TX packets 567  bytes 78901 (77.0 KiB)
```

**Anatomy of output:**
| Field | Meaning |
|-------|---------|
| `flags` | Interface capabilities (UP, BROADCAST, RUNNING, MULTICAST) |
| `mtu` | Maximum Transmission Unit (bytes) |
| `inet` | IPv4 address, netmask, broadcast |
| `inet6` | IPv6 address and prefix length |
| `ether` | MAC address |
| `RX/TX packets` | Received/transmitted packet counts and bytes |

**Common options:**
- `-a` – show all interfaces (including down)
- `up` / `down` – bring interface up/down
- `add` / `del` – add or remove IP address

**Example:**
```bash
ifconfig eth0 192.168.1.10 netmask 255.255.255.0 up
```

### 1.2 `ip` – Modern Replacement

**Explanation:** The `ip` command from the `iproute2` package replaces `ifconfig`, `route`, `arp`, and others.

**Common subcommands:**
- `ip a` (or `ip addr`) – show all IP addresses
- `ip link` – show network interfaces (layer 2)
- `ip route` – show routing table
- `ip neigh` – show ARP cache

**Example output of `ip a`:**
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
    inet6 fe80::20c:29ff:fe3a:1234/64 scope link
```

**Anatomy:**
- `<LOOPBACK,UP,LOWER_UP>` – interface flags (UP = administratively up, LOWER_UP = cable connected)
- `qdisc` – queuing discipline
- `state UNKNOWN/UP/DOWN` – operational state
- `group default` – interface group
- `scope global` / `scope link` – address scope

**Common options for `ip addr`:**
- `ip addr add 192.168.1.10/24 dev eth0` – add IP
- `ip addr del 192.168.1.10/24 dev eth0` – remove IP
- `ip link set eth0 up/down` – bring interface up/down

> **Note:** `ip a` shows **all** IP addresses (including secondary and virtual), unlike `ifconfig` which may hide some.

### 1.3 `ping`

**Explanation:** Sends ICMP Echo Request to test connectivity and measure round‑trip time.

**Syntax:** `ping [options] destination`

**Example output:**
```
PING google.com (142.250.185.46) 56(84) bytes of data.
64 bytes from 142.250.185.46: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 142.250.185.46: icmp_seq=2 ttl=117 time=11.9 ms
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 11.9/12.1/12.3/0.2 ms
```

**Anatomy:**
- `icmp_seq` – sequence number (detects packet loss)
- `ttl` – Time To Live (hops remaining)
- `time` – round‑trip time in milliseconds

**Common options:**
| Option | Meaning |
|--------|---------|
| `-c count` | Stop after `count` replies |
| `-i interval` | Seconds between packets (default 1) |
| `-s size` | Packet size in bytes |
| `-4` / `-6` | Force IPv4 or IPv6 |
| `-W timeout` | Timeout in seconds |
| `-f` | Flood ping (root only, for stress testing) |

**Example:**
```bash
ping -c 4 -i 0.5 8.8.8.8
```

### 1.4 `tracepath` / `traceroute`

**Explanation:** Shows the path (route) packets take to a destination, displaying each hop.

- `tracepath` – simpler, does not require root, uses UDP or ICMP.
- `traceroute` – more options, often requires root or `-I` for ICMP.

**Syntax:** `tracepath destination`

**Example output:**
```
 1:  192.168.1.1                                        0.512ms
 2:  10.0.0.1                                           1.234ms
 3:  172.16.0.1                                         5.678ms
 4:  core-router.example.com                           15.234ms
 5:  google.com                                        20.123ms reached
     Resume: pmtu 1500 hops 5 back 5
```

**Common options for `traceroute`:**
- `-n` – do not resolve hostnames (faster)
- `-I` – use ICMP Echo instead of UDP (often works without root)
- `-T` – use TCP SYN (good for firewalls blocking UDP)
- `-p port` – specify destination port
- `-m max_ttl` – maximum number of hops

**Example:**
```bash
traceroute -n -I google.com
```

### 1.5 `arp`

**Explanation:** Displays and manipulates the ARP (Address Resolution Protocol) cache – maps IP addresses to MAC addresses on the local network.

**Syntax:** `arp [options]`

**Example output:**
```
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.1.1              ether   00:11:22:33:44:55   C                     eth0
192.168.1.23             ether   aa:bb:cc:dd:ee:ff   C                     eth0
```

**Anatomy:**
- `Address` – IP address
- `HWtype` – hardware type (ether = Ethernet)
- `HWaddress` – MAC address
- `Flags` – `C` = complete (resolved), `M` = permanent, `P` = published
- `Iface` – interface

**Common options:**
- `-n` – show IP addresses numerically (no hostname resolution)
- `-a` – display all entries
- `-d ip` – delete ARP entry for `ip`
- `-s ip mac` – add a static ARP entry

> **Modern replacement:** `ip neigh` (neighbour table) provides similar functionality.

### 1.6 `netstat` (legacy)

**Explanation:** Displays network connections, routing tables, interface statistics, and more. Deprecated; replaced by `ss` and `ip route`.

**Common uses and their modern equivalents:**
| Old command | Modern replacement |
|-------------|-------------------|
| `netstat -tulpn` | `ss -tulpn` |
| `netstat -r` | `ip route` or `route -n` |
| `netstat -i` | `ip -s link` |
| `netstat -s` | `ip -s link` or `nstat` |

**Example output of `netstat -tulpn`:**
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State    PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN   1234/sshd
tcp6       0      0 :::80                   :::*                    LISTEN   5678/nginx
```

### 1.7 `ss` – Socket Statistics (modern netstat)

**Explanation:** Dumps socket statistics. Faster and more detailed than `netstat`.

**Syntax:** `ss [options]`

**Common options:**
| Option | Meaning |
|--------|---------|
| `-t` | TCP sockets |
| `-u` | UDP sockets |
| `-l` | Listening sockets |
| `-p` | Show process using the socket |
| `-n` | Numeric (no name resolution) |
| `-r` | Resolve service names |
| `-a` | All sockets (listening + established) |

**Example:**
```bash
ss -tulpn
```

**Example output:**
```
Netid  State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port   Process
tcp    LISTEN  0       128     0.0.0.0:22           0.0.0.0:*            users:(("sshd",pid=1234,fd=3))
tcp    LISTEN  0       128     *:80                  *:*                  users:(("nginx",pid=5678,fd=6))
```

**Anatomy:**
- `Netid` – protocol (tcp, udp, unix)
- `State` – LISTEN, ESTAB, TIME‑WAIT, etc.
- `Recv-Q` / `Send-Q` – bytes queued
- `Local Address:Port` – bind address
- `Peer Address:Port` – remote endpoint

### 1.8 `dig` – DNS lookup

**Explanation:** Domain Information Groper – queries DNS servers and returns detailed results.

**Syntax:** `dig [options] domain [type]`

**Common record types:**
- `A` – IPv4 address
- `AAAA` – IPv6 address
- `CNAME` – canonical name (alias)
- `MX` – mail exchanger
- `NS` – name servers
- `TXT` – text records

**Example:**
```bash
dig google.com A +short
```

**Example output (verbose):**
```
; <<>> DiG 9.16.1 <<>> google.com
;; ANSWER SECTION:
google.com.     300     IN      A       142.250.185.46
```

**Useful options:**
- `+short` – only print IP address
- `+trace` – follow delegation chain from root
- `-x IP` – reverse lookup (PTR record)
- `@server` – query a specific DNS server

### 1.9 `nc` (netcat) – Swiss Army knife for networking

**Explanation:** Reads and writes data across network connections. Used for port scanning, transferring files, chatting, and debugging.

**Syntax:** `nc [options] host port`

**Common uses:**

| Task | Command |
|------|---------|
| Port scan | `nc -zv host 1-1000` |
| Simple TCP client | `nc host port` |
| Listen on port | `nc -l -p 1234` |
| Transfer file | `nc -l -p 1234 > file` (receiver) <br> `nc host 1234 < file` (sender) |
| Banner grab | `echo "" | nc host port` |

**Options:**
- `-v` – verbose
- `-z` – zero I/O mode (scanning)
- `-l` – listen mode
- `-p port` – local port
- `-u` – UDP (default is TCP)

### 1.10 `curl` – Transfer data from/to server

**Explanation:** Supports HTTP, HTTPS, FTP, and many other protocols. Essential for testing APIs and web services.

**Syntax:** `curl [options] URL`

**Common options:**
| Option | Meaning |
|--------|---------|
| `-I` | Fetch headers only (HTTP HEAD) |
| `-X METHOD` | HTTP method (GET, POST, PUT, DELETE) |
| `-d data` | Send POST data |
| `-H "Header: value"` | Set request header |
| `-o file` | Write output to file |
| `-s` | Silent mode (no progress) |
| `-k` | Ignore SSL certificate errors |
| `-v` | Verbose (show request/response) |

**Examples:**
```bash
curl -I https://google.com
curl -X POST -d "name=alice" https://api.example.com/user
curl -H "Authorization: Bearer token" https://api.example.com/data
```

---

## 2. Network Interface Naming in Linux

### Old naming scheme (traditional)

Interfaces were named `eth0`, `eth1`, etc., based on detection order. This was **unpredictable** – adding a NIC could renumber interfaces.

### New naming scheme (systemd/udev)

Consistent, predictable names based on hardware topology. Format: `type + connection + number`

**Type prefixes:**
| Prefix | Meaning |
|--------|---------|
| `en` | Ethernet |
| `br` | Bridge |
| `team` | Teaming (bonding) |
| `virt` | Virtual (VM) |
| `ww` | WWAN (mobile broadband) |
| `wi` | Wi‑Fi |

**Connection suffixes:**
| Suffix | Meaning |
|--------|---------|
| `oN` | On‑board (N = index) e.g., `eno1` |
| `pNsN` | PCI bus (p = PCI, N bus number, sN slot) e.g., `enp2s0` |
| `sN` | Hot‑plug slot e.g., `ens3` |

**Examples:**
- `eno1` – on‑board Ethernet, port 1
- `enp2s0` – PCI Ethernet at bus 2, slot 0
- `ens3` – hot‑plug slot 3

**Disable predictable naming (if needed):**  
Add `net.ifnames=0` to kernel command line (in GRUB) or revert to `eth*` via udev rules.

---

## 3. Managing Network Interfaces with NetworkManager

**NetworkManager** is the default network management service on most modern distributions. It handles both wired and wireless connections, VPNs, and even bridges.

### 3.1 `nmcli` – Command‑line client

**Explanation:** Full control over NetworkManager from the terminal. Ideal for scripting and remote administration.

**Common operations:**

| Operation | `nmcli` command |
|-----------|-----------------|
| Show all connections | `nmcli connection show` |
| Show all devices | `nmcli device status` |
| Add a new Ethernet connection | `nmcli connection add type ethernet con-name mynet ifname eth0` |
| Modify IP address | `nmcli connection modify mynet ipv4.addresses 192.168.1.10/24` |
| Set manual IP (static) | `nmcli connection modify mynet ipv4.method manual` |
| Set DHCP | `nmcli connection modify mynet ipv4.method auto` |
| Bring connection up | `nmcli connection up mynet` |
| Bring connection down | `nmcli connection down mynet` |
| Delete a connection | `nmcli connection delete mynet` |
| Reload NetworkManager | `nmcli general reload` |

**Real‑world example – configure static IP on `eth0`:**
```bash
nmcli connection add type ethernet con-name production ifname eth0
nmcli connection modify production ipv4.method manual ipv4.addresses 192.168.1.100/24 ipv4.gateway 192.168.1.1 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection up production
```

**Check device status:**
```bash
nmcli device status
```

**Example output:**
```
DEVICE  TYPE      STATE      CONNECTION
eth0    ethernet  connected  production
lo      loopback  connected  lo
```

### 3.2 `nmtui` – Text user interface

**Explanation:** Curse‑based interactive tool for managing NetworkManager. No need to remember command syntax.

**Usage:**
```bash
sudo nmtui
```

Use arrow keys, Tab, and Enter. Options:
- **Edit a connection** – modify IP, DNS, gateway, etc.
- **Activate a connection** – bring up/down
- **Set system hostname**

---

## 4. Network Configuration Files

### 4.1 Old (legacy) locations (ifcfg style)

Used by `network-scripts` (deprecated in RHEL/CentOS 8+).

- `/etc/sysconfig/network-scripts/ifcfg-eth0` – interface configuration
- `/etc/sysconfig/network` – global network settings (hostname, gateway)
- `/etc/resolv.conf` – DNS resolver (often overwritten by DHCP/NetworkManager)

**Example `ifcfg-eth0`:**
```
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
ONBOOT=yes
```

### 4.2 New (NetworkManager) locations

- `/etc/NetworkManager/NetworkManager.conf` – main configuration
- `/etc/NetworkManager/conf.d/` – drop‑in snippets
- `/etc/NetworkManager/system-connections/` – stored connection profiles (plain text, keyfiles)

**Example connection file (`/etc/NetworkManager/system-connections/production.nmconnection`):**
```ini
[connection]
id=production
uuid=...
type=ethernet
interface-name=eth0

[ipv4]
method=manual
address1=192.168.1.100/24,192.168.1.1
dns=8.8.8.8;8.8.4.4;

[ipv6]
method=disabled
```

> **Note:** These files are protected (permissions 600) because they may contain secrets.

**Other important files:**
- `/etc/hosts` – static hostname to IP mapping
- `/etc/hostname` – system hostname (used at boot)
- `/etc/nsswitch.conf` – name service switch order (files, dns, etc.)

---

## 5. Important Network Ports to Know

| Port | Protocol | Service | Description |
|------|----------|---------|-------------|
| 20,21 | TCP | FTP | File Transfer Protocol (21 control, 20 data) |
| 22 | TCP | SSH | Secure Shell |
| 23 | TCP | Telnet | Unencrypted remote shell (avoid) |
| 25 | TCP | SMTP | Email sending |
| 53 | TCP/UDP | DNS | Domain Name System |
| 67,68 | UDP | DHCP | Dynamic Host Configuration Protocol |
| 80 | TCP | HTTP | Web (unencrypted) |
| 110 | TCP | POP3 | Email retrieval |
| 123 | UDP | NTP | Network Time Protocol |
| 143 | TCP | IMAP | Email retrieval |
| 161 | UDP | SNMP | Simple Network Management Protocol |
| 443 | TCP | HTTPS | Web (encrypted) |
| 465 | TCP | SMTPS | SMTP over SSL |
| 993 | TCP | IMAPS | IMAP over SSL |
| 995 | TCP | POP3S | POP3 over SSL |
| 3306 | TCP | MySQL | MySQL database |
| 5432 | TCP | PostgreSQL | PostgreSQL database |
| 8080 | TCP | HTTP-alt | Common proxy / Tomcat / Jenkins |
| 8443 | TCP | HTTPS-alt | Alternative HTTPS |

---

## 6. Common Network Problems and Troubleshooting

### Problem 1: No network connectivity

**Symptoms:** `ping 8.8.8.8` fails, `ip a` shows interface down or no IP.

**Steps:**
1. Check physical connection: `ip link` – look for `LOWER_UP` and `state UP`.
2. Bring interface up: `sudo ip link set eth0 up`
3. Check if interface has IP: `ip a`
4. If no IP and DHCP expected, restart NetworkManager or run `sudo dhclient eth0`.
5. Check if network service is running: `systemctl status NetworkManager`

### Problem 2: DNS resolution fails (can ping IP but not domain)

**Symptoms:** `ping google.com` fails, but `ping 8.8.8.8` works.

**Steps:**
1. Check `/etc/resolv.conf` – should contain nameserver entries.
2. If it's empty or wrong, reconfigure DNS via NetworkManager.
3. Test DNS: `dig google.com` or `nslookup google.com`.
4. Try public DNS: temporarily edit `/etc/resolv.conf` to `nameserver 8.8.8.8`.

### Problem 3: Slow network or high latency

**Tools:** `ping`, `tracepath`, `mtr` (my traceroute).

**Steps:**
1. `ping -c 10 destination` – look for high variance (mdev) or packet loss.
2. `mtr destination` – continuously shows per-hop loss and latency.
3. Check interface errors: `ip -s link show eth0` – look for dropped packets or errors.
4. Check system load: `top`, `vmstat` – CPU or memory could cause latency.

### Problem 4: Cannot reach a specific service (port filtered)

**Symptoms:** `curl http://server:8080` times out.

**Steps:**
1. Verify service is listening: `ss -tulpn | grep 8080`
2. Check local firewall: `sudo iptables -L -n` or `sudo firewall-cmd --list-all` (firewalld).
3. Check remote firewall (cloud security group, corporate firewall).
4. Test port with `nc -zv server 8080`.

### Problem 5: Duplicate IP address

**Symptoms:** Intermittent connectivity, `arp` entries flapping.

**Steps:**
1. Check ARP table: `ip neigh` or `arp -n`
2. Send a gratuitous ARP: `arping -I eth0 -A <IP>` (optional).
3. Use `arping -D -I eth0 <IP>` to detect if IP is already in use.
4. Reconfigure static IP to a different address.

### Problem 6: Interface naming changed after kernel update

**Symptoms:** Interface `enp2s0` suddenly becomes `enp3s0`.

**Solution:**
- Use udev rules to create persistent names based on MAC address.
- Or revert to `eth0` style by adding `net.ifnames=0` to GRUB_CMDLINE_LINUX in `/etc/default/grub`, then `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`.

---

## 7. Quick Reference Table

| Task | Command |
|------|---------|
| Show IP addresses | `ip a` |
| Show interface status | `ip link` |
| Show routing table | `ip route` |
| Show ARP cache | `ip neigh` |
| Test connectivity | `ping -c 4 host` |
| Trace route | `tracepath host` or `traceroute -n host` |
| Show listening ports | `ss -tulpn` |
| DNS lookup | `dig host` |
| Port scan | `nc -zv host port-range` |
| HTTP test | `curl -I http://url` |
| Manage NetworkManager | `nmcli` or `nmtui` |
| Restart network | `sudo systemctl restart NetworkManager` |
| Check network service status | `systemctl status NetworkManager` |
| View firewall rules (firewalld) | `sudo firewall-cmd --list-all` |
| View firewall rules (iptables) | `sudo iptables -L -n` |
| Disable/enable interface | `nmcli device disconnect eth0` / `connect eth0` |

---

## Practice Lab – Verify Your Understanding

1. Display all IP addresses on your system using `ip a`. Identify the MAC address of your primary Ethernet interface.
2. Ping your gateway and a remote address (e.g., 8.8.8.8). Note the differences in latency.
3. Use `ss -tulpn` to find which process is listening on port 22.
4. Perform a DNS lookup for `redhat.com` using `dig`. Repeat with `+short`.
5. Add a temporary IP alias to your interface (e.g., `192.168.1.200/24`). Delete it afterwards.
6. Check your routing table with `ip route`. Identify the default gateway.
7. Use `tracepath` to see the route to `google.com`. Spot at least three hops.
8. Create a new NetworkManager connection profile using `nmcli` with a static IP (test on a dummy interface or VM).
9. Examine `/etc/resolv.conf`. What nameservers are configured? Which service manages it?
10. Simulate a port scan on localhost using `nc -zv 127.0.0.1 1-1000`. Which ports are open?

---

## Real‑World Scenario – Setting Up and Troubleshooting a New Production Server’s Network

### Background

You are provisioning a new CentOS 9 server named **web‑prod‑01**. The data center has provided the following network information:

- **Interface:** single Ethernet port (connected)
- **Static IP:** `10.20.30.40/24`
- **Gateway:** `10.20.30.1`
- **DNS servers:** `10.20.30.2` (primary, internal), `8.8.8.8` (secondary)
- **Search domain:** `example.com`

The server will host a web application on port 8080 later. First you must configure the network, verify everything works, and document your findings.

All tasks are performed directly on the server console (or via SSH if you already have temporary access). Log in as the `admin` user with sudo privileges.

### Step 1: Initial Inspection

1. **List all network interfaces** along with their operational state and MAC addresses:
   ```bash
   ip link
   ```
   Look for an interface like `eno1`, `enp2s0`, or `ens3`. Note its name and confirm `state UP` and `LOWER_UP` (cable connected).

2. **View all IP addresses** assigned to interfaces:
   ```bash
   ip a
   ```
   If the interface already has an IP (for example via DHCP), note it for later.

3. **Check the current routing table**:
   ```bash
   ip route
   ```
   If DHCP is active, you may already have a default gateway.

4. **Check the DNS resolver configuration**:
   ```bash
   cat /etc/resolv.conf
   ```
   On CentOS 9 this file is usually managed by NetworkManager. It might be empty.

5. **Verify NetworkManager status**:
   ```bash
   systemctl status NetworkManager
   nmcli device status
   ```
   You should see your Ethernet device, likely in state `connected` (if DHCP) or `disconnected`.

### Step 2: Configure a Static IP with `nmcli`

1. **Create a new connection profile** named `production` (replace `eno1` with your actual interface):
   ```bash
   sudo nmcli connection add type ethernet con-name production ifname eno1
   ```

2. **Set the static IP, gateway, and DNS**:
   ```bash
   sudo nmcli connection modify production ipv4.method manual \
         ipv4.addresses 10.20.30.40/24 \
         ipv4.gateway 10.20.30.1 \
         ipv4.dns "10.20.30.2 8.8.8.8" \
         ipv4.dns-search example.com
   ```

3. **Bring the connection up**:
   ```bash
   sudo nmcli connection up production
   ```

4. **Verify the settings**:
   ```bash
   ip a show eno1
   ip route
   cat /etc/resolv.conf
   ```
   You should see the static IP, default route via `10.20.30.1`, and the DNS servers.

5. **Make it start automatically on boot**:
   ```bash
   sudo nmcli connection modify production connection.autoconnect yes
   ```

### Step 3: Basic Connectivity Testing

1. **Ping the gateway**:
   ```bash
   ping -c 4 10.20.30.1
   ```
   Expect 0% packet loss and low latency.

2. **Ping an external IP** (bypass DNS):
   ```bash
   ping -c 4 8.8.8.8
   ```

3. **Ping an external hostname** (tests DNS):
   ```bash
   ping -c 4 google.com
   ```
   If this fails but the previous step worked, you have a DNS problem – see the troubleshooting section later.

4. **Perform a manual DNS lookup**:
   ```bash
   dig google.com +short
   ```
   Also query the internal DNS server directly:
   ```bash
   dig @10.20.30.2 example.com
   ```

5. **Trace the route to an external host**:
   ```bash
   tracepath -n 8.8.8.8
   ```
   The first hop should be your gateway.

### Step 4: Socket and Service Inspection

1. **List all listening TCP and UDP ports with processes**:
   ```bash
   sudo ss -tulpn
   ```
   Expect `sshd` on port 22, maybe `chronyd` on udp/123.

2. **Check established connections**:
   ```bash
   ss -tan state established
   ```
   If you are connected via SSH, you will see an established connection on port 22.

3. **Test HTTP connectivity to the future app port** (should be refused, not blocked):
   ```bash
   curl -I http://10.20.30.40:8080
   ```
   “Connection refused” indicates the firewall is not blocking the port.

### Step 5: Temporary Network Changes (Alias and Route)

1. **Add a temporary IP alias**:
   ```bash
   sudo ip addr add 10.20.30.41/24 dev eno1
   ip a show eno1
   ```

2. **Ping the alias** from another machine or locally.

3. **Remove the alias**:
   ```bash
   sudo ip addr del 10.20.30.41/24 dev eno1
   ```

4. **Add a static route** to a test network (e.g., 192.168.100.0/24) via the gateway:
   ```bash
   sudo ip route add 192.168.100.0/24 via 10.20.30.1
   ip route
   ```
   Then delete it:
   ```bash
   sudo ip route del 192.168.100.0/24
   ```

### Step 6: Firewall Configuration (firewalld)

1. **View current firewall settings**:
   ```bash
   sudo firewall-cmd --list-all
   ```

2. **Allow port 8080/tcp** for the upcoming web application:
   ```bash
   sudo firewall-cmd --permanent --add-port=8080/tcp
   sudo firewall-cmd --reload
   sudo firewall-cmd --list-all
   ```
   Now `curl` to port 8080 will not time out (it will be refused until a service is running).

3. **Optionally examine raw iptables rules**:
   ```bash
   sudo iptables -L -n
   ```

### Step 7: Deliberate DNS Problem and Recovery

1. **Break DNS resolution** by removing the internal DNS server:
   ```bash
   sudo nmcli connection modify production ipv4.dns "8.8.8.8"
   sudo nmcli connection up production
   ```

2. **Test that external resolution still works but internal fails**:
   ```bash
   ping google.com            # works
   dig intranet.example.com   # fails (assuming internal zone only exists on internal DNS)
   ```

3. **Diagnose**:
   ```bash
   dig @8.8.8.8 intranet.example.com   # likely returns NXDOMAIN
   ```

4. **Restore correct DNS**:
   ```bash
   sudo nmcli connection modify production ipv4.dns "10.20.30.2 8.8.8.8"
   sudo nmcli connection up production
   ```

### Step 8: ARP and Neighbor Table

1. **Ping the gateway** to populate the ARP cache.

2. **View the ARP table**:
   ```bash
   ip neigh
   ```
   You should see the gateway entry with `REACHABLE` or `STALE`.

3. **Legacy check** (if `net-tools` is installed):
   ```bash
   arp -n
   ```

4. **Clear the ARP cache** (optional, then repopulate):
   ```bash
   sudo ip neigh flush all
   ```

### Step 9: Monitoring and Error Checking

1. **Check interface statistics**:
   ```bash
   ip -s link show eno1
   ```
   Look for RX/TX errors, dropped packets – they should be 0.

2. **Check kernel messages for network issues**:
   ```bash
   dmesg | grep -i "eth\|link\|net"
   ```

3. **Socket summary**:
   ```bash
   ss -s
   ```

### Step 10: Document the Setup

Collect all relevant information into a report:

```bash
echo "=== IP Addresses ===" > network_report.txt
ip a >> network_report.txt
echo -e "\n=== Routing Table ===" >> network_report.txt
ip route >> network_report.txt
echo -e "\n=== Listening Services ===" >> network_report.txt
sudo ss -tulpn >> network_report.txt
echo -e "\n=== DNS Config ===" >> network_report.txt
cat /etc/resolv.conf >> network_report.txt
echo -e "\n=== Firewall Rules ===" >> network_report.txt
sudo firewall-cmd --list-all >> network_report.txt
```

Review `network_report.txt`.

---

### Final Verification Checklist

- [ ] `ip a` shows the correct static IP and netmask.
- [ ] `ip route` has a default gateway.
- [ ] `cat /etc/resolv.conf` lists both DNS servers.
- [ ] `ping -c 4 8.8.8.8` succeeds with 0% loss.
- [ ] `ping -c 4 google.com` succeeds.
- [ ] `dig intranet.example.com` (or equivalent) resolves correctly.
- [ ] `tracepath 8.8.8.8` shows a path through the gateway.
- [ ] `sudo ss -tulpn` shows `sshd` listening and no unexpected open ports.
- [ ] `sudo firewall-cmd --list-all` includes port 8080/tcp.
- [ ] `ip -s link show eno1` shows zero errors.
- [ ] `ip neigh` shows the gateway ARP entry.
- [ ] `curl -I http://localhost:8080` returns “Connection refused” (not timeout).

---

**Date documented:** 2026-04-27  
**Sources:** Red Hat System Administration, `iproute2` documentation, NetworkManager manual, Linux man pages