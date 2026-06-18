# Bash Scripting

## Table of Contents

1. [What is a Shell? What is Bash? What is a Terminal?](#1-what-is-a-shell-what-is-bash-what-is-a-terminal)
2. [Setting Up the Bash Environment](#2-setting-up-the-bash-environment)
3. [Writing Your First Bash Script (Shebang)](#3-writing-your-first-bash-script-shebang)
4. [Variables and Constants](#4-variables-and-constants)
5. [User Input and Command‑Line Arguments](#5-user-input-and-commandline-arguments)
6. [Conditional Statements (`if`, `case`)](#6-conditional-statements-if-case)
7. [Loops (`for`, `while`, `until`)](#7-loops-for-while-until)
8. [Functions – Reusable Code Blocks](#8-functions--reusable-code-blocks)
9. [Arrays – Storing Lists of Data](#9-arrays--storing-lists-of-data)
10. [Exit Codes and Error Handling](#10-exit-codes-and-error-handling)
11. [Text Processing – `grep`, `sed`, `awk`, `find`, `cut`, `sort`, `uniq`](#11-text-processing--grep-sed-awk-find-cut-sort-uniq)
12. [Scripting Real‑World Examples](#12-scripting-realworld-examples)
    - 12.1 Log Analysis Script
    - 12.2 New Developer Environment Setup Script
    - 12.3 Log Rotation and Cleanup Script
13. [Writing to Files and Reporting](#13-writing-to-files-and-reporting)
14. [Scheduling Scripts with Cron](#14-scheduling-scripts-with-cron)
15. [Quick Reference Table](#15-quick-reference-table)
16. [Practice Lab – Verify Your Understanding](#16-practice-lab--verify-your-understanding)

---

## 1. What is a Shell? What is Bash? What is a Terminal?

| Term | Definition |
|------|------------|
| **Terminal** | The application (window) where you type commands. It displays output. |
| **Shell** | The program that interprets and executes your commands. It is the interface between you and the Linux kernel. |
| **Bash** | **B**ourne **A**gain **SH**ell – the most common shell on Linux. It is a full programming language, not just a command interpreter. |

**Why Bash?**
- Installed by default on almost every Linux distribution.
- Powerful scripting capabilities (variables, loops, conditionals, arrays).
- Great for system administration, automation, and DevOps.
- Other shells: `sh` (Bourne – older, less features), `zsh` (Z shell – more interactive), `fish` (Friendly Interactive SHell).

**CLI vs. GUI:**
- CLI is faster for repetitive tasks (e.g., creating 100 folders with one command: `mkdir folder{1..100}`).
- CLI is scriptable – you can automate complex workflows.

---

## 2. Setting Up the Bash Environment

| File | Purpose |
|------|---------|
| `~/.bashrc` | Executed for **interactive non‑login** shells. Commonly used for aliases, prompt customisation, environment variables. |
| `~/.bash_profile` | Executed for **login shells** (e.g., SSH, console login). Often sources `~/.bashrc`. |
| `~/.bash_history` | Stores command history (view with `history`). |
| `/etc/bashrc` | System‑wide bash configuration (applies to all users). |
| `/etc/profile` | System‑wide login shell configuration. |

**Common aliases (add to `~/.bashrc`):**
```bash
alias ll='ls -la'
alias gs='git status'
alias ..='cd ..'
```

**Reload without logging out:**
```bash
source ~/.bashrc
# or
. ~/.bashrc
```

---

## 3. Writing Your First Bash Script (Shebang)

A Bash script is a text file containing a series of commands. The **shebang** (`#!`) tells the OS which interpreter to use.

```bash
#!/bin/bash
# This is a comment
echo "Hello, World!"
```

**Make the script executable:**
```bash
chmod +x myscript.sh
```

**Run it:**
```bash
./myscript.sh          # requires execute permission
bash myscript.sh       # doesn't require execute permission
sh myscript.sh         # runs in POSIX mode (may fail with bash‑specific features)
source myscript.sh     # runs in current shell (variables persist)
```

**File naming:** Use `.sh` extension for readability – it helps editors with syntax highlighting, but it's not required.

---

## 4. Variables and Constants

### 4.1 Defining Variables (no spaces around `=`)

```bash
name="Alice"
age=30
greeting="Hello, $name!"   # double quotes allow variable expansion
```

**Access with `$`:**
```bash
echo $name
echo ${name}               # safer when variable is adjacent to other text
```

### 4.2 Environment Variables vs. Shell Variables

| Type | Scope | Definition |
|------|-------|------------|
| Shell variable | Current shell only | `MYVAR="hello"` |
| Environment variable | Inherited by child processes | `export MYVAR="hello"` |

**Common environment variables:**
```bash
echo $PATH              # directories where executables are found
echo $HOME              # user's home directory
echo $USER              # current username
echo $PWD               # current working directory
echo $SHELL             # current shell
```

### 4.3 Constants (readonly)

```bash
readonly PI=3.14159
PI=3.14                 # error: readonly variable
```

### 4.4 Command Substitution

Capture the output of a command into a variable.

```bash
# Modern syntax (preferred)
current_date=$(date +%Y-%m-%d)
file_count=$(ls -1 | wc -l)

# Legacy (backticks – deprecated)
current_date=`date +%Y-%m-%d`
```

---

## 5. User Input and Command‑Line Arguments

### 5.1 Reading User Input (`read`)

```bash
#!/bin/bash
echo "Enter your name:"
read name
echo "Hello, $name!"
```

**With a prompt in one line:**
```bash
read -p "Enter your age: " age
```

**Silent input (e.g., password):**
```bash
read -s -p "Enter password: " password
```

### 5.2 Command‑Line Arguments (`$1`, `$2`, ...)

| Special Variable | Meaning |
|------------------|---------|
| `$0` | Script name |
| `$1` | First argument |
| `$2` | Second argument |
| `$#` | Number of arguments |
| `$@` | All arguments (as separate strings) |
| `$*` | All arguments (as a single string) |
| `$?` | Exit code of the last command |
| `$$` | PID of the current shell |

**Example:**
```bash
#!/bin/bash
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Total arguments: $#"
```

**Checking if arguments are provided:**
```bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi
```

---

## 6. Conditional Statements (`if`, `case`)

### 6.1 `if` – Single Condition

```bash
if [ condition ]; then
    # code if true
elif [ another_condition ]; then
    # code if another_condition true
else
    # code if none true
fi
```

### 6.2 Numeric Comparisons

| Operator | Meaning |
|----------|---------|
| `-eq` | Equal |
| `-ne` | Not equal |
| `-lt` | Less than |
| `-le` | Less than or equal |
| `-gt` | Greater than |
| `-ge` | Greater than or equal |

**Example:**
```bash
age=25
if [ $age -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi
```

### 6.3 String Comparisons

| Operator | Meaning |
|----------|---------|
| `=`, `==` | Equal (POSIX uses `=`, bash accepts `==`) |
| `!=` | Not equal |
| `-z` | String is empty |
| `-n` | String is not empty |
| `<`, `>` | Lexicographic (use `[[ ]]`) |

**Example:**
```bash
name="Alice"
if [ "$name" = "Alice" ]; then
    echo "Hello Alice"
fi
```

### 6.4 File and Directory Tests

| Operator | True if |
|----------|---------|
| `-e file` | File exists |
| `-f file` | File exists and is a regular file |
| `-d dir` | Directory exists |
| `-r file` | File is readable |
| `-w file` | File is writable |
| `-x file` | File is executable |
| `-s file` | File exists and is not empty |
| `-L file` | File is a symbolic link |
| `file1 -nt file2` | file1 is newer than file2 |
| `file1 -ot file2` | file1 is older than file2 |

**Example:**
```bash
if [ -f "/etc/passwd" ]; then
    echo "passwd exists"
fi
if [ -d "$HOME" ]; then
    echo "Home directory exists"
fi
```

### 6.5 Logical Operators

| Operator | Meaning |
|----------|---------|
| `!` | NOT |
| `-a` | AND (in `[ ]`) |
| `-o` | OR (in `[ ]`) |
| `&&`, `\|\|` | AND, OR (in `[[ ]]` or outside) |

**Examples:**
```bash
# Using && inside if
if [ -f file.txt ] && [ -r file.txt ]; then
    echo "File exists and is readable"
fi

# Using || to handle failure
mkdir /tmp/testdir || echo "Failed to create directory"
```

### 6.6 `case` – Multiple Conditions

```bash
case $1 in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

---

## 7. Loops (`for`, `while`, `until`)

### 7.1 `for` – Iterate over a list

```bash
for item in item1 item2 item3; do
    echo "$item"
done
```

**Common patterns:**
```bash
# Numbers
for i in {1..10}; do
    echo "Number $i"
done

# Files
for file in *.txt; do
    echo "Processing $file"
done

# Command output
for user in $(cut -d: -f1 /etc/passwd); do
    echo "User: $user"
done

# C‑style loop
for ((i=0; i<10; i++)); do
    echo "i = $i"
done
```

### 7.2 `while` – Loop while condition is true

```bash
counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done
```

**Reading a file line by line:**
```bash
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt
```

### 7.3 `until` – Loop until condition is true

```bash
counter=1
until [ $counter -gt 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done
```

---

## 8. Functions – Reusable Code Blocks

### 8.1 Defining and Calling Functions

```bash
function greet() {
    echo "Hello, $1!"
}

greet "Alice"
```

### 8.2 Function with Return Value

Functions can return exit codes (0–255) using `return`.

```bash
is_even() {
    if (( $1 % 2 == 0 )); then
        return 0    # success = even
    else
        return 1    # failure = odd
    fi
}

is_even 4
if [ $? -eq 0 ]; then
    echo "Even"
else
    echo "Odd"
fi
```

### 8.3 Returning Strings via `echo`

```bash
get_date() {
    echo $(date +%Y-%m-%d)
}

today=$(get_date)
echo "Today is $today"
```

### 8.4 Local Variables in Functions

Variables defined inside a function are **global** unless marked `local`.

```bash
my_func() {
    local local_var="Only visible inside"
    global_var="Visible outside"
}
```

---

## 9. Arrays – Storing Lists of Data

### 9.1 Defining and Accessing Arrays

```bash
# Indexed array
fruits=("apple" "banana" "cherry")

echo ${fruits[0]}    # apple
echo ${fruits[1]}    # banana
echo ${#fruits[@]}   # length: 3

# All elements
echo ${fruits[@]}    # apple banana cherry
echo ${fruits[*]}    # same, but as a single string when quoted
```

**Add elements:**
```bash
fruits+=("date")
```

**Iterate over array:**
```bash
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done
```

### 9.2 Associative Arrays (Key‑Value)

```bash
declare -A user
user[name]="Alice"
user[role]="admin"
user[email]="alice@example.com"

echo "${user[name]}"   # Alice

for key in "${!user[@]}"; do
    echo "$key: ${user[$key]}"
done
```

---

## 10. Exit Codes and Error Handling

### 10.1 Exit Codes

Every command returns an exit code:
- `0` – success
- `1` – general error
- `2` – misuse of shell built‑in
- `126` – command cannot execute
- `127` – command not found
- `130` – terminated by Ctrl+C (SIGINT)

**Check exit code:**
```bash
$?                 # last command's exit code
```

**Set exit code in script:**
```bash
exit 0             # success
exit 1             # failure
```

### 10.2 Error Handling with `set`

| Option | Effect |
|--------|--------|
| `set -e` | Exit immediately if any command fails |
| `set -u` | Exit if an undefined variable is used |
| `set -x` | Print each command before executing (debugging) |
| `set -o pipefail` | Exit if any command in a pipeline fails |

**Example:**
```bash
#!/bin/bash
set -e          # stop on error
set -u          # error on undefined variables
set -o pipefail # pipe failures count

echo "This will run"
false           # exits immediately
echo "This will NOT run"
```

**Unset with:**
```bash
set +e
set +u
```

### 10.3 Trap Signals

```bash
# Clean up temporary files on exit
trap 'rm -f /tmp/mytemp.*; echo "Cleaned up"' EXIT
```

**Common signals:**
- `SIGINT` (Ctrl+C) – interrupt
- `SIGTERM` – terminate
- `SIGHUP` – hang up
- `EXIT` – script exit

**Example:**
```bash
#!/bin/bash
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/myfile.tmp
}

trap cleanup EXIT
trap "echo 'Ctrl+C pressed'; exit 1" SIGINT
```

---

## 11. Text Processing – `grep`, `sed`, `awk`, `find`, `cut`, `sort`, `uniq`

### 11.1 `grep` – Search for Patterns

| Option | Meaning |
|--------|---------|
| `-i` | Case‑insensitive |
| `-v` | Invert match (exclude) |
| `-c` | Count matches |
| `-l` | Show filenames with matches |
| `-n` | Show line numbers |
| `-r` | Recursive |
| `-E` | Extended regex |

**Examples:**
```bash
grep "ERROR" log.txt
grep -i "warning" *.log
grep -c "failed" /var/log/secure
grep -r "TODO" /home/user/projects/
ps aux | grep -v grep | grep sshd
```

### 11.2 `sed` – Stream Editor (Text Replacement)

**Syntax:** `sed 's/pattern/replacement/flags'`

**Examples:**
```bash
echo "apple apple" | sed 's/apple/orange/'       # orange apple
echo "apple apple" | sed 's/apple/orange/g'      # orange orange
sed -i.bak 's/old/new/g' file.txt                # in‑place with backup
sed '/pattern/d' file.txt                        # delete matching lines
```

### 11.3 `awk` – Pattern Scanning and Processing

**Syntax:** `awk 'pattern { action }' file`

**Examples:**
```bash
awk '{print $1}' /etc/passwd                     # first column
awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd  # users with UID >= 1000
awk '{sum += $1} END {print sum}' numbers.txt    # sum of first column
awk '/error/ {print NR, $0}' log.txt             # line number + error lines
```

### 11.4 `find` – Search for Files and Directories

**Syntax:** `find [path] [expression]`

**Common expressions:**
```bash
find . -name "*.log"                             # by name
find /var/log -type f -size +100M                # files >100MB
find /home -type d -name "temp"                  # directories named temp
find /tmp -mtime -1                              # modified in last 24 hours
find . -name "*.tmp" -exec rm {} \;              # delete found files
find / -type f -perm -4000 2>/dev/null           # SUID binaries
```

### 11.5 `cut` – Extract Columns

```bash
cut -d: -f1 /etc/passwd                          # usernames
cut -d: -f1,6 /etc/passwd                        # username and home dir
ls -l | cut -c1-10                               # first 10 chars
```

### 11.6 `sort` – Sort Lines

```bash
sort file.txt
sort -r file.txt
sort -n file.txt                                 # numeric
sort -k2 -n data.txt                             # sort by second column numeric
```

### 11.7 `uniq` – Remove/Count Duplicate Lines (requires sorted input)

```bash
sort names.txt | uniq -c                         # count occurrences
sort list.txt | uniq -d                          # show only duplicates
sort list.txt | uniq -u                          # show only unique
```

### 11.8 `wc` – Word, Line, Character Count

```bash
wc -l file.txt                                   # line count
ls | wc -l                                       # count files in directory
wc -w file.txt                                   # word count
```

---

## 12. Scripting Real‑World Examples

### 12.1 Log Analysis Script

**Problem:** Manually searching multiple log files for "ERROR" and "CRITICAL" is tedious and error‑prone.

**Solution:** A script that scans all logs, counts errors, and generates a report.

```bash
#!/bin/bash
# analyse-logs.sh – Analyze log files for errors and critical events

set -e

# Configuration
LOG_DIR="/var/log"
REPORT_FILE="log_analysis_report.txt"
ERROR_PATTERNS=("ERROR" "CRITICAL" "FATAL")

# Functions
check_logs() {
    local log_file="$1"
    echo "Processing: $log_file"
    echo "--- $log_file ---" >> "$REPORT_FILE"
    
    for pattern in "${ERROR_PATTERNS[@]}"; do
        count=$(grep -c "$pattern" "$log_file" 2>/dev/null || echo 0)
        echo "$pattern: $count" >> "$REPORT_FILE"
        
        if [ "$count" -gt 0 ]; then
            echo "First 3 lines with $pattern:" >> "$REPORT_FILE"
            grep "$pattern" "$log_file" | head -3 >> "$REPORT_FILE"
            echo "" >> "$REPORT_FILE"
        fi
    done
    echo "--------------------" >> "$REPORT_FILE"
}

# Main script
echo "Log Analysis Report" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "-----------------------------------" >> "$REPORT_FILE"

# Find log files from the last 24 hours
find "$LOG_DIR" -name "*.log" -type f -mtime -1 | while read -r logfile; do
    check_logs "$logfile"
done

echo "Report generated: $REPORT_FILE"
```

**Usage:**
```bash
./analyse-logs.sh
cat log_analysis_report.txt
```

### 12.2 New Developer Environment Setup Script

This script automates the setup of a new developer's local environment (common in DevOps onboarding).

```bash
#!/bin/bash
# setup-dev-env.sh – Configure a new developer's local environment

set -e

# Configuration
DEV_USER="$1"
DEV_HOME="/home/$DEV_USER"

if [ -z "$DEV_USER" ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

# Check if user exists
if ! id "$DEV_USER" &>/dev/null; then
    echo "Creating user: $DEV_USER"
    sudo useradd -m -s /bin/bash "$DEV_USER"
    echo "Set password for $DEV_USER:"
    sudo passwd "$DEV_USER"
fi

# Install common developer tools (RHEL example)
echo "Installing developer tools..."
sudo dnf groupinstall -y "Development Tools" 2>/dev/null || echo "Group not found"

# Add user to groups
echo "Adding user to required groups..."
sudo usermod -aG wheel,docker,dev "$DEV_USER"

# Clone configuration repository (if exists)
if [ -d "/etc/config-repo" ]; then
    sudo -u "$DEV_USER" git clone /etc/config-repo "$DEV_HOME/config"
fi

# Set up Git config
sudo -u "$DEV_USER" git config --global user.name "$DEV_USER"
sudo -u "$DEV_USER" git config --global user.email "$DEV_USER@example.com"

echo "Environment setup complete for $DEV_USER"
echo "User can now log in and start developing."
```

### 12.3 Log Rotation and Cleanup Script

This script scans logs, compresses old ones, checks disk space, and notifies admins.

```bash
#!/bin/bash
# log-cleanup.sh – Rotate, compress, and clean old logs

set -e

# Configuration
LOG_DIR="/var/log"
ARCHIVE_DIR="/var/log/archive"
DAYS_TO_KEEP=7
COMPRESSION="gzip"
MAX_DISK_USAGE=80
ADMIN_EMAIL="admin@example.com"

# Functions
send_alert() {
    local message="$1"
    echo "$message" | mail -s "Log Cleanup Alert" "$ADMIN_EMAIL"
}

# Create archive directory if missing
mkdir -p "$ARCHIVE_DIR"

# Compress logs older than 1 day
echo "Compressing logs older than 1 day..."
find "$LOG_DIR" -name "*.log" -type f -mtime +1 -exec $COMPRESSION {} \;

# Move compressed logs to archive
echo "Archiving old logs..."
find "$LOG_DIR" -name "*.gz" -type f -mtime +$DAYS_TO_KEEP -exec mv {} "$ARCHIVE_DIR" \;

# Delete logs older than 30 days from archive
echo "Deleting archived logs older than 30 days..."
find "$ARCHIVE_DIR" -name "*.gz" -type f -mtime +30 -delete

# Check disk usage
disk_usage=$(df -h "$LOG_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$disk_usage" -gt "$MAX_DISK_USAGE" ]; then
    send_alert "WARNING: Log directory is $disk_usage% full!"
fi

echo "Log cleanup complete."
```

---

## 13. Writing to Files and Reporting

### 13.1 Redirecting Output to Files

```bash
echo "Log entry" >> logfile.txt     # append
echo "New content" > logfile.txt    # overwrite
```

### 13.2 Here Document (Multi‑line Text)

```bash
cat << EOF > report.txt
Log Analysis Report
Generated: $(date)
--------------------
Total errors: $error_count
Total warnings: $warning_count
EOF
```

### 13.3 Redirecting Errors

```bash
command 2> error.log      # only stderr
command &> output.log     # both stdout and stderr
```

---

## 14. Scheduling Scripts with Cron

To run your script automatically:

```bash
crontab -e
```

**Example entries:**
```cron
# Run log analysis daily at 2 AM
0 2 * * * /home/scripts/analyse-logs.sh

# Run cleanup every Sunday at 3 AM
0 3 * * 0 /home/scripts/log-cleanup.sh

# Run a script every hour
0 * * * * /home/scripts/hourly-task.sh
```

---

## 15. Quick Reference Table

| Task | Command / Syntax |
|------|------------------|
| Shebang | `#!/bin/bash` |
| Make executable | `chmod +x script.sh` |
| Run script | `./script.sh` or `bash script.sh` |
| Define variable | `name="value"` |
| Access variable | `$name` |
| Command substitution | `$(command)` |
| If condition | `if [ condition ]; then ...; fi` |
| For loop | `for i in {1..10}; do ...; done` |
| While loop | `while [ condition ]; do ...; done` |
| Function | `func() { ... }` |
| Array define | `arr=("a" "b" "c")` |
| Array access | `${arr[0]}` |
| Exit code check | `$?` |
| Debugging | `set -x` |
| Strict mode | `set -euo pipefail` |

---

## 16. Practice Lab – Verify Your Understanding

1. **Hello World:** Create a script that prints "Hello, World!" and your current username.

2. **File checker:** Write a script that accepts a filename as an argument and prints whether it exists, is a file, or is a directory.

3. **Log analyzer:** Create a script that counts errors in `/var/log/messages` and outputs the top 5 most common error messages.

4. **User setup:** Script that creates a new user, sets a password, adds them to the `wheel` group, and creates a `.bashrc` file with common aliases.

5. **Disk usage alert:** Script that checks disk usage and sends an alert (to a file) if usage exceeds 80%.

6. **Backup script:** Create a script that compresses a directory, adds a timestamp to the filename, and moves it to a backup location. Keep only the last 7 backups.

---

**Date documented:** 2026-06-18  
**Sources:** Bash manual, Linux System Administration, Bash scripting best practices

---