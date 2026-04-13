Here is your **pro markdown version** of the notes for **Chapter 2: Accessing the Command Line**. Save it as `phases/phase01/topics-notes/accessing-command-line.md`

---

# Accessing the Command Line

## Anaconda File & Installation Choices

During Red Hat OS installation, the **Anaconda installer** monitors all your answers and saves a configuration file (`anaconda-ks.cfg`) to your home directory.  
You can reuse this file on another machine with tools like **Kickstart** to automate the same installation choices without re‑entering them.

### Installation Environment Options

| Option | Description |
|--------|-------------|
| **Server with GUI** | Full server + graphical interface |
| **Server** | Server without GUI (command line only) |
| **Minimal** | Bare minimum – only essential packages, no GUI |
| **Workstation** | Suitable for personal laptops |
| **Virtualization Host** | For running guest OSes (KVM) |

### Partitioning Options

| Type | How it works |
|------|--------------|
| **Standard** | Static size – cannot extend later when full |
| **LVM (Logical Volume Manager)** | Allocates full size upfront (e.g., 10 GB reserved whether used or not) |
| **LVM Thin** | Grows to maximum allocation only as needed – takes space when actually used |

### Managing the OS

- **GUI** – Graphical interface (if installed)
- **Shell** – Command line interface

In the shell, you have **6 TTY sessions** (virtual terminals) you can access simultaneously.

| Shortcut | Action |
|----------|--------|
| `Ctrl + Alt + F1` | Switch to GUI |
| `Ctrl + Alt + F2` | TTY 2 |
| `Ctrl + Alt + F3` | TTY 3 |
| `Ctrl + Alt + F4` | TTY 4 |
| `Ctrl + Alt + F5` | TTY 5 |
| `Ctrl + Alt + F6` | TTY 6 |

---

## Command Reference

### `w` – Who is logged in and what they are doing

| Property | Value |
|----------|-------|
| **Abbreviation** | who |
| **Explanation** | Shows who is currently using the computer, system load, and which processes are running |

**Example output:**

```
 15:30:01 up 2 days,  1:23,  2 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     tty2     -                14:20    1:09m  0.03s  0.03s -bash
alice    pts/0    192.168.1.100    15:00    0.00s  0.02s  0.00s w
```

---

### Prompt Anatomy

The shell prompt gives you important context.

```
root@server ~ #
```

| Part | Meaning |
|------|---------|
| `root` | Login name |
| `server` | Host name |
| `~` | Current working directory (home directory) |
| `#` | **Root user** (normal user would show `$`) |

---

### `pwd` – Print Working Directory

| Property | Value |
|----------|-------|
| **Abbreviation** | print working directory |
| **Explanation** | Prints the full path of the current directory |

**Example:**

```bash
$ pwd
/home/alice
```

---

### `ls` – List Directory Contents

| Property | Value |
|----------|-------|
| **Abbreviation** | list |
| **Explanation** | Lists information about files (default: current directory) |

| Option | Description |
|--------|-------------|
| `-a`, `--all` | Do not ignore entries starting with `.` |
| `-h`, `--human-readable` | With `-l`, print sizes like 1K, 234M, 2G |
| `-i`, `--inode` | Print the index number (inode) of each file |
| `-l` | Use a long listing format (permissions, size, etc.) |
| `-r`, `--reverse` | Reverse order while sorting |
| `-R`, `--recursive` | List subdirectories recursively |

**Example:**

```bash
$ ls -lah
total 12K
drwxr-x--- 2 alice alice 4.0K Apr 13 10:00 .
drwxr-xr-x 5 root  root  4.0K Apr 13 09:30 ..
-rw------- 1 alice alice  220 Apr 13 10:00 .bashrc
```

---

### `su` – Switch User

| Property | Value |
|----------|-------|
| **Abbreviation** | switch / substitute user |
| **Explanation** | Without a username, starts an interactive shell as `root`. With a username, switches to that user. |

| Option | Description |
|--------|-------------|
| `-c`, `--command` `command` | Pass a command to the shell |
| `-s`, `--shell` `shell` | Run the specified shell instead of default |

