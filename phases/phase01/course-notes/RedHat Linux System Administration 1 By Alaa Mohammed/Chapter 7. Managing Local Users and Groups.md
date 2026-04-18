

# Managing Local Users and Groups

## 1. Types of Users in Linux

| User Type | UID Range | Description |
|-----------|-----------|-------------|
| **Root (Superuser)** | `0` | Full system control. Can install software, modify config files, delete anything. |
| **System Users** | `1 – 199` | Used by the OS for system services (e.g., `systemd`, `kernel`). No login shell typically. |
| **Service / Application Users** | `200 – 999` | Non‑human accounts for daemons and services (e.g., `mysql`, `nginx`, `apache`). |
| **Normal (Regular) Users** | `1000+` | Human users with limited privileges. Each has a home directory under `/home/`. |

> **Note:** The maximum UID limit is typically `60000`, but modern systems allow up to `2³²-2`. The ranges above follow RHEL/CentOS conventions.

---

## 2. Types of Groups

| Group Type | Description |
|------------|-------------|
| **Primary Group** | Assigned to a user when the account is created. By default, the group has the same name as the user. Each user has exactly **one** primary group. Files created by the user inherit this group. |
| **Secondary (Supplementary) Group** | Created manually to grant additional permissions. A user can belong to **multiple** secondary groups. Used for team‑based access (e.g., `docker`, `wheel`, `developers`). |

---

## 3. Operations You Can Apply to Users and Groups

| Operation | User Commands | Group Commands |
|-----------|---------------|----------------|
| **Create** | `useradd` | `groupadd` |
| **Modify** | `usermod`, `passwd`, `chage` | `groupmod`, `gpasswd` |
| **Delete** | `userdel` | `groupdel` |
| **Set permissions / ownership** | `chown`, `chmod` (files) | `chgrp` |
| **Privilege escalation** | `sudo`, `visudo` | – |

---

## 4. Key User & Group Files

| File | Purpose | Permissions (typical) |
|------|---------|----------------------|
| `/etc/passwd` | Basic user account info (username, UID, GID, home, shell) | `644` (world‑readable) |
| `/etc/shadow` | Encrypted passwords + password aging policies | `600` or `640` (root + shadow group) |
| `/etc/group` | Group definitions and members | `644` |
| `/etc/gshadow` | Secure group info (encrypted group passwords, admins) | `600` |
| `/etc/login.defs` | Default settings for user creation (UID ranges, password policies) | `644` |
| `/etc/skel/` | Template files copied to new user’s home directory (e.g., `.bashrc`, `.profile`) | `755` |
| `/var/log/auth.log` (Debian/Ubuntu) or `/var/log/secure` (RHEL) | Authentication logs (logins, sudo, lockouts) | `640` |
| `/etc/sudoers` | Rules for `sudo` access (edit with `visudo`) | `440` |

---

## 5. Anatomy of `/etc/passwd` (7 fields)

```
username:password:UID:GID:comment:home_directory:shell
```

| Field | Example | Meaning |
|-------|---------|---------|
| `username` | `alice` | Login name |
| `password` | `x` | Placeholder – actual hash is in `/etc/shadow` |
| `UID` | `1001` | User ID |
| `GID` | `1001` | Primary Group ID |
| `comment` | `Alice Johnson` | GECOS field (full name, office, phone) |
| `home_directory` | `/home/alice` | User’s home directory |
| `shell` | `/bin/bash` | Login shell (e.g., `/bin/bash`, `/bin/sh`, `/sbin/nologin`) |

---

## 6. Anatomy of `/etc/shadow` (9 fields)

```
username:encrypted_password:last_change:min:max:warn:inactive:expire:reserved
```

| Field | Meaning |
|-------|---------|
| `username` | Login name (matches `/etc/passwd`) |
| `encrypted_password` | Hash in `$type$salt$hash` format. `!` or `*` means locked; `!!` means no password set. |
| `last_change` | Days since 1970‑01‑01 of last password change |
| `min` | Minimum days before password can be changed again (`0` = anytime) |
| `max` | Maximum days before password must be changed (`99999` = never) |
| `warn` | Warning days before expiry |
| `inactive` | Days after expiry before account is disabled |
| `expire` | Absolute expiry date (days since 1970‑01‑01) |
| `reserved` | Unused field |

> **View human‑readable aging info:** `sudo chage -l username`

---

## 7. User Management Commands

### 7.1 `useradd` – Create a New User

**Syntax:** `useradd [options] username`

