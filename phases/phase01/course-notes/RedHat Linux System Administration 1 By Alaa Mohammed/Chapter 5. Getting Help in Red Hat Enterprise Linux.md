

# Linux Help & Documentation Commands

Linux provides several built-in utilities to help you understand commands and navigate the system without needing to search online.

---

## Primary Documentation Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `man` | Comprehensive manual pages | `man ls` |
| `--help` | Quick summary of options (external commands) | `ls --help` |
| `help` | Brief info for shell built‑in commands | `help cd` |
| `info` | More detailed, hyperlinked documentation | `info ls` |

---

## `man` – Manual Pages

**Abbreviation:** manual  
**Explanation:** Displays detailed documentation about commands, system calls, library functions, and configuration files. Includes syntax, options, examples, and cross‑references.

### Syntax

```bash
man [option] [command]
```

### Man Page Sections

Manuals are divided into numbered sections:

| Section | Content |
|---------|---------|
| 1 | Executable programs / shell commands (e.g., `ls`, `grep`) |
| 2 | System calls (e.g., `open`, `read`, `write`) |
| 3 | Library calls (e.g., `printf`, `malloc`) |
| 4 | Special files (e.g., `/dev/null`, `/dev/sda`) |
| 5 | File formats and conventions (e.g., `/etc/passwd`) |
| 6 | Games |
| 7 | Miscellaneous (macro packages, conventions) |
| 8 | System administration commands (e.g., `mount`, `iptables`) |
| 9 | Kernel routines (non‑standard) |

### Common Options

| Option | Description |
|--------|-------------|
| `man [command]` | Display the manual page for the specified command |
| `man [section] [command]` | Display manual page from a specific section |
| `-f`, `--whatis` | Show one‑line description of the command |
| `-k`, `--apropos` | Search for commands related to a keyword |
| `-a`, `--all` | Display all matching manual pages in succession |
| `-w`, `--where` | Show the file path of the manual page |
| `-I` | Case‑sensitive search |

### Navigation Inside `man` (when viewing a page)

| Key | Action |
|-----|--------|
| `Space` | Move forward one page |
| `Enter` | Move forward one line |
| `b` | Move backward one page |
| `/pattern` | Search forward for pattern |
| `n` | Next match |
| `q` | Quit |

### Examples

```bash
# Basic manual for ls
man ls

# Display intro from section 2 (system calls)
man 2 intro

# Show which sections contain the 'ls' command
man -f ls

# Search all manuals for keyword 'cd'
man -k cd

# Display all intro manuals one after another
man -a intro

# Show file location of ls manual page
man -w ls

# Case‑sensitive search for printf (lowercase only)
man -I printf
```

**Example output of `man -f ls`:**

```
ls (1)               - list directory contents
```

**Example output of `man -k cd`:**

```
cd (1)               - change the current directory
cd (1p)              - change directory (POSIX)
```

---

## `--help` Option

**Abbreviation:** (none)  
**Explanation:** Provides a quick summary of usage and available options for most external commands. Output is usually shorter than `man`.

### Syntax

```bash
<command> --help
```

### Example

```bash
ls --help
```

**Partial output:**

```
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
  -a, --all                  do not ignore entries starting with .
  -l                         use a long listing format
  -h, --human-readable       with -l, print sizes like 1K 234M 2G
```

---

## `help` – Shell Built‑in Help

**Abbreviation:** (none)  
**Explanation:** Displays brief information about **shell built‑in commands** (e.g., `cd`, `alias`, `history`, `echo`). Does not work for external commands like `ls` or `cp`.

### Syntax

```bash
help [built‑in]
```

### Example

```bash
help cd
```

**Output (partial):**

```
cd: cd [-L|[-P [-e]] [-@]] [dir]
    Change the shell working directory.
    Options:
      -L  force symbolic links to be followed
      -P  use the physical directory structure
```

---

## `info` – Hyperlinked Documentation

**Abbreviation:** (none)  
**Explanation:** Provides more detailed, structured, and hyperlinked documentation than `man`. Often includes examples and cross‑references.

### Syntax

```bash
info [command]
```

### Navigation Inside `info`

| Key | Action |
|-----|--------|
| `Space` | Next page |
| `b` | Beginning of document |
| `q` | Quit |
| `Tab` | Jump to next hyperlink |
| `Enter` | Follow hyperlink |

### Example

```bash
info ls
```

---

## Specialized Help Utilities

### `apropos` – Search Manual Descriptions

**Abbreviation:** (none)  
**Explanation:** Searches the **descriptions** of all manual pages for a given keyword. Useful when you don't remember the exact command name.

**Syntax:** `apropos <keyword>`

**Example:**

```bash
apropos archive
```

**Output (partial):**

```
tar (1)               - an archiving utility
zip (1)               - package and compress (archive) files
```

> **Note:** `apropos` is equivalent to `man -k`.

---

### `whatis` – One‑Line Command Description

**Abbreviation:** (none)  
**Explanation:** Displays a very short, one‑line description of what a command does.

**Syntax:** `whatis <command>`

**Example:**

```bash
whatis ls
```

**Output:**

```
ls (1)               - list directory contents
```

---

### `which` – Locate Executable Path

**Abbreviation:** (none)  
**Explanation:** Shows the full file path of the executable that runs when you type a command. Helps determine if a command is an external program, a script, or a built‑in.

**Syntax:** `which <command>`

**Example:**

```bash
which ls
```

**Output:**

```
/bin/ls
```

For a shell built‑in (e.g., `cd`), `which` may return nothing or indicate a built‑in.

---

## Quick Reference Table

| Command | Purpose | Example |
|---------|---------|---------|
| `man ls` | Full manual page | `man ls` |
| `man 2 intro` | Manual from section 2 | `man 2 intro` |
| `ls --help` | Quick option summary | `ls --help` |
| `help cd` | Help for shell built‑in | `help cd` |
| `info ls` | Hyperlinked documentation | `info ls` |
| `apropos keyword` | Search manual descriptions | `apropos network` |
| `whatis ls` | One‑line command description | `whatis ls` |
| `which ls` | Show executable path | `which ls` |

---

## Key Takeaways for Cloud Engineering

- **Never memorize every option** – know how to find them quickly with `--help` or `man`.
- Use `apropos` when you know what you want to do but not the command name (e.g., `apropos "compress"`).
- `which` is invaluable when troubleshooting `command not found` errors on EC2 instances or containers.
- Shell built‑ins (`cd`, `exit`, `history`) require `help`, not `man` (though `man` may redirect).

---

## Practice Check

- [ ] I can view the manual page for `cp` and find the option for recursive copying
- [ ] I can get a one‑line description of the `grep` command
- [ ] I can search for all manual pages related to "password"
- [ ] I can find the location of the `tar` executable
- [ ] I know the difference between `man`, `--help`, and `help`

---

**Date documented:** 2026-04-13  
**Sources:** Linux Administration, GeeksforGeeks, course notes

---
