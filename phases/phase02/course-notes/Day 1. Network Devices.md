# Day 1: Network Devices

This guide defines the fundamental building blocks of any network: **clients, servers, switches, routers, and firewalls**. Understanding the role of each device is essential for designing, troubleshooting, and securing networks – including cloud‑based virtual networks.

---

## Table of Contents

- [Day 1: Network Devices](#day-1-network-devices)
  - [Table of Contents](#table-of-contents)
  - [1. What is a Network?](#1-what-is-a-network)
  - [2. Network Nodes](#2-network-nodes)
  - [3. Clients and Servers](#3-clients-and-servers)
  - [4. Switches](#4-switches)
  - [5. Routers](#5-routers)
  - [6. Firewalls](#6-firewalls)
    - [6.1 Hardware Firewalls](#61-hardware-firewalls)
    - [6.2 Next‑Generation Firewalls (NGFW)](#62-nextgeneration-firewalls-ngfw)
    - [6.3 Host‑Based Firewalls](#63-hostbased-firewalls)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [Defense in Depth Diagram (Conceptual)](#defense-in-depth-diagram-conceptual)

---

## 1. What is a Network?

A **network** is a collection of connected devices (computers, servers, printers, etc.) that can share resources (files, printers, internet access) and communicate with each other.

- **Purpose:** Resource sharing, communication, centralised data storage, remote access.
- **Examples:** Home Wi‑Fi, corporate LAN, cloud VPC.

---

## 2. Network Nodes

A **node** is any active device connected to a network. Nodes can be:

- **End devices:** Computers, servers, smartphones, printers.
- **Intermediate devices:** Switches, routers, firewalls, access points.

Every node has at least one **network interface** (NIC) and an **IP address** (at Layer 3).

---

## 3. Clients and Servers

| Device Type | Role | Examples |
|-------------|------|----------|
| **Client** | Requests services or resources from a server. | PC, laptop, smartphone, IoT device. |
| **Server** | Provides services (web, email, file, database) to clients. | Web server, mail server, file server, database server. |

> **Note:** The same physical device can act as both a client and a server depending on the context. For example, a database server might request updates from a repository (acting as client) while simultaneously serving queries (acting as server).

---

## 4. Switches

A **switch** operates at **Layer 2 (Data Link)** of the OSI model. It connects multiple devices **within the same Local Area Network (LAN)**.

| Feature | Description |
|---------|-------------|
| **Function** | Forwards data (frames) based on **MAC addresses**. |
| **Port count** | Typically 24, 48, or more ports for end hosts. |
| **Capability** | Cannot connect different LANs or route over the internet. |
| **Intelligence** | Learns which MAC address is on which port (MAC address table). |
| **Traffic handling** | Sends frames only to the destination port – not broadcast to all (unlike hubs). |

**Use case:** Connecting all computers and printers in an office floor.

**Cloud equivalent:** Virtual switches inside a hypervisor (e.g., Open vSwitch) or AWS VPC subnet (implicit switching).

---

## 5. Routers

A **router** operates at **Layer 3 (Network)**. It connects **different networks** (e.g., LAN to WAN, LAN to another LAN) and forwards packets based on **IP addresses**.

| Feature | Description |
|---------|-------------|
| **Function** | Routes packets between networks using IP addresses and routing tables. |
| **Port count** | Fewer ports than a switch (e.g., 2, 4, 8) – typically one port connects to ISP, others to internal switches. |
| **Capability** | Connects LANs together and provides access to the internet. |
| **Intelligence** | Maintains a routing table (static or dynamic via OSPF, BGP). |
| **Additional features** | Many include NAT, DHCP, firewall, VPN. |

**Use case:** Connecting a home LAN to the internet; connecting corporate branch offices via a WAN router.

**Cloud equivalent:** Virtual routers (e.g., AWS Route Tables, Azure Route Server), Internet Gateway, NAT Gateway.

---

## 6. Firewalls

A **firewall** controls incoming and outgoing network traffic based on a set of security rules (policies). It is a critical security device.

### 6.1 Hardware Firewalls

- **Dedicated physical appliance** placed at the network perimeter (between internal network and internet).
- Filters traffic based on:
  - Source/destination IP
  - Port numbers (TCP/UDP)
  - Protocol (e.g., HTTP, SSH)
- Can be placed **inside** the network (internal segmentation) or **outside** (edge firewall).

### 6.2 Next‑Generation Firewalls (NGFW)

Modern firewalls that go beyond simple port/protocol filtering. NGFW features:

- **Deep Packet Inspection (DPI)** – inspects application‑layer payloads.
- **Intrusion Detection/Prevention System (IDS/IPS)** – detects and blocks known attack patterns.
- **Application awareness** – e.g., allow Facebook but block Facebook chat.
- **TLS/SSL decryption** (with proper policies).
- **User identity awareness** (tied to Active Directory).

**Examples:** Palo Alto Networks, Fortinet FortiGate, Cisco Firepower.

### 6.3 Host‑Based Firewalls

- **Software running on an individual host** (server, PC, laptop).
- Filters traffic entering or exiting that specific machine.
- Provides **defense in depth** – even if the network firewall is compromised, the host firewall still protects.

**Examples:**
- **Linux:** `firewalld`, `iptables`, `nftables`
- **Windows:** Windows Defender Firewall
- **Cloud:** Security Groups (AWS), Network Security Groups (Azure), Cloud Firewall (GCP)

> **Key principle:** Even when a network firewall is in place, each host should run a host‑based firewall as a **defense in depth** measure.

---

## 7. Quick Reference Table

| Device | OSI Layer | Primary Function | Identifies Traffic By | Example |
|--------|-----------|------------------|-----------------------|---------|
| **Switch** | Layer 2 (Data Link) | Forward frames within a LAN | MAC address | Office LAN switch |
| **Router** | Layer 3 (Network) | Route packets between networks | IP address | Home Wi‑Fi router |
| **Firewall (hardware)** | Layers 3–4 (and up) | Filter traffic based on rules | IP, port, protocol, application | Corporate edge firewall |
| **Host firewall** | Software on host | Filter traffic to/from the host | IP, port, application | `firewalld`, Security Group |

---

## Defense in Depth Diagram (Conceptual)

```
Internet
    │
    ▼
[Edge Firewall (hardware NGFW)]   ← perimeter security
    │
    ▼
[Router]
    │
    ▼
[Switch] ────┬──── [Server A with host firewall]
             ├──── [Server B with host firewall]
             └──── [Workstation with host firewall]
```

Even if an attacker bypasses the edge firewall, the host firewalls on each server provide additional layers of protection.

---

**Date documented:** 2026-06-14  
**Sources:** Networking fundamentals, Cisco/CompTIA Network+ materials

---
