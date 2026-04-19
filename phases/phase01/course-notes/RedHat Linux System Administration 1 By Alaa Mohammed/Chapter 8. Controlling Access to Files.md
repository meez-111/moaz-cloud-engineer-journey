

# Controlling Access to Files – Permissions, Special Bits, Umask & ACLs

## 1. What Are Permissions?

**Definition:** Permissions define **who** can access **what** and **what they can do** (read, write, execute).

Permissions apply to:
- **Files** (regular files, scripts, binaries)
- **Directories** (folders)

---

## 2. Types of Permissions

| Permission | Effect on File | Effect on Directory |
|------------|----------------|---------------------|
| **Read (r)** | View file content (`cat`, `less`, `vi`, `head`, `tail`) | List directory contents (`ls`) |
| **Write (w)** | Edit, delete, rename, copy over (`vi`, `cp`, `mv`, `rm`, `ln`) | Create, rename, delete files/subdirs (`touch`, `mkdir`, `rm`, `mv`) |
| **Execute (x)** | Run as a program/script | Enter (`cd`) into the directory |

---

## 3. Who Gets Permissions (Ownership Classes)

| Class | Symbol | Description |
|-------|--------|-------------|
| **User / Owner** | `u` | The user who owns the file |
| **Group** | `g` | Users in the file’s group |
| **Others** | `o` | Everyone else (not owner, not in group) |
| **All** | `a` | `u` + `g` + `o` combined |

---

## 4. Viewing Permissions (`ls -l`)

**Command:** `ls -l filename`

**Example output:**
```
-rw-rw-r-- 1 root root 68524 2026-04-12 07:18 file
```

**Anatomy:**

```
-  rw-  rw-  r--  1  root  root  68524 2026-04-12 07:18  file
│  │    │    │    │   │     │      │       │          │
│  │    │    │    │   │     │      │       │          └─ filename
│  │    │    │    │   │     │      │       └─ date/time
│  │    │    │    │   │     │      └─ size (bytes)
│  │    │    │    │   │     └─ group owner
│  │    │    │    │   └─ user owner
│  │    │    │    └─ link count
│  │    │    └─ others permissions (r-- = read only)
│  │    └─ group permissions (rw- = read+write)
│  └─ owner permissions (rw- = read+write)
└─ file type (- = regular file, d = directory, l = link, b = block device, etc.)
```

### Common File Types

| Symbol | Type |
|--------|------|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `b` | Block device (e.g., hard disk) |
| `c` | Character device (e.g., terminal) |
| `p` | Named pipe |
| `s` | Socket |

**Check file type:** `file filename`

4.1 Changing File Ownership – chown and chgrp
Permissions are tied to who owns the file. Use these commands to change ownership:

Command	Purpose	Example
chown user file	Change file owner	sudo chown alice report.txt
chown user:group file	Change owner and group	sudo chown alice:developers report.txt
chgrp group file	Change group only	sudo chgrp www-data uploads/
chown -R user:group dir/	Recursively change ownership	sudo chown -R alice:devs /home/project
Note: Only root can change file ownership. Group changes require the user to be a member of the target group (unless you are root).


4.2 Viewing Detailed Metadata with stat
The stat command displays comprehensive file information, including permissions in both symbolic and numeric formats.

Example:
stat script.sh

Sample output:
File: script.sh
Size: 128 Blocks: 8 IO Block: 4096 regular file
Device: 801h/2049d Inode: 1234567 Links: 1
Access: (0755/-rwxr-xr-x) Uid: (1000/ alice) Gid: (1000/ alice)
Access: 2026-04-19 10:30:00.000000000 +0000
Modify: 2026-04-19 10:15:00.000000000 +0000
Change: 2026-04-19 10:15:00.000000000 +0000

The line "Access: (0755/-rwxr-xr-x)" shows numeric (0755) and symbolic (-rwxr-xr-x) permissions at a glance.