| Option | Description | Example |
|--------|-------------|---------|
| `-d /path` | Set custom home directory | `useradd -d /data/john john` |
| `-u UID` | Set specific user ID | `useradd -u 1500 jane` |
| `-g GID` | Set **primary** group (by GID or name) | `useradd -g developers alice` |
| `-G group1,group2` | Set **secondary** groups | `useradd -G wheel,docker bob` |
| `-M` | Do **not** create home directory | `useradd -M service_user` |
| `-m` | Force create home directory (default on many systems) | `useradd -m charlie` |
| `-e YYYY-MM-DD` | Account expiry date | `useradd -e 2026-12-31 temp_user` |
| `-c "comment"` | Add GECOS comment | `useradd -c "John Doe, IT" jdoe` |
| `-s /bin/shell` | Set login shell | `useradd -s /bin/zsh alice` |
| `-r` | Create a system user (UID < 1000) | `useradd -r mydaemon` |

**Files modified by `useradd`:**
- `/etc/passwd` – adds user entry
- `/etc/shadow` – adds password placeholder (`!!`)
- `/etc/group` – adds group with same name (unless `-g` or `-N`)
- `/etc/gshadow` – secure group info
- `/home/username` – home directory (if created) populated from `/etc/skel`

> **`adduser` vs `useradd`:**  
> - `adduser` (Debian/Ubuntu) – interactive, user‑friendly  
> - `useradd` (RHEL/CentOS/Fedora) – low‑level, good for scripting

---

### 7.2 `usermod` – Modify Existing User

**Syntax:** `usermod [options] username`

| Option | Description | Example |
|--------|-------------|---------|
| `-c "new comment"` | Change GECOS comment | `usermod -c "Jane Smith" jsmith` |
| `-d /new/home` | Change home directory | `usermod -d /home/jane_new jane` |
| `-m` | Move home directory contents to new location (use with `-d`) | `usermod -d /home/jane_new -m jane` |
| `-u NEWUID` | Change user ID | `usermod -u 2000 jane` |
| `-g GROUP` | Change **primary** group | `usermod -g developers alice` |
| `-G group1,group2` | Set **secondary** groups (replaces existing) | `usermod -G wheel,docker bob` |
| `-aG group` | **Append** to secondary groups (preserve existing) | `usermod -aG docker bob` |
| `-l new_login` | Change login name | `usermod -l jane_doe jane` |
| `-e YYYY-MM-DD` | Change expiry date | `usermod -e 2027-01-01 temp_user` |
| `-L` | Lock account (adds `!` to password hash) | `usermod -L bob` |
| `-U` | Unlock account | `usermod -U bob` |
| `-s /bin/shell` | Change login shell | `usermod -s /bin/bash alice` |

---

### 7.3 `userdel` – Delete a User

**Syntax:** `userdel [options] username`

| Option | Description |
|--------|-------------|
| (no option) | Removes user from `/etc/passwd` and `/etc/shadow`; home directory remains |
| `-r` | Remove user **and** home directory + mail spool |
| `-f` | Force delete even if user is logged in |

**Example:**
```bash
sudo userdel -r olduser   # deletes user and /home/olduser
```

---

### 7.4 `passwd` – Manage Passwords

| Command | Description |
|---------|-------------|
| `passwd` | Change your own password |
| `sudo passwd username` | Change another user’s password (root only) |
| `sudo passwd -l username` | Lock account (adds `!` to shadow) |
| `sudo passwd -u username` | Unlock account |
| `sudo passwd -e username` | Expire password (force change on next login) |
| `sudo passwd -S username` | Show account status (locked, last change, etc.) |
| `sudo passwd -n 7 username` | Minimum 7 days between password changes |
| `sudo passwd -x 90 username` | Password valid for max 90 days |
| `sudo passwd -w 7 username` | Warn 7 days before expiry |

---

### 7.5 `chage` – Change Password Aging (human‑friendly)

| Command | Description |
|---------|-------------|
| `sudo chage -l username` | List aging information |
| `sudo chage -d 0 username` | Force password change at next login |
| `sudo chage -M 90 username` | Set max days to 90 |
| `sudo chage -E 2026-12-31 username` | Set account expiry date |

---

### 7.6 Other Useful Commands

| Command | Description |
|---------|-------------|
| `id username` | Show UID, GID, and group memberships |
| `groups username` | List groups the user belongs to |
| `who` | Show who is logged in |
| `last` | Show last logins (reads `/var/log/wtmp`) |
| `lastb` | Show failed login attempts (reads `/var/log/btmp`) |
| `awk -F: '{ print $1}' /etc/passwd` | List all users |

---

## 8. Group Management Commands

### 8.1 `groupadd` – Create a Group

**Syntax:** `groupadd [options] groupname`

| Option | Description |
|--------|-------------|
| `-g GID` | Specify group ID |
| `-r` | Create system group (GID < 1000) |

**Example:**
```bash
sudo groupadd developers
sudo groupadd -g 3000 accounting
```

---

### 8.2 `groupmod` – Modify Group

| Option | Description | Example |
|--------|-------------|---------|
| `-n new_name` | Rename group | `sudo groupmod -n devs developers` |
| `-g newGID` | Change group ID | `sudo groupmod -g 2500 devs` |

---

### 8.3 `groupdel` – Delete Group

