
# Chapter 9: Monitoring and Managing Linux Processes

## 1. What is a Process?

A **process** is a running instance of a program. Every command you execute creates one or more processes.

**As a sysadmin/cloud engineer, you need to:**
- List / monitor processes
- Control them (pause, resume)
- Kill them (when unresponsive)
- Set / change their priority

---

## 2. Process Identifiers (PID and PPID)

| Term | Meaning |
|------|---------|
| **PID** | Process ID – a unique 5‑digit number assigned to each process |
| **PPID** | Parent Process ID – the PID of the process that started this process |

- No two running processes share the same PID.
- After a process ends, its PID may be reused later.
- The first process started at boot is `init` or `systemd` (PID 1).

---

## 3. Process States (Status Codes)

When you run `ps` or `top`, you’ll see a status letter:

| State | Symbol | Meaning |
|-------|--------|---------|
| **Running** | `R` | Currently executing or ready to run |
| **Interruptible Sleep** | `S` | Waiting for an event (e.g., user input, disk I/O). Can be interrupted. |
| **Uninterruptible Sleep** | `D` | Waiting for I/O (e.g., disk) – cannot be interrupted. Usually indicates disk/network latency. |
| **Stopped** | `T` | Suspended by a job control signal (e.g., `Ctrl+Z`) |
| **Zombie** | `Z` | Process has finished but parent hasn't read its exit status. Consumes almost no resources but remains in process table. |
| **Idle** | `I` | Idle kernel thread (Linux specific) |

### Zombie Processes Explained
- A child process finishes, sends `SIGCHLD` to parent.
- If parent doesn't "reap" it (call `wait()`), the child becomes a zombie.
- Zombies cannot be killed with `kill -9` – you must kill the parent or reboot.
- Harmless in small numbers; many zombies indicate a buggy parent.

### Orphan Processes
- When a parent dies before its child, the child becomes an **orphan**.
- Orphans are automatically adopted by `init`/`systemd` (PID 1), which will clean them up.

### Daemon Processes
- Background system processes that run continuously (e.g., `sshd`, `cron`, `nginx`).
- No associated terminal (TTY = `?` in `ps` output).
- Usually start at boot and run with root or service user privileges.

---

## 4. Foreground vs Background Processes

| Mode | Behavior |
|------|----------|
| **Foreground** | Runs in the terminal, blocks it until finished. Takes keyboard input. Default mode. |
| **Background** | Runs independently; terminal remains free. Add `&` at the end of the command. |

**Example:**
```bash
sleep 60 &          # runs in background
[1] 2456            # job number 1, PID 2456
```

---

## 5. Job Control Commands (for shell sessions)

| Command | Purpose |
|---------|---------|
| `Ctrl+Z` | Suspend the current foreground process (stops it, puts in background) |
| `jobs` | List all jobs (stopped or background) for the current shell |
| `bg %job_number` | Resume a stopped job in the background |
| `fg %job_number` | Bring a background job to the foreground |
| `&` at end | Start a command directly in the background |
| `disown` | Detach a background job from the shell so it survives logout |

**Example session:**
```bash
sleep 300
^Z                 # Ctrl+Z
[1]+  Stopped      sleep 300

jobs
[1]+  Stopped      sleep 300

bg %1
[1]+ sleep 300 &

fg %1
sleep 300          # now in foreground
```

---

## 6. `ps` – Process Snapshot (Static)

**Abbreviation:** process status  
**Explanation:** Takes a static snapshot of processes at the moment the command is run. Does not update continuously.

### Syntax
```bash
ps [options]
```
Without options: shows processes for the current terminal only.

### Most Useful `ps` Options

#### Unix (POSIX) Style (with dash)

| Option | Meaning | Example |
|--------|---------|---------|
| `-e` | All processes | `ps -e` |
| `-f` | Full format (UID, PID, PPID, C, STIME, TTY, TIME, CMD) | `ps -ef` (most common) |
| `-u user` | Processes of a specific user | `ps -u root` |
| `-p PID` | Process by PID (comma‑separated) | `ps -p 1,2,3` |
| `-C command` | Processes by command name | `ps -C systemd` |
| `-G group` | Processes by group name | `ps -G root` |
| `-g GID` | Processes by group ID | `ps -g 1000` |
| `-a` | All with terminal, except session leaders | `ps -a` |
| `-x` | Processes without a controlling terminal (daemons) | `ps -x` |
| `-A` | All processes (same as `-e`) | `ps -A` |
| `-d` | All except session leaders | `ps -d` |
| `-N` or `--deselect` | Negate selection | `ps -a -N` |
| `-T` | Processes associated with current terminal | `ps -T` |

