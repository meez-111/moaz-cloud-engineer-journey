
# Chapter 10: Controlling Services and Daemons

## 1. The Linux Boot Process (Phases)

The boot process from power‑on to a fully functional system consists of several well‑defined stages.

| Phase | Component | What Happens |
|-------|-----------|---------------|
| 1 | **Power‑on** | User presses the power button; power supply stabilizes. |
| 2 | **BIOS/UEFI** | Basic Input/Output System initialises hardware (CPU, RAM, disk controllers). Performs Power‑On Self Test (POST). Locates the boot device (hard disk, USB, DVD) according to boot order. |
| 3 | **MBR / GPT** | Master Boot Record (first 512 bytes of disk) or GUID Partition Table contains the bootloader (e.g., GRUB). BIOS loads and executes the bootloader. |
| 4 | **Boot Loader** | GRUB (Grand Unified Bootloader) presents a menu (if multiple kernels). Loads the selected kernel into memory and passes control to it. |
| 5 | **Kernel** | The kernel initialises devices, mounts the initial RAM disk (`initramfs`), and starts the first user‑space process – **systemd** (PID 1). |
| 6 | **systemd (PID 1)** | The mother of all processes. It starts all other services, daemons, and targets according to its configuration. |

---

## 2. What is a Service / Daemon?

- **Daemon**: A background process that runs continuously, usually started at boot, without a controlling terminal. Examples: `sshd`, `cron`, `nginx`, `systemd-journald`.
- **Service**: A unit of work managed by systemd. Usually a daemon, but can also be a oneshot task (e.g., filesystem check).

**Key concept:** systemd treats nearly everything as a **unit**. Services are one type of unit.

---

## 3. systemd – The First Process (PID 1)

systemd is the default init system on most modern Linux distributions (RHEL 7+, CentOS 7+, Ubuntu 15.04+, Fedora, Debian 8+). It:

- Starts and manages services and daemons.
- Manages system state (targets, like runlevels).
- Tracks processes via cgroups.
- Provides logging via `journald`.
- Handles mount points, sockets, timers, and devices.

### Unit Types (Categories)

systemd organises resources into **unit files** with different suffixes.

| Unit Type | File Extension | Purpose |
|-----------|----------------|---------|
| `.service` | `.service` | A service (daemon) – most common. |
| `.socket` | `.socket` | Socket activation (listening on a socket). |
| `.target` | `.target` | Group of units (like runlevels). |
| `.timer` | `.timer` | Scheduled jobs (cron replacement). |
| `.path` | `.path` | Activates a service when a file/directory changes. |
| `.mount` | `.mount` | Filesystem mount point. |
| `.automount` | `.automount` | On‑demand mounting. |
| `.device` | `.device` | Kernel device (hotplug). |
| `.slice` | `.slice` | Resource isolation (cgroups). |

---

## 4. Service States – Understanding `systemctl status`

A service can be in several states. `systemctl status` shows:

| State | Meaning |
|-------|---------|
| **active (running)** | The service is running normally. |
| **active (exited)** | Service ran once and exited (e.g., oneshot). |
| **active (waiting)** | Service is running but waiting for something (e.g., a socket). |
| **inactive (dead)** | Service is not running. |
| **enabled** | Service will start automatically at boot. |
| **disabled** | Service will not start at boot. |
| **static** | Service cannot be enabled/disabled manually (controlled by kernel or another service). |
| **masked** | Service is completely disabled (cannot be started even manually). |
| **loaded** | Unit file was parsed successfully. |
| **failed** | Service crashed or exited with error. |

**Important distinction:**
- **active/inactive** refers to *current* running state.
- **enabled/disabled** refers to *boot‑time* behaviour.

---

## 5. `systemctl` – The Primary Command

`systemctl` is the main tool to control systemd.

### Basic Operations

