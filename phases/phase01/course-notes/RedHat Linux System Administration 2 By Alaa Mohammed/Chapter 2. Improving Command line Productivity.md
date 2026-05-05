# Chapter 2: Improving Command Line Productivity

## Table of Contents

- [Chapter 2: Improving Command Line Productivity](#chapter-2-improving-command-line-productivity)
  - [Table of Contents](#table-of-contents)
  - [1. Shell Special Characters](#1-shell-special-characters)
  - [2. Bash Scripting – Everything You Need](#2-bash-scripting--everything-you-need)
    - [2.1 Anatomy of a Bash Script (Shebang)](#21-anatomy-of-a-bash-script-shebang)
    - [2.2 Script Arguments and User Input](#22-script-arguments-and-user-input)
    - [2.3 `$()` vs `${}` – Command Substitution vs Variable Expansion](#23--vs---command-substitution-vs-variable-expansion)
    - [2.4 Comparison Expressions (Numeric, String, File Tests)](#24-comparison-expressions-numeric-string-file-tests)
      - [Numeric Comparisons (use `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`)](#numeric-comparisons-use--eq--ne--lt--le--gt--ge)
      - [String Comparisons](#string-comparisons)
      - [File Test Operators (used with `[ -f file ]`)](#file-test-operators-used-with---f-file-)
    - [2.5 Exit Codes and `return`](#25-exit-codes-and-return)
    - [2.6 The `test` Command and `[ ]` / `[[ ]]` Syntax](#26-the-test-command-and------syntax)
    - [2.7 Running a Bash Script (4 Methods)](#27-running-a-bash-script-4-methods)
  - [3. Environment Variables](#3-environment-variables)
    - [3.1 What Are Environment Variables?](#31-what-are-environment-variables)
    - [3.2 `$PATH` – How the Shell Finds Commands](#32-path--how-the-shell-finds-commands)
    - [3.3 Adding Your Own Scripts to `$PATH`](#33-adding-your-own-scripts-to-path)
      - [Temporary (for the current shell session)](#temporary-for-the-current-shell-session)
      - [Permanent (for a specific user only)](#permanent-for-a-specific-user-only)
      - [Permanent (system‑wide)](#permanent-systemwide)
    - [3.4 Other Important Environment Files](#34-other-important-environment-files)
  - [4. Text Processing – Tools, Options, and Regex](#4-text-processing--tools-options-and-regex)
    - [4.1 `grep` – Search Text Using Patterns](#41-grep--search-text-using-patterns)
    - [4.2 `sed` – Stream Editor for Text Transformation](#42-sed--stream-editor-for-text-transformation)
    - [4.3 `awk` – Pattern Scanning and Processing](#43-awk--pattern-scanning-and-processing)
    - [4.4 `cut` – Remove Sections from Lines](#44-cut--remove-sections-from-lines)
    - [4.5 `sort` – Sort Lines](#45-sort--sort-lines)
    - [4.6 `uniq` – Report or Omit Repeated Lines](#46-uniq--report-or-omit-repeated-lines)
    - [4.7 `wc` – Word, Line, Character Count](#47-wc--word-line-character-count)
    - [4.8 `tr` – Translate or Delete Characters](#48-tr--translate-or-delete-characters)
    - [4.9 Regular Expressions (Regex) – Complete Reference](#49-regular-expressions-regex--complete-reference)
  - [5. Quick Reference Table](#5-quick-reference-table)
  - [6. Real‑World Scenario – Analyzing a Failed Service Log](#6-realworld-scenario--analyzing-a-failed-service-log)
    - [Step 1 – Gather Basic Information](#step-1--gather-basic-information)
    - [Step 2 – Extract Relevant Errors from the Log](#step-2--extract-relevant-errors-from-the-log)
    - [Step 3 – Analyse the Error Occurrences](#step-3--analyse-the-error-occurrences)
    - [Step 4 – Process a Specific Time Window](#step-4--process-a-specific-time-window)
    - [Step 5 – Automate Diagnosis with a Bash Script](#step-5--automate-diagnosis-with-a-bash-script)
    - [Step 6 – Parse and Format Configuration for a Report](#step-6--parse-and-format-configuration-for-a-report)
    - [Step 7 – Clean Up Old Log Files Using a Regex](#step-7--clean-up-old-log-files-using-a-regex)
    - [Step 8 – Validate the Solution](#step-8--validate-the-solution)
  - [7. Practice Lab – Verify Your Understanding](#7-practice-lab--verify-your-understanding)

---

## 1. Shell Special Characters

The shell interprets many characters specially. Mastering them is key to command‑line productivity.

| Character | Name | Meaning / Use |
|-----------|------|----------------|
| `~` | Tilde | User's home directory. `~` = current user's home, `~alice` = home of alice. |
| `#` | Hash | Start of a comment (ignores rest of line) |
| `$` | Dollar | Variable expansion (e.g., `$VAR` or `${VAR}`) |
| `*` | Asterisk | Wildcard (matches any string, including empty) |
| `?` | Question mark | Wildcard (matches exactly one character) |
| `[ ]` | Square brackets | Character class (e.g., `[abc]` matches a, b, or c) |
| `{ }` | Curly braces | Brace expansion (e.g., `file{1,2,3}` -> `file1 file2 file3`) |
| `` ` `` | Backtick | Command substitution (old style, same as `$()`) |
| `$( )` | Dollar+parentheses | Command substitution (preferred) |
| `" "` | Double quotes | Weak quoting: variables and commands inside are expanded |
| `' '` | Single quotes | Strong quoting: no expansion whatsoever |
| `\` | Backslash | Escape character: removes special meaning of next character |
| `\|` | Pipe | Sends stdout of left command to stdin of right command |
| `&` | Ampersand | Run command in background |
| `;` | Semicolon | Command separator (run sequentially) |
| `&&` | AND operator | Right command runs only if left succeeds (exit 0) |
| `\|\|` | OR operator | Right command runs only if left fails (non‑zero exit) |
| `>` | Redirection | Redirect stdout to file (overwrite) |
| `>>` | Append redirection | Redirect stdout to file (append) |
| `2>` | Error redirection | Redirect stderr (file descriptor 2) |
| `&>` | Redirect both stdout and stderr | Both streams to same file |
| `<` | Input redirection | Feed file as stdin to command |
| `<<` | Here document | Inline input redirection |
| `<<<` | Here string | Pass a string as stdin to a command |

**Examples:**
```bash
# Wildcards
ls f??*               # files starting with f then at least 2 more chars
ls *.text             # all files ending with .text

# Brace expansion
echo {1..10}          # 1 2 3 4 5 6 7 8 9 10
mkdir backup{2026..2029}  # creates backup2026 to backup2029

# Command substitution
echo "Today is $(date +%A)"   # Today is Tuesday

# Pipes and redirections
cat file.txt | grep "error" | wc -l > error_count.txt
```

---

## 2. Bash Scripting – Everything You Need

### 2.1 Anatomy of a Bash Script (Shebang)

The **shebang** (`#!`) is the first line of a script. It tells the kernel which interpreter to use.

```bash
#!/bin/bash
# This is a comment
echo "Hello, World!"
```

- The script must be executable (`chmod +x script.sh`).
- Common shebangs: `#!/bin/bash`, `#!/bin/sh`, `#!/usr/bin/env python3`.
- Without a shebang, the current shell's interpreter is used (bash, zsh, etc.).

### 2.2 Script Arguments and User Input

Scripts can accept command‑line arguments and prompt the user for input.

**Positional parameters:**
- `$1`, `$2`, … – first, second, … argument
- `$0` – the script name itself
- `$#` – number of arguments
- `$@` – all arguments as separate words
- `$*` – all arguments as one string

**Example:**
```bash
#!/bin/bash
echo "Script name: $0"
echo "First argument: $1"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

**Reading user input:**
```bash
#!/bin/bash
read -p "Enter your name: " username
echo "Hello, $username"
```

Sensitive input can be hidden with `-s`:
```bash
read -sp "Password: " pass
echo "Password entered."
```

### 2.3 `$()` vs `${}` – Command Substitution vs Variable Expansion

| Syntax | Name | Use | Example |
|--------|------|-----|---------|
| `$(command)` | Command substitution | Run command and capture its output | `files=$(ls)` |
| `${variable}` | Variable expansion | Safely access variable value (braces often optional) | `echo "${USER}_file"` |

**Key difference:**
- `$()` replaces the whole expression with the output of the command inside.
- `${}` simply expands a variable; braces are useful when the variable name is adjacent to other characters that could be misinterpreted.

**Examples:**
```bash
current_date=$(date +%Y-%m-%d)
echo "Today is $current_date"

filename="backup"
echo "${filename}_2026.txt"    # backup_2026.txt
echo "$filename_2026.txt"      # (empty, because _2026 is part of var name)

# Nested substitution
file_count=$(ls -1 | wc -l)
echo "Number of files: $(($file_count + 1))"
```

### 2.4 Comparison Expressions (Numeric, String, File Tests)

#### Numeric Comparisons (use `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`)

| Operator | Meaning |
|----------|---------|
| `-eq` | equal |
| `-ne` | not equal |
| `-lt` | less than |
| `-le` | less than or equal |
| `-gt` | greater than |
| `-ge` | greater than or equal |

**Example:**
```bash
age=25
if [ $age -ge 18 ]; then
    echo "Adult"
fi
```

#### String Comparisons

| Operator | Meaning |
|----------|---------|
| `=` or `==` | equal (POSIX uses `=`, bash accepts `==`) |
| `!=` | not equal |
| `-z` | string is empty (zero length) |
| `-n` | string is not empty |
| `<` | lexicographically less (in `[[ ]]`) |
| `>` | lexicographically greater (in `[[ ]]`) |

**Examples:**
```bash
name="Alice"
if [ "$name" = "Alice" ]; then
    echo "Hello Alice"
fi

if [ -z "$var" ]; then
    echo "var is empty or unset"
fi

# Always quote variables in [ ] to avoid syntax errors when empty.
```

#### File Test Operators (used with `[ -f file ]`)

| Operator | True if |
|----------|---------|
| `-e file` | file exists |
| `-f file` | file exists and is a regular file |
| `-d file` | file exists and is a directory |
| `-r file` | file is readable |
| `-w file` | file is writable |
| `-x file` | file is executable |
| `-s file` | file exists and is not empty |
| `-L file` | file is a symbolic link |
| `file1 -nt file2` | file1 is newer than file2 |
| `file1 -ot file2` | file1 is older than file2 |

**Examples:**
```bash
if [ -f /etc/passwd ]; then
    echo "passwd exists"
fi

if [ -d "$HOME" ]; then
    echo "Home directory exists"
fi
```

### 2.5 Exit Codes and `return`

- Every command returns an **exit code** (0–255).  
  **0** = success (true), **non‑zero** = failure or false.

```bash
ls /tmp
echo $?      # prints 0 if success, else 2 (commonly for "no such file")
```

Use exit codes in conditionals:
```bash
if grep -q "error" log.txt; then
    echo "Error found"
else
    echo "No error"
fi
```

**`exit`** sets the exit code of the script itself.  
**`return`** is used inside functions to set the function’s exit code.

```bash
function is_even {
    local num=$1
    if (( num % 2 == 0 )); then
        return 0    # success = even
    else
        return 1    # failure = odd
    fi
}

is_even 4
echo $?   # prints 0
```

### 2.6 The `test` Command and `[ ]` / `[[ ]]` Syntax

The `test` command evaluates expressions and returns 0 (true) or non‑zero (false).

```bash
# Equivalent forms:
test -f /etc/passwd
[ -f /etc/passwd ]
[[ -f /etc/passwd ]]   # bash extended test
```

**Difference between `[ ]` and `[[ ]]`:**

| Feature | `[ ]` (POSIX) | `[[ ]]` (Bash) |
|---------|---------------|----------------|
| Word splitting | Yes (variables must be quoted) | No (safe without quotes) |
| Pattern matching | No | Yes (`==` with wildcards) |
| Regex matching | No | Yes (`=~`) |
| Logical operators | `-a` (and), `-o` (or) | `&&`, `\|\|` inside |
| `< >` comparison | Lexicographic (needs escaping) | Lexicographic inside |

**Examples:**
```bash
# POSIX style – quote variables
if [ "$USER" = "root" ]; then
    echo "Hello root"
fi

# Bash extended – no quotes, pattern matching
if [[ $USER == r* ]]; then
    echo "Username starts with r"
fi

# Regex matching
if [[ "abc123" =~ ^[a-z]+[0-9]+$ ]]; then
    echo "Matches pattern"
fi
```

### 2.7 Running a Bash Script (4 Methods)

| Method | Command | Notes |
|--------|---------|-------|
| 1. Execute directly (must have execute permission) | `./script.sh` | Works if script has shebang and `chmod +x` |
| 2. Invoke bash interpreter | `bash script.sh` | No execute permission needed; ignores shebang |
| 3. Invoke sh interpreter | `sh script.sh` | Runs in POSIX mode; may fail if uses bash extensions |
| 4. Source (run in current shell) | `source script.sh` or `. script.sh` | Variables and functions remain available after script ends |

**Important difference:**
- Executing (`./script` or `bash script`) runs the script in a **subshell** – changes to environment variables are lost.
- **Sourcing** runs the script in the **current shell** – useful for setting environment variables or aliases.

---

## 3. Environment Variables

### 3.1 What Are Environment Variables?

Environment variables are name‑value pairs inherited by child processes. They control system behaviour (e.g., `PATH`, `HOME`, `LANG`).

```bash
# List all environment variables
env

# Print a variable
echo $HOME
echo ${PATH}

# Set a variable (local to shell, not exported to child processes)
MYVAR="hello"

# Export to make it available to child processes
export MYVAR="hello"

# Unset a variable
unset MYVAR
```

### 3.2 `$PATH` – How the Shell Finds Commands

`PATH` is a colon‑separated list of directories where the shell looks for executables.

```bash
echo $PATH
# Typical output: /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

When you type a command (e.g., `ls`), the shell searches each directory in order until it finds an executable with that name.

### 3.3 Adding Your Own Scripts to `$PATH`

#### Temporary (for the current shell session)

```bash
export PATH="$PATH:/home/username/scripts"
```

Now scripts placed in `~/scripts` can be run from anywhere without `./`.

#### Permanent (for a specific user only)

Edit the user's `~/.bashrc` (for interactive non‑login shells) or `~/.bash_profile` / `~/.profile` (for login shells) and add:

```bash
export PATH="$PATH:$HOME/bin"
```

Reload without logging out: `source ~/.bashrc`

#### Permanent (system‑wide)

Edit `/etc/bashrc` (or `/etc/bash.bashrc` on Debian‑based) or `/etc/environment` (for all processes, not just bash) and add:

```bash
export PATH="$PATH:/opt/myscripts"
```

### 3.4 Other Important Environment Files

| File | Scope | Purpose |
|------|-------|---------|
| `/etc/environment` | system‑wide, all shells | Defines global environment variables (not a script, just `KEY=value`). |
| `/etc/profile` | system‑wide, login shells | Shell initialisation script. |
| `~/.bash_profile` | user‑specific, login bash | Personalised init for login shells. |
| `~/.bashrc` | user‑specific, interactive non‑login shells | Aliases, functions, prompt. |
| `/etc/bashrc` | system‑wide, interactive non‑login shells | System‑wide bash settings. |

**Note:** The exact files sourced depend on whether the shell is a login shell or an interactive shell. Knowing this helps debug PATH issues.

---

## 4. Text Processing – Tools, Options, and Regex

### 4.1 `grep` – Search Text Using Patterns

`grep` searches for patterns (basic regex by default) in files or stdin.

| Option | Meaning |
|--------|---------|
| `-i` | Case‑insensitive |
| `-v` | Invert match (print non‑matching lines) |
| `-c` | Count matching lines |
| `-l` | Print only filenames with matches |
| `-n` | Show line numbers |
| `-r` | Recursively search directories |
| `-E` | Extended regex (same as `egrep`) |
| `-o` | Print only the matched part of the line |
| `-A N` | Show N lines **after** match |
| `-B N` | Show N lines **before** match |
| `-C N` | Show N lines **around** match (context) |

**Examples:**
```bash
grep "error" /var/log/messages
grep -i "warning" *.log
grep -r "TODO" /home/user/projects/
grep -E "FAILED|DENIED" auth.log
ps aux | grep -v grep | grep sshd
```

### 4.2 `sed` – Stream Editor for Text Transformation

`sed` performs non‑interactive text substitutions, deletions, insertions.

**Basic syntax:** `sed 's/pattern/replacement/flags'`

**Common flags:**
- `g` – global (all matches on line)
- `i` – case‑insensitive (GNU sed)
- `p` – print the changed line (often with `-n`)

**Examples:**
```bash
# Substitute first "apple" with "orange" per line
echo "apple apple" | sed 's/apple/orange/'
# orange apple

# Substitute all (global)
echo "apple apple" | sed 's/apple/orange/g'
# orange orange

# In‑place edit (backup original)
sed -i.bak 's/old/new/g' file.txt

# Delete lines containing "pattern"
sed '/pattern/d' file.txt

# Print only lines 10 to 20
sed -n '10,20p' file.txt
```

### 4.3 `awk` – Pattern Scanning and Processing

`awk` processes structured text (columns). Basic structure: `awk 'pattern { action }' file`

**Built‑in variables:**
- `$1`, `$2`, ... – column numbers
- `NF` – number of fields (columns) in current line
- `NR` – current line number
- `$0` – whole line

**Examples:**
```bash
# Print first column
awk '{print $1}' /etc/passwd

# Print lines where column 3 > 1000
awk -F: '$3 > 1000 {print $1, $3}' /etc/passwd

# Sum column values
awk '{sum += $1} END {print sum}' numbers.txt

# Print lines with pattern
awk '/error/ {print NR, $0}' log.txt
```

### 4.4 `cut` – Remove Sections from Lines

`cut` extracts columns or character positions.

| Option | Meaning |
|--------|---------|
| `-d DELIM` | Use DELIM as field separator (default TAB) |
| `-f FIELDS` | Select fields (1‑based, can use ranges like `2-5`) |
| `-c RANGE` | Select characters (e.g., `-c 1-10`) |

**Examples:**
```bash
cut -d: -f1 /etc/passwd          # list usernames
cut -d: -f1,6 /etc/passwd        # username and home directory
echo "col1 col2 col3" | cut -d' ' -f2   # col2
ls -l | cut -c1-10                # first 10 chars of each line
```

### 4.5 `sort` – Sort Lines

| Option | Meaning |
|--------|---------|
| `-n` | Numeric sort |
| `-r` | Reverse order |
| `-k` | Sort by key (e.g., `-k2` sorts by second field) |
| `-t` | Field separator |
| `-u` | Unique (remove duplicates) |
| `-h` | Human‑readable (e.g., 1K, 2M) |

**Examples:**
```bash
sort file.txt
sort -r file.txt
ls -l | sort -k5 -n          # sort by file size (5th column) numerically
sort -t: -k3 -n /etc/passwd  # sort by UID
```

### 4.6 `uniq` – Report or Omit Repeated Lines

`uniq` normally works on **sorted** input. It removes or counts adjacent duplicates.

| Option | Meaning |
|--------|---------|
| `-c` | Count occurrences |
| `-d` | Print only duplicate lines |
| `-u` | Print only unique lines |

**Examples:**
```bash
sort names.txt | uniq -c     # count occurrences
sort list.txt | uniq -d      # show only duplicates
```

### 4.7 `wc` – Word, Line, Character Count

| Option | Meaning |
|--------|---------|
| `-l` | Lines |
| `-w` | Words |
| `-c` | Bytes |
| `-m` | Characters |
| `-L` | Length of longest line |

**Examples:**
```bash
wc -l file.txt      # line count
ls | wc -l          # count files in directory
ps aux | wc -l      # count processes
```

### 4.8 `tr` – Translate or Delete Characters

`tr` replaces or deletes characters from stdin.

**Syntax:** `tr [options] SET1 [SET2]`

| Option | Meaning |
|--------|---------|
| `-d` | Delete characters in SET1 |
| `-s` | Squeeze repeated characters |
| `-t` | Truncate SET1 to length of SET2 |

**Examples:**
```bash
echo "Hello World" | tr '[:lower:]' '[:upper:]'   # HELLO WORLD
echo "abc123" | tr -d 'a-z'                       # 123
cat file.txt | tr -s '\n'                         # replace multiple newlines with single
```

### 4.9 Regular Expressions (Regex) – Complete Reference

Regex is used with `grep -E`, `sed`, `awk`, `less`, `vim`, etc.

| Metacharacter | Meaning |
|---------------|---------|
| `.` | Any single character (except newline) |
| `*` | Zero or more of the preceding character/group |
| `+` | One or more of the preceding (ERE – extended) |
| `?` | Zero or one of the preceding (ERE) |
| `^` | Start of line |
| `$` | End of line |
| `[abc]` | Character class – a, b, or c |
| `[^abc]` | Negated class – any except a,b,c |
| `[a-z]` | Range – lowercase letters |
| `\|` | Alternation (OR) – `(cat\|dog)` |
| `( )` | Grouping – apply quantifiers to a group |
| `{n}` | Exactly n occurrences |
| `{n,}` | At least n occurrences |
| `{n,m}` | Between n and m occurrences |
| `\` | Escape special character |
| `\b` | Word boundary (GNU grep) |
| `\d` | Digit (Perl‑like, not in basic grep; use `[0-9]`) |

**Examples (using `grep -E` for extended regex):**
```bash
grep -E '^root:' /etc/passwd               # lines starting with "root:"
grep -E 'error|failed' log.txt             # lines containing error OR failed
grep -E '^[0-9]{1,3}\.[0-9]{1,3}' ip.txt   # lines starting with IPv4 pattern
grep -E 'http(s)?://' urls.txt             # http or https
grep -E '\b[0-9]{4}\b' file.txt            # exactly 4 digit numbers as whole words
```

---

## 5. Quick Reference Table

| Task | Command / Expression |
|------|----------------------|
| Find text in files | `grep -r "pattern" /path/` |
| Case‑insensitive search | `grep -i "pattern" file` |
| Replace text in file (in‑place) | `sed -i 's/old/new/g' file` |
| Print first column | `awk '{print $1}' file` |
| Cut first field (colon‑separated) | `cut -d: -f1 /etc/passwd` |
| Sort by second column numerically | `sort -k2 -n file` |
| Count unique lines | `sort file \| uniq -c` |
| Count lines in file | `wc -l file` |
| Convert to uppercase | `tr '[:lower:]' '[:upper:]'` |
| Regex – line starting with digit | `^[0-9]` |
| Regex – valid email (simple) | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` |

---

## 6. Real‑World Scenario – Analyzing a Failed Service Log

**Background:** As a junior sysadmin, you receive an alert that the `webapp` service on server `srv01` has failed. You SSH into the server and need to quickly diagnose the cause using command‑line tools. The service writes logs to `/var/log/webapp/app.log`.

### Step 1 – Gather Basic Information

Check if the service is running and how many times it has failed recently.

```bash
systemctl status webapp
journalctl -u webapp --since "30 minutes ago"
```

### Step 2 – Extract Relevant Errors from the Log

Use `grep` to isolate lines containing “ERROR” or “FATAL”:

```bash
grep -E 'ERROR|FATAL' /var/log/webapp/app.log
```

Too many lines? Save the result to a file for further processing:

```bash
grep -E 'ERROR|FATAL' /var/log/webapp/app.log > /tmp/errors.log
```

### Step 3 – Analyse the Error Occurrences

Count total error lines:

```bash
wc -l /tmp/errors.log
```

Find the most common error messages:

```bash
awk '{print $4 " " $5}' /tmp/errors.log | sort | uniq -c | sort -nr
```

(Assumes the error type/keyword is in fields 4–5; adjust to match actual log format.)

### Step 4 – Process a Specific Time Window

If the failure started at 14:00, extract only the last hour:

```bash
grep "2026-05-05 14" /var/log/webapp/app.log | grep ERROR
```

Or with `sed` to print lines between two timestamps:

```bash
sed -n '/2026-05-05 14:00/,/2026-05-05 15:00/p' /var/log/webapp/app.log
```

### Step 5 – Automate Diagnosis with a Bash Script

Create a small diagnostic script `/home/admin/bin/diag_webapp.sh`:

```bash
#!/bin/bash
LOGFILE="/var/log/webapp/app.log"
echo "=== WebApp Error Report ==="
echo "Total error lines: $(grep -c ERROR $LOGFILE)"
echo "Top 5 error types:"
grep ERROR $LOGFILE | awk '{print $4}' | sort | uniq -c | sort -nr | head -5
echo "Errors in last hour:"
grep "$(date +%Y-%m-%d) $(date +%H)" $LOGFILE | grep -c ERROR
```

Make it executable and add to your PATH:

```bash
chmod +x /home/admin/bin/diag_webapp.sh
export PATH="$PATH:/home/admin/bin"   # temporary, or add to ~/.bashrc
```

Now you can run `diag_webapp.sh` from anywhere.

### Step 6 – Parse and Format Configuration for a Report

Extract the last 50 lines of the log and format them as a CSV for further analysis:

```bash
tail -50 /var/log/webapp/app.log | awk '{print $1","$2","$3","$4","$5","$6}' > /tmp/report.csv
```

### Step 7 – Clean Up Old Log Files Using a Regex

Remove archived logs older than 30 days (files matching `app.log-2026-04*`):

```bash
find /var/log/webapp -name "app.log-2026-04*" -delete
```

Or using an extended glob (if enabled):

```bash
rm -f /var/log/webapp/app.log-2026-04{01..30}
```

### Step 8 – Validate the Solution

After fixing the root cause (e.g., a configuration error), use a simple regex check to verify the main config line is correct:

```bash
grep -E '^Listen\s+0.0.0.0:8080$' /etc/webapp/config.conf
```

---

This scenario demonstrates how shell special characters, scripting, environment management, and text processing tools combine to solve real‑world sysadmin tasks quickly and efficiently.

---

## 7. Practice Lab – Verify Your Understanding

1. **Special characters:** Create a directory with `mkdir testdir{1..5}`. Use a wildcard `?` to list only directories with a single digit.
2. **Bash script:** Write a script that accepts a filename as argument and prints whether it is a regular file, directory, or other. Use `test` operators.
3. **Exit codes:** Write a function `is_prime` that returns 0 if the number is prime, else 1. Use it in an `if` statement.
4. **PATH modification:** Add a temporary directory to your `PATH`, place a script there, and run it from another directory.
5. **Text processing:** Given the file `/etc/passwd`, extract the usernames and UIDs of users whose shell is `/bin/bash`. (Hint: `grep`, `cut`, or `awk`).
6. **Regex:** From a log file, extract all lines containing IPv4 addresses (e.g., `192.168.1.100`). Use `grep -E`.
7. **`sed` practice:** Replace all occurrences of `foo` with `bar` in a file, but only on lines that contain `baz`.
8. **Process pipeline:** Count how many processes your user is running. Use `ps -u $USER | tail -n +2 | wc -l`.
9. **Create a diagnostic script** similar to the real‑world scenario but for a different service (e.g., SSH). Automate the detection of failed logins from `/var/log/secure`.

---

**Date documented:** 2026-05-05  
**Sources:** Red Hat System Administration, Bash manual, GNU grep/sed/awk documentation, man pages

---