#### BSD Style (no dash)

| Option | Meaning | Example |
|--------|---------|---------|
| `aux` | All processes, detailed (user, CPU, memory, etc.) | `ps aux` (very common) |

#### GNU / Long Options

| Option | Meaning | Example |
|--------|---------|---------|
| `--forest` | Display process tree (parent‑child hierarchy) | `ps -ef --forest` |

### Understanding `ps -ef` Columns

| Column | Meaning |
|--------|---------|
| `UID` | User ID of process owner |
| `PID` | Process ID |
| `PPID` | Parent Process ID |
| `C` | CPU utilization (integer) |
| `STIME` | Start time |
| `TTY` | Terminal (`?` = daemon) |
| `TIME` | Cumulative CPU time |
| `CMD` | Command (full path if available) |

### Understanding `ps aux` Columns

| Column | Meaning |
|--------|---------|
| `USER` | Owner |
| `PID` | Process ID |
| `%CPU` | CPU usage percentage |
| `%MEM` | Memory usage percentage |
| `VSZ` | Virtual memory size (KiB) |
| `RSS` | Resident set size (physical memory, KiB) |
| `TTY` | Terminal |
| `STAT` | Process state (R,S,D,Z,T) plus modifiers |
| `START` | Start time |
| `TIME` | Cumulative CPU time |
| `COMMAND` | Command name |

### Examples
```bash
# All processes, full format (most common)
ps -ef

# All processes, BSD detailed view
ps aux

# Show only processes of user 'alice'
ps -u alice

# Find PID of a specific command
ps -C sshd

# Show process tree
ps -ef --forest

# Show specific PIDs
ps -p 1,2,3

# Show daemons (no terminal)
ps -x
```

---

## 7. `top` – Real‑Time Process Viewer

**Abbreviation:** table of processes (historical)  
**Explanation:** Displays a continuously updating list of running processes with system resource usage (CPU, memory, load average). Allows interactive management (kill, renice, sort).

### Syntax
```bash
top [options]
```

### Understanding `top` Output

#### Summary Area (first 5 lines)

| Line | Content |
|------|---------|
| 1 | System time, uptime, number of users, load average (1,5,15 min) |
| 2 | Tasks: total, running, sleeping, stopped, zombie |
| 3 | CPU(s): `us` (user), `sy` (system), `ni` (nice), `id` (idle), `wa` (I/O wait), `hi` (hardware interrupts), `si` (software interrupts), `st` (steal time – virtualized) |
| 4 | Memory (MiB Mem): total, used, free, buffers/cache |
| 5 | Swap (MiB Swap): total, used, free, available |

#### Process List Columns

| Column | Meaning |
|--------|---------|
| `PID` | Process ID |
| `USER` | Owner of the process |
| `PR` | Priority (lower number = higher priority) |
| `NI` | Nice value (-20 to +19) |
| `VIRT` | Virtual memory used (KiB) |
| `RES` | Physical RAM used (KiB) |
| `SHR` | Shared memory (KiB) |
| `S` | Process state (R,S,D,Z,T) |
| `%CPU` | CPU usage percentage |
| `%MEM` | Memory usage percentage |
| `TIME+` | Total CPU time (hundredths of a second) |
| `COMMAND` | Command name or path |

### Common `top` Options

| Option | Description | Example |
|--------|-------------|---------|
| `-v` or `--version` | Show version and exit | `top -v` |
| `-p PID` | Monitor only specific PID(s) | `top -p 1234` |
| `-M k/m/g` | Set memory display unit – *some versions* | `top -M m` |
| `-b` | Batch mode (output to file or script) | `top -b -n 1 > snapshot.txt` |
| `-n N` | Number of iterations before exiting (use with `-b`) | `top -b -n 5` |
| `-1` (digit one) | Show per‑core CPU usage instead of average | `top -1` |
| `-h` | Show help | `top -h` |

### Interactive Keys (while `top` is running)