| Operation | Command | Example |
|-----------|---------|---------|
| List all active units | `systemctl list-units` | `systemctl list-units` |
| List all units (including inactive) | `systemctl list-units --all` | |
| List only service units | `systemctl list-units --type=service` | |
| List all unit files (enabled/disabled) | `systemctl list-unit-files` | |
| Show status of a service | `systemctl status name` | `systemctl status sshd` |
| Start a service | `systemctl start name` | `sudo systemctl start nginx` |
| Stop a service | `systemctl stop name` | |
| Restart a service | `systemctl restart name` | (stops then starts) |
| Reload a service | `systemctl reload name` | Reload config **without** stopping (if supported) |
| Enable at boot | `systemctl enable name` | Creates symlink in `/etc/systemd/system/multi-user.target.wants/` |
| Disable at boot | `systemctl disable name` | Removes that symlink |
| Check if running | `systemctl is-active name` | Returns `active` or `inactive` (exit code 0/3) |
| Check if enabled | `systemctl is-enabled name` | Returns `enabled` or `disabled` |
| Mask (prevent any start) | `systemctl mask name` | Links unit to `/dev/null` |
| Unmask | `systemctl unmask name` | |
| Show dependencies | `systemctl list-dependencies name` | |
| Show system state | `systemctl is-system-running` | `running`, `degraded`, `maintenance` |

### Examples with Output

```bash
# Check if sshd is active
systemctl is-active sshd
# Output: active

# Check if sshd is enabled
systemctl is-enabled sshd
# Output: enabled

# View detailed status
systemctl status sshd
```

**Sample output of `systemctl status sshd`:**
```
● sshd.service - OpenSSH server daemon
   Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2026-04-20 09:00:00 UTC; 2h ago
     Docs: man:sshd(8)
 Main PID: 1234 (sshd)
    Tasks: 1 (limit: 4915)
   Memory: 2.5M
   CGroup: /system.slice/sshd.service
           └─1234 /usr/sbin/sshd -D
```

---

## 6. How systemd Enables/Disables a Service at Boot

When you run `systemctl enable service`, systemd creates a **symbolic link** from the service file (usually in `/usr/lib/systemd/system/`) to a `.wants/` directory inside the appropriate **target** (e.g., `multi-user.target.wants/`).

- **Enabling**: `ln -s /usr/lib/systemd/system/sshd.service /etc/systemd/system/multi-user.target.wants/sshd.service`
- **Disabling**: Removes that symlink.

The target determines when the service starts:

| Target | Equivalent old runlevel | Purpose |
|--------|------------------------|---------|
| `poweroff.target` | 0 | Shutdown |
| `rescue.target` | 1 | Single‑user mode |
| `multi-user.target` | 3 | Multi‑user, no GUI |
| `graphical.target` | 5 | Multi‑user with GUI |
| `reboot.target` | 6 | Reboot |

---

## 7. Anatomy of a systemd Service Unit File

A `.service` file is divided into sections. The most important are `[Unit]`, `[Service]`, and `[Install]`.

**Example:** `/usr/lib/systemd/system/sshd.service`

```ini
[Unit]
Description=OpenSSH server daemon
After=network.target        # Start after network is up

[Service]
Type=simple                 # Main process is the daemon
ExecStart=/usr/sbin/sshd -D # Command to start
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target  # Enable for multi‑user target
```

| Directive | Meaning |
|-----------|---------|
| `Type=` | `simple` (default), `forking`, `oneshot`, `notify`, `dbus` |
| `ExecStart` | Command to start the service |
| `ExecStop` | Command to stop (optional) |
| `ExecReload` | Command to reload configuration |
| `Restart=` | `no`, `on-failure`, `always`, `on-abort` |
| `User=` | Run as specific user (security) |
| `EnvironmentFile=` | Load environment variables from file |

---

## 8. Viewing Service Logs – `journalctl`

systemd collects logs from all services via its journal.

| Command | Purpose |
|---------|---------|
| `journalctl` | Show all logs (paged) |
| `journalctl -u service` | Show logs for a specific service |
| `journalctl -f` | Follow (tail) logs |
| `journalctl --since "1 hour ago"` | Time‑filtered |
| `journalctl -n 50` | Show last 50 lines |
| `journalctl -p err` | Show only error priority |

**Example:**
```bash
journalctl -u sshd -f
```

---

## 9. Legacy Init Systems (Comparison)

Before systemd, Linux used older init systems. Understanding them helps when working on older servers.

### SysVinit (used by RHEL 5/6, Debian 6/7)

- Scripts in `/etc/rc.d/init.d/` or `/etc/init.d/`
- Runlevels (0‑6) with symlinks in `/etc/rc?.d/`
- Commands: `service name start/stop/status`, `chkconfig on/off`
- **Limitations:** sequential startup (slow), no dependency management, no automatic restart.

