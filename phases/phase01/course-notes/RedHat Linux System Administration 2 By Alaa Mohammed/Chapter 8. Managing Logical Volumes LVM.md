# Chapter 8: Managing Logical Volumes (LVM)


## Table of Contents

- [Chapter 8: Managing Logical Volumes (LVM)](#chapter-8-managing-logical-volumes-lvm)
  - [Table of Contents](#table-of-contents)
  - [1. Why LVM? – Problems Solved](#1-why-lvm--problems-solved)
  - [2. LVM Architecture: PV, VG, LV](#2-lvm-architecture-pv-vg-lv)
    - [2.1 Physical Volume (PV)](#21-physical-volume-pv)
    - [2.2 Volume Group (VG)](#22-volume-group-vg)
    - [2.3 Logical Volume (LV)](#23-logical-volume-lv)
    - [2.4 Physical Extents (PE) and Logical Extents (LE)](#24-physical-extents-pe-and-logical-extents-le)
  - [3. Creating LVM Components Step‑by‑Step](#3-creating-lvm-components-stepbystep)
    - [3.1 Creating Physical Volumes](#31-creating-physical-volumes)
    - [3.2 Creating Volume Groups](#32-creating-volume-groups)
    - [3.3 Creating Logical Volumes](#33-creating-logical-volumes)
    - [3.4 Creating a File System and Mounting](#34-creating-a-file-system-and-mounting)
  - [4. Viewing and Displaying LVM Information](#4-viewing-and-displaying-lvm-information)
  - [5. Extending Logical Volumes](#5-extending-logical-volumes)
    - [5.1 Extending the Logical Volume and File System Together (`-r`)](#51-extending-the-logical-volume-and-file-system-together--r)
    - [5.2 Manual Extension (LV then FS)](#52-manual-extension-lv-then-fs)
    - [5.3 Adding Physical Storage to a Volume Group](#53-adding-physical-storage-to-a-volume-group)
  - [6. Reducing (Shrinking) Logical Volumes](#6-reducing-shrinking-logical-volumes)
    - [6.1 Shrink ext4 (Unmounted)](#61-shrink-ext4-unmounted)
    - [6.2 XFS Cannot Be Shrunk](#62-xfs-cannot-be-shrunk)
  - [7. Removing Logical Volumes, Volume Groups, Physical Volumes](#7-removing-logical-volumes-volume-groups-physical-volumes)
  - [8. LVM Snapshots](#8-lvm-snapshots)
    - [8.1 Creating a Snapshot](#81-creating-a-snapshot)
    - [8.2 Merging a Snapshot (Reverting)](#82-merging-a-snapshot-reverting)
    - [8.3 Removing a Snapshot](#83-removing-a-snapshot)
  - [9. LVM Thin Provisioning (Thin Pool \& Thin Volumes)](#9-lvm-thin-provisioning-thin-pool--thin-volumes)
    - [9.1 Creating a Thin Pool](#91-creating-a-thin-pool)
    - [9.2 Creating Thin Volumes](#92-creating-thin-volumes)
    - [9.3 Monitoring Thin Pool Usage](#93-monitoring-thin-pool-usage)
  - [10. LVM RAID – Integrated RAID Functionality](#10-lvm-raid--integrated-raid-functionality)
    - [10.1 Creating a RAID Logical Volume](#101-creating-a-raid-logical-volume)
    - [10.2 Converting an Existing LV to RAID](#102-converting-an-existing-lv-to-raid)
    - [10.3 Checking RAID Status](#103-checking-raid-status)
  - [11. LVM Cache Volumes (Advanced)](#11-lvm-cache-volumes-advanced)
  - [12. Troubleshooting and Recovery](#12-troubleshooting-and-recovery)
    - [12.1 Missing Volume Group](#121-missing-volume-group)
    - [12.2 Failed Physical Volume (`vgreduce --removemissing`)](#122-failed-physical-volume-vgreduce---removemissing)
  - [13. Quick Reference Table](#13-quick-reference-table)
  - [14. Practice Lab – Verify Your Understanding](#14-practice-lab--verify-your-understanding)

---

## 1. Why LVM? – Problems Solved

Traditional disk partitions have fixed sizes. When a partition runs out of space, you cannot easily expand it without moving data or repartitioning. LVM introduces an **indirection layer** that separates the logical view of storage from the physical hardware.

**Problems LVM solves:**

- **Inflexible partition sizes** – LVs can be resized online (grown) and, for ext4, even shrunk.
- **Difficulty adding new disks** – Add a new disk as a Physical Volume, extend the Volume Group, then allocate space to any Logical Volume.
- **No snapshots** – LVM provides copy‑on‑write snapshots for consistent backups.
- **No striping / mirroring** – LVM can combine disks for performance (striping) or redundancy (mirroring).

---

## 2. LVM Architecture: PV, VG, LV

```
Physical Storage → Physical Volume (PV) → Volume Group (VG) → Logical Volume (LV) → File system
```

### 2.1 Physical Volume (PV)

- A disk or partition initialised for LVM usage.
- Metadata is stored at the beginning of the device (2nd sector).
- Commands: `pvcreate`, `pvs`, `pvdisplay`, `pvremove`, `pvmove`.

### 2.2 Volume Group (VG)

- A pool of storage composed of one or more PVs.
- Physical Extents (PEs) are fixed‑size chunks (default 4 MiB) managed by the VG.
- Commands: `vgcreate`, `vgs`, `vgdisplay`, `vgextend`, `vgreduce`, `vgremove`.

### 2.3 Logical Volume (LV)

- A virtual block device carved from a VG‘s free extents.
- Appears as `/dev/vg_name/lv_name` or `/dev/mapper/vg_name-lv_name`.
- Commands: `lvcreate`, `lvs`, `lvdisplay`, `lvextend`, `lvreduce`, `lvremove`.

### 2.4 Physical Extents (PE) and Logical Extents (LE)

- PE: smallest allocatable unit on a PV (default 4 MiB, set with `vgcreate -s`).
- LE: same size as PE; mapping of LE to PE is stored in VG metadata.
- Allows LVs to be striped, mirrored, or spread across PVs.

---

## 3. Creating LVM Components Step‑by‑Step

### 3.1 Creating Physical Volumes

Assumption: you have raw partitions or whole disks, e.g., `/dev/sdb1`, `/dev/sdc`.

```bash
# Initialize a partition as a PV
sudo pvcreate /dev/sdb1

# Initialize a whole disk (no partition table) – works but not recommended for boot disks
sudo pvcreate /dev/sdc

# View PVs
sudo pvs
sudo pvdisplay /dev/sdb1
```

### 3.2 Creating Volume Groups

```bash
# Create a VG named vg_data containing /dev/sdb1
sudo vgcreate vg_data /dev/sdb1

# Add another PV to an existing VG
sudo vgextend vg_data /dev/sdc

# View VGs
sudo vgs
sudo vgdisplay vg_data
```

### 3.3 Creating Logical Volumes

```bash
# Create a 5 GiB LV named lv_home in VG vg_data
sudo lvcreate -n lv_home -L 5G vg_data

# Create an LV using all remaining free space
sudo lvcreate -n lv_backup -l 100%FREE vg_data

# Create a striped LV across two PVs (better performance)
sudo lvcreate -n lv_striped --stripes 2 --stripesize 64K -L 10G vg_data

# Create a mirrored LV (RAID1)
sudo lvcreate --type raid1 -n lv_mirror -L 5G vg_data

# View LVs
sudo lvs
sudo lvdisplay /dev/vg_data/lv_home
```

### 3.4 Creating a File System and Mounting

```bash
# Format with XFS (default)
sudo mkfs.xfs /dev/vg_data/lv_home

# Or ext4
sudo mkfs.ext4 /dev/vg_data/lv_home

# Mount temporarily
sudo mkdir -p /mnt/home
sudo mount /dev/vg_data/lv_home /mnt/home
```

Add to `/etc/fstab` for persistence:

```
/dev/vg_data/lv_home   /mnt/home   xfs   defaults   0 0
```

---

## 4. Viewing and Displaying LVM Information

| Command | Purpose |
|---------|---------|
| `pvs` | Short summary of PVs |
| `pvdisplay` | Detailed PV information |
| `vgs` | Short summary of VGs |
| `vgdisplay` | Detailed VG information |
| `lvs` | Short summary of LVs |
| `lvdisplay` | Detailed LV information |
| `lvmdiskscan` | List all devices LVM can use |
| `lvscan` / `vgscan` | Scan for existing LVs/VGs |

**Examples:**

```bash
pvs --units g    # show sizes in gigabytes
vgs -o vg_name,size,free  # custom columns
lvs -o lv_name,vg_name,size,attr
```

---

## 5. Extending Logical Volumes

### 5.1 Extending the Logical Volume and File System Together (`-r`)

The simplest method – extends the LV and resizes the file system in one command.

```bash
# Extend by 2 GiB
sudo lvextend -r -L +2G /dev/vg_data/lv_home

# Extend to an absolute size of 10 GiB
sudo lvextend -r -L 10G /dev/vg_data/lv_home
```

### 5.2 Manual Extension (LV then FS)

If you prefer separate steps:

```bash
# Extend LV first
sudo lvextend -L +2G /dev/vg_data/lv_home

# Then resize file system
# For XFS (mounted)
sudo xfs_growfs /mnt/home

# For ext4 (mounted)
sudo resize2fs /dev/vg_data/lv_home
```

### 5.3 Adding Physical Storage to a Volume Group

When a VG runs out of free space, add a new disk or partition.

```bash
# Add a new PV
sudo pvcreate /dev/sdd1

# Extend the VG
sudo vgextend vg_data /dev/sdd1

# Now you can extend any LV as shown above
```

---

## 6. Reducing (Shrinking) Logical Volumes

**Important:** XFS **cannot** be shrunk. Only **ext4** can be shrunk offline (unmounted).

### 6.1 Shrink ext4 (Unmounted)

```bash
# Unmount the file system
sudo umount /mnt/home

# Check the file system
sudo e2fsck -f /dev/vg_data/lv_home

# Shrink the file system to 5 GiB
sudo resize2fs /dev/vg_data/lv_home 5G

# Shrink the LV to match (or slightly larger)
sudo lvreduce -L 5G /dev/vg_data/lv_home

# Remount
sudo mount /dev/vg_data/lv_home /mnt/home
```

### 6.2 XFS Cannot Be Shrunk

If you need shrinkable storage, choose ext4. For XFS, you must backup, delete, recreate smaller LV, and restore.

---

## 7. Removing Logical Volumes, Volume Groups, Physical Volumes

```bash
# Remove a logical volume (must be unmounted first)
sudo lvremove /dev/vg_data/lv_home

# Remove a volume group (after all LVs are removed)
sudo vgremove vg_data

# Remove a physical volume (after removing from any VG)
sudo pvremove /dev/sdb1
```

---

## 8. LVM Snapshots

Snapshots are **copy‑on‑write** LVs that capture the state of an original LV at a point in time. They are useful for consistent backups.

### 8.1 Creating a Snapshot

```bash
# Create a snapshot of lv_home (size 1 GiB – will hold changes)
sudo lvcreate -s -n lv_home_snap -L 1G /dev/vg_data/lv_home

# The snapshot appears as /dev/vg_data/lv_home_snap
```

- The snapshot size limits how many changes can be recorded. If it fills up, the snapshot becomes invalid (`INACTIVE`).
- While the snapshot exists, writes to the original LV cause old data to be copied to the snapshot area.

### 8.2 Merging a Snapshot (Reverting)

```bash
# Merge the snapshot back into the original LV (reverts changes)
sudo lvconvert --merge /dev/vg_data/lv_home_snap
```

After merging, the snapshot is automatically removed.

### 8.3 Removing a Snapshot

```bash
sudo lvremove /dev/vg_data/lv_home_snap
```

---

## 9. LVM Thin Provisioning (Thin Pool & Thin Volumes)

Thin provisioning allows you to create **virtual** LVs that appear larger than the actual physical storage allocated. Suitable for over‑committing storage across many volumes.

### 9.1 Creating a Thin Pool

```bash
# Create a thin pool of 10 GiB (physical size)
sudo lvcreate -L 10G -T vg_data/thin_pool
```

### 9.2 Creating Thin Volumes

```bash
# Create a thin LV with virtual size 1 TiB (only consumes what is written)
sudo lvcreate -V 1T -T vg_data/thin_pool -n lv_thin1
```

### 9.3 Monitoring Thin Pool Usage

```bash
lvs -a -o lv_name,size,data_percent,metadata_percent vg_data
```

If `data_percent` reaches 100%, writes will fail. Extend the thin pool:

```bash
sudo lvextend -L +2G vg_data/thin_pool
```

---

## 10. LVM RAID – Integrated RAID Functionality

LVM can create RAID LVs (levels 0, 1, 4, 5, 6, 10) using the kernel `md` subsystem but managed entirely with LVM commands.

### 10.1 Creating a RAID Logical Volume

```bash
# RAID1 (mirror) with 2 legs
sudo lvcreate --type raid1 -n lv_mirror1 -L 5G vg_data

# RAID5 (striped with parity) with 3 PVs in VG
sudo lvcreate --type raid5 -n lv_raid5 -L 10G -i 3 vg_data
```

### 10.2 Converting an Existing LV to RAID

```bash
# Convert a linear LV to RAID1
sudo lvconvert --type raid1 /dev/vg_data/lv_linear
```

### 10.3 Checking RAID Status

```bash
sudo lvs -a -o name,attr,size,raid_sync_action,raid_mismatch_count
```

---

## 11. LVM Cache Volumes (Advanced)

LVM cache uses a fast SSD as a cache for a slower HDD LV. This is covered in advanced chapters but briefly:

```bash
# Create cache pool LV (fast disk)
# Then attach to main LV
sudo lvconvert --type cache --cachepool vg_data/cache_pool vg_data/lv_slow
```

---

## 12. Troubleshooting and Recovery

### 12.1 Missing Volume Group

If LVs disappear after rebooting or moving disks, rescan:

```bash
sudo vgscan
sudo vgchange -ay   # activate all VGs
```

### 12.2 Failed Physical Volume (`vgreduce --removemissing`)

If a PV fails and you cannot replace it, remove it from the VG (data on that PV will be lost):

```bash
sudo vgreduce --removemissing vg_data
```

To replace a failed PV while keeping data (if redundancy exists, e.g., RAID1):

```bash
# Add a new PV
sudo pvcreate /dev/sde1
# Replace the failed PV
sudo vgreduce --removemissing --mirrorlog thin vg_data
# Then mirror using lvconvert
```

---

## 13. Quick Reference Table

| Task | Command |
|------|---------|
| Create a PV | `sudo pvcreate /dev/sdb1` |
| List PVs | `pvs`, `pvdisplay` |
| Create VG | `sudo vgcreate vg_name /dev/sdb1` |
| List VGs | `vgs`, `vgdisplay` |
| Extend VG | `sudo vgextend vg_name /dev/sdc1` |
| Reduce VG (remove PV) | `sudo vgreduce vg_name /dev/sdb1` |
| Create LV (linear) | `sudo lvcreate -n lv_name -L 5G vg_name` |
| Create LV (striped) | `sudo lvcreate -i2 -I64 -n lv_name -L 10G vg_name` |
| Extend LV (+2G) | `sudo lvextend -r -L +2G /dev/vg_name/lv_name` |
| Extend LV to size | `sudo lvextend -r -L 10G /dev/vg_name/lv_name` |
| Shrink ext4 LV | (unmount, e2fsck, resize2fs, lvreduce) |
| Remove LV | `sudo lvremove /dev/vg_name/lv_name` |
| Remove VG | `sudo vgremove vg_name` |
| Remove PV | `sudo pvremove /dev/sdb1` |
| Create snapshot | `sudo lvcreate -s -n snap -L 1G /dev/vg_name/lv_name` |
| Merge snapshot | `sudo lvconvert --merge /dev/vg_name/snap` |
| Create thin pool | `sudo lvcreate -L 10G -T vg_name/thin_pool` |
| Create thin LV | `sudo lvcreate -V 100G -T vg_name/thin_pool -n thin_lv` |
| Create RAID1 LV | `sudo lvcreate --type raid1 -n mirror -L 5G vg_name` |
| Activate all VGs | `sudo vgchange -ay` |
| Scan for VGs | `sudo vgscan` |

---

## 14. Practice Lab – Verify Your Understanding

1. **Create a test environment** with two 5 GiB virtual disks (`/dev/sdb`, `/dev/sdc`). Ensure they are empty.

2. **Create a VG named `vg_test`** using two partitions (or whole disks). Create one 3 GiB LV named `lv_test` and format as XFS. Mount it under `/mnt/test`.

3. **Write a large file** inside the mount point (`dd if=/dev/zero of=/mnt/test/bigfile bs=1M count=500`).

4. **Extend** the LV by 1 GiB (online) and verify the file system grew using `df -h`.

5. **Add another disk** (`/dev/sdd`) as a PV, extend the VG, then extend the LV again.

6. **Create a snapshot** of `lv_test` (1 GiB size). Modify some files in the original LV, then merge the snapshot to revert. Verify the revert.

7. **Thin provisioning** (if you have enough space) – create a thin pool of 2 GiB, then create two thin LVs of 10 GiB each. Observe that `lvs` shows `data_percent` low.

8. **Clean up** – remove all LVs, VG, and PVs.

---

**Date documented:** 2026-05-10  
**Sources:** Red Hat Enterprise Linux 9 Logical Volume Manager Administration, LVM man pages

---
