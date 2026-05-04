# Chapter 16: Accessing Linux File Systems – Complete Professional Guide

## Table of Contents

- [1. Complete Disk Lifecycle Tutorial – From Physics to `fstab`](#1-complete-disk-lifecycle-tutorial--from-physics-to-fstab)
- [2. Deep Dive into Interfaces and Device Naming](#2-deep-dive-into-interfaces-and-device-naming)
- [3. Partitioning – MBR and GPT (Detailed)](#3-partitioning--mbr-and-gpt-detailed)
- [4. Logical Volume Manager (LVM) – Complete Reference](#4-logical-volume-manager-lvm--complete-reference)
- [5. File Systems – XFS and ext4](#5-file-systems--xfs-and-ext4)
- [6. Mounting and `/etc/fstab`](#6-mounting-and-etcfstab)
- [7. Disk Space Management – `df` and `du`](#7-disk-space-management--df-and-du)
- [8. RAID – Redundant Array of Independent Disks](#8-raid--redundant-array-of-independent-disks)
- [9. Important Disk Utilities – Comprehensive](#9-important-disk-utilities--comprehensive)
- [10. Searching for Files – `locate` vs `find`](#10-searching-for-files--locate-vs-find)
- [11. Additional Important Notes](#11-additional-important-notes)
- [12. Quick Reference Table](#12-quick-reference-table)
- [13. Practice Lab – Verify Your Understanding](#13-practice-lab--verify-your-understanding)
- [14. Real‑World Scenario – Setting Up Storage for a Database Server](#14-realworld-scenario--setting-up-storage-for-a-database-server)

---

## 1. Complete Disk Lifecycle Tutorial – From Physics to `fstab`

This section tells the **story** of how data moves from spinning platters (or flash chips) to a mounted file system in Linux. Each phase is explained with the **historical problem** it solved.

### 1.1 The Physical Layer (Hardware)

#### Magnetic vs. Silicon – HDD, SSD, NVMe

- **HDD (Hard Disk Drive)** – Spinning magnetic platters, read/write head on an arm. Data stored in tracks and sectors (512 or 4096 bytes). **Problem:** slow seek time, latency.
- **SSD (Solid State Drive)** – NAND flash memory, no moving parts. **Problem:** SATA interface became a bottleneck (max ~550 MB/s).
- **NVMe (Non‑Volatile Memory Express)** – Protocol designed for flash over PCIe. Supports 65k queues with 64k commands each. Appears as `/dev/nvme0n1`.

#### Historical Interfaces – Why Linux Uses `/dev/sdX`

- **PATA (Parallel ATA)** – Old ribbon cable, master/slave, max 133 MB/s. Linux naming: `/dev/hdX` (deprecated).
- **SATA (Serial ATA)** – Point‑to‑point, hot‑plug, up to 16 GB/s. Still uses ATA command set but wraps into SCSI via **libata**.
- **SCSI (Small Computer System Interface)** – Original server‑grade parallel bus. High reliability.
- **SAS (Serial Attached SCSI)** – Modern point‑to‑point, dual‑port, scales to thousands of devices.
- **iSCSI (Internet SCSI)** – SCSI commands over IP networks.

The Linux kernel’s **SCSI subsystem** handles SATA, SAS, USB, and many virtual disks. Therefore almost all appear as `/dev/sdX`. NVMe has its own driver (`/dev/nvmeXnY`).

### 1.2 Partitioning – MBR vs. GPT

Before using a disk, you must create a **partition table** that defines logical sections.

- **MBR (Master Boot Record)** – Legacy (1983). Limits: 2 TiB max disk, 4 primary partitions. Workaround: extended partitions. No redundancy, no checksum.
- **GPT (GUID Partition Table)** – Modern. Supports disks up to 9.4 ZiB, 128 partitions, backup table at end of disk, CRC32 checksums, unique partition GUIDs.

**Tools:** `fdisk` (MBR+GPT), `gdisk` (GPT only), `parted` (both).

### 1.3 LVM Initialisation – PV, VG, LV

LVM adds **flexibility** by abstracting physical storage.

- **Physical Volume (PV)** – A disk or partition initialised with LVM metadata.
- **Volume Group (VG)** – A pool of physical extents (PEs, default 4 MiB).
- **Logical Volume (LV)** – A set of PEs; appears as a block device.

**Why LVM?** You can resize LVs online, take snapshots, stripe across disks, and add/remove physical disks without downtime.

### 1.4 File System Creation (Formatting)

An LV is raw space. A **file system** organises it into directories, files, and metadata.

- **XFS** – Default in RHEL. Scalable, high performance, **cannot shrink**.
- **ext4** – Mature, can be shrunk offline, good for general purpose.

**Command:** `mkfs.xfs` or `mkfs.ext4`.

### 1.5 Mounting – Attaching to the Directory Tree

Linux accesses file systems through **mount points** (directories).

- Manual: `mount /dev/vg01/lv01 /mnt/data`
- Automatic: `/etc/fstab` entries using **UUID** (persistent identifier).

### 1.6 Resizing – The Golden Rule

- **XFS:** only grow. `lvextend -r` (or `lvextend` then `xfs_growfs`).
- **ext4:** grow online, shrink offline (unmount → `e2fsck` → `resize2fs` → `lvreduce`).

---

## 2. Deep Dive into Interfaces and Device Naming

### 2.1 PATA, SATA, SCSI, SAS, iSCSI

| Interface | Type | Speed | Linux device |
|-----------|------|-------|---------------|
| PATA | Parallel | ≤133 MB/s | `/dev/hdX` (old) |
| SATA | Serial | ≤16 GB/s | `/dev/sdX` |
| SCSI | Parallel | ≤640 MB/s | `/dev/sdX` |
| SAS | Serial | ≤22.5 GB/s | `/dev/sdX` |
| iSCSI | Network | limited by network | `/dev/sdX` |

### 2.2 HDD, SSD, NVMe Mechanics

See section 1.1.

### 2.3 Linux Device Names

```bash
# Traditional SATA/SAS/USB
/dev/sda   # first disk
/dev/sda1  # first partition
/dev/sdb   # second disk

# NVMe
/dev/nvme0n1     # first namespace on first controller
/dev/nvme0n1p1   # first partition
```

**List all block devices:** `lsblk`

---

## 3. Partitioning – MBR and GPT (Detailed)

### 3.1 MBR Limitations and Structure

- **Disk size limit:** 2 TiB (32‑bit sector addresses, 512‑byte sectors).
- **Partition entries:** 4 primary (16 bytes each). Logical drives possible inside extended partition.
- **No redundancy** – single copy; a corrupted sector can lose entire disk.

**Example `fdisk` on MBR disk:**
```bash
sudo fdisk /dev/sdb
# Command: p (print), n (new), t (type 83 for Linux), w (write)
```

### 3.2 GPT Advantages and Layout

- **64‑bit LBAs** → 9.4 ZiB max.
- **128 partitions** by default.
- **Protective MBR** (LBA 0) prevents old tools from overwriting.
- **Primary GPT header** (LBA 1) with CRC32.
- **Partition entries** (LBA 2–33).
- **Backup GPT** at end of disk.

**Example `gdisk` on GPT disk:**
```bash
sudo gdisk /dev/sdb
# o – new GPT table
# n – new partition (accept defaults, then type 8E00 for LVM)
# w – write
```

### 3.3 Partitioning Tools – Complete Options

| Tool | Supported Tables | Interactive | Scripting | Key Options / Examples |
|------|-----------------|-------------|-----------|------------------------|
| `fdisk` | MBR + GPT | `fdisk /dev/sdb` | `fdisk -l` (list), `sfdisk -d` (dump) | `-l, -s, -u` |
| `gdisk` | GPT | `gdisk /dev/sdb` | `sgdisk` (scripting) | `-o` (new), `-n` (new part), `-t` (type) |
| `parted` | MBR + GPT | `parted /dev/sdb` | `parted -s` | `mklabel gpt`, `mkpart primary 0% 100%`, `print` |
| `sfdisk` | MBR + GPT (dump/restore) | no | `sfdisk -d /dev/sda > table` | `-d` (dump), `-f` (force) |

**Examples:**
```bash
# Dump partition table to a file
sudo sfdisk -d /dev/sda > mypartitions.bak

# Restore to another disk
sudo sfdisk /dev/sdb < mypartitions.bak

# Create a GPT partition using parted non-interactively
sudo parted /dev/sdb mklabel gpt mkpart primary ext4 0% 100% set 1 lvm on

# Reload partition table without reboot
sudo partprobe /dev/sdb
```

---

## 4. Logical Volume Manager (LVM) – Complete Reference

### 4.1 LVM Layers

```
Disk → Partition → Physical Volume (PV) → Volume Group (VG) → Logical Volume (LV) → File system
```

### 4.2 LVM Commands – Full Options and Examples

#### Physical Volume (PV)

| Command | Options | Example |
|---------|---------|---------|
| `pvcreate` | `-f` (force), `-u` (UUID) | `sudo pvcreate /dev/sdb1` |
| `pvs` | `-o` (columns), `--units` | `pvs --units g` |
| `pvdisplay` | `-m` (map), `-C` (column) | `sudo pvdisplay /dev/sdb1` |
| `pvremove` | – | `sudo pvremove /dev/sdb1` |

**Example – list PVs with custom columns:**
```bash
pvs -o pv_name,vg_name,pv_size,pv_used --units g
```

#### Volume Group (VG)

| Command | Options | Example |
|---------|---------|---------|
| `vgcreate` | `-s` (PE size) | `sudo vgcreate -s 16M vg_data /dev/sdb1` |
| `vgs` | `-o` | `vgs --sort vg_name` |
| `vgdisplay` | `-v` (verbose) | `sudo vgdisplay vg_data` |
| `vgextend` | – | `sudo vgextend vg_data /dev/sdc1` |
| `vgreduce` | `-a` (remove missing) | `sudo vgreduce vg_data /dev/sdc1` |
| `vgremove` | – | `sudo vgremove vg_data` |

#### Logical Volume (LV)

| Command | Options | Example |
|---------|---------|---------|
| `lvcreate` | `-L` (size), `-n` (name), `-s` (snapshot) | `sudo lvcreate -L 10G -n lv_data vg_data` |
| `lvs` | `-o` (columns), `--units` | `lvs -o lv_name,size,data_percent` |
| `lvdisplay` | `-m` (map) | `sudo lvdisplay /dev/vg_data/lv_data` |
| `lvextend` | `-L +SIZE`, `-r` (resize fs) | `sudo lvextend -r -L +5G /dev/vg_data/lv_data` |
| `lvreduce` | `-L SIZE` | `sudo lvreduce -L 8G /dev/vg_data/lv_data` |
| `lvremove` | `-f` (force) | `sudo lvremove -f /dev/vg_data/lv_data` |
| `lvrename` | – | `sudo lvrename vg_data lv_data lv_backup` |
| `lvconvert` | `--type raid1` (LVM RAID) | `sudo lvconvert --type raid1 /dev/vg_data/lv_backup` |

**Snapshots (copy‑on‑write):**
```bash
sudo lvcreate -s -n lv_data_snap -L 1G /dev/vg_data/lv_data
```

**Thin provisioning (create thin pool, then thin LV):**
```bash
sudo lvcreate -L 100G -T vg_data/thinpool
sudo lvcreate -V 200G -T vg_data/thinpool -n lv_thin
```

---

## 5. File Systems – XFS and ext4

### 5.1 XFS – Internals, Features, Commands

**Key characteristics:**
- Designed for large files and high concurrency.
- Uses **allocation groups (AGs)** – each AG has its own inode and free‑space maps → parallel I/O.
- Delayed allocation (write buffering) → better block layout.
- **Cannot shrink** – even offline.
- Online defragmentation (`xfs_fsr`).

**`mkfs.xfs` options:**

| Option | Meaning | Example |
|--------|---------|---------|
| `-m reflink=1` | Enable file reflinks (dedupe) | `mkfs.xfs -m reflink=1 /dev/vg/lv` |
| `-d agcount=N` | Number of allocation groups | `-d agcount=4` |
| `-n size=value` | Directory block size | `-n size=8192` |
| `-i maxpct=N` | Maximum percentage of inode space | `-i maxpct=5` |

**XFS grow (while mounted):**
```bash
sudo xfs_growfs /mnt/point
```

**XFS repair (must be unmounted):**
```bash
sudo xfs_repair -n /dev/vg/lv   # dry run
sudo xfs_repair /dev/vg/lv       # actual repair
```

**XFS defrag:**
```bash
sudo xfs_fsr /dev/vg/lv
```

### 5.2 ext4 – Internals, Features, Commands

**Key characteristics:**
- Mature, stable, can be shrunk offline.
- Uses **extents** (instead of block lists) for large files.
- Supports `resize2fs` (grow online, shrink offline).

**`mkfs.ext4` options:**

| Option | Meaning | Example |
|--------|---------|---------|
| `-m 0` | Reserved blocks percentage (default 5%) | `mkfs.ext4 -m 0 /dev/vg/lv` |
| `-O ^has_journal` | Disable journal (recovery, not recommended) | `-O ^has_journal` |
| `-E stride=...` | RAID stripe optimisation | `-E stride=64,stripe_width=128` |
| `-N inodes` | Number of inodes | `-N 500000` |

**Format example:**
```bash
mkfs.ext4 -m 1 -E stride=64 -L mydata /dev/vg/lv
```

**Resize ext4:**
```bash
# Grow (while mounted)
sudo resize2fs /dev/vg/lv     # after lvextend -r

# Shrink (must be unmounted)
sudo umount /mnt/point
sudo e2fsck -f /dev/vg/lv
sudo resize2fs /dev/vg/lv 8G
sudo lvreduce -L 8G /dev/vg/lv
sudo mount /dev/vg/lv /mnt/point
```

### 5.3 Formatting with `mkfs` – General Notes

- Use `blkid` to confirm UUID after formatting.
- Use `mkfs.xfs -f` to force overwrite (if previous signatures exist).
- For ext4, you can set a label with `-L`.

---

## 6. Mounting and `/etc/fstab`

### 6.1 Manual Mount – `mount` Options

**Syntax:** `mount [-t type] [-o options] device mountpoint`

**Common options:**

| Option | Meaning |
|--------|---------|
| `-t ext4` | Specify file system type |
| `-o ro` | Read‑only |
| `-o rw` | Read‑write |
| `-o noexec` | Disallow execution of binaries |
| `-o nosuid` | Ignore SUID bits |
| `-o nodev` | Ignore device files |
| `-o relatime` | Update access times less frequently (default) |
| `-o noatime` | No access time updates (performance) |
| `-o remount` | Change options on an already mounted FS |
| `-o loop` | Mount a file as a loop device |

**Examples:**
```bash
# Mount with noexec (cannot run binaries)
sudo mount -o noexec /dev/vg/lv /mnt/secure

# Remount as read‑only
sudo mount -o remount,ro /mnt/point

# Mount ISO file
sudo mount -o loop /path/to/image.iso /mnt/iso
```

### 6.2 Unmounting and Troubleshooting

```bash
sudo umount /mnt/point
sudo umount /dev/vg/lv
```

**If device is busy:** find the offender
```bash
lsof /mnt/point
fuser -v /mnt/point

# Kill processes using the mount
sudo fuser -km /mnt/point
sudo umount /mnt/point
```

### 6.3 The `/etc/fstab` File – Fields and Examples

Each line: `<device> <mountpoint> <fstype> <options> <dump> <pass>`

- **`device`** – often `UUID=...` (persistent). Also `LABEL=...` or `/dev/vg/lv`.
- **`options`** – comma‑separated (e.g., `defaults,noatime`).
- **`dump`** – 0 (ignore) or 1 (backup by dump utility).
- **`pass`** – fsck order. 0 = skip, 1 = root, 2 = other. XFS should be 0.

**Example entries:**
```
UUID=1234-5678-90ab-cdef  /boot  xfs   defaults        0 0
UUID=abcd-efgh-ijkl-mnop  /      xfs   defaults,noatime 0 0
/dev/vg_data/lv_home      /home  ext4  defaults        0 2
//192.168.1.5/share       /mnt/nfs nfs  defaults,_netdev 0 0
```

**Test after editing:** `sudo mount -a` (mounts all entries not yet mounted).

---

## 7. Disk Space Management – `df` and `du`

### 7.1 `df` – Report File System Disk Space

| Option | Meaning | Example |
|--------|---------|---------|
| `-h` | Human‑readable (MiB/GiB) | `df -h` |
| `-T` | Show file system type | `df -T` |
| `-i` | Show inode usage | `df -i` |
| `-x type` | Exclude FS type (e.g., `-x tmpfs`) | `df -x tmpfs` |
| `--total` | Show total line | `df -h --total` |
| `-t type` | Only show specific type | `df -t xfs` |
| `-B` | Block size (e.g., `-B 1M`) | `df -B 1G` |
| `-l` | Local file systems only | `df -l` |
| `-P` | POSIX output (no line breaks) | `df -P` |

**Examples:**
```bash
df -hT                      # human‑readable with type
df -i /home                 # inode usage of /home
df -x tmpfs --total         # exclude tmpfs and show total
```

### 7.2 `du` – Estimate File/Directory Space

| Option | Meaning | Example |
|--------|---------|---------|
| `-h` | Human‑readable | `du -h /home` |
| `-s` | Summary (total only) | `du -sh /var/log` |
| `-a` | Show all files, not just directories | `du -ah ~` |
| `-c` | Grand total | `du -ch *.log` |
| `-d N` | Max depth (`--max-depth=N`) | `du -h --max-depth=1 /home` |
| `-t size` | Show only entries larger than size (e.g., `-t 100M`) | `du -t 1G /data` |
| `--apparent-size` | Size as used by applications (not disk usage) | `du --apparent-size -sh *` |

**Examples:**
```bash
# Find top 5 largest directories in /home
du -sh /home/* | sort -hr | head -5

# Show size of current directory with depth 2
du -h --max-depth=2 | sort -hr
```

---

## 8. RAID – Redundant Array of Independent Disks

### 8.1 Core Concepts

- **Striping** – Data split across disks (performance).
- **Mirroring** – Data duplicated on two or more disks (redundancy).
- **Parity** – Mathematical checksum (e.g., XOR) to rebuild lost data.

### 8.2 RAID Levels

| Level | Description | Min disks | Capacity | Fault tolerance |
|-------|-------------|-----------|----------|----------------|
| 0 | Striping | 2 | Sum of all disks (100%) | None (one disk fails → all lost) |
| 1 | Mirroring | 2 | 50% (half capacity) | 1 disk |
| 5 | Striping + distributed parity | 3 | (N-1) disks | 1 disk |
| 10 | Mirrored stripes (1+0) | 4 | 50% | 1 disk per mirror |

### 8.3 Implementation: Software RAID (`mdadm`) and LVM RAID

**Software RAID with `mdadm` (example RAID 1):**
```bash
# Create RAID 1 array
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# Create filesystem
sudo mkfs.xfs /dev/md0

# Mount
sudo mount /dev/md0 /mnt/raid

# Save configuration
sudo mdadm --detail --scan >> /etc/mdadm/mdadm.conf

# Examine array
sudo mdadm --detail /dev/md0
```

**LVM RAID** – use `lvconvert`:
```bash
# Assume existing LV on single disk
sudo lvconvert --type raid1 --mirrors 1 /dev/vg_data/lv_data
```

**Replace failed disk in RAID 1 (mdadm):**
```bash
# Fail the faulty disk
sudo mdadm /dev/md0 --fail /dev/sdb1
sudo mdadm /dev/md0 --remove /dev/sdb1

# Add new disk partition
sudo mdadm /dev/md0 --add /dev/sdd1
```

---

## 9. Important Disk Utilities – Comprehensive

### 9.1 `lsblk` – List Block Devices

| Option | Meaning |
|--------|---------|
| `-f` | Show file system info (type, UUID, mount point) |
| `-m` | Show owner, group, mode |
| `-o` | Specify columns (e.g., `NAME,SIZE,TYPE,MOUNTPOINT`) |
| `-l` | Use list format (no tree) |
| `-p` | Show full device paths |
| `-J` | JSON output |

**Examples:**
```bash
lsblk -f
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,UUID
lsblk -J /dev/sda
```

### 9.2 `blkid` – Show Block Device Attributes

```bash
sudo blkid /dev/sda1
# Output: /dev/sda1: UUID="..." TYPE="xfs" PARTUUID="..."
```

**Options:**
- `-s` – Only show specific tag (e.g., `-s UUID`)
- `-p` – Probe (low‑level)
- `-o value` – Output only the value

**Examples:**
```bash
sudo blkid -s UUID -o value /dev/sda1   # prints UUID only
```

### 9.3 Partitioning Tools – `fdisk` and `gdisk` (Extended)

**Interactive commands inside `fdisk` / `gdisk`:**
- `m` – help
- `p` – print partition table
- `n` – new partition
- `d` – delete partition
- `t` – change partition type code (fdisk: `8e` for LVM; gdisk: `8E00`)
- `w` – write changes
- `q` – quit without saving
- `o` – create new empty partition table (GPT in gdisk, DOS in fdisk)

**Example – create a 10GB LVM partition using `fdisk`:**
```bash
sudo fdisk /dev/sdb
# Command: n (new), p (primary), 1 (first), accept defaults, then +10G
# Command: t (type), 8e (Linux LVM)
# Command: w
sudo partprobe /dev/sdb
```

---

## 10. Searching for Files – `locate` vs `find`

### 10.1 `locate` – Fast Database Search

- Uses database `/var/lib/mlocate/mlocate.db`.
- Updated daily via cron (`updatedb`). Manual update: `sudo updatedb`.
- Searches by **filename or path only**, not metadata.

**Options:**

| Option | Meaning |
|--------|---------|
| `-i` | Case‑insensitive |
| `-l N` | Limit output to N lines |
| `-r regex` | Use regular expression |
| `-0` | Null‑separated (for `xargs -0`) |
| `-c` | Count matches |
| `-b` | Match only basename (no path) |

**Examples:**
```bash
locate .conf                # find all .conf files
locate -i nginx.conf
locate -r '\.conf$'         # regex: files ending with .conf
locate -c .conf             # count
locate -b "ssh_config"      # exact basename
```

### 10.2 `find` – Real‑time, Metadata Search

**Syntax:** `find [path...] [expression]`

**Tests (conditions):**

| Test | Meaning | Example |
|------|---------|---------|
| `-name pattern` | Case‑sensitive name | `find / -name "*.conf"` |
| `-iname pattern` | Case‑insensitive | `find . -iname "readme*"` |
| `-type f` / `d` / `l` | File type | `find /home -type d -name ".*"` |
| `-size [+-]N[cwbkMG]` | Size (c=bytes, k=KiB) | `find /var/log -size +100M` |
| `-mtime N` | Modified N days ago | `find . -mtime -7` (last 7 days) |
| `-mmin N` | Modified N minutes ago | `find . -mmin -60` |
| `-atime N` | Accessed N days ago | `find /tmp -atime +30` |
| `-ctime N` | Changed (metadata) N days ago | – |
| `-user name` | Owner | `find /home -user alice` |
| `-group name` | Group | `find /var -group www-data` |
| `-perm mode` | Exact permissions | `find / -perm 644` |
| `-perm -mode` | At least these bits | `find / -perm -4000` (SUID) |
| `-perm /mode` | Any of these bits | `find / -perm /6000` (SUID or SGID) |
| `-empty` | Empty file or directory | `find /tmp -empty` |
| `-links N` | Number of hard links | `find / -links 1` (files with only one link) |

**Actions:**

| Action | Meaning |
|--------|---------|
| `-print` | Print path (default) |
| `-ls` | `ls -l` style output |
| `-delete` | Delete matching files (use caution) |
| `-exec cmd {} \;` | Execute command once per result |
| `-exec cmd {} +` | Batch execution (more efficient) |
| `-ok cmd {} \;` | Ask before execution |

**Examples:**

```bash
# Find empty files in /var/log
find /var/log -type f -empty

# Find files modified in last hour
find ~ -type f -mmin -60

# Find and delete core dumps older than 7 days
find / -name "core.*" -mtime +7 -delete

# Find files larger than 500MB and list with size
find /home -type f -size +500M -exec ls -lh {} \;

# Find SUID binaries owned by root
find / -type f -user root -perm -4000 2>/dev/null

# Find .tmp files and remove interactively
find . -name "*.tmp" -ok rm {} \;

# Batch chmod (efficient)
find . -type f -name "*.sh" -exec chmod +x {} +

# Find and tar archive (using -print0 for safety)
find /data -name "*.log" -print0 | tar -czvf logs.tar.gz --null -T -
```

**Performance tips:**
- Do not start from `/` unless necessary; use specific directories.
- Use `-maxdepth N` to limit recursion.
- Redirect stderr (`2>/dev/null`) to avoid permission errors.

---

## 11. Additional Important Notes

### 11.1 UUID (Universally Unique Identifier)

- Stored in file system superblock (or LVM metadata).
- Persistent across reboots and device reordering.
- Recommended over device names in `/etc/fstab`.
- Get UUID: `blkid /dev/sda1` or `lsblk -f`.

### 11.2 Creation Size vs. Actual Size

- **Creation size** – logical size of an LV (e.g., `-L 10G`).
- **Actual size** – physical space allocated. For thin LVs, actual may be smaller.
- Use `lvs -a -o lv_name,size,data_percent` to see thin pool usage.
- For regular LVs, logical size = allocated size.

---

## 12. Quick Reference Table

| Task | Command |
|------|---------|
| List block devices | `lsblk -f` |
| Show UUID of a device | `blkid /dev/sda1` |
| Partition (GPT interactive) | `sudo gdisk /dev/sdb` |
| Partition (MBR interactive) | `sudo fdisk /dev/sdb` |
| Reload partition table | `sudo partprobe /dev/sdb` |
| Create PV | `sudo pvcreate /dev/sdb1` |
| List PVs | `pvs`, `pvdisplay` |
| Create VG | `sudo vgcreate vg_name /dev/sdb1` |
| List VGs | `vgs`, `vgdisplay` |
| Create LV | `sudo lvcreate -n lv_name -L 10G vg_name` |
| Extend LV + FS | `sudo lvextend -r -L +5G /dev/vg/lv` |
| Shrink ext4 (unmounted) | `umount; e2fsck -f; resize2fs; lvreduce` |
| Format XFS | `sudo mkfs.xfs /dev/vg/lv` |
| Mount manually | `sudo mount /dev/vg/lv /mnt/point` |
| Unmount | `sudo umount /mnt/point` |
| Check open files on mount | `lsof /mnt/point`, `fuser -v /mnt/point` |
| Show disk usage | `df -hT` |
| Show directory size | `du -sh /home` |
| Find directories > 1GB | `du -t 1G /` |
| Locate file (fast) | `locate .conf` |
| Find by name | `find / -name "*.conf" 2>/dev/null` |
| Find by size | `find / -size +100M` |
| Execute on found files | `find . -name "*.tmp" -exec rm {} \;` |
| Create software RAID 1 | `mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1` |
| Check RAID status | `mdadm --detail /dev/md0` |

---

## 13. Practice Lab – Verify Your Understanding

1. **Explore your system:** Run `lsblk -f`. Identify the root file system type (XFS or ext4). Note all mounted partitions and their UUIDs.
2. **Add a virtual disk** (e.g., 5GiB) in your VM/cloud environment. Partition it with `gdisk` as a single LVM partition (`8E00`).
3. **Create LVM stack:** `pvcreate` → `vgcreate` → `lvcreate -n lv_test -L 2G`.
4. **Format, mount, test:** `mkfs.xfs`, mount to `/mnt/test`, write a test file.
5. **Extend:** Use `vgextend` to add another partition (or another disk). Extend LV by +1G and grow the filesystem online.
6. **`/etc/fstab`:** Add entry using UUID, test with `mount -a`.
7. **Practice `find`:**  
   - Find all files in `/etc` modified in the last 7 days.  
   - Find all empty files in `/tmp`.  
   - Find all SUID binaries and save the list to a file.
8. **Practice `locate`:** Update database (`sudo updatedb`) and search for all `.repo` files.
9. **RAID simulation (if you have spare disks):** Create a RAID 1 array using `mdadm`, format, mount, then simulate a disk failure and recover.
10. **Clean up:** Remove test partitions, LV, VG, PV.

---

## 14. Real‑World Scenario – Setting Up Storage for a Database Server

### Background

You are provisioning a new database server for a PostgreSQL deployment. The server has a system disk (`/dev/sda`) already in use. Two additional 20 GB disks (`/dev/sdb` and `/dev/sdc`) have been attached for database storage. You must prepare them using LVM and XFS, mount them persistently, and then extend the volume when more space is needed. Finally, you need to locate large log files and clean up old data.

### Step‑by‑Step Implementation

#### 1. Inspect the current disk layout
```bash
lsblk -f
sudo pvs; sudo vgs; sudo lvs   # see existing LVM (if any)
fdisk -l /dev/sdb /dev/sdc    # check for existing partition tables
```

#### 2. Create GPT partitions on both new disks
```bash
sudo gdisk /dev/sdb
# o (new GPT), n (new partition, use entire disk, type code 8E00 for Linux LVM), w (write)
sudo gdisk /dev/sdc
# same as above
sudo partprobe /dev/sdb /dev/sdc   # inform kernel
```

#### 3. Create Physical Volumes
```bash
sudo pvcreate /dev/sdb1 /dev/sdc1
pvs --units g
```

#### 4. Create a Volume Group for the database
```bash
sudo vgcreate vg_db /dev/sdb1 /dev/sdc1
vgs vg_db
```

#### 5. Create a Logical Volume for data files (16 GB initially)
```bash
sudo lvcreate -n lv_data -L 16G vg_db
lvs vg_db/lv_data
```

#### 6. Format the Logical Volume with XFS
```bash
sudo mkfs.xfs -L DB_DATA /dev/vg_db/lv_data
sudo blkid /dev/vg_db/lv_data   # note UUID
```

#### 7. Create a mount point and mount manually
```bash
sudo mkdir -p /var/lib/pgsql/data
sudo mount /dev/vg_db/lv_data /var/lib/pgsql/data
```

#### 8. Add entry to `/etc/fstab` for automatic mounting at boot
```bash
# Retrieve UUID
UUID=$(sudo blkid -s UUID -o value /dev/vg_db/lv_data)
echo "UUID=$UUID  /var/lib/pgsql/data  xfs  defaults,noatime  0 0" | sudo tee -a /etc/fstab
sudo mount -a    # test without reboot
df -h /var/lib/pgsql/data
```

#### 9. Simulate database growth – extend the LV and filesystem online
Assume the database grows and you need 4 GB more space:
```bash
sudo lvextend -r -L +4G /dev/vg_db/lv_data   # -r resizes XFS automatically
df -h /var/lib/pgsql/data   # verify new size is 20 GB
```

#### 10. Check disk usage and find large directories
```bash
df -hT /var/lib/pgsql/data
du -sh /var/lib/pgsql/* | sort -hr
```

#### 11. Locate archive logs older than 30 days and delete them (simulated)
```bash
sudo find /var/lib/pgsql/data/pg_wal -name "*.backup" -mtime +30 -delete
# Or use -exec ls -lh {} \; for verification first
```

#### 12. Use `find` to identify large core dumps (if any) and remove them
```bash
sudo find /var/lib/pgsql/data -name "core.*" -size +100M -exec ls -lh {} \;
# If safe, rm them: sudo find ... -exec rm {} \;
```

#### 13. Practice `locate` to quickly find PostgreSQL configuration files (after `updatedb`)
```bash
sudo updatedb
locate -i postgresql.conf
locate -b "pg_hba.conf"
```

#### 14. (Optional) Create a snapshot of the LV before a major migration
```bash
sudo lvcreate -s -n lv_data_snap -L 2G /dev/vg_db/lv_data
# Mount snapshot temporarily to verify data
sudo mkdir /mnt/snap
sudo mount -o ro /dev/vg_db/lv_data_snap /mnt/snap
ls /mnt/snap
sudo umount /mnt/snap
sudo lvremove -f /dev/vg_db/lv_data_snap
```

### Verification Checklist

- [ ] `lsblk -f` shows `vg_db-lv_data` mounted on `/var/lib/pgsql/data` with XFS.
- [ ] `/etc/fstab` entry exists with correct UUID.
- [ ] `mount -a` completes without errors.
- [ ] `df -h` reports 20 GB after extension.
- [ ] `pvs`, `vgs`, `lvs` display correct sizes and usage.
- [ ] `find` commands correctly identify and remove targeted files.
- [ ] `locate` returns configuration files quickly.

---

**Date documented:** 2026-05-04  
**Sources:** Red Hat System Administration, LVM documentation, `find`/`locate` man pages, `xfs`/`ext4` documentation