### Upstart (used by Ubuntu 6.10 – 14.10, RHEL 6)

- Event‑based (starts services when events occur, e.g., filesystem mounted)
- Commands: `initctl start/stop/status`
- Hybrid model.

### Comparison Table

| Feature | SysVinit | Upstart | systemd |
|---------|----------|---------|---------|
| Startup | Sequential | Event‑driven | Parallel (aggressive) |
| Dependency handling | Manual (LSB headers) | Partial | Full (targets, `After=`, `Requires=`) |
| Logging | Each service logs separately | Optional | Integrated (`journald`) |
| Process tracking | PID files | Partial | cgroups (reliable) |
| Command | `service`, `chkconfig` | `initctl` | `systemctl` |

---

## 10. Analyzing Boot Performance with `systemd-analyze`

A critical tool for diagnosing slow boots and understanding startup dependencies.

| Command | Purpose |
|---------|---------|
| `systemd-analyze time` | Show total boot time (kernel + userspace) |
| `systemd-analyze blame` | List services sorted by initialization time (descending) |
| `systemd-analyze critical-chain` | Show the critical path of units that delayed reaching the default target |
| `systemd-analyze plot > boot.svg` | Generate a graphical timeline of the boot process |

**Example:**
```bash
systemd-analyze time
# Startup finished in 2.345s (kernel) + 8.912s (userspace) = 11.257s

systemd-analyze blame | head -5
# 6.123s NetworkManager-wait-online.service
# 3.456s docker.service
# 2.100s postgresql.service
```

---

## 11. systemd Timers – Modern Cron Replacement

Timers trigger service units at scheduled times. They are more flexible than cron: support calendar events, monotonic timers (e.g., "5 minutes after boot"), and can handle missed events.

**Example: Run a backup script daily at 2 AM**

`/etc/systemd/system/backup.service`:
```ini
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

`/etc/systemd/system/backup.timer`:
```ini
[Unit]
Description=Run backup daily at 2 AM

[Timer]
OnCalendar=daily
# Or specific time: OnCalendar=*-*-* 02:00:00
Persistent=true   # Run immediately if missed while system was off

[Install]
WantedBy=timers.target
```

**Commands:**
```bash
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
systemctl list-timers --all
```

---

## 12. Overriding Vendor Units with Drop‑in Files

Instead of editing `/usr/lib/systemd/system/` files directly (which can be overwritten by package updates), create **drop‑in** directories.

**Example:** Override `cron.service` to add an environment variable.

```bash
sudo mkdir -p /etc/systemd/system/cron.service.d
sudo tee /etc/systemd/system/cron.service.d/override.conf <<EOF
[Service]
Environment="MYAPP_DEBUG=true"
EOF
sudo systemctl daemon-reload
```

Verify:
```bash
systemctl show cron.service -p Environment
```

---

## 13. User Services – Managing Services Without Root

Users can run their own services with `systemctl --user`. This is ideal for user‑specific daemons (e.g., syncthing, gpg‑agent) or containerized environments.

**Create a user service:**
```bash
mkdir -p ~/.config/systemd/user
```

Create `~/.config/systemd/user/myservice.service`:
```ini
[Unit]
Description=My User Service

[Service]
ExecStart=/home/user/bin/myscript.sh
Restart=on-failure

[Install]
WantedBy=default.target
```

**Commands:**
```bash
systemctl --user daemon-reload
systemctl --user enable --now myservice.service
systemctl --user status myservice.service
```

**Enable lingering** so the service starts at boot even when the user is not logged in:
```bash
sudo loginctl enable-linger username
```

---

## 14. Common Troubleshooting Scenarios

### Service fails to start

1. `systemctl status service` – shows error message.
2. `journalctl -u service -n 50` – look for detailed errors.
3. Check syntax of unit file: `systemd-analyze verify service.service`.
4. Check that all `ExecStart` dependencies exist (e.g., binary path).

### Service enabled but not starting at boot

- `systemctl is-enabled service` → should return `enabled`.
- Check if it's masked: `systemctl is-enabled service` returns `masked`.
- Check that the target wants directory contains the symlink: `ls -l /etc/systemd/system/multi-user.target.wants/service.service`.

### Service restarts constantly

- `systemctl status` shows `active (running)` but then restarts.
- Check `Restart=` in unit file.
- Look for crashes in journal.

### "Unit file is masked"

- Cannot start/stop/enable. Unmask: `systemctl unmask service`.

---

## 15. Creating a Custom systemd Service (Example)

Let’s create a simple service that runs a Python script.

**Step 1:** Create script `/usr/local/bin/myservice.py`:
```python
#!/usr/bin/env python3
import time
while True:
    with open("/tmp/myservice.log", "a") as f:
        f.write("alive\n")
    time.sleep(60)
