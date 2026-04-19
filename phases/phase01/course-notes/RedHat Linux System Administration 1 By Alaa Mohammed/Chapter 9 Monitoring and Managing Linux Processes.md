
# Chapter 9: Monitoring and Managing Linux Processes – Complete Professional Reference

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

## 8. Additional Process Listing and Tree Tools

### 8.1 `pstree` – Display Process Tree Visually

```bash
pstree -p          # show PIDs
pstree -u          # show user ownership
pstree -a          # show command line arguments
pstree -s PID      # show only ancestors of PID
```

### 8.2 `pgrep` – Advanced Process Finding

More powerful than `pidof`. Options:

| Option | Meaning | Example |
|--------|---------|---------|
| `-u user` | Processes owned by user | `pgrep -u alice` |
| `-P PID` | Child processes of PID | `pgrep -P 1234` |
| `-f` | Match full command line | `pgrep -f "nginx: worker"` |
| `-l` | Show process name + PID | `pgrep -l ssh` |
| `-c` | Count matches | `pgrep -c bash` |

### 8.3 `pkill` – Kill by Name with Filters

Same options as `pgrep`. Example:
```bash
pkill -f "long_running_script"   # kill by full command line
pkill -u alice                   # kill all processes of user alice
```

### 8.4 `pidof` – Simple PID by Exact Name

```bash
pidof sshd
# Output: 987 654 321
```

---

## 9. The `/proc` Filesystem – Deep Process Inspection

`/proc` is a virtual filesystem containing runtime system information. Each process has a subdirectory `/proc/[PID]/`.

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

**Example: Find what files a process has open:**
```bash
ls -l /proc/1234/fd/
```

**Example: See full command line of a process (when `ps` truncates):**
```bash
cat /proc/1234/cmdline | tr '\0' ' '
```

---

## 10. Killing Processes – Signals and Commands

### Signals List

All signals can be listed with:
```bash
kill -l
```

Common signals:

| Signal Number | Name | Effect |
|---------------|------|--------|
| `1` | `SIGHUP` | Hang up – often used to reload configuration |
| `2` | `SIGINT` | Interrupt (same as `Ctrl+C`) |
| `9` | `SIGKILL` | Force kill – cannot be ignored or caught |
| `15` | `SIGTERM` | Terminate – graceful shutdown (default) |
| `18` | `SIGCONT` | Continue a stopped process |
| `19` | `SIGSTOP` | Stop (pause) a process |

### `kill` Command
```bash
kill PID                # sends SIGTERM (15)
kill -15 PID            # same as above
kill -9 PID             # force kill (use only if graceful fails)
kill -1 PID             # reload configuration (e.g., nginx -s reload)
kill -STOP PID          # pause process
kill -CONT PID          # resume paused process
```

### `pkill` – kill by name (supports `-f`, `-u`, etc.)
```bash
pkill sleep             # sends SIGTERM to all "sleep" processes
pkill -9 sleep          # force kill all sleep processes
```

### `killall` – kill by exact name
```bash
killall sleep           # kills all processes named exactly "sleep"
```

---

## 11. Keeping Processes Alive After Logout

| Method | Command | When to Use |
|--------|---------|-------------|
| `nohup` | `nohup long_script.sh &` | Start a process that ignores SIGHUP. Output goes to `nohup.out`. |
| `disown` | `long_script &` then `disown %1` | Already started a job; detach it from shell. |
| `screen` | `screen` then `Ctrl+A D` to detach | Full terminal multiplexer with reattach capability. |
| `tmux` | `tmux new -s mysession` then `Ctrl+B D` | Modern alternative to screen with more features. |

### `screen` Basics
```bash
screen -S session_name     # create named session
screen -ls                 # list sessions
screen -r session_name     # reattach
```

### `tmux` Basics
```bash
tmux new -s dev            # new session
tmux ls                    # list sessions
tmux attach -t dev         # reattach
```

---

## 12. Process Priority – `nice` and `renice`

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

## 13. System Resource Commands

### 13.1 `df` – Disk space usage (file systems)
```bash
df -h          # human‑readable sizes
df -i          # show inode usage
```

### 13.2 `free` – Memory usage
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

### 13.3 `uptime` – Quick load average
```bash
uptime
# 14:23:45 up 10 days,  3:15,  2 users,  load average: 0.05, 0.10, 0.15
```
Load average shows 1, 5, and 15 minute averages of runnable + uninterruptible tasks.

### 13.4 `lscpu` – CPU architecture info
```bash
lscpu
```
Shows cores, threads, model, virtualization support, etc.

### 13.5 `vmstat` – Virtual memory statistics
```bash
vmstat 2 5                # every 2 seconds, 5 times
```
Columns: `r` (runnable), `b` (blocked on I/O), `swpd`, `free`, `buff`, `cache`, `si` (swap in), `so` (swap out), `bi` (block in), `bo` (block out), `in` (interrupts), `cs` (context switches), `us`, `sy`, `id`, `wa` (I/O wait), `st` (steal).