| Key | Action |
|-----|--------|
| `q` | Quit `top` |
| `k` | Kill a process – prompts for PID and signal (default 15 = SIGTERM) |
| `r` | Renice a process – change priority (nice value) |
| `z` | Toggle color / highlighting |
| `c` | Show absolute command path instead of just name |
| `P` | Sort by CPU usage (Shift+P) |
| `M` | Sort by memory usage (Shift+M) |
| `T` | Sort by cumulative CPU time (Shift+T) |
| `1` | Toggle per‑core CPU display |
| `u` | Show only processes of a specific user (prompts for username) |
| `A` | Toggle alternative display mode (multiple windows) |
| `s` | Change refresh delay (seconds, decimals allowed) |
| `H` | Show threads instead of processes |
| `W` | Write current configuration to `~/.toprc` |

### Examples
```bash
# Basic real‑time monitoring
top

# Monitor only processes 1234 and 5678
top -p 1234,5678

# Take a single snapshot in batch mode (useful for scripts)
top -b -n 1 > /tmp/top_snapshot.txt

# Show per‑core CPU usage from start
top -1

# Inside top: kill process with PID 9999
# Press k, enter 9999, press Enter (sends SIGTERM)
```

---

## 8. Killing Processes – `kill`, `pkill`, `killall`

### Signals

A **signal** is a software interrupt sent to a process. Common signals:

| Signal Number | Name | Effect |
|---------------|------|--------|
| `1` | `SIGHUP` | Hang up – often used to reload configuration |
| `2` | `SIGINT` | Interrupt (same as `Ctrl+C`) |
| `9` | `SIGKILL` | Force kill – cannot be ignored or caught |
| `15` | `SIGTERM` | Terminate – graceful shutdown (default) |
| `18` | `SIGCONT` | Continue a stopped process |
| `19` | `SIGSTOP` | Stop (pause) a process |

### `kill` command
```bash
kill PID                # sends SIGTERM (15)
kill -15 PID            # same as above
kill -9 PID             # force kill (use only if graceful fails)
kill -1 PID             # reload configuration (e.g., nginx -s reload)
kill -STOP PID          # pause process
kill -CONT PID          # resume paused process
```

### `pkill` – kill by name
```bash
pkill sleep             # sends SIGTERM to all "sleep" processes
pkill -9 sleep          # force kill all sleep processes
```

### `killall` – kill by exact name
```bash
killall sleep           # kills all processes named exactly "sleep"
```

### `pidof` – Find PID by process name
```bash
pidof sshd
# Output: 987 654 321
```

---

## 9. Process Priority – `nice` and `renice`

Linux processes run with a **nice value** ranging from `-20` (highest priority) to `+19` (lowest priority).  
Default nice value for new processes is `0` (or inherited from parent).

| Nice Value | Priority |
|------------|----------|
| `-20` | Highest (least nice – uses more CPU) |
| `0` | Default |
| `+19` | Lowest (most nice – yields CPU to others) |

### `nice` – Start a process with a given priority
```bash
nice -n 10 long_running_script.sh   # low priority
nice -n -5 urgent_task              # higher priority (requires root)
```

### `renice` – Change priority of an already running process
```bash
renice -n 5 -p 2456      # set PID 2456 to nice 5
renice -n -10 -u alice   # change all processes of user alice
```

**Check a process's nice value:** `ps -l` shows `NI` column, or `top` (NI column).

---

## 10. System Resource Commands (Disk & Memory)

### `df` – Disk space usage (file systems)
```bash
df -h          # human‑readable sizes
df -i          # show inode usage
```

### `free` – Memory usage
```bash
free -h        # human‑readable
free -m        # in MB
free -s 2      # refresh every 2 seconds
```

**Example output:**
```
              total        used        free      shared  buff/cache   available
Mem:           7.7G        2.1G        4.2G        123M        1.4G        5.1G
Swap:          2.0G        0.0B        2.0G
```

### `lscpu` – CPU architecture info
```bash
lscpu
```
Shows cores, threads, model, virtualization support, etc.

---

## 11. Additional Process Tools (Brief)

| Tool | Description | Install / Run |
|------|-------------|---------------|
| `htop` | Interactive, color‑coded, scrollable process viewer | `sudo apt install htop` (Debian) / `sudo yum install htop` (RHEL); then `htop` |
| `atop` | Advanced performance monitor (CPU, memory, disk, network per process) | `sudo apt install atop` / `sudo dnf install atop`; then `atop` |
| `pgrep` | Find PIDs by name/pattern | `pgrep systemd`, `pgrep -u root bash` |
| `watch` | Run a command repeatedly | `watch -n 1 ps -ef` |

---

