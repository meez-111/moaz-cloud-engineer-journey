# Days 44–45: NAT (Network Address Translation) – Complete Professional Guide

## Table of Contents

- [Days 44–45: NAT (Network Address Translation) – Complete Professional Guide](#days-4445-nat-network-address-translation--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. The Problem: IPv4 Address Exhaustion](#1-the-problem-ipv4-address-exhaustion)
  - [2. Short‑Term Solutions to IPv4 Exhaustion](#2-shortterm-solutions-to-ipv4-exhaustion)
  - [3. Private IPv4 Address Ranges](#3-private-ipv4-address-ranges)
  - [4. What is NAT?](#4-what-is-nat)
    - [4.1 How NAT Works – Step by Step](#41-how-nat-works--step-by-step)
    - [4.2 NAT Example – Simple Outbound Connection](#42-nat-example--simple-outbound-connection)
  - [5. Why Use NAT?](#5-why-use-nat)
  - [6. Types of NAT](#6-types-of-nat)
    - [6.1 Source NAT vs. Destination NAT](#61-source-nat-vs-destination-nat)
    - [6.2 Static Source NAT (One‑to‑One)](#62-static-source-nat-onetoone)
    - [6.3 Dynamic Source NAT (Pool, One‑to‑One)](#63-dynamic-source-nat-pool-onetoone)
    - [6.4 Dynamic PAT / NAT Overload (Many‑to‑One)](#64-dynamic-pat--nat-overload-manytoone)
  - [7. Real‑World NAT in Cloud Networking](#7-realworld-nat-in-cloud-networking)
    - [7.1 AWS NAT Gateway](#71-aws-nat-gateway)
    - [7.2 AWS Internet Gateway (IGW)](#72-aws-internet-gateway-igw)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Practice Examples](#9-practice-examples)
    - [Example 1: You have 5 public IPs and 50 internal hosts. Which NAT type is best?](#example-1-you-have-5-public-ips-and-50-internal-hosts-which-nat-type-is-best)
    - [Example 2: A web server must be reachable from the internet at `203.0.113.10`. Inside, it has `192.168.1.100`. What NAT configuration is needed?](#example-2-a-web-server-must-be-reachable-from-the-internet-at-203011310-inside-it-has-1921681100-what-nat-configuration-is-needed)
    - [Example 3: AWS NAT Gateway – why does a private subnet need a NAT Gateway to reach the internet?](#example-3-aws-nat-gateway--why-does-a-private-subnet-need-a-nat-gateway-to-reach-the-internet)
    - [Example 4: What happens to a DNS response packet when it returns through a PAT router?](#example-4-what-happens-to-a-dns-response-packet-when-it-returns-through-a-pat-router)

---

## 1. The Problem: IPv4 Address Exhaustion

IPv4 provides approximately **4.3 billion** unique addresses. With the explosion of internet‑connected devices (smartphones, laptops, IoT), this pool has been exhausted.

**Two broad solutions:**
- **Long‑term solution:** Transition to **IPv6** (128‑bit, virtually unlimited addresses).
- **Short‑term solutions** (used today to extend IPv4’s life):
  1. **CIDR** – flexible allocation, replacing rigid classful addressing.
  2. **Private IPv4 addresses** – addresses reserved for internal networks.
  3. **NAT** – allows multiple private devices to share a single public IP.

---

## 2. Short‑Term Solutions to IPv4 Exhaustion

| Solution | Description |
|----------|-------------|
| **CIDR** | Classless Inter‑Domain Routing – enables efficient allocation of IP prefixes, reducing waste. |
| **Private IPv4 addresses** | Reserved address ranges for internal use, not routable on the internet. |
| **NAT** | Translates private IPs to public IPs, allowing many devices to share one public address. |

---

## 3. Private IPv4 Address Ranges

Private addresses are **not globally routable** – they cannot be used directly on the internet. They are intended for internal networks (corporate LANs, home networks, cloud VPCs).

| Class | Private Range | CIDR | Total Addresses |
|-------|---------------|------|-----------------|
| A | 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | 16,777,216 |
| B | 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | 1,048,576 |
| C | 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | 65,536 |

**Why private addresses?**
- They conserve public IPv4 space.
- They provide security – internal devices are not directly exposed to the internet.
- NAT is required for these devices to communicate with the internet.

---

## 4. What is NAT?

**NAT (Network Address Translation)** is a process where a router/firewall modifies the source or destination IP address of a packet as it passes through.

The most common use: allowing hosts with **private IP addresses** to communicate with the internet using a **single public IP address**.

### 4.1 How NAT Works – Step by Step

**Simple outbound connection (PC → Internet)**

1. **PC (private IP)** sends a packet to `8.8.8.8`:
   - Source IP: `192.168.1.10:54321` (private + random port)
   - Destination: `8.8.8.8:53`

2. **NAT router** intercepts the packet:
   - Changes source IP to its **public IP** (e.g., `203.0.113.5`)
   - Changes source port to a **random port** (e.g., `54321` → `50001`)
   - Stores the mapping in a **NAT table**

3. **Internet** sees the packet as coming from `203.0.113.5:50001`.

4. **Response returns** from `8.8.8.8` to `203.0.113.5:50001`.

5. **NAT router** looks up its table, translates back:
   - Destination IP: `203.0.113.5:50001` → `192.168.1.10:54321`
   - Forwards to PC.

**NAT Table example:**

| Inside Local | Inside Global | Outside Global |
|--------------|---------------|----------------|
| 192.168.1.10:54321 | 203.0.113.5:50001 | 8.8.8.8:53 |

### 4.2 NAT Example – Simple Outbound Connection

```
PC (192.168.1.10) → NAT Router (203.0.113.5) → Internet (8.8.8.8)

Step 1: PC sends: SRC=192.168.1.10:54321, DST=8.8.8.8:53
Step 2: NAT changes: SRC=203.0.113.5:50001, DST=8.8.8.8:53
Step 3: Response: SRC=8.8.8.8:53, DST=203.0.113.5:50001
Step 4: NAT reverses: SRC=8.8.8.8:53, DST=192.168.1.10:54321
```

---

## 5. Why Use NAT?

| Reason | Explanation |
|--------|-------------|
| **Conserve public IPs** | One public IP can serve thousands of private hosts. |
| **Security** | Private IPs are hidden from the internet – direct inbound attacks are harder. |
| **Flexibility** | Internal networks can be renumbered without affecting external connectivity. |
| **Load balancing** | NAT can be combined with load balancing to distribute inbound traffic. |

---

## 6. Types of NAT

### 6.1 Source NAT vs. Destination NAT

| Type | Abbreviation | Direction | Purpose |
|------|--------------|-----------|---------|
| **Source NAT** | SNAT | Outbound | Translate private source IP to public IP (allows internal hosts to reach internet). |
| **Destination NAT** | DNAT | Inbound | Translate public destination IP to private IP (allows external hosts to reach internal servers). |

### 6.2 Static Source NAT (One‑to‑One)

- A **fixed mapping** between one private IP and one public IP.
- Each internal device has a dedicated public IP.
- Requires as many public IPs as internal hosts.

**Use case:** A server that must be reachable from the internet with a consistent public IP (e.g., public‑facing web server).

**Example:**
- Private IP: `192.168.1.10` ↔ Public IP: `203.0.113.10`

### 6.3 Dynamic Source NAT (Pool, One‑to‑One)

- A **pool of public IPs** is shared among a larger number of private hosts.
- When a host initiates a session, it gets **one public IP** from the pool (temporarily).
- Still one‑to‑one mapping: each session uses a different public IP.

**Use case:** Organisations with more public IPs than static NAT but fewer than number of hosts.

**Example:**
- Public pool: `203.0.113.10` – `203.0.113.15` (6 IPs)
- 20 internal hosts share this pool – each session gets a unique IP from the pool.

### 6.4 Dynamic PAT / NAT Overload (Many‑to‑One)

**PAT (Port Address Translation)** – also called **NAT Overload**. This is the most common NAT used in home routers and corporate environments.

- Many private hosts **share a single public IP**.
- The router distinguishes sessions by using **different source ports**.
- Thousands of simultaneous sessions can share one IP.

**Why PAT is popular:**
- Conserves public IPs massively.
- Works seamlessly with most applications (HTTP, HTTPS, DNS, etc.).
- Default in home routers and cloud NAT gateways.

**Example:**

| Inside Local | Inside Global | Outside Global |
|--------------|---------------|----------------|
| 192.168.1.10:12345 | 203.0.113.5:50001 | 8.8.8.8:53 |
| 192.168.1.20:12345 | 203.0.113.5:50002 | 8.8.8.8:53 |
| 192.168.1.30:80 | 203.0.113.5:50003 | 93.184.216.34:80 |

Three different hosts all share the same public IP (`203.0.113.5`) but different source ports (`50001`, `50002`, `50003`).

---

## 7. Real‑World NAT in Cloud Networking

### 7.1 AWS NAT Gateway

- Managed service that enables instances in a **private subnet** to connect to the internet (for updates, patches, external APIs).
- Performs **PAT (NAT Overload)** – multiple private instances share the NAT Gateway’s Elastic IP.
- Requires a **public subnet** and an **Internet Gateway** to work.
- **Pricing:** Charged per hour + per GB of data processed.

### 7.2 AWS Internet Gateway (IGW)

- A horizontally scaled, redundant VPC component that allows communication between your VPC and the internet.
- **Not a NAT device** – it simply provides a target for internet‑routable traffic.
- Instances in **public subnets** with public IPs can use the IGW directly.
- Instances in **private subnets** must use a NAT Gateway to reach the internet via the IGW.

**Cloud NAT vs. Traditional NAT:**
- In traditional networking, NAT is often a router/firewall function.
- In cloud, NAT is a **managed service** – you don't configure NAT tables manually; you attach the service to a subnet.

---

## 8. Quick Reference Table

| NAT Type | Mapping | Port Translation? | Public IP Usage | Use Case |
|----------|---------|-------------------|-----------------|----------|
| **Static NAT** | 1 private ↔ 1 public | No | One IP per host | Public servers, consistent IPs |
| **Dynamic NAT** | Pool of private ↔ pool of public | No | One IP per session (dynamically assigned) | Organisations with multiple public IPs |
| **PAT (NAT Overload)** | Many private ↔ 1 public | Yes | One IP for all hosts | Home routers, corporate gateways, cloud NAT |
| **Destination NAT** | Public IP ↔ Private IP (inbound) | Optional | One public IP per service | Port forwarding, load balancers |

---

## 9. Practice Examples

### Example 1: You have 5 public IPs and 50 internal hosts. Which NAT type is best?

- Static NAT: not possible (only 5 public IPs for 50 hosts).
- Dynamic NAT: possible – 5 hosts can be online at once; others wait.
- PAT (Overload): best – all 50 hosts share one of the public IPs using different ports.

### Example 2: A web server must be reachable from the internet at `203.0.113.10`. Inside, it has `192.168.1.100`. What NAT configuration is needed?

- **Destination NAT (DNAT) / Port Forwarding:** Incoming traffic to `203.0.113.10:80` is translated to `192.168.1.100:80`.
- Outbound traffic from the server may also need SNAT (if it initiates connections).

### Example 3: AWS NAT Gateway – why does a private subnet need a NAT Gateway to reach the internet?

- Private subnets have **no route to the Internet Gateway** (no public IPs, no direct internet access).
- A NAT Gateway sits in a public subnet, translates private IPs to its own public IP, and forwards traffic through the Internet Gateway.

### Example 4: What happens to a DNS response packet when it returns through a PAT router?

- The DNS response is addressed to the router’s public IP and the source port used for the request.
- The router looks up its NAT table, finds the original private IP and port, changes the destination back, and forwards to the internal host.

---

**Date documented:** 2026-06-16  
**Sources:** Networking fundamentals, RFC 1918 (Private Addresses), cloud provider documentation (AWS NAT Gateway)

---