### 13.6 `iostat` – CPU and I/O statistics
```bash
iostat -x 2               # extended stats every 2 sec
```
Look for `%util` (device saturation) and `await` (I/O wait time).

### 13.7 `sar` – System Activity Reporter (requires `sysstat` package)
```bash
sar -u 2 5                # CPU usage every 2 sec, 5 times
sar -r                    # memory usage history
sar -n DEV                # network device statistics
```

---

## 14. Advanced Troubleshooting Tools

### 14.1 `lsof` – List Open Files (everything is a file)
```bash
lsof -i :80                # which process is listening on port 80?
lsof -p 1234               # all files opened by PID 1234
lsof -u alice              # files opened by user alice
lsof /var/log/syslog       # processes using this file
lsof +D /home              # all open files under /home
```

### 14.2 `strace` – Trace System Calls and Signals
```bash
strace -p 1234             # attach to running process
strace -c -p 1234          # summary of syscalls when detached (Ctrl+C)
strace -e open ls          # trace only open() calls of 'ls'
strace -o output.txt command  # save trace to file
```
Use `strace` when a process hangs or behaves unexpectedly.

### 14.3 `time` – Measure Execution Duration
```bash
time cp largefile.iso /backup/
# real: wall clock time
# user: CPU time in user mode
# sys:  CPU time in kernel mode
```

---

## 15. Modern Resource Control – cgroups and systemd

### 15.1 `systemd-cgtop` – Show control group resource usage (like `top` for cgroups)
```bash
systemd-cgtop
```

### 15.2 `systemd-cgls` – List cgroup hierarchy
```bash
systemd-cgls
```

### 15.3 Checking a process's cgroup
```bash
cat /proc/[PID]/cgroup
```

### 15.4 Adjusting OOM Killer Preference
```bash
echo -1000 > /proc/[PID]/oom_adj    # protect from OOM (requires root)
echo 1000 > /proc/[PID]/oom_adj     # make it a prime candidate
```
Alternatively, use `systemd` service `OOMScoreAdjust=` directive.

---

## 16. Putting It All Together – Practical Examples

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

### Example 8: Identify which process has a file open (debugging "file busy")
```bash
lsof /path/to/config/file
```

### Example 9: Trace a hanging process
```bash
sudo strace -p 1234
```

---

## 17. Quick Reference Table

| Task | Command |
|------|---------|
| List processes (snapshot) | `ps -ef` |
| List all processes (BSD style) | `ps aux` |
| Real‑time monitoring | `top` or `htop` |
| Find PID of a process | `pidof name` or `pgrep name` |
| Find processes by full command line | `pgrep -f "pattern"` |
| Process tree | `ps -ef --forest` or `pstree -p` |
| Gracefully kill process | `kill PID` |
| Force kill process | `kill -9 PID` |
| Kill all processes by name | `pkill name` |
| Suspend foreground process | `Ctrl+Z` |
| Resume in background | `bg %1` |
| Bring to foreground | `fg %1` |
| Keep process after logout | `nohup`, `disown`, `screen`, `tmux` |
| Start low priority process | `nice -n 19 command` |
| Change priority of running process | `renice -n 10 -p PID` |
| View disk usage | `df -h` |
| View memory usage | `free -h` |
| View load average | `uptime` |
| View per‑core CPU info | `lscpu` |
| System activity (CPU, memory, I/O) | `vmstat 2`, `iostat -x 2`, `sar` |
| List open files | `lsof` |
| Trace system calls | `strace -p PID` |
| Measure execution time | `time command` |
| List all signals | `kill -l` |

---

## 18. Common Mistakes & Pitfalls

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `kill -9` as default | Process can't clean up (temp files, sockets left behind) | Try `kill` (SIGTERM) first, only use `-9` if unresponsive |
| Killing a parent process without reaping children | Creates orphans (harmless but messy) | Let init adopt them; avoid killing init/systemd |
| Starting long process in foreground and closing terminal | Process gets SIGHUP and terminates | Use `&` and `disown` or `nohup` |
| Setting nice value too low (`-20`) on user process | Can starve system processes (requires root) | Only root can set negative nice values |
| Not checking memory before running heavy job | OOM killer may kill critical processes | Use `free -h` and `vmstat` first |
| Editing `/proc/[PID]/oom_adj` as non‑root | Permission denied | Use `sudo` |
| Using `ps -ef` and missing daemons | Daemons have `?` TTY but still appear | Use `ps -ef` includes them; `ps -x` shows without terminal |

---

## 19. Complete Professional Mastery Test – Linux Process Management

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

## 20. Answer Key

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

## 21. Self‑Evaluation Checklist

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

**Date documented:** 2026-04-19  
**Sources:** Linux Administration, GeeksforGeeks, man pages, Red Hat documentation

---
