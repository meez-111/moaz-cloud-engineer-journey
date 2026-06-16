# Day 39. DHCP

## Table of Contents

- [Day 39. DHCP](#day-39-dhcp)
  - [Table of Contents](#table-of-contents)
  - [1. What is DHCP?](#1-what-is-dhcp)
  - [2. Why Do We Need DHCP?](#2-why-do-we-need-dhcp)
  - [3. DHCP Components](#3-dhcp-components)
    - [3.1 DHCP Server](#31-dhcp-server)
    - [3.2 DHCP Client](#32-dhcp-client)
    - [3.3 DHCP Relay Agent](#33-dhcp-relay-agent)
  - [4. DHCP Operation – The DORA Process](#4-dhcp-operation--the-dora-process)
    - [4.1 DISCOVER (Client → Server)](#41-discover-client--server)
    - [4.2 OFFER (Server → Client)](#42-offer-server--client)
    - [4.3 REQUEST (Client → Server)](#43-request-client--server)
    - [4.4 ACKNOWLEDGE (Server → Client)](#44-acknowledge-server--client)
  - [5. DHCP Lease Process](#5-dhcp-lease-process)
    - [5.1 Lease Timeline](#51-lease-timeline)
    - [5.2 Renewal (T1)](#52-renewal-t1)
    - [5.3 Rebinding (T2)](#53-rebinding-t2)
    - [5.4 Lease Release (Optional)](#54-lease-release-optional)
  - [6. DHCP Options](#6-dhcp-options)
    - [6.1 Common DHCP Options](#61-common-dhcp-options)
    - [6.2 Custom Options](#62-custom-options)
  - [7. DHCP in Cloud Engineering](#7-dhcp-in-cloud-engineering)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Practice Lab – Verify Your Understanding](#9-practice-lab--verify-your-understanding)

---

## 1. What is DHCP?

**DHCP (Dynamic Host Configuration Protocol)** is a network protocol that automatically assigns IP addresses and other network configuration parameters to devices on a network.

**Analogy:** DHCP is like a hotel reception desk. When you check in, they assign you a room number (IP address), tell you the Wi‑Fi password (gateway), and give you a key (lease). When you check out, the room becomes available for the next guest.

**Key point:** DHCP eliminates the need to manually configure IP addresses, subnet masks, default gateways, and DNS servers on every device. It also prevents IP address conflicts.

---

## 2. Why Do We Need DHCP?

| Benefit | Explanation |
|---------|-------------|
| **Automation** | No need to manually assign IPs to every device. |
| **Centralised management** | All IP configuration is managed from a single server. |
| **Prevents conflicts** | Ensures each device gets a unique IP address. |
| **Efficient reuse** | IP addresses are leased and returned, reducing waste. |
| **Mobility support** | Laptops, phones, and tablets automatically get network settings when they connect. |

**Alternative:** **Static IP** – manually assigned, never changes. Used for servers, routers, printers that need a fixed address.

**Cloud note:** Most cloud instances use DHCP (or a cloud‑specific equivalent) to receive their private IPs. Public IPs are assigned separately (Elastic IPs, etc.).

---

## 3. DHCP Components

### 3.1 DHCP Server

- The server that assigns IP addresses and configuration parameters.
- Maintains a **pool of available IP addresses** (scope).
- Responds to DHCP requests from clients.

**Software examples:**
- **ISC DHCP** – open‑source, most common on Linux.
- **dnsmasq** – lightweight DHCP + DNS server.
- **Windows DHCP Server** – built into Windows Server.
- **Cisco IOS** – embedded in routers.

### 3.2 DHCP Client

- Any device that requests and uses DHCP settings (PC, laptop, phone, IoT device).
- Sends DHCP broadcasts to find a server.
- Renews its lease before it expires.

### 3.3 DHCP Relay Agent

- Forwards DHCP broadcasts from a subnet to a DHCP server in another subnet.
- Used when the DHCP server is not on the same broadcast domain as the clients.

**Why needed:** DHCP uses **broadcast** messages, which do not cross routers. A relay agent converts the broadcast to a unicast and forwards it to the DHCP server.

---

## 4. DHCP Operation – The DORA Process

The DHCP process consists of four steps, abbreviated as **DORA**:

```
Client                    DHCP Server
   |                           |
   |---- DISCOVER (broadcast) -→|   "I need an IP address"
   |                           |
   |←--- OFFER (unicast) ------|   "Here is an IP address 10.0.0.100"
   |                           |
   |---- REQUEST (broadcast) -→|   "I accept 10.0.0.100"
   |                           |
   |←--- ACKNOWLEDGE (unicast)-|   "You can use 10.0.0.100 for 24 hours"
   |                           |
   |    (IP configuration complete)  |
```

### 4.1 DISCOVER (Client → Server)

- Client broadcasts a DHCPDISCOVER message (to `255.255.255.255`).
- Source IP: `0.0.0.0` (no IP yet).
- Destination port: `67` (UDP – DHCP server).
- The client asks: "Is there a DHCP server available?"

### 4.2 OFFER (Server → Client)

- DHCP server(s) send a DHCPOFFER message (unicast or broadcast).
- Contains:
  - Offered IP address
  - Subnet mask
  - Lease duration
  - Options (default gateway, DNS, etc.)
- Server reserves the IP address for the client (temporarily).

### 4.3 REQUEST (Client → Server)

- Client broadcasts a DHCPREQUEST message (to `255.255.255.255`).
- Requests the offered IP address.
- This step also informs any other servers that the client has accepted an offer.

### 4.4 ACKNOWLEDGE (Server → Client)

- Server sends a DHCPACK message (unicast).
- Confirms the IP assignment.
- Client can now use the IP address.

**Note:** If the DHCP server cannot accept the request (e.g., IP already taken), it sends a **DHCPNAK**. The client then starts the DORA process again.

---

## 5. DHCP Lease Process

A **lease** is the duration for which an IP address is assigned to a client. The client must renew the lease before it expires.

### 5.1 Lease Timeline

```
    0%                   50%                    87.5%           100%
    │                     │                       │               │
    │                     │                       │               │
    ▼                     ▼                       ▼               ▼
[Lease assigned]     [T1 – Renewal]         [T2 – Rebinding]  [Expiry]
```

- **T1 (50%)** – Client tries to **renew** the lease with the original DHCP server.
- **T2 (87.5%)** – If renewal fails, client tries to **rebind** with any DHCP server.
- **Expiry (100%)** – If no server responds, the IP address is released.

### 5.2 Renewal (T1)

- At 50% of the lease time, the client sends a **unicast** DHCPREQUEST to the original DHCP server.
- The server can respond with:
  - **DHCPACK** – lease extended.
  - **DHCPNAK** – lease not granted (client must request new IP).

### 5.3 Rebinding (T2)

- At 87.5% of the lease time, if the original server hasn't responded, the client switches to **broadcast** DHCPREQUEST.
- Any DHCP server can respond with a DHCPACK.
- This allows the client to get an IP even if the original server is down.

### 5.4 Lease Release (Optional)

- Client can release the IP address early by sending a **DHCPRELEASE** message.
- This frees the IP for other clients (useful for mobile devices).

**Example lease timeline:**
- Lease time: 24 hours (86400 seconds)
- T1 = 12 hours – client renews.
- T2 = 21 hours – if no response, rebind with any server.
- 24 hours – lease expires if no response.

---

## 6. DHCP Options

DHCP options provide additional configuration beyond the IP address. They are sent as part of the OFFER and ACK messages.

### 6.1 Common DHCP Options

| Option Number | Name | Description |
|---------------|------|-------------|
| 1 | Subnet Mask | The subnet mask for the client. |
| 3 | Router (Default Gateway) | The default gateway IP. |
| 6 | DNS Servers | Primary and secondary DNS servers. |
| 15 | Domain Name | The domain name (e.g., `example.com`). |
| 51 | Lease Time | Duration of the lease. |
| 54 | Server Identifier | IP of the DHCP server (for renewal). |
| 66 | TFTP Server Name | Boot server for network boot (PXE). |
| 67 | Bootfile Name | File name for network boot. |
| 121 | Classless Static Routes | CIDR‑based static routes. |

### 6.2 Custom Options

- DHCP servers allow custom options (e.g., for VoIP phones, printers, or proprietary applications).
- Uses option code ranges: **128–254** (user‑defined).

**Example – ISC DHCP server configuration:**

```
subnet 10.0.0.0 netmask 255.255.255.0 {
    range 10.0.0.10 10.0.0.250;
    option routers 10.0.0.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "example.com";
    default-lease-time 86400;
    max-lease-time 172800;
}
```

---

## 7. DHCP in Cloud Engineering

**Public cloud providers (AWS, Azure, GCP) handle DHCP behind the scenes – you rarely interact with it directly.**

| Cloud Provider | DHCP Equivalent |
|----------------|-----------------|
| **AWS** | VPC automatically assigns private IPs via its internal DHCP service. You cannot configure it. |
| **Azure** | VNet provides DHCP for VMs. You can set a static IP via the Azure portal/CLI. |
| **GCP** | VPC network automatically assigns IPs. You can reserve static internal IPs. |

**When DHCP still matters in cloud engineering:**

| Scenario | Why |
|----------|-----|
| **Hybrid cloud** | On‑premises DHCP servers may need to assign IPs to cloud resources via VPN/Direct Connect. |
| **On‑premises migration** | You may need to replicate DHCP scopes to the cloud. |
| **Bare metal / colocation** | If you run physical servers, you'll need DHCP. |
| **Virtualisation (VMware, OpenStack)** | You can configure DHCP on virtual networks. |
| **Troubleshooting** | If an EC2 instance fails to get an IP, you check DHCP logs (which are usually opaque – you rely on the cloud console). |

**Cloud static IPs:**
- AWS **Elastic IPs** – static public IPs, assigned separately.
- Azure **Public IP Address** – static public IPs.
- GCP **Static External IPs** – reserved public IPs.

---

## 8. Quick Reference Table

| Topic | Summary |
|-------|---------|
| **DHCP** | Dynamically assigns IP addresses and network config. |
| **DORA** | DISCOVER → OFFER → REQUEST → ACKNOWLEDGE. |
| **Ports** | UDP 67 (server), UDP 68 (client). |
| **Lease** | Time an IP is assigned to a client. |
| **T1** | 50% of lease – renewal with original server. |
| **T2** | 87.5% of lease – rebinding with any server. |
| **Common options** | Subnet mask (1), Router (3), DNS (6), Domain (15). |
| **Cloud DHCP** | Handled internally by VPC/VNet – not configurable. |
| **Static IPs** | Used for servers, managed via cloud console. |

---

## 9. Practice Lab – Verify Your Understanding

1. **Check your current DHCP lease:**
   - On Linux: `cat /var/lib/dhclient/dhclient.leases` (or `dhcpd.leases`).
   - On Windows: `ipconfig /all` (look for `Lease Obtained` and `Lease Expires`).

2. **DORA simulation:**
   - On your Linux machine, release your DHCP lease: `sudo dhclient -r`.
   - Renew: `sudo dhclient -v`.
   - Watch the DORA exchange in the output.

3. **DHCP options:**
   - On your Linux machine, run `nmap --script broadcast-dhcp-discover` to see what DHCP options are offered.

4. **DHCP server (if you have a lab):**
   - Install `isc-dhcp-server` (or `dnsmasq`), configure a scope, and test with a client.

5. **Cloud scenario:**
   - In AWS, you launch an EC2 instance in a VPC. The instance gets a private IP automatically. Where is the DHCP server? (It's internal – you don't see it.)

6. **Static vs. dynamic:**
   - In a cloud environment, when would you use a static private IP (AWS allows you to assign a static internal IP via ENI)? (For database servers, critical services, or when you need a consistent IP for security groups.)

---

**Date documented:** 2026-06-16  
**Sources:** RFC 2131 (DHCP), ISC DHCP documentation, AWS VPC documentation

---