## 12. Putting It All Together – Practical Examples

### Example 1: Find a misbehaving process using too much CPU
```bash
top
# Press 'P' to sort by CPU, note the PID
# Then press 'k', enter PID, send signal 15 (SIGTERM)
```

### Example 2: Run a long backup script in the background with low priority
```bash
nice -n 19 ./backup.sh &
```

### Example 3: Gracefully reload nginx configuration without downtime
```bash
kill -1 $(pidof nginx)   # SIGHUP causes reload
```

### Example 4: Find and kill all leftover `sleep` processes
```bash
pkill sleep
```

### Example 5: Suspend a large file copy to free terminal, then resume later
```bash
cp hugefile.iso /backup/ &
^Z
jobs
bg %1
disown %1   # detach from terminal so it continues after logout
```

### Example 6: Monitor memory usage every 2 seconds
```bash
watch -n 2 free -h
```

### Example 7: Take a batch snapshot of `top` for logging
```bash
top -b -n 1 > /var/log/top_snapshot_$(date +%Y%m%d).txt
```

---

## 13. Quick Reference Table

| Task | Command |
|------|---------|
| List processes (snapshot) | `ps -ef` |
| List all processes (BSD style) | `ps aux` |
| Real‑time monitoring | `top` or `htop` |
| Find PID of a process | `pidof processname` or `pgrep name` |
| Gracefully kill process | `kill PID` |
| Force kill process | `kill -9 PID` |
| Kill all processes by name | `pkill name` |
| Suspend foreground process | `Ctrl+Z` |
| Resume in background | `bg %1` |
| Bring to foreground | `fg %1` |
| Start low priority process | `nice -n 19 command` |
| Change priority of running process | `renice -n 10 -p PID` |
| View disk usage | `df -h` |
| View memory usage | `free -h` |
| View CPU info | `lscpu` |

---

## 14. Common Mistakes & Pitfalls

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `kill -9` as default | Process can't clean up (temp files, sockets left behind) | Try `kill` (SIGTERM) first, only use `-9` if unresponsive |
| Killing a parent process without reaping children | Creates orphans (harmless but messy) | Let init adopt them; avoid killing init/systemd |
| Starting long process in foreground and closing terminal | Process gets SIGHUP and terminates | Use `&` and `disown` or `nohup` |
| Setting nice value too low (`-20`) on user process | Can starve system processes (requires root) | Only root can set negative nice values |
| Not checking memory before running heavy job | OOM killer may kill critical processes | Use `free -h` and `vmstat` first |

---

## 15. Practice Lab – Verify Your Understanding

1. Run `sleep 300` in the background. Find its PID with `pidof`. Verify with `ps -ef | grep sleep`.
2. Suspend a foreground `ping` process with `Ctrl+Z`, then resume it in the background.
3. Use `top` to find a process using the most CPU. Quit `top`.
4. Start a process with low priority (`nice -n 15`) and verify its nice value using `ps -l`.
5. Take a batch snapshot of `top` with 2 iterations and save to a file: `top -b -n 2 > top_snapshot.txt`.
6. Use `ps -ef --forest` to see the process tree. Find the parent of your shell.
7. Run `ps aux` and explain the meaning of `STAT` column for three different processes.

---

This is an excellent, well‑structured chapter. It covers the essentials of process management thoroughly. Below is a detailed review followed by additional professional‑level topics you should add to make it truly comprehensive, plus a complete practical mastery test that covers everything—including the added material.

---

## Deep Review of Chapter 9 – Monitoring and Managing Linux Processes

### Strengths
- **Clear definitions:** Process, PID/PPID, states, foreground/background, signals, nice values.
- **Practical command coverage:** `ps`, `top`, `kill` family, job control.
- **Well‑organized tables:** Makes quick reference easy.
- **Real‑world examples:** Section 12 ties commands to actual tasks.
- **Common pitfalls:** Helps avoid typical mistakes.

### What's Missing (Important for Pro‑Level Mastery)

