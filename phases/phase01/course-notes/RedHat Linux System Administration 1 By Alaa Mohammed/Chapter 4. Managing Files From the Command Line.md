
# File Operations – Creating, Copying, Moving, Removing & Links

## 1. Basic File Management (CRUD)

Your essential commands for creating, reading, updating, and deleting files and directories.

| Operation | Command(s) | Description |
|-----------|------------|-------------|
| **Create (File)** | `touch` or `>` | Creates an empty file or redirects output to a new file |
| **Create (Dir)** | `mkdir` | Makes a new directory (use `-p` for nested paths) |
| **Read/View** | `cat`, `less`, `head`, `tail` | Displays content. `less` is best for large files |
| **Update/Edit** | `nano`, `vim`, `vi` | Terminal-based text editors |
| **Delete** | `rm`, `rmdir` | Removes files or empty directories. `rm -rf` deletes folders with content |

---

## 2. Navigation & Organization

| Command | Purpose |
|---------|---------|
| `pwd` | Print Working Directory – shows where you are |
| `cd` | Change directory |
| `ls` | List files. Use `ls -la` to see hidden files and details |
| `mv` | Move or rename files/folders |
| `cp` | Copy files. Use `cp -r` for directories |

---

## 3. Archiving & Compression

| Command | Description |
|---------|-------------|
| `tar` | Tape Archiver – bundles files together (e.g., `tar -cvf archive.tar folder/`) |
| `gzip` / `zip` / `xz` | Different compression algorithms to shrink file size |

---

## 4. Pipes and Redirection (Combine Commands)

| Symbol | Name | Description |
|--------|------|-------------|
| `|` | Pipe | Takes output of one command and sends it as input to another (e.g., `ls \| grep "txt"`) |
| `>` | Redirect (overwrite) | Saves output to a file, overwriting if exists |
| `>>` | Redirect (append) | Adds output to the end of an existing file |

---

## 5. Links – Hard vs Soft (Symbolic)

In Linux, there are two types of links. Think of them as the difference between a "twin" and a "shortcut."

| Link Type | Command | Description |
|-----------|---------|-------------|
| **Hard Link** | `ln [target] [link_name]` | Creates a new filename pointing to the same data on disk. Deleting the original leaves the data as long as the hard link exists. Cannot cross filesystems or link directories. |
| **Soft (Symbolic) Link** | `ln -s [target] [link_name]` | Like a Windows shortcut – points to the *name* of the original file. If original is deleted, the link breaks. Can cross filesystems and link directories. |

### Hard Links – Key Points

- Same Inode value as original → reference the same physical file location
- `ls -l` shows link count in the second column
- Removing any link just reduces link count; other links remain valid
- Changing original filename does not break hard links
- Cannot create hard link for a directory (avoids recursive loops)
- Size of all hard links is identical; changes to content reflect everywhere

**Command:** `ln original.txt link.txt`

### Soft Links – Key Points

- Separate Inode value that points to the original file's path
- `ls -l` shows first column as `l` and an arrow `->` to the original
- Removing soft link does nothing; removing original creates a "dangling" link
- Can link to directories
- Size of soft link equals the length of the path string (e.g., 14 bytes for `/tmp/hello.txt`)
- If original file is renamed, the soft link breaks

**Command:** `ln -s original.txt link.txt`

---

## 6. Paths – Absolute vs Relative

### Absolute Path – The "Full Address"

Starts from the root (`/`). Works no matter where you are.

**Example:** `/home/username/Documents`

### Relative Path – The "Directions from Here"

Starts from your current directory. Only works if you are in the right starting spot.

**Example:** `Documents/` (if already in `/home/username`)

### Path Shortcut Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `.` | Current directory | `./script.sh` |
| `..` | Parent directory (one level up) | `cd ..` |
| `~` | Your home directory | `cd ~/Downloads` |
| `-` | Previous directory | `cd -` (toggles back) |

---

## 7. `mkdir` – Make Directory

**Abbreviation:** make directory  
**Explanation:** Creates new folders. Essential for organizing the filesystem.

### Most Used Options

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-p` | `--parents` | Creates parent directories if they don't exist; no error if folder exists |
| `-v` | `--verbose` | Prints a message for every directory created |
| `-m` | `--mode` | Sets permissions at creation (like `chmod`) |

### Examples

```bash
# Basic create
mkdir docs

# Create nested directories (parents if needed)
mkdir -p project/code/python

# Create multiple folders at once
mkdir images videos documents
mkdir lab{1..3}          # creates lab1, lab2, lab3

# Create with specific permissions (only owner has access)
mkdir -m 700 private_data
```

---

## 8. `cp` – Copy Files and Directories

**Abbreviation:** copy  
**Explanation:** Duplicates files or directories from one location to another.

### Syntax

```bash
cp [options] <source> <destination>
cp [options] <source1> <source2> ... <destination_directory>
```

### Common Options

| Option | Description |
|--------|-------------|
| `-i` | Interactive – prompt before overwriting |
| `-f` | Force – overwrite without prompt |
| `-r` or `-R` | Recursive – copy directories and their contents |
| `-p` | Preserve – keep permissions, ownership, timestamps |
| `*` (wildcard) | Copy multiple files matching a pattern (e.g., `*.txt`) |

### Examples

```bash
# Copy one file to another (overwrites destination if exists)
cp a.txt b.txt

# Copy multiple files into a directory
cp a.txt b.txt c.txt new/

# Copy directory recursively
cp -R geeksforgeeks/ gfg/