Tip: Use "stat -c "%a %n" *" to output only numeric permissions for all files in a directory.



---

## 5. Changing Permissions – `chmod`

### 5.1 Numeric (Absolute) Mode

Each permission is assigned a number:

| Permission | Value |
|------------|-------|
| Read (r)   | 4     |
| Write (w)  | 2     |
| Execute (x)| 1     |

**Add values for combinations:**

| Permission string | Numeric |
|-------------------|---------|
| `rwx` | 4+2+1 = 7 |
| `rw-` | 4+2 = 6 |
| `r-x` | 4+1 = 5 |
| `r--` | 4 |
| `-wx` | 2+1 = 3 |
| `-w-` | 2 |
| `--x` | 1 |
| `---` | 0 |

**Syntax:** `chmod XYZ filename`
- X = owner permissions
- Y = group permissions
- Z = others permissions

**Example:** `chmod 754 file`
- Owner: 7 = `rwx`
- Group: 5 = `r-x`
- Others: 4 = `r--`

Result: `-rwxr-xr--`

### 5.2 Symbolic Mode

**Syntax:** `chmod [class][operator][permission] file`

**Operators:**
- `+` : Add permission
- `-` : Remove permission
- `=` : Set exact permission (override)

**Examples:**

| Command | Effect |
|---------|--------|
| `chmod u+x file` | Give owner execute |
| `chmod g-w file` | Remove group write |
| `chmod o=r file` | Set others to read-only |
| `chmod ugo+rwx file` | Give all full perms (same as `chmod a+rwx`) |
| `chmod a+x file` | Give execute to all |
| `chmod u+x, g+r, o-x file` | Combine multiple |

---

## 6. Special Permissions (SUID, SGID, Sticky Bit)

These are extra bits that modify execution behavior.

| Special Bit | Symbol | Numeric Value | Applies to | Effect |
|-------------|--------|---------------|------------|--------|
| **SUID** (Set User ID) | `u+s` | 4 (prepend) | **Executable files only** | Runs with **owner's** privileges, not the user who runs it (e.g., `passwd` runs as root). |
| **SGID** (Set Group ID) | `g+s` | 2 (prepend) | **Directories** (and sometimes files) | New files/dirs created inside inherit the **group ownership** of the parent directory. |
| **Sticky Bit** | `o+t` | 1 (prepend) | **Directories** | Only **owner** (or root) can delete/rename files inside, even if others have write permission (e.g., `/tmp`). |

### Numeric Special Permissions

**Syntax:** `chmod [special][owner][group][others] file`

**Example:** `chmod 4755 file`
- 4 = SUID
- 7 = `rwx` for owner
- 5 = `r-x` for group
- 5 = `r-x` for others

**Common combinations:**

| Command | Numeric | Meaning |
|---------|---------|---------|
| `chmod 4755 file` | 4+755 | SUID + `rwxr-xr-x` |
| `chmod 2755 dir` | 2+755 | SGID on directory |
| `chmod 1777 dir` | 1+777 | Sticky bit + full perms (like `/tmp`) |

### Display of Special Bits in `ls -l`

| If x is present | If x is absent |
|----------------|----------------|
| `rws` (SUID) | `rwS` (capital S) |
| `rws` (SGID on file) | `rwS` |
| `rwt` (Sticky + x) | `rwT` |

**Note:** Capital `S` or `T` means the execute bit is **missing** – the special bit is set but useless.

**Only file owner or root can set SUID/SGID bits.**

---

## 7. Default Permissions – `umask`

When a new file or directory is created, it gets default permissions based on the **umask** (user file-creation mode mask).

### Base Values

| Type | Base Permission |
|------|----------------|
| **File** | `666` (`rw-rw-rw-`) |
| **Directory** | `777` (`rwxrwxrwx`) |

**Formula:**  
`Actual permission = Base - umask` (subtract bits)

**Default umask on most Linux systems:** `0022` (often written as `022`)

### How umask 022 works

