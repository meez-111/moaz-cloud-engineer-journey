# IPv4 Addressing – Complete Professional Guide

## Table of Contents

- [IPv4 Addressing – Complete Professional Guide](#ipv4-addressing--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What is an IPv4 Address?](#1-what-is-an-ipv4-address)
  - [2. IPv4 Address Structure](#2-ipv4-address-structure)
    - [2.1 Binary vs. Decimal Representation](#21-binary-vs-decimal-representation)
    - [2.2 Network and Host Portions](#22-network-and-host-portions)
  - [3. IPv4 Address Classes (Classful Addressing)](#3-ipv4-address-classes-classful-addressing)
    - [3.1 Class A, B, C, D, E](#31-class-a-b-c-d-e)
    - [3.2 Reserved Addresses](#32-reserved-addresses)
  - [4. Private IPv4 Addresses (RFC 1918)](#4-private-ipv4-addresses-rfc-1918)
  - [5. Special IPv4 Addresses](#5-special-ipv4-addresses)
    - [5.1 Loopback (127.0.0.0/8)](#51-loopback-1270008)
    - [5.2 Link‑Local (169.254.0.0/16)](#52-linklocal-1692540016)
    - [5.3 Multicast (224.0.0.0/4)](#53-multicast-2240004)
    - [5.4 Limited Broadcast (255.255.255.255)](#54-limited-broadcast-255255255255)
  - [6. IPv4 vs. IPv6](#6-ipv4-vs-ipv6)
  - [7. IPv4 in Cloud Engineering](#7-ipv4-in-cloud-engineering)
    - [7.1 VPC CIDR Blocks](#71-vpc-cidr-blocks)
    - [7.2 Public vs. Private IPs in AWS](#72-public-vs-private-ips-in-aws)
    - [7.3 Elastic IPs (AWS)](#73-elastic-ips-aws)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Practice Lab – Verify Your Understanding](#9-practice-lab--verify-your-understanding)

---

## 1. What is an IPv4 Address?

An **IPv4 address** is a 32‑bit numerical label assigned to each device on a network. It serves two primary functions:

- **Network identification** – identifies which network the device belongs to.
- **Host identification** – identifies the specific device on that network.

**Analogy:** An IP address is like a postal address. The network portion is the street, and the host portion is the house number.

---

## 2. IPv4 Address Structure

### 2.1 Binary vs. Decimal Representation

- **32 bits** divided into **4 octets** (8 bits each).
- Written in **dotted decimal** notation: `192.168.1.100`.

| Decimal | Binary |
|---------|--------|
| 192 | 11000000 |
| 168 | 10101000 |
| 1   | 00000001 |
| 100 | 01100100 |

Each octet ranges from `0` to `255` (2^8 = 256 values).

### 2.2 Network and Host Portions

An IP address consists of two parts:

- **Network portion** – identifies the network (subnet).
- **Host portion** – identifies the specific device on that network.

The **subnet mask** (or prefix length) defines the boundary between network and host bits.

| Example | Subnet Mask | Network Bits | Host Bits |
|---------|-------------|--------------|-----------|
| `192.168.1.100/24` | `255.255.255.0` | 24 | 8 |
| `10.0.0.5/8` | `255.0.0.0` | 8 | 24 |
| `172.16.10.0/16` | `255.255.0.0` | 16 | 16 |

---

## 3. IPv4 Address Classes (Classful Addressing)

In the early internet, addresses were divided into **fixed classes** based on the first few bits.

| Class | Leading Bits | First Octet Range | Default Mask | Use | Total Addresses |
|-------|--------------|-------------------|--------------|-----|-----------------|
| A | `0` | 1–126 | /8 | Large networks | 16,777,216 |
| B | `10` | 128–191 | /16 | Medium networks | 65,536 |
| C | `110` | 192–223 | /24 | Small networks | 256 |
| D | `1110` | 224–239 | (none) | Multicast | – |
| E | `1111` | 240–255 | (none) | Experimental | – |

**Note:** Classful addressing is **obsolete**. Modern networks use **CIDR** (Classless Inter‑Domain Routing) for flexible allocation.

### 3.1 Class A, B, C, D, E

| Class | Purpose | Example Range |
|-------|---------|---------------|
| **A** | Very large networks (e.g., `10.0.0.0/8` – private) | `10.0.0.0 – 10.255.255.255` |
| **B** | Medium networks (e.g., `172.16.0.0/12` – private) | `172.16.0.0 – 172.31.255.255` |
| **C** | Small networks (e.g., `192.168.0.0/16` – private) | `192.168.0.0 – 192.168.255.255` |
| **D** | Multicast groups | `224.0.0.0 – 239.255.255.255` |
| **E** | Reserved for future use / research | `240.0.0.0 – 255.255.255.255` |

### 3.2 Reserved Addresses

| Address Range | Purpose |
|---------------|---------|
| `0.0.0.0/8` | Network identification (default route) |
| `127.0.0.0/8` | Loopback (localhost – `127.0.0.1`) |
| `169.254.0.0/16` | Link‑Local (APIPA – when DHCP fails) |
| `224.0.0.0/4` | Multicast |
| `255.255.255.255` | Limited Broadcast |

---

## 4. Private IPv4 Addresses (RFC 1918)

Private addresses are **not globally routable** – they cannot be used on the public internet. They are intended for internal networks and **must be translated** via NAT to communicate with the internet.

| Class | Private Range | CIDR | Total Addresses |
|-------|---------------|------|-----------------|
| A | `10.0.0.0 – 10.255.255.255` | `10.0.0.0/8` | 16,777,216 |
| B | `172.16.0.0 – 172.31.255.255` | `172.16.0.0/12` | 1,048,576 |
| C | `192.168.0.0 – 192.168.255.255` | `192.168.0.0/16` | 65,536 |

**Why private addresses?**
- Conserve public IPv4 space.
- Provide security (internal devices are not directly exposed to the internet).
- Flexible internal addressing – can be renumbered without affecting external connectivity.

**Cloud relevance:** Every VPC (AWS, Azure, GCP) uses private IP ranges (commonly `10.0.0.0/16` or `172.31.0.0/16`) for instances.

---

## 5. Special IPv4 Addresses

### 5.1 Loopback (127.0.0.0/8)

- Used for **internal communication** on the same device.
- `127.0.0.1` is the standard localhost address.
- Traffic sent to loopback never leaves the device.

**Use:** Testing network services locally (e.g., `curl localhost:8080`).

### 5.2 Link‑Local (169.254.0.0/16)

- Assigned automatically when a DHCP server is unavailable.
- Also called **APIPA** (Automatic Private IP Addressing).
- Only works within the same subnet – no routing to the internet.

**Use:** Troubleshooting when `ifconfig` shows a `169.254.x.x` address – indicates DHCP failure.

### 5.3 Multicast (224.0.0.0/4)

- Used to send a single packet to **multiple** hosts simultaneously.
- Common in streaming media, routing protocols (OSPF, EIGRP), and service discovery.

**Cloud note:** Not commonly used in day‑to‑day cloud engineering.

### 5.4 Limited Broadcast (255.255.255.255)

- Sends a packet to **all devices** on the local network.
- Used for DHCP discovery and ARP requests.

**Note:** Routers do **not** forward broadcast packets.

---

## 6. IPv4 vs. IPv6

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address size | 32 bits | 128 bits |
| Dotted decimal | `192.168.1.100` | Hexadecimal: `2001:0db8::1` |
| Address space | ~4.3 billion | 2^128 (virtually unlimited) |
| NAT required | Yes (for private IPs) | No (enough addresses for every device) |
| Header complexity | More complex | Simplified |
| Security | IPsec optional | IPsec built‑in |
| Adoption | Still dominant | Growing, but slow |

**Cloud relevance:** Most cloud providers still use IPv4 internally. IPv6 support is available but often optional.

---

## 7. IPv4 in Cloud Engineering

### 7.1 VPC CIDR Blocks

When you create a VPC, you define a **CIDR block** – the IP range for your entire virtual network.

**Common VPC CIDRs:**

| CIDR | Addresses | Use |
|------|-----------|-----|
| `10.0.0.0/16` | 65,536 | Large VPC |
| `10.0.0.0/20` | 4,096 | Medium VPC |
| `172.31.0.0/16` | 65,536 | AWS default VPC |

### 7.2 Public vs. Private IPs in AWS

| IP Type | Description | Example |
|---------|-------------|---------|
| **Private IPv4** | Internal IP within the VPC | `10.0.1.10` |
| **Public IPv4** | Routable over the internet | `203.0.113.5` |
| **Elastic IPv4** | Static public IP (attached/removed) | `54.123.45.67` |

- Instances in private subnets have **no public IP** – they reach the internet via **NAT Gateway**.
- Instances in public subnets can have a public IP (assigned automatically or via Elastic IP).

### 7.3 Elastic IPs (AWS)

- A **static** public IPv4 address.
- Can be remapped between instances.
- You are charged for idle Elastic IPs (not attached to a running instance).

**Use:** Public‑facing services (web servers, VPN gateways) that need a consistent IP.

---

## 8. Quick Reference Table

| Topic | Details |
|-------|---------|
| **IPv4 bits** | 32 bits (4 octets) |
| **Private ranges** | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| **Loopback** | `127.0.0.1` (localhost) |
| **Link‑Local** | `169.254.0.0/16` (APIPA) |
| **Broadcast** | `255.255.255.255` (local network) |
| **Public IPs** | Routable on the internet (assigned by ISPs, cloud providers) |
| **NAT** | Translates private IPs to public IPs |
| **VPC CIDR** | `10.0.0.0/16` or `172.31.0.0/16` (common) |
| **Elastic IP** | Static public IP in AWS |

---

## 9. Practice Lab – Verify Your Understanding

1. **Identify your current IP:**
   - On your Linux machine, run `ip a` or `ifconfig`. Identify your IPv4 address, subnet mask, and broadcast address.

2. **Classify an IP:**
   - Is `10.0.0.5` private or public? What class is it?
   - Is `172.16.10.100` private or public? What class is it?
   - Is `192.168.1.50` private or public? What class is it?

3. **Cloud scenario:**
   - You create an AWS VPC with `10.0.0.0/16`. How many total addresses are available? How many are usable?
   - You create a subnet with `10.0.1.0/24`. How many usable addresses? What is the network address? Broadcast address?

4. **Troubleshooting:**
   - Your EC2 instance is assigned a private IP of `10.0.1.5` but cannot reach the internet. What services do you need? (NAT Gateway / Internet Gateway)

5. **Elastic IP:**
   - When would you use an Elastic IP instead of an auto‑assigned public IP?

---

**Date documented:** 2026-06-16  
**Sources:** RFC 791 (IPv4), RFC 1918 (Private Addresses), AWS VPC documentation

---
