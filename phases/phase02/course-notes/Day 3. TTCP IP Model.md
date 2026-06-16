# Day 3. TCP/IP Model

## Table of Contents

- [Day 3. TCP/IP Model](#day-3-tcpip-model)
  - [Table of Contents](#table-of-contents)
  - [1. What is the TCP/IP Model?](#1-what-is-the-tcpip-model)
  - [2. The Four Layers of TCP/IP](#2-the-four-layers-of-tcpip)
    - [2.1 Layer 4: Application Layer](#21-layer-4-application-layer)
    - [2.2 Layer 3: Transport Layer](#22-layer-3-transport-layer)
    - [2.3 Layer 2: Internet Layer](#23-layer-2-internet-layer)
    - [2.4 Layer 1: Network Access Layer](#24-layer-1-network-access-layer)
  - [3. TCP/IP vs. OSI Model](#3-tcpip-vs-osi-model)
  - [4. Data Encapsulation – How Data Travels](#4-data-encapsulation--how-data-travels)
  - [5. TCP/IP in Cloud Engineering](#5-tcpip-in-cloud-engineering)
  - [6. Quick Reference Table](#6-quick-reference-table)
  - [7. Practice Lab – Verify Your Understanding](#7-practice-lab--verify-your-understanding)

---

## 1. What is the TCP/IP Model?

The **TCP/IP model** (Transmission Control Protocol/Internet Protocol) is a **practical, simplified framework** for understanding how data travels across networks. It was developed by the U.S. Department of Defense (DARPA) in the 1970s and is the foundation of the modern internet.

**Why TCP/IP matters for cloud engineers:**
- Every cloud service (AWS, Azure, GCP) runs on TCP/IP.
- Debugging connectivity issues (e.g., EC2 instances not communicating) requires understanding which layer is failing.
- Load balancers, firewalls, and VPCs operate at specific TCP/IP layers.

**Key principle:** The TCP/IP model is the **real‑world implementation**; the OSI model is the **conceptual reference**. The internet actually runs on TCP/IP.

---

## 2. The Four Layers of TCP/IP

| Layer | Name | Function | Protocols / Technologies |
|-------|------|----------|--------------------------|
| 4 | **Application** | User interaction, application‑level protocols | HTTP, HTTPS, FTP, SSH, DNS, SMTP |
| 3 | **Transport** | End‑to‑end communication, reliability, flow control | TCP, UDP |
| 2 | **Internet** | Addressing, routing, packet forwarding | IP (IPv4, IPv6), ICMP, ARP |
| 1 | **Network Access** | Physical transmission, framing, MAC addressing | Ethernet, Wi‑Fi, PPP, ATM |

---

### 2.1 Layer 4: Application Layer

**Role:** Provides protocols that applications use to communicate. This is where user‑facing services live.

**Key protocols:**

| Protocol | Port | Purpose |
|----------|------|---------|
| HTTP | 80 | Web browsing (unencrypted) |
| HTTPS | 443 | Secure web browsing |
| SSH | 22 | Secure remote shell |
| DNS | 53 | Domain name resolution |
| SMTP | 25 | Email sending |
| FTP | 20,21 | File transfer |

**Cloud relevance:**
- Security Groups (AWS) and Network Security Groups (Azure) allow/deny traffic based on Application Layer protocols (e.g., allow HTTP/HTTPS, deny SSH from the internet).
- Load balancers (e.g., AWS ALB) operate at Layer 7 – they can route based on HTTP headers, paths, hostnames.

**Example:** When you visit `https://aws.amazon.com`, your browser uses **HTTPS** (Application Layer) to request the web page.

---

### 2.2 Layer 3: Transport Layer

**Role:** Provides **end‑to‑end communication** between applications on different hosts. It ensures data is delivered correctly, in order, and without errors.

**Two main protocols:**

| Protocol | Characteristics | Use Case |
|----------|-----------------|----------|
| **TCP** | Connection‑oriented, reliable, ordered, flow control | HTTP, HTTPS, SSH, FTP, email |
| **UDP** | Connectionless, fast, no guarantee of delivery | DNS, streaming, VoIP, gaming |

**TCP Three‑Way Handshake (Establishing a Connection):**

```
Client                    Server
  |                         |
  |---- SYN (Seq=x) -------→|
  |                         |
  |←--- SYN-ACK (Seq=y, Ack=x+1) --|
  |                         |
  |---- ACK (Ack=y+1) -----→|
  |                         |
  |    (Data transfer)      |
```

**TCP Flags (in TCP headers):**
- **SYN** – synchronise (start connection)
- **ACK** – acknowledgement (confirm receipt)
- **FIN** – finish (close connection gracefully)
- **RST** – reset (abort connection)
- **PSH** – push (deliver data immediately)
- **URG** – urgent (priority data)

**Cloud relevance:**
- **TCP** is used for reliable services: web servers, databases, SSH.
- **UDP** is used for DNS, streaming media, and real‑time applications.
- Security groups (AWS) filter by protocol (TCP/UDP/ICMP) and port.

---

### 2.3 Layer 2: Internet Layer

**Role:** Handles **addressing** and **routing** of packets across networks. This is where **IP addresses** are used.

**Key protocols:**

| Protocol | Function |
|----------|----------|
| **IPv4** | 32‑bit addressing (e.g., 192.168.1.10) |
| **IPv6** | 128‑bit addressing (future‑proof) |
| **ICMP** | Diagnostic (ping, traceroute) |
| **ARP** | Resolves IP to MAC address (within a subnet) |

**Routing:** The Internet Layer decides **how** to forward a packet from source to destination across multiple routers. It uses **routing tables** and protocols like BGP, OSPF, and RIP (though you rarely manage these directly in the cloud).

**Cloud relevance:**
- **VPC CIDR** – you define the IP range for your cloud network.
- **Subnets** – divide your VPC into smaller networks (works at Layer 2/3).
- **Route Tables** – control where traffic is directed within the VPC and to the internet.

**Example:** When an EC2 instance sends traffic to `8.8.8.8`, the Internet Layer adds the source IP (`10.0.1.10`) and destination IP (`8.8.8.8`) to the packet.

---

### 2.4 Layer 1: Network Access Layer

**Role:** Handles the **physical transmission** of data over the network medium (cables, Wi‑Fi, fibre). It includes framing, MAC addressing, and error detection.

**Key components:**
- **Ethernet** – most common LAN technology.
- **Wi‑Fi** – wireless networks.
- **MAC addresses** – 48‑bit unique hardware addresses (e.g., `00:11:22:33:44:55`).

**Cloud relevance:**
- In cloud environments, you don't manage physical switches, cables, or MAC addresses directly.
- However, understanding the Network Access Layer helps when troubleshooting:
  - **MTU (Maximum Transmission Unit)** – if packets are too large, they may be dropped.
  - **VLANs** – cloud providers use virtualised Layer 2 networks under the hood.

**Example:** A packet being sent from an EC2 instance to an S3 bucket travels through the cloud provider's physical infrastructure – all at the Network Access Layer.

---

## 3. TCP/IP vs. OSI Model

| OSI Layer | OSI Name | TCP/IP Layer | Notes |
|-----------|----------|--------------|-------|
| 7 | Application | Application | Combined in TCP/IP |
| 6 | Presentation | Application | Encryption, encoding, compression |
| 5 | Session | Application | Session management, NetBIOS |
| 4 | Transport | Transport | TCP, UDP |
| 3 | Network | Internet | IP, ICMP, routing |
| 2 | Data Link | Network Access | MAC addressing, Ethernet |
| 1 | Physical | Network Access | Cables, signalling |

**Key takeaway:** The OSI model is **conceptual** – used for teaching and troubleshooting. The TCP/IP model is **implementation** – what the internet actually uses.

**Troubleshooting with the TCP/IP model:**
- **Application Layer** – is the service running? (e.g., `systemctl status nginx`)
- **Transport Layer** – is the port open? (`ss -tulpn | grep 443`)
- **Internet Layer** – can the host reach the destination? (`ping`, `traceroute`)
- **Network Access Layer** – is the cable plugged in? (physical issues)

---

## 4. Data Encapsulation – How Data Travels

When an application sends data, it is **encapsulated** (wrapped) with headers at each layer.

```
+----------------------------------------------------------------+
|  Application Data (e.g., HTTP request)                         |
+----------------------------------------------------------------+
| TCP Header (Src/Dst Port, Seq, Ack, Flags) | Application Data |  ← Transport
+----------------------------------------------------------------+
| IP Header (Src IP, Dst IP, TTL) | TCP Header | Application Data |  ← Internet
+----------------------------------------------------------------+
| Ethernet Header (Src/Dst MAC) | IP Header | TCP Header | Data |  ← Network Access
+----------------------------------------------------------------+
| Physical Bits on the Wire                                       |
+----------------------------------------------------------------+
```

**Encapsulation terms:**
- **Data** – Application Layer (original message)
- **Segment** – Transport Layer (TCP/UDP header + data)
- **Packet** – Internet Layer (IP header + segment)
- **Frame** – Network Access Layer (Ethernet header + packet)

---

## 5. TCP/IP in Cloud Engineering

| TCP/IP Layer | Cloud Equivalent | Why It Matters |
|--------------|------------------|----------------|
| **Application** | Security Groups (allow HTTP/HTTPS), ALB (Layer 7 routing) | Control which applications can be accessed |
| **Transport** | Network ACLs (stateless rules), NLB (Layer 4 load balancing) | Control traffic based on ports/protocols |
| **Internet** | VPC, Subnets, Route Tables, NAT Gateway | Define network topology and routing |
| **Network Access** | VPC (virtualised Ethernet), Elastic Network Interfaces | Underlying infrastructure – rarely managed directly |

**Common cloud scenarios:**
1. **Web application:** Users connect via HTTPS (Layer 7). The load balancer (ALB) terminates TLS and forwards to EC2 instances (Layer 4/7).
2. **Database access:** Application connects to RDS using TCP (Layer 4) over port 5432 (PostgreSQL).
3. **VPC peering:** Traffic between VPCs uses the Internet Layer (routing) to determine path.

---

## 6. Quick Reference Table

| Layer | TCP/IP Name | Key Protocols | Key Concepts | Cloud Equivalent |
|-------|-------------|---------------|--------------|------------------|
| 4 | Application | HTTP, HTTPS, SSH, DNS, SMTP | User‑facing services, ports | Security Groups, ALB |
| 3 | Transport | TCP, UDP | Reliability, ports, handshake | Network ACLs, NLB |
| 2 | Internet | IP, ICMP, ARP | Addressing, routing, TTL | VPC, Subnets, Route Tables |
| 1 | Network Access | Ethernet, Wi‑Fi, PPP | MAC, physical transmission | ENI, Virtual switches |

---

## 7. Practice Lab – Verify Your Understanding

1. **Identify layers in `curl`:**
   - Run `curl -v https://example.com`. List the TCP/IP layers involved:
     - Application: HTTPS (Layer 4)
     - Transport: TCP (Layer 3)
     - Internet: IP (Layer 2)
     - Network Access: Ethernet (Layer 1)

2. **Analyse a packet capture:**
   - Using `tcpdump -i any -n -c 5`, capture 5 packets. Identify the source IP, destination IP, source port, destination port, and protocol (TCP/UDP).

3. **Port and protocol filtering:**
   - In AWS, create a Security Group allowing TCP port 22 only from a specific IP. Explain which layers this affects (Transport + Internet).

4. **Three‑way handshake:**
   - Use `tcpdump` to capture a SSH connection (`ssh localhost`). Observe the SYN, SYN‑ACK, ACK exchange.

5. **VPC design:**
   - Draw a simple VPC with a public subnet and a private subnet. Label which TCP/IP layers are involved at each step:
     - Internet Gateway → Route Table → Subnet → EC2 instance.

---

**Date documented:** 2026-06-16  
**Sources:** Networking fundamentals, RFC 791 (IP), RFC 793 (TCP), cloud provider documentation

---