# Interactive mode (asks before overwrite)
cp -i a.txt b.txt

# Force overwrite (no prompt)
cp -f a.txt b.txt

# Preserve attributes (permissions, timestamps)
cp -p d.txt b.txt

# Copy all .txt files
cp *.txt new/
```

---

## 9. `mv` – Move or Rename

**Abbreviation:** move  
**Explanation:** Moves or renames files/directories. Does not create a copy – changes location or name.

### Syntax

```bash
mv [options] <source> <destination>
mv [options] <file1> <file2> ... <destination_directory>
```

### Common Options

| Option | Description |
|--------|-------------|
| `-i` | Interactive – prompt before overwriting |
| `-f` | Force – overwrite without prompt |
| `-n` | No-clobber – do not overwrite existing files |
| `-b` | Backup – create a backup (~ suffix) before overwriting |

### Examples

```bash
# Rename a file
mv jayesh_gfg geeksforgeeks

# Move a file to another directory
mv geeksforgeeks /home/jayeshkumar/jkj/

# Move multiple files to a directory
mv gfg_1 gfg_2 /home/jayeshkumar/jkj/

# Rename a directory
mv jkj new_gfg

# Interactive move (asks before overwrite)
mv -i jayesh_gfg geeksforgeeks

# Force move (overwrites without asking)
mv -f gfg geeksforgeeks

# No-clobber (don't overwrite existing)
mv -n oldfile newfile

# Backup existing file before overwriting
mv -b first_file second_file   # creates second_file~
```

---

## 10. `rm` – Remove Files and Directories

**Abbreviation:** remove  
**Explanation:** Permanently deletes files/directories. **No recycle bin – cannot recover.**

> ⚠️ **Warning:** Deleted files are gone forever. Use with caution.

### Common Options

| Option | Description |
|--------|-------------|
| `-i` | Interactive – prompt before each deletion |
| `-f` | Force – delete without confirmation (even write-protected) |
| `-r` or `-R` | Recursive – delete directories and all contents |
| `-v` | Verbose – show details of each deleted file |
| `-d` | Delete empty directories only |

### Examples

```bash
# Delete a single file
rm a.txt

# Delete multiple files
rm b.txt c.txt

# Interactive delete (asks for confirmation)
rm -i file.txt

# Force delete (no questions)
rm -f file.txt

# Delete directory and all contents recursively
rm -r foldername/

# Delete file that starts with a hyphen
rm -- -file.txt

# Dangerous: recursive force (be extremely careful)
rm -rf foldername/
```

### `rm` vs `rmdir`

| Feature | `rm` | `rmdir` |
|---------|------|---------|
| Purpose | Deletes files and directories | Deletes **only empty** directories |
| Recursive support | Yes (`-r`) | No |
| Force delete | Yes (`-f`) | Not applicable |
| Fails on non-empty | N/A (deletes anyway with `-r`) | Yes, fails with error |

---

## 11. File Type Indicators & Colors

### Standard Linux Color Codes (default terminal themes)

| Color | File Type | Related Commands |
|-------|-----------|------------------|
| **Blue** | Directories | `mkdir`, `cd` |
| **Cyan** | Symbolic links | `ln` |
| **Green** | Executable files | Running scripts/programs |
| **Red** | Archives / compressed | `tar`, `gzip`, `xz` |
| **Yellow** | Device files | Hardware-related |
| **Magenta** | Images / multimedia | Viewing graphics |
| **Bold White** | Regular text files | `cat`, `less`, `nano` |

### File Type Character (`ls -l`)

The first character of `ls -l` output indicates the file type:

| Character | Type | Description |
|-----------|------|-------------|
| `-` | Regular file | Text, image, script |
| `d` | Directory | Folder |
| `l` | Symbolic link | Shortcut |
| `b` | Block device | Hard drives (in `/dev`) |
| `c` | Character device | Terminals, keyboards |
| `p` | Named pipe | Process communication |
| `s` | Socket | Local network communication |

### Classification Symbols (`ls -F`)

Appends a symbol to filenames:

| Symbol | Meaning |
|--------|---------|
| `/` | Directory |
| `*` | Executable file |
| `@` | Symbolic link |
| `|` | FIFO (pipe) |
| `=` | Socket |

**Example output:** `myscript.sh*` or `backup_folder/`

### Hidden Files

Files or directories starting with a dot (`.bashrc`) are hidden.  
View them with `ls -a` (all).

### Permission Indicators (`rwx`)

Following the file type character, nine characters like `rwxr-xr-x`:

- `r` = read
- `w` = write
- `x` = execute (can run as a program)

---

## Key Takeaways for Cloud Engineering

- These commands are used **daily** when SSH into EC2 instances, debugging containers, or writing automation scripts.
- Understanding hard vs soft links helps with managing configuration files and log rotation.
- `cp -p` preserves timestamps – critical for backups.
- `rm -rf` is powerful and dangerous – always double-check the path.

---

## Practice Check

- [ ] I can create nested directories with a single command (`mkdir -p`)
- [ ] I can copy a directory and all its contents (`cp -r`)
- [ ] I can rename a file using `mv`
- [ ] I understand the difference between hard and soft links
- [ ] I can interpret `ls -l` output (file type, permissions, link count)
- [ ] I know the danger of `rm -rf` and how to use `-i` for safety

---

**Date documented:** 2026-04-13  
**Sources:** Linux Administration – File Operations, GeeksforGeeks, course notes

---