**Syntax:** `sudo groupdel groupname`

> **Note:** Cannot delete a group if it is the **primary group** of any existing user. Remove or reassign those users first.

---

### 8.4 Adding/Removing Users to/from Groups

| Method | Command | Effect |
|--------|---------|--------|
| **Append user to secondary group** (preserve others) | `sudo usermod -aG groupname username` | Recommended |
| **Replace all secondary groups** | `sudo usermod -G group1,group2 username` | Use with caution |
| **Add multiple users to a group** (replace members) | `sudo gpasswd -M user1,user2,user3 groupname` | No spaces after commas |
| **Remove a user from a group** | `sudo gpasswd -d username groupname` | Keeps user in other groups |
| **Set group password** (rare) | `sudo gpasswd groupname` | Stores in `/etc/gshadow` |

---

### 8.5 `gpasswd` – Advanced Group Management

**Syntax:** `gpasswd [options] group`

| Option | Description |
|--------|-------------|
| `-a username` | Add user to group |
| `-d username` | Remove user from group |
| `-M user1,user2,...` | Set exact member list (replaces) |
| `-A admin1,admin2,...` | Set group administrators |
| `-r` | Remove group password |
| `-R` | Restrict group access (only members can use `newgrp`) |

**Example:**
```bash
sudo gpasswd -a alice developers        # add alice
sudo gpasswd -d bob developers          # remove bob
sudo gpasswd -M alice,charlie,david devs  # set members
```

---

## 9. Special Group: `wheel` (or `sudo` on Debian)

On RHEL/CentOS/Fedora, users in the `wheel` group can run `sudo` (depending on `/etc/sudoers` configuration).

**To grant sudo access:**
```bash
sudo usermod -aG wheel username
```

On Debian/Ubuntu, the group is `sudo`:
```bash
sudo usermod -aG sudo username
```

---

## 10. Viewing and Troubleshooting

### Check a user’s groups
```bash
groups alice
id alice
```

### Find all members of a group
```bash
getent group developers
```

### Lock/Unlock account
```bash
sudo usermod -L username   # lock
sudo usermod -U username   # unlock
# or using passwd
sudo passwd -l username    # lock
sudo passwd -u username    # unlock
```

### Force password change on next login
```bash
sudo passwd -e username
# or
sudo chage -d 0 username
```

### Check authentication logs
```bash
# Debian/Ubuntu
sudo tail -f /var/log/auth.log

# RHEL/CentOS/Fedora
sudo tail -f /var/log/secure

# systemd systems
sudo journalctl -u sshd -f
```


---

## 11. The `wheel` Group (RHEL/CentOS/Fedora) and `sudo` Group (Debian/Ubuntu)

### What is `wheel`?

On Red Hat‑based systems, the `wheel` group is a special administrative group. Users in `wheel` can execute commands as `root` using `sudo` (if configured in `/etc/sudoers`).

**Check if `wheel` exists:**
```bash
getent group wheel
```

**Add a user to `wheel`:**
```bash
sudo usermod -aG wheel alice
```

**Verify:**
```bash
id alice
# Output should show: groups=... ,wheel
```

### Debian/Ubuntu equivalent – `sudo` group

On Debian/Ubuntu, the group is named `sudo`:
```bash
sudo usermod -aG sudo bob
```

### Why use `wheel`/`sudo` instead of logging in as root?

| Reason | Explanation |
|--------|-------------|
| **Auditing** | Every `sudo` command is logged (who, what, when). |
| **Least privilege** | Users get only the permissions they need. |
| **Accountability** | Commands are traceable to individual users. |
| **Security** | Root login can be disabled entirely (`PermitRootLogin no` in `/etc/ssh/sshd_config`). |

---

## 12. `/etc/sudoers` – Deep Dive

The `/etc/sudoers` file controls who can run what commands with `sudo`. **Never edit this file directly** – always use `visudo`, which checks syntax before saving.

### 12.1 Using `visudo`

```bash
sudo visudo
```

**What `visudo` does:**
- Locks the file to prevent concurrent edits.
- Performs syntax validation.
- If an error is found, it asks how to proceed (save anyway? re-edit? abort?).

### 12.2 Basic `/etc/sudoers` Syntax

```
user/group    host=(run_as_user)    command
```

| Field | Meaning | Example |
|-------|---------|---------|
| `user/group` | Username or `%groupname` | `alice`, `%wheel` |
| `host` | Usually `ALL` (all hosts) | `ALL` |
| `(run_as_user)` | User to run as – `(root)` or `(ALL)` | `(root)` or `(ALL:ALL)` |
| `command` | Full path to command (or `ALL`) | `/bin/systemctl restart nginx` |

### 12.3 Common Examples – Add these to your notes as reference

#### Example 1: Allow a user to run any command as root
```
alice    ALL=(root)    ALL
```

#### Example 2: Allow a group (`wheel`) to run any command as root
```
%wheel   ALL=(root)    ALL
```