```
Make it executable: `chmod +x /usr/local/bin/myservice.py`

**Step 2:** Create unit file `/etc/systemd/system/myservice.service`:
```ini
[Unit]
Description=My custom Python service
After=network.target

[Service]
Type=simple
User=nobody
ExecStart=/usr/local/bin/myservice.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 3:** Reload systemd, start, enable:
```bash
sudo systemctl daemon-reload
sudo systemctl start myservice
sudo systemctl enable myservice
```

**Step 4:** Check status and logs:
```bash
sudo systemctl status myservice
sudo journalctl -u myservice -f
```

---

## 16. Quick Reference – `systemctl` Cheat Sheet

| Task | Command |
|------|---------|
| List active services | `systemctl list-units --type=service` |
| List all service files | `systemctl list-unit-files --type=service` |
| Start | `systemctl start name` |
| Stop | `systemctl stop name` |
| Restart | `systemctl restart name` |
| Reload config | `systemctl reload name` |
| Enable at boot | `systemctl enable name` |
| Disable at boot | `systemctl disable name` |
| Check if active | `systemctl is-active name` |
| Check if enabled | `systemctl is-enabled name` |
| Mask (cannot start) | `systemctl mask name` |
| Unmask | `systemctl unmask name` |
| Show dependencies | `systemctl list-dependencies name` |
| View logs | `journalctl -u name` |
| Follow logs | `journalctl -u name -f` |
| Reload systemd (after unit change) | `systemctl daemon-reload` |
| Show default target | `systemctl get-default` |
| Change default target | `systemctl set-default graphical.target` |
| Boot into rescue mode | `systemctl rescue` |
| Boot into emergency mode | `systemctl emergency` |
| Analyze boot time | `systemd-analyze time` |
| Show slow services | `systemd-analyze blame` |
| List timers | `systemctl list-timers` |

---

## 17. Practice Lab – Verify Your Understanding

1. Check the status of `sshd` (or `cron`). Determine if it's active and enabled.
2. Stop the `cron` service, verify it's inactive, then start it again.
3. Disable the `cron` service, reboot (or check the symlink), then re‑enable it.
4. View the last 20 log lines of `sshd` using `journalctl`.
5. Create a simple oneshot service that runs `echo "Hello"` and exits. Test it.
6. Mask the `cron` service, try to start it (should fail), then unmask it.
7. List all services that are currently failed (`systemctl --failed`).

---

## 18. Complete Practical Mastery Test – Controlling Services and Daemons

This test covers everything in this chapter. Perform all tasks on a systemd‑based Linux VM.

### Part 1: Boot Process and System State

**Task 1.1** – List the six phases of the Linux boot process in order.

**Task 1.2** – Use `systemd-analyze` to find:
- Total boot time.
- The service that took the longest to initialize.

**Task 1.3** – Determine the current default target. Then switch the default to `multi-user.target` (if not already). Verify and then restore the original.

**Task 1.4** – Check the overall system state with `systemctl is-system-running`. If it shows `degraded`, list the failed units.

---

### Part 2: Basic `systemctl` Operations

**Task 2.1** – List all active service units.

**Task 2.2** – List all service unit files (enabled/disabled/static) and count how many are enabled.

**Task 2.3** – Display the status of `sshd.service` (or `cron.service`). Identify:
- Loaded state and enablement status.
- Active state.
- Main PID.
- CGroup path.

**Task 2.4** – Stop the `cron` service. Verify it is inactive. Start it again.

**Task 2.5** – Disable `cron` from starting at boot. Check the symlink in `/etc/systemd/system/multi-user.target.wants/` to confirm it is removed. Then re‑enable it.

**Task 2.6** – Mask the `cron` service. Attempt to start it (should fail). Unmask it.

**Task 2.7** – Show the dependencies of `sshd.service` (or `multi-user.target`).

---