| Type | Base | umask | Result | Permission |
|------|------|-------|--------|------------|
| File | 666 | 022 | 644 | `rw-r--r--` |
| Directory | 777 | 022 | 755 | `rwxr-xr-x` |

### View current umask

```bash
umask
# Output: 0022
```

### Change umask

#### Temporary (current shell session only)

```bash
umask 0077
```

Now new files will be `600` (`rw-------`) and directories `700` (`rwx------`).

#### Permanent

- **For current user only:** Add `umask 0077` to `~/.bashrc` (or `~/.profile`).
- **System-wide (all users):** Edit `/etc/profile` or `/etc/bashrc` (requires root).

---

## 8. Access Control Lists (ACLs)

ACLs allow **granular** permissions for **specific users or groups** beyond the standard `u/g/o` model.

### When to use ACLs

- You need to give **one extra user** read/write access without changing group membership.
- You want a **directory** to automatically give certain permissions to a specific user for all new files.

### Key Commands

| Command | Purpose |
|---------|---------|
| `getfacl file` | View ACL entries |
| `setfacl -m "u:username:perms" file` | Add/modify ACL for a user |
| `setfacl -m "g:groupname:perms" file` | Add/modify ACL for a group |
| `setfacl -x "u:username" file` | Remove ACL entry for a user |
| `setfacl -b file` | Remove all ACL entries |
| `setfacl -dm "u:username:perms" dir` | Set **default** ACL on directory (new files inherit) |

### Permission strings for ACLs

Use `rwx` letters (e.g., `r-x`, `rw-`, `rwx`).

### Examples

#### Give user `alice` read+execute access to a file

```bash
setfacl -m "u:alice:r-x" /data/config.ini
```

#### Give group `developers` write access to a directory

```bash
setfacl -m "g:developers:rwx" /shared/project
```

#### Make all new files in `/shared` automatically readable by `alice`

```bash
setfacl -dm "u:alice:r-x" /shared
```

#### Remove ACL for user `bob`

```bash
setfacl -x "u:bob" /data/secret.txt
```

#### Remove all ACLs from a file

```bash
setfacl -b /data/secret.txt
```

### Detecting ACLs

When a file or directory has ACL entries, `ls -l` shows a **`+`** sign at the end of the permission string:

```
-rw-rwxr--+ 1 root root 1024 Apr 18 10:00 file_with_acl
```

### Viewing ACLs

```bash
getfacl /shared/project
```

**Example output:**
```
# file: shared/project
# owner: root
# group: root
user::rwx
user:alice:r-x
group::r-x
mask::r-x
other::---
```

### Important Notes

- ACLs **work alongside** standard Unix permissions. The standard perms still apply.
- When both standard perms and ACLs exist, the **effective** permission is the union (most permissive) subject to the mask.
- Use `setfacl -m "mask:perms"` to limit maximum effective permissions.


8.1 Understanding the ACL Mask
The mask is a special ACL entry that limits the maximum permissions that can be granted to named users (except the file owner) and group members. It does not affect the file owner or "others" permissions.

Example: Mask Restricting Access

Suppose you give user bob full rwx via ACL, but the mask is set to r-x.

setfacl -m u:bob:rwx project/
setfacl -m mask::r-x project/

Now getfacl project/ shows:

file: project/
owner: alice
group: devs
user::rwx
user:bob:rwx # effective: r-x
group::r-x
mask::r-x
other::---

Notice the comment "# effective: r-x" next to Bob's entry. Even though Bob was granted rwx, the mask reduces his effective rights to r-x. He cannot write or delete files in this directory.

Why This Matters

The mask ensures that ACLs do not accidentally grant more access than intended, especially when copying files between systems or when default ACLs are set broadly.

You can adjust the mask with "setfacl -m mask::perms file".

Viewing Effective Permissions

getfacl automatically calculates and displays effective rights. Use it to verify what a user can actually do.


---

