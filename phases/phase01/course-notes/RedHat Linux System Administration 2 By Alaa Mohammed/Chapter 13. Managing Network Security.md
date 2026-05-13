# Chapter 13: Managing Network Security

## Table of Contents

- [Chapter 13: Managing Network Security](#chapter-13-managing-network-security)
  - [Table of Contents](#table-of-contents)
  - [1. What is a Firewall? Why Do We Need It?](#1-what-is-a-firewall-why-do-we-need-it)
  - [2. Netfilter and iptables – The Kernel Firewall](#2-netfilter-and-iptables--the-kernel-firewall)
  - [3. Firewalld – Dynamic Firewall Manager](#3-firewalld--dynamic-firewall-manager)
    - [3.1 Core Concepts](#31-core-concepts)
    - [3.2 Firewalld Zones – Detailed Description](#32-firewalld-zones--detailed-description)
    - [3.3 Accept, Reject, Drop – Packet Handling](#33-accept-reject-drop--packet-handling)
  - [4. Firewalld Modes: Runtime and Permanent](#4-firewalld-modes-runtime-and-permanent)
  - [5. Firewall-cmd – Command‑Line Interface](#5-firewall-cmd--commandline-interface)
    - [5.1 Basic Operations](#51-basic-operations)
    - [5.2 Working with Services](#52-working-with-services)
    - [5.3 Working with Ports (TCP/UDP)](#53-working-with-ports-tcpudp)
    - [5.4 Rich Rules (Advanced)](#54-rich-rules-advanced)
    - [5.5 Masquerading and NAT](#55-masquerading-and-nat)
  - [6. Firewalld Configuration Files](#6-firewalld-configuration-files)
  - [7. SELinux Port Labeling](#7-selinux-port-labeling)
    - [7.1 Viewing Port Labels](#71-viewing-port-labels)
    - [7.2 Adding Custom Port Labels](#72-adding-custom-port-labels)
    - [7.3 Removing Custom Port Labels](#73-removing-custom-port-labels)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Real‑World Scenario – Securing a Public Web Application Server](#9-realworld-scenario--securing-a-public-web-application-server)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [1. Inspect current firewall state](#1-inspect-current-firewall-state)
      - [2. Allow necessary services in the public zone](#2-allow-necessary-services-in-the-public-zone)
      - [3. Restrict SSH access to your office IP using a rich rule](#3-restrict-ssh-access-to-your-office-ip-using-a-rich-rule)
      - [4. Add custom application port 3000/tcp](#4-add-custom-application-port-3000tcp)
      - [5. Allow MongoDB only from the internal app server](#5-allow-mongodb-only-from-the-internal-app-server)
      - [6. Reload the firewall to apply the permanent changes](#6-reload-the-firewall-to-apply-the-permanent-changes)
      - [7. Label the Node.js port with SELinux](#7-label-the-nodejs-port-with-selinux)
      - [8. Test connectivity](#8-test-connectivity)
      - [9. Make runtime backup (optional)](#9-make-runtime-backup-optional)
    - [Result](#result)
  - [10. Practice Lab – Verify Your Understanding](#10-practice-lab--verify-your-understanding)

---

## 1. What is a Firewall? Why Do We Need It?

A **firewall** is a system that monitors and controls incoming and outgoing network traffic based on predefined security rules. It acts as a barrier between trusted internal networks and untrusted external networks (e.g., the internet).

**Why do we need it?**
- Block unauthorised access (e.g., SSH from unknown IPs).
- Permit only necessary services (e.g., HTTP/HTTPS for web servers).
- Prevent denial‑of‑service attacks.
- Control outbound traffic (e.g., block malware connections).

**Types of firewalls (by implementation):**
- **Network firewall** – dedicated hardware appliance.
- **Host‑based firewall** – software running on the host (like firewalld, iptables).
- **Cloud firewall** – security groups, NACLs (AWS), NSGs (Azure).

This chapter focuses on **host‑based** firewalls on RHEL, specifically **firewalld** and the kernel’s **netfilter** framework.

---

## 2. Netfilter and iptables – The Kernel Firewall

- **Netfilter** is the packet filtering framework inside the Linux kernel. It hooks into the network stack at various points (PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING).
- **iptables** is the traditional user‑space tool to manipulate netfilter rules. It uses tables (`filter`, `nat`, `mangle`, `raw`) and chains (`INPUT`, `FORWARD`, `OUTPUT`).

**Why iptables is still relevant:** firewalld and other frontends ultimately generate `iptables` (or `nftables`) rules. However, for daily administration, firewalld is recommended.

**Limitations of iptables:**
- Changes are **immediate** and destructive; if you misconfigure, you lock yourself out.
- No built‑in support for zones or dynamic updates.
- Rules are stored in files and reloaded entirely on restart.

**Modern replacement:** `nftables` (RHEL 8+ uses nftables as backend, but firewalld abstracts it). Administrators rarely use `nft` directly.

---

## 3. Firewalld – Dynamic Firewall Manager

**Firewalld** is a dynamic firewall management tool that supports **zones** and **runtime/permanent** configurations. It is the default on RHEL 7, 8, 9.

### 3.1 Core Concepts

| Concept | Description |
|---------|-------------|
| **Zone** | A predefined set of rules that defines the trust level of a network interface or source IP. |
| **Service** | A predefined combination of ports, protocols, and helper modules (e.g., `ssh`, `http`, `https`). |
| **Port** | A single TCP/UDP port or range (e.g., 8080/tcp). |
| **Rich Rule** | An advanced rule that can combine source/destination, logging, actions, and time limits. |
| **Masquerade** | Source NAT (SNAT) – hides internal IP addresses behind the firewall’s IP. |
| **Forward** | Routing traffic between interfaces (e.g., from internal to external). |

### 3.2 Firewalld Zones – Detailed Description

Each zone has its own set of rules. An interface or source IP can be assigned to **only one** zone at a time.

| Zone | Trust Level | Default behaviour | Use case |
|------|-------------|-------------------|----------|
| `drop` | Lowest (0) | Any incoming packet is dropped without reply. Outgoing allowed. | Untrusted networks (e.g., public Wi‑Fi). |
| `block` | Very low | Incoming connections are rejected with `icmp-host-prohibited` message. | Similar to drop but sends a rejection. |
| `public` | Low | Only selected incoming connections (e.g., SSH) are allowed. | Typical public network (internet‑facing services). |
| `external` | Low | For systems behind a router – masquerading enabled. | Gateway / NAT router. |
| `dmz` | Medium | Allows limited access (e.g., HTTP, HTTPS) but isolates internal network. | DMZ zone for publicly accessible servers. |
| `work` | Medium | More open than public, e.g., file sharing, printing. | Trusted work environment. |
| `home` | Medium | Similar to work, but typically allows more services (UPnP). | Home network. |
| `internal` | High | Allows many services (NFS, Samba, SSH). | Trusted internal network. |
| `trusted` | Highest | Accepts all traffic (no filtering). | Very trusted network (e.g., management VLAN). |

**Viewing current zones:**
```bash
firewall-cmd --get-active-zones
```

**Listing all zones:**
```bash
firewall-cmd --get-zones
```

### 3.3 Accept, Reject, Drop – Packet Handling

| Action | Behaviour |
|--------|-----------|
| **Accept** | Let the packet pass. |
| **Drop** | Silently discard the packet (no response). Improves security but may cause timeouts. |
| **Reject** | Discard the packet and send an ICMP error (e.g., `port-unreachable`). Useful for debugging. |

In firewalld, zones define which traffic is accepted, and by default other traffic is **reject** or **drop** depending on zone (e.g., `drop` zone uses drop, `block` zone uses reject).

---

## 4. Firewalld Modes: Runtime and Permanent

| Mode | Description |
|------|-------------|
| **Runtime** | Changes take immediate effect, but are lost after reboot or firewall reload. |
| **Permanent** | Changes are stored in configuration files and survive reboot. They require a reload to take effect (or `--permanent` + `firewall-cmd --reload`). |

**Important:** Most `firewall-cmd` commands default to runtime mode. Use `--permanent` to write to persistent config. After making permanent changes, run `sudo firewall-cmd --reload` to apply them (or combine with `--runtime-to-permanent`).

---

## 5. Firewall-cmd – Command‑Line Interface

`firewall-cmd` is the primary tool for managing firewalld.

### 5.1 Basic Operations

| Operation | Command |
|-----------|---------|
| **List all rules (current zone)** | `firewall-cmd --list-all` |
| **List all rules for zone `public`** | `firewall-cmd --zone=public --list-all` |
| **Get default zone** | `firewall-cmd --get-default-zone` |
| **Set default zone** | `sudo firewall-cmd --set-default-zone=internal` |
| **Reload firewall (apply permanent)** | `sudo firewall-cmd --reload` |
| **Complete reload (resets runtime)** | `sudo firewall-cmd --complete-reload` (loss of state) |
| **Add interface to zone** | `sudo firewall-cmd --zone=public --add-interface=eth0` |
| **Query if interface in zone** | `firewall-cmd --zone=public --query-interface=eth0` |
| **Change interface zone** | `sudo firewall-cmd --zone=internal --change-interface=eth0` |

### 5.2 Working with Services

Services are pre‑defined in `/usr/lib/firewalld/services/`. You can also create custom services in `/etc/firewalld/services/`.

| Operation | Command |
|-----------|---------|
| **List available services** | `firewall-cmd --get-services` |
| **Add service (runtime)** | `sudo firewall-cmd --add-service=http` |
| **Add service (permanent)** | `sudo firewall-cmd --add-service=http --permanent` |
| **Remove service** | `sudo firewall-cmd --remove-service=http` |
| **Query if service is allowed** | `firewall-cmd --query-service=http` |

### 5.3 Working with Ports (TCP/UDP)

Use when a service is not defined or you need a specific port.

| Operation | Command |
|-----------|---------|
| **Add port (TCP, runtime)** | `sudo firewall-cmd --add-port=8080/tcp` |
| **Add port (UDP, permanent)** | `sudo firewall-cmd --add-port=53/udp --permanent` |
| **Add port range** | `sudo firewall-cmd --add-port=1000-2000/tcp` |
| **Remove port** | `sudo firewall-cmd --remove-port=8080/tcp` |
| **List ports** | `firewall-cmd --list-ports` |

**Examples:**
```bash
# Allow port 3306 (MySQL) only from internal zone
sudo firewall-cmd --zone=internal --add-port=3306/tcp
```

### 5.4 Rich Rules (Advanced)

Rich rules allow fine‑grained control: source/destination IP, logging, time limits, different actions.

**Syntax example:**
```bash
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.100" service="ssh" accept'
```

**Common rich rule patterns:**

| Purpose | Command |
|---------|---------|
| Allow SSH only from a specific IP | `sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.5" service="ssh" accept'` |
| Reject HTTP from a specific IP | `sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="1.2.3.4" service="http" reject'` |
| Log and accept a port | `sudo firewall-cmd --add-rich-rule='rule family="ipv4" port port=8080 protocol=tcp log prefix="8080_access" accept'` |
| Limit connections per second (DoS mitigation) | `sudo firewall-cmd --add-rich-rule='rule service="http" limit value="10/s" accept'` |

**Remove a rich rule:** Use `--remove-rich-rule` with the exact same string.

### 5.5 Masquerading and NAT

Masquerading allows a host to act as a router, translating private IPs to its own public IP.

| Operation | Command |
|-----------|---------|
| **Enable masquerading** | `sudo firewall-cmd --add-masquerade` |
| **Query masquerade status** | `firewall-cmd --query-masquerade` |
| **Disable masquerading** | `sudo firewall-cmd --remove-masquerade` |

**Port forwarding example (using rich rule):**
```bash
# Forward local port 2222 to port 22 on 192.168.1.10
sudo firewall-cmd --add-rich-rule='rule family=ipv4 destination address="$(ip addr show eth0 | grep -oP 'inet \K[0-9.]+')" forward-port port=2222 protocol=tcp to-port=22 to-addr=192.168.1.10'
```

---

## 6. Firewalld Configuration Files

| Path | Purpose |
|------|---------|
| `/usr/lib/firewalld/` | Default configurations (services, zones, icmptypes). Do not edit directly. |
| `/etc/firewalld/` | Custom configurations (override defaults). |
| `/etc/firewalld/zones/` | Custom zone definitions (e.g., `public.xml`, `internal.xml`). |
| `/etc/firewalld/services/` | Custom service definitions. |
| `/etc/firewalld/firewalld.conf` | Main configuration (default zone, logging, lock file). |

**Backup custom rules:**
```bash
sudo cp -r /etc/firewalld /root/firewalld_backup
```

---

## 7. SELinux Port Labeling

SELinux also restricts which **ports** a process can bind to. For example, the default HTTP port 80 is labelled `http_port_t`. If you configure Apache to listen on port 8080, you must either change the port label or add the new port to the existing type.

### 7.1 Viewing Port Labels

```bash
sudo semanage port -l | grep http
```

**Sample output:**
```
http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
```

### 7.2 Adding Custom Port Labels

If you want to run a service on a non‑standard port (e.g., SSH on port 2222), you need to label it:

```bash
# Add port 2222 to the SSH port label (ssh_port_t)
sudo semanage port -a -t ssh_port_t -p tcp 2222
```

Verify:
```bash
sudo semanage port -l | grep ssh
```

### 7.3 Removing Custom Port Labels

```bash
sudo semanage port -d -t ssh_port_t -p tcp 2222
```

**Important:** After adding a port label, `firewalld` still needs to allow the port (or service). The SELinux label and firewall work independently.

---

## 8. Quick Reference Table

| Task | Command |
|------|---------|
| List all zones | `firewall-cmd --get-zones` |
| Show current default zone | `firewall-cmd --get-default-zone` |
| Show active zones with interfaces | `firewall-cmd --get-active-zones` |
| List all rules in current zone | `firewall-cmd --list-all` |
| Add service (runtime) | `sudo firewall-cmd --add-service=http` |
| Add service (permanent) | `sudo firewall-cmd --add-service=http --permanent` |
| Remove service | `sudo firewall-cmd --remove-service=http` |
| Add port (runtime) | `sudo firewall-cmd --add-port=8080/tcp` |
| Make runtime changes permanent | `sudo firewall-cmd --runtime-to-permanent` |
| Reload permanent rules | `sudo firewall-cmd --reload` |
| Add rich rule (allow SSH from IP) | `sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.10" service="ssh" accept'` |
| Enable masquerading | `sudo firewall-cmd --add-masquerade` |
| Check SELinux port labels | `sudo semanage port -l` |
| Add custom port label (SELinux) | `sudo semanage port -a -t http_port_t -p tcp 8080` |

---

## 9. Real‑World Scenario – Securing a Public Web Application Server

### Background

You have deployed a RHEL 9 cloud instance (`web‑app‑01`) that hosts a custom Node.js application listening on **port 3000**, as well as a **MongoDB** instance that should only be accessible internally from a separate application server (`app‑01` at IP `10.0.1.20`). The server is on the public internet, so SSH must be restricted to your office static IP `203.0.113.55`. The server must also serve HTTPS (port 443) via Nginx as a reverse proxy.

Your tasks:
- Configure firewalld with a `public` zone that allows HTTP, HTTPS, and SSH (only from your office IP).
- Add the custom Node.js port 3000.
- Add a rich rule to allow port 27017 (MongoDB) only from `10.0.1.20`.
- Label the custom port with SELinux so Node.js can bind to it without denials.
- Ensure all changes persist after reboot.

### Step‑by‑Step Implementation

#### 1. Inspect current firewall state

```bash
firewall-cmd --get-default-zone
firewall-cmd --list-all
```

Likely the `public` zone is active with only `ssh` and `dhcpv6-client` allowed.

#### 2. Allow necessary services in the public zone

```bash
sudo firewall-cmd --add-service=http --add-service=https --permanent
```

#### 3. Restrict SSH access to your office IP using a rich rule

First, remove the default open SSH service (if present):

```bash
sudo firewall-cmd --remove-service=ssh --permanent
```

Then add the rich rule:

```bash
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="203.0.113.55" service="ssh" accept' --permanent
```

#### 4. Add custom application port 3000/tcp

```bash
sudo firewall-cmd --add-port=3000/tcp --permanent
```

#### 5. Allow MongoDB only from the internal app server

```bash
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.1.20" port port="27017" protocol="tcp" accept' --permanent
```

#### 6. Reload the firewall to apply the permanent changes

```bash
sudo firewall-cmd --reload
```

Verify with `sudo firewall-cmd --list-all`. You should see the services, ports, and rich rules.

#### 7. Label the Node.js port with SELinux

Check if port 3000 already has a label:

```bash
sudo semanage port -l | grep 3000
```

If not, add it to the `http_port_t` type (since Node.js web applications are treated as HTTP servers):

```bash
sudo semanage port -a -t http_port_t -p tcp 3000
```

Restart the Node.js application (or `systemctl restart nodeapp`). It should now bind to port 3000 without SELinux denials.

#### 8. Test connectivity

- From your office IP, SSH into the server. It should work.
- From another IP, attempt SSH – should be blocked.
- Access `http://server-ip` and `https://server-ip` – Nginx proxy responds.
- Access `http://server-ip:3000` directly – Node.js application responds.
- From `app‑01` (`10.0.1.20`), connect to `mongodb://web-app-01:27017` – successful.
- From any other IP, attempt the MongoDB connection – blocked.

#### 9. Make runtime backup (optional)

```bash
sudo cp -r /etc/firewalld /root/firewalld_backup_$(date +%F)
```

### Result

The web application server is now tightly secured, with only necessary services exposed, restricted administrative access, and SELinux correctly labelling custom ports.

---

## 10. Practice Lab – Verify Your Understanding

1. **Explore zones** – List all zones, check default zone, and display active zones.

2. **Add SSH service permanently** – Ensure `ssh` is allowed in the default zone (probably already). Remove it, then add it back.

3. **Add a custom port** – Allow TCP port 9999 for testing (runtime). Verify with `--list-ports`. Remove after testing.

4. **Rich rule** – Allow HTTP access only from your local subnet (e.g., `192.168.1.0/24`). Use `--add-rich-rule`. Test by trying to access from another IP (if possible).

5. **Masquerading** – On a machine with two interfaces (e.g., `eth0` external, `eth1` internal), enable masquerading and configure forwarding. (Requires IP forwarding enabled: `sysctl net.ipv4.ip_forward=1`.)

6. **SELinux port labeling** – Try to start a web server (e.g., `python3 -m http.server 8080`) and see if SELinux forbids it. Add label `http_port_t` for port 8080, then restart the server.

7. **Firewall logs** – Enable logging of dropped packets: `sudo firewall-cmd --set-log-denied=all`. Check `/var/log/messages` for `FIREWALL` entries. Revert with `--set-log-denied=off`.

---

**Date documented:** 2026-05-13  
**Sources:** Red Hat Enterprise Linux 9 Security Guide, `firewall-cmd` man page, `semanage` man page, firewalld documentation.