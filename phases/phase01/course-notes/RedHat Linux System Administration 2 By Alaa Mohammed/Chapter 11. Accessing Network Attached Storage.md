# Chapter 11: Accessing Network Attached Storage – RHCSA Complete Guide

## Table of Contents

- [Chapter 11: Accessing Network Attached Storage – RHCSA Complete Guide](#chapter-11-accessing-network-attached-storage--rhcsa-complete-guide)
  - [Table of Contents](#table-of-contents)
  - [1. NFS Basics](#1-nfs-basics)
    - [1.1 What is NFS?](#11-what-is-nfs)
    - [1.2 NFS Versions (v3, v4)](#12-nfs-versions-v3-v4)
    - [1.3 Exporting NFS Shares (Server Side)](#13-exporting-nfs-shares-server-side)
  - [2. Mounting NFS Shares Manually](#2-mounting-nfs-shares-manually)
  - [3. Persistent Mounts with `/etc/fstab`](#3-persistent-mounts-with-etcfstab)
  - [4. Autofs – On‑Demand Mounting](#4-autofs--ondemand-mounting)
    - [4.1 Why Autofs?](#41-why-autofs)
    - [4.2 Architecture](#42-architecture)
    - [4.3 Indirect Mounts](#43-indirect-mounts)
    - [4.4 Direct Mounts](#44-direct-mounts)
    - [4.5 Managing Autofs Service](#45-managing-autofs-service)
  - [5. Accessing CIFS/SMB Shares](#5-accessing-cifssmb-shares)
    - [5.1 Manual and Persistent Mounts](#51-manual-and-persistent-mounts)
    - [5.2 Using a Credentials File](#52-using-a-credentials-file)
    - [5.3 Autofs for CIFS](#53-autofs-for-cifs)
  - [6. Quick Reference Table](#6-quick-reference-table)
  - [7. Real‑World Scenario – Shared Storage for a Web Server Cluster](#7-realworld-scenario--shared-storage-for-a-web-server-cluster)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [1. On the NFS server (`nas01`)](#1-on-the-nfs-server-nas01)
      - [2. On each web server (`web01`, `web02`)](#2-on-each-web-server-web01-web02)
      - [3. Verify](#3-verify)
  - [8. Practice Lab](#8-practice-lab)
    - [Lab 1: NFS Server and Client Basics](#lab-1-nfs-server-and-client-basics)
    - [Lab 2: Persistent Mount via `/etc/fstab`](#lab-2-persistent-mount-via-etcfstab)
    - [Lab 3: Autofs Indirect Map](#lab-3-autofs-indirect-map)
    - [Lab 4: Autofs Direct Map](#lab-4-autofs-direct-map)
    - [Lab 5: CIFS Mount (if you have a Windows or Samba share)](#lab-5-cifs-mount-if-you-have-a-windows-or-samba-share)

---

## 1. NFS Basics

### 1.1 What is NFS?

NFS (Network File System) allows a client to mount a remote directory over the network and use it as if it were local. It is the standard Linux/Unix file‑sharing protocol.

### 1.2 NFS Versions (v3, v4)

- **NFSv3** – works over UDP or TCP. Relies on client‑side UID/GID mapping (AUTH_SYS). Simple, still used, but being phased out.
- **NFSv4** – TCP only, improved security (Kerberos), stateful, better performance.  
  **RHCSA focus:** Use `vers=4` (or `vers=3`) when mounting.

### 1.3 Exporting NFS Shares (Server Side)

On the NFS server, edit `/etc/exports`:

```
/path/to/share    client(options)
```

**Common export options:**

| Option | Meaning |
|--------|---------|
| `rw` | Read‑write |
| `ro` | Read‑only |
| `sync` | Write to disk before replying (safe) |
| `no_subtree_check` | Disable subtree checking (recommended) |
| `root_squash` | Map root (UID 0) to anonymous `nfsnobody` |

**Example:**
```
/srv/shared  192.168.1.0/24(rw,sync,no_subtree_check)
```

Apply changes:
```bash
sudo exportfs -r
```

Verify exports:
```bash
showmount -e server-ip
```

---

## 2. Mounting NFS Shares Manually

**Command:**
```bash
sudo mount -t nfs server:/export /local/mountpoint
```

**Add options with `-o`:**
```bash
sudo mount -t nfs -o rw,vers=4 192.168.1.200:/srv/shared /mnt/nfs
```

**Common mount options:**

| Option | Meaning |
|--------|---------|
| `vers=4` | Use NFSv4 |
| `rw`/`ro` | Read‑write / read‑only |
| `hard` | Retry indefinitely (default) |
| `soft` | Return error after timeout |
| `noac` | Disable attribute caching (avoids stale data) |

To unmount: `sudo umount /mnt/nfs`

---

## 3. Persistent Mounts with `/etc/fstab`

Add an entry to `/etc/fstab` to mount automatically at boot.

**Format:**
```
server:/export   /mountpoint   nfs   defaults,_netdev,vers=4   0 0
```

- `_netdev` – ensures the network is up before mounting.
- `0 0` – disable dump and fsck (NFS doesn’t need them).

**Example:**
```
192.168.1.200:/srv/shared   /mnt/nfs   nfs   defaults,_netdev,vers=4   0 0
```

Test without rebooting:
```bash
sudo mount -a
```

> **RHCSA tip:** Always verify the mount works, and that it survives a reboot (or at least `mount -a`).

---

## 4. Autofs – On‑Demand Mounting

### 4.1 Why Autofs?

- Mounts shares **only when accessed**.
- Automatically unmounts after idle time.
- Saves system resources and speeds up boot.
- **RHCSA:** Know how to configure indirect and direct maps.

### 4.2 Architecture

```
/etc/auto.master  →  points to map files
  ├── indirect: /parent/dir   /etc/auto.map
  └── direct:   /-            /etc/auto.direct
```

### 4.3 Indirect Mounts

Indirect maps place sub‑directories under a common parent.

**1. Edit `/etc/auto.master`:**
```
/misc   /etc/auto.misc   --timeout=60
```

**2. Create `/etc/auto.misc`:**
```
backup   -fstype=nfs4,rw   192.168.1.200:/srv/backup
logs     -fstype=nfs4,ro   192.168.1.200:/var/log/shared
```

**3. Start autofs:**
```bash
sudo systemctl enable --now autofs
```

**4. Trigger the mount:**
```bash
ls /misc/backup      # this mounts the share
```

After 60 seconds of inactivity, it unmounts automatically.

### 4.4 Direct Mounts

Direct mounts allow absolute mount points anywhere.

**1. Add to `/etc/auto.master`:**
```
/-   /etc/auto.direct
```

**2. Create `/etc/auto.direct`:**
```
/mnt/nfs1   -fstype=nfs4,rw   192.168.1.200:/srv/nfs1
/mnt/nfs2   -fstype=nfs4,ro   192.168.1.200:/srv/nfs2
```

**3. Reload autofs:**
```bash
sudo systemctl reload autofs
```

Access `/mnt/nfs1` to mount it.

### 4.5 Managing Autofs Service

- `systemctl start/stop/enable/reload autofs`
- Global timeout and other options in `/etc/autofs.conf`
- Important: after editing map files, reload with `systemctl reload autofs`

---

## 5. Accessing CIFS/SMB Shares

### 5.1 Manual and Persistent Mounts

Install utilities:
```bash
sudo dnf install cifs-utils
```

**Manual mount:**
```bash
sudo mount -t cifs //server/share /mnt/win -o username=alice,password=secret
```

**For `/etc/fstab`:**
```
//server/share  /mnt/win  cifs  credentials=/etc/samba/cred.txt,uid=1000,gid=1000,_netdev  0 0
```

### 5.2 Using a Credentials File

Create a file with `username` and `password` (mode 600):
```bash
echo "username=alice" > /etc/samba/cred.txt
echo "password=secret" >> /etc/samba/cred.txt
chmod 600 /etc/samba/cred.txt
```

### 5.3 Autofs for CIFS

Indirect map entry (`/etc/auto.cifs`):
```
data   -fstype=cifs,credentials=/etc/samba/cred.txt   ://server/share
```

Master map:
```
/cifs   /etc/auto.cifs
```

---

## 6. Quick Reference Table

| Task | Command / Configuration |
|------|--------------------------|
| Show exports on server | `showmount -e server` |
| Export after editing `/etc/exports` | `sudo exportfs -r` |
| Manual NFS mount | `mount -t nfs -o vers=4 server:/path /local` |
| /etc/fstab NFS entry | `server:/path /local nfs defaults,_netdev,vers=4 0 0` |
| Install autofs | `sudo dnf install autofs` |
| Enable and start autofs | `sudo systemctl enable --now autofs` |
| Reload autofs after map changes | `sudo systemctl reload autofs` |
| Master map file | `/etc/auto.master` |
| Indirect map example | `/misc /etc/auto.misc` |
| Direct map marker | `/- /etc/auto.direct` |
| Indirect map line | `key -fstype=nfs4,rw server:/export` |
| Direct map line | `/absolute -fstype=nfs4,rw server:/export` |
| Autofs global configuration | `/etc/autofs.conf` |
| CIFS manual mount | `mount -t cifs //server/share /local -o username=user` |
| CIFS credentials file | `/etc/samba/cred.txt` (600 permissions) |

---

## 7. Real‑World Scenario – Shared Storage for a Web Server Cluster

### Background

Two web servers (`web01` and `web02`) serve the same PHP application. User‑uploaded files must be stored on a central NFS server so that both web servers see the same content. You need to:

- Export `/srv/uploads` from the NFS server (`nas01`) with read‑write access for both web servers.
- On each web server, mount the share **on‑demand** using autofs under `/var/www/html/uploads`.
- The share must unmount after 5 minutes of inactivity.

### Step‑by‑Step Implementation

#### 1. On the NFS server (`nas01`)

```bash
# Install NFS server
sudo dnf install -y nfs-utils
sudo systemctl enable --now nfs-server rpcbind

# Create shared directory
sudo mkdir -p /srv/uploads
sudo chmod 755 /srv/uploads

# Configure exports
echo "/srv/uploads 192.168.1.0/24(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
sudo exportfs -r
```

#### 2. On each web server (`web01`, `web02`)

```bash
# Install autofs
sudo dnf install -y autofs

# Edit /etc/auto.master
echo "/var/www/html/uploads /etc/auto.uploads --timeout=300" | sudo tee -a /etc/auto.master

# Create the indirect map file
echo "uploads -fstype=nfs4,rw nas01:/srv/uploads" | sudo tee /etc/auto.uploads

# Restart autofs
sudo systemctl restart autofs
```

Now, when any user or application accesses `/var/www/html/uploads`, autofs automatically mounts the NFS share. After 5 minutes of no activity, it unmounts.

#### 3. Verify

```bash
# On web01
ls /var/www/html/uploads
touch /var/www/html/uploads/test.txt

# On web02
ls /var/www/html/uploads   # should show test.txt
```

The shared storage is transparent and requires no `fstab` entries. This setup is exam‑ready and production‑tested.

---

## 8. Practice Lab

### Lab 1: NFS Server and Client Basics

1. On a server VM:
   ```bash
   sudo dnf install -y nfs-utils
   sudo systemctl enable --now nfs-server rpcbind
   sudo mkdir -p /srv/share
   echo "Hello NFS" | sudo tee /srv/share/file.txt
   sudo chmod 755 /srv/share
   echo "/srv/share *(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
   sudo exportfs -r
   ```

2. On a client VM:
   ```bash
   sudo mkdir -p /mnt/nfs
   sudo mount -t nfs -o vers=4 server_ip:/srv/share /mnt/nfs
   ls /mnt/nfs
   sudo umount /mnt/nfs
   ```

### Lab 2: Persistent Mount via `/etc/fstab`

Add to client’s `/etc/fstab`:
```
server_ip:/srv/share  /mnt/nfs  nfs  defaults,_netdev,vers=4  0 0
```
Test with `sudo mount -a`.

### Lab 3: Autofs Indirect Map

1. `sudo dnf install -y autofs`
2. Add to `/etc/auto.master`:
   ```
   /mnt/autofs   /etc/auto.autofs   --timeout=60
   ```
3. Create `/etc/auto.autofs`:
   ```
   share   -fstype=nfs4,rw   server_ip:/srv/share
   ```
4. `sudo systemctl enable --now autofs`
5. `ls /mnt/autofs/share` → triggers mount.
6. Wait 60 seconds, check with `mount | grep /mnt/autofs` (should disappear).

### Lab 4: Autofs Direct Map

1. Add to `/etc/auto.master`:
   ```
   /-   /etc/auto.direct
   ```
2. Create `/etc/auto.direct`:
   ```
   /mnt/directshare   -fstype=nfs4,rw   server_ip:/srv/share
   ```
3. Reload: `sudo systemctl reload autofs`
4. `ls /mnt/directshare` → mounted.

### Lab 5: CIFS Mount (if you have a Windows or Samba share)

1. `sudo dnf install -y cifs-utils`
2. Manual: `sudo mount -t cifs //windows_ip/share /mnt/win -o username=user`
3. Persistent: create credentials file, add to `/etc/fstab`.

---

**Date documented:** 2026-05-11  
**Sources:** Red Hat Enterprise Linux 9 Storage Administration, RHCSA exam objectives, autofs and NFS man pages.