## 9. Real-World Examples (Putting It All Together)

### Example 1: Make a script executable only by owner

```bash
chmod 700 script.sh
# or
chmod u=rwx,go= script.sh
```

### Example 2: Give group read access to a file, others none

```bash
chmod 640 secret.doc
```

### Example 3: Create a shared directory where all new files belong to the same group

```bash
mkdir /shared
sudo groupadd team
sudo chown :team /shared
sudo chmod 2770 /shared   # SGID + rwx for owner and group
```

Now any file created inside `/shared` will have group `team`.

### Example 4: Protect `/tmp` style directory – everyone can create, only owner deletes

```bash
mkdir /project_temp
chmod 1777 /project_temp
```

### Example 5: Give `apache` user read access to a file without changing its group

```bash
setfacl -m "u:apache:r--" /etc/custom.conf
```

### Example 6: Remove all special permissions from a file

```bash
chmod 755 file          # numeric removes SUID/SGID/sticky
# or
chmod u-s,g-s,o-t file
```

---

## 10. Quick Reference Table

| Task | Command |
|------|---------|
| View permissions | `ls -l file` |
| Change perms (numeric) | `chmod 644 file` |
| Change perms (symbolic) | `chmod u+x,g-w,o=r file` |
| Set SUID | `chmod u+s file` |
| Set SGID on directory | `chmod g+s dir` |
| Set sticky bit | `chmod o+t dir` |
| View umask | `umask` |
| Set umask (temp) | `umask 027` |
| View ACLs | `getfacl file` |
| Grant user access via ACL | `setfacl -m "u:name:rwx" file` |
| Grant group access via ACL | `setfacl -m "g:name:rx" file` |
| Remove ACL entry | `setfacl -x "u:name" file` |
| Remove all ACLs | `setfacl -b file` |
| Set default ACL on dir | `setfacl -dm "u:name:rwx" dir` |


10.1 Searching for Files by Permission with find
Auditing file permissions across a system is a critical security practice. The find command can locate files with specific permission bits.

Task	Command
Find all SUID files	find / -perm -4000 -type f 2>/dev/null
Find all SGID files	find / -perm -2000 -type f 2>/dev/null
Find world-writable files	find / -perm -o+w -type f 2>/dev/null
Find files with exact permissions 777	find / -perm 777 -type f
Find directories without sticky bit (but world-writable)	find / -type d -perm -o+w ! -perm -o+t 2>/dev/null
How -perm works:
-perm mode : exact match
-perm -mode : all of these bits are set
-perm /mode : any of these bits are set

Example: Find all files in /home that are group-writable:
find /home -type f -perm -g+w

---

## 11. Common Mistakes & Pitfalls

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Forgetting that directories need `x` to `cd` into | Users can't enter directory | `chmod a+x dir` |
| Using `chmod 777` on sensitive files | Anyone can read/write | Use `750` or `640` |
| Setting SUID on a script | SUID is ignored on scripts (security) | Use only on compiled binaries |
| Forgetting `-a` with `usermod -G` | User loses all other groups | Use `-aG` |
| Setting sticky bit without execute (`T`) | Useless | Ensure directory has `x` for others (`chmod o+xt`) |
| Editing `/etc/sudoers` directly | Syntax error breaks sudo | Always use `visudo` |

---

## 12. Practice Lab – Verify Your Understanding

1. Create a file `test.txt` and set permissions so that owner can read/write, group can read, others nothing.
2. Create a directory `shared` and set SGID so new files inherit group ownership.
3. Give user `alice` (create if needed) read access to `test.txt` using ACL.
4. Change umask temporarily to `027` and create a new file – check its permissions.
5. Set sticky bit on `/tmp/mytest` (create first) and verify with `ls -ld`.



---

## 13. Complete Practical Mastery Test – Permissions, Special Bits, Umask & ACLs

