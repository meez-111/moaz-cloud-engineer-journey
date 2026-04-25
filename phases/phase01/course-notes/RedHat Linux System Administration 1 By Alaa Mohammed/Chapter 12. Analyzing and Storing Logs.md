# Chapter 12: Analyzing and Storing Logs – Professional Complete Guide

## Table of Contents

- [Chapter 12: Analyzing and Storing Logs – Professional Complete Guide](#chapter-12-analyzing-and-storing-logs--professional-complete-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Linux Logging Architecture](#1-linux-logging-architecture)
    - [Who Sends Logs?](#who-sends-logs)
    - [Who Collects Logs?](#who-collects-logs)
  - [2. Standard Log Files and Locations](#2-standard-log-files-and-locations)
  - [3. Log Message Anatomy and Severities](#3-log-message-anatomy-and-severities)
    - [Standard Syslog Message Format](#standard-syslog-message-format)
    - [Syslog Severity Levels (Priority)](#syslog-severity-levels-priority)
    - [Syslog Facilities (Categories)](#syslog-facilities-categories)
  - [4. `rsyslog` – The Modern Log Collector](#4-rsyslog--the-modern-log-collector)
    - [Configuration Files](#configuration-files)
    - [Rule Syntax](#rule-syntax)
    - [Common Configuration Examples](#common-configuration-examples)
    - [Testing and Reloading](#testing-and-reloading)
    - [Using `logger` to Test](#using-logger-to-test)
  - [5. `systemd-journald` – The Binary Journal](#5-systemd-journald--the-binary-journal)
    - [Storage Modes](#storage-modes)
    - [Enabling Persistent Storage](#enabling-persistent-storage)
    - [Basic `journalctl` Queries](#basic-journalctl-queries)
    - [Comparison: Journal vs. Syslog](#comparison-journal-vs-syslog)
  - [6. Log Rotation with `logrotate`](#6-log-rotation-with-logrotate)
    - [Configuration Files](#configuration-files-1)
    - [Common Directives](#common-directives)
    - [Example: Nginx](#example-nginx)
    - [Example: Custom Application](#example-custom-application)
    - [Testing Logrotate](#testing-logrotate)
  - [7. Time Synchronisation with `chrony`](#7-time-synchronisation-with-chrony)
    - [Comparison: `chrony` vs. `ntpd` vs. `systemd-timesyncd`](#comparison-chrony-vs-ntpd-vs-systemd-timesyncd)
    - [Basic Configuration – `/etc/chrony.conf`](#basic-configuration--etcchronyconf)
    - [Managing Time with `timedatectl`](#managing-time-with-timedatectl)
    - [Monitoring with `chronyc`](#monitoring-with-chronyc)
  - [8. Kernel Messages – `dmesg`](#8-kernel-messages--dmesg)
  - [9. Linux Audit Framework – `auditd`](#9-linux-audit-framework--auditd)
    - [System Logs vs. Audit Logs](#system-logs-vs-audit-logs)
    - [Installation and Enablement](#installation-and-enablement)
    - [Configuration Files](#configuration-files-2)
    - [Key `auditd.conf` Directives](#key-auditdconf-directives)
    - [Adding Audit Rules (`auditctl`)](#adding-audit-rules-auditctl)
    - [Making Rules Persistent](#making-rules-persistent)
    - [Searching Audit Logs – `ausearch`](#searching-audit-logs--ausearch)
    - [Generating Audit Reports – `aureport`](#generating-audit-reports--aureport)
  - [10. Advanced Logging – Custom Application Integration](#10-advanced-logging--custom-application-integration)
    - [10.1 Method 1: Application → Socket → rsyslog (Standard)](#101-method-1-application--socket--rsyslog-standard)
    - [10.2 Method 2: Hybrid Forwarder (Local + Remote)](#102-method-2-hybrid-forwarder-local--remote)
    - [10.3 Method 3: Legacy File Ingestion (`imfile`)](#103-method-3-legacy-file-ingestion-imfile)
    - [10.4 Method 4: Direct Remote Bypass (App → Remote)](#104-method-4-direct-remote-bypass-app--remote)
    - [Admin Troubleshooting Cheat Sheet](#admin-troubleshooting-cheat-sheet)
    - [Log Rotation for Custom Logs](#log-rotation-for-custom-logs)
  - [11. Complete Real‑World Production Scenario](#11-complete-realworld-production-scenario)
    - [Step 1: Ensure Accurate Time with `chrony`](#step-1-ensure-accurate-time-with-chrony)
    - [Step 2: Enable Persistent `systemd-journald`](#step-2-enable-persistent-systemd-journald)
    - [Step 3: Configure `rsyslog` for the Application](#step-3-configure-rsyslog-for-the-application)
    - [Step 4: Use `logger` to Simulate Application Messages](#step-4-use-logger-to-simulate-application-messages)
    - [Step 5: Set Up Log Rotation](#step-5-set-up-log-rotation)
    - [Step 6: Query Logs Like a Pro](#step-6-query-logs-like-a-pro)
    - [Step 7: Configure Auditing](#step-7-configure-auditing)
    - [Step 8: Final Verification Checklist](#step-8-final-verification-checklist)
  - [12. Essential Log Commands – Quick Reference](#12-essential-log-commands--quick-reference)
  - [13. Best Practices for Log Management](#13-best-practices-for-log-management)
  - [14. Practice Lab – Verify Your Understanding](#14-practice-lab--verify-your-understanding)

---

## 1. Linux Logging Architecture

Logging in Linux follows a **modular architecture**:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Kernel    │────▶│   klogd     │────▶│             │
└─────────────┘     └─────────────┘     │             │
                                         │   rsyslogd  │────▶ /var/log/messages
┌─────────────┐     ┌─────────────┐     │  (or syslogd)│     /var/log/secure
│   Users     │────▶│             │     │             │     /var/log/maillog
├─────────────┤     │   rsyslogd   │────▶│             │
│  Services   │────▶│  (collector) │     └─────────────┘
├─────────────┤     │             │
│  Devices    │────▶│             │
└─────────────┘     └─────────────┘
```

### Who Sends Logs?

| Source | Examples |
|--------|----------|
| **Kernel** | Hardware events, driver messages, OOM killer, filesystem errors |
| **Users** | Login attempts, command history, sudo usage |
| **Services (Daemons)** | `sshd`, `cron`, `nginx`, `mysql`, `httpd` |
| **Devices** | USB hotplug, disk I/O errors, network interface state changes |
| **Applications** | Custom scripts, web applications, database queries |

### Who Collects Logs?

| Component | Role |
|-----------|------|
| **`klogd`** (Kernel Log Daemon) | Collects log messages directly from the kernel ring buffer (`/proc/kmsg`). |
| **`rsyslogd`** (modern) | Collects logs from userspace applications, services, and devices via `/dev/log` socket. |
| **`syslogd`** (legacy) | Traditional syslog daemon (old Unix systems). |

> **Modern systems:** `rsyslog` has replaced legacy `syslogd`. It supports TCP, TLS encryption, and advanced filtering.

---

## 2. Standard Log Files and Locations

| File | Purpose | Typical Contents |
|------|---------|------------------|
| `/var/log/messages` | General system messages (non‑security, non‑mail) | Kernel messages, service startup/shutdown, hardware events |
| `/var/log/secure` (RHEL) `/var/log/auth.log` (Debian) | Authentication and security logs | Login attempts (success/failure), sudo usage, SSH access |
| `/var/log/maillog` (RHEL) `/var/log/mail.log` (Debian) | Mail server logs | Sendmail/Postfix activity, spam filtering |
| `/var/log/dnf.log` (RHEL) `/var/log/apt/history.log` (Debian) | Package manager logs | Installed/removed packages, updates |
| `/var/log/cron` | Scheduled job logs | Cron execution output, errors |
| `/var/log/boot.log` | System boot messages | Service start/stop during boot |
| `/var/log/httpd/` (or `/var/log/nginx/`) | Web server logs | Access logs, error logs |
| `/var/log/audit/audit.log` | Linux Audit Framework logs | Security events, file access monitoring |

**Note:** Many services create their own **subdirectories** under `/var/log/` (e.g., `/var/log/nginx/`, `/var/log/mysql/`).

---

## 3. Log Message Anatomy and Severities

### Standard Syslog Message Format

```
2026-04-22T10:38:51.123456+02:00 hostname service-name[PID]: priority: Message body
```

| Field | Example | Meaning |
|-------|---------|---------|
| **Date** | `2026-04-22` | ISO 8601 date |
| **Time** | `10:38:51.123456` | Timestamp with microseconds (if configured) |
| **Hostname** | `webserver01` | Name of the system that generated the log |
| **Service name** | `sshd` | Name of the daemon/process |
| **PID** | `[1234]` | Process ID (often optional) |
| **Priority** | `info`, `warning`, `err`, `crit` | Severity level (see table below) |
| **Message body** | `Accepted password for alice from 192.168.1.100 port 22 ssh2` | The actual log content |

### Syslog Severity Levels (Priority)

| Code | Severity | Keyword | Description |
|------|----------|---------|-------------|
| 0 | Emergency | `emerg` | System is unusable |
| 1 | Alert | `alert` | Action must be taken immediately |
| 2 | Critical | `crit` | Critical conditions |
| 3 | Error | `err` | Error conditions |
| 4 | Warning | `warning` | Warning conditions |
| 5 | Notice | `notice` | Normal but significant condition |
| 6 | Informational | `info` | Informational messages |
| 7 | Debug | `debug` | Debug‑level messages |

### Syslog Facilities (Categories)

| Facility Code | Keyword | Description |
|---------------|---------|-------------|
| 0 | `kern` | Kernel messages |
| 1 | `user` | User‑level messages (default) |
| 2 | `mail` | Mail system |
| 3 | `daemon` | System daemons |
| 4 | `auth` | Security/authorization messages |
| 5 | `syslog` | Messages generated internally by syslogd |
| 6 | `lpr` | Line printer subsystem |
| 7 | `news` | Network news subsystem |
| 8 | `uucp` | UUCP subsystem |
| 9 | `cron` | Cron subsystem |
| 10 | `authpriv` | Private security/authorization messages |
| 11 | `ftp` | FTP daemon |
| 16–23 | `local0`–`local7` | Locally defined (custom applications) |

---

## 4. `rsyslog` – The Modern Log Collector

`rsyslog` is the default syslog daemon on RHEL/CentOS 7+, Debian 8+, Ubuntu 14.04+.

### Configuration Files

| File/Directory | Purpose |
|----------------|---------|
| `/etc/rsyslog.conf` | Main configuration file |
| `/etc/rsyslog.d/*.conf` | Drop‑in directory for custom rules (recommended) |

> **Best practice:** Leave `/etc/rsyslog.conf` untouched and place your custom rules in `/etc/rsyslog.d/` with a `.conf` extension.

### Rule Syntax

Legacy format (still works):
```
facility.priority    action
```

Modern RainerScript format (recommended):
```
if ($syslogfacility-text == "local3") then {
    action(type="omfile" file="/var/log/myapp.log")
}
```

### Common Configuration Examples

| Purpose | Configuration |
|---------|---------------|
| Custom file for `local0` | `local0.*    /var/log/myapp.log` |
| Discard all debug messages | `*.debug    stop` |
| Forward to remote server over TCP | `*.*    @@192.168.1.100:514` ( `@` = UDP, `@@` = TCP) |
| Log kernel messages separately | `kern.*    /var/log/kernel.log` |
| Load TCP input module | `module(load="imtcp")`<br>`input(type="imtcp" port="514")` |

### Testing and Reloading

```bash
# Check configuration syntax
sudo rsyslogd -N 1

# Reload after changes
sudo systemctl reload rsyslog

# View status
sudo systemctl status rsyslog
```

### Using `logger` to Test

```bash
logger "Test message"
logger -p local0.info "Application started"
logger -t MYSCRIPT -p user.warning "Disk space low"
```

---

## 5. `systemd-journald` – The Binary Journal

`systemd-journald` collects logs in a **binary, indexed format** for fast search. It coexists with `rsyslog`.

### Storage Modes

| Mode | Location | Behavior |
|------|----------|----------|
| **Volatile** (default) | `/run/log/journal` | Logs lost on reboot |
| **Persistent** | `/var/log/journal` | Logs survive reboots (recommended for servers) |
| **Auto** | Uses `/var/log/journal` if directory exists, else volatile | Fallback |

### Enabling Persistent Storage

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
sudo journalctl --flush          # needed on some systemd versions
```

### Basic `journalctl` Queries

| Command | Purpose |
|---------|---------|
| `journalctl` | View all logs (paged) |
| `journalctl -u service` | Logs for a specific service |
| `journalctl -f` | Follow (tail) new logs |
| `journalctl --since "1 hour ago"` | Time‑filtered |
| `journalctl -n 50` | Last 50 lines |
| `journalctl -p err` | Only errors and higher |
| `journalctl -k` | Kernel messages only |
| `journalctl -b` | Current boot only |
| `journalctl -o json-pretty` | JSON format for scripting |

### Comparison: Journal vs. Syslog

| Feature | systemd‑journald | rsyslog |
|---------|------------------|---------|
| Storage | Binary, indexed | Plain text |
| Search speed | Very fast | Slower (`grep`) |
| Remote logging | Limited | Full (TCP, TLS) |
| Structured data | Yes (fields) | Limited |
| Traditional tools | `journalctl` | `grep`, `tail`, `less` |

**Recommendation:** Use both – journal for fast search, rsyslog for remote forwarding and long‑term archiving.

---

## 6. Log Rotation with `logrotate`

### Configuration Files

| File | Purpose |
|------|---------|
| `/etc/logrotate.conf` | Global configuration |
| `/etc/logrotate.d/` | Application‑specific configuration |

### Common Directives

| Directive | Purpose |
|-----------|---------|
| `daily`, `weekly`, `monthly` | Rotation frequency |
| `rotate N` | Keep `N` rotated files |
| `compress` | Compress old logs with gzip |
| `delaycompress` | Compress one cycle later (works with `copytruncate`) |
| `create mode owner group` | Create new log after rotation |
| `copytruncate` | Copy then truncate (for apps that can't reopen logs) |
| `missingok` | No error if log missing |
| `notifempty` | Do not rotate empty logs |
| `dateext` | Append date to rotated filename |
| `maxsize size` | Rotate when file exceeds size (e.g., `100M`) |
| `postrotate`/`endscript` | Run commands after rotation |

### Example: Nginx

```bash
/var/log/nginx/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 nginx adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### Example: Custom Application

```bash
/var/log/myapp/*.log {
    size 100M
    rotate 7
    compress
    missingok
    notifempty
    copytruncate
}
```

### Testing Logrotate

```bash
# Dry run
sudo logrotate -d /etc/logrotate.conf

# Force rotation
sudo logrotate -f /etc/logrotate.conf

# Check rotation status
cat /var/lib/logrotate/status
```

---

## 7. Time Synchronisation with `chrony`

Accurate time is **critical** for logs, certificates, cron jobs, and distributed systems.

### Comparison: `chrony` vs. `ntpd` vs. `systemd-timesyncd`

| Feature | `chrony` | `ntpd` | `systemd-timesyncd` |
|---------|----------|--------|---------------------|
| Modern default | ✅ (RHEL 7+, Ubuntu 25.10+) | ❌ legacy | ✅ simple client |
| Fast sync | ✅ | ❌ | ❌ |
| Works on intermittent networks | ✅ | ❌ | ❌ |
| NTS encryption | ✅ | ❌ | ❌ |
| Best for | Servers, VMs, containers | Strict compliance | Simple clients |

### Basic Configuration – `/etc/chrony.conf`

```
pool 0.pool.ntp.org iburst
pool 1.pool.ntp.org iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
```

### Managing Time with `timedatectl`

```bash
# Check status
timedatectl status

# Set timezone
sudo timedatectl set-timezone Asia/Riyadh

# Enable/disable NTP
sudo timedatectl set-ntp true
```

### Monitoring with `chronyc`

```bash
chronyc sources -v          # show time sources
chronyc tracking            # detailed synchronisation
```

In the output:
- `^*` = current synchronised source
- `^-` = acceptable source
- `?` = unreachable source

Verify synchronisation:
```bash
timedatectl status | grep "System clock synchronized"
```

---

## 8. Kernel Messages – `dmesg`

```bash
dmesg                   # view kernel ring buffer
dmesg -w                # follow new messages
dmesg --level=err,crit  # only errors/critical
dmesg -T                # human‑readable timestamps
sudo dmesg -c           # clear buffer
```

**Common use cases:** disk errors, USB issues, memory problems, hardware compatibility.

---

## 9. Linux Audit Framework – `auditd`

`auditd` tracks **security‑relevant events** – file access, system calls, user logins.

### System Logs vs. Audit Logs

| Feature | System Logs (`rsyslog`/`journald`) | Audit Logs (`auditd`) |
|---------|-------------------------------------|----------------------|
| Purpose | Monitoring, debugging | Security auditing, compliance |
| Granularity | Application/kernel messages | Configurable syscalls/files |
| Default logging | Yes | No (must be configured) |
| Location | `/var/log/messages`, journal | `/var/log/audit/audit.log` |

### Installation and Enablement

```bash
sudo dnf install -y audit          # RHEL
sudo apt install -y auditd         # Debian
sudo systemctl enable --now auditd
```

### Configuration Files

| File | Purpose |
|------|---------|
| `/etc/audit/auditd.conf` | Daemon configuration (log location, rotation) |
| `/etc/audit/rules.d/audit.rules` | Audit rules |

### Key `auditd.conf` Directives

| Directive | Recommended Value |
|-----------|-------------------|
| `log_file = /var/log/audit/audit.log` | Log location |
| `log_format = ENRICHED` | Resolve UIDs, GIDs, syscall names |
| `flush = INCREMENTAL_ASYNC` | Performance |
| `max_log_file = 50` | Max MB before rotation |
| `num_logs = 5` | Number of rotated logs |

### Adding Audit Rules (`auditctl`)

```bash
# Watch file/directory
sudo auditctl -w /etc/passwd -p rwxa -k identity_changes

# Watch directory recursively
sudo auditctl -w /etc/ssh/ -p wa -k ssh_config_changes

# Monitor system call
sudo auditctl -a always,exit -S execve -k command_execution

# List rules
sudo auditctl -l

# Delete all rules
sudo auditctl -D
```

**Rule breakdown:**
- `-w` = watch file/directory
- `-p` = permissions: r=read, w=write, x=execute, a=attribute
- `-k` = search key
- `-S` = system call
- `-a` = add rule

### Making Rules Persistent

Edit `/etc/audit/rules.d/audit.rules`:

```
-w /etc/passwd -p rwxa -k identity_changes
-w /etc/shadow -p rwxa -k identity_changes
-w /etc/ssh/sshd_config -p wa -k ssh_config_changes
```

Then reload:

```bash
sudo augenrules --load
sudo systemctl restart auditd
```

### Searching Audit Logs – `ausearch`

```bash
sudo ausearch -k identity_changes
sudo ausearch -ua alice
sudo ausearch -ts today
sudo ausearch -p 1234
sudo ausearch -m SYSCALL -sv no      # failed syscalls
```

### Generating Audit Reports – `aureport`

```bash
sudo aureport          # summary
sudo aureport -au      # authentication failures
sudo aureport -l       # user logins
sudo aureport -f       # file access
sudo aureport -x       # command execution
```

---

## 10. Advanced Logging – Custom Application Integration

This section covers four methods to integrate custom applications with the system logging infrastructure.

### 10.1 Method 1: Application → Socket → rsyslog (Standard)

Most efficient local method. The application writes directly to the system's Unix domain socket.

**Python producer:**
```python
import logging
import logging.handlers

logger = logging.getLogger('MyApp')
handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

logger.info("Local standard log message")
```

**rsyslog rule** (`/etc/rsyslog.d/10-myapp.conf`):
```
if $programname == 'MyApp' then /var/log/myapp.log
& stop
```

**Test with `logger`:**
```bash
logger -t MyApp "Testing Local Standard Flow"
tail -f /var/log/myapp.log
```

### 10.2 Method 2: Hybrid Forwarder (Local + Remote)

Best practice: local backup + remote forwarding, with rsyslog buffering network outages.

**On remote receiver server** (`/etc/rsyslog.conf` or a drop‑in):
```
module(load="imtcp")
input(type="imtcp" port="514")

template(name="RemoteStore" type="string" string="/var/log/remote/%HOSTNAME%/%programname%.log")
*.* ?RemoteStore
```

**On client** (`/etc/rsyslog.d/30-forwarder.conf`):
```
if $programname == 'MyApp' then /var/log/myapp.log
if $programname == 'MyApp' then @@192.168.1.100:514
& stop
```

**Test:**
```bash
logger -t MyApp "Testing Hybrid Flow"
```

### 10.3 Method 3: Legacy File Ingestion (`imfile`)

Use when an application only writes to its own text file and cannot use sockets.

**rsyslog configuration** (`/etc/rsyslog.d/40-watcher.conf`):
```
module(load="imfile")

input(type="imfile"
      File="/opt/custom-app/app.log"
      Tag="LegacyApp"
      Severity="info")

if $programname == 'LegacyApp' then /var/log/legacy-managed.log
```

**Test by appending to the file:**
```bash
echo "App wrote this" >> /opt/custom-app/app.log
tail -f /var/log/legacy-managed.log
```

### 10.4 Method 4: Direct Remote Bypass (App → Remote)

Direct network logging without a local syslog daemon – useful for serverless or containers.

**Python producer:**
```python
import logging.handlers
logger = logging.getLogger('DirectApp')
handler = logging.handlers.SysLogHandler(address=('192.168.1.100', 514))
logger.addHandler(handler)
logger.info("Direct network bypass message")
```

**Test with `logger` (TCP):**
```bash
logger -T -n 192.168.1.100 -P 514 -t DirectApp "Testing Direct Network Bypass"
```

### Admin Troubleshooting Cheat Sheet

| Command | Purpose |
|---------|---------|
| `rsyslogd -N1` | Validate configuration syntax |
| `systemctl restart rsyslog` | Apply changes |
| `ls -l /dev/log` | Check socket symlink |
| `logger -p local0.err "Msg"` | Simulate a log message |
| `ss -tulpn \| grep 514` | Check if rsyslog is listening on port 514 |

### Log Rotation for Custom Logs

Create `/etc/logrotate.d/myapp`:

```
/var/log/myapp.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        /usr/bin/systemctl kill -s HUP rsyslog.service >/dev/null 2>&1 || true
    endscript
}
```

---

## 11. Complete Real‑World Production Scenario

This scenario walks through setting up a production server with proper time sync, persistent journal, custom application logging, log rotation, and auditing.

**Environment:** CentOS/RHEL 9, hostname `app01`, custom application `myapp` writing logs to `/var/log/myapp/app.log`.

### Step 1: Ensure Accurate Time with `chrony`

```bash
sudo dnf install -y chrony
sudo systemctl enable --now chronyd
sudo vi /etc/chrony.conf   # add pool lines as shown earlier
sudo systemctl restart chronyd
chronyc sources -v         # verify ^* source
timedatectl status         # check synchronised
```

### Step 2: Enable Persistent `systemd-journald`

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
sudo journalctl --flush
ls /var/log/journal/        # should contain machine‑ID directory
```

### Step 3: Configure `rsyslog` for the Application

```bash
sudo mkdir -p /var/log/myapp
sudo touch /var/log/myapp/app.log
sudo vi /etc/rsyslog.d/myapp.conf
```

Content:
```
module(load="imfile")

input(type="imfile"
      File="/var/log/myapp/app.log"
      Tag="myapp"
      Severity="info"
      Facility="local0")

local0.*    /var/log/myapp/rsyslog-processed.log
```

Restart and test:
```bash
sudo systemctl restart rsyslog
echo "Application started" | sudo tee -a /var/log/myapp/app.log
sleep 2
sudo tail /var/log/myapp/rsyslog-processed.log
journalctl -t myapp --since "1 minute ago"
```

### Step 4: Use `logger` to Simulate Application Messages

```bash
logger -p local0.warning -t MYAPP "Disk usage >80%"
logger -p local0.err -t MYAPP "Database connection failed"
journalctl -t MYAPP --since "1 minute ago"
```

### Step 5: Set Up Log Rotation

```bash
sudo vi /etc/logrotate.d/myapp
```

Content:
```
/var/log/myapp/app.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 0644 admin admin
    postrotate
        /bin/systemctl restart rsyslog > /dev/null 2>&1 || true
    endscript
}
```

Test:
```bash
sudo logrotate -d /etc/logrotate.d/myapp
sudo logrotate -f /etc/logrotate.d/myapp
ls -l /var/log/myapp/
```

### Step 6: Query Logs Like a Pro

```bash
journalctl -b
journalctl -t myapp -p err
journalctl --since "1 hour ago" -o json-pretty | less
dmesg -Tw          # follow kernel messages
dmesg --level=err,crit
```

### Step 7: Configure Auditing

```bash
sudo dnf install -y audit
sudo systemctl enable --now auditd
sudo vi /etc/audit/rules.d/audit.rules
```

Add:
```
-w /etc/passwd -p wa -k identity_changes
-w /etc/ssh/sshd_config -p wa -k ssh_config_changes
-w /var/log/myapp/ -p wa -k app_log_access
```

Load rules:
```bash
sudo augenrules --load
sudo systemctl restart auditd
sudo auditctl -l
```

Generate events:
```bash
sudo touch /etc/passwd
echo "test" | sudo tee -a /var/log/myapp/app.log
```

Search:
```bash
sudo ausearch -k identity_changes
sudo ausearch -k app_log_access
sudo aureport -k
```

### Step 8: Final Verification Checklist

- [ ] `chronyc sources -v` shows `^*`
- [ ] `timedatectl status` shows synchronised
- [ ] `/var/log/journal` contains files
- [ ] `/var/log/myapp/rsyslog-processed.log` receives messages
- [ ] `journalctl -t myapp` shows test messages
- [ ] `logrotate -d` passes and rotation works
- [ ] `dmesg -T` shows no critical hardware errors
- [ ] `sudo auditctl -l` lists active rules
- [ ] `sudo ausearch -k identity_changes` returns events
- [ ] Disk space is adequate (`df -h /var/log`)

---

## 12. Essential Log Commands – Quick Reference

| Command | Purpose |
|---------|---------|
| `tail -f /var/log/messages` | Follow log file (real‑time) |
| `head -20 /var/log/secure` | View first 20 lines |
| `less /var/log/maillog` | Page through large files |
| `grep "Failed password" /var/log/secure` | Search for patterns |
| `journalctl -u sshd -f` | Follow service logs via journal |
| `journalctl --since "1 hour ago"` | Recent logs |
| `logger "Test message"` | Send custom message to syslog |
| `logger -p local0.info -t SCRIPT "Hello"` | Tagged, facility‑specific |
| `dmesg -T | grep -i error` | Kernel errors with timestamps |
| `logrotate -d /etc/logrotate.conf` | Debug rotation |
| `chronyc sources -v` | Check NTP sources |
| `timedatectl status` | Check time sync |
| `auditctl -l` | List audit rules |
| `ausearch -k keyname` | Search audit logs by key |

---

## 13. Best Practices for Log Management

1. **Enable persistent journald** on all servers (`mkdir /var/log/journal`).
2. **Use both rsyslog and journald** – journal for fast search, rsyslog for remote forwarding.
3. **Configure logrotate** for all custom application logs.
4. **Keep accurate time** with `chrony` – logs without correct timestamps are nearly useless.
5. **Centralise logs** from all servers to a central syslog server or SIEM.
6. **Set appropriate log levels** – avoid excessive debug logs in production.
7. **Protect logs** – restrict access to `/var/log/secure`, `/var/log/audit/`.
8. **Monitor disk space** – use `logrotate` and alerts to prevent filling partitions.
9. **Use structured logging** (JSON) where possible – easier to parse and search.
10. **Document your logging configuration** – especially audit rules for compliance.

---

## 14. Practice Lab – Verify Your Understanding

1. View the last 20 lines of `/var/log/secure` (or `/var/log/auth.log`).
2. Follow the journal logs for the `sshd` service in real time.
3. Send a test log message with `logger` using facility `local5` and priority `warning`.
4. Enable persistent journald storage and verify logs exist in `/var/log/journal/`.
5. Check your system's time synchronisation status with `timedatectl`.
6. Add a logrotate rule for a custom log file that rotates daily, keeps 7 rotations, and compresses old logs.
7. Create an audit rule that monitors all writes to `/etc/hosts`. Generate an event and search for it with `ausearch`.
8. Use `dmesg` to check for hardware errors.

---

**Date documented:** 2026-04-25  
**Sources:** Red Hat System Administration, rsyslog documentation, systemd documentation, auditd man pages, chrony project

---