**Examples:**

```bash
$ su                     # become root (asks for root password)
$ su - alice             # switch to alice with her environment
$ su -c "ls /root"       # run command as root without full login
```

---

### `date` – Display or Set Date/Time

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Display and manipulate system date and time |

**Examples:**

```bash
$ date
Wed May 4 15:20:30 UTC 2023

$ date '+%Y-%m-%d %H:%M:%S'
2023-05-04 15:20:30

$ date -d '+7 days'
Wed May 11 15:20:30 UTC 2023

$ sudo date -s '2023-05-04 15:20:30'
Thu May 4 15:20:30 UTC 2023
```

---

### `cal` – Calendar

| Property | Value |
|----------|-------|
| **Abbreviation** | calendar |
| **Explanation** | Displays a calendar of the current month (today highlighted) |

| Option | Description |
|--------|-------------|
| `-y` | Show the entire current year |
| `cal month year` | Show specific month/year (e.g., `cal 08 2000`) |

**Example:**

```bash
$ cal
     April 2026
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30
```

---

### Tab Completion

Press **Tab** to auto‑complete commands, file names, or paths.

---

### `cat` – Concatenate and Display Files

| Property | Value |
|----------|-------|
| **Abbreviation** | concatenate |
| **Explanation** | Reads, displays, and concatenates text files |

| Option | Description |
|--------|-------------|
| `-n`, `--number` | Number all output lines |

**Example:**

```bash
$ cat -n file.txt
     1  first line
     2  second line
```

---

### `tail` – View End of File

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Outputs the last part of files (great for logs) |

| Option | Description |
|--------|-------------|
| `-n N` | Show last N lines (default 10) |
| `-f` | Follow mode – keep reading as file grows |

**Example:**

```bash
$ tail -n 20 /var/log/messages
$ tail -f /var/log/nginx/access.log   # live monitor
```

---

### `head` – View Beginning of File

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Outputs the first part of files |

| Option | Description |
|--------|-------------|
| `-n N` | Show first N lines (default 10) |

**Example:**

```bash
$ head -n 5 /etc/passwd
```

---

### `less` – Page Through Files

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | View file contents one page at a time (does not load entire file). Allows scrolling forward/backward, searching with `/pattern`. |

| Option | Description |
|--------|-------------|
| `-E` | Automatically exit at end of file |
| `-f` | Force open non‑regular files |
| `-F` | Exit immediately if file fits on one screen |
| `-g` | Highlight only the last searched string |
| `-G` | Disable all highlighting |
| `-i` | Case‑insensitive search |
| `-n` | Hide line numbers |
| `-p pattern` | Open at first occurrence of pattern |
| `-s` | Squeeze multiple blank lines |

**Navigation shortcuts inside `less`:**

| Key | Action |
|-----|--------|
| `Space` | Next page |
| `b` | Previous page |
| `/pattern` | Search forward |
| `?pattern` | Search backward |
| `n` | Next match |
| `q` | Quit |

**Example – search for "fail" in dmesg output:**

```bash
dmesg | less -p "fail"
```

---

### Grouping Commands

Use **`;`** to run multiple commands sequentially:

```bash
$ ls; date; cal
```

Use **`\`** to write a command across multiple lines:

```bash
$ cal \
; ls \
; date
```

---

### `wc` – Word Count

| Property | Value |
|----------|-------|
| **Abbreviation** | word count |
| **Explanation** | Counts lines, words, characters, and bytes in a file or input |

| Option | Output |
|--------|--------|
| `-l` | Line count |
| `-w` | Word count |
| `-c` | Byte count |
| `-m` | Character count |

**Examples:**

```bash
$ wc state.txt
 5  7 58 state.txt   # lines, words, bytes

$ wc -l state.txt
5 state.txt

$ ls gfg | wc -l    # count files in directory
7
```

**Multiple files:**

```bash
$ wc state.txt capital.txt
  5   7  58 state.txt
  5   5  39 capital.txt
 10  12  97 total