This test simulates real‑world file permission management tasks covering **every section** of this chapter. Perform each task on a Linux VM or container with `sudo` access. Verify your work using the provided verification commands. **Attempt all tasks before looking at the answer key.**

> **Prerequisite:** Create a working directory for this test: `mkdir ~/permission_lab && cd ~/permission_lab`

---

### Part 1: Permission Inspection and Interpretation

**Task 1.1 – Decode `ls -l` Output**

Given this output from `ls -l`:
```
-rwxr-x--- 1 alice developers 4096 Apr 19 10:30 script.sh
```
Answer:
1. What are the permissions for the owner?
2. What can members of the `developers` group do with this file?
3. What can "others" do?
4. Who owns the file? What is the group?

**Task 1.2 – Determine File Type**

Run `ls -l /dev/sda` (if it exists) or `/dev/null`. What does the first character of the permission string indicate? What type of file is it?

**Task 1.3 – Explain Missing Execute on Directory**

A directory has permissions `drw-r--r--`. Can the owner `cd` into it? Why or why not?

---

### Part 2: Changing Permissions – `chmod` Numeric and Symbolic

**Task 2.1 – Create Test Files**
```bash
touch file1.txt file2.txt script.sh
echo "echo Hello" > script.sh
```

**Task 2.2 – Set Permissions Using Numeric Mode**
Set the following permissions using numeric `chmod`:
- `file1.txt`: Owner can read/write, group can read, others no access.
- `script.sh`: Owner can read/write/execute, group and others can read/execute.

**Task 2.3 – Set Permissions Using Symbolic Mode**
Starting from default permissions (likely `664` for files), use symbolic mode to:
- Add execute permission for the owner on `file2.txt`.
- Remove write permission for group on `file2.txt`.
- Set others permissions to read‑only on `file2.txt`.

**Task 2.4 – Combine Multiple Changes in One Command**
Use a single symbolic `chmod` command to:
- Give owner execute on `file1.txt`
- Remove write from group on `file1.txt`
- Set others to no permissions on `file1.txt`

---

### Part 3: Special Permissions – SUID, SGID, Sticky Bit

**Task 3.1 – Set SUID on a Binary (Simulated)**
Create a copy of `/bin/ls` in your lab directory:
```bash
cp /bin/ls ./myls
```
Set the SUID bit on `myls`. Verify with `ls -l` that the owner's execute field shows `s`.

**Task 3.2 – Set SGID on a Directory**
Create a directory named `team_shared`. Set SGID on it and change its group to a group you are a member of (e.g., your primary group). Verify that new files created inside inherit that group.

**Task 3.3 – Set Sticky Bit on a World‑Writable Directory**
Create a directory `public_temp`. Make it world‑writable (`777`) and set the sticky bit. Verify with `ls -ld` that the others execute field shows `t`.

**Task 3.4 – Interpret Capital `S` and `T`**
Create a file `weird` and set SUID without execute (`chmod 4644 weird`). What does `ls -l` show for the owner permission field? Why is it capital `S`?

---

### Part 4: Default Permissions – `umask`

**Task 4.1 – View Current umask**
Run `umask`. What is the current umask value? What would be the default permissions for a new file and directory created under this umask?

**Task 4.2 – Temporarily Change umask and Test**
Set umask to `0077`. Create a new file `secret.txt` and a directory `private_dir`. Verify their permissions with `ls -l` and `ls -ld`. Are they what you expected?

**Task 4.3 – Reset umask**
Reset umask to your original value (or `022` if unsure). Create another file `normal.txt` to confirm permissions return to `644`.

**Task 4.4 – Explain umask Subtraction**
Given a umask of `027`, what permissions will a new directory have? Show the calculation.

---

### Part 5: Access Control Lists (ACLs)

**Task 5.1 – Install ACL Package (if needed)**
On some minimal installations, ACL tools may not be installed. Install `acl` if `setfacl` is not found:
```bash
sudo apt install acl        # Debian/Ubuntu
sudo yum install acl        # RHEL/CentOS
```