| Missing Topic | Why It Matters |
|---------------|----------------|
| **`/proc` filesystem** | Deep inspection of process details (e.g., `/proc/[PID]/`). Essential for debugging. |
| **`pstree`** | Visualize parent‑child relationships better than `ps --forest`. |
| **`pgrep` and `pkill` with advanced matching** | Covered briefly but missing options like `-f` (full command), `-u` (user), `-P` (parent). |
| **`nohup` and `disown` explained fully** | Ensures processes survive terminal logout. Critical for long‑running jobs. |
| **`screen` / `tmux`** | Terminal multiplexers. Industry standard for keeping sessions alive on remote servers. |
| **`lsof`** | List open files per process – crucial for finding which process uses a port or file. |
| **`strace`** | Trace system calls of a process. Indispensable for debugging stuck or misbehaving programs. |
| **`vmstat`, `iostat`, `sar`** | System‑wide performance metrics beyond `top` (especially `wa` – I/O wait). |
| **`cgroups` and `systemd-cgls` / `systemd-cgtop`** | Modern resource control. Cloud engineers must understand container‑like isolation. |
| **`oom_score` and `oom_adj`** | How the Out‑Of‑Memory killer chooses victims. Vital for tuning critical services. |
| **`kill -l`** | List all available signals. |
| **`time` command** | Measure how long a process takes. |
| **`uptime`** | Quick system load average. |

I will provide these additions as plain text you can insert into your notes.

---

## Additions to Chapter 9 (Insert at Appropriate Places)

### Addition 1: The /proc Filesystem – Process Information Goldmine

The `/proc` directory is a virtual filesystem containing runtime system information. Each process has a subdirectory named by its PID (`/proc/[PID]/`).

| File / Directory | Purpose |
|------------------|---------|
| `/proc/[PID]/cmdline` | Command line used to start the process (null‑separated). |
| `/proc/[PID]/environ` | Environment variables of the process. |
| `/proc/[PID]/fd/` | Directory of open file descriptors (links to actual files/sockets). |
| `/proc/[PID]/exe` | Symlink to the executable binary. |
| `/proc/[PID]/cwd` | Symlink to current working directory. |
| `/proc/[PID]/status` | Human‑readable status (Name, State, Uid, VmRSS, Threads). |
| `/proc/[PID]/stat` | Machine‑readable status (used by `ps`). |
| `/proc/[PID]/limits` | Resource limits (ulimit). |
| `/proc/[PID]/oom_score` | Current OOM score (higher = more likely to be killed). |
| `/proc/[PID]/oom_adj` | OOM adjustment value (-1000 to 1000) to influence killer. |

Example: Find what files a process has open:
```bash
ls -l /proc/1234/fd/
```

Example: See full command line of a process (useful when `ps` truncates):
```bash
cat /proc/1234/cmdline | tr '\0' ' '
```

---

### Addition 2: Advanced Process Listing Tools

**pstree** – Display process tree visually.
```bash
pstree -p          # show PIDs
pstree -u          # show user ownership
pstree -a          # show command line arguments
pstree -s PID      # show only ancestors of PID
```

**pgrep with advanced filters** (more than just name):
```bash
pgrep -u alice                     # processes owned by alice
pgrep -P 1234                      # child processes of PID 1234
pgrep -f "nginx: worker"           # match full command line
pgrep -l ssh                       # show process name and PID
pgrep -c bash                      # count of processes matching
```

**pidof** is simple; `pgrep` is more powerful.

---

### Addition 3: Keeping Processes Alive After Logout – nohup, disown, screen, tmux

| Method | Command | When to Use |
|--------|---------|-------------|
| `nohup` | `nohup long_script.sh &` | Start a process that ignores SIGHUP. Output goes to `nohup.out`. |
| `disown` | `long_script &` then `disown %1` | Already started a job; detach it from shell. |
| `screen` | `screen` then `Ctrl+A D` to detach | Full terminal multiplexer with reattach capability. |
| `tmux` | `tmux new -s mysession` then `Ctrl+B D` | Modern alternative to screen with more features. |

**screen basic commands:**
```bash
screen -S session_name     # create named session
screen -ls                 # list sessions
screen -r session_name     # reattach
```

**tmux basic commands:**
```bash
tmux new -s dev            # new session
tmux ls                    # list sessions
tmux attach -t dev         # reattach
```

---

### Addition 4: Process Troubleshooting Power Tools

**lsof** – List open files (everything is a file).
```bash
lsof -i :80                # which process is listening on port 80?
lsof -p 1234               # all files opened by PID 1234
lsof -u alice              # files opened by user alice
lsof /var/log/syslog       # processes using this file
lsof +D /home              # all open files under /home
```

**strace** – Trace system calls and signals.
```bash
strace -p 1234             # attach to running process
strace -c -p 1234          # summary of syscalls when detached (Ctrl+C)
strace -e open ls          # trace only open() calls of 'ls'
strace -o output.txt command  # save trace to file
```
Use `strace` when a process hangs or behaves unexpectedly.

