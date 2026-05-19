# Chapter 12: Controlling the Boot Process

## Table of Contents

- [Chapter 12: Controlling the Boot Process](#chapter-12-controlling-the-boot-process)
  - [Table of Contents](#table-of-contents)
  - [1. The Linux Booting Sequence – Step by Step](#1-the-linux-booting-sequence--step-by-step)
  - [2. Runlevels (SysV) and systemd Targets](#2-runlevels-sysv-and-systemd-targets)
    - [2.1 What are Runlevels? Why Were They Used?](#21-what-are-runlevels-why-were-they-used)
    - [2.2 systemd Targets (Modern Replacement)](#22-systemd-targets-modern-replacement)
    - [2.3 Comparison: Runlevels vs. Targets](#23-comparison-runlevels-vs-targets)
  - [3. Switching Between Targets (Runlevels)](#3-switching-between-targets-runlevels)
    - [3.1 Temporary Switch (`systemctl isolate`)](#31-temporary-switch-systemctl-isolate)
    - [3.2 Permanent Default Target (`systemctl set-default`)](#32-permanent-default-target-systemctl-set-default)
  - [4. Relation Between Targets and Installation Types](#4-relation-between-targets-and-installation-types)
  - [5. Systemd Unit Dependencies – `.wants` Directories](#5-systemd-unit-dependencies--wants-directories)
  - [6. Boot Files and Directories](#6-boot-files-and-directories)
    - [6.1 `/boot/` Directory Contents](#61-boot-directory-contents)
    - [6.2 GRUB2 Configuration (`/boot/grub2/grub.cfg`)](#62-grub2-configuration-bootgrub2grubcfg)
    - [6.3 `/etc/default/grub` – Kernel Boot Parameters](#63-etcdefaultgrub--kernel-boot-parameters)
    - [6.4 Generating a New GRUB2 Configuration (`grub2-mkconfig`)](#64-generating-a-new-grub2-configuration-grub2-mkconfig)
  - [7. Dracut – Initial RAM Disk (initramfs)](#7-dracut--initial-ram-disk-initramfs)
  - [8. Selecting a Different Kernel at Boot Time](#8-selecting-a-different-kernel-at-boot-time)
  - [9. Resetting the Root Password (`rd.break`)](#9-resetting-the-root-password-rdbreak)
    - [9.1 Method 1: Using `rd.break` at Boot](#91-method-1-using-rdbreak-at-boot)
    - [9.2 Method 2: Using `init=/bin/bash` (Legacy)](#92-method-2-using-initbinbash-legacy)
- [new and reliable password reset method](#new-and-reliable-password-reset-method)
  - [10. Secure Boot (UEFI) – Overview](#10-secure-boot-uefi--overview)
  - [11. Quick Reference Table](#11-quick-reference-table)
  - [12. Real‑World Scenario – Managing a Headless Server’s Boot Process](#12-realworld-scenario--managing-a-headless-servers-boot-process)
    - [Background](#background)
    - [Step 1 – Initial State and Temporary Switch](#step-1--initial-state-and-temporary-switch)
    - [Step 2 – Set Permanent Default](#step-2--set-permanent-default)
    - [Step 3 – Boot with a Specific Kernel and Custom Parameters](#step-3--boot-with-a-specific-kernel-and-custom-parameters)
    - [Step 4 – Reset Root Password with `rd.break`](#step-4--reset-root-password-with-rdbreak)
    - [Step 5 – Verify and Document](#step-5--verify-and-document)
  - [13. Practice Lab – Verify Your Understanding](#13-practice-lab--verify-your-understanding)

---

## 1. The Linux Booting Sequence – Step by Step

| Step | Component | What Happens |
|------|-----------|---------------|
| **1** | **Power‑on / Reset** | CPU starts executing firmware (BIOS or UEFI). |
| **2** | **BIOS / UEFI** | Performs POST, initialises hardware, locates boot device. |
| **3** | **Boot Loader (GRUB2)** | Loads from MBR or EFI System Partition. Displays menu, loads kernel and initramfs. |
| **4** | **Kernel** | Decompresses, initialises core subsystems, mounts **initramfs** temporarily. |
| **5** | **initramfs (initial RAM file system)** | Contains minimal drivers and `systemd` (dracut). Loads modules, discovers root file system (LVM, RAID, encryption). |
| **6** | **Switch Root** | Kernel unmounts initramfs and mounts the real root file system as `/`. |
| **7** | **systemd (PID 1)** | Starts all units according to the default target (e.g., `multi-user.target` or `graphical.target`). |
| **8** | **User Login** | Console or graphical login prompt appears. |

---

## 2. Runlevels (SysV) and systemd Targets

### 2.1 What are Runlevels? Why Were They Used?

In the **SysV init** system, runlevels were single‑digit states (0–6) defining which services were started.

| Runlevel | Purpose |
|----------|---------|
| 0 | Halt (shutdown) |
| 1 | Single‑user mode (rescue) |
| 2 | Multi‑user, no NFS (rarely used) |
| 3 | Full multi‑user (text mode) |
| 4 | Unused / custom |
| 5 | X11 (graphical) |
| 6 | Reboot |

### 2.2 systemd Targets (Modern Replacement)

systemd replaces runlevels with **targets** – named groups of units that can start in parallel.

**Most important targets:**

| Target | Equivalent Runlevel | Description |
|--------|--------------------|-------------|
| `poweroff.target` | 0 | Shut down and power off. |
| `rescue.target` | 1 | Single‑user mode with basic system, no networking. **Can be isolated.** |
| `multi-user.target` | 3 | Multi‑user, non‑graphical (text consoles). **Can be isolated.** |
| `graphical.target` | 5 | Multi‑user with graphical interface. **Can be isolated.** |
| `reboot.target` | 6 | Reboot. |
| `emergency.target` | (special) | Minimal shell, no services, root mounted read‑only. **Can be isolated.** |

> Not all targets can be isolated (switched to at runtime). The ones marked can be isolated are safe.

### 2.3 Comparison: Runlevels vs. Targets

| Feature | SysV Runlevels | systemd Targets |
|---------|----------------|-----------------|
| Configuration | `/etc/inittab`, `/etc/rc.d/rc?.d/` | Unit files (`.target`) |
| Startup | Sequential | Parallel (dependency‑based) |
| Dynamic switching | `init N` | `systemctl isolate name.target` |
| Default | `id:3:initdefault:` in `/etc/inittab` | `systemctl set-default name.target` |

---

## 3. Switching Between Targets (Runlevels)

### 3.1 Temporary Switch (`systemctl isolate`)

```bash
# Switch to multi‑user (text) mode
sudo systemctl isolate multi-user.target

# Switch to graphical mode
sudo systemctl isolate graphical.target

# Enter rescue mode (minimal services, network available)
sudo systemctl isolate rescue.target

# Enter emergency mode (minimal shell, read‑only root)
sudo systemctl isolate emergency.target
```

**Difference between rescue and emergency:**
- `rescue.target` – network, basic services, does not require root password.
- `emergency.target` – only a shell on the console, root is read‑only, needs root password.

### 3.2 Permanent Default Target (`systemctl set-default`)

```bash
# Set graphical as default
sudo systemctl set-default graphical.target

# Set text mode as default
sudo systemctl set-default multi-user.target

# Show current default
systemctl get-default
```

---

## 4. Relation Between Targets and Installation Types

| Installation type | Default target | Services included |
|------------------|----------------|-------------------|
| **Minimal Install** | `multi-user.target` | Only core tools, no GUI. |
| **Server with GUI** | `graphical.target` | `multi-user.target` + GNOME/KDE + display manager. |
| **Workstation** | `graphical.target` | As above, plus desktop applications. |

---

## 5. Systemd Unit Dependencies – `.wants` Directories

A target can **want** certain units. When a target starts, all units symlinked in its `.wants` directory are also started.

```bash
# See services that start with graphical.target
ls -l /etc/systemd/system/graphical.target.wants/
```

Enabling a service creates a symlink in the appropriate target’s `.wants` directory:
```bash
sudo systemctl enable httpd
# Creates symlink in /etc/systemd/system/multi-user.target.wants/httpd.service
```

---

## 6. Boot Files and Directories

### 6.1 `/boot/` Directory Contents

| File / Directory | Purpose |
|-----------------|---------|
| `vmlinuz-<version>` | Compressed Linux kernel image. |
| `initramfs-<version>.img` | Initial RAM file system (dracut). |
| `grub2/` | GRUB2 boot loader configuration and modules. |
| `efi/` | EFI System Partition mount point (UEFI). |

### 6.2 GRUB2 Configuration (`/boot/grub2/grub.cfg`)

**Do not edit this file directly** – it is automatically generated. Changes should be made in `/etc/default/grub` and then regenerated.

Simplified structure:
```
set default="0"
set timeout=5
menuentry 'RHEL 9 (5.14.0-162.el9.x86_64) ...' {
    linux   /vmlinuz-5.14.0-162.el9.x86_64 root=UUID=... ro
    initrd  /initramfs-5.14.0-162.el9.x86_64.img
}
```

### 6.3 `/etc/default/grub` – Kernel Boot Parameters

**Primary source for GRUB2 configuration.**

| Directive | Meaning |
|-----------|---------|
| `GRUB_TIMEOUT` | Seconds to display menu before booting default. `0` = skip menu, `-1` = wait forever. |
| `GRUB_DEFAULT` | Default menu entry (by index, name, or `saved`). |
| `GRUB_CMDLINE_LINUX` | Kernel command line parameters (e.g., `rhgb quiet`). |
| `GRUB_ENABLE_BLSCFG` | Enable BootLoaderSpec (default `true` on RHEL 9). |

**Common kernel parameters:**

| Parameter | Effect |
|-----------|--------|
| `rhgb` | Red Hat Graphical Boot – shows graphical boot screen. |
| `quiet` | Suppress most kernel messages. |
| `single` or `systemd.unit=rescue.target` | Boot into rescue mode. |
| `rd.break` | Break before switch root (reset root password). |
| `nomodeset` | Disable kernel mode setting (GPU issues). |

### 6.4 Generating a New GRUB2 Configuration (`grub2-mkconfig`)

After editing `/etc/default/grub`, regenerate:

**For BIOS:**
```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

**For UEFI:**
```bash
sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg
```

(RHEL 9’s `/boot/grub2/grub.cfg` is a symlink to the correct location; the above command writes to the right place.)

---

## 7. Dracut – Initial RAM Disk (initramfs)

**Dracut** generates the `initramfs` image. It contains kernel modules and scripts necessary to mount the real root file system.

**Rebuild initramfs for current kernel:**
```bash
sudo dracut --force
```

**Rebuild for a specific kernel:**
```bash
sudo dracut --force /boot/initramfs-$(uname -r).img $(uname -r)
```

---

## 8. Selecting a Different Kernel at Boot Time

At the GRUB2 menu:
1. Use arrow keys to highlight the desired kernel.
2. Press `Enter` to boot normally.

**Temporary kernel parameters:**
- Highlight the kernel line, press `e`.
- Navigate to the line starting with `linux` (UEFI) or `linux16` (BIOS).
- Add parameters (e.g., `rd.break`).
- Press `Ctrl+X` or `F10` to boot with these parameters (changes are **not** persistent).

**Set a kernel as default:** edit `GRUB_DEFAULT` in `/etc/default/grub` and regenerate.

---

## 9. Resetting the Root Password (`rd.break`)

### 9.1 Method 1: Using `rd.break` at Boot

1. At GRUB2 menu, highlight entry, press `e`.
2. Find the line starting with `linux`. Append **`rd.break`** at the end.
3. Press `Ctrl+X` to boot.
4. System drops into **initramfs shell** (read‑only root).
5. Remount root as read‑write:
   ```bash
   mount -o remount,rw /sysroot
   ```
6. Change into the real root:
   ```bash
   chroot /sysroot
   ```
7. Reset the password:
   ```bash
   passwd root
   ```
8. Ensure SELinux relabeling on next boot:
   ```bash
   touch /.autorelabel
   ```
9. Exit and reboot:
   ```bash
   exit
   reboot
   ```

### 9.2 Method 2: Using `init=/bin/bash` (Legacy)

- At GRUB edit, replace `rhgb quiet` with `init=/bin/bash`.
- Remount root as rw, change password, remount ro, reboot.

---

# new and reliable password reset method

This video, by beanologi, provides a guide on how to reset a forgotten root password on RHEL 9.0 as part of an RHCSA exam objective. Key points include:

Boot Process Intervention: The creator demonstrates booting the system by passing init=/bin/bash to the kernel via the GRUB menu (0:03:03-0:03:32).
File System Access: You must remount the root file system as read-write (mount -o remount,rw /) to modify system files (0:03:38-0:04:19).
Managing SE Linux: Because SE Linux is disabled during this process, modifying /etc/shadow causes it to lose its security context. The creator demonstrates using chcon to manually restore the correct labels to avoid login failures (0:04:23-0:07:11).
System Resumption: After resetting the password and fixing the context, the system must execute exec /sbin/init to properly boot into the systemd environment (0:07:12-0:08:06).
Inconsistency Note: The creator specifically addresses why this manual method is preferred over others, noting inconsistent behavior with the rd.break command in early RHEL 9 versions (0:00:54-0:02:12).

---

## 10. Secure Boot (UEFI) – Overview

**Secure Boot** ensures only signed bootloaders and kernels can run. RHEL 9 supports it.

- **Shim** – a signed bootloader that then loads GRUB2.
- **Signatures** – kernels and modules must be signed.
- **MokManager** – enroll custom keys.

**Check if Secure Boot is enabled:**
```bash
mokutil --sb-state
```

---

## 11. Quick Reference Table

| Task | Command / Action |
|------|------------------|
| Switch to text mode (temporary) | `sudo systemctl isolate multi-user.target` |
| Switch to graphical mode (temporary) | `sudo systemctl isolate graphical.target` |
| Set default to text mode | `sudo systemctl set-default multi-user.target` |
| Set default to graphical | `sudo systemctl set-default graphical.target` |
| Show current default target | `systemctl get-default` |
| Enter rescue mode | `sudo systemctl isolate rescue.target` |
| Enter emergency mode | `sudo systemctl isolate emergency.target` |
| Edit GRUB parameters | `/etc/default/grub` → change `GRUB_CMDLINE_LINUX` |
| Regenerate GRUB2 config | `sudo grub2-mkconfig -o /boot/grub2/grub.cfg` |
| Rebuild initramfs | `sudo dracut --force` |
| Reset root password | Add `rd.break` → `mount -o remount,rw /sysroot` → `chroot /sysroot` → `passwd` → `touch /.autorelabel` → `reboot` |
| Check Secure Boot status | `mokutil --sb-state` |

---

## 12. Real‑World Scenario – Managing a Headless Server’s Boot Process

### Background

You administer a remote RHEL 9 server `srv01` that runs in a data centre. It typically boots to `multi-user.target` (no GUI). For a maintenance window, you need to:

- Temporarily switch to `graphical.target` for a remote admin to use a desktop session (they will connect via VNC).
- After maintenance, revert to the default `multi-user.target` for normal operations.
- Set the default target permanently to `multi-user.target` to avoid wasting resources on boot.
- While testing a new kernel, you need to temporarily boot with a specific kernel version and add `rhgb quiet` to reduce verbosity.
- Simulate a lost root password by booting with `rd.break`, resetting it, and ensuring the system can boot normally afterward.

### Step 1 – Initial State and Temporary Switch

Check current target:
```bash
systemctl get-default
```

While running, temporarily switch to graphical mode so the admin can connect:
```bash
sudo systemctl isolate graphical.target
```

The admin does their work. After they disconnect, revert:
```bash
sudo systemctl isolate multi-user.target
```

### Step 2 – Set Permanent Default

```bash
sudo systemctl set-default multi-user.target
```

Now even after reboot, the system starts in text mode.

### Step 3 – Boot with a Specific Kernel and Custom Parameters

At the GRUB2 menu:

1. Highlight the desired kernel (e.g., an older one), press `e`.
2. Go to the `linux` line, make sure `rhgb quiet` is present (if missing, add it).
3. Press `Ctrl+X` to boot.

To make this persistent, edit `/etc/default/grub`:
```bash
sudo vi /etc/default/grub
# Set GRUB_DEFAULT to the menu entry name or index
# Ensure GRUB_CMDLINE_LINUX contains "rhgb quiet"
```
Then regenerate:
```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

### Step 4 – Reset Root Password with `rd.break`

You receive an alert that root password is unknown. Perform:

1. Reboot, interrupt GRUB, edit the entry, append `rd.break` to the `linux` line, boot (`Ctrl+X`).
2. In the initramfs shell:
   ```bash
   mount -o remount,rw /sysroot
   chroot /sysroot
   passwd root
   touch /.autorelabel
   exit
   reboot
   ```
3. After reboot, SELinux will relabel the filesystem, then the system comes up normally with the new root password.

### Step 5 – Verify and Document

- After reboots, confirm default target with `systemctl get-default`.
- Test that the system boots to the expected kernel version: `uname -r`.
- Check that `rhgb quiet` suppresses console messages during boot.

---

## 13. Practice Lab – Verify Your Understanding

1. **Boot to different target** – While logged in graphically, run `sudo systemctl isolate multi-user.target`. You will see the display manager terminate and switch to text consoles. Return to graphical with `sudo systemctl isolate graphical.target`.

2. **Change default target** – Temporarily set default to multi‑user, reboot, then change back.

3. **Edit kernel parameters** – Add `console=tty0 console=ttyS0` to `GRUB_CMDLINE_LINUX` in `/etc/default/grub`. Regenerate GRUB2 config and reboot. (For VMs, note the effect.)

4. **Reset root password** – Simulate lost root password:
   - Reboot, edit GRUB entry, append `rd.break`.
   - Follow the steps in section 9.1.
   - After reboot, log in with new root password.

5. **Explore `/boot`** – `ls -l /boot` and identify kernel, initramfs, and grub2 directory.

6. **List dependencies of a target** – `systemctl list-dependencies multi-user.target`.

7. **Check current kernel parameters** – `cat /proc/cmdline`.

---

**Date documented:** 2026-05-12  
**Sources:** Red Hat Enterprise Linux 9 System Administration, GRUB2 manual, `systemd` documentation, Dracut manual.