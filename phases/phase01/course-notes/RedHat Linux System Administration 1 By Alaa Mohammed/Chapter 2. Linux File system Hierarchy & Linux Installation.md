Here is your **pro markdown version** of the notes. You can save this as `phases/phase01/topics-notes/linux-filesystem-hierarchy.md`

---

# Linux File System Hierarchy & Installation

## What is a File System?

A file system is a built‑in OS layer used to manage and organize disk storage. It handles:
- File naming
- File size
- Indexing of data

---

## How File Systems Differ

| Feature | Description |
|---------|-------------|
| **Size** | e.g., FAT16 supports up to 16 GB |
| **Naming** | Allowed characters, case sensitivity, length limits |
| **Security** | Permissions, ACLs, encryption |
| **Journaling** | Prevents data corruption after crashes |
| **OS Support** | Windows, Linux, macOS, etc. |

---

## Common Linux File Systems

- `ext2`
- `ext3`
- `ext4`
- `xfs`
- `zfs`

> 📺 Best video to understand file systems:  
> [File Systems - freeCodeCamp](https://www.youtube.com/watch?v=_h30HBYxtws&t=299s)

---

## Journaling File System

A journaling file system avoids data corruption by logging **all uncommitted changes** to a journal before they are written to disk.  
If power is lost, the system can recover quickly by replaying the journal.

✅ Example: `NTFS` (Windows) and `ext3`/`ext4` (Linux) support journaling.

---

## Linux File System Hierarchy (FHS)

Everything in Linux is a **file** – even directories, hard disks, and devices.

| Directory | Purpose |
|-----------|---------|
| `/` | Root directory – the top of the file system |
| `/bin` | Binaries (commands) available to normal users |
| `/sbin` | System binaries – commands for the root user |
| `/boot` | Boot loader and kernel |
| `/dev` | Device files (hard disks, USB, drivers) |
| `/etc` | Editable text configuration files (e.g., `dhcp`, `apache`) |
| `/home` | Home directories for normal users (e.g., `/home/alice`) |
| `/root` | Home directory for the `root` user |
| `/run` | Current running processes (temporary, in memory) |
| `/tmp` | Temporary files – cleared on reboot |
| `/usr` | Installed packages and applications |
| `/var` | Variable files: logs, databases, mail (size changes over time) |

---

## Swap Space

Swap is space on a hard disk used when **RAM is full**.  
Inactive processes are moved from RAM → swap to free memory.

- **Old systems**: swap was a dedicated partition  
- **Modern systems**: swap is usually a file

### How to Choose Swap Size (recommended)

| RAM Size | Swap Size |
|----------|-----------|
| Less than 16 GB | `2 × RAM` |
| 16 GB or more | Depends on application requirements (e.g., 4–8 GB) |

> 💡 **Pro tip**: Enable **LVM** (Logical Volume Manager) during installation – it allows you to extend partitions later if they fill up.

### Useful Resources on Swap

- [Red Hat: Swap Space (RHEL 7)](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-swapspace)
- [YouTube: Swap Explained – Chris Titus Tech](https://www.youtube.com/watch?v=XqWD0bWDljw)
- [YouTube: Linux Swap – Mental Outlaw](https://www.youtube.com/watch?v=XTMyJ5l0GLg)

---

## Key Takeaways for Cloud Engineering

- Understanding the file system hierarchy helps you **navigate any Linux server** (EC2, containers, on‑prem).
- Journaling and swap knowledge is critical for **troubleshooting high‑memory EC2 instances**.
- LVM is used in cloud environments to **resize EBS volumes** without downtime.

---

## Practice Check

- [ ] I can list the purpose of `/etc`, `/var`, `/usr`, `/bin`
- [ ] I know when swap is used and how to check it (`free -h`, `swapon --show`)
- [ ] I can explain why journaling matters for cloud databases

---

**Date documented:** 2026-04-12  
**Source:** Linux Administration (Chapter 1 – File System Hierarchy & Installation)

---

Do you want me to add a **commands section** with `lsblk`, `df -h`, `du -sh`, and `free -h` as practical examples?