**time** – Measure execution duration.
```bash
time cp largefile.iso /backup/
# real: wall clock time
# user: CPU time in user mode
# sys:  CPU time in kernel mode
```

---

### Addition 5: System Performance Commands

**uptime** – Quick load average.
```bash
uptime
# 14:23:45 up 10 days,  3:15,  2 users,  load average: 0.05, 0.10, 0.15
```
Load average shows 1, 5, and 15 minute averages of runnable + uninterruptible tasks.

**vmstat** – Virtual memory statistics.
```bash
vmstat 2 5                # every 2 seconds, 5 times
```
Columns: r (runnable), b (blocked on I/O), swpd, free, buff, cache, si (swap in), so (swap out), bi (block in), bo (block out), in (interrupts), cs (context switches), us, sy, id, wa (I/O wait), st (steal).

**iostat** – CPU and I/O statistics for devices/partitions.
```bash
iostat -x 2               # extended stats every 2 sec
```
Look for `%util` (device saturation) and `await` (I/O wait time).

**sar** – System Activity Reporter (part of sysstat package).
```bash
sar -u 2 5                # CPU usage every 2 sec, 5 times
sar -r                    # memory usage history
sar -n DEV                # network device statistics
```

---

### Addition 6: Modern Resource Control – cgroups and systemd

**systemd-cgtop** – Show control group resource usage (like `top` for cgroups).
```bash
systemd-cgtop
```

**systemd-cgls** – List cgroup hierarchy.
```bash
systemd-cgls
```

**Checking a process's cgroup:**
```bash
cat /proc/[PID]/cgroup
```

**Adjust OOM killer preference:**
```bash
echo -1000 > /proc/[PID]/oom_adj    # protect from OOM (requires root)
echo 1000 > /proc/[PID]/oom_adj     # make it a prime candidate
```
Alternatively, use `systemd` service `OOMScoreAdjust=` directive.

---

### Addition 7: List All Signals
```bash
kill -l
```
Shows all 64 signals (1-64). Common ones: 1 SIGHUP, 2 SIGINT, 9 SIGKILL, 15 SIGTERM, 17 SIGCHLD, 18 SIGCONT, 19 SIGSTOP, 20 SIGTSTP.

---

Now, here is a complete, professional‑level practical test that covers **everything** in the chapter plus the additions above.

---

## 16. Complete Professional Mastery Test – Linux Process Management

This test simulates real‑world system administration and cloud engineering tasks. Perform it on a Linux VM or container with `sudo` access. **Attempt all tasks before looking at the answer key.**

---

### Part 1: Process Fundamentals – Identification and States

**Task 1.1** – Start a `sleep 600` process in the background. Note its PID. Use three different methods to find that PID again.

**Task 1.2** – Suspend the `sleep` process (if foreground) or find a way to put a running process into Stopped (`T`) state. Verify its state with `ps`.

**Task 1.3** – Create a zombie process. (Hint: Write a short C program or use a shell trick: `(sleep 1 & exec sleep 1)` then immediately check with `ps aux | grep Z`). Identify the zombie and its parent.

**Task 1.4** – Explain the difference between `S` and `D` states. Give a real‑world scenario where you would see a process in `D` state.

---

### Part 2: Job Control and Background/Foreground

**Task 2.1** – Start a `ping localhost` command in the foreground. Suspend it with `Ctrl+Z`. List jobs. Resume it in the background. Then bring it back to the foreground and terminate with `Ctrl+C`.

**Task 2.2** – Start a long‑running command (e.g., `find / -name "*.conf" 2>/dev/null`) in the background. Disown it so it survives terminal closure. Verify it continues after logging out and back in.

**Task 2.3** – Use `screen` or `tmux` to create a new session named "testlab". Inside, run `top`. Detach and reattach to confirm the session persists.

---

### Part 3: Process Inspection with `ps`, `pstree`, and `/proc`

**Task 3.1** – Use `ps -ef --forest` to view the process tree. Identify the parent of your current shell.

**Task 3.2** – Use `ps aux` to find the process with the highest memory usage. Write the command to show only that process.

**Task 3.3** – Use `pstree -p` to visualize the hierarchy of the `sshd` service processes. Note the PIDs.

