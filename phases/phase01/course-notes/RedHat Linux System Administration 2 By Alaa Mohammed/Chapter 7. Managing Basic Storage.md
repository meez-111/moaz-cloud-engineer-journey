# Chapter 7: Managing Basic Storage

---

## Table of Contents

- [Chapter 7: Managing Basic Storage](#chapter-7-managing-basic-storage)
  - [Table of Contents](#table-of-contents)
  - [1. Operations You Can Perform on a Disk](#1-operations-you-can-perform-on-a-disk)
  - [2. Scanning for Newly Connected Disks](#2-scanning-for-newly-connected-disks)
    - [2.1 Rescanning SCSI / SATA / SAS Buses](#21-rescanning-scsi--sata--sas-buses)
    - [2.2 Using `partprobe`](#22-using-partprobe)
    - [2.3 Using `udevadm settle`](#23-using-udevadm-settle)
    - [2.4 Reloading Systemd Device Units (`systemctl daemon-reload`)](#24-reloading-systemd-device-units-systemctl-daemon-reload)
  - [3. Working with Disk Partitions](#3-working-with-disk-partitions)
  - [4. Creating and Mounting File Systems](#4-creating-and-mounting-file-systems)
  - [5. Managing Swap Space](#5-managing-swap-space)
    - [5.1 Creating a Swap Partition](#51-creating-a-swap-partition)
    - [5.2 Creating a Swap File](#52-creating-a-swap-file)
    - [5.3 Enabling and Disabling Swap](#53-enabling-and-disabling-swap)
    - [5.4 Persistent Swap Configuration (`/etc/fstab`)](#54-persistent-swap-configuration-etcfstab)
  - [6. Persistent Mounts with `/etc/fstab`](#6-persistent-mounts-with-etcfstab)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [8. Practice Lab – Verify Your Understanding](#8-practice-lab--verify-your-understanding)

---

## 1. Operations You Can Perform on a Disk

From a system administrator’s perspective, the typical lifecycle of a disk in Linux involves the following operations:

| Step | Operation | Tools / Commands |
|------|-----------|------------------|
| 1 | **Detect / scan** the disk | `lsblk`, `fdisk -l`, `lsscsi`, `echo "- - -" > /sys/class/scsi_host/hostN/scan` |
| 2 | **Partition** the disk | `fdisk`, `gdisk`, `parted` |
| 3 | **Reload partition table** | `partprobe`, `udevadm settle` |
| 4 | **Create a file system** (format) | `mkfs.xfs`, `mkfs.ext4`, `mkswap` |
| 5 | **Mount** the file system (temporary) | `mount` |
| 6 | **Persistent mount** (at boot) | edit `/etc/fstab`, then `mount -a` |
| 7 | **Unmount** and **remove** (optional) | `umount`, remove partition entries |

---

## 2. Scanning for Newly Connected Disks

When you attach a new disk (physical or virtual) to a running system, it may not appear automatically. You must trigger a rescan of the storage buses.

### 2.1 Rescanning SCSI / SATA / SAS Buses

For SCSI‑based devices (including SATA and USB mass storage), each SCSI host adapter has a `scan` file.

First, list the existing SCSI hosts:

```bash
ls /sys/class/scsi_host/
# Example: host0  host1  host2 ...
```

Rescan each host:

```bash
for host in /sys/class/scsi_host/host*; do
    echo "- - -" | sudo tee "$host/scan"
done
```

- `- - -` means: scan all channels, all targets, all LUNs.

Alternatively, use the `rescan-scsi-bus` script (if installed from `scsi‑target‑utils`):

```bash
sudo rescan-scsi-bus
```

### 2.2 Using `partprobe`

`partprobe` (part of the `parted` package) informs the kernel about partition table changes **on existing disks**. It does not detect new disks, but after you have created/changed partitions, `partprobe` re‑reads the partition table without requiring a reboot.

```bash
sudo partprobe /dev/sdb
```

- Without a device argument, `partprobe` attempts to update all disks.

### 2.3 Using `udevadm settle`

After scanning or partitioning, `udevadm settle` waits until **all udev events** (device node creation, symlinks, permissions) have been processed. This ensures that subsequent commands (like `mkfs`) see the new device.

```bash
sudo udevadm settle
```

**Typical workflow:**

```bash
echo "- - -" > /sys/class/scsi_host/host0/scan
sudo udevadm settle
lsblk   # now the new disk should appear
```

### 2.4 Reloading Systemd Device Units (`systemctl daemon-reload`)

Systemd creates device units (`.device`) for many hardware devices. If you add a disk and it does not appear in `systemctl list-units --type=device`, you can force systemd to re‑probe hardware:

```bash
sudo systemctl daemon-reload
```

However, this is rarely needed for basic disks; `udevadm settle` is usually sufficient.

---

## 3. Working with Disk Partitions

Use `lsblk` to list block devices and `gdisk` (for GPT) or `fdisk` (for MBR/GPT) to partition.

**Example – create a single partition on `/dev/sdb` (GPT):**

```bash
sudo gdisk /dev/sdb
```

Inside `gdisk`:

- `o` – create new GPT table (will erase all data)
- `n` – new partition (accept defaults for partition number, first sector, last sector)
- `t` – change type to `8300` for Linux filesystem
- `w` – write changes

After writing, update the kernel:

```bash
sudo partprobe /dev/sdb
sudo udevadm settle
```

Verify:

```bash
lsblk /dev/sdb
```

---

## 4. Creating and Mounting File Systems

Format the partition (e.g., `/dev/sdb1`) with a file system.

```bash
# XFS (default in RHEL)
sudo mkfs.xfs /dev/sdb1

# or ext4
sudo mkfs.ext4 /dev/sdb1
```

**Mount temporarily:**

```bash
sudo mkdir -p /mnt/data
sudo mount /dev/sdb1 /mnt/data
```

Verify:

```bash
df -hT /mnt/data
mount | grep /mnt/data
```

---

## 5. Managing Swap Space

Swap space provides virtual memory when RAM is full. It can be a dedicated partition or a file.

### 5.1 Creating a Swap Partition

1. **Create a partition** of type `8200` (Linux swap) using `gdisk` or `fdisk`.
2. **Mark it as swap** and format:

   ```bash
   sudo mkswap /dev/sdb2
   ```

3. **Activate it**:

   ```bash
   sudo swapon /dev/sdb2
   ```

4. **Verify**:

   ```bash
   swapon --show
   free -h
   ```

### 5.2 Creating a Swap File

If you need additional swap without repartitioning:

```bash
# Create a 2 GiB file
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

To make it permanent, add entry to `/etc/fstab` (see below).

### 5.3 Enabling and Disabling Swap

| Command | Effect |
|---------|--------|
| `swapon /dev/sdb2` | Enable a specific swap area |
| `swapon -a` | Enable all swap areas listed in `/etc/fstab` |
| `swapon --show` | List active swap areas |
| `swapoff /dev/sdb2` | Disable a specific swap area |
| `swapoff -a` | Disable all swap |

### 5.4 Persistent Swap Configuration (`/etc/fstab`)

Add an entry to `/etc/fstab` for swap:

```
UUID=<swap-uuid>   none   swap   defaults   0 0
```

Get the UUID using `blkid /dev/sdb2`. Then test with:

```bash
sudo swapoff -a && sudo swapon -a
```

---

## 6. Persistent Mounts with `/etc/fstab`

To automatically mount a file system at boot, add a line to `/etc/fstab`. Use **UUID** instead of device names for stability.

```bash
sudo blkid /dev/sdb1
# Output: UUID="a1b2c3d4-..." ...
```

Add an entry:

```
UUID=a1b2c3d4-...   /mnt/data   xfs   defaults   0 0
```

After editing `fstab`, test without rebooting:

```bash
sudo mount -a
```

If no errors, the mount is ready for next boot.

---

## 7. Quick Reference Table

| Task | Command |
|------|---------|
| List all block devices | `lsblk` or `lsblk -f` |
| Show all disks (including unpartitioned) | `fdisk -l` (requires sudo) |
| Scan SCSI hosts for new disks | `echo "- - -" > /sys/class/scsi_host/hostN/scan` |
| Inform kernel about partition changes | `sudo partprobe /dev/sdb` |
| Wait for udev to process events | `sudo udevadm settle` |
| Reload systemd device units | `sudo systemctl daemon-reload` (rarely needed) |
| Partition a disk (GPT) | `sudo gdisk /dev/sdb` |
| Partition a disk (MBR) | `sudo fdisk /dev/sdb` |
| Create XFS file system | `sudo mkfs.xfs /dev/sdb1` |
| Create ext4 file system | `sudo mkfs.ext4 /dev/sdb1` |
| Create a swap partition | `sudo mkswap /dev/sdb2` |
| Enable swap | `sudo swapon /dev/sdb2` |
| Show swap status | `swapon --show` |
| Disable swap | `sudo swapoff /dev/sdb2` |
| Temporary mount | `sudo mount /dev/sdb1 /mount/point` |
| Unmount | `sudo umount /mount/point` |
| Test `/etc/fstab` entries | `sudo mount -a` |

---

## 8. Practice Lab – Verify Your Understanding

1. **Add a new virtual disk** of 5 GiB to your VM. Scan for it without rebooting. Confirm it appears as `/dev/sdc` (or similar) using `lsblk`.

2. **Partition** the new disk using GPT: create one partition of type `8300` (Linux filesystem) using `gdisk`. Write the table and run `partprobe`.

3. **Format** the partition as XFS. Mount it under `/mnt/storage` and create a test file.

4. **Add an extra partition** of 1 GiB of type `8200` (Linux swap). Use `mkswap` and `swapon`. Verify with `free -h` and `swapon --show`.

5. **Make both mounts permanent**:
   - For the data partition, add an entry in `/etc/fstab` using the UUID.
   - For the swap partition, also add an UUID‑based entry.
   - Test with `mount -a` and `swapon -a` after unmounting and swapping off.

6. **Clean up**: Unmount, remove entries from `/etc/fstab`, and delete the partitions using `gdisk`.

---

**Date documented:** 2026-05-10  
**Sources:** Red Hat Enterprise Linux 9 Storage Administration Guide, `partprobe(8)`, `udevadm(8)`, `systemctl(1)` man pages

---