```

---

### `passwd` – Manage User Passwords

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Change your own password or manage other users' passwords (as root) |

| Command | What it does |
|---------|--------------|
| `passwd` | Change your own password |
| `sudo passwd [user]` | Change another user's password |
| `sudo passwd -l [user]` | Lock the account |
| `sudo passwd -u [user]` | Unlock the account |
| `sudo passwd -e [user]` | Expire password (force change on next login) |
| `sudo passwd -S [user]` | Show account status |
| `sudo passwd -x [days] [user]` | Set maximum password age |
| `sudo passwd -n [days] [user]` | Set minimum days between changes |
| `sudo passwd -w [days] [user]` | Set warning days before expiry |

**Example:**

```bash
$ passwd
Changing password for alice.
Current password:
New password:
Retype new password:
passwd: all authentication tokens updated successfully.
```

---

### `useradd` – Create User Accounts

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Low‑level command to create user accounts (non‑interactive, good for scripting) |

**Common options:**

| Option | Description |
|--------|-------------|
| `-d /home/dir` | Set custom home directory |
| `-u UID` | Set specific user ID |
| `-g GID` | Set primary group ID |
| `-M` | Do not create a home directory |
| `-e YYYY-MM-DD` | Account expiry date |
| `-c "comment"` | Add a comment (e.g., full name) |
| `-s /bin/shell` | Set default login shell |

**Examples:**

```bash
sudo useradd -d /home/test_user test_user
sudo useradd -u 1234 test_user
sudo useradd -g 1000 test_user
sudo useradd -M test_user          # no home directory
sudo useradd -e 2026-12-31 test_user
sudo useradd -c "John Developer" johnd
sudo useradd -s /bin/sh test_user
```

**Files modified by `useradd`:**

- `/etc/passwd` – user info
- `/etc/shadow` – encrypted password
- `/etc/group` – group info
- `/etc/gshadow` – secure group info
- `/home/[username]` – home directory (if created)

> **Note:** `adduser` (interactive) vs `useradd` (low‑level). On Debian/Ubuntu, `adduser` is friendlier. On RHEL/Fedora, `useradd` is standard.

---

### `history` – Command History

| Property | Value |
|----------|-------|
| **Abbreviation** | (none) |
| **Explanation** | Displays list of previously executed commands (default last 1000). Stored in `~/.bash_history`. |

**Common operations:**

| Command | Action |
|---------|--------|
| `history` | Show full history |
| `history N` | Show last N commands |
| `!1997` | Rerun command with event number 1997 |
| `!1997:p` | Print command #1997 without running it |
| `!!` | Rerun the last command |
| `!string` | Rerun the latest command starting with "string" |
| `history | grep pattern` | Search history |
| `history -d 1996` | Delete command #1996 |
| `history -c` | Clear entire history |

**Examples:**

```bash
$ history 5
 1995  ls -la
 1996  cd /var/log
 1997  cat messages
 1998  w
 1999  history 5

$ !1997
cat messages

$ !!
cat messages

$ history | grep passwd
 1985  sudo passwd alice
```

---

### Command Line Editing Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + A` | Jump to beginning of line |
| `Ctrl + E` | Jump to end of line |
| `Ctrl + D` | Logout (or delete character) |
| `Ctrl + L` | Clear screen |

**Logout commands:**

- `Ctrl + D`
- `logout`
- `exit`

---

## Key Takeaways for Cloud Engineering

- Knowing these commands is **daily work** for any cloud engineer (SSH into EC2, debugging containers, inspecting logs).
- `less`, `tail -f`, and `grep` are essential for **troubleshooting**.
- `useradd` and `passwd` are needed when **managing access** to Linux servers.
- History shortcuts (`!!`, `Ctrl+R`) save **massive time** in production.

---

## Practice Check

- [ ] I can explain the difference between `#` and `$` in the prompt
- [ ] I can list all files in a directory with human‑readable sizes (`ls -lah`)
- [ ] I can view the last 20 lines of a log file and follow it live
- [ ] I can search my command history for a specific command
- [ ] I can create a new user with a custom home directory and then switch to that user

---

**Date documented:** 2026-04-13  
**Source:** Linux Administration (Chapter 2 – Accessing the Command Line)

---