**Task 3.4** – Navigate to `/proc/PID/` for the `sshd` parent process. Examine `status`, `cmdline`, and `fd/`. Report:
- The process name from `status`.
- The full command line from `cmdline`.
- How many open file descriptors.

---

### Part 4: Process Signals and Termination

**Task 4.1** – Start a `sleep 500` process. Terminate it gracefully using the correct signal number and name. Verify it is gone.

**Task 4.2** – Start a process that ignores `SIGTERM` but can be killed with `SIGKILL`. (Hint: `trap '' TERM; sleep 1000` in a script). Send `SIGTERM` and observe it stays. Then send `SIGKILL`.

**Task 4.3** – Use `pkill` to kill all processes whose command line contains "sleep". Then use `pgrep` to confirm none remain.

**Task 4.4** – Reload the `cron` service configuration without restarting the daemon. (Hint: send SIGHUP to `cron` PID).

---

### Part 5: Process Priority – nice and renice

**Task 5.1** – Start a CPU‑intensive task (e.g., `dd if=/dev/zero of=/dev/null`) with a low priority (nice value 15). Verify its nice value using `ps -l`.

**Task 5.2** – While the task runs, change its priority to the highest possible value (nice -20). Note: requires root.

**Task 5.3** – Explain why a normal user cannot set a negative nice value. What security implication does this have?

---

### Part 6: Resource Monitoring and Performance Analysis

**Task 6.1** – Run `top` in batch mode for 3 iterations with a 2‑second delay, saving output to a file. Then extract the line containing the process with the highest CPU usage from that file.

**Task 6.2** – Use `free -h -s 2` to watch memory usage for 10 seconds. Note the available memory trend.

**Task 6.3** – Use `vmstat 2 5` and identify if the system is experiencing I/O wait (`wa` column). Then use `iostat -x 2` to find which disk is most utilized.

**Task 6.4** – Check the system load average using `uptime`. Explain what each of the three numbers means in relation to CPU cores.

---

### Part 7: Advanced Tools – `lsof`, `strace`, `time`

**Task 7.1** – Use `lsof` to find which process is listening on port 22 (SSH). Also find which process has opened `/var/log/syslog` (or `/var/log/messages`).

**Task 7.2** – Attach `strace` to a running `sleep` process for a few seconds. Observe the system calls. Then run `strace ls` and save the output to a file.

**Task 7.3** – Use the `time` command to measure how long it takes to recursively list all files in `/etc`.

---

### Part 8: Real‑World Scenarios

**Scenario 1: Misbehaving Web Server**

You notice a web server (nginx) process consuming 100% CPU. You need to identify the exact PID, understand if it's stuck in a loop, and restart only that worker without dropping connections.

**Task 8.1** – Use `top` to find the high‑CPU nginx worker PID.
**Task 8.2** – Use `strace -p PID` to see what system calls it's making (e.g., infinite loop of `epoll_wait` or `read`). Stop after a few seconds.
**Task 8.3** – Send the appropriate signal to nginx master process to gracefully reload configuration and restart workers. (Hint: SIGHUP).

**Scenario 2: OOM Killer Tuning**

A critical database process keeps getting killed by the OOM killer under memory pressure.

**Task 8.4** – Find the current `oom_score` of the database process.
**Task 8.5** – Adjust its `oom_adj` to -500 to make it less likely to be killed.
**Task 8.6** – Explain why this is a temporary fix and what long‑term solutions exist.

**Scenario 3: Background Job Management for a Cloud Engineer**

You need to run a database backup script that takes 2 hours. You are connected via SSH and your connection might drop.

**Task 8.7** – Demonstrate three different ways to ensure the backup continues even if you disconnect. Write the exact commands for each method.

**Scenario 4: Identifying a File Lock**

An application reports "cannot write to config file, permission denied" but permissions look correct (`rw-r--r--`). You suspect another process has the file open with a write lock.

**Task 8.8** – Use `lsof` to see which process has the file open.

---

### Part 9: Cleanup

Kill any remaining test processes (`sleep`, `dd`, `find`), remove test files, and exit any screen/tmux sessions.

---

## 17. Self‑Evaluation Checklist