### Part 3: Unit Files – Inspection and Creation

**Task 3.1** – Use `systemctl cat` to view the full unit file of `sshd.service`.

**Task 3.2** – Explain the meaning of `Type=simple`, `Type=forking`, and `Type=oneshot`. Which type does `sshd.service` use?

**Task 3.3** – Create a custom service unit `/etc/systemd/system/hello.service` with:
- Description "Hello World Service"
- Type `oneshot`
- ExecStart `/bin/echo "Hello from systemd"`
- WantedBy `multi-user.target`

Reload systemd, start the service, and check its status. View its log with `journalctl`.

**Task 3.4** – Modify the service to run every boot. Enable it and verify with `systemctl is-enabled`.

**Task 3.5** – Create a persistent service `logger.service` that runs a simple shell loop writing a timestamp to `/tmp/logger.out` every 30 seconds. It should:
- Run as user `nobody`
- Restart on failure
- Be enabled at boot

---

### Part 4: systemd Timers

**Task 4.1** – Create a oneshot service `logtime.service` that runs `date >> /tmp/logtime.out`.

**Task 4.2** – Create a timer `logtime.timer` that triggers the service every 1 minute.

**Task 4.3** – Enable and start the timer. Use `systemctl list-timers` to verify it is scheduled.

---

### Part 5: Drop‑in Files

**Task 5.1** – Create a drop‑in directory for `cron.service` at `/etc/systemd/system/cron.service.d/`.

**Task 5.2** – Add a file `override.conf` that sets an environment variable `MYAPP_DEBUG=true`.

**Task 5.3** – Reload systemd and verify the environment variable is present in the service's properties (`systemctl show cron.service -p Environment`).

---

### Part 6: User Services

**Task 6.1** – As your normal user, create a user service `~/.config/systemd/user/mytimer.service` that runs `date >> /tmp/user-timer.log` (ensure `/tmp/user-timer.log` is writable).

**Task 6.2** – Start the user service with `systemctl --user start mytimer.service`. Verify it runs.

**Task 6.3** – Enable lingering for your user so user services can start at boot without login: `sudo loginctl enable-linger $USER`.

---

### Part 7: Log Analysis with `journalctl`

**Task 7.1** – Show all logs for the current boot.

**Task 7.2** – Show logs for `sshd.service` from the last 30 minutes.

**Task 7.3** – Follow the logs of `cron.service` in real time, then stop with `Ctrl+C`.

**Task 7.4** – Show only error‑priority messages for `sshd.service`.

---

### Part 8: Troubleshooting Scenarios

**Task 8.1** – Create a broken service `fail.service` with `ExecStart=/bin/false`. Start it. Use `systemctl status` and `journalctl -xe` to diagnose the failure. Then fix it by changing `ExecStart` to `/bin/true`.

**Task 8.2** – Simulate a service that constantly restarts. Create a service with `ExecStart=/bin/sleep 1` and `Restart=always`. Observe with `systemctl status`. Stop and disable it.

**Task 8.3** – Find all currently failed units using `systemctl --failed`.

---

### Part 9: Real‑World Scenarios

**Scenario 1: Web Server Configuration Reload** – You have `nginx.service` running. Show the command to reload its configuration without dropping connections.

**Scenario 2: Disabling an Unnecessary Service** – You find `bluetooth.service` enabled but the system has no Bluetooth hardware. Mask it completely.

**Scenario 3: Investigating a Service That Won't Start** – `mysqld.service` fails to start. List three commands you would run to investigate.

**Scenario 4: Boot Time Analysis for Cloud VM** – You suspect a cloud VM is booting slowly. What two `systemd-analyze` subcommands would you use first?

---

### Part 10: Cleanup

Remove all custom units, drop‑ins, and test files. Restore default target if changed. Disable lingering if desired.

---

## 19. Self‑Evaluation Checklist

| I can... | Done |
|----------|------|
| Describe the six boot phases and systemd's role | ☐ |
| Distinguish between active, enabled, static, and masked | ☐ |
| Use `systemctl` to start, stop, enable, disable, mask, unmask | ☐ |
| List units and unit files | ☐ |
| View and interpret `systemctl status` output | ☐ |
| Create a custom service unit (simple and oneshot) | ☐ |
| Understand service types (`simple`, `forking`, `oneshot`) | ☐ |
| Use `systemd-analyze` for boot performance | ☐ |
| Create a systemd timer and list active timers | ☐ |
| Override vendor units with drop‑in files | ☐ |
| Manage user services with `systemctl --user` | ☐ |
| Use `journalctl` to filter and follow logs | ☐ |
| Troubleshoot service failures using status and journal | ☐ |
| Reload systemd after unit changes (`daemon-reload`) | ☐ |