#### Example 3: Allow a user to run specific commands without a password
```
bob      ALL=(root)    NOPASSWD: /bin/systemctl restart nginx, /bin/systemctl reload nginx
```

#### Example 4: Allow a user to run any command but require password (default)
```
charlie  ALL=(root)    ALL
```

#### Example 5: Allow a user to run commands as any user (not just root)
```
david    ALL=(ALL)     ALL
```

#### Example 6: Allow a group to run only systemctl for specific services
```
%webadmins    ALL=(root)    /bin/systemctl restart nginx, /bin/systemctl reload nginx, /bin/systemctl status nginx
```

#### Example 7: Deny a specific command while allowing others
```
alice    ALL=(root)    ALL, !/usr/bin/passwd root, !/bin/su -
```
> This allows all commands except changing root's password or switching to root via `su`.

#### Example 8: Allow a user to run commands without a password for a specific script
```
deploy   ALL=(root)    NOPASSWD: /usr/local/bin/deploy.sh
```

### 12.4 Important `sudoers` Aliases (for cleaner config)

```
User_Alias     WEBADMINS = alice, bob, charlie
Cmnd_Alias     WEB_CMDS = /bin/systemctl restart nginx, /bin/systemctl reload nginx
Runas_Alias    WEB_RUNAS = www-data, root

WEBADMINS   ALL=(WEB_RUNAS)   WEB_CMDS
```

### 12.5 Verify `sudo` access for a user

```bash
sudo -l -U alice
```

This lists what commands `alice` is allowed to run.

### 12.6 Common `sudo` troubleshooting

| Problem | Check |
|---------|-------|
| User not in `sudoers` | `groups username` – are they in `wheel` or `sudo`? |
| Syntax error in `/etc/sudoers` | Run `sudo visudo -c` to check syntax |
| Command path wrong | Use `which nginx` to find full path |
| `sudo` still asks for password | Look for `NOPASSWD:` in the rule |
| User is in group but can't run | Ensure group line has `%` prefix (`%wheel` not `wheel`) |

### 12.7 Default `sudo` behavior (no `NOPASSWD`)

When `NOPASSWD` is **not** specified, `sudo` asks for the **user's own password** (not root's password). The password is cached for 5 minutes by default (configurable with `timestamp_timeout` in `/etc/sudoers`).

---

## 13. `/etc/login.defs` – Default User Creation Settings

This file controls default values for `useradd` and password aging policies. It is **read by `useradd`**, not a database itself.