| I can... | Done |
|----------|------|
| Find a process PID using `pidof`, `pgrep`, and `ps` | ☐ |
| Interpret process states (R, S, D, T, Z) and identify zombies | ☐ |
| Manage foreground/background jobs with `&`, `Ctrl+Z`, `bg`, `fg`, `jobs` | ☐ |
| Use `disown`, `nohup`, `screen`, or `tmux` to keep processes alive | ☐ |
| Read detailed process info from `/proc/[PID]/` | ☐ |
| View process trees with `ps --forest` and `pstree` | ☐ |
| Send signals with `kill`, `pkill`, `killall` and know when to use `-9` | ☐ |
| Adjust process priority with `nice` and `renice` | ☐ |
| Monitor real‑time system resources with `top`, `htop`, `vmstat`, `iostat` | ☐ |
| Use `lsof` to find open files and listening ports | ☐ |
| Trace process system calls with `strace` | ☐ |
| Measure execution time with `time` | ☐ |
| Understand load average and CPU core correlation | ☐ |
| Adjust OOM killer behavior via `oom_adj` | ☐ |
| Troubleshoot hung processes using signals and tracing | ☐ |

---

## 18. Answer Key

### Part 1

**1.1** Methods: `pidof sleep`, `pgrep sleep`, `ps -ef | grep sleep | grep -v grep`.

**1.2** Suspend: `kill -STOP PID` or `Ctrl+Z`. State becomes `T`.

**1.3** Zombie creation:
```bash
( sleep 1 & exec sleep 1 ) &
ps aux | grep Z
```
Parent is the shell that didn't reap.

**1.4** `S` = interruptible sleep (can be killed); `D` = uninterruptible sleep (waiting for I/O, cannot be killed). `D` occurs with failing NFS mount or bad disk.

### Part 2

**2.1** `ping localhost` → `Ctrl+Z` → `jobs` → `bg %1` → `fg %1` → `Ctrl+C`.

**2.2** `find / -name "*.conf" 2>/dev/null &` then `disown %1`. Logout and back in, process still running (check with `ps`).

**2.3** `screen -S testlab`, then `top`, detach `Ctrl+A D`. Reattach `screen -r testlab`.

### Part 3

**3.1** Parent of shell: `ps -ef --forest | grep -B1 $$`.

**3.2** `ps aux --sort=-%mem | head -2`.

**3.3** `pstree -p | grep sshd`.

**3.4** `cat /proc/[PID]/status`, `cat /proc/[PID]/cmdline | tr '\0' ' '`, `ls -l /proc/[PID]/fd | wc -l`.

### Part 4

**4.1** `kill -15 PID` or `kill -TERM PID`.

**4.2** Script `trap '' TERM; sleep 1000`. `kill -15 PID` does nothing; `kill -9 PID` works.

**4.3** `pkill sleep` then `pgrep sleep` returns empty.

**4.4** `sudo kill -HUP $(pidof cron)` or `sudo pkill -HUP cron`.

### Part 5

**5.1** `nice -n 15 dd if=/dev/zero of=/dev/null bs=1M &` then `ps -l`.

**5.2** `sudo renice -n -20 -p PID`.

**5.3** Negative nice values increase priority; normal users could starve system processes. Only root can set negative nice.

### Part 6

**6.1** `top -b -n 3 -d 2 > top.out`. Then `grep -A1 "PID USER" top.out | tail -1` or similar.

**6.2** `free -h -s 2` then `Ctrl+C` after a few iterations.

**6.3** `vmstat 2 5`; `iostat -x 2 5`.

**6.4** Load average of 1.00 on a single‑core system means CPU is fully utilized. On a 4‑core system, 1.00 means 25% utilization. Numbers > cores indicate overload.

### Part 7

**7.1** `sudo lsof -i :22`; `sudo lsof /var/log/syslog`.

**7.2** `sudo strace -p PID`; `strace -o ls.trace ls`.

**7.3** `time ls -lR /etc > /dev/null`.

### Part 8

**8.1** `top` then press `P` to sort by CPU.

**8.2** `sudo strace -p PID` (observe). `Ctrl+C`.

**8.3** `sudo kill -HUP $(cat /var/run/nginx.pid)`.

**8.4** `cat /proc/[PID]/oom_score`.

**8.5** `echo -500 | sudo tee /proc/[PID]/oom_adj`.

**8.6** Increase system memory, set memory limits in service unit, adjust `OOMScoreAdjust` in systemd service file.

**8.7** Methods: `nohup ./backup.sh &`, `./backup.sh & disown`, or `screen -dmS backup ./backup.sh`.

**8.8** `sudo lsof /path/to/config/file`.

### Part 9

`pkill -u $USER sleep dd find`; `screen -X quit` or `tmux kill-server`.



---