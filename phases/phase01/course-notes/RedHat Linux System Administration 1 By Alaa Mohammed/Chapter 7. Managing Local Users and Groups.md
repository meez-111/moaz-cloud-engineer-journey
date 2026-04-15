

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
