# Chapter 10: Using the Virtual Data Optimizer (VDO)

This chapter explains the **Virtual Data Optimizer (VDO)** – a storage‑layer technology that increases usable capacity by eliminating duplicate blocks, compressing data, and stripping zero‑filled regions. VDO is part of Red Hat Enterprise Linux 8 and 9 and is especially useful for reducing storage footprint in virtualized environments, container storage, and backup targets.

---

## Table of Contents

- [Chapter 10: Using the Virtual Data Optimizer (VDO)](#chapter-10-using-the-virtual-data-optimizer-vdo)
  - [Table of Contents](#table-of-contents)
  - [1. What is VDO? Why Do We Need It?](#1-what-is-vdo-why-do-we-need-it)
  - [2. VDO Architecture – kvdo and uds](#2-vdo-architecture--kvdo-and-uds)
  - [3. The Three Core Features of VDO](#3-the-three-core-features-of-vdo)
    - [3.1 Zero‑Block Elimination](#31-zeroblock-elimination)
    - [3.2 Deduplication](#32-deduplication)
    - [3.3 Compression](#33-compression)
  - [4. How VDO Works – On‑the‑Fly Processing](#4-how-vdo-works--onthefly-processing)
  - [5. Which Data Types Benefit Most?](#5-which-data-types-benefit-most)
  - [6. Installing and Managing VDO](#6-installing-and-managing-vdo)
    - [6.1 Installing VDO Packages](#61-installing-vdo-packages)
    - [6.2 Creating a VDO Volume](#62-creating-a-vdo-volume)
    - [6.3 Managing a VDO Volume (Start, Stop, Status)](#63-managing-a-vdo-volume-start-stop-status)
    - [6.4 Formatting and Mounting a VDO Volume](#64-formatting-and-mounting-a-vdo-volume)
    - [6.5 Checking Deduplication and Compression Statistics](#65-checking-deduplication-and-compression-statistics)
  - [7. VDO Performance Considerations](#7-vdo-performance-considerations)
  - [8. Limitations and Caveats](#8-limitations-and-caveats)
  - [9. Comparison: VDO vs. LVM Thin Provisioning vs. Stratis](#9-comparison-vdo-vs-lvm-thin-provisioning-vs-stratis)
  - [10. Quick Reference Table](#10-quick-reference-table)
  - [11. Practice Lab – Demonstrating VDO Efficiency](#11-practice-lab--demonstrating-vdo-efficiency)

---

## 1. What is VDO? Why Do We Need It?

**VDO (Virtual Data Optimizer)** is a Linux kernel module and a set of user‑space tools that sit between the block device layer and the file system. It **transparently** reduces the amount of physical storage consumed by data.

**Why do we need it?**

- **Reduce storage costs** – Store more logical data on the same physical disks.
- **Extend lifetime of SSDs** – Fewer writes due to deduplication and compression.
- **Optimise for virtualisation** – Many VMs running the same OS and applications produce large amounts of duplicate data.
- **Efficient backups** – Backup repositories often contain repeated blocks across different snapshots.
- **Container images** – Docker / Podman images share layers; VDO deduplicates them.

**How it appears to the system:**  
VDO creates a **virtual block device** (e.g., `/dev/mapper/vdo‑volume`). You format it with a file system (XFS or ext4) and mount it like any ordinary disk. All reads and writes are automatically processed for zero‑block elimination, deduplication, and compression.

---

## 2. VDO Architecture – kvdo and uds

VDO consists of two kernel modules that work together:

| Module | Role | Description |
|--------|------|-------------|
| **kvdo** | Data path module | Handles I/O requests, performs zero‑block detection, deduplication index lookup, compression, and writing to underlying storage. |
| **uds** | Indexing module | Provides a **deduplication index** (UDS = Universal Deduplication Service) that stores fingerprints of data blocks. New writes are compared against this index to find duplicates. |

**User‑space component:**  
`vdo` command (part of `vdo` package) creates, configures, and manages VDO volumes. It also supplies the `uds` index configuration (size, memory, etc.).

**Simplified I/O flow (write):**

```
Application write → File system → VDO block device (/dev/mapper/vdo‑vol)
                                          │
                                          ├─ kvdo: zero‑block? → discard
                                          ├─ kvdo: lookup uds index for fingerprint
                                          ├─ if duplicate → reference existing block
                                          ├─ else compress → store → update index
                                          └─ write to underlying physical device
```

---

## 3. The Three Core Features of VDO

### 3.1 Zero‑Block Elimination

- **What it does:** Detects blocks that are entirely zeros and does **not** allocate physical storage for them. Instead, only a small metadata entry marks the range as zero.
- **Why beneficial:** Zero‑filled areas (new LVs, unused space, sparse files) can consume enormous logical space but occupy almost nothing physically.
- **Example:** A freshly created 1 TiB thin‑provisioned LV filled with zeros uses zero physical blocks after VDO elimination.

### 3.2 Deduplication

- **What it does:** Identifies duplicate data blocks (e.g., same 4 KiB block appearing multiple times) and stores only **one** physical copy. All references point to that single block.
- **How it works:** Each incoming block is hashed (using a collision‑resistant hash). The hash is looked up in the UDS index. If the block is already stored, no new write is performed; only a reference count is incremented.
- **Example:** 100 VMs based on the same RHEL template may share many identical OS files – VDO deduplication can reduce the total physical usage to that of a single VM.

### 3.3 Compression

- **What it does:** Compresses data blocks (e.g., using LZ4 algorithm) *before* writing them to the physical device. Blocks that do not compress well are stored uncompressed.
- **How it affects capacity:** Typically reduces textual data (logs, config files, XML/JSON) by 50–70%. Binary executables and already compressed media see little benefit.
- **Example:** A 4 KiB block of log text could compress to 1 KiB, saving 75% physical space.

> **Important:** All three features are applied **simultaneously** and **online** – no offline optimisation pass is required.

---

## 4. How VDO Works – On‑the‑Fly Processing

When a write request reaches the VDO device:

1. **Zero‑block detection** – If the block is completely zero, it is discarded (no physical storage allocated). The logical block is marked as zero in VDO metadata.
2. **Fingerprint calculation** – A hash (e.g., SHA‑256) of the block (or only if non‑zero).
3. **Deduplication lookup** – The hash is checked against the UDS index.
   - If a match is found (same block already stored), VDO increments the reference count for that physical block and does **not** write the block again.
   - If no match, continue.
4. **Compression** – The block is compressed.
   - If compression saves space (e.g., compressed size < original), the compressed block is stored.
   - If compression does not reduce size, the original uncompressed block is stored.
5. **Index update** – The hash and mapping are stored in the UDS index for future lookups.
6. **Physical write** – The (compressed or uncompressed) block is written to the underlying storage device.

**Read path:**  
When an application reads a logical block, VDO looks up the physical block address (if it maps to a real block) or returns zeros (if it was zero‑eliminated). Deduplicated reads are just regular reads from the single physical block.

---

## 5. Which Data Types Benefit Most?

| Data Type | Deduplication | Compression | Zero‑block elimination |
|-----------|:-------------:|:-----------:|:----------------------:|
| VM disk images (OS, applications) | Very high | Low (many binaries) | Medium (empty disk areas) |
| Container images / layers | Very high | Medium | High (layers diff) |
| Database backup dumps (text logs) | High | High | Low |
| Mail server storage | Medium | Medium | Low |
| Office documents (DOCX, XLSX) | Low (already compressed) | Low | Low |
| Media (JPEG, MP4, MP3) | Very low | Very low | Low |
| Log files (text, JSON) | Medium | Very high | Medium |
| OS root images (RHEL / Ubuntu) | Very high | Medium | Medium |

> **Rule of thumb:** VDO performs best on datasets with **many duplicates** (virtualisation, containers, backups) and **compressible text**. It performs poorly on already‑compressed media.

---

## 6. Installing and Managing VDO

### 6.1 Installing VDO Packages

```bash
sudo dnf install vdo
```

The package installs:
- `vdo` – management command
- `kvdo.ko` and `uds.ko` – kernel modules
- `vdo` systemd service (`vdo.service`)

### 6.2 Creating a VDO Volume

Basic syntax:

```bash
sudo vdo create --name <vdo_name> --device <block_device> --vdoLogicalSize <size>
```

**Example:** Create a VDO volume named `vdo1` on `/dev/sdb` with a logical size of 1 TiB (physical disk is only 200 GiB).

```bash
sudo vdo create --name vdo1 --device /dev/sdb --vdoLogicalSize 1T
```

**Important options:**

| Option | Meaning |
|--------|---------|
| `--name` | Name of the VDO volume (appears as `/dev/mapper/vdo‑name`). |
| `--device` | Underlying block device (partition, disk, LVM LV). |
| `--vdoLogicalSize` | Logical size (user‑visible capacity) – can exceed physical size. |
| `--vdoSlabSize` | Slab size for VDO metadata (default 2 GiB). |
| `--indexMem` | Memory (GB) allocated to UDS deduplication index (default 0.25 GB). Increase for better dedup on large datasets. |
| `--blockMapCacheSize` | Cache size for block map (default 128 MiB). |
| `--writePolicy` | `sync` (safe, slower) or `async` (faster, risk of data loss on power failure). Default = `auto` (sync for physical devices without cache). |

**Example with custom index memory:**

```bash
sudo vdo create --name vdo2 --device /dev/sdc --vdoLogicalSize 2T --indexMem 1 --writePolicy sync
```

### 6.3 Managing a VDO Volume (Start, Stop, Status)

```bash
# Start a VDO volume
sudo vdo start --name vdo1

# Stop a VDO volume
sudo vdo stop --name vdo1

# List all VDO volumes
sudo vdo list

# Show detailed status
sudo vdo status --name vdo1
```

After creation, the VDO volume is automatically started and enabled to start on boot. You can check its device with:

```bash
lsblk /dev/mapper/vdo-vdo1
```

### 6.4 Formatting and Mounting a VDO Volume

Once the VDO volume is created, treat it as a normal block device:

```bash
# Format with XFS
sudo mkfs.xfs /dev/mapper/vdo-vdo1

# Mount
sudo mkdir -p /mnt/vdo
sudo mount /dev/mapper/vdo-vdo1 /mnt/vdo
```

**Automount at boot** – add entry to `/etc/fstab`:

```
/dev/mapper/vdo-vdo1 /mnt/vdo xfs defaults 0 0
```

### 6.5 Checking Deduplication and Compression Statistics

The `vdo status` command provides detailed metrics:

```bash
sudo vdo status --name vdo1 | grep -E "(deduplication|compression|saving)"
```

**Key statistics lines:**

| Metric | Meaning |
|--------|---------|
| `Logical blocks used` | Logical blocks written by file system. |
| `Physical blocks used` | Blocks actually stored on disk. |
| `Deduplication ratio` | Logical / Physical after dedup. |
| `Compression ratio` | Compressed size / original size (inverse). |
| `Saving percentage` | Overall space saved = (logical - physical) / logical. |

**Monitor in real time** – use:

```bash
watch -n 2 'sudo vdo status --name vdo1 | grep -E "(Logical blocks used|Physical blocks used|deduplication ratio|compression ratio)"'
```

---

## 7. VDO Performance Considerations

- **CPU overhead** – Hashing, compression, and index lookups consume CPU. For high‑throughput workloads, provision additional CPU cores.
- **Memory requirements** – The UDS index (`--indexMem`) plus block map cache (`--blockMapCacheSize`) can require GBs of RAM. A 1 TiB logical size with default index (0.25 GB) may be insufficient; increase to 1 GB for better dedup hit rate.
- **Write amplification** – Deduplication and compression can reduce writes but also cause additional I/O for index updates. For SSD storage, this may actually improve endurance.
- **When to avoid VDO** – Already‑compressed datasets (media archives), high‑performance trading systems, or latency‑sensitive applications (dedup adds latency).

---

## 8. Limitations and Caveats

| Limitation | Impact |
|------------|--------|
| **Cannot shrink a VDO volume** | Logical size can be increased, but never reduced (unless you recreate the volume). |
| **Cannot use VDO on top of other VDO volumes** | Layers would cause severe performance degradation. |
| **Deduplication only within a single VDO volume** | Does not deduplicate across volumes (unless shared underlying storage). |
| **Synchronous writes** – default `writePolicy auto` may still be `sync` on many devices, hurting performance. For workloads tolerant of some data loss, change to `async`. |
| **Not recommended for databases** – High random I/O and low dedup ratios make VDO less beneficial. |

---

## 9. Comparison: VDO vs. LVM Thin Provisioning vs. Stratis

| Feature | VDO | LVM Thin | Stratis |
|---------|-----|----------|---------|
| **Zero‑block elimination** | ✅ native | ❌ (no) | ❌ (not directly) |
| **Deduplication** | ✅ integrated | ❌ | ❌ (planned?) |
| **Compression** | ✅ (LZ4) | ❌ | ❌ |
| **Thin provisioning** | ✅ (by logical size) | ✅ (thin pool) | ✅ (all file systems thinly provisioned) |
| **Snapshots** | ❌ (separate tool, e.g., `dm‑snap`) | ✅ (thin snapshots) | ✅ (native) |
| **File system** | Any (XFS, ext4) | Any | Only XFS |
| **Management complexity** | Medium | Medium | Low |
| **Best use case** | Reducing duplicate/compressible data | Flexible volume sizing | Simple thin storage management |

**Combine them?** Yes – you can create an LVM thin pool, format it as XFS, then place a VDO volume on top of an LV? Not recommended. Typical practice: **VDO on a raw disk or partition**; LVM on top of VDO is possible but adds overhead.

---

## 10. Quick Reference Table

| Task | Command |
|------|---------|
| Install VDO | `sudo dnf install vdo` |
| Create VDO volume | `sudo vdo create --name vdo_name --device /dev/sdX --vdoLogicalSize SIZE` |
| Start a VDO volume | `sudo vdo start --name vdo_name` |
| Stop a VDO volume | `sudo vdo stop --name vdo_name` |
| List volumes | `sudo vdo list` |
| Show status | `sudo vdo status --name vdo_name` |
| Remove VDO volume | `sudo vdo remove --name vdo_name` |
| Format VDO volume | `sudo mkfs.xfs /dev/mapper/vdo‑vdo_name` |
| Mount | `sudo mount /dev/mapper/vdo‑vdo_name /mountpoint` |
| Get statistics | `sudo vdo status --name vdo_name \| grep -E "(logical|physical|deduplication|compression)"` |

---

## 11. Practice Lab – Demonstrating VDO Efficiency

**Goal:** Create a VDO volume on a small disk (e.g., 10 GiB) with a large logical size (e.g., 50 GiB), fill it with duplicate data, and verify the physical usage is much smaller.

**Step‑by‑step:**

1. **Add a spare disk** (e.g., `/dev/vdb`) of 10 GiB to your VM.

2. **Install VDO** and start the service:
   ```bash
   sudo dnf install -y vdo
   sudo systemctl enable --now vdo
   ```

3. **Create VDO volume**:
   ```bash
   sudo vdo create --name vdo_lab --device /dev/vdb --vdoLogicalSize 50G --indexMem 0.25
   ```

4. **Check creation**:
   ```bash
   sudo vdo list
   lsblk /dev/mapper/vdo-vdo_lab
   ```

5. **Format and mount**:
   ```bash
   sudo mkfs.xfs /dev/mapper/vdo-vdo_lab
   sudo mkdir -p /mnt/vdo_lab
   sudo mount /dev/mapper/vdo-vdo_lab /mnt/vdo_lab
   df -h /mnt/vdo_lab   # should show ~50 GiB logical capacity
   ```

6. **Generate duplicate data** – a 1 GiB file of zeros (already zero‑block eliminated) and a text file repeated many times:
   ```bash
   # Create 10 copies of the same random file (compressible)
   dd if=/dev/urandom of=/tmp/seed.bin bs=1M count=10
   for i in {1..10}; do cp /tmp/seed.bin /mnt/vdo_lab/duplicate_$i.bin; done
   ```

7. **Check VDO statistics**:
   ```bash
   sudo vdo status --name vdo_lab | grep -E "Physical blocks used|deduplication"
   ```

   The physical blocks used should be close to the size of a single 10 MiB block (plus metadata), not 100 MiB.

8. **Clean up**:
   ```bash
   sudo umount /mnt/vdo_lab
   sudo vdo stop --name vdo_lab
   sudo vdo remove --name vdo_lab
   ```

---

**Date documented:** 2026-05-11  
**Sources:** Red Hat Enterprise Linux 9 Managing Storage Devices, `vdo` man pages, Red Hat Virtual Data Optimizer documentation.

---
