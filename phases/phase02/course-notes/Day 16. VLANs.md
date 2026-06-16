# Day 16. VLANs (Virtual LANs)

## Table of Contents

- [Day 16. VLANs (Virtual LANs)](#day-16-vlans-virtual-lans)
  - [Table of Contents](#table-of-contents)
  - [1. What is a VLAN?](#1-what-is-a-vlan)
  - [2. Why Use VLANs?](#2-why-use-vlans)
  - [3. How VLANs Work](#3-how-vlans-work)
    - [3.1 VLAN Tagging (802.1Q)](#31-vlan-tagging-8021q)
    - [3.2 VLAN Trunking](#32-vlan-trunking)
    - [3.3 Access Ports vs. Trunk Ports](#33-access-ports-vs-trunk-ports)
  - [4. VLAN Types](#4-vlan-types)
    - [4.1 Default VLAN (VLAN 1)](#41-default-vlan-vlan-1)
    - [4.2 Data VLAN](#42-data-vlan)
    - [4.3 Voice VLAN](#43-voice-vlan)
    - [4.4 Management VLAN](#44-management-vlan)
    - [4.5 Native VLAN](#45-native-vlan)
  - [5. VLAN Configuration Basics (Cisco / Linux)](#5-vlan-configuration-basics-cisco--linux)
    - [Cisco CLI Example:](#cisco-cli-example)
    - [Linux / `ip` command (for VLAN interfaces on a Linux host):](#linux--ip-command-for-vlan-interfaces-on-a-linux-host)
  - [6. VLANs in Cloud Engineering](#6-vlans-in-cloud-engineering)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [8. Practice Lab – Verify Your Understanding](#8-practice-lab--verify-your-understanding)

---

## 1. What is a VLAN?

A **VLAN (Virtual Local Area Network)** is a **logical** subdivision of a physical network. It allows you to group devices together **regardless of their physical location** – they can be on different switches, in different buildings, or even in different cities.

**Analogy:** Imagine a large office building. Physically, everyone is in the same building. But VLANs are like assigning people to different floors or departments – they can communicate freely within their floor, but need a router to talk to other floors.

**Key point:** VLANs operate at **Layer 2 (Data Link)** of the OSI model. They segment broadcast domains – traffic within a VLAN stays within that VLAN.

---

## 2. Why Use VLANs?

| Benefit | Explanation |
|---------|-------------|
| **Security** | Devices in different VLANs cannot communicate directly – they need a router/firewall. This isolates sensitive systems (e.g., HR, finance). |
| **Performance** | Reduces broadcast traffic – broadcasts are contained within the VLAN, not sent to the entire network. |
| **Flexibility** | Users can be moved to a different VLAN without changing physical cabling – just reconfigure the switch port. |
| **Cost savings** | Instead of buying separate physical switches for each department, you use one switch with multiple VLANs. |
| **Simplified management** | VLANs can group devices by function (e.g., all VoIP phones in one VLAN, all servers in another) rather than by physical location. |

**Example:** A company with 500 employees across 3 floors. Instead of physically cabling each floor to a separate switch, they use VLANs to segment:
- VLAN 10: Finance (floor 1 + 2)
- VLAN 20: Engineering (floor 2 + 3)
- VLAN 30: HR (floor 1 + 3)
- VLAN 40: Guest Wi‑Fi (isolated from internal network)

---

## 3. How VLANs Work

### 3.1 VLAN Tagging (802.1Q)

When a frame travels across a trunk link (between switches), it needs to be identified as belonging to a specific VLAN. **802.1Q** is the IEEE standard that adds a **VLAN tag** (4 bytes) to the Ethernet frame.

**Tag fields:**
- **TPID (Tag Protocol Identifier)** – `0x8100` – indicates 802.1Q tagging.
- **TCI (Tag Control Information)** – 16 bits:
  - **Priority Code Point (PCP)** – 3 bits (QoS)
  - **Drop Eligible Indicator (DEI)** – 1 bit
  - **VLAN ID (VID)** – 12 bits (allows up to 4096 VLANs: 1–4094)

**What the tag looks like:**

```
+-----------+-----------+-----------+-----------+-----------+-----------+
| DA (6)    | SA (6)    | 802.1Q    | VLAN ID  | Type (2)  | Data      |
|           |           | Tag (4)   | (12 bits) |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
```

### 3.2 VLAN Trunking

A **trunk** is a link that carries traffic for **multiple VLANs** between switches (or between a switch and a router/firewall). The trunk adds 802.1Q tags to frames so the receiving device knows which VLAN each frame belongs to.

**Without trunking:** Each VLAN would need a separate physical cable – impractical for many VLANs.
**With trunking:** One cable carries all VLAN traffic, with tags distinguishing them.

### 3.3 Access Ports vs. Trunk Ports

| Port Type | Function | Tagging |
|-----------|----------|---------|
| **Access Port** | Connects to an end device (PC, printer, server). The device belongs to a single VLAN. | No tag – frames are untagged (the switch adds the VLAN ID internally). |
| **Trunk Port** | Connects to another switch, router, or firewall. Carries multiple VLANs. | 802.1Q tags are added to each frame. |

**Note:** The **Native VLAN** on a trunk is untagged – frames from the native VLAN are sent without a tag. This is important for backward compatibility.

---

## 4. VLAN Types

### 4.1 Default VLAN (VLAN 1)

- All switch ports belong to VLAN 1 by default.
- VLAN 1 carries management traffic (CDP, VTP, etc.) by default.
- **Security best practice:** Do not use VLAN 1 for user traffic – move management to a separate VLAN.

### 4.2 Data VLAN

- Carries **user data** (PCs, printers, servers).
- Typically assigned to end devices.

### 4.3 Voice VLAN

- Dedicated VLAN for VoIP (Voice over IP) phones.
- QoS (Quality of Service) is often applied to prioritise voice traffic.
- Phones automatically receive an IP address from a DHCP server on the voice VLAN.

### 4.4 Management VLAN

- Used for **network management** (SSH, SNMP, syslog).
- Separates management traffic from user data – improves security.
- The VLAN IP address is usually the switch's management IP.

### 4.5 Native VLAN

- The VLAN that carries **untagged** traffic on a trunk.
- By default, VLAN 1 is the native VLAN.
- **Security best practice:** Change the native VLAN to an unused VLAN (e.g., VLAN 999) to prevent VLAN hopping attacks.

---

## 5. VLAN Configuration Basics (Cisco / Linux)

### Cisco CLI Example:

```cisco
! Create VLANs
vlan 10
 name Finance
vlan 20
 name Engineering

! Assign port to VLAN (Access Port)
interface fa0/1
 switchport mode access
 switchport access vlan 10

! Configure Trunk Port
interface gi0/1
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30
```

### Linux / `ip` command (for VLAN interfaces on a Linux host):

```bash
# Create VLAN 10 on interface eth0
ip link add link eth0 name eth0.10 type vlan id 10
ip link set eth0.10 up
ip addr add 192.168.10.10/24 dev eth0.10
```

---

## 6. VLANs in Cloud Engineering

**VLANs are not directly used in public cloud (AWS, Azure, GCP)** – they are replaced by **VPCs** and **subnets**.

| Traditional Networking | Cloud Equivalent |
|------------------------|------------------|
| VLAN | Subnet (within a VPC) |
| Trunk | VPC peering / Transit Gateway |
| Access Port | Security Group (controls traffic to/from instance) |
| Native VLAN | (not applicable) |

**Why VLANs are still relevant for cloud engineers:**
- **Hybrid cloud:** On‑premises networks still use VLANs. Connecting on‑prem to cloud (via Direct Connect / VPN) requires understanding VLANs.
- **Network troubleshooting:** If you work with on‑prem servers or network appliances, VLANs are common.
- **Managed hosting:** Some colocation providers still use VLANs for tenant isolation.
- **Edge / local cloud:** Tools like OpenStack, OpenShift, and VMware use VLANs for network segmentation.

**But for pure cloud (AWS, Azure, GCP):** You will rarely (if ever) configure a VLAN directly.

---

## 7. Quick Reference Table

| Term | Description |
|------|-------------|
| **VLAN** | Logical segmentation of a physical network. |
| **802.1Q** | IEEE standard for VLAN tagging. |
| **VLAN ID** | 12‑bit identifier (1–4094). |
| **Access Port** | Port assigned to a single VLAN (untagged). |
| **Trunk Port** | Port that carries multiple VLANs (tagged). |
| **Native VLAN** | VLAN that carries untagged traffic on a trunk. |
| **VLAN Hopping** | Attack where an attacker tries to access another VLAN. |
| **VTP** | Cisco VLAN Trunking Protocol – automatically propagates VLANs across switches. |

---

## 8. Practice Lab – Verify Your Understanding

1. **VLAN planning:**
   - You have 100 users in Finance, 200 in Engineering, and 50 in HR. Design a VLAN scheme:
     - VLAN 10: Finance (100 users)
     - VLAN 20: Engineering (200 users)
     - VLAN 30: HR (50 users)
     - What subnet mask would you use for each?

2. **Trunking question:**
   - Two switches are connected via a trunk. Why is it important to set the same native VLAN on both ends?

3. **Security:**
   - Why should you change the native VLAN from VLAN 1 to an unused VLAN?

4. **Cloud context:**
   - In AWS, you create a VPC with CIDR `10.0.0.0/16`. You need three subnets: public, private, and database. How would you map this to VLAN concepts?

5. **Linux VLAN interface:**
   - On a Linux machine with `eth0`, create VLAN 100 with IP `192.168.100.10/24`. Verify with `ip a`.

---

**Date documented:** 2026-06-16  
**Sources:** IEEE 802.1Q, Cisco CCNA, Linux networking

---