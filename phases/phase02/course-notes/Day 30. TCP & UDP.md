# Day 30. TCP & UDP

## Table of Contents

- [Day 30. TCP \& UDP](#day-30-tcp--udp)
  - [Table of Contents](#table-of-contents)
  - [1. What Are Transport Layer Protocols?](#1-what-are-transport-layer-protocols)
  - [2. TCP – Transmission Control Protocol](#2-tcp--transmission-control-protocol)
    - [2.1 Characteristics of TCP](#21-characteristics-of-tcp)
    - [2.2 TCP Three‑Way Handshake](#22-tcp-threeway-handshake)
    - [2.3 TCP Flags](#23-tcp-flags)
    - [2.4 TCP Sequence and Acknowledgement Numbers](#24-tcp-sequence-and-acknowledgement-numbers)
    - [2.5 TCP Flow Control and Congestion Control](#25-tcp-flow-control-and-congestion-control)
    - [2.6 TCP Ports and Sockets](#26-tcp-ports-and-sockets)
  - [3. UDP – User Datagram Protocol](#3-udp--user-datagram-protocol)
    - [3.1 Characteristics of UDP](#31-characteristics-of-udp)
    - [3.2 UDP Header Format](#32-udp-header-format)
    - [3.3 When to Use UDP](#33-when-to-use-udp)
  - [4. TCP vs. UDP – Comparison Table](#4-tcp-vs-udp--comparison-table)
  - [5. Common Ports for TCP and UDP](#5-common-ports-for-tcp-and-udp)
  - [6. TCP and UDP in Cloud Engineering](#6-tcp-and-udp-in-cloud-engineering)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [8. Practice Lab – Verify Your Understanding](#8-practice-lab--verify-your-understanding)

---

## 1. What Are Transport Layer Protocols?

The **Transport Layer** (Layer 4 of the OSI model, and also Layer 4 of the TCP/IP model) is responsible for **end‑to‑end communication** between applications on different hosts. It provides:

- **Data segmentation** – breaks application data into smaller segments.
- **Port addressing** – identifies the source and destination applications (using port numbers).
- **Error detection** – checks if data is corrupted.
- **Flow control** – manages the rate of data transmission.
- **Multiplexing** – allows multiple applications to send/receive data simultaneously.

The two most important transport layer protocols are **TCP** (Transmission Control Protocol) and **UDP** (User Datagram Protocol). They serve different purposes and are used for different types of applications.

---

## 2. TCP – Transmission Control Protocol

### 2.1 Characteristics of TCP

| Feature | Description |
|---------|-------------|
| **Connection‑oriented** | A connection must be established before data transfer (3‑way handshake). |
| **Reliable** | Guarantees delivery of data – lost packets are retransmitted. |
| **Ordered** | Data arrives in the same order it was sent (sequence numbers). |
| **Flow control** | Prevents sender from overwhelming the receiver (windowing). |
| **Congestion control** | Adjusts transmission rate based on network conditions. |
| **Full‑duplex** | Data can be sent and received simultaneously. |
| **Heavy overhead** | Larger header (20–60 bytes) due to flags, sequence numbers, etc. |

**Use cases:** Web browsing (HTTP/HTTPS), email (SMTP, IMAP), file transfer (FTP), remote access (SSH), databases (MySQL, PostgreSQL).

### 2.2 TCP Three‑Way Handshake

Before sending data, TCP establishes a connection using a **three‑way handshake**:

```
Client                      Server
   |                           |
   |---- SYN (Seq=x) ---------→|
   |                           |
   |←--- SYN-ACK (Seq=y, Ack=x+1) --|
   |                           |
   |---- ACK (Ack=y+1) -------→|
   |                           |
   |    (Data transfer starts) |
```

- **SYN** – synchronise (initiate connection)
- **SYN‑ACK** – acknowledge SYN and send own SYN
- **ACK** – final acknowledgement, connection established

**Why 3 steps?** To ensure both sides are ready and synchronised. It prevents old, duplicate packets from interfering.

### 2.3 TCP Flags

| Flag | Meaning | Function |
|------|---------|----------|
| **SYN** | Synchronise | Initiate connection |
| **ACK** | Acknowledgement | Confirm receipt of data |
| **FIN** | Finish | Gracefully close connection |
| **RST** | Reset | Abort connection immediately |
| **PSH** | Push | Deliver data immediately (no buffering) |
| **URG** | Urgent | Mark urgent data |

### 2.4 TCP Sequence and Acknowledgement Numbers

- **Sequence number** – identifies the position of the first byte of data in the segment.
- **Acknowledgement number** – the next expected byte from the other side (cumulative ACK).

This allows TCP to reassemble data in the correct order and detect lost segments.

### 2.5 TCP Flow Control and Congestion Control

**Flow control** uses a **sliding window** – the receiver advertises a window size (how much data it can buffer). The sender limits its send rate to avoid overflowing the receiver.

**Congestion control** uses algorithms like **TCP Reno**, **CUBIC**, and **BBR** to dynamically adjust the send rate based on detected packet loss and network delays.

**In cloud environments**, congestion control is important for high‑throughput services (e.g., video streaming, large file transfers).

### 2.6 TCP Ports and Sockets

A **socket** is the combination of an IP address and a port number (e.g., `192.168.1.10:443`). Ports identify the specific application or service on a host.

| Port Range | Purpose |
|------------|---------|
| 0–1023 | Well‑known ports (system‑assigned) |
| 1024–49151 | Registered ports (user‑assigned) |
| 49152–65535 | Dynamic / ephemeral ports (client‑side) |

---

## 3. UDP – User Datagram Protocol

### 3.1 Characteristics of UDP

| Feature | Description |
|---------|-------------|
| **Connectionless** | No handshake – data is sent without establishing a connection. |
| **Unreliable** | No guarantee of delivery – packets may be lost, duplicated, or out of order. |
| **No flow control** | Sends data at the rate of the application, regardless of network conditions. |
| **Low overhead** | Simple 8‑byte header – fast and efficient. |
| **Broadcast / Multicast** | Supports sending to multiple recipients. |

**Use cases:** DNS (queries), streaming media (video/audio), VoIP, online gaming, SNMP, DHCP, syslog.

**Why use UDP?** Speed and low latency are more important than reliability. Loss of a few packets in a voice call is acceptable, but delays are not.

### 3.2 UDP Header Format

```
+---------+---------+---------+---------+
|  Source Port (16) |  Dest Port (16)  |
+---------+---------+---------+---------+
|   Length (16)     |  Checksum (16)   |
+---------+---------+---------+---------+
```

- **Source port** – optional (may be 0)
- **Destination port** – required
- **Length** – header + data length (minimum 8 bytes)
- **Checksum** – optional in IPv4, mandatory in IPv6

### 3.3 When to Use UDP

| Scenario | Why UDP |
|----------|---------|
| **DNS** | Queries are small and fast; losing a response is handled at application level (retry). |
| **Video streaming** | Missing a frame is better than delaying the entire stream. |
| **VoIP** | Real‑time voice – small delays cause jitter. |
| **Online gaming** | Fast response time is critical; a lost packet can be re‑requested later. |
| **DHCP** | Broadcast discovery messages; connection overhead is not needed. |

---

## 4. TCP vs. UDP – Comparison Table

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Connection‑oriented (3‑way handshake) | Connectionless |
| **Reliability** | Reliable (acknowledgements, retransmissions) | Unreliable (no guarantees) |
| **Ordering** | Data arrives in order | Data may arrive out of order |
| **Flow control** | Yes (windowing) | No |
| **Congestion control** | Yes | No |
| **Header size** | 20–60 bytes | 8 bytes |
| **Speed** | Slower (overhead) | Very fast |
| **Broadcast/Multicast** | No | Yes |
| **Use cases** | HTTP, HTTPS, SSH, FTP, SMTP, databases | DNS, streaming, VoIP, DHCP, SNMP, gaming |

---

## 5. Common Ports for TCP and UDP

| Port | Protocol | Service | Type |
|------|----------|---------|------|
| 20,21 | FTP | File Transfer | TCP |
| 22 | SSH | Secure Shell | TCP |
| 23 | Telnet | Remote terminal | TCP |
| 25 | SMTP | Email sending | TCP |
| 53 | DNS | Domain Name System | TCP/UDP |
| 67,68 | DHCP | IP assignment | UDP |
| 80 | HTTP | Web | TCP |
| 110 | POP3 | Email retrieval | TCP |
| 123 | NTP | Time synchronisation | UDP |
| 143 | IMAP | Email retrieval | TCP |
| 161 | SNMP | Network management | UDP |
| 443 | HTTPS | Secure Web | TCP |
| 514 | Syslog | System logging | UDP |
| 3306 | MySQL | Database | TCP |
| 5432 | PostgreSQL | Database | TCP |
| 8080 | HTTP‑alt | Web alternative | TCP |

---

## 6. TCP and UDP in Cloud Engineering

| Cloud Service | Transport Protocol | Why |
|---------------|-------------------|-----|
| **AWS ALB (Application Load Balancer)** | TCP (Layer 7) | Routes HTTP/HTTPS traffic (uses TCP). |
| **AWS NLB (Network Load Balancer)** | TCP/UDP (Layer 4) | Handles TCP and UDP traffic (e.g., gaming, streaming). |
| **Security Groups** | TCP/UDP/ICMP | Filter traffic based on protocol and port. |
| **VPC Endpoints** | TCP | Most services (S3, DynamoDB) use TCP. |
| **Route53 (DNS)** | TCP/UDP | DNS uses both (TCP for large responses). |
| **ElastiCache (Redis)** | TCP | Client‑server communication. |
| **IoT Core** | TCP/UDP | Depending on MQTT (TCP) or CoAP (UDP). |

**Debugging TCP issues:**
- `ss -tulpn` – list listening TCP and UDP ports.
- `telnet host port` – test TCP connectivity.
- `nc -vz host port` – test TCP/UDP with netcat.
- `tcpdump -i any port 443` – capture TCP traffic.

**Debugging UDP issues:**
- `tcpdump -i any udp port 53` – capture DNS queries.
- `dig google.com +tcp` – force TCP for DNS (useful for large responses).

---

## 7. Quick Reference Table

| Topic | Summary |
|-------|---------|
| **TCP** | Reliable, ordered, connection‑oriented, heavy overhead. |
| **UDP** | Fast, lightweight, connectionless, no guarantees. |
| **Three‑way handshake** | SYN → SYN‑ACK → ACK (establish TCP connection) |
| **TCP Flags** | SYN, ACK, FIN, RST, PSH, URG |
| **UDP Header** | Source Port, Dest Port, Length, Checksum (8 bytes) |
| **Common TCP ports** | 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL) |
| **Common UDP ports** | 53 (DNS), 67/68 (DHCP), 123 (NTP), 161 (SNMP) |
| **Cloud use (TCP)** | ALB, Security Groups, SSH, web services |
| **Cloud use (UDP)** | NLB, DNS, streaming, gaming |

---

## 8. Practice Lab – Verify Your Understanding

1. **Identify ports and protocols:**
   - Run `ss -tulpn | grep LISTEN` on your Linux machine. Which services are listening? Which protocol are they using?

2. **TCP handshake capture:**
   - Use `tcpdump -i any port 22 -c 10` to capture an SSH connection. Observe the SYN, SYN‑ACK, ACK exchange.

3. **UDP test:**
   - Use `dig google.com` (DNS query over UDP). Capture with `tcpdump -i any udp port 53` and observe the request/response.

4. **Cloud scenario:**
   - You need to host a web application using HTTPS and a gaming server using UDP. Which load balancer would you choose in AWS? (ALB for HTTPS, NLB for UDP.)

5. **Firewall rules:**
   - Write a Security Group rule that allows SSH (TCP 22) from your home IP and HTTP (TCP 80) from anywhere. Which protocol/port would you open?

---

**Date documented:** 2026-06-16  
**Sources:** RFC 793 (TCP), RFC 768 (UDP), cloud provider documentation

---