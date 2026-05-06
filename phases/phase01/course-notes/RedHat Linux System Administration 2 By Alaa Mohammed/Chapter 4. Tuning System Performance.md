# Chapter 4: Tuning System Performance – Complete Professional Guide

## Table of Contents

- [Chapter 4: Tuning System Performance – Complete Professional Guide](#chapter-4-tuning-system-performance--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What is Tuning? Why Do We Need It?](#1-what-is-tuning-why-do-we-need-it)
  - [2. Tuning Profiles – Detailed Descriptions](#2-tuning-profiles--detailed-descriptions)
  - [3. Installing Additional Profiles](#3-installing-additional-profiles)
  - [4. `tuned` – The System Tuning Daemon](#4-tuned--the-system-tuning-daemon)
    - [Service Management](#service-management)
    - [`tuned` Main Config File (`/etc/tuned/tuned-main.conf`)](#tuned-main-config-file-etctunedtuned-mainconf)
  - [5. `tuned-adm` – Managing Profiles](#5-tuned-adm--managing-profiles)
    - [Common Commands](#common-commands)
    - [Examples](#examples)
  - [6. File Locations and Configuration](#6-file-locations-and-configuration)
  - [7. How Tuned Works Under the Hood](#7-how-tuned-works-under-the-hood)
  - [8. Process Prioritisation – `nice` and `renice`](#8-process-prioritisation--nice-and-renice)
    - [8.1 What is Nice Value? Why?](#81-what-is-nice-value-why)
    - [8.2 Child Process Inheritance of Nice Value](#82-child-process-inheritance-of-nice-value)
    - [8.3 `nice` – Start a Process with a Priority](#83-nice--start-a-process-with-a-priority)
    - [8.4 `renice` – Change Priority of a Running Process](#84-renice--change-priority-of-a-running-process)
    - [8.5 Monitoring Nice Values](#85-monitoring-nice-values)
  - [9. Quick Reference Table](#9-quick-reference-table)
  - [10. Real‑World Scenario – Optimising a Mixed‑Workload Server](#10-realworld-scenario--optimising-a-mixedworkload-server)
    - [Background](#background)
    - [Step 1 – Install any missing tuned profiles](#step-1--install-any-missing-tuned-profiles)
    - [Step 2 – Switch to a suitable base profile](#step-2--switch-to-a-suitable-base-profile)
    - [Step 3 – Create a custom profile inheriting from `throughput-performance`](#step-3--create-a-custom-profile-inheriting-from-throughput-performance)
    - [Step 4 – Activate the custom profile](#step-4--activate-the-custom-profile)
    - [Step 5 – Schedule the reporting job with low CPU priority](#step-5--schedule-the-reporting-job-with-low-cpu-priority)
    - [Step 6 – (Optional) Boost PostgreSQL priority if necessary](#step-6--optional-boost-postgresql-priority-if-necessary)
    - [Step 7 – Monitor the system during the reporting window](#step-7--monitor-the-system-during-the-reporting-window)
    - [Step 8 – Validate stability and performance](#step-8--validate-stability-and-performance)
  - [11. Practice Lab – Verify Your Understanding](#11-practice-lab--verify-your-understanding)

---

## 1. What is Tuning? Why Do We Need It?

**Tuning** means adjusting system parameters (kernel, CPU scheduler, memory management, I/O, network) to optimise performance for a specific workload.

**Why do we need it?**

| Scenario | Problem | Tuning Solution |
|----------|---------|----------------|
| **Database server** | Default kernel settings may cause high context switches, poor I/O throughput. | Tune for **throughput‑performance** (increase dirty ratios, adjust swappiness, use `deadline` I/O scheduler). |
| **Web server (low latency)** | Default CPU governor may favour power saving, increasing latency. | Switch to `performance` governor, disable transparent hugepages, use `network-latency` profile. |
| **Virtualisation host** | Host may not optimise for guest performance (e.g., KVM). | Use `virtual-host` profile (disables some power saving, tunes memory overcommit). |
| **Desktop / laptop** | Battery life is important; maximum performance not needed. | Use `powersave` or `balanced` profile (CPU governor `ondemand` or `conservative`). |
| **Low‑memory system** | Heavy swapping degrades performance. | Reduce swappiness, adjust `vm.dirty_ratio`. |

**Examples:**
- A default RHEL installation is balanced for general purpose. Running a high‑throughput database (e.g., PostgreSQL) may benefit from `throughput-performance` which increases kernel dirty page limits, changes I/O scheduler, and disables power saving.
- A real‑time audio workstation may require `realtime` profile to minimise latency.

---

## 2. Tuning Profiles – Detailed Descriptions

`tuned` ships with many pre‑defined profiles. Below are the most important ones.

| Profile | Description | When to Use |
|---------|-------------|-------------|
| **balanced** | Default profile. Enables energy saving while maintaining good performance. | General‑purpose servers, desktops. |
| **throughput-performance** | Maximises throughput (data processed per time unit). Disables power saving, uses `performance` CPU governor, `noop` or `none` I/O scheduler, increases dirty ratios. | Database servers, file servers, batch processing. |
| **latency-performance** | Minimises latency (response time). Disables power saving, locks CPU frequency to highest, uses `madvise` for transparent hugepages. | Web servers, low‑latency trading systems, real‑time applications. |
| **network-latency** | Optimises for low network latency. Disables power saving, tunes TCP parameters (e.g., `tcp_slow_start_after_idle=0`, increases `netdev_max_backlog`). | High‑frequency trading, VoIP servers, game servers. |
| **network-throughput** | Maximises network throughput. Increases socket buffers, enables TCP window scaling, adjusts `rmem_max`/`wmem_max`. | File transfer servers, backup servers, CDN nodes. |
| **virtual-host** | Optimises a host that runs virtual machines (KVM). Disables some power saving, tunes memory management, enables `isolation` for CPU pinning. | Hypervisor servers. |
| **virtual-guest** | Optimises a guest VM. Similar to `throughput-performance` but with some VM‑specific adjustments. | Virtual machines (if `tuned` is installed inside). |
| **desktop** | For interactive desktop. Uses `balanced` base but may adjust scheduler for UI responsiveness. | Workstations. |
| **powersave** | Maximises energy efficiency. Uses `powersave` CPU governor, aggressive power management, reduces wakeups. | Laptops on battery, low‑power servers. |
| **realtime** | For real‑time workloads (requires `kernel-rt`). Sets CPU affinity, isolates cores, uses `SCHED_FIFO`. | Real‑time audio/video processing, industrial control. |
| **hpc-compute** | High‑performance computing. Disables hyper‑threading, uses `performance` governor, may set memory binding. | Cluster compute nodes. |

**Check available profiles:**
```bash
tuned-adm list
```

**Recommend profile based on your system:**
```bash
tuned-adm recommend
```

---

## 3. Installing Additional Profiles

Some profiles are in separate packages.

```bash
# List tuned profile packages
dnf search tuned-profiles

# Install all optional profiles (including realtime, oracle, mssql, etc.)
sudo dnf install tuned-profiles-*

# Install only specific ones
sudo dnf install tuned-profiles-realtime
```

After installation, new profiles appear in `tuned-adm list`.

---

## 4. `tuned` – The System Tuning Daemon

`tuned` is a service that applies tuning profiles dynamically. It can also monitor system activity and react to changes (e.g., switch to `powersave` when on battery).

### Service Management

```bash
# Start and enable tuned
sudo systemctl enable --now tuned

# Check status
sudo systemctl status tuned

# Restart after manual config changes
sudo systemctl restart tuned

# View logs
journalctl -u tuned
```

### `tuned` Main Config File (`/etc/tuned/tuned-main.conf`)

Key directives:

| Directive | Meaning | Example |
|-----------|---------|---------|
| `dynamic_tuning` | Allow dynamic adjustments based on system load. | `dynamic_tuning=1` (default) |
| `sleep_interval` | Seconds between monitoring checks. | `sleep_interval=5` |
| `update_interval` | Seconds between applying changes. | `update_interval=10` |
| `recommend_command` | How to determine default profile. | `recommend_command=no` (use static) |

**Example:** Disable dynamic tuning (always apply profile statically):
```ini
dynamic_tuning=0
```

---

## 5. `tuned-adm` – Managing Profiles

`tuned-adm` is the command‑line tool to switch profiles, view active profile, verify, and list recommendations.

### Common Commands

| Command | Purpose |
|---------|---------|
| `tuned-adm list` | Show all available profiles (active profile marked with `[` `]`). |
| `tuned-adm active` | Show currently active profile. |
| `tuned-adm recommend` | Print the recommended profile for your system. |
| `tuned-adm profile <name>` | Activate a specific profile (e.g., `tuned-adm profile throughput-performance`). |
| `tuned-adm off` | Disable all tuning (revert to kernel defaults). |
| `tuned-adm verify` | Check whether the applied profile settings are actually active (compares expected vs current kernel parameters). |
| `tuned-adm profile_info <name>` | Show description and parameters of a profile. |

### Examples

```bash
# List all profiles
tuned-adm list

# Switch to throughput-performance
sudo tuned-adm profile throughput-performance

# Verify that settings are applied
sudo tuned-adm verify

# Temporarily turn off tuning (e.g., for debugging)
sudo tuned-adm off

# Re‑enable the previous profile
sudo tuned-adm profile throughput-performance

# Show details of a profile
tuned-adm profile_info balanced
```

---

## 6. File Locations and Configuration

| Path | Purpose |
|------|---------|
| `/etc/tuned/tuned-main.conf` | Main daemon configuration. |
| `/etc/tuned/active_profile` | Contains name of the currently active profile. |
| `/etc/tuned/profile_mode` | Mode (`manual` or `auto`). |
| `/usr/lib/tuned/` | System‑shipped profile directories (e.g., `/usr/lib/tuned/balanced/`). |
| `/etc/tuned/` | Custom profiles (override system profiles if same name). |
| `/var/log/tuned/tuned.log` | Log file (if logging enabled). |
| `/sys/kernel/debug/tuned/` | Debug interface (if mounted). |
| `/proc/sys/` | Many kernel parameters changed by `tuned` (e.g., vm.swappiness). |

**Custom profile creation:** You can create your own profile under `/etc/tuned/myprofile/` with a `tuned.conf` file that inherits from an existing profile and overrides parameters.

Example `/etc/tuned/myprofile/tuned.conf`:
```ini
[main]
include=throughput-performance

[sysctl]
vm.swappiness=10
vm.dirty_ratio=30
```

Activate: `sudo tuned-adm profile myprofile`.

---

## 7. How Tuned Works Under the Hood

The `tuned` daemon uses a plugin system to apply system adjustments. When you activate a profile, `tuned`:

1. **Reads the profile definition** (`tuned.conf`) – each line specifies a plugin and its parameters.
2. **Applies the settings** using the appropriate kernel interfaces:
   - **CPU** – scaling governor (via `cpufreq`), pinning (via `cpuset`), energy‑efficient policy.
   - **Disk** – I/O scheduler (e.g., `noop`, `none`, `mq-deadline`), read‑ahead values, queue depth.
   - **Memory** – sysctl parameters: `vm.swappiness`, `vm.dirty_background_ratio`, `vm.dirty_ratio`, transparent hugepages (`/sys/kernel/mm/transparent_hugepage/enabled`).
   - **Network** – sysctl parameters: `net.core.rmem_max`, `net.core.wmem_max`, `tcp_slow_start_after_idle`, `netdev_max_backlog`.
   - **Bootloader** – can add kernel command line arguments (requires reboot).

3. **Monitors** system events (dynamic tuning) – e.g., when AC power is disconnected, change to `powersave` profile.

**Under‑the‑hood plugins (common):**

| Plugin | What it controls | Example parameter |
|--------|------------------|-------------------|
| `cpu` | CPU governor, min/max frequency | `governor=performance` |
| `disk` | I/O scheduler, read‑ahead | `elevator=noop` |
| `sysctl` | Kernel runtime parameters | `vm.swappiness=10` |
| `vm` | Virtual memory behaviour | `transparent_hugepages=always` |
| `net` | Network stack tuning | `tcp_congestion_control=bbr` |
| `bootloader` | Kernel command line | `cmdline=processor.max_cstate=1` |
| `script` | Run custom scripts | `script=${i:PROFILE_DIR}/script.sh` |

**Verification:** `tuned-adm verify` uses the same plugins to read current values and compare with expected.

---

## 8. Process Prioritisation – `nice` and `renice`

### 8.1 What is Nice Value? Why?

The **nice value** determines a process’s CPU priority. It ranges from `-20` (highest priority, least “nice”) to `+19` (lowest priority, most “nice”). Default is `0`.

- **Higher nice value** → process yields CPU to others → **lower priority**.
- **Lower nice value** → process gets more CPU → **higher priority** (requires root).

**Why?** To ensure that important tasks (e.g., system daemons) get CPU before less critical background jobs (e.g., backup scripts, batch processing).

**Example:** A database server should have higher priority (nice -5) than a log compressing job (nice 15).

### 8.2 Child Process Inheritance of Nice Value

When a parent process spawns a child (e.g., using `fork()`), the child **inherits** the parent’s nice value. This is important for session management.

```bash
# Parent has nice 5
nice -n 5 bash
# All commands run from this child shell will have nice 5 (unless overridden)
```

**Visual:**

```
Parent (nice 0)
    │
    ├── Child A (nice 0)   ← inherits default
    └── Child B (nice 5)   ← if parent had nice 5
```

### 8.3 `nice` – Start a Process with a Priority

**Syntax:** `nice -n <adjustment> command`

- `-n 5` adds 5 to the default priority (so default 0 becomes 5, less priority).
- `-n -5` reduces nice value (higher priority) – requires root.

**Examples:**

```bash
# Run a CPU‑intensive task with low priority (nice +10)
nice -n 10 dd if=/dev/zero of=/dev/null bs=1M &

# Run with high priority (root only)
sudo nice -n -5 ./important_process

# Without adjustment, nice shows current value (but default)
nice top
```

If you omit `-n`, the default adjustment is +10 (lower priority).

### 8.4 `renice` – Change Priority of a Running Process

**Syntax:** `renice -n <new_priority> -p <PID>`

**Options:**
- `-n` – new nice value (absolute, not adjustment).
- `-p` – process ID(s).
- `-u` – change priority for all processes of a user.
- `-g` – change priority for a process group.

**Examples:**

```bash
# Reduce priority of process with PID 1234
sudo renice -n 15 -p 1234

# Increase priority of all of user alice’s processes
sudo renice -n -5 -u alice

# Increase priority of a process group (e.g., all processes in a session)
sudo renice -n -10 -g 1234
```

**Check current nice values:** `ps -l` (NI column) or `top` (NI column).

### 8.5 Monitoring Nice Values

```bash
# Show nice values with ps
ps -l
# Output: F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD
# NI column = nice value

# In top, press 'r' to renice a process interactively.
```

---

## 9. Quick Reference Table

| Task | Command |
|------|---------|
| List available profiles | `tuned-adm list` |
| Activate a profile | `sudo tuned-adm profile <name>` |
| Show active profile | `tuned-adm active` |
| Verify profile settings | `tuned-adm verify` |
| Turn off tuning | `sudo tuned-adm off` |
| Install extra profiles | `sudo dnf install tuned-profiles-*` |
| Edit tuned main config | `/etc/tuned/tuned-main.conf` |
| View tuned logs | `journalctl -u tuned` |
| Run a command with high priority (root) | `sudo nice -n -5 command` |
| Run a command with low priority | `nice -n 15 command` |
| Change priority of running process | `sudo renice -n 10 -p PID` |
| Show nice value of processes | `ps -l` or `top` |

---

## 10. Real‑World Scenario – Optimising a Mixed‑Workload Server

### Background

You manage a server (`app‑server‑01`) that runs a **PostgreSQL database** and a **background reporting job** that runs every night at 2 AM. The reporting job belongs to user `reportuser` and is very CPU‑intensive (it aggregates large tables). The database must remain responsive during the reporting window because some API requests still access it.

Additionally, the server has a default `balanced` profile, but you suspect latency is higher than expected for database queries. You decide to optimise:

- Switch to a throughput‑optimised profile for the database workload.
- Ensure the reporting job runs at a **low CPU priority** (nice +10) so that PostgreSQL (with default nice 0) always gets CPU first.
- Create a custom tuned profile that keeps throughput settings but also reduces `vm.swappiness` to 10 (to avoid swapping) and sets the I/O scheduler to `mq-deadline`.

### Step 1 – Install any missing tuned profiles

```bash
sudo dnf install tuned-profiles-* -y
```

### Step 2 – Switch to a suitable base profile

```bash
sudo tuned-adm profile throughput-performance
sudo tuned-adm verify
```

### Step 3 – Create a custom profile inheriting from `throughput-performance`

Create `/etc/tuned/postgresql-custom/tuned.conf`:

```ini
[main]
include=throughput-performance

[sysctl]
vm.swappiness=10
vm.dirty_ratio=20

[disk]
# Set I/O scheduler for all disks (you can target specific disks if needed)
devices=sda, sdb
elevator=mq-deadline
```

### Step 4 – Activate the custom profile

```bash
sudo tuned-adm profile postgresql-custom
sudo tuned-adm verify
```

### Step 5 – Schedule the reporting job with low CPU priority

The job is launched by `reportuser`’s crontab. You modify the crontab entry:

```cron
0 2 * * * /usr/bin/nice -n 10 /opt/reporting/nightly-report.sh > /var/log/report.log 2>&1
```

All child processes of the script will inherit nice 10, so they won’t starve PostgreSQL (which runs at nice 0, possibly even higher priority for some DB processes that might be manually reniced).

### Step 6 – (Optional) Boost PostgreSQL priority if necessary

If you notice PostgreSQL still struggles, you can increase its priority:

```bash
# Find the PID of the PostgreSQL main process (postmaster)
# and renice all its children
sudo renice -n -5 -u postgres
```

### Step 7 – Monitor the system during the reporting window

Use `top` or `htop` to verify that the reporting job uses CPU only when PostgreSQL is idle, and that the CPU governor is `performance`. Check effective nice values with `ps -eo pid,comm,ni`.

### Step 8 – Validate stability and performance

After a few nights, verify that the reporting job completes on time and that database query latency has improved. You can compare before/after using `tuned-adm verify` and monitoring tools.

**Result:** The server now efficiently balances foreground database operations and background reporting, with kernel parameters tuned for a database workload and process priorities ensuring responsiveness.

---

## 11. Practice Lab – Verify Your Understanding

1. **Check current profile:** Run `tuned-adm active` and `tuned-adm recommend`. Switch to `throughput-performance` and verify with `tuned-adm verify`.

2. **Observe CPU governor change:** While using `balanced` profile, check current governor: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`. Switch to `powersave` and check again.

3. **Create a custom profile:** Create `/etc/tuned/mycustom/tuned.conf` that inherits from `balanced` and sets `vm.swappiness=10`. Activate it and verify with `sysctl vm.swappiness`.

4. **Process priority experiment:** Run an infinite loop `while true; do :; done` in background. Use `top` to see its CPU usage and nice value (default 0). Use `renice` to lower its priority to +19, then observe CPU usage drop (if there are other processes competing). Then raise priority to -10 (requires root) and observe.

5. **Nice inheritance:** Start a shell with `nice -n 10 bash`. Inside it, run a CPU‑intensive command and check its nice value (should be 10). Exit and run the same command from the original shell – nice value should be 0.

6. **Dynamic tuning (optional):** If your hardware supports power events (e.g., laptop), plug/unplug AC and monitor whether `tuned` switches profiles (requires `dynamic_tuning=1` in `tuned-main.conf`).

---

**Date documented:** 2026-05-06  
**Sources:** Red Hat Enterprise Linux 9 Performance Tuning Guide, `tuned` documentation, `nice`/`renice` man pages

---