---

## 20. Answer Key

<details>
<summary><b>Click to reveal answers – attempt the test first!</b></summary>

### Part 1
**1.1** Power‑on → BIOS/UEFI → MBR/GPT → Boot Loader (GRUB) → Kernel → systemd (PID 1).
**1.2** `systemd-analyze time`; `systemd-analyze blame | head -5`.
**1.3** `systemctl get-default`; `sudo systemctl set-default multi-user.target`; restore with `sudo systemctl set-default graphical.target`.
**1.4** `systemctl is-system-running`; `systemctl --failed`.

### Part 2
**2.1** `systemctl list-units --type=service`.
**2.2** `systemctl list-unit-files --type=service | grep enabled | wc -l`.
**2.3** `systemctl status sshd`.
**2.4** `sudo systemctl stop cron`; `systemctl is-active cron`; `sudo systemctl start cron`.
**2.5** `sudo systemctl disable cron`; check symlink; `sudo systemctl enable cron`.
**2.6** `sudo systemctl mask cron`; `sudo systemctl start cron` → fails; `sudo systemctl unmask cron`.
**2.7** `systemctl list-dependencies sshd.service`.

### Part 3
**3.1** `systemctl cat sshd.service`.
**3.2** `simple`: main process is the service; `forking`: service forks and parent exits; `oneshot`: runs once and exits. `sshd` typically uses `notify` or `simple`.
**3.3** Create unit, `sudo systemctl daemon-reload`, `sudo systemctl start hello`, `sudo systemctl status hello`, `journalctl -u hello`.
**3.4** `sudo systemctl enable hello`.
**3.5** Unit with `Type=simple`, `ExecStart=/bin/sh -c 'while true; do date >> /tmp/logger.out; sleep 30; done'`, `User=nobody`, `Restart=on-failure`, `WantedBy=multi-user.target`.

### Part 4
**4.1** Unit with `Type=oneshot`, `ExecStart=/bin/sh -c 'date >> /tmp/logtime.out'`.
**4.2** Timer with `[Timer] OnCalendar=*:0/1` (every minute) and `[Install] WantedBy=timers.target`.
**4.3** `sudo systemctl enable --now logtime.timer`; `systemctl list-timers`.

### Part 5
**5.1** `sudo mkdir -p /etc/systemd/system/cron.service.d`.
**5.2** Create `override.conf` with `[Service] Environment="MYAPP_DEBUG=true"`.
**5.3** `sudo systemctl daemon-reload`; `systemctl show cron.service -p Environment`.

### Part 6
**6.1** `mkdir -p ~/.config/systemd/user`; create service file.
**6.2** `systemctl --user daemon-reload`; `systemctl --user start mytimer.service`.
**6.3** `sudo loginctl enable-linger $USER`.

### Part 7
**7.1** `journalctl -b`.
**7.2** `journalctl -u sshd --since "30 minutes ago"`.
**7.3** `journalctl -u cron -f`.
**7.4** `journalctl -u sshd -p err`.

### Part 8
**8.1** `sudo systemctl start fail`; `systemctl status fail`; `journalctl -xe`; edit to `ExecStart=/bin/true`.
**8.2** Service with `ExecStart=/bin/sleep 1` and `Restart=always`. Stop with `sudo systemctl stop`.
**8.3** `systemctl --failed`.

### Part 9
**Scenario 1:** `sudo systemctl reload nginx`.
**Scenario 2:** `sudo systemctl mask bluetooth`.
**Scenario 3:** `systemctl status mysqld`, `journalctl -u mysqld -n 50`, `systemctl cat mysqld`.
**Scenario 4:** `systemd-analyze blame` and `systemd-analyze critical-chain`.

### Part 10
Remove custom files, run `daemon-reload`. Restore default target. `sudo loginctl disable-linger $USER`.

</details>

---

**Date documented:** 2026-04-20  
**Sources:** Red Hat System Administration, systemd documentation, man pages