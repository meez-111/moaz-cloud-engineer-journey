# Day 31. IPv6

## Table of Contents

- [Day 31. IPv6](#day-31-ipv6)
  - [Table of Contents](#table-of-contents)
  - [1. Why IPv6? – The Problem with IPv4](#1-why-ipv6--the-problem-with-ipv4)
  - [2. IPv6 Address Format](#2-ipv6-address-format)
    - [2.1 Hexadecimal Notation](#21-hexadecimal-notation)
    - [2.2 Shortening IPv6 Addresses](#22-shortening-ipv6-addresses)
    - [2.3 IPv6 Prefixes](#23-ipv6-prefixes)
  - [3. IPv6 Address Types](#3-ipv6-address-types)
    - [3.1 Unicast](#31-unicast)
    - [3.2 Multicast](#32-multicast)
    - [3.3 Anycast](#33-anycast)
  - [4. Special IPv6 Addresses](#4-special-ipv6-addresses)
  - [5. IPv6 vs. IPv4 – Comparison Table](#5-ipv6-vs-ipv4--comparison-table)
  - [6. IPv6 Header Format](#6-ipv6-header-format)
  - [7. IPv6 in Cloud Engineering](#7-ipv6-in-cloud-engineering)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Practice Lab – Verify Your Understanding](#9-practice-lab--verify-your-understanding)

---

## 1. Why IPv6? – The Problem with IPv4

IPv4 provides approximately **4.3 billion** unique addresses. This seemed sufficient in the 1980s, but the explosion of internet‑connected devices (smartphones, laptops, IoT, cloud servers) has led to **IPv4 address exhaustion**.

**The problem:**
- The last IPv4 blocks were allocated in 2011.
- NAT (Network Address Translation) was a temporary fix, but it adds complexity and breaks end‑to‑end connectivity.

**The solution: IPv6**
- **128‑bit** addresses – provides **2^128** (approximately 3.4 × 10^38) addresses.
- This is enough to assign an IP address to **every atom on Earth** with room to spare.

**IPv6 is not just about more addresses** – it also includes built‑in security (IPsec), simplified headers, and better support for mobility.

---

## 2. IPv6 Address Format

### 2.1 Hexadecimal Notation

IPv6 addresses are **128 bits** long, written as **8 groups of 16 bits** (4 hexadecimal characters each), separated by colons (`:`).

**Example:**
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

| Group | Bits | Hex |
|-------|------|-----|
| 1 | 16 | 2001 |
| 2 | 16 | 0db8 |
| 3 | 16 | 85a3 |
| 4 | 16 | 0000 |
| 5 | 16 | 0000 |
| 6 | 16 | 8a2e |
| 7 | 16 | 0370 |
| 8 | 16 | 7334 |

### 2.2 Shortening IPv6 Addresses

IPv6 addresses can be shortened using two rules:

**Rule 1 – Omit leading zeros within each group:**
- `0db8` → `db8`
- `0000` → `0`
- `0370` → `370`

**Example:** `2001:0db8:85a3:0000:0000:8a2e:0370:7334` → `2001:db8:85a3:0:0:8a2e:370:7334`

**Rule 2 – Replace consecutive groups of zeros with `::` (only once per address):**
- `2001:db8:85a3:0:0:8a2e:370:7334` → `2001:db8:85a3::8a2e:370:7334`

**Examples of shortened addresses:**
- Loopback: `0:0:0:0:0:0:0:1` → `::1`
- Unspecified: `0:0:0:0:0:0:0:0` → `::`
- IPv4‑mapped: `0:0:0:0:0:ffff:192.168.1.100` → `::ffff:192.168.1.100`

### 2.3 IPv6 Prefixes

Like IPv4, IPv6 uses **CIDR notation** to specify the prefix length (number of network bits).

**Example:** `2001:db8:1234::/48`

- `/48` – first 48 bits are network prefix.
- Remaining 80 bits are host bits.
- Common prefix lengths:
  - `/32` – ISP assignment
  - `/48` – site prefix (typical for organisations)
  - `/64` – subnet prefix (the only prefix that supports SLAAC – Stateless Address Autoconfiguration)

**Subnetting in IPv6:**
- Unlike IPv4, IPv6 subnets are usually `/64` (providing 2^64 host addresses – enough for any subnet).
- Smaller subnets (e.g., `/127`) are used for point‑to‑point links (RFC 6164).

---

## 3. IPv6 Address Types

### 3.1 Unicast

A **unicast** address identifies a single interface. Packets sent to a unicast address are delivered to that specific interface.

| Type | Prefix | Description |
|------|--------|-------------|
| **Global Unicast** | `2000::/3` | Routable on the internet (similar to IPv4 public IPs). |
| **Unique Local (ULA)** | `fc00::/7` | Private, internally routable (similar to IPv4 private IPs). |
| **Link‑Local** | `fe80::/10` | Auto‑configured, only valid on the local link (not routed). |
| **Loopback** | `::1/128` | Localhost (similar to `127.0.0.1`). |
| **Unspecified** | `::/128` | Represents an unknown address (used in source fields). |

### 3.2 Multicast

A **multicast** address identifies a **group** of interfaces. Packets sent to a multicast address are delivered to all members of the group.

- Prefix: `ff00::/8`
- Well‑known multicast addresses:
  - `ff02::1` – all nodes on the local link
  - `ff02::2` – all routers on the local link
  - `ff02::fb` – mDNS

### 3.3 Anycast

An **anycast** address is assigned to **multiple interfaces** (usually on different routers). Packets are delivered to the **nearest** (most routing‑protocol‑optimal) interface.

**Use case:** DNS servers, CDN edge nodes. Anycast ensures users reach the closest server, reducing latency.

---

## 4. Special IPv6 Addresses

| Address | Prefix | Description |
|---------|--------|-------------|
| **Loopback** | `::1/128` | Localhost – similar to `127.0.0.1`. |
| **Unspecified** | `::/128` | Used when no address is assigned (e.g., DHCP requests). |
| **Link‑Local** | `fe80::/10` | Automatically assigned; used for local network communication (e.g., Neighbor Discovery, DHCPv6). |
| **Unique Local (ULA)** | `fc00::/7` | Private addresses for internal use (not routable on the internet). |
| **Global Unicast** | `2000::/3` | Public, globally routable addresses. |
| **Multicast** | `ff00::/8` | Group communication. |
| **IPv4‑mapped** | `::ffff:0:0/96` | Represents IPv4 addresses within IPv6 (for transition). |

**Link‑Local vs. Unique Local:**
- **Link‑Local** – only works on the same subnet; not routable.
- **Unique Local** – routable within the organisation (like RFC 1918 private IPs), but not on the internet.

---

## 5. IPv6 vs. IPv4 – Comparison Table

| Feature | IPv4 | IPv6 |
|---------|------|------|
| **Address size** | 32 bits | 128 bits |
| **Address space** | ~4.3 billion | 3.4 × 10^38 |
| **Notation** | Dotted decimal | Hexadecimal |
| **Example** | `192.168.1.100` | `2001:db8::1` |
| **NAT** | Required (for private IPs) | Not required |
| **Header complexity** | More complex | Simplified |
| **IPsec** | Optional | Built‑in |
| **Auto‑configuration** | DHCP (optional) | SLAAC (built‑in) |
| **Broadcast** | Yes (255.255.255.255) | No (uses multicast) |
| **Checksum** | Header checksum | Removed (handled at higher layers) |
| **IPv6 migration** | – | Dual‑stack, tunnels, translation |

---

## 6. IPv6 Header Format

The IPv6 header is **simpler and more efficient** than IPv4 – it has a fixed size of 40 bytes and fewer fields.

```
+---------+---------+---------+---------+
| Version | Traffic Class | Flow Label   |
|  (4)    |    (8)       |    (20)      |
+---------+---------+---------+---------+
| Payload Length  | Next Header | Hop Limit |
|    (16)         |    (8)      |    (8)    |
+---------+---------+---------+---------+
|               Source Address             |
|               (128 bits)                 |
+-----------------------------------------+
|             Destination Address          |
|               (128 bits)                 |
+-----------------------------------------+
```

- **Version** – 6 (for IPv6)
- **Traffic Class** – QoS (similar to IPv4 ToS)
- **Flow Label** – identifies a specific flow (for QoS and load balancing)
- **Payload Length** – length of the data (not including header)
- **Next Header** – indicates the next protocol (TCP, UDP, ICMPv6, or an extension header)
- **Hop Limit** – replaces TTL (prevents packets from looping forever)

---

## 7. IPv6 in Cloud Engineering

**IPv6 adoption in cloud:**
- Most cloud providers (AWS, Azure, GCP) support IPv6, but **IPv4 is still dominant**.
- AWS VPCs can be configured with **dual‑stack** (both IPv4 and IPv6).
- IPv6 addresses are **global** – they can be reached from the internet without NAT.

**AWS IPv6 features:**
- VPCs can have an IPv6 CIDR (e.g., `2600:1f18::/56`).
- Subnets can be assigned a `/64` IPv6 CIDR.
- EC2 instances can receive IPv6 addresses automatically.
- IPv6 traffic can be routed through Internet Gateway (no NAT required).
- Security Groups support IPv6 CIDRs.

**Azure IPv6 features:**
- Dual‑stack virtual networks (VNet).
- IPv6 supports both public and private addresses.
- Load Balancer supports IPv6 frontend configurations.

**GCP IPv6 features:**
- VPC networks can have IPv6 enabled.
- Compute Engine instances can have IPv6 addresses.
- Global and regional load balancers support IPv6.

**Why IPv6 is still not mandatory:**
- Most workloads still use IPv4.
- NAT and IPv4 have been "good enough" for internal cloud networks.
- Transitioning requires infrastructure changes (firewalls, load balancers, monitoring).

**When to consider IPv6:**
- If your users are in regions with heavy IPv6 adoption (e.g., India, USA).
- If you need to avoid NAT for end‑to‑end encryption.
- If you are building IoT or mobile‑first applications.

---

## 8. Quick Reference Table

| Topic | Details |
|-------|---------|
| **Address bits** | 128 bits |
| **Groups** | 8 groups of 16 bits (hexadecimal) |
| **Shortening rules** | Omit leading zeros, use `::` for consecutive zeros |
| **Loopback** | `::1` |
| **Unspecified** | `::` |
| **Link‑Local** | `fe80::/10` (auto‑configured) |
| **Unique Local** | `fc00::/7` (private) |
| **Global Unicast** | `2000::/3` (public) |
| **Multicast** | `ff00::/8` |
| **Prefix lengths** | `/32` (ISP), `/48` (site), `/64` (subnet) |
| **SLAAC** | Stateless Address Autoconfiguration (uses `/64` prefix) |
| **Header size** | 40 bytes (fixed) |
| **Cloud support** | AWS, Azure, GCP (dual‑stack) |

---

## 9. Practice Lab – Verify Your Understanding

1. **Shorten the following IPv6 addresses:**
   - `2001:0db8:0000:0000:0000:0000:0000:0001`
   - `fe80:0000:0000:0000:0200:5eff:fe00:1234`
   - `ff02:0000:0000:0000:0000:0000:0000:0002`

2. **Expand the following shortened IPv6 addresses:**
   - `2001:db8::1`
   - `fe80::1`
   - `::ffff:192.168.1.100`

3. **Find your IPv6 address (if available):**
   - Run `ip -6 addr` or `ifconfig` on your Linux machine.

4. **Cloud scenario:**
   - You are creating an AWS VPC. You add an IPv6 CIDR block. Your subnets now have both IPv4 and IPv6. How do you ensure EC2 instances can be reached over IPv6? (Attach an IPv6 address, update security groups, route through Internet Gateway.)

5. **Prefix calculation:**
   - How many subnets can you create from a `/48` prefix if each subnet is `/64`?  
     - Answer: `2^(64-48) = 2^16 = 65,536` subnets.

---

**Date documented:** 2026-06-16  
**Sources:** RFC 8200 (IPv6), AWS VPC documentation, cloud provider networking guides

---