# Chapter 14: Archiving and Transferring Files

## Table of Contents

- [Chapter 14: Archiving and Transferring Files](#chapter-14-archiving-and-transferring-files)
  - [Table of Contents](#table-of-contents)
  - [1. Archive vs. Compression – Concepts](#1-archive-vs-compression--concepts)
    - [What is an Archive?](#what-is-an-archive)
    - [What is Compression?](#what-is-compression)
    - [Archive vs. Compression – Key Differences](#archive-vs-compression--key-differences)
  - [2. Archiving with `tar`](#2-archiving-with-tar)
    - [Basic Syntax](#basic-syntax)
    - [Common `tar` Options (Detailed)](#common-tar-options-detailed)
    - [Examples](#examples)
  - [3. Compression Tools](#3-compression-tools)
    - [3.1 `gzip` (GNU zip)](#31-gzip-gnu-zip)
    - [3.2 `bzip2`](#32-bzip2)
    - [3.3 `xz`](#33-xz)
    - [3.4 Comparison Table](#34-comparison-table)
  - [4. Combining Archive and Compression – One‑Command Solution](#4-combining-archive-and-compression--onecommand-solution)
    - [4.1 Creating Compressed Archives](#41-creating-compressed-archives)
    - [4.2 Extracting Compressed Archives](#42-extracting-compressed-archives)
    - [4.3 Listing Contents Without Extracting](#43-listing-contents-without-extracting)
    - [4.4 Appending to an Archive](#44-appending-to-an-archive)
  - [5. Remote File Transfer](#5-remote-file-transfer)
    - [5.1 `scp` – Secure Copy](#51-scp--secure-copy)
    - [5.2 `sftp` – Secure File Transfer Protocol (Interactive)](#52-sftp--secure-file-transfer-protocol-interactive)
    - [5.3 `rsync` – Fast, Incremental Synchronisation](#53-rsync--fast-incremental-synchronisation)
    - [5.4 Comparison: `scp` vs. `rsync`](#54-comparison-scp-vs-rsync)
  - [6. Quick Reference Table](#6-quick-reference-table)
  - [7. Practice Lab – Verify Your Understanding](#7-practice-lab--verify-your-understanding)
  - [8. Real‑World Scenario – Backup and Transfer Workflow](#8-realworld-scenario--backup-and-transfer-workflow)
    - [Background](#background)
    - [Scenario Steps](#scenario-steps)
    - [Verification Checklist](#verification-checklist)

---

## 1. Archive vs. Compression – Concepts

### What is an Archive?

An **archive** is a single file that contains multiple files and directories, preserving their structure, metadata (timestamps, permissions, ownership), and relative paths. Archiving alone does **not** reduce file size.

**Analogy:** A filing cabinet folder that holds all documents of one student – grouped together but not compressed.

### What is Compression?

**Compression** reduces the size of data by encoding it more efficiently. It removes redundancy (e.g., in text, repeated patterns) and can be applied to individual files or archives.

**Analogy:** Stuffing the student’s folder into a vacuum bag – takes much less space.

### Archive vs. Compression – Key Differences

| Feature | Archiving | Compression |
|---------|-----------|-------------|
| Primary purpose | Combine many files into one | Reduce size |
| Size change | None | Significant reduction |
| Preserves metadata | Yes (permissions, timestamps) | Usually not (works on raw data) |
| Typical use | Backup, transfer preparation | Save storage, bandwidth |
| Tools | `tar`, `cpio`, `zip` | `gzip`, `bzip2`, `xz` |

> **Best practice:** Archive **first**, then compress. In Linux, `tar` can do both in one step.

---

## 2. Archiving with `tar`

`tar` (Tape ARchiver) is the standard archiving tool on Linux. It preserves permissions, ownership, and directory structure.

### Basic Syntax

```bash
tar [options] archive-name.tar [files/directories]
```

### Common `tar` Options (Detailed)

| Option | Long form | Meaning |
|--------|-----------|---------|
| `-c` | `--create` | Create a new archive |
| `-x` | `--extract` | Extract files from an archive |
| `-t` | `--list` | List contents of an archive (no extraction) |
| `-v` | `--verbose` | Verbose output (show files being processed) |
| `-f` | `--file` | Use archive file (must be last before filename) |
| `-p` | `--preserve-permissions` | Keep original permissions (useful for backups) |
| `-z` | `--gzip` | Filter archive through `gzip` (compression) |
| `-j` | `--bzip2` | Filter through `bzip2` |
| `-J` | `--xz` | Filter through `xz` |
| `-r` | `--append` | Append files to the end of an archive |
| `-u` | `--update` | Append files newer than those in archive |
| `-A` | `--catenate` | Concatenate two archives |
| `--delete` | – | Delete a file from an archive (not on all versions) |
| `--exclude` | – | Exclude files matching a pattern |
| `-C` | `--directory` | Change to directory before operation |

> **Note:** `tar` also accepts the **BSD style** with no dash for short options (e.g., `tar cvf` instead of `tar -cvf`). Both work.

### Examples

```bash
# Create an archive of a directory
tar -cvf backup.tar /home/user/docs

# Create verbose archive with multiple files
tar cvf project.tar file1.txt file2.txt folder1

# List contents without extracting
tar -tvf backup.tar

# Extract archive in current directory
tar -xvf backup.tar

# Extract to specific directory
tar -xvf backup.tar -C /target/path

# Extract only one file
tar -xvf backup.tar home/user/docs/important.txt

# Append a file to existing archive
tar -rvf backup.tar newfile.txt

# Preserve permissions (important for system backups)
tar -cvpf system-backup.tar /etc /var/log
```

---

## 3. Compression Tools

### 3.1 `gzip` (GNU zip)

**Explanation:** Fast compression, widely compatible. Best for general‑purpose use.

**Extension:** `.gz`

**Compress:** `gzip file` (replaces original with `file.gz`)  
**Decompress:** `gunzip file.gz` or `gzip -d file.gz`  
**Keep original:** `-k` (`gzip -k file` – not on all versions; use `gzip -c file > file.gz`)

**Common options:**

| Option | Meaning |
|--------|---------|
| `-d` | Decompress |
| `-c` | Write to stdout (preserves original) |
| `-v` | Verbose |
| `-1` to `-9` | Compression level (1 = fastest, 9 = smallest) |
| `-t` | Test integrity |

**Examples:**
```bash
gzip large.log                # creates large.log.gz, removes original
gunzip large.log.gz           # restores original
gzip -c document.txt > doc.gz # keep original
gzip -9 -v bigfile.txt        # maximum compression
```

### 3.2 `bzip2`

**Explanation:** Slower than `gzip` but provides better compression ratio, especially for text.

**Extension:** `.bz2`

**Compress:** `bzip2 file` (replaces original)  
**Decompress:** `bunzip2 file.bz2` or `bzip2 -d`

**Common options:**

| Option | Meaning |
|--------|---------|
| `-d` | Decompress |
| `-c` | Write to stdout |
| `-v` | Verbose |
| `-1` to `-9` | Block size (1 = 100k, 9 = 900k, higher = better compression) |
| `-t` | Test integrity |

**Examples:**
```bash
bzip2 backup.sql                  # backup.sql.bz2
bunzip2 backup.sql.bz2
bzip2 -9 -v data.tar
```

### 3.3 `xz`

**Explanation:** Highest compression ratio, but slowest. Ideal for long‑term archival.

**Extension:** `.xz`

**Compress:** `xz file` (replaces original)  
**Decompress:** `unxz file.xz` or `xz -d`

**Common options:**

| Option | Meaning |
|--------|---------|
| `-d` | Decompress |
| `-c` | Write to stdout |
| `-v` | Verbose |
| `-0` to `-9` | Compression presets (9 = extreme, very slow) |
| `-e` | Extreme (even slower, better compression) |
| `-T N` | Use N threads for compression (accelerates multi‑core) |
| `-t` | Test integrity |

**Examples:**
```bash
xz archive.tar                    # archive.tar.xz
unxz archive.tar.xz
xz -9e -T 4 bigdata.dat           # max compression, 4 threads
```

### 3.4 Comparison Table

| Feature | `gzip` | `bzip2` | `xz` |
|---------|--------|---------|------|
| Extension | `.gz` | `.bz2` | `.xz` |
| Compression speed | Fastest | Medium | Slowest |
| Decompression speed | Fast | Fast | Medium |
| Compression ratio | Low | Medium | **Highest** |
| Memory usage | Low | Medium | High (can be > 1GB at levels 9) |
| Multi‑thread support | No | No | Yes (`-T`) |
| Best for | Logs, quick backups, web assets | Moderate compression needs | Long‑term archival, distribution packages |
| Typical use with `tar` | `-z` | `-j` | `-J` |

---

## 4. Combining Archive and Compression – One‑Command Solution

Instead of two steps (`tar`, then compress), `tar` can directly produce compressed archives using the built‑in filters.

### 4.1 Creating Compressed Archives

| Compression | `tar` flags | Typical extension | Example |
|-------------|-------------|-------------------|---------|
| `gzip` | `-czf` | `.tar.gz` or `.tgz` | `tar -czf backup.tgz /home/user` |
| `bzip2` | `-cjf` | `.tar.bz2` or `.tbz2` | `tar -cjf backup.tbz2 /home/user` |
| `xz` | `-cJf` | `.tar.xz` or `.txz` | `tar -cJf backup.txz /home/user` |

**Preserve permissions:** Add `-p` flag, e.g., `tar -czpf backup.tgz /etc`.

**Recommendation:** Use `.tar.gz` for general transfers, `.tar.xz` for long‑term storage.

### 4.2 Extracting Compressed Archives

Replace `-c` (create) with `-x` (extract):

| Compression | Extract command |
|-------------|-----------------|
| `gzip` | `tar -xzf archive.tar.gz` |
| `bzip2` | `tar -xjf archive.tar.bz2` |
| `xz` | `tar -xJf archive.tar.xz` |

**To extract into a specific directory:** `tar -xzf archive.tgz -C /target/dir`

### 4.3 Listing Contents Without Extracting

Replace `-c` with `-t`:

```bash
tar -tzf archive.tar.gz      # list gzip archive
tar -tjf archive.tar.bz2     # list bzip2 archive
tar -tJf archive.tar.xz      # list xz archive
```

### 4.4 Appending to an Archive

`tar` supports appending **only to uncompressed archives** (or before compression). For compressed archives, you must extract, append, re‑compress.

```bash
# Append to an uncompressed .tar
tar -rvf existing.tar newfile.txt

# For compressed archives, do:
gunzip archive.tar.gz
tar -rvf archive.tar newfile.txt
gzip archive.tar
```

---

## 5. Remote File Transfer

### 5.1 `scp` – Secure Copy

**Explanation:** Copies files between hosts over SSH. Simple, widely available.

**Syntax:** `scp [options] source destination`

**Common options:**

| Option | Meaning |
|--------|---------|
| `-r` | Recursive (copy directories) |
| `-P port` | Specify remote SSH port |
| `-i key` | Use specific identity file (private key) |
| `-v` | Verbose (debug) |
| `-C` | Enable compression |
| `-p` | Preserve timestamps and permissions |
| `-q` | Quiet mode (no progress) |

**Examples:**
```bash
# Copy local file to remote server
scp file.txt user@192.168.1.100:/home/user/

# Copy remote file to local
scp user@192.168.1.100:/home/user/file.txt .

# Copy directory recursively
scp -r myfolder/ user@server:/backups/

# Copy with different port (2222) and identity key
scp -P 2222 -i ~/.ssh/mykey data.bin user@server:~
```

### 5.2 `sftp` – Secure File Transfer Protocol (Interactive)

**Explanation:** Interactive session to browse remote directories, upload/download, etc. Like an FTP client over SSH.

**Syntax:** `sftp [options] user@host`

**Common commands inside `sftp`:**

| Command | Meaning |
|---------|---------|
| `ls` | List remote files |
| `lls` | List local files |
| `cd` | Change remote directory |
| `lcd` | Change local directory |
| `get file` | Download file |
| `put file` | Upload file |
| `mget *` | Download multiple files |
| `mput *` | Upload multiple files |
| `rm file` | Delete remote file |
| `mkdir dir` | Create remote directory |
| `exit` or `quit` | Close session |

**Examples:**
```bash
sftp user@server
sftp> cd /var/log
sftp> get messages
sftp> put localfile.txt
sftp> ls -la
sftp> exit
```

**Non‑interactive `sftp` using batch file:**
```bash
sftp -b batchfile.txt user@server
```

### 5.3 `rsync` – Fast, Incremental Synchronisation

**Explanation:** Copies only the **differences** between source and destination, making it extremely efficient for repeated transfers. Works locally or over SSH.

**Syntax:** `rsync [options] source destination`

**Common options:**

| Option | Meaning |
|--------|---------|
| `-a` | Archive mode (preserve permissions, timestamps, recursion, etc.) – very common |
| `-v` | Verbose |
| `-z` | Compress during transfer |
| `-P` | Show progress and keep partial files |
| `-n` or `--dry-run` | Perform trial run without changes |
| `--delete` | Delete files in destination that don't exist in source |
| `-e ssh` | Use SSH as transport (default) |
| `-r` | Recursive (implied by `-a`) |
| `-H` | Preserve hard links |
| `-A` | Preserve ACLs |
| `-X` | Preserve extended attributes |
| `--exclude` | Exclude files/directories matching pattern |

**Examples:**

```bash
# Local sync
rsync -av /home/user/docs/ /backups/docs/

# Remote sync over SSH (push to server)
rsync -avz -e ssh /local/data/ user@server:/remote/data/

# Pull from server
rsync -avz user@server:/remote/data/ /local/backup/

# Dry run – see what would be copied
rsync -avn /source/ /dest/

# Sync with deletion (mirror)
rsync -av --delete /source/ /dest/

# Exclude certain files
rsync -av --exclude="*.tmp" --exclude="logs/" /home/user/ /backup/
```

**Trailing slash rule (critical):**
- `/source/` – copies the **contents** of `source` into destination.
- `/source` – copies the **directory itself** into destination.

### 5.4 Comparison: `scp` vs. `rsync`

| Feature | `scp` | `rsync` |
|---------|-------|---------|
| Incremental copy | No (copies all files every time) | Yes (only changed blocks) |
| Resume interrupted transfer | No | Yes (with `-P`) |
| Preserve metadata | With `-p` | Yes (`-a` preserves all) |
| Delete extra files | No | Yes (`--delete`) |
| Speed for large repeated transfers | Slower | Much faster |
| Availability | Everywhere (part of OpenSSH) | Usually installed, but not always |
| Suited for | One‑off transfers, scripts | Backups, synchronisation, mirroring |

> **Best practice:** Use `rsync` for repeated synchronisation (e.g., backups, mirroring). Use `scp` for simple one‑file transfers when `rsync` may not be available.

---

## 6. Quick Reference Table

| Task | Command |
|------|---------|
| Create uncompressed archive | `tar -cvf archive.tar files/` |
| Extract uncompressed archive | `tar -xvf archive.tar` |
| Create `tar.gz` | `tar -czvf archive.tgz files/` |
| Extract `tar.gz` | `tar -xzvf archive.tgz` |
| Create `tar.bz2` | `tar -cjvf archive.tbz2 files/` |
| Extract `tar.bz2` | `tar -xjvf archive.tbz2` |
| Create `tar.xz` | `tar -cJvf archive.txz files/` |
| Extract `tar.xz` | `tar -xJvf archive.txz` |
| List archive contents | `tar -tvf archive.tar` (add `z`/`j`/`J` for compressed) |
| Compress single file (`gzip`) | `gzip file` |
| Decompress `*.gz` | `gunzip file.gz` |
| Compress single file (`bzip2`) | `bzip2 file` |
| Decompress `*.bz2` | `bunzip2 file.bz2` |
| Compress single file (`xz`) | `xz file` |
| Decompress `*.xz` | `unxz file.xz` |
| `scp` local → remote | `scp file user@host:/path/` |
| `scp` remote → local | `scp user@host:/path/file .` |
| `scp` recursive | `scp -r folder/ user@host:/target/` |
| Interactive `sftp` | `sftp user@host` |
| `rsync` local | `rsync -av src/ dest/` |
| `rsync` remote (push) | `rsync -avz -e ssh local/ user@host:/remote/` |
| `rsync` remote (pull) | `rsync -avz user@host:/remote/ local/` |
| `rsync` dry run | `rsync -avn src/ dest/` |

---

## 7. Practice Lab – Verify Your Understanding

1. Create a directory `lab14` with three text files. Use `tar` to create an uncompressed archive.
2. Compress that archive using `gzip`, then `bzip2`, then `xz`. Compare the resulting file sizes (`ls -lh`). Which is smallest?
3. Extract the `tar.xz` version into a new directory.
4. Create a `tar.gz` of `/var/log` (use `sudo` to read log files). List the contents without extracting.
5. Use `scp` to copy a file to a remote VM (or localhost if you have SSH enabled). Then copy it back with a different name.
6. Start an `sftp` session to a remote host. Navigate, download a file, upload a file, then exit.
7. Use `rsync` to synchronise `lab14/` to `lab14_backup/`. Run it twice – note the second run should be very fast.
8. Experiment with `rsync --dry-run` and `rsync --delete` on a test directory.

---

## 8. Real‑World Scenario – Backup and Transfer Workflow

### Background

You are managing a production web server (`web01`, IP `192.168.1.100`) that hosts a PHP application. Your task is to prepare a weekly backup routine for the application code and upload the compressed backup to a central backup server (`backup01`). After transfer, you must extract and verify the backup on the backup server, and then synchronise the application directory with a staging copy on the same server to facilitate testing.

### Scenario Steps

**1. Create a dedicated backup directory on `web01`.**
   ```bash
   mkdir -p /tmp/backup_work
   ```

**2. Prepare a simulated application directory.**
   ```bash
   mkdir -p /tmp/app_site/{public,config,logs}
   echo "<?php echo 'hello';" > /tmp/app_site/public/index.php
   echo "DB_PASSWORD=secret" > /tmp/app_site/config/database.ini
   echo "Access log" > /tmp/app_site/logs/access.log
   ```

**3. Create a compressed archive of the application directory using `tar` with `gzip` (fast for transfer).**
   ```bash
   cd /tmp
   tar -czpf /tmp/backup_work/web01_app_$(date +%Y%m%d).tar.gz -C /tmp/app_site .
   ```
   - `-p` preserves permissions.
   - `-C` changes to the directory before archiving (so the archive contains the files directly, not the `app_site` folder itself).

**4. List the contents of the compressed archive to verify it includes all files.**
   ```bash
   tar -tzf /tmp/backup_work/web01_app_*.tar.gz
   ```

**5. Transfer the archive to the backup server using `scp` (one‑off secure copy).**
   ```bash
   scp /tmp/backup_work/web01_app_*.tar.gz admin@backup01:/backups/incoming/
   ```
   (The target directory `/backups/incoming/` must exist on `backup01`; you can create it with `mkdir -p` via SSH.)

**6. Log into `backup01` and extract the archive for verification.**
   ```bash
   ssh admin@backup01
   cd /backups/incoming
   mkdir extracted
   tar -xzf web01_app_*.tar.gz -C extracted
   ls -la extracted/            # Should show public/, config/, logs/
   ```

**7. Create a longer‑term archival copy using `xz` (highest compression).**
   ```bash
   # While on backup01, convert the gz archive to xz
   tar -xzf web01_app_*.tar.gz
   tar -cJf /backups/archive/web01_app_$(date +%Y%m%d).tar.xz *
   ```
   (Assume `/backups/archive/` is the long‑term storage directory.)

**8. Use `sftp` to download a specific configuration file from `web01` for inspection (interactive session).**
   ```bash
   sftp admin@web01
   sftp> cd /tmp/app_site/config
   sftp> get database.ini
   sftp> exit
   ```

**9. Synchronise the extracted backup with a staging directory using `rsync` (incremental).**
   ```bash
   rsync -av /backups/incoming/extracted/ /srv/staging/app/
   ```
   - The trailing slash on `extracted/` copies the contents.
   - `-a` preserves permissions, timestamps, and recursion.

**10. Perform a dry‑run with deletion on the staging directory to see what would be removed (if we wanted an exact mirror).**
   ```bash
   rsync -avn --delete /backups/incoming/extracted/ /srv/staging/app/
   ```

**11. Set up a daily cron job on `web01` that creates the compressed archive and uses `rsync` to push only changes to `backup01`.**
    Example cron entry:
    ```cron
    0 2 * * * tar -czpf /tmp/backup_work/web01_app_$(date +\%Y\%m\%d).tar.gz -C /var/www/app . && rsync -avz /tmp/backup_work/ admin@backup01:/backups/daily/
    ```

### Verification Checklist

- [ ] Archive created with `tar -czpf` and contains the correct files.
- [ ] Listing contents with `tar -tzf` shows all expected files.
- [ ] `scp` transfers the archive without errors.
- [ ] Extraction on the backup server preserves file structure.
- [ ] `sftp` retrieves a single file correctly.
- [ ] `rsync` synchronises directories incrementally; second run is fast.
- [ ] Dry‑run with `rsync -n` previews changes correctly.
- [ ] Cron job syntax is valid and covers the complete workflow.

---

**Date documented:** 2026-04-28  
**Sources:** Red Hat System Administration, `tar`/`gzip`/`bzip2`/`xz` man pages, `rsync` documentation