### 13.1 Important Parameters in `/etc/login.defs`

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| `PASS_MAX_DAYS` | Maximum days a password is valid | `90` |
| `PASS_MIN_DAYS` | Minimum days between password changes | `7` |
| `PASS_WARN_AGE` | Days before expiry to show warning | `7` |
| `UID_MIN` | Minimum UID for normal users | `1000` |
| `UID_MAX` | Maximum UID for normal users | `60000` |
| `GID_MIN` | Minimum GID for normal groups | `1000` |
| `GID_MAX` | Maximum GID for normal groups | `60000` |
| `CREATE_HOME` | Create home directory by default? | `yes` |
| `UMASK` | Default file creation mask (for user's home) | `077` (private) or `022` |
| `USERGROUPS_ENAB` | Delete user's private group when last user removed? | `yes` |
| `ENCRYPT_METHOD` | Hashing algorithm for passwords | `SHA512` or `YESCRYPT` |
| `MAIL_DIR` | Location of user mail spool | `/var/spool/mail` |

### 13.2 View current settings

```bash
grep -E "^(PASS|UID|GID|CREATE_HOME|UMASK)" /etc/login.defs
```

### 13.3 Example: Change default UID range

Edit `/etc/login.defs` as root:
```
UID_MIN     2000
UID_MAX     50000
```
Now new users will get UIDs starting from 2000.

### 13.4 Overriding `/etc/login.defs` with `useradd` options

Command-line options to `useradd` take precedence over `/etc/login.defs`:

| `/etc/login.defs` parameter | `useradd` override |
|----------------------------|--------------------|
| `UID_MIN` / `UID_MAX` | `-u` (specific UID) |
| `CREATE_HOME yes` | `-M` (do not create home) |
| `CREATE_HOME no` | `-m` (force create home) |
| `UMASK 022` | Not directly – use `-m` + `/etc/skel` permissions |
| `PASS_MAX_DAYS` | Can't be overridden by `useradd` – use `chage` after creation |

---

## 14. Real-World Examples – User & Group Management Scenarios

### Scenario 1: Onboarding a new developer (Alice)

**Requirements:**
- Username: `alice`
- Full name: "Alice Johnson"
- Primary group: `developers`
- Secondary groups: `docker`, `wheel` (for sudo)
- Home directory: `/home/alice`
- Default shell: `/bin/bash`
- Password must expire after 90 days

**Commands:**
```bash
# Create group if not exists
sudo groupadd developers

# Create user with custom comment, primary group, secondary groups
sudo useradd -c "Alice Johnson" -g developers -G docker,wheel -s /bin/bash alice

# Set initial password (force change on first login)
sudo passwd -e alice

# Set password aging: max 90 days, warn 7 days before
sudo chage -M 90 -W 7 alice

# Verify
id alice
sudo chage -l alice
```

### Scenario 2: Adding an existing user (bob) to multiple groups without losing current groups

**Current groups of bob:** `bob` (primary), `sales` (secondary)

**New requirement:** Also add to `marketing` and `developers`

**Command:**
```bash
sudo usermod -aG marketing,developers bob
```

**Check:**
```bash
groups bob
# Output: bob sales marketing developers
```

### Scenario 3: Creating a service user for a web application

**Requirements:**
- Username: `webapp`
- No login shell (use `/sbin/nologin`)
- No home directory
- UID in system range (e.g., 450)
- Part of group `www-data`

**Commands:**
```bash
sudo groupadd -r www-data
sudo useradd -r -u 450 -g www-data -s /sbin/nologin -M -c "Web Application Service" webapp
```

**Verify:**
```bash
grep webapp /etc/passwd
# Output: webapp:x:450:450:Web Application Service:/home/webapp:/sbin/nologin
# (home directory listed but not created because of -M)
```

### Scenario 4: Temporarily lock a user who went on leave

```bash
sudo usermod -L alice
# or
sudo passwd -l alice
```

**Unlock when they return:**
```bash
sudo usermod -U alice
```

### Scenario 5: Force all users to change passwords next login (e.g., after security breach)

```bash
# For a single user
sudo passwd -e alice

# For all normal users (UID >= 1000)
awk -F: '$3>=1000 {print $1}' /etc/passwd | while read user; do sudo passwd -e "$user"; done
```

### Scenario 6: Create a shared group and add multiple users at once

```bash
# Create group
sudo groupadd projectx

# Add three users (assume they exist)
sudo gpasswd -M alice,bob,charlie projectx

# Verify members
getent group projectx
```

### Scenario 7: Remove a user and reassign their files to another user

```bash
# Delete user 'olduser' but keep home directory
sudo userdel olduser

# Reassign all files owned by olduser (UID 1010) to newuser (UID 1020)
sudo find / -user 1010 -exec chown 1020 {} \;
```

### Scenario 8: Allow a user to run `systemctl` only for nginx without password

Edit `/etc/sudoers` with `visudo` and add:
```
deploy    ALL=(root)    NOPASSWD: /bin/systemctl status nginx, /bin/systemctl restart nginx
```

Test:
```bash
sudo -u deploy sudo -l
```

### Scenario 9: Create a user with a custom home directory outside `/home`

```bash
sudo useradd -d /data/ftp/anna -m -c "Anna FTP User" -s /bin/bash anna
```

### Scenario 10: Set password aging policy for a new user with very strict rules

```bash
# Create user
sudo useradd strict_user

# Set password (force change immediately)
sudo passwd -e strict_user

# Set: min 1 day, max 30 days, warn 5 days, inactive 3 days, expire on 2026-12-31
sudo chage -m 1 -M 30 -W 5 -I 3 -E 2026-12-31 strict_user
```

---

## 15. Quick Command Cheat Sheet for Users & Groups

| Task | Command |
|------|---------|
| List all users | `awk -F: '{print $1}' /etc/passwd` |
| List all groups | `awk -F: '{print $1}' /etc/group` |
| Show user's UID, GID, groups | `id username` |
| Show user's groups only | `groups username` |
| Create user with defaults | `sudo useradd username` |
| Create user with home, shell, comment | `sudo useradd -c "Name" -m -s /bin/bash username` |
| Set/change password | `sudo passwd username` |
| Force password change next login | `sudo passwd -e username` |
| Lock account | `sudo usermod -L username` |
| Unlock account | `sudo usermod -U username` |
| Add user to group (append) | `sudo usermod -aG groupname username` |
| Remove user from group | `sudo gpasswd -d username groupname` |
| Delete user (keep home) | `sudo userdel username` |
| Delete user + home + mail | `sudo userdel -r username` |
| Create group | `sudo groupadd groupname` |
| Delete group | `sudo groupdel groupname` |
| Show group members | `getent group groupname` |
| Set group members (replace) | `sudo gpasswd -M user1,user2 groupname` |
| View sudo privileges for user | `sudo -l -U username` |
| Check sudoers syntax | `sudo visudo -c` |
| View password aging | `sudo chage -l username` |

---

## 16. Common Pitfalls and How to Avoid Them

| Pitfall | Solution |
|---------|----------|
| Forgetting `-a` with `usermod -G` | Always use `-aG` unless you intend to replace all groups |
| Deleting a user with `userdel` (no `-r`) leaves home directory | Use `userdel -r` or manually clean up |
| Editing `/etc/sudoers` directly | Always use `visudo` – syntax errors break `sudo` for everyone |
| Giving `NOPASSWD: ALL` too broadly | Limit to specific commands and users |
| Not checking if a group is a primary group before `groupdel` | Use `grep :gid: /etc/passwd` to find users with that primary group |
| UID/GID conflicts when restoring from backup | Use `-u` and `-g` to match original IDs |

---

## 17. Verification Lab – Test Your Knowledge

Run these commands and explain the output:

1. `sudo useradd -m -s /bin/bash -c "Test User" -G wheel testuser`
2. `sudo passwd -e testuser`
3. `id testuser`
4. `sudo chage -l testuser`
5. `sudo usermod -aG docker testuser`
6. `groups testuser`
7. `sudo userdel -r testuser`

Then, in `/etc/sudoers` (using `visudo`), add a line that allows user `testuser` to run `/bin/systemctl status *` without a password. Verify with `sudo -l -U testuser`.

---

## 18. Complete Practical Mastery Test – Users & Groups

This test simulates real‑world administrative tasks covering **every section** of this chapter. Perform each task on a Linux VM or container with `sudo` access. Verify your work with the provided commands. **Attempt all tasks before looking at the answer key.**

> **Prerequisite:** Take a snapshot of your VM or ensure you are on a disposable test system.

---

### Part 1: Understanding Configuration Files (Inspection)

**Task 1.1 – Decode `/etc/passwd` and `/etc/shadow`**

Given this `/etc/passwd` entry:
```
alice:x:1001:1001:Alice Johnson, IT Dept:/home/alice:/bin/bash
```
Answer:
1. What does the `x` in the password field signify?
2. What is Alice's primary group ID?
3. Where is the actual password hash stored?

Given this `/etc/shadow` entry:
```
bob:$6$randomsalt$hashedpassword...:19500:7:90:14:30:19600:
```
Answer:
1. How many days must Bob wait before changing his password again?
2. After how many days will Bob be warned about password expiration?
3. When does Bob's account absolutely expire? (Hint: field 8)

**Task 1.2 – Inspect `/etc/login.defs`**
```bash
grep -E "^(PASS_MAX_DAYS|UID_MIN|CREATE_HOME)" /etc/login.defs
```
What is the default maximum password age for new users on this system?

---

### Part 2: User Creation and Basic Management

**Task 2.1 – Create a User with Custom Attributes**
Create a new user `intern1` with:
- Full name: "Summer Intern 2026"
- Primary group: `interns` (create if needed)
- Secondary groups: `docker`, `wheel`
- Home directory: `/home/intern1`
- Shell: `/bin/bash`
- UID: 1500

**Task 2.2 – Set Password and Force Change**
Set a temporary password for `intern1` and force a password change on first login.

**Task 2.3 – Verify User Creation**
Check `intern1` exists and display all group memberships.
```bash
id intern1
groups intern1
```

**Task 2.4 – Create a Service Account**
Create a system user `monitor_app` with:
- No login shell (`/sbin/nologin`)
- No home directory
- UID 450
- Primary group `monitor` (create if needed)

---

### Part 3: Modifying Existing Users and Groups

**Task 3.1 – Add User to Additional Group**
Create group `project_alpha` and add `intern1` to it **without removing** existing secondary groups.

**Task 3.2 – Change User’s Primary Group**
Change `intern1`’s primary group to `project_alpha`. What happens to the original primary group `interns`?

**Task 3.3 – Rename a User**
Rename `intern1` to `summer_intern`.

**Task 3.4 – Move Home Directory**
Move `summer_intern`’s home directory to `/data/home/summer_intern` (assume `/data/home` exists). Ensure all files are moved.

**Task 3.5 – Lock and Unlock Account**
Lock the account of `summer_intern`. Verify the password field in `/etc/shadow` starts with `!`. Then unlock the account.

---

### Part 4: Password Aging Policies

**Task 4.1 – Set Strict Aging for `summer_intern`**
Configure:
- Password must be changed every 60 days
- Minimum 1 day between changes
- Warning 7 days before expiry
- Account inactive if password not changed for 10 days after expiry
- Account expires on December 31, 2026

**Task 4.2 – Verify Aging Settings**
```bash
sudo chage -l summer_intern
```

**Task 4.3 – Force All Non‑System Users to Change Password at Next Login**
Write a one‑liner that forces a password change for every user with UID >= 1000.

---

### Part 5: Group Management

**Task 5.1 – Create a Group with Specific GID**
Create group `finance` with GID 3000.

**Task 5.2 – Add Multiple Users to a Group at Once**
Create three temporary users (`user1`, `user2`, `user3`). Add them all to `finance` in a single command, replacing any existing membership list.

**Task 5.3 – Remove a User from a Group**
Remove `user2` from the `finance` group using `gpasswd`.

**Task 5.4 – Delete a Group**
Attempt to delete group `interns`. If it fails, identify why and resolve the issue before deleting it.

---

### Part 6: `sudo` Configuration and `visudo`

**Task 6.1 – Grant Passwordless `sudo` for Specific Commands**
Allow `summer_intern` to run the following commands **without a password**:
- `/bin/systemctl restart nginx`
- `/bin/systemctl status nginx`
- `/bin/journalctl -u nginx`

Use `visudo` to add the rule.

**Task 6.2 – Create a Command Alias and User Alias**
Using `visudo`, define:
- `User_Alias WEBTEAM = summer_intern, user1`
- `Cmnd_Alias WEB_CMDS = /bin/systemctl restart nginx, /bin/systemctl status nginx, /bin/journalctl -u nginx`
- Grant `WEBTEAM` passwordless access to `WEB_CMDS`.

**Task 6.3 – Verify `sudo` Privileges**
```bash
sudo -l -U summer_intern
sudo -l -U user1
```

**Task 6.4 – Test the Configuration**
Switch to `summer_intern` and test running an allowed command with `sudo`. Confirm no password is prompted.

---

### Part 7: Troubleshooting and Log Analysis

**Task 7.1 – Check Authentication Logs**
Generate a failed login attempt (e.g., `su - summer_intern` with wrong password). Locate the failure in the appropriate log file (`/var/log/auth.log` or `/var/log/secure`).

**Task 7.2 – Find Users with a Specific Primary Group**
Write a command to list all users whose primary group is `project_alpha`.

**Task 7.3 – Identify Orphaned Home Directories**
Create a test user, delete it **without** the `-r` flag, then find and remove the orphaned home directory.

---

### Part 8: Real‑World Scenario – Onboarding a DevOps Engineer

**Scenario:** Onboard **Emma Lopez** (username `elopez`) with:
- Full name: "Emma Lopez"
- Primary group: `devops` (create it)
- Secondary groups: `docker`, `wheel`, `developers` (create `developers` if needed)
- Home directory: `/home/elopez` with skeleton files
- Shell: `/bin/zsh` (install `zsh` if not present)
- Password must be changed on first login, then every 90 days with 7‑day warning

**Task 8.1 – Execute Onboarding**
Write and execute all necessary commands.

**Task 8.2 – Grant `sudo` for Docker Commands**
Using `visudo`, allow `elopez` to run **any** `docker` command (e.g., `/usr/bin/docker *`) without a password.

**Task 8.3 – Document the Process**
Create a markdown file `onboarding_elopez.md` containing all commands used and verification output (`id elopez`, `chage -l elopez`, `sudo -l -U elopez`).

---

### Part 9: Cleanup and Restoration

**Task 9.1 – Remove All Test Users and Groups**
Delete all users created in this test (`summer_intern`, `monitor_app`, `user1`, `user2`, `user3`, `elopez`) along with their home directories. Delete the groups `interns`, `project_alpha`, `finance`, `devops`, `developers`, `monitor`.

**Task 9.2 – Verify No Artifacts Remain**
Check `/etc/passwd`, `/etc/group`, and `/home`.

---

## 19. Practical Test Answer Key

<details>
<summary><b>Click to reveal answers – attempt the test first!</b></summary>

### Part 1 Answers

**1.1**
1. `x` = password hash is stored in `/etc/shadow`.
2. Primary group ID = `1001`.
3. `/etc/shadow`.

**1.2**
- Minimum days = 7, Warn days = 14, Expiry field 8 = 19600 (approx 2023-09-01).

### Part 2 Commands

```bash
# 2.1
sudo groupadd interns
sudo useradd -u 1500 -g interns -G docker,wheel -c "Summer Intern 2026" -m -s /bin/bash intern1

# 2.2
sudo passwd intern1
sudo passwd -e intern1

# 2.4
sudo groupadd -r monitor
sudo useradd -r -u 450 -g monitor -s /sbin/nologin -M -c "Monitoring Service" monitor_app
```

### Part 3 Commands

```bash
# 3.1
sudo groupadd project_alpha
sudo usermod -aG project_alpha intern1

# 3.2
sudo usermod -g project_alpha intern1
# 'interns' remains as a secondary group.

# 3.3
sudo usermod -l summer_intern intern1

# 3.4
sudo mkdir -p /data/home
sudo usermod -d /data/home/summer_intern -m summer_intern

# 3.5
sudo usermod -L summer_intern
sudo grep summer_intern /etc/shadow   # should see '!'
sudo usermod -U summer_intern
```

### Part 4 Commands

```bash
# 4.1
sudo chage -M 60 -m 1 -W 7 -I 10 -E 2026-12-31 summer_intern

# 4.3
awk -F: '$3>=1000 {print $1}' /etc/passwd | while read user; do sudo passwd -e "$user"; done
```

### Part 5 Commands

```bash
# 5.1
sudo groupadd -g 3000 finance

# 5.2
for i in 1 2 3; do sudo useradd -m user$i; done
sudo gpasswd -M user1,user2,user3 finance

# 5.3
sudo gpasswd -d user2 finance

# 5.4
# Find users with primary group 'interns' and reassign them first.
sudo groupdel interns   # only after no user has it as primary
```

### Part 6 Configuration

Add to `/etc/sudoers` via `sudo visudo`:
```
User_Alias WEBTEAM = summer_intern, user1
Cmnd_Alias WEB_CMDS = /bin/systemctl restart nginx, /bin/systemctl status nginx, /bin/journalctl -u nginx
WEBTEAM ALL=(root) NOPASSWD: WEB_CMDS
```

Test:
```bash
sudo -u summer_intern sudo systemctl status nginx   # no password prompt
```

### Part 7 Commands

```bash
# 7.1
sudo tail /var/log/auth.log   # Debian/Ubuntu
sudo tail /var/log/secure     # RHEL

# 7.2
getent passwd | awk -F: '$4 == "'$(getent group project_alpha | cut -d: -f3)'" {print $1}'

# 7.3
sudo useradd testorphan
sudo userdel testorphan
ls -ld /home/testorphan   # still exists
sudo rm -rf /home/testorphan
```

### Part 8 Commands

```bash
# 8.1
sudo groupadd devops
sudo groupadd developers
sudo useradd -c "Emma Lopez" -g devops -G docker,wheel,developers -m -s /bin/zsh elopez
sudo passwd -e elopez
sudo chage -M 90 -W 7 elopez
```

**8.2** Add to `/etc/sudoers`:
```
elopez ALL=(root) NOPASSWD: /usr/bin/docker *
```

### Part 9 Cleanup

```bash
sudo userdel -r summer_intern monitor_app user1 user2 user3 elopez
sudo groupdel interns project_alpha finance devops developers monitor
# Verify with: getent passwd, getent group, ls /home
```

</details>

---

## 20. Self‑Evaluation Checklist

| I can... | Done |
|----------|------|
| Explain each field in `/etc/passwd` and `/etc/shadow` | ☐ |
| Create a user with custom UID, home, shell, comment, and groups | ☐ |
| Distinguish between primary and secondary groups | ☐ |
| Modify a user’s groups without losing existing memberships (`-aG`) | ☐ |
| Lock and unlock an account using `usermod` or `passwd` | ☐ |
| Set password aging policies with `chage` | ☐ |
| Create and delete groups, including handling primary group conflicts | ☐ |
| Use `gpasswd` to manage group memberships and administrators | ☐ |
| Safely edit `/etc/sudoers` with `visudo` and define aliases | ☐ |
| Grant passwordless `sudo` for specific commands | ☐ |
| Troubleshoot authentication issues using log files | ☐ |
| Automate bulk user operations with `awk` and loops | ☐ |
| Perform a complete user offboarding (including file reassignment) | ☐ |
| Understand UID/GID ranges and system vs. normal users | ☐ |


---

## Final Check – What's Now Covered

| Topic | Status |
|-------|--------|
| User types and UID ranges | ✓ |
| Primary vs secondary groups | ✓ |
| `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow` | ✓ |
| `useradd`, `usermod`, `userdel` with all options | ✓ |
| `groupadd`, `groupmod`, `groupdel` | ✓ |
| `passwd`, `chage` | ✓ |
| `gpasswd` (add, remove, set members) | ✓ |
| `wheel` / `sudo` groups | ✓ |
| `/etc/sudoers` detailed syntax, `visudo`, examples, aliases | ✓ |
| `/etc/login.defs` parameters and usage | ✓ |
| Real-world scenarios (10 examples) | ✓ |
| Cheat sheet | ✓ |
| Pitfalls and verification lab | ✓ |


---

## Key Takeaways for Cloud Engineering

- **User/group management is essential for EC2 instance security** – always create separate users, never work as `root`.
- **Use `sudo` with least privilege** – add users to specific groups (`wheel`, `docker`, `www-data`) rather than giving full root.
- **Lock accounts immediately** when an employee leaves or a service account is compromised.
- **`/etc/skel`** is your friend for standardizing shell environments across many users.
- **System accounts (UID 1-999)** should have `/sbin/nologin` or `/bin/false` as their shell.

---

## Practice Check

- [ ] I can create a new user with a custom home directory and a comment
- [ ] I can add a user to a secondary group without removing existing group memberships
- [ ] I can lock a user account and verify it is locked
- [ ] I can force a password change on next login
- [ ] I can view the password aging policy for a user with `chage -l`
- [ ] I can delete a group and remove a user from a group
- [ ] I can explain the difference between `/etc/passwd` and `/etc/shadow`
- [ ] I know which UID range is reserved for normal users

---

**Date documented:** 2026-04-14  
**Sources:** Linux Administration, GeeksforGeeks, Red Hat documentation, course notes

---
