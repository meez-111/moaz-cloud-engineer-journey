# Chapter 5: Controlling Access to Files with ACLs – Complete Professional Guide

## Table of Contents

- [Chapter 5: Controlling Access to Files with ACLs – Complete Professional Guide](#chapter-5-controlling-access-to-files-with-acls--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Refresh: Basic and Special Permissions](#1-refresh-basic-and-special-permissions)
    - [1.1 Standard Unix Permissions (rwx)](#11-standard-unix-permissions-rwx)
    - [1.2 Special Permissions](#12-special-permissions)
  - [2. What is ACL? Why Do We Need It?](#2-what-is-acl-why-do-we-need-it)
    - [2.1 Limitations of Standard Permissions](#21-limitations-of-standard-permissions)
    - [2.2 How ACL Solves the Problem](#22-how-acl-solves-the-problem)
  - [3. ACL Mask – The Effective Permission Ceiling](#3-acl-mask--the-effective-permission-ceiling)
    - [3.1 What is the Mask?](#31-what-is-the-mask)
    - [3.2 Mask Examples and Behaviour](#32-mask-examples-and-behaviour)
  - [4. Default ACLs – Inheritance for New Files/Directories](#4-default-acls--inheritance-for-new-filesdirectories)
    - [4.1 Setting Default ACLs on Directories](#41-setting-default-acls-on-directories)
    - [4.2 How Default ACLs Propagate](#42-how-default-acls-propagate)
  - [5. Identifying ACLs – The `+` Sign in `ls -l`](#5-identifying-acls--the--sign-in-ls--l)
  - [6. ACL Commands – `setfacl` and `getfacl`](#6-acl-commands--setfacl-and-getfacl)
    - [6.1 `getfacl` – Display ACLs](#61-getfacl--display-acls)
    - [6.2 `setfacl` – Set or Modify ACLs](#62-setfacl--set-or-modify-acls)
    - [6.3 Removing ACL Entries](#63-removing-acl-entries)
    - [6.4 Copying ACLs from One File to Another](#64-copying-acls-from-one-file-to-another)
  - [7. Practical Examples: Real‑World ACL Usage Scenarios](#7-practical-examples-realworld-acl-usage-scenarios)
    - [Scenario 1: Shared Project Directory with Multiple Collaborators](#scenario-1-shared-project-directory-with-multiple-collaborators)
    - [Scenario 2: Default ACL for Shared Directory for Web Development](#scenario-2-default-acl-for-shared-directory-for-web-development)
    - [Scenario 3: Temporarily Restrict Access for All Named Users (Using Mask)](#scenario-3-temporarily-restrict-access-for-all-named-users-using-mask)
    - [Scenario 4: Copying ACLs from Template to Many Files](#scenario-4-copying-acls-from-template-to-many-files)
    - [Scenario 5: Recursively Remove a User’s ACL from a Subtree](#scenario-5-recursively-remove-a-users-acl-from-a-subtree)
  - [8. Important Notes and Best Practices](#8-important-notes-and-best-practices)
  - [9. Quick Reference Table](#9-quick-reference-table)
  - [10. Real‑World Scenario – Managing a Shared Development Directory](#10-realworld-scenario--managing-a-shared-development-directory)
    - [Background](#background)
    - [Step 1 – Create the base directory and verify current permissions](#step-1--create-the-base-directory-and-verify-current-permissions)
    - [Step 2 – Add access ACLs for the team](#step-2--add-access-acls-for-the-team)
    - [Step 3 – Set default ACLs so new files inherit the same rules](#step-3--set-default-acls-so-new-files-inherit-the-same-rules)
    - [Step 4 – Test inheritance by creating a new file and subdirectory](#step-4--test-inheritance-by-creating-a-new-file-and-subdirectory)
    - [Step 5 – Temporarily freeze writes using the mask (maintenance window)](#step-5--temporarily-freeze-writes-using-the-mask-maintenance-window)
    - [Step 6 – Remove a departing user (dan) from all files recursively](#step-6--remove-a-departing-user-dan-from-all-files-recursively)
    - [Step 7 – Document and backup/restore ACLs for disaster recovery](#step-7--document-and-backuprestore-acls-for-disaster-recovery)
    - [Verification Checklist](#verification-checklist)
  - [11. Practice Lab – Verify Your Understanding](#11-practice-lab--verify-your-understanding)

---

## 1. Refresh: Basic and Special Permissions

### 1.1 Standard Unix Permissions (rwx)

Three permission classes:
- **User (u)** – owner of the file.
- **Group (g)** – group owning the file.
- **Others (o)** – everyone else.

Three permission types:
- **read (r)** – view content; for directories, list contents.
- **write (w)** – modify, delete; for directories, create/remove files.
- **execute (x)** – run as program; for directories, traverse (`cd`).

**Numeric representation:** `r=4, w=2, x=1` → sum for each class.

**Example:** `chmod 750 file` → owner: rwx (7), group: r-x (5), others: --- (0).

### 1.2 Special Permissions

| Bit | Symbolic | Numeric | Effect |
|-----|----------|---------|--------|
| **SUID** | `u+s` | `4` | When executable: runs with owner’s privileges, not the user’s. |
| **SGID** | `g+s` | `2` | On file: runs with group’s privileges. On directory: new files inherit group of parent. |
| **Sticky** | `o+t` | `1` | On directory: only file owner can delete/rename files inside. |

**Example:** `/tmp` has sticky bit (`drwxrwxrwt`).  
**Set SUID:** `chmod 4755 /bin/su` (rarely used manually now).

---

## 2. What is ACL? Why Do We Need It?

### 2.1 Limitations of Standard Permissions

Standard Unix permissions only allow **one owner**, **one group**, and **others**. What if you need:

- User `alice` to have read access, user `bob` to have read+write, user `carol` to have no access?
- A shared directory where users from three different groups each need different permissions?
- A service account (e.g., `apache`) to read a file owned by `root:root` without changing group ownership?

**Without ACLs**, you would be forced to:
- Create a new group and add all relevant users (inflexible, messy).
- Use `sudo` wrappers or setuid scripts (security risk).

### 2.2 How ACL Solves the Problem

**Access Control Lists (ACLs)** extend the standard Unix permission model by allowing you to grant permissions to:
- **Individual users** (by UID or username)
- **Individual groups** (by GID or group name)
- **Multiple named users/groups** on the same file

ACLs are stored as additional entries in the file’s extended attributes. The `ls -l` output shows a `+` sign when ACLs are present.

**Example:** After setting ACLs:
```bash
-rw-rwxr--+ 1 root root 1024 May 6 17:00 secret.txt
```

The `+` indicates extended ACL entries.

---

## 3. ACL Mask – The Effective Permission Ceiling

### 3.1 What is the Mask?

The **mask** is a special ACL entry that limits the maximum permissions granted to **all named users** (not the owner, not others) and **named groups**, as well as the owning group.

In other words, the effective permissions for any named user or group are the **intersection (AND)** of the ACL entry’s permissions and the mask.

- The mask does **not** affect the file owner, the `other` entry, or `default` ACLs.
- The mask is automatically recalculated when you modify permissions (unless you use `-n` or `setfacl -m mask:...`).

**View mask:** `getfacl` shows a line like `mask::r-x`.

### 3.2 Mask Examples and Behaviour

**Example 1 – Mask restricts named user’s permissions**

```bash
# Start: File with default mask (rw)
$ touch test.txt
$ setfacl -m u:alice:rwx test.txt
$ getfacl test.txt
# file: test.txt
user::rw-
user:alice:rwx
group::r--
mask::rwx          # mask automatically set to union of all group entries + named entries
other::r--

# Now set mask to r-x (removing write)
$ setfacl -m mask:r-x test.txt
$ getfacl test.txt | grep alice
user:alice:rwx     # entry still has rwx
# but effective permissions = rwx & r-x = r-x
```

When you try to access (e.g., write) as `alice`, write will be denied because mask lacks `w`.

**Example 2 – Named group limited by mask**

```bash
$ setfacl -m g:developers:rwx test.txt
$ setfacl -m mask:r-- test.txt
# effective permissions for group developers = r-- (read only)
```

**Why mask exists?** It provides a single point to lower permissions for all named entries without deleting them. For example, to temporarily make a file read‑only for all named users/groups, you can just change the mask to `r--`.

---

## 4. Default ACLs – Inheritance for New Files/Directories

### 4.1 Setting Default ACLs on Directories

A **default ACL** is applied to a **directory**. When new files or subdirectories are created inside that directory, they inherit the default ACL as their **initial access ACL**.

- Default ACL entries are stored with the `default:` prefix in `getfacl` output.
- Only directories can have default ACLs.
- If a directory has a default ACL, new files/directories will have permissions based on the combination of:
  - The creating process’s umask (but **masked** by default ACL)
  - For directories, the default ACL becomes the new directory’s default ACL (inherited).

**Set default ACL:**
```bash
setfacl -m d:u:alice:rwx /shared/project
```
The `d:` prefix means default.

### 4.2 How Default ACLs Propagate

**Example:**

```bash
$ mkdir /data/share
$ setfacl -m d:u:alice:rwx /data/share
$ setfacl -m d:o::--- /data/share   # others no access by default
$ getfacl /data/share
# file: data/share
# owner: root
# group: root
user::rwx
group::r-x
other::r-x
default:user::rwx
default:user:alice:rwx
default:group::r-x
default:mask::rwx
default:other::---

$ touch /data/share/newfile.txt
$ getfacl /data/share/newfile.txt
# file: newfile.txt
# owner: root
# group: root
user::rw-                   # inherited from default:user::rwx, but file creation umask removed execute
user:alice:rwx              # inherited
group::r-x                  # inherited
mask::rwx                   # effective mask
other::---                  # inherited from default:other::---
```

- The new file **does not** get the default ACL itself (only directories can have default ACLs), but its access ACL entry set.
- For a new subdirectory, the inheritance includes the default ACL entries as its own default ACL.

---

## 5. Identifying ACLs – The `+` Sign in `ls -l`

When a file or directory has any ACL entry (including mask or default entries), the `ls -l` permission string ends with a `+` sign.

```bash
$ ls -l /data/share
drwxr-x---+ 2 root root 4096 May 6 17:00 share
-rw-rwxr--+ 1 root root    0 May 6 17:01 newfile.txt
```

The `+` is a quick indicator, but to see actual ACL entries, you must use `getfacl`.

---

## 6. ACL Commands – `setfacl` and `getfacl`

### 6.1 `getfacl` – Display ACLs

**Syntax:** `getfacl [OPTION]... FILE...`

**Common options:**

| Option | Meaning |
|--------|---------|
| (none) | Show ACL for file/directory, including default entries if present. |
| `-a` | Show only access ACL (no default entries). |
| `-d` | Show only default ACL. |
| `-R` | Recursive (list ACLs for all files/subdirs). |
| `-L` | Follow symlinks (when used with `-R`). |
| `-P` | Do not follow symlinks (default). |
| `-e` | Show effective permissions (mask applied). |
| `-t` | Tabular output (show in table format). |
| `-n` | Do not resolve numeric UIDs/GIDs (show numbers). |

**Examples:**

```bash
# Basic display
getfacl file.txt

# Show only access ACL
getfacl -a file.txt

# Show only default ACL of a directory
getfacl -d /shared/

# Recursive (all files under directory)
getfacl -R /data/project

# With effective permissions
getfacl -e file.txt
```

### 6.2 `setfacl` – Set or Modify ACLs

**Syntax:** `setfacl [OPTION]... [ACL_ENTRY]... FILE...`

**ACL entry format:**

| Type | Format | Example |
|------|--------|---------|
| User (named) | `u:username:perms` | `u:alice:rwx` |
| User (owner) | `u::perms` | `u::rw-` |
| Group (named) | `g:groupname:perms` | `g:developers:rx` |
| Group (owning) | `g::perms` | `g::r-x` |
| Others | `o::perms` | `o::r--` |
| Mask | `mask:perms` | `mask::rwx` |
| Default entry | `d:` prefix (as above) | `d:u:alice:rwx` |
| Remove entry | `d:` with no permissions? Use `-x` | see section 6.3 |

**Common options:**

| Option | Meaning |
|--------|---------|
| `-m` | Modify/add ACL entries (main operation). |
| `-x` | Remove specific ACL entries (but not default entries). |
| `-b` | Remove all ACL entries (leave basic Unix permissions). |
| `-k` | Remove default ACL entries (only for directories). |
| `-R` | Recursive (apply to all files/subdirs). |
| `-d` | Operate on default ACL (instead of access ACL). |
| `-n` | Do not recalculate mask automatically (use as is). |
| `-M file` | Read ACL entries from a file (one per line). |
| `-X file` | Read entries to remove from a file. |
| `--set` | Replace whole ACL with new entries (remove all existing). |
| `--restore` | Restore ACLs from a `getfacl` output. |

**Examples – Adding/Modifying:**

```bash
# Give user alice read+write on file
setfacl -m u:alice:rw file.txt

# Give group developers read+execute on directory (and recursively)
setfacl -R -m g:developers:rx /data/dev

# Set mask to r-x explicitly (no automatic recalc)
setfacl -n -m mask:r-x file.txt

# Set default ACL for new files in a directory
setfacl -m d:u:alice:rwx,d:mask:rwx /shared

# Add multiple entries at once (space separated)
setfacl -m u:alice:r,u:bob:rw,g:admins:r file
```

**Examples – Replacing whole ACL (`--set`):**

```bash
# Reset ACL to: owner rwx, group r-x, others ---, plus user alice:r
setfacl --set u::rwx,g::r-x,o::---,u:alice:r file
```

**Examples – Recursive operations:**

```bash
# Recursively give user alice read access to all files under /data
setfacl -R -m u:alice:r /data

# Recursively remove user alice’s ACL entries from all files
setfacl -R -x u:alice /data
```

### 6.3 Removing ACL Entries

- **Remove a specific named user entry:**
  ```bash
  setfacl -x u:alice file.txt
  ```
- **Remove a named group entry:**
  ```bash
  setfacl -x g:developers file.txt
  ```
- **Remove all ACL entries (restore to basic Unix permissions):**
  ```bash
  setfacl -b file.txt
  ```
- **Remove default ACL from directory:**
  ```bash
  setfacl -k /shared
  ```
- **Remove mask entry?** You cannot remove mask; it is always present. You can set it to desired value.

### 6.4 Copying ACLs from One File to Another

```bash
# Copy ACL from source to target
getfacl source.txt | setfacl --set-file=- target.txt
```

The `-` tells `setfacl` to read from stdin.

---

## 7. Practical Examples: Real‑World ACL Usage Scenarios

### Scenario 1: Shared Project Directory with Multiple Collaborators

**Requirements:**
/`data/project` owned by `root:projectteam`. User `alice` needs `rwx`, user `bob` needs `rx`, user `carol` needs `rw`, group `interns` needs `r` only. Others no access.

```bash
mkdir /data/project
setfacl -m u:alice:rwx,u:bob:rx,u:carol:rw,g:interns:r /data/project
setfacl -m mask::rwx /data/project
# Verify
getfacl /data/project
```

### Scenario 2: Default ACL for Shared Directory for Web Development

**Requirements:** All new files created in `/var/www/mysite` should be readable by user `apache` (web server) and writable by user `alice`. Others no access.

```bash
sudo mkdir -p /var/www/mysite
sudo setfacl -m u:alice:rwx,u:apache:rx /var/www/mysite
sudo setfacl -m mask::rwx /var/www/mysite
sudo setfacl -m d:u:alice:rwx,d:u:apache:rx,d:mask:rwx /var/www/mysite
```

Now any file created inside will automatically grant those permissions.

### Scenario 3: Temporarily Restrict Access for All Named Users (Using Mask)

Given a file with many named ACL entries, you want to make it read‑only for all those users without removing entries.

```bash
setfacl -m mask:r-- myfile.txt
# Later, re‑allow writes
setfacl -m mask:rwx myfile.txt
```

### Scenario 4: Copying ACLs from Template to Many Files

```bash
getfacl template.txt > acl_template
setfacl --restore=acl_template   # restores for files listed inside
```

But for many files, you may need to use a loop.

### Scenario 5: Recursively Remove a User’s ACL from a Subtree

```bash
setfacl -R -x u:departed /home/departed_data
```

---

## 8. Important Notes and Best Practices

- **ACLs only work on file systems mounted with `acl` option.** Most modern Linux systems (ext4, xfs, btrfs) enable ACLs by default. Check with `tune2fs -l /dev/sda1 | grep "Default mount options"`.
- **`cp` and `mv` behaviour:** `cp` by default does not preserve ACLs unless `--preserve=all` or `-a` (archive). `mv` preserves ACLs because it moves the inode.
- **`tar` and `rsync`:** Use `--acls` with `rsync` (since version 3.0.0) or `tar --acls` to preserve ACLs in archives.
- **Performance:** ACLs add a small overhead (extra extended attribute lookups). For millions of small files, avoid excessive ACL entries.
- **Security:** Do not confuse mask with permissions for owner/others. Mask only affects named entries and owning group.

---

## 9. Quick Reference Table

| Task | Command |
|------|---------|
| Show ACLs | `getfacl file` |
| Add user entry | `setfacl -m u:username:rwx file` |
| Add group entry | `setfacl -m g:groupname:rx file` |
| Remove user entry | `setfacl -x u:username file` |
| Remove group entry | `setfacl -x g:groupname file` |
| Remove all ACLs | `setfacl -b file` |
| Set mask | `setfacl -m mask:r-x file` |
| Set default ACL on directory | `setfacl -m d:u:username:rwx dir` |
| Remove default ACL | `setfacl -k dir` |
| Recursively add ACL | `setfacl -R -m u:username:r dir` |
| Copy ACLs | `getfacl source \| setfacl --set-file=- target` |
| Check if ACLs enabled on FS | `mount \| grep acl` |

---

## 10. Real‑World Scenario – Managing a Shared Development Directory

### Background

Your team maintains a web application stored in `/srv/webapp`. The directory and existing files are owned by `root:devteam`. Because team members have varying roles, standard Unix permissions are insufficient. You need fine‑grained control:

- Full control: user `alice` (lead developer)
- Read/write: user `bob` and user `carol` (developers)
- Read‑only: user `dan` (intern) and group `qa` (testers)
- Others: no access

Additionally, any new file or subdirectory created inside `/srv/webapp` must automatically inherit these rules, so you don’t have to set ACLs again.

### Step 1 – Create the base directory and verify current permissions

```bash
sudo mkdir -p /srv/webapp
sudo chown root:devteam /srv/webapp
sudo chmod 770 /srv/webapp
ls -ld /srv/webapp
# output: drwxrwx--- 2 root devteam 4096 ...
```

### Step 2 – Add access ACLs for the team

```bash
sudo setfacl -m u:alice:rwx,u:bob:rwx,u:carol:rwx,u:dan:r-x,g:qa:r-x /srv/webapp
sudo setfacl -m mask::rwx /srv/webapp
sudo setfacl -m o::--- /srv/webapp
```

Verify with `getfacl /srv/webapp`:
```
# file: srv/webapp
# owner: root
# group: devteam
user::rwx
user:alice:rwx
user:bob:rwx
user:carol:rwx
user:dan:r-x
group::rwx
group:qa:r-x
mask::rwx
other::---
```

### Step 3 – Set default ACLs so new files inherit the same rules

```bash
sudo setfacl -m d:u:alice:rwx,d:u:bob:rwx,d:u:carol:rwx,d:u:dan:r-x,d:g:qa:r-x,d:mask:rwx,d:o::--- /srv/webapp
```

Now `getfacl /srv/webapp` also shows `default:` entries.

### Step 4 – Test inheritance by creating a new file and subdirectory

```bash
sudo touch /srv/webapp/index.html
sudo mkdir /srv/webapp/subdir
ls -l /srv/webapp
# The index.html and subdir should show a '+' sign
getfacl /srv/webapp/index.html
```

The new file has the ACL entries from the default ACL (minus execute for files due to umask).

### Step 5 – Temporarily freeze writes using the mask (maintenance window)

Before a production deployment, you want to make all developers (except the owner) read‑only.

```bash
sudo setfacl -m mask:r-x /srv/webapp   # removes write everywhere
```

Now `alice`, `bob`, `carol` can read but not write. After deployment, restore mask:

```bash
sudo setfacl -m mask:rwx /srv/webapp
```

### Step 6 – Remove a departing user (dan) from all files recursively

```bash
sudo setfacl -R -x u:dan /srv/webapp
```

Check that `dan` no longer appears in `getfacl` for any file.

### Step 7 – Document and backup/restore ACLs for disaster recovery

Dump ACLs to a file:

```bash
getfacl -R /srv/webapp > /backup/webapp_acl.txt
```

If the directory must be recreated, restore ACLs later:

```bash
setfacl --restore=/backup/webapp_acl.txt
```

### Verification Checklist

- [ ] `ls -l /srv/webapp` shows a `+` sign.
- [ ] `getfacl /srv/webapp` shows all users and groups with correct permissions.
- [ ] New files automatically inherit the named entries.
- [ ] Mask change immediately read‑only for all named users.
- [ ] `dan` removed recursively, no leftover entries.
- [ ] ACL backup file exists and can be restored.

---

## 11. Practice Lab – Verify Your Understanding

1. **Basic ACL:** Create a file `acl_test.txt` with standard permissions `644`. Add an ACL entry giving user `nobody` (or another non‑owner user) `rw` access. Verify with `getfacl` and by switching to that user (e.g., `sudo -u nobody cat acl_test.txt`).

2. **Mask effect:** Set mask to `r--` and then attempt to write as the named user (should fail). Then set mask back to `rwx` and verify write works.

3. **Default ACL:** Create a directory `shared` and set a default ACL so that all new files are readable by a group `wheel` and writable by user `alice`. Create a file inside and verify its ACL.

4. **Recursive operation:** Recursively give read access to user `alice` for all files under `/tmp/testtree` (create a small tree of files first).

5. **Removal:** Remove the ACL entry for `alice` and then remove all ACLs from the file/directory.

6. **Backup/restore:** Dump ACLs of a directory tree using `getfacl -R` and restore them to another location.

---

**Date documented:** 2026-05-06  
**Sources:** Red Hat System Administration, `acl(5)` man page, `setfacl`/`getfacl` documentation