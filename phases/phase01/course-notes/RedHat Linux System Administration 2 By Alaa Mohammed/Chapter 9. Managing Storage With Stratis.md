# Chapter 9: Managing Storage With Stratis

## Table of Contents

- [Chapter 9: Managing Storage With Stratis](#chapter-9-managing-storage-with-stratis)
  - [Table of Contents](#table-of-contents)
  - [1. What is Stratis?](#1-what-is-stratis)
  - [2. Core Concepts of Stratis](#2-core-concepts-of-stratis)
  - [3. LVM Overview (For Comparison)](#3-lvm-overview-for-comparison)
  - [4. Detailed Comparison – LVM vs Stratis](#4-detailed-comparison--lvm-vs-stratis)
  - [5. When to Use LVM](#5-when-to-use-lvm)
  - [6. When to Use Stratis](#6-when-to-use-stratis)
  - [7. Installation and Basic Management](#7-installation-and-basic-management)
    - [7.1 Install Stratis](#71-install-stratis)
    - [7.2 Start and enable the daemon](#72-start-and-enable-the-daemon)
    - [7.3 Creating a Storage Pool](#73-creating-a-storage-pool)
    - [7.4 Creating a Filesystem in the Pool](#74-creating-a-filesystem-in-the-pool)
    - [7.5 Mounting a Stratis Filesystem](#75-mounting-a-stratis-filesystem)
    - [7.6 Expanding a Pool](#76-expanding-a-pool)
    - [7.7 Creating a Snapshot](#77-creating-a-snapshot)
    - [7.8 Checking Size and Usage](#78-checking-size-and-usage)
    - [7.9 Removing a Filesystem and Pool](#79-removing-a-filesystem-and-pool)
  - [8. Advanced Features (Stratis)](#8-advanced-features-stratis)
  - [9. Important Limitations and Caveats](#9-important-limitations-and-caveats)
  - [10. Summary Table – LVM vs Stratis](#10-summary-table--lvm-vs-stratis)
  - [11. Real‑World Scenario – Provisioning Storage for a Containerized Application](#11-realworld-scenario--provisioning-storage-for-a-containerized-application)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [1. Install and start Stratis](#1-install-and-start-stratis)
      - [2. Create a single pool across all three disks](#2-create-a-single-pool-across-all-three-disks)
      - [3. Create the required file systems](#3-create-the-required-file-systems)
      - [4. Mount the file systems persistently](#4-mount-the-file-systems-persistently)
      - [5. Set appropriate permissions for the container user](#5-set-appropriate-permissions-for-the-container-user)
      - [6. Use volume mounts in Podman containers](#6-use-volume-mounts-in-podman-containers)
      - [7. Take a snapshot of the database volume before a migration](#7-take-a-snapshot-of-the-database-volume-before-a-migration)
      - [8. Check pool usage and alerts](#8-check-pool-usage-and-alerts)
      - [9. Clean up after testing](#9-clean-up-after-testing)
    - [Benefits Realized](#benefits-realized)
  - [12. Practice Lab – Getting Hands‑on with Stratis](#12-practice-lab--getting-handson-with-stratis)

---

## 1. What is Stratis?

Stratis is a **local storage-management solution for Linux** introduced by Red Hat. It’s designed to simplify storage administration by abstracting away the complexity of low‑level storage stacks like LVM, device‑mapper, and XFS. In the background, Stratis runs as a system service (`stratisd`) and uses battle‑tested components: XFS for the file system, LVM’s thin‑provisioning features, and device‑mapper for cache and encryption. Version 3.9.0 adds online encryption management and cache‑less pool startup.

**Architecture** – Stratis relies on a daemon (`stratisd`) that manages pools of block devices. It exposes a simple command‑line interface (`stratis`) and a D‑Bus API for automation. All user interactions go through `stratis`, which instructs the daemon to carry out the required operations.

---

## 2. Core Concepts of Stratis

| Term | Meaning |
|------|---------|
| **blockdev** | A raw block device (disk, partition, LVM LV, LUKS volume, MD RAID member) that can be added to a pool. |
| **pool** | One or more block devices aggregated into a single storage pool. The pool has a fixed total size (sum of its blockdevs) and provides the foundation for file systems. Stratis creates a `/dev/stratis/<pool_name>` directory that holds links to the file systems in that pool. |
| **filesystem** | A thinly‑provisioned XFS file system that lives inside a pool. It has no fixed size; it grows automatically as data is added. Stratis manages the XFS file system and automatically expands the thin volume when needed. |

> **Important**: Once a file system is managed by Stratis, you must **not** reconfigure or reformat it using standard XFS tools – only through the `stratis` CLI.

---

## 3. LVM Overview (For Comparison)

**LVM** (Logical Volume Manager) is the classic, mature storage‑management toolkit. It operates on three layers:

- **Physical Volume (PV)** – a raw disk or partition that has been initialized for LVM.
- **Volume Group (VG)** – a pool of space aggregated from one or more PVs.
- **Logical Volume (LV)** – a virtual block device carved from a VG. LVs can be resized (extended, and with ext4 also reduced), cloned, and striped.

LVM supports:
- Thin provisioning (LVM thin pool)
- Snapshots (copy‑on‑write)
- Software RAID (through `lvconvert` or kernel MD)
- Encryption (via `cryptsetup`)

---

## 4. Detailed Comparison – LVM vs Stratis

| Feature / Aspect | LVM (Traditional) | Stratis |
|-----------------|-------------------|---------|
| **Abstraction level** | Low‑level; you manage PVs, VGs, LVs, file systems, encryption, and caching separately. | High‑level; a single command (`stratis`) handles the entire stack. |
| **Installation** | `lvm2` package – always present on enterprise Linux. | `stratisd` + `stratis-cli` – must be installed separately. |
| **Daemon requirement** | `lvm2-lvmetad` and `lvm2-pvscan` (optional). | `stratisd` **must** be running. |
| **File system** | Any file system (XFS, ext4, etc.) you format manually. | Only XFS, automatically formatted and managed by Stratis. |
| **Thin provisioning** | LVM‑thin pool – create thin pool LV, then thin LVs. Manual steps. | Built‑in; every Stratis file system is thinly provisioned by default. |
| **Snapshots** | LVM‑thin snapshots are supported; requires thin pool and manual creation. | `stratis filesystem snapshot` – one command, no separate pool needed. |
| **Storage pool** | VG – you explicitly create the VG and then add PVs. | Pool is created directly from blockdevs in a single step (`pool create`). |
| **Capacity expansion** | Add new PV to VG, then extend LV and file system (separate commands). | Add block devices to pool with `pool add-data`, file systems grow automatically. |
| **Encryption** | Manual – create LUKS device, decrypt, then use as PV. | Built‑in – `pool create --encrypt`; supports LUKS2, NBDE, TPM2. |
| **Caching** | Manual – create cache pool LV, attach to main LV. | Integrated – Stratis automatically uses your fastest block devices as cache. |
| **API / automation** | Standard CLI (`pvs`, `vgs`, `lvs`). | D‑Bus API and REST‑like API (through `stratis`) – “Rich API” for developers. |
| **Error handling** | Very robust, decades of production use. | Still maturing; in RHEL 8 it was Technology Preview, **full support starting with RHEL 9.3**. |
| **Data self‑repair** | No (checksums are file‑system dependent; XFS/JFS lack built‑in repair). | Not yet supported. |
| **Performance (benchmark)** | Higher raw transfer speeds (e.g., 82.8 MB/s upload). | Faster write speeds (e.g., 254.9 MB/s using `dd`) in some tests. |

---

## 5. When to Use LVM

- **Existing infrastructure** – you already have mature LVM scripts and knowledge.
- **Mixed file systems** – you need ext4 (e.g., you want shrink support) or other non‑XFS file systems.
- **Maximum control** – you want to tune every layer (cache size, stripe width, mirror layout).
- **Complex RAID layouts** – LVM can build RAID 0/1/4/5/6/10 and you can integrate with `mdadm` or hardware RAID.
- **Legacy support** – older RHEL versions where Stratis is not fully supported.

---

## 6. When to Use Stratis

- **Simplicity** – you want to create a storage pool and multiple file systems with just two commands.
- **Developer / dev‑test environments** – quickly spin up and tear down thinly provisioned file systems; snapshots for fast rollbacks.
- **Modern workloads** – containers, cloud VMs, or edge devices where production support in RHEL 9.3+ is acceptable.
- **Encryption & caching out of the box** – you need disk encryption and SSD caching but don’t want to learn dm‑crypt or LVM cache.
- **Automation** – the D‑Bus API makes it easy to integrate storage provisioning into CM tools (Ansible, Puppet) without scripting low‑level commands.

---

## 7. Installation and Basic Management

### 7.1 Install Stratis

```bash
sudo dnf install stratisd stratis-cli
```

### 7.2 Start and enable the daemon

```bash
sudo systemctl enable --now stratisd
```

### 7.3 Creating a Storage Pool

```bash
stratis pool create pool_data /dev/sdb /dev/sdc
```

To list pools:

```bash
stratis pool list
```

### 7.4 Creating a Filesystem in the Pool

```bash
stratis filesystem create pool_data fs_app
```

This creates a thinly‑provisioned XFS file system. The mount point is:

```
/dev/stratis/pool_data/fs_app
```

### 7.5 Mounting a Stratis Filesystem

```bash
sudo mkdir -p /mnt/appdata
sudo mount /dev/stratis/pool_data/fs_app /mnt/appdata
```

To make it persistent in `/etc/fstab`, use the UUID from `blkid` and add `x-systemd.requires=stratisd.service`:

```
UUID="..."  /mnt/appdata  xfs  defaults,x-systemd.requires=stratisd.service  0 0
```

### 7.6 Expanding a Pool

```bash
stratis pool add-data pool_data /dev/sdd /dev/sde
```

### 7.7 Creating a Snapshot

```bash
stratis filesystem snapshot pool_data fs_app fs_app_snap
```

Mount the snapshot similarly:

```bash
mkdir /mnt/snapshot
mount /dev/stratis/pool_data/fs_app_snap /mnt/snapshot
```

### 7.8 Checking Size and Usage

Because Stratis uses thin provisioning, `df -h` will show the **virtual size** (e.g., 1 TiB) even if the pool is almost full. Use:

```bash
stratis pool list
stratis filesystem list
stratis blockdev list
```

### 7.9 Removing a Filesystem and Pool

```bash
stratis filesystem destroy pool_data fs_app_snap
stratis pool destroy pool_data
```

---

## 8. Advanced Features (Stratis)

- **Encryption** – create an encrypted pool:
  ```bash
  stratis pool create --encrypt pool_enc /dev/sdb
  ```
  The system will prompt for a passphrase or you can use NBDE/TPM2.

- **Key management** – Stratis 3.9.0 allows **re‑encryption** of a pool (change the encryption key) without losing data.

- **Cache tiering** – Stratis uses the fastest block devices in a pool as a non‑volatile data cache (dm‑cache target). No manual setup needed.

- **Monitoring** – Stratis monitors the pool health. If a blockdev fails, `stratis pool list` shows alerts.

---

## 9. Important Limitations and Caveats

| Limitation | Explanation |
|------------|-------------|
| **XFS only** | You cannot use ext4, ZFS, or other file systems with Stratis. |
| **No shrink** | XFS file systems managed by Stratis cannot be shrunk. |
| **No self‑repair** | Unlike ZFS or Btrfs, Stratis does not provide data checksums with self‑healing. |
| **`df` reports inaccurate sizes** | `df -h` shows the virtual (thin) size, not the actual pool usage. Always use `stratis filesystem list`. |
| **Do not mix management tools** | Do not use LVM or XFS commands directly on objects managed by Stratis – you will corrupt metadata. |
| **Do not stack Stratis on thin provisioned devices** | “Red Hat does not recommend placing a Stratis pool on block devices that are already thinly‑provisioned”. |

---

## 10. Summary Table – LVM vs Stratis

| | LVM | Stratis |
|--|-----|---------|
| **Complexity** | High – many layers and commands | Low – one CLI, daemon handles the rest |
| **Deployment speed** | Minutes to hours (depending on experience) | Seconds |
| **Footprint** | Minimal (kernel LVM module only) | Additional daemon (`stratisd`) + Python tooling |
| **Home / dev‑test** | Overkill | Excellent |
| **Production (RHEL 9.3+)** | Fully supported | Fully supported |
| **Encryption** | Via LUKS (separate steps) | Built‑in (LUKS2, NBDE, TPM2) |
| **Snapshot & revert** | Yes, but requires thin pool | Yes, one command, no separate pool |
| **Cache** | Manual | Automatic |
| **Data checksums** | No | No (planned for future?) |

---

## 11. Real‑World Scenario – Provisioning Storage for a Containerized Application

### Background

Your team is deploying a containerized microservices platform on a RHEL 9 server named `appnode‑01`. The platform uses Podman and requires:

- A persistent volume for the database (`/data/db`) that can grow dynamically.
- A fast, temporary cache volume for logs (`/data/logs`) where performance is key but data is not critical.
- Ability to take point‑in‑time snapshots of the database volume before schema migrations.
- The server has three spare physical disks: `/dev/sdb` (100 GB, SSD), `/dev/sdc` (100 GB, SSD), `/dev/sdd` (200 GB, HDD).

Your task is to provision this storage using Stratis, leveraging its simplicity and thin provisioning.

### Step‑by‑Step Implementation

#### 1. Install and start Stratis

```bash
sudo dnf install -y stratisd stratis-cli
sudo systemctl enable --now stratisd
```

#### 2. Create a single pool across all three disks

```bash
sudo stratis pool create apppool /dev/sdb /dev/sdc /dev/sdd
```

Stratis automatically uses the SSDs (`/dev/sdb`, `/dev/sdc`) as a cache tier for the slower HDD (`/dev/sdd`). The pool aggregates all space.

Verify with:

```bash
sudo stratis pool list
```

#### 3. Create the required file systems

```bash
sudo stratis filesystem create apppool db_data
sudo stratis filesystem create apppool log_data
```

Both are thinly provisioned; they will grow automatically as needed.

List them:

```bash
sudo stratis filesystem list
```

#### 4. Mount the file systems persistently

Get the UUIDs with `sudo blkid /dev/stratis/apppool/db_data` (or use `/dev/stratis/apppool/db_data` directly in a pinch).

Create mount points and temporary mounts:

```bash
sudo mkdir -p /data/db /data/logs
sudo mount /dev/stratis/apppool/db_data /data/db
sudo mount /dev/stratis/apppool/log_data /data/logs
```

Add entries to `/etc/fstab`:

```
/dev/stratis/apppool/db_data  /data/db   xfs  defaults,x-systemd.requires=stratisd.service  0 0
/dev/stratis/apppool/log_data /data/logs  xfs  defaults,x-systemd.requires=stratisd.service  0 0
```

Test with `sudo mount -a`.

#### 5. Set appropriate permissions for the container user

```bash
sudo chown -R podman_user:podman_group /data/db /data/logs
```

#### 6. Use volume mounts in Podman containers

For the database service, you can map `/data/db` into the container. For logs, `/data/logs`.

#### 7. Take a snapshot of the database volume before a migration

```bash
sudo stratis filesystem snapshot apppool db_data db_data_pre_migration
```

You can mount this snapshot later to verify data or roll back.

```bash
mkdir /mnt/db_snap
sudo mount /dev/stratis/apppool/db_data_pre_migration /mnt/db_snap
# Verify data ...
sudo umount /mnt/db_snap
```

If the migration fails, you could restore from the snapshot by copying data back, or by creating a new file system from the snapshot (Stratis copies are read‑write, but the snapshot itself is a point‑in‑time copy that you can work with – note: Stratis snapshots are read‑write by default, so they can serve as a direct replacement if mounted in place).

#### 8. Check pool usage and alerts

```bash
sudo stratis pool list
sudo stratis blockdev list
```

If a disk fails, the pool will show a warning. You can add a replacement disk to the pool (`sudo stratis pool add-data apppool /dev/sde`).

#### 9. Clean up after testing

```bash
sudo stratis filesystem destroy apppool db_data_pre_migration   # optional if you want to keep snapshot
sudo umount /data/db
sudo umount /data/logs
sudo stratis filesystem destroy apppool db_data
sudo stratis filesystem destroy apppool log_data
sudo stratis pool destroy apppool
```

### Benefits Realized

- The entire storage stack was provisioned with 6 commands (`pool create`, two `filesystem create`s, two `mount`s, one `snapshot`).
- No need to deal with LVM volumes, XFS formatting, or thin pool management.
- Snapshots are instantaneous and enable safe application updates.
- Cache tiering automatically used the SSDs, improving performance without any extra configuration.

---

## 12. Practice Lab – Getting Hands‑on with Stratis

1. **Install** `stratisd` and `stratis-cli` on your RHEL 9 system. Start and enable the service.

2. **Add two spare disks** (e.g., `/dev/vdb`, `/dev/vdc`) to your VM. **Clean** the disks using `wipefs -af /dev/vdb` and `/dev/vdc`.

3. **Create a Stratis pool** called `pool_lab` using both spare disks.

4. **Create two file systems** inside `pool_lab`: `fs_data` and `fs_backup`.

5. **Mount** both file systems under `/mnt/data` and `/mnt/backup` and write some test files.

6. **Create a snapshot** of `fs_data` called `fs_data_snap`. Verify that the snapshot appears in `/dev/stratis/pool_lab/`.

7. **Extend the pool** by adding a third spare disk (`/dev/vdd`). Check the pool size with `stratis pool list`.

8. **Encryption testing**: create a second, encrypted pool (provide a temporary passphrase). Unlock and mount it.

9. **Clean up** – destroy the snapshots, file systems, and pools.

10. **Compare logs** – run `journalctl -u stratisd` to see detailed daemon operations.

---

**Date documented:** 2026-05-11  
**Sources:** Red Hat Enterprise Linux 9 documentation, Stratis design documents, LVM manual pages

---
