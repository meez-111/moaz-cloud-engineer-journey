# Day 38. DNS (Domain Name System)

## Table of Contents

- [Day 38. DNS (Domain Name System)](#day-38-dns-domain-name-system)
  - [Table of Contents](#table-of-contents)
  - [1. What is DNS? Why Do We Need It?](#1-what-is-dns-why-do-we-need-it)
  - [2. DNS Hierarchy – The Distributed Database](#2-dns-hierarchy--the-distributed-database)
    - [2.1 Root DNS Servers](#21-root-dns-servers)
    - [2.2 TLD (Top‑Level Domain) Servers](#22-tld-toplevel-domain-servers)
    - [2.3 Authoritative DNS Servers](#23-authoritative-dns-servers)
    - [2.4 Recursive Resolvers](#24-recursive-resolvers)
  - [3. DNS Resolution Process – Step by Step](#3-dns-resolution-process--step-by-step)
  - [4. DNS Record Types](#4-dns-record-types)
    - [4.1 A and AAAA Records](#41-a-and-aaaa-records)
    - [4.2 CNAME (Canonical Name)](#42-cname-canonical-name)
    - [4.3 MX (Mail Exchange)](#43-mx-mail-exchange)
    - [4.4 TXT (Text)](#44-txt-text)
    - [4.5 NS (Name Server)](#45-ns-name-server)
    - [4.6 SOA (Start of Authority)](#46-soa-start-of-authority)
    - [4.7 PTR (Pointer – Reverse DNS)](#47-ptr-pointer--reverse-dns)
    - [4.8 SRV (Service)](#48-srv-service)
  - [5. DNS Caching – TTL and Propagation](#5-dns-caching--ttl-and-propagation)
  - [6. DNS Tools – `dig`, `nslookup`, `host`](#6-dns-tools--dig-nslookup-host)
    - [6.1 `dig` – Domain Information Groper](#61-dig--domain-information-groper)
    - [6.2 `nslookup` – Name Server Lookup](#62-nslookup--name-server-lookup)
    - [6.3 `host` – Simple Lookup](#63-host--simple-lookup)
  - [7. DNS in Cloud Engineering](#7-dns-in-cloud-engineering)
    - [7.1 AWS Route 53](#71-aws-route-53)
    - [7.2 Azure DNS](#72-azure-dns)
    - [7.3 Google Cloud DNS](#73-google-cloud-dns)
  - [8. Common DNS Troubleshooting](#8-common-dns-troubleshooting)
  - [9. Quick Reference Table](#9-quick-reference-table)
  - [10. Practice Lab – Verify Your Understanding](#10-practice-lab--verify-your-understanding)

---

## 1. What is DNS? Why Do We Need It?

**DNS (Domain Name System)** translates human‑readable domain names (e.g., `www.google.com`) into machine‑readable IP addresses (e.g., `142.250.185.46`).

**Analogy:** DNS is like a phonebook for the internet. You know the person's name (domain), but you need their phone number (IP address) to call them.

**Why DNS matters:**
- Humans remember names, not numbers.
- IP addresses change (e.g., cloud instances get new IPs on restart). DNS abstracts this.
- Load balancing – DNS can return different IPs for the same domain (round‑robin, geo‑routing).
- Cloud services (S3, ELB, CloudFront) rely heavily on DNS.

**Key point:** DNS is a **distributed, hierarchical** database – no single server holds all DNS records.

---

## 2. DNS Hierarchy – The Distributed Database

```
                      ┌─────────────┐
                      │   Root      │  (13 root server clusters worldwide)
                      │   Servers   │
                      └─────────────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   TLD       │  (.com, .org, .net, .uk, .sa, etc.)
                      │   Servers   │
                      └─────────────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   Authoritative │  (e.g., ns1.example.com)
                      │   Servers   │
                      └─────────────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   Recursive │  (ISP or public resolver like 8.8.8.8)
                      │   Resolver  │
                      └─────────────┘
```

### 2.1 Root DNS Servers

- The top of the hierarchy – 13 logical root server clusters (letters A through M).
- They don't know the IP of `example.com` – they point to the **TLD servers** for `.com`.

### 2.2 TLD (Top‑Level Domain) Servers

- Responsible for a specific TLD (e.g., `.com`, `.org`, `.uk`, `.sa`).
- Store the addresses of the **authoritative name servers** for domains under that TLD.

### 2.3 Authoritative DNS Servers

- The "source of truth" for a specific domain (e.g., `example.com`).
- Store all DNS records for that domain (A, CNAME, MX, TXT, etc.).
- Managed by domain registrars, hosting providers, or cloud providers (Route 53).

### 2.4 Recursive Resolvers

- Act on behalf of the client – they query the hierarchy and return the final answer.
- Usually provided by ISPs or public services (e.g., Google Public DNS `8.8.8.8`, Cloudflare `1.1.1.1`).
- They **cache** responses to speed up future queries.

---

## 3. DNS Resolution Process – Step by Step

**Example:** User types `www.example.com` into a browser.

```
Step 1: Client asks Recursive Resolver (e.g., 8.8.8.8)
        "What is the IP of www.example.com?"

Step 2: Recursive Resolver queries Root DNS Server
        "Where do I find the .com TLD servers?"
        Root responds with a list of .com TLD servers.

Step 3: Recursive Resolver queries a .com TLD Server
        "Where do I find the authoritative servers for example.com?"
        TLD responds with ns1.example.com and ns2.example.com.

Step 4: Recursive Resolver queries an Authoritative Server (ns1.example.com)
        "What is the IP of www.example.com?"
        Authoritative server returns: 192.0.2.10

Step 5: Recursive Resolver returns 192.0.2.10 to the client.

Step 6: Client connects to 192.0.2.10 (the web server).
```

**Why this is efficient:**
- The Recursive Resolver caches the TLD and Authoritative NS info.
- Subsequent queries for `example.com` (or even `mail.example.com`) are faster.

---

## 4. DNS Record Types

| Record Type | Purpose | Example |
|-------------|---------|---------|
| **A** | IPv4 address | `www.example.com. A 192.0.2.10` |
| **AAAA** | IPv6 address | `www.example.com. AAAA 2001:db8::1` |
| **CNAME** | Canonical name (alias) | `blog.example.com. CNAME example.com.` |
| **MX** | Mail exchange (email routing) | `example.com. MX 10 mail.example.com.` |
| **TXT** | Text (SPF, DKIM, verification) | `example.com. TXT "v=spf1 include:..."` |
| **NS** | Name servers for the domain | `example.com. NS ns1.example.com.` |
| **SOA** | Start of Authority (administrative info) | `example.com. SOA ns1.example.com. admin.example.com. ...` |
| **PTR** | Reverse DNS (IP → hostname) | `10.2.0.192.in-addr.arpa. PTR www.example.com.` |
| **SRV** | Service location | `_sip._tcp.example.com. SRV 10 5 5060 sipserver.example.com.` |

### 4.1 A and AAAA Records

- **A** – points a domain to an IPv4 address.
- **AAAA** – points a domain to an IPv6 address.

**Example:**
```
example.com.   A   192.0.2.10
example.com.   AAAA 2001:db8::1
```

### 4.2 CNAME (Canonical Name)

- Creates an alias: `www.example.com` points to `example.com` (or another domain).
- **Important:** A CNAME cannot be present with other record types (e.g., MX) at the same label.

**Example:**
```
www.example.com. CNAME example.com.
```

### 4.3 MX (Mail Exchange)

- Directs email to the correct mail server.
- Includes a **priority** (lower number = higher priority).

**Example:**
```
example.com. MX 10 mail1.example.com.
example.com. MX 20 mail2.example.com.
```

### 4.4 TXT (Text)

- Used for:
  - **SPF** (Sender Policy Framework) – which servers can send email for the domain.
  - **DKIM** (DomainKeys Identified Mail) – email signing.
  - **Domain verification** (e.g., for Google Workspace, AWS Certificate Manager).

**Example:**
```
example.com. TXT "v=spf1 include:_spf.google.com ~all"
```

### 4.5 NS (Name Server)

- Identifies which DNS servers are authoritative for the domain.

**Example:**
```
example.com. NS ns1.awsdns-01.com.
example.com. NS ns2.awsdns-02.com.
```

### 4.6 SOA (Start of Authority)

- Contains administrative information for the zone:
  - Primary NS (master server)
  - Email address of the administrator
  - Serial number (incremented on changes)
  - Refresh, retry, expire timers

**Example:**
```
example.com. SOA ns1.example.com. admin.example.com. 2026061601 3600 1800 604800 3600
```

### 4.7 PTR (Pointer – Reverse DNS)

- Maps an IP address back to a hostname (reverse lookup).
- Used for SMTP (email) and logging.

**Example:**
```
10.2.0.192.in-addr.arpa. PTR www.example.com.
```

### 4.8 SRV (Service)

- Used for specific services (e.g., VoIP, SIP, LDAP).
- Contains priority, weight, port, and target.

**Example:**
```
_sip._tcp.example.com. SRV 10 5 5060 sipserver.example.com.
```

---

## 5. DNS Caching – TTL and Propagation

**TTL (Time to Live)** – the amount of time (in seconds) a DNS record can be cached by resolvers.

- Short TTL (e.g., 60 seconds) – changes propagate quickly, but query load increases.
- Long TTL (e.g., 86400 seconds = 24 hours) – lower load, but changes are slow to propagate.

**Propagation** – the time it takes for a DNS change to be visible globally. It depends on:

- The TTL of the old record.
- How long each recursive resolver caches the old value.
- In practice, changes can take minutes to hours.

**Cloud best practice:** Before making a critical change (e.g., migrating a web server), lower the TTL to 60 seconds a day in advance, make the change, and then raise the TTL back.

---

## 6. DNS Tools – `dig`, `nslookup`, `host`

### 6.1 `dig` – Domain Information Groper

`dig` is the most powerful and widely used DNS diagnostic tool.

**Syntax:** `dig [options] domain [record_type]`

| Option / Example | Description |
|------------------|-------------|
| `dig google.com` | Basic A record lookup. |
| `dig google.com AAAA` | Lookup IPv6 address. |
| `dig google.com MX` | Lookup mail servers. |
| `dig google.com +short` | Show only the IP address. |
| `dig @8.8.8.8 google.com` | Query a specific resolver. |
| `dig -x 8.8.8.8` | Reverse DNS (PTR record). |
| `dig +trace google.com` | Show the full resolution path (root → TLD → authoritative). |

**Example output:**
```bash
$ dig google.com +short
142.250.185.46
```

### 6.2 `nslookup` – Name Server Lookup

`nslookup` is an older tool but still useful for interactive queries.

**Usage:**
```bash
nslookup google.com
nslookup 8.8.8.8
nslookup -type=MX google.com
```

### 6.3 `host` – Simple Lookup

`host` is a lightweight alternative (simpler output).

**Usage:**
```bash
host google.com
host -t MX google.com
host 8.8.8.8
```

---

## 7. DNS in Cloud Engineering

### 7.1 AWS Route 53

**Route 53** is AWS's DNS service.

- **Features:**
  - Register and manage domains.
  - Create **hosted zones** (public or private).
  - **Record sets** – define A, CNAME, MX, TXT, etc.
  - **Alias records** – point to AWS resources (ALB, CloudFront, S3) without extra charges.
  - **Routing policies:**
    - Simple (single IP)
    - Weighted (traffic distribution)
    - Latency (route to lowest latency region)
    - Geolocation (route based on user's country)
    - Failover (active‑passive)
    - Multivalue answer (multiple IPs)

- **Health checks** – monitor endpoints and automatically route traffic away from unhealthy targets.

### 7.2 Azure DNS

- **Azure DNS** – host domains and create record sets.
- **Private DNS zones** – for internal VNet resolution.
- **Traffic Manager** – global load balancing (DNS‑based).

### 7.3 Google Cloud DNS

- **Cloud DNS** – managed DNS service.
- Supports public and private zones.
- **DNSSEC** support for signing records.

**Cloud DNS best practices:**
- Use **Alias/A‑Alias** records for cloud resources (AWS Route 53 alias, Azure CNAME with A‑record).
- Implement **TTL management** for critical changes.
- Monitor DNS query logs for security (e.g., AWS Route 53 query logging).

---

## 8. Common DNS Troubleshooting

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **DNS resolution fails** | `ping google.com` returns `unknown host` | Check `/etc/resolv.conf`, ensure DNS server is reachable, try `dig @8.8.8.8 google.com`. |
| **Propagation delay** | New record not visible | Check TTL of old record; use `dig +trace` to see current authoritative answer. |
| **Wrong IP returned** | Site points to old server | Flush local cache (`ipconfig /flushdns`, `sudo systemd-resolve --flush-caches`). |
| **CNAME conflict** | MX or SOA records missing | Cannot have CNAME with other record types at the same label. Use A record instead. |
| **DNSSEC validation failure** | `dig +dnssec` shows errors | Check key rollover, ensure resolver supports DNSSEC. |

---

## 9. Quick Reference Table

| Topic | Summary |
|-------|---------|
| **DNS** | Translates domain names to IP addresses. |
| **Root servers** | 13 clusters – point to TLD servers. |
| **TLD servers** | Manage `.com`, `.org`, etc. |
| **Authoritative servers** | Source of truth for a domain. |
| **Recursive resolver** | Queries on behalf of client (e.g., 8.8.8.8). |
| **A record** | IPv4 address. |
| **AAAA** | IPv6 address. |
| **CNAME** | Alias to another domain. |
| **MX** | Mail server priority. |
| **TXT** | SPF, DKIM, verification. |
| **TTL** | Time to Live (caching duration). |
| **dig** | Primary DNS troubleshooting tool. |
| **AWS Route 53** | Managed DNS with advanced routing. |

---

## 10. Practice Lab – Verify Your Understanding

1. **Basic DNS lookup:**
   - Use `dig google.com +short` to find the IPv4 address of `google.com`.
   - Use `dig google.com AAAA +short` to find the IPv6 address.

2. **Mail server lookup:**
   - Find the MX records for `gmail.com` (or your own domain).
   - Identify the priority values.

3. **Reverse DNS:**
   - Use `dig -x 8.8.8.8` to find the PTR record for Google's public DNS.

4. **DNS trace:**
   - Run `dig +trace google.com`. Observe the root → .com → google.com path.

5. **Cloud scenario:**
   - You are migrating a web application from `10.0.1.10` to `10.0.1.20` in AWS. The DNS TTL is set to 3600 seconds. How long before users see the new IP? What can you do to speed it up? (Lower the TTL to 60 seconds before the change.)

6. **Azure/GCP equivalent:**
   - In AWS Route 53, you want to route traffic to the nearest region for a global application. Which routing policy would you use? (Latency‑based routing.)

---

**Date documented:** 2026-06-16  
**Sources:** RFC 1034 (DNS), AWS Route 53 documentation, `dig` manual

---