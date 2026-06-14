# Phase 2: Networking Fundamentals – Complete Professional Guide

This guide covers the essential networking concepts every cloud engineer must know: IP addressing, subnetting, CIDR, ports and protocols, OSI/TCP‑IP models, network infrastructure devices, and cloud‑specific networking (VPC, CDN, WAF).

---

## Table of Contents

- [Phase 2: Networking Fundamentals – Complete Professional Guide](#phase-2-networking-fundamentals--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. IP Addressing (IPv4 \& IPv6)](#1-ip-addressing-ipv4--ipv6)
    - [IPv4](#ipv4)
    - [IPv6](#ipv6)
  - [2. Subnetting and CIDR](#2-subnetting-and-cidr)
    - [Subnetting](#subnetting)
    - [CIDR (Classless Inter‑Domain Routing)](#cidr-classless-interdomain-routing)
    - [Broadcast Address](#broadcast-address)
  - [3. Ports and Protocols](#3-ports-and-protocols)
    - [Ports – Addressing Applications on a Machine](#ports--addressing-applications-on-a-machine)
      - [Common Ports](#common-ports)
    - [Protocols – Rules for Data Transmission](#protocols--rules-for-data-transmission)
  - [4. OSI and TCP/IP Models](#4-osi-and-tcpip-models)
    - [OSI Model (7 layers)](#osi-model-7-layers)
    - [TCP/IP Model (4 layers)](#tcpip-model-4-layers)
  - [5. SSL/TLS Handshake](#5-ssltls-handshake)
  - [6. Network Infrastructure Devices](#6-network-infrastructure-devices)
  - [7. VLANs (Virtual LANs)](#7-vlans-virtual-lans)
  - [8. NAT (Network Address Translation)](#8-nat-network-address-translation)
  - [9. VPNs and Load Balancers](#9-vpns-and-load-balancers)
    - [VPN (Virtual Private Network)](#vpn-virtual-private-network)
    - [Load Balancer](#load-balancer)
  - [10. Firewalls and DNS](#10-firewalls-and-dns)
    - [Firewall](#firewall)
    - [DNS (Domain Name System)](#dns-domain-name-system)
  - [11. Cloud Networking – VPC, Route Tables, CDN, WAF](#11-cloud-networking--vpc-route-tables-cdn-waf)
    - [VPC (Virtual Private Cloud)](#vpc-virtual-private-cloud)
    - [Route Tables](#route-tables)
    - [CDN (Content Delivery Network)](#cdn-content-delivery-network)
    - [WAF (Web Application Firewall)](#waf-web-application-firewall)
  - [12. Quick Reference Table](#12-quick-reference-table)

---

## 1. IP Addressing (IPv4 & IPv6)

An **IP address** is a unique numerical label assigned to each device on a network. Without it, data cannot be delivered – like a pizza delivery needing your address.

### IPv4

- **32‑bit** address, written as four decimal octets separated by dots.
- Each octet ranges from `0` to `255`.
- Total possible addresses: **≈4.3 billion**.
- Example: `192.168.1.100`

**Problem:** IPv4 address exhaustion – the world ran out of unique IPv4 addresses, especially with the explosion of IoT devices.

### IPv6

- **128‑bit** address, written in hexadecimal, grouped in 8 blocks of 16 bits.
- Provides virtually unlimited addresses.
- Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Bit length | 32 bits | 128 bits |
| Notation | Dotted decimal | Hexadecimal |
| Header complexity | More complex | Simplified |
| Hop limit field | TTL (Time to Live) | Hop Limit |
| Availability | Exhausted | Abundant |

**Why TTL/Hop Limit?** Prevents packets from looping forever on the network.

**Cloud note:** Most internal cloud networks still use IPv4, but understanding IPv6 is important as systems scale.

---

## 2. Subnetting and CIDR

### Subnetting

Subnetting divides a larger network into smaller, logical subnetworks. Benefits:

- **Organization** – like dividing a city into neighbourhoods.
- **Security** – if one subnet is compromised, others remain isolated.
- **Performance** – reduces broadcast traffic.

### CIDR (Classless Inter‑Domain Routing)

CIDR is a compact way to describe subnets. It uses a slash (`/`) followed by the number of network bits.

**Example:** `192.168.1.0/24` means the first **24 bits** are the network prefix, leaving **8 bits** for host addresses.

- Available host addresses: `2^(32 - 24) - 2 = 254` usable IPs (subtract network and broadcast addresses).
- In the cloud (e.g., AWS VPC), CIDR blocks define the IP range for your virtual network.

### Broadcast Address

A special address used to send a message to **all devices within a subnet** for device discovery.

---

## 3. Ports and Protocols

### Ports – Addressing Applications on a Machine

An IP address finds the **machine**; a **port** finds the **specific application or service** on that machine.

**Analogy:** IP address is the building address; the port is the apartment number.

**Port mapping:** Crucial for containers – e.g., mapping host port `80` to container port `3000`.

#### Common Ports

| Port | Protocol | Service |
|------|----------|---------|
| 20,21 | TCP | FTP (File Transfer) |
| 22 | TCP | SSH (Secure Shell) |
| 23 | TCP | Telnet (unencrypted) |
| 25 | TCP | SMTP (Email sending) |
| 53 | TCP/UDP | DNS (Domain Name System) |
| 80 | TCP | HTTP (Web) |
| 110 | TCP | POP3 (Email retrieval) |
| 123 | UDP | NTP (Network Time) |
| 143 | TCP | IMAP (Email) |
| 443 | TCP | HTTPS (Secure Web) |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |

### Protocols – Rules for Data Transmission

Protocols define **how** data is packaged and transmitted.

| Protocol | Layer | Description |
|----------|-------|-------------|
| **TCP** | Transport | Connection‑oriented, reliable, ordered. Used for web, email, file transfer. |
| **UDP** | Transport | Connectionless, fast, no guarantee. Used for streaming, DNS, VoIP. |
| **IP** | Network | Routing and addressing. |
| **ICMP** | Network | Diagnostic (e.g., `ping`). |
| **HTTP/HTTPS** | Application | Web traffic. |

---

## 4. OSI and TCP/IP Models

### OSI Model (7 layers)

The OSI model is **conceptual** – it helps diagnose network problems by pinpointing which layer is failing.

| Layer | Name | Function | Example |
|-------|------|----------|---------|
| 7 | Application | User interaction | HTTP, FTP, DNS |
| 6 | Presentation | Data translation, encryption | SSL/TLS, JPEG |
| 5 | Session | Manage sessions | NetBIOS, RPC |
| 4 | Transport | Reliable delivery, error recovery | TCP, UDP |
| 3 | Network | Routing, addressing | IP, ICMP |
| 2 | Data Link | Framing, MAC addressing | Ethernet, Wi‑Fi |
| 1 | Physical | Cables, signals, bits | Ethernet cable, radio |

### TCP/IP Model (4 layers)

The **internet actually runs on the TCP/IP model** – it condenses OSI layers into four.

| Layer | OSI Equivalent |
|-------|----------------|
| **Application** | Layers 5,6,7 |
| **Transport** | Layer 4 |
| **Internet** | Layer 3 |
| **Network Access** | Layers 1,2 |

**Why learn these models?** They help you diagnose issues: a broken cable is Layer 1; a misconfigured firewall rule is Layer 3/4; a certificate error is Layer 6.

---

## 5. SSL/TLS Handshake

The SSL/TLS handshake is where client and server **authenticate**, agree on an encryption algorithm, and exchange keys **before** transmitting data.

**Simplified steps:**

1. **Client Hello** – client sends supported cipher suites, TLS version, and a random number.
2. **Server Hello** – server chooses cipher suite, sends its certificate (public key) and a random number.
3. **Certificate Verification** – client verifies the server certificate (trust chain).
4. **Key Exchange** – client generates a pre‑master secret, encrypts with server’s public key, sends it.
5. **Session Keys Generation** – both sides derive symmetric session keys.
6. **Finished Messages** – encrypted handshake confirmation.
7. **Secure Data Transfer** – application data is encrypted with session keys.

---

## 6. Network Infrastructure Devices

| Device | Layer | Function |
|--------|-------|----------|
| **Hub** | Layer 1 (Physical) | Broadcasts every packet to all connected devices (obsolete). |
| **Switch** | Layer 2 (Data Link) | Uses **MAC addresses** to send packets only to the destination device. |
| **Router** | Layer 3 (Network) | Connects different networks, uses **IP addresses** to route traffic between networks and the internet. |

**Analogy:** Routers are highway intersections; switches are neighbourhood intersections.

---

## 7. VLANs (Virtual LANs)

VLANs create **logical** (not physical) network segmentation. For example, you can separate guest Wi‑Fi traffic from admin traffic on the same physical switches. This improves security and reduces broadcast domains.

---

## 8. NAT (Network Address Translation)

NAT allows an entire private network to share **one public IP address** to access the internet. It translates private IPv4 addresses (e.g., `192.168.1.x`) to a single public IP.

**Why NAT?** IPv4 addresses are limited and expensive. Instead of giving every device a public IP, NAT conserves addresses. In cloud networking, NAT Gateways allow private subnets to reach the internet.

---

## 9. VPNs and Load Balancers

### VPN (Virtual Private Network)

Creates an encrypted tunnel over the internet, extending a private network securely.

### Load Balancer

Distributes incoming traffic across multiple servers to avoid overloading a single server.

**Types:**
- **Application Load Balancer** (Layer 7) – routes based on HTTP headers, URL.
- **Network Load Balancer** (Layer 4) – routes based on IP and port.

---

## 10. Firewalls and DNS

### Firewall

Controls incoming and outgoing traffic based on predefined rules. In the cloud, firewalls correspond to **Security Groups** (AWS), **Cloud Firewalls** (GCP), and **Network Security Groups** (Azure).

### DNS (Domain Name System)

Humans cannot remember IP addresses. DNS translates domain names (e.g., `www.google.com`) into IP addresses.

**Complete DNS process:**

1. User types `www.example.com` in browser.
2. Browser checks local cache.
3. Recursive resolver queries root DNS server.
4. Root server directs to TLD (Top‑Level Domain) server (`.com`).
5. TLD server directs to authoritative DNS server for `example.com`.
6. Authoritative server returns the IP address.
7. Browser uses IP to connect.

---

## 11. Cloud Networking – VPC, Route Tables, CDN, WAF

### VPC (Virtual Private Cloud)

A **private** section of the cloud provider’s network, isolated for your resources. You define your own IP range using CIDR.

- Common internal IP range: `10.0.0.0/16`
- Inside a VPC, you create **subnets**:
  - **Public subnet** – faces the internet (load balancers, bastion hosts, internet gateway).
  - **Private subnet** – not directly internet‑accessible (databases, internal servers). Uses **NAT Gateway** to access the internet for updates.

### Route Tables

Define rules (routes) that determine where network traffic is directed. Each subnet in a VPC is associated with a route table.

### CDN (Content Delivery Network)

Caches content at **edge locations** (servers around the world) to bring data closer to users, reducing latency. Also helps protect against DDoS attacks.

### WAF (Web Application Firewall)

Filters and blocks malicious traffic (e.g., SQL injection, cross‑site scripting) before it reaches your web servers.

---

## 12. Quick Reference Table

| Concept | Short Definition | Example / Command |
|---------|------------------|-------------------|
| IPv4 address | 32‑bit, dotted decimal | `192.168.1.100` |
| IPv6 address | 128‑bit, hexadecimal | `2001:0db8:...` |
| CIDR | Compact subnet description | `/24` means 24 network bits |
| Subnetting | Dividing a network | `10.0.0.0/16` into `/24` subnets |
| TCP | Reliable, connection‑oriented | HTTP, SSH |
| UDP | Fast, connectionless | DNS, streaming |
| OSI Model | 7‑layer conceptual model | Layer 3 = Network (IP) |
| TCP/IP Model | 4‑layer real‑world model | Internet layer = IP |
| Switch | Layer 2, uses MAC addresses | – |
| Router | Layer 3, uses IP addresses | – |
| VLAN | Logical segmentation | Separate guest Wi‑Fi |
| NAT | One public IP for many private | Cloud NAT Gateway |
| Load Balancer | Distributes traffic | ALB, NLB |
| Firewall | Filters traffic | Security Group, WAF |
| DNS | Domain → IP | `dig google.com` |
| VPC | Isolated cloud network | `10.0.0.0/16` |
| CDN | Caches content at edge | CloudFront, Cloud CDN |
| WAF | Filters web attacks | AWS WAF |

---

**Date documented:** 2026-06-14  
**Sources:** Networking fundamentals, cloud provider documentation

---
