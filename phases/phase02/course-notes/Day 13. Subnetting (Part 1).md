# Days 13–15: Subnetting

## Table of Contents

- [Days 13–15: Subnetting](#days-1315-subnetting)
  - [Table of Contents](#table-of-contents)
  - [1. IPv4 Address Classes (Classful Addressing)](#1-ipv4-address-classes-classful-addressing)
  - [2. The Problem: Wasted IP Addresses](#2-the-problem-wasted-ip-addresses)
  - [3. CIDR (Classless Inter‑Domain Routing)](#3-cidr-classless-interdomain-routing)
    - [3.1 What is CIDR?](#31-what-is-cidr)
    - [3.2 CIDR Notation](#32-cidr-notation)
    - [3.3 How to Use CIDR – Examples](#33-how-to-use-cidr--examples)
  - [4. Variable Length Subnet Masking (VLSM)](#4-variable-length-subnet-masking-vlsm)
    - [4.1 What is VLSM?](#41-what-is-vlsm)
    - [4.2 How VLSM Works (Step‑by‑Step)](#42-how-vlsm-works-stepbystep)
    - [4.3 VLSM Example – Office Network](#43-vlsm-example--office-network)
    - [4.4 VLSM vs. FLSM (Fixed Length Subnet Mask)](#44-vlsm-vs-flsm-fixed-length-subnet-mask)
  - [5. Calculating CIDR for a Specific Number of Hosts](#5-calculating-cidr-for-a-specific-number-of-hosts)
    - [5.1 Formula for Number of Hosts](#51-formula-for-number-of-hosts)
    - [5.2 Example: Two Hosts – The /31 Subnet](#52-example-two-hosts--the-31-subnet)
    - [5.3 Example: Single Host – The /32 Subnet](#53-example-single-host--the-32-subnet)
  - [6. Calculating the Number of Subnets](#6-calculating-the-number-of-subnets)
  - [7. Real‑World Subnetting – What Engineers Actually Do](#7-realworld-subnetting--what-engineers-actually-do)
    - [7.1 Scenario 1: Designing a VPC in AWS](#71-scenario-1-designing-a-vpc-in-aws)
    - [7.2 Scenario 2: On‑Premises Corporate Network](#72-scenario-2-onpremises-corporate-network)
    - [7.3 Scenario 3: Troubleshooting with CIDR](#73-scenario-3-troubleshooting-with-cidr)
  - [8. Quick Reference Table (CIDR to Hosts)](#8-quick-reference-table-cidr-to-hosts)
  - [9. Practice Examples (with Solutions)](#9-practice-examples-with-solutions)
    - [Example 1: You need 120 usable IP addresses. Which CIDR should you use?](#example-1-you-need-120-usable-ip-addresses-which-cidr-should-you-use)
    - [Example 2: A company has `172.16.0.0/16`. They want to create subnets with exactly 500 usable addresses each. Find the CIDR and number of subnets.](#example-2-a-company-has-172160016-they-want-to-create-subnets-with-exactly-500-usable-addresses-each-find-the-cidr-and-number-of-subnets)
    - [Example 3: Design a VLSM plan for `192.168.10.0/24` with:](#example-3-design-a-vlsm-plan-for-19216810024-with)
    - [Example 4: A VPC CIDR is `10.0.0.0/16`. If you create a subnet `10.0.0.0/24`, can you also create `10.0.0.128/25`?](#example-4-a-vpc-cidr-is-1000016-if-you-create-a-subnet-1000024-can-you-also-create-100012825)

---

## 1. IPv4 Address Classes (Classful Addressing)

In the early days of the internet, IP addresses were allocated using **fixed classes** based on the first few bits of the address. This is called **classful addressing**.

| Class | Leading Bits | First Octet Range | Default Subnet Mask | Intended Use |
|-------|--------------|-------------------|---------------------|---------------|
| A | `0` | 1–126 | /8 (255.0.0.0) | Very large networks |
| B | `10` | 128–191 | /16 (255.255.0.0) | Medium networks |
| C | `110` | 192–223 | /24 (255.255.255.0) | Small networks |
| D | `1110` | 224–239 | (none – multicast) | Multicast groups |
| E | `1111` | 240–255 | (reserved) | Experimental / reserved |

**Important reserved addresses:**
- **Class A, 127.x.x.x** – Loopback (localhost, `127.0.0.1`)
- **Class D** – Multicast (not used for standard host addressing)
- **Class E** – Reserved for research

**Example classful addresses:**
- `10.0.0.0` – Class A (16 million+ hosts)
- `172.16.0.0` – Class B (65,536 hosts)
- `192.168.1.0` – Class C (254 hosts)

---

## 2. The Problem: Wasted IP Addresses

Fixed classes were **inflexible**. A company needing 300 IP addresses had to take a full Class B (/16) block, wasting over 65,000 addresses. Class C (/24) provided only 254 addresses – too small.

This led to rapid **IPv4 address exhaustion**. The solution was **CIDR** (Classless Inter‑Domain Routing), introduced in 1993.

---

## 3. CIDR (Classless Inter‑Domain Routing)

### 3.1 What is CIDR?

CIDR removes the rigid class boundaries. Instead of fixed /8, /16, or /24 masks, you can use **any prefix length** (e.g., /23, /27, /29). This allows networks to be sized precisely for the number of required hosts, minimising waste.

CIDR also introduced the notation `IP_address/prefix_length`.

### 3.2 CIDR Notation

- Prefix length = number of **network bits** (the bits that are fixed for the entire subnet).
- The remaining bits are **host bits**.

Example: `192.168.1.0/24` means the first 24 bits are network, last 8 bits are host.

### 3.3 How to Use CIDR – Examples

| CIDR | Subnet Mask | Number of Hosts (usable) | Example Use |
|------|-------------|--------------------------|-------------|
| /24 | 255.255.255.0 | 254 | Small office LAN |
| /25 | 255.255.255.128 | 126 | Dividing a /24 into two subnets |
| /26 | 255.255.255.192 | 62 | Further subdivision |
| /27 | 255.255.255.224 | 30 | Small workgroup |
| /28 | 255.255.255.240 | 14 | Very small network |
| /29 | 255.255.255.248 | 6 | Point‑to‑point or tiny LAN |
| /30 | 255.255.255.252 | 2 | Classic point‑to‑point link |
| /31 | 255.255.255.254 | 2 (no broadcast) | Modern point‑to‑point (RFC 3021) |
| /32 | 255.255.255.255 | 1 | Single host (loopback, tunnel) |

**Example calculation for /27:**
- Network bits = 27, host bits = 32 - 27 = 5
- Total addresses = 2^5 = 32
- Usable hosts = 32 - 2 (network and broadcast) = 30

---

## 4. Variable Length Subnet Masking (VLSM)

### 4.1 What is VLSM?

**VLSM** allows you to use **different subnet masks** within the same major network (e.g., the same Class A, B, or C range). Instead of forcing every subnet to have the same size (Fixed Length Subnet Mask – FLSM), VLSM lets you allocate subnets of varying sizes based on actual host requirements.

**Why VLSM?**  
- **Efficiency:** Reduce wasted IP addresses.  
- **Flexibility:** Assign a /30 to a point‑to‑point link and a /24 to a large LAN within the same `10.0.0.0/8` network.  
- **Standard practice:** VLSM is used in all modern networks (e.g., OSPF, EIGRP, BGP, cloud VPCs).

### 4.2 How VLSM Works (Step‑by‑Step)

1. **List subnet requirements** (largest to smallest number of hosts).  
2. **Determine the CIDR for each subnet** using the formula `2^(32 - prefix) - 2 ≥ required hosts`.  
3. **Allocate subnets from largest to smallest** without overlapping.

### 4.3 VLSM Example – Office Network

You are given: `192.168.1.0/24` (256 total addresses).  
You need four subnets with:
- Subnet A: 100 hosts  
- Subnet B: 50 hosts  
- Subnet C: 20 hosts  
- Subnet D: 2 hosts (point‑to‑point)

**Step 1 – Find CIDR for each:**
- 100 hosts → need 7 host bits (2^7 = 128, minus 2 = 126) → /25  
- 50 hosts → need 6 host bits (2^6 = 64, minus 2 = 62) → /26  
- 20 hosts → need 5 host bits (2^5 = 32, minus 2 = 30) → /27  
- 2 hosts → /30 (or /31 if RFC 3021 supported)

**Step 2 – Allocate largest to smallest:**

| Subnet | Required CIDR | Subnet Address | Usable Range | Broadcast |
|--------|---------------|----------------|--------------|-----------|
| A (/25) | /25 | 192.168.1.0/25 | 192.168.1.1 – 192.168.1.126 | 192.168.1.127 |
| B (/26) | /26 | 192.168.1.128/26 | 192.168.1.129 – 192.168.1.190 | 192.168.1.191 |
| C (/27) | /27 | 192.168.1.192/27 | 192.168.1.193 – 192.168.1.222 | 192.168.1.223 |
| D (/30) | /30 | 192.168.1.224/30 | 192.168.1.225 – 192.168.1.226 | 192.168.1.227 |

No overlap – all subnets fit inside the original /24.

### 4.4 VLSM vs. FLSM (Fixed Length Subnet Mask)

| Feature | FLSM | VLSM |
|---------|------|------|
| Subnet masks | All subnets use same mask | Masks can vary per subnet |
| Address waste | High (e.g., /24 for a 2‑host link) | Minimal (use /30 or /31) |
| Routing protocol support | All | Requires classless protocols (OSPF, EIGRP, BGP, RIP‑2) |
| Cloud usage | Not used | Default in VPCs (you choose CIDR per subnet) |

---

## 5. Calculating CIDR for a Specific Number of Hosts

### 5.1 Formula for Number of Hosts

```
Usable hosts = 2^(32 - prefix_length) - 2
```

To find the smallest CIDR that accommodates `N` hosts:

1. Find the smallest integer `h` (host bits) such that `2^h - 2 ≥ N`.
2. Then `prefix_length = 32 - h`.

### 5.2 Example: Two Hosts – The /31 Subnet

Classic point‑to‑point links (e.g., two routers connected directly) need exactly two IP addresses. A /30 gives 2 usable addresses but wastes 2 addresses (network and broadcast). For **point‑to‑point**, RFC 3021 allows the use of `/31` subnets, which have **no network or broadcast addresses**:

- `/31` mask: `255.255.255.254`
- Total addresses: `2^1 = 2`
- Usable addresses: both (no subtraction)
- This is only valid for point‑to‑point links where broadcasts are not needed.

**Example:** Two routers can use `10.0.0.0/31` and `10.0.0.1/31`.

### 5.3 Example: Single Host – The /32 Subnet

A `/32` mask (`255.255.255.255`) defines exactly one IP address. It is commonly used for:
- Loopback interfaces (e.g., `127.0.0.1/32`)
- VPN tunnel endpoints
- AWS VPC route table entries for a single network interface

**Note:** A /32 has no network or broadcast addresses – it’s simply a host route.

---

## 6. Calculating the Number of Subnets

When you borrow bits from the host portion to create subnets:

```
Number of subnets = 2^(borrowed_bits)
```

**Borrowed bits** = new prefix length − original classful prefix length.

**Example:** Starting with a Class C /24 network (e.g., `192.168.1.0/24`). If you use a /27 subnet mask:

- Borrowed bits = 27 − 24 = 3
- Number of subnets = 2^3 = 8 subnets
- Each /27 subnet has 32 addresses (30 usable).

**Visual for /24 → /27:**

```
192.168.1.0/27
192.168.1.32/27
192.168.1.64/27
...
192.168.1.224/27
```

---

## 7. Real‑World Subnetting – What Engineers Actually Do

### 7.1 Scenario 1: Designing a VPC in AWS

A cloud engineer needs to create a VPC with CIDR `10.0.0.0/16` (65,536 total addresses). They must define subnets across three Availability Zones (AZs) for a web application:

- Public subnets: For load balancers, bastion hosts (each needs at least 256 addresses).
- Private subnets: For application servers (each needs 1024 addresses).
- Database subnets: For managed database instances (each needs 64 addresses).

**Real implementation:**

| AZ | Public Subnet CIDR | Private Subnet CIDR | DB Subnet CIDR |
|----|--------------------|---------------------|----------------|
| AZ1 | 10.0.1.0/24 (254) | 10.0.2.0/22 (1022) | 10.0.0.0/26 (62) |
| AZ2 | 10.0.4.0/24 | 10.0.8.0/22 | 10.0.0.64/26 |
| AZ3 | 10.0.5.0/24 | 10.0.12.0/22 | 10.0.0.128/26 |

**Why these CIDRs?**  
- Public subnets only need enough for load balancers and NAT gateways – /24 is plenty.
- Private subnets need more room for auto‑scaling app servers – /22 gives 1022 addresses.
- Database subnets are small – /26 is sufficient.

The engineer uses **VLSM** to efficiently pack the VPC address space, leaving room for future expansion.

### 7.2 Scenario 2: On‑Premises Corporate Network

A company has `10.0.0.0/8` (16 million addresses). They need to allocate subnets to different departments:

| Department | Required Hosts | CIDR chosen | Subnet range |
|------------|---------------|-------------|---------------|
| Engineering | 3000 | /20 (4094 hosts) | 10.0.16.0/20 |
| Marketing | 500 | /23 (510 hosts) | 10.0.32.0/23 |
| HR | 100 | /25 (126 hosts) | 10.0.48.0/25 |
| Finance | 200 | /24 (254 hosts) | 10.0.49.0/24 |
| Guest Wi‑Fi | 1000 | /22 (1022 hosts) | 10.0.64.0/22 |

**Total allocated:** ~10,000 addresses – a tiny fraction of the /8. The rest is reserved for future growth.

**Real‑world trick:** Always leave at least 25‑50% free space in your address plan for unexpected growth.

### 7.3 Scenario 3: Troubleshooting with CIDR

A network admin sees a firewall log: `Denied: src=192.168.50.15, dest=10.0.0.5`. The firewall rule allows only `10.0.0.0/24` to talk to `192.168.1.0/24`. Why is the packet denied?

- Destination `10.0.0.5` is inside `10.0.0.0/24` – OK.
- Source `192.168.50.15` is **not** inside `192.168.1.0/24`.  
  The admin realises they misconfigured the source CIDR – it should be `192.168.50.0/24`. After correction, traffic flows.

**Takeaway:** Understanding CIDR is essential for debugging firewall rules, routing tables, and security groups.

---

## 8. Quick Reference Table (CIDR to Hosts)

| CIDR | Subnet Mask | Total Addresses | Usable Hosts |
|------|-------------|----------------|--------------|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |
| /31 | 255.255.255.254 | 2 | 2 (no broadcast) |
| /32 | 255.255.255.255 | 1 | 1 |

---

## 9. Practice Examples (with Solutions)

### Example 1: You need 120 usable IP addresses. Which CIDR should you use?

- /24 gives 254 → overkill.
- /25 gives 126 → exactly fits.
- Answer: `/25`

### Example 2: A company has `172.16.0.0/16`. They want to create subnets with exactly 500 usable addresses each. Find the CIDR and number of subnets.

- 500 usable → need host bits `h` such that `2^h - 2 ≥ 500` → `2^9 = 512`, `512 - 2 = 510` → `h = 9`.
- Prefix length = 32 − 9 = /23.
- Original network /16, new prefix /23 → borrowed bits = 23 − 16 = 7.
- Number of subnets = 2^7 = 128 subnets.
- Each /23 subnet has 512 total addresses (510 usable).

### Example 3: Design a VLSM plan for `192.168.10.0/24` with:
- Subnet 1: 60 hosts  
- Subnet 2: 30 hosts  
- Subnet 3: 10 hosts  
- Subnet 4: 2 hosts (router‑to‑router)

**Solution:**
- Largest (60) → need /26 (62 usable) → allocate `192.168.10.0/26`
- Next (30) → need /27 (30 usable) → `192.168.10.64/27`
- Next (10) → need /28 (14 usable) → `192.168.10.96/28`
- Point‑to‑point (2) → /30 → `192.168.10.112/30`

Check: all subnets fit inside the /24 without overlap.

### Example 4: A VPC CIDR is `10.0.0.0/16`. If you create a subnet `10.0.0.0/24`, can you also create `10.0.0.128/25`?

- `10.0.0.0/24` uses 0‑255.
- `10.0.0.128/25` uses 128‑255 (overlaps).
- Not allowed – subnets cannot overlap in a VPC.
- The second must be `10.0.1.0/25` or another non‑overlapping block.

---

**Date documented:** 2026-06-15  
**Sources:** Networking fundamentals, CIDR (RFC 4632), VLSM, cloud provider documentation

---