**Task 5.2 – Grant a Specific User Access via ACL**
Create a file `report.txt` with content "Confidential". Grant user `nobody` (or any existing non‑owner user) read and write access using ACL. Verify with `getfacl`.

**Task 5.3 – Grant a Group Access via ACL**
Create a directory `project_docs`. Grant group `adm` (or any existing group) read and execute access using ACL. Check that the `+` sign appears in `ls -ld`.

**Task 5.4 – Set Default ACL for Inheritance**
On the `project_docs` directory, set a default ACL so that user `nobody` automatically gets read permission on any new file created inside. Test by creating a new file and checking its ACL.

**Task 5.5 – Remove an ACL Entry**
Remove the ACL entry for user `nobody` from `report.txt`. Verify it is gone.

**Task 5.6 – Remove All ACLs**
Remove all extended ACL entries from `report.txt` and `project_docs`. Confirm with `ls -l` that the `+` sign disappears.

---

### Part 6: Real‑World Scenarios – Putting It All Together

**Scenario 1: Secure Web Application Directory**

You have a directory `/var/www/project` owned by `root` and group `www-data`. Requirements:
- The web server (running as `www-data`) must be able to read and traverse the directory and all files inside.
- A developer `alice` (create if necessary) needs full read/write/execute access to the directory and new files.
- New files created inside should automatically be owned by group `www-data` and be readable/writable by both `alice` and `www-data`.
- Other users should have no access.

**Task 6.1 – Execute the Setup**
Create the directory structure, set ownership, set SGID, set standard permissions, and use ACLs as needed to fulfill the requirements.

**Scenario 2: Shared Team Directory with Restricted Deletion**

