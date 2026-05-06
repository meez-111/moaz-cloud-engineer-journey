# Chapter 3: Scheduling Future Tasks – Complete Professional Guide

## Table of Contents

- [Chapter 3: Scheduling Future Tasks – Complete Professional Guide](#chapter-3-scheduling-future-tasks--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. What is Task Scheduling? Why Do We Need It?](#1-what-is-task-scheduling-why-do-we-need-it)
  - [2. Types of Scheduling (Time Perspective)](#2-types-of-scheduling-time-perspective)
  - [3. `at` – One‑Time Task Scheduling](#3-at--onetime-task-scheduling)
    - [3.1 Installing and Enabling `atd`](#31-installing-and-enabling-atd)
    - [3.2 Syntax and Time Specification](#32-syntax-and-time-specification)
    - [3.3 `at` Command Options](#33-at-command-options)
    - [3.4 Batch Processing with `batch`](#34-batch-processing-with-batch)
    - [3.5 Managing Jobs (`atq`, `atrm`)](#35-managing-jobs-atq-atrm)
    - [3.6 File Locations and Logs](#36-file-locations-and-logs)
  - [4. `cron` – Periodic Task Scheduling](#4-cron--periodic-task-scheduling)
    - [4.1 Installing and Enabling `crond`](#41-installing-and-enabling-crond)
    - [4.2 Crontab Format (Minute, Hour, Day, Month, Weekday)](#42-crontab-format-minute-hour-day-month-weekday)
    - [4.3 Special Strings (Shortcuts)](#43-special-strings-shortcuts)
    - [4.4 Crontab Management (`crontab -e`, `-l`, `-r`, `-u`)](#44-crontab-management-crontab--e--l--r--u)
    - [4.5 System Crontab and Drop‑In Directories](#45-system-crontab-and-dropin-directories)
    - [4.6 Environment Variables in Cron](#46-environment-variables-in-cron)
    - [4.7 Logging and Debugging](#47-logging-and-debugging)
  - [5. `anacron` – Periodic Tasks with Boot‑Time Catch‑Up](#5-anacron--periodic-tasks-with-boottime-catchup)
    - [5.1 Why anacron? Problem It Solves](#51-why-anacron-problem-it-solves)
    - [5.2 Configuration File (`/etc/anacrontab`)](#52-configuration-file-etcanacrontab)
    - [5.3 How Anacron Works](#53-how-anacron-works)
    - [5.4 Differences from Cron](#54-differences-from-cron)
  - [6. `systemd` Timers – Modern Periodic Scheduling](#6-systemd-timers--modern-periodic-scheduling)
    - [6.1 Why Systemd Timers?](#61-why-systemd-timers)
    - [6.2 Structure: `.timer` + `.service` Unit Files](#62-structure-timer--service-unit-files)
      - [Service unit (`/etc/systemd/system/mybackup.service`)](#service-unit-etcsystemdsystemmybackupservice)
      - [Timer unit (`/etc/systemd/system/mybackup.timer`)](#timer-unit-etcsystemdsystemmybackuptimer)
    - [6.3 `OnCalendar` Syntax (Date/Time Specifications)](#63-oncalendar-syntax-datetime-specifications)
    - [6.4 Other Timer Types (Not Only Calendar)](#64-other-timer-types-not-only-calendar)
    - [6.5 Managing Timers (Enable, Start, List, Status)](#65-managing-timers-enable-start-list-status)
    - [6.6 Example: Creating a Custom Timer](#66-example-creating-a-custom-timer)
  - [7. Quick Reference Table](#7-quick-reference-table)
  - [8. Real‑World Scenario – Comprehensive Server Maintenance Scheduling](#8-realworld-scenario--comprehensive-server-maintenance-scheduling)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [Step 1 – Schedule the one‑time reboot with `at`](#step-1--schedule-the-onetime-reboot-with-at)
      - [Step 2 – User cron job for nightly backup](#step-2--user-cron-job-for-nightly-backup)
      - [Step 3 – User cron job for developer](#step-3--user-cron-job-for-developer)
      - [Step 4 – System‑wide daily script via drop‑in](#step-4--systemwide-daily-script-via-dropin)
      - [Step 5 – Verify anacron for missed daily jobs on `dev01`](#step-5--verify-anacron-for-missed-daily-jobs-on-dev01)
      - [Step 6 – Create a systemd timer for health checks](#step-6--create-a-systemd-timer-for-health-checks)
  - [9. Practice Lab – Verify Your Understanding](#9-practice-lab--verify-your-understanding)

---

## 1. What is Task Scheduling? Why Do We Need It?

**Task scheduling** means automatically executing commands, scripts, or programs at a specified future time or at regular intervals.

**Why do we need it?**

- **System maintenance:** Daily log rotation (`logrotate`), temporary file cleanup (`tmpwatch`), database backups.
- **Security:** Regular vulnerability scans, SELinux relabeling, certificate renewal.
- **User tasks:** Sending reminder emails, generating reports, synchronising data.
- **Resource optimisation:** Running heavy jobs during off‑peak hours (nightly batch processing).

**Examples:**
- Run a backup script every night at 2:00 AM.
- Send a report every Monday at 9:00 AM.
- Execute a one‑time command to reboot the server at 3:00 AM next Sunday.

---

## 2. Types of Scheduling (Time Perspective)

| Type | Description | Tool(s) |
|------|-------------|---------|
| **One‑time / at** | Execute a command **exactly once** at a specified future time. | `at`, `batch` (atd) |
| **Periodic** | Execute repeatedly at fixed intervals (minutes, hours, days, weeks, months). | `cron` (crond), `systemd timers` |
| **Periodic with boot‑time catch‑up** | Like cron, but if the system was down when a job should have run, it runs after the next boot. | `anacron` |

---

## 3. `at` – One‑Time Task Scheduling

The `at` command schedules a command or script to run **once** at a specified future time. The `atd` daemon runs these jobs.

### 3.1 Installing and Enabling `atd`

```bash
# Install (if not present)
sudo dnf install at

# Enable and start the service
sudo systemctl enable --now atd

# Verify
sudo systemctl status atd
```

### 3.2 Syntax and Time Specification

```bash
at [options] time
```

After typing `at time`, you enter the command(s) on the following lines, then press `Ctrl+D` to finish.

**Time formats (very flexible):**

| Example | Meaning |
|---------|---------|
| `at 15:30` | Today at 3:30 PM (if later than now), otherwise tomorrow. |
| `at 15:30 tomorrow` | Tomorrow at 3:30 PM. |
| `at 23:45 2026-12-31` | Specific date (YYYY-MM-DD). |
| `at now + 5 minutes` | 5 minutes from now. |
| `at noon + 3 days` | 3 days from now at noon. |
| `at 4pm + 2 weeks` | 2 weeks from now at 4 PM. |
| `at 09:00 next month` | Same day next month at 9:00 AM. |
| `at teatime` | 4:00 PM (16:00). |
| `at midnight` | 00:00. |
| `at 13:59 05.06.26` | Date in DD.MM.YY format. |

### 3.3 `at` Command Options

| Option | Meaning | Example |
|--------|---------|---------|
| `-f file` | Read commands from a file instead of stdin. | `at -f script.sh 09:00` |
| `-m` | Send mail to the user even if command produces no output. | `at -m 06:00` |
| `-M` | Never send mail (overrides `-m`). | `at -M 06:00` |
| `-q queue` | Use a specific queue (a–z, A–Z). Higher letter = lower priority. | `at -q b 23:00` |
| `-l` | List pending jobs (same as `atq`). | `at -l` |
| `-r job_id` | Remove a job (same as `atrm`). | `at -r 5` |
| `-d` | Same as `-r`. | |
| `-v` | Show the time the job will be executed (verbose). | `at -v 16:00` |
| `-c job_id` | Display the job’s content (commands). | `at -c 7` |

### 3.4 Batch Processing with `batch`

`batch` (or `at -b`) executes commands when system load drops below a certain level (typically 1.5). Jobs are queued and run as soon as resources allow.

```bash
batch
> echo "Heavy computation starts" > /tmp/batch.log
> ./bigjob.sh
> ^D
```

### 3.5 Managing Jobs (`atq`, `atrm`)

```bash
atq                     # list pending jobs (job ID, time, queue, user)
atq -q a               # list only queue a

atrm 5                 # remove job with ID 5
atrm 2 4 7             # remove multiple jobs
atrm -q b              # remove all jobs in queue b
```

### 3.6 File Locations and Logs

| File/Directory | Purpose |
|----------------|---------|
| `/var/spool/at/` | Spool directory for `at` jobs (should not be manually edited). |
| `/etc/at.allow` | List of users allowed to use `at` (one user per line). If this file exists, only listed users can use `at`. |
| `/etc/at.deny` | List of users **denied** to use `at` (default: empty). If `at.allow` does not exist, `at.deny` is checked. |
| `/var/log/cron` (or `journalctl`) | Logs of `at` job executions (since `at` logs via syslog). |

**Check `at` logs:**
```bash
journalctl -u atd
```

---

## 4. `cron` – Periodic Task Scheduling

`cron` is the classic Linux scheduler for executing commands at fixed intervals (minutes, hours, days, weeks, months). The `crond` daemon reads crontab files.

### 4.1 Installing and Enabling `crond`

```bash
sudo dnf install cronie          # if not present
sudo systemctl enable --now crond
sudo systemctl status crond
```

### 4.2 Crontab Format (Minute, Hour, Day, Month, Weekday)

A crontab line has **6 fields** (5 time fields + command). The format:

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0–7, where 0 and 7 = Sunday)
│ │ │ └───── Month (1–12)
│ │ └─────── Day of month (1–31)
│ └───────── Hour (0–23)
└─────────── Minute (0–59)
```

**Special characters:**
- `*` – Any value (every minute, every hour, etc.)
- `,` – List separator: `1,15,30` (minutes 1, 15, 30)
- `-` – Range: `1-5` (Monday to Friday)
- `/` – Step: `*/15` (every 15 minutes)

**Examples:**

| Cron expression | Meaning |
|----------------|---------|
| `0 2 * * *` | At 2:00 AM every day. |
| `*/5 * * * *` | Every 5 minutes. |
| `0 9 * * 1-5` | At 9:00 AM Monday through Friday. |
| `0 0 1 * *` | At midnight on the 1st day of every month. |
| `15 3 * * 0` | At 3:15 AM every Sunday. |
| `0 22 15 * *` | At 10:00 PM on the 15th of every month. |
| `*/10 8-17 * * 1-5` | Every 10 minutes between 8 AM and 5 PM, weekdays. |

### 4.3 Special Strings (Shortcuts)

| String | Equivalent | Meaning |
|--------|------------|---------|
| `@reboot` | (no time) | Run once at system startup. |
| `@yearly` | `0 0 1 1 *` | At midnight on January 1. |
| `@annually` | same as `@yearly` | – |
| `@monthly` | `0 0 1 * *` | At midnight on the first of each month. |
| `@weekly` | `0 0 * * 0` | At midnight on Sunday. |
| `@daily` | `0 0 * * *` | At midnight every day. |
| `@hourly` | `0 * * * *` | At the beginning of every hour. |

**Example:**
```cron
@reboot /usr/local/bin/start-my-service.sh
@hourly /usr/bin/update-cache
```

### 4.4 Crontab Management (`crontab -e`, `-l`, `-r`, `-u`)

| Command | Purpose |
|---------|---------|
| `crontab -e` | Edit the current user’s crontab (default editor). |
| `crontab -l` | List current user’s crontab entries. |
| `crontab -r` | Remove current user’s crontab. |
| `crontab -i` | Prompt before removal (use with `-r`). |
| `crontab -u username` | Operate on another user’s crontab (requires root). |

**Example (as root):**
```bash
crontab -u alice -e          # edit alice's crontab
crontab -u alice -l          # list alice's jobs
```

**Note:** User crontabs are stored in `/var/spool/cron/` (do not edit directly). Always use the `crontab` command.

### 4.5 System Crontab and Drop‑In Directories

- **System crontab:** `/etc/crontab` – has an **extra field** (user) between time and command.

```bash
# /etc/crontab format:
* * * * * username command
```

Example:
```
0 2 * * * root /usr/local/bin/backup.sh
```

- **Drop‑in directories:** Put scripts in these directories to run automatically.

| Directory | Run frequency |
|-----------|---------------|
| `/etc/cron.hourly/` | Every hour (run by `run-parts` from `/etc/crontab`) |
| `/etc/cron.daily/` | Every day |
| `/etc/cron.weekly/` | Every week |
| `/etc/cron.monthly/` | Every month |

Scripts placed in these directories must be executable and must **not** have a file extension (or must be plain scripts without `.sh` extensions because `run-parts` excludes dot files and some patterns).

- **Custom system cron jobs:** `/etc/cron.d/` – files in this directory follow the `/etc/crontab` format (with user field).

Example `/etc/cron.d/myapp`:
```
*/10 * * * * myuser /home/myuser/check-status.sh
```

### 4.6 Environment Variables in Cron

Cron jobs run with a minimal environment: `SHELL=/bin/sh`, `PATH=/usr/bin:/bin`, etc. To set environment variables, add them at the top of the crontab:

```cron
MAILTO=admin@example.com
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
SHELL=/bin/bash

10 1 * * * /opt/myapp/backup.sh
```

**Redirect output to avoid mail spamming:**
```cron
0 3 * * * /backup/run.sh > /dev/null 2>&1
```

### 4.7 Logging and Debugging

- **Log file:** `/var/log/cron` (traditional) or `journalctl`.
- **Check logs:**
  ```bash
  journalctl -u crond
  tail -f /var/log/cron
  ```
- **Debug a cron job:** Redirect output to a file and capture errors.
  ```cron
  5 * * * * /usr/bin/myjob >> /tmp/myjob.log 2>&1
  ```

---

## 5. `anacron` – Periodic Tasks with Boot‑Time Catch‑Up

`anacron` is designed to run periodic tasks even when the system is not running 24/7 (e.g., laptops, desktops). If a scheduled job was missed because the system was powered off, `anacron` runs it after next boot with a **delay**.

### 5.1 Why anacron? Problem It Solves

- **Cron limitation:** If a cron job was scheduled at 2:00 AM and the system is off at that time, the job is **never** run.
- **Anacron solution:** It records the last execution date. If a job should have run but didn’t, it runs shortly after boot (with a random delay to avoid boot‑time congestion).

### 5.2 Configuration File (`/etc/anacrontab`)

Format:
```
period delay job-identifier command
```

- **period** – Frequency in days (e.g., `1` = daily, `7` = weekly, `30` = monthly).
- **delay** – Minutes to wait **after boot** before running the job (random extra delay is added).
- **job-identifier** – Unique name for log messages (any string).
- **command** – The command to run (usually invoking `run-parts`).

**Default `/etc/anacrontab`:**
```
# period in days   delay in minutes   job-identifier   command
1		5		cron.daily		run-parts /etc/cron.daily
7		10		cron.weekly		run-parts /etc/cron.weekly
30		15		cron.monthly		run-parts /etc/cron.monthly
```

**Important:** Anacron is typically invoked by **cron** itself (either `/etc/crontab` or `/etc/cron.hourly/anacron`). On RHEL, anacron runs daily via cron.

### 5.3 How Anacron Works

1. On boot (or when anacron runs), it reads `/var/spool/anacron/` to see last execution dates.
2. For each job, it checks if the next scheduled run is in the past.
3. If missed, it runs the command after the specified **delay** (plus a random offset to avoid all jobs starting simultaneously).
4. Updates the timestamp in `/var/spool/anacron/`.

### 5.4 Differences from Cron

| Feature | Cron | Anacron |
|---------|------|---------|
| Intended for | Servers running 24/7 | Desktops/laptops that may be off |
| Sub‑minute granularity | Yes (minutes) | No (days only) |
| User crontabs | Yes (per user) | No (system‑wide only) |
| Runs after reboot to catch up | No | Yes |
| Random delay to avoid congestion | No | Yes |

**Note:** For modern laptops, `anacron` ensures that backup scripts, log rotations, and other maintenance still happen even if the machine was off overnight.

---

## 6. `systemd` Timers – Modern Periodic Scheduling

**Systemd timers** are the modern replacement for cron and anacron on RHEL 7+. They integrate with systemd services, provide flexible calendar expressions, and support monotonic timers (relative to boot).

### 6.1 Why Systemd Timers?

- **Integration with systemd** – can trigger any service unit, not just commands.
- **More precise** – supports sub‑second granularity.
- **Better logging** – integration with `journald`.
- **Advanced scheduling** – calendar events (like `OnCalendar`) and monotonic timers (`OnBootSec`, `OnUnitActiveSec`).
- **Persistent timers** – catch up missed runs (`Persistent=true`).

### 6.2 Structure: `.timer` + `.service` Unit Files

A timer unit defines **when** to run; a service unit defines **what** to run. Both files must have the same base name (unless otherwise specified).

**Example: `mybackup.timer`** and **`mybackup.service`**.

#### Service unit (`/etc/systemd/system/mybackup.service`)
```ini
[Unit]
Description=My backup script

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

#### Timer unit (`/etc/systemd/system/mybackup.timer`)
```ini
[Unit]
Description=Run my backup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### 6.3 `OnCalendar` Syntax (Date/Time Specifications)

`OnCalendar` uses a flexible syntax similar to cron but more readable.

**Basic format:** `DayOfWeek YYYY-MM-DD HH:MM:SS`

**Common examples:**

| OnCalendar expression | Meaning |
|----------------------|---------|
| `daily` | Every day at 00:00:00. |
| `hourly` | At the beginning of every hour. |
| `weekly` | Every Monday at 00:00:00. |
| `monthly` | Every first day of the month at 00:00:00. |
| `*:0/15` | Every 15 minutes (`/15`). |
| `*-*-* 02:00:00` | Every day at 2:00 AM. |
| `Mon..Fri 09:00:00` | Weekdays at 9:00 AM. |
| `Sat,Sun 22:30:00` | Weekends at 10:30 PM. |
| `2026-12-31 23:59:59` | One‑time at New Year’s Eve 2026. |

**Repetition:** `OnCalendar=*:*:0/10` (every 10 seconds – not recommended for heavy tasks).

### 6.4 Other Timer Types (Not Only Calendar)

| Timer type | Meaning |
|------------|---------|
| `OnActiveSec` | Time after the timer itself is activated. |
| `OnBootSec` | Time after boot. |
| `OnStartupSec` | Time after the systemd service manager starts (very early). |
| `OnUnitActiveSec` | Time after the service unit was last activated. |
| `OnCalendar` | Real‑time calendar schedule. |

**Example – run 5 minutes after boot:**
```ini
[Timer]
OnBootSec=5min
```

**Example – run every 2 hours after the service finished its last run:**
```ini
[Timer]
OnUnitActiveSec=2h
```

**Combine types:** You can specify more than one; the next trigger is the earliest.

### 6.5 Managing Timers (Enable, Start, List, Status)

```bash
# Enable and start a timer
sudo systemctl enable --now mybackup.timer

# List all active timers
systemctl list-timers

# List all timers (including inactive)
systemctl list-timers --all

# Show status of a specific timer
systemctl status mybackup.timer

# Show next execution time of a timer
systemctl show mybackup.timer -p NextElapseUSecMonotonic
# or (human‑readable)
systemctl status mybackup.timer | grep "Trigger:"

# Disable and stop
sudo systemctl disable --now mybackup.timer

# View logs of the triggered service
journalctl -u mybackup.service
```

**Important:** The service does **not** have to be enabled; the timer will start it when triggered.

### 6.6 Example: Creating a Custom Timer

**Step 1: Create the service unit** – `/etc/systemd/system/cleanup.service`

```ini
[Unit]
Description=Clean temporary files

[Service]
Type=oneshot
ExecStart=/usr/bin/find /tmp -type f -atime +7 -delete
```

**Step 2: Create the timer unit** – `/etc/systemd/system/cleanup.timer`

```ini
[Unit]
Description=Run cleanup daily at 3am

[Timer]
OnCalendar=03:00:00
Persistent=yes   # catch up if missed due to power off

[Install]
WantedBy=timers.target
```

**Step 3: Reload systemd and start the timer**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cleanup.timer
```

**Verify:**
```bash
systemctl list-timers | grep cleanup
```

---

## 7. Quick Reference Table

| Task | Command |
|------|---------|
| Schedule one‑time job at 2:30 PM | `at 14:30` |
| List pending `at` jobs | `atq` |
| Remove `at` job #5 | `atrm 5` |
| Edit your crontab | `crontab -e` |
| List your crontab | `crontab -l` |
| Edit root’s crontab | `sudo crontab -e` |
| System crontab file | `/etc/crontab` |
| Drop‑in directory for scripts | `/etc/cron.daily/`, etc. |
| Run a cron job every 10 minutes | `*/10 * * * * command` |
| Run a cron job at 2:30 AM every day | `30 2 * * * command` |
| Run a cron job every Monday at 9 AM | `0 9 * * 1 command` |
| Check logs of cron jobs | `journalctl -u crond` |
| Edit anacron configuration | `/etc/anacrontab` |
| List all systemd timers | `systemctl list-timers` |
| Create a systemd timer | create `.timer` and `.service` units, then `enable --now` |
| Check next trigger of a timer | `systemctl status mytimer.timer` |

---

## 8. Real‑World Scenario – Comprehensive Server Maintenance Scheduling

### Background

You manage a small group of servers: `web01` (production web server) and `dev01` (development workstation). You need to set up the following automated tasks:

- **One‑time:** At 23:00 tonight, reboot `web01` because a kernel update was installed an hour ago, but the server must stay up during business hours.
- **Periodic (cron):**  
  - On `web01`, run a daily backup script (`/opt/scripts/backup.sh`) at 2:15 AM.  
  - On `dev01`, a developer’s crontab should run a script (`~/bin/fetch-data.sh`) every Monday at 9:00 AM and redirect output to a log.
- **System periodic:** Place a script `/opt/scripts/disk-cleanup.sh` in the appropriate drop‑in directory so it runs **daily** system‑wide.
- **Boot‑time catch‑up (anacron):** On `dev01` (which may be powered off at night), ensure that the daily system maintenance jobs (from `cron.daily`) still run even if the machine missed them overnight.
- **Modern scheduling (systemd timer):** Create a systemd timer that runs a health‑check service (`/usr/local/bin/healthcheck.sh`) every 30 minutes on `web01`, with persistent catching up if the server was down.

### Step‑by‑Step Implementation

#### Step 1 – Schedule the one‑time reboot with `at`

On `web01`:
```bash
sudo at 23:00
> /usr/sbin/reboot
> ^D
```
Verify with `atq`. The job runs once at 11 PM.

#### Step 2 – User cron job for nightly backup

As the `backup` user on `web01`:
```bash
crontab -e
```
Add:
```cron
15 2 * * * /opt/scripts/backup.sh > /var/log/backup/backup.log 2>&1
```
Save. Confirm with `crontab -l`.

#### Step 3 – User cron job for developer

As the developer on `dev01`:
```bash
crontab -e
```
Add:
```cron
0 9 * * 1 /home/devuser/bin/fetch-data.sh >> /home/devuser/fetch.log 2>&1
```

#### Step 4 – System‑wide daily script via drop‑in

Place the script in `/etc/cron.daily/` (ensure it has no `.sh` extension according to `run-parts`):
```bash
sudo cp /opt/scripts/disk-cleanup.sh /etc/cron.daily/disk-cleanup
sudo chmod +x /etc/cron.daily/disk-cleanup
```
The script will run every day when the `cron.daily` job is executed (around 4–6 AM depending on cron configuration).

#### Step 5 – Verify anacron for missed daily jobs on `dev01`

Check `/etc/anacrontab`; the default entries will invoke `run-parts /etc/cron.daily` with a 5‑minute delay. Since `anacron` is triggered by cron, it will catch up when the machine boots. Simulate a missed day by powering off the machine before midnight, then booting it in the morning. The daily jobs will run shortly after boot.

#### Step 6 – Create a systemd timer for health checks

On `web01`:

**1. Service unit** `/etc/systemd/system/healthcheck.service`:
```ini
[Unit]
Description=Server Health Check

[Service]
Type=oneshot
ExecStart=/usr/local/bin/healthcheck.sh
```

**2. Timer unit** `/etc/systemd/system/healthcheck.timer`:
```ini
[Unit]
Description=Run health check every 30 minutes

[Timer]
OnCalendar=*:0/30
Persistent=true

[Install]
WantedBy=timers.target
```

**3. Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now healthcheck.timer
```

**4. Verify:**
```bash
systemctl list-timers | grep healthcheck
journalctl -u healthcheck.service
```

---

Now all tasks are scheduled appropriately, combining the strengths of each tool.

---

## 9. Practice Lab – Verify Your Understanding

1. **`at`:** Schedule a command to create a file in `/tmp` 3 minutes from now. Use `atq` to list the job, then wait and verify the file was created.
2. **`atrm`:** Schedule two `at` jobs, then remove one of them with `atrm`.
3. **Crontab (user):** Write a crontab entry that appends the current date and time to `~/cron-test.log` every hour at minute 0.
4. **Crontab (system):** Create a script `/usr/local/bin/disk-check.sh` that logs disk usage. Add a system cron job (in `/etc/crontab`) to run it as root every day at 4 AM.
5. **Anacron:** Check your `/etc/anacrontab`. Identify the delay for `cron.daily`. Explain when a daily job would run if the system was off for two days.
6. **Systemd timer:** Create a service and timer that runs `echo "Hello timer" >> /tmp/timer.log` every 2 minutes. Enable and start the timer. Verify with `systemctl list-timers` and check the log file.
7. **Persistent timer:** Modify the timer to have `Persistent=true`. Stop the timer, manually change the system clock to one hour ahead, then restart the timer – observe if it runs immediately to catch up.
8. **Logs:** Find the last execution time of your systemd timer in `journalctl`.

---

**Date documented:** 2026-05-06  
**Sources:** Red Hat System Administration, `at`/`cron`/`anacron` man pages, systemd.timer documentation

---