Create a directory `/shared/team` with the following:
- All members of group `engineers` can create and modify files.
- Users can only delete files they themselves own (prevent accidental deletion of others' work).
- New files should inherit the group `engineers`.

**Task 6.2 – Execute the Setup**
Create the group `engineers`, create two test users in that group, create the directory with appropriate permissions, special bits, and verify the behavior.

**Scenario 3: System‑Wide Temporary Directory Hardening**

The system's `/tmp` directory already has sticky bit set (`1777`). Verify its permissions and explain how it prevents one user from deleting another user's files.

**Task 6.3 – Verify `/tmp` Permissions**
Run `ls -ld /tmp` and interpret the output. Create a file as your user in `/tmp`, then switch to another user (or use `sudo -u nobody`) and attempt to delete it. What happens?

---

### Part 7: Cleanup

**Task 7.1 – Remove Test Users and Groups**
Delete any test users (`alice`, `bob`, etc.) and groups (`engineers`) created during the test.

**Task 7.2 – Remove Test Directories and Files**
Delete the `~/permission_lab` directory and any directories created under `/var/www/project` or `/shared/team` (if you used those paths).

**Task 7.3 – Restore Original umask**
Ensure your umask is reset to the system default (usually `022`).

---

## 14. Self‑Evaluation Checklist

| I can... | Done |
|----------|------|
| Interpret `ls -l` output and identify file types | ☐ |
| Explain the difference between read, write, and execute on files vs directories | ☐ |
| Use numeric `chmod` to set precise permissions | ☐ |
| Use symbolic `chmod` to modify permissions incrementally | ☐ |
| Set and identify SUID, SGID, and sticky bits in `ls -l` output | ☐ |
| Understand the implications of capital `S` and `T` | ☐ |
| Calculate default permissions given a umask value | ☐ |
| Temporarily and permanently change umask | ☐ |
| Use `getfacl` and `setfacl` to manage ACLs for specific users/groups | ☐ |
| Set default ACLs for inheritance | ☐ |
| Remove individual and all ACL entries | ☐ |
| Design a shared directory with proper SGID and sticky bit for collaborative work | ☐ |
| Secure a web directory using both standard permissions and ACLs | ☐ |
| Troubleshoot permission issues using `ls`, `stat`, and `getfacl` | ☐ |

---

## 15. Practical Test Answer Key


### Part 1 Answers

**1.1**
1. Owner: read, write, execute (`rwx`).
2. Group (`developers`): read and execute (`r-x`).
3. Others: no permissions (`---`).
4. Owner: `alice`, Group: `developers`.

**1.2**
First character `b` indicates block device (for `/dev/sda`); `c` for character device (like `/dev/null`). The file type is a device file.

**1.3**
No. Directories require execute (`x`) permission to be accessed with `cd`. Read (`r`) only allows listing contents.

### Part 2 Commands

```bash
# 2.2
chmod 640 file1.txt
chmod 755 script.sh

# 2.3
chmod u+x,g-w,o=r file2.txt

# 2.4
chmod u+x,g-w,o= file1.txt
```

### Part 3 Commands

```bash
# 3.1
cp /bin/ls ./myls
chmod u+s myls
ls -l myls   # should show -rwsr-xr-x

# 3.2
mkdir team_shared
chgrp $(id -gn) team_shared   # use your primary group
chmod g+s team_shared
touch team_shared/testfile
ls -l team_shared/testfile    # group ownership should match team_shared

# 3.3
mkdir public_temp
chmod 1777 public_temp
ls -ld public_temp   # drwxrwxrwt

# 3.4
touch weird
chmod 4644 weird
ls -l weird   # shows -rwSr--r--  (capital S because execute missing)
```

### Part 4 Commands

```bash
# 4.1
umask   # e.g., 0022 → files 644, dirs 755

# 4.2
umask 0077
touch secret.txt
mkdir private_dir
ls -l secret.txt       # -rw-------
ls -ld private_dir     # drwx------

# 4.3
umask 0022
touch normal.txt       # should be -rw-r--r--

# 4.4
# Base for directory: 777 - 027 = 750 → rwxr-x---
```

### Part 5 Commands

```bash
# 5.2
echo "Confidential" > report.txt
sudo setfacl -m u:nobody:rw- report.txt
getfacl report.txt

# 5.3
mkdir project_docs
sudo setfacl -m g:adm:r-x project_docs
ls -ld project_docs   # shows '+'

# 5.4
sudo setfacl -dm u:nobody:r-- project_docs
touch project_docs/newfile
getfacl project_docs/newfile   # should show user:nobody:r--

# 5.5
sudo setfacl -x u:nobody report.txt

# 5.6
sudo setfacl -b report.txt
sudo setfacl -b project_docs
```

### Part 6 Scenarios

**Scenario 1 (Web Directory):**
```bash
sudo mkdir -p /var/www/project
sudo chown root:www-data /var/www/project
sudo chmod 2770 /var/www/project                # SGID + rwx for owner/group
sudo setfacl -m u:alice:rwx /var/www/project
sudo setfacl -dm u:alice:rwx /var/www/project   # default for new files
sudo setfacl -dm g:www-data:rwx /var/www/project
```

**Scenario 2 (Team Directory):**
```bash
sudo groupadd engineers
sudo useradd -m -G engineers alice
sudo useradd -m -G engineers bob
sudo mkdir -p /shared/team
sudo chgrp engineers /shared/team
sudo chmod 3770 /shared/team   # sticky bit + SGID + rwx for owner/group
# Verify: alice creates file, bob cannot delete it.
```

**Scenario 3 (`/tmp`):**
```bash
ls -ld /tmp   # drwxrwxrwt
touch /tmp/mytest-$$
sudo -u nobody rm /tmp/mytest-$$   # "Operation not permitted"
```

### Part 7 Cleanup

```bash
sudo userdel -r alice bob   # if created
sudo groupdel engineers
rm -rf ~/permission_lab
sudo rm -rf /var/www/project /shared/team
umask 0022
```


---

**Date documented:** 2026-04-18  
**Sources:** Linux Administration, GeeksforGeeks, Red Hat documentation

---
