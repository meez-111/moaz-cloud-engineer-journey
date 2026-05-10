Here is the **complete final note** for **Chapter 6: Managing SELinux Security**, now including a comprehensive **real‑world scenario** that takes you through a full SELinux troubleshooting and management workflow on a production web server.

---

# Chapter 6: Managing SELinux Security – Complete Professional Guide

## Table of Contents

1. [What is Access Control?](#1-what-is-access-control)
2. [Components of Access Control (Subject, Object, Action, Policy)](#2-components-of-access-control-subject-object-action-policy)
3. [Main Access Control Models (DAC, MAC, RBAC, ABAC)](#3-main-access-control-models-dac-mac-rbac-abac)
4. [SELinux Components – Labels, Contexts, and the Security Server](#4-selinux-components--labels-contexts-and-the-security-server)
   - 4.1 The SELinux Security Context (Label)
   - 4.2 Viewing Labels with `-Z` Options
5. [SELinux Modes (Enforcing, Permissive, Disabled)](#5-selinux-modes-enforcing-permissive-disabled)
6. [SELinux Policies (Targeted, Strict, MLS)](#6-selinux-policies-targeted-strict-mls)
7. [SELinux Booleans – Runtime Policy Toggles](#7-selinux-booleans--runtime-policy-toggles)
8. [SELinux File System Labeling Management](#8-selinux-file-system-labeling-management)
   - 8.1 Temporary Changes with `chcon`
   - 8.2 Persistent Changes with `semanage fcontext` and `restorecon`
   - 8.3 Other Label Management Commands
9. [Troubleshooting SELinux Denials](#9-troubleshooting-selinux-denials)
   - 9.1 Identifying Denials in Audit Logs (`ausearch`)
   - 9.2 Analyzing Denials with `sealert` (setroubleshoot)
   - 9.3 Creating Custom Policy Modules with `audit2allow`
10. [Important SELinux Configuration Files and Directories](#10-important-selinux-configuration-files-and-directories)
11. [How SELinux Works Under the Hood – LSM, AVC, and Type Enforcement](#11-how-selinux-works-under-the-hood--lsm-avc-and-type-enforcement)
12. [Quick Reference Table](#12-quick-reference-table)
13. [Real‑World Scenario – Deploying a Web Application with SELinux](#13-realworld-scenario--deploying-a-web-application-with-selinux)
14. [Practice Lab – Verify Your Understanding](#14-practice-lab--verify-your-understanding)

---

## 1. What is Access Control?

Access Control is a standard used to define permissions on computer systems. It determines **who** can access **what** resources and perform **which actions**. On Linux, traditional file permissions (read, write, execute) are one form of access control, but SELinux adds much stronger and finer‑grained controls.

---

## 2. Components of Access Control (Subject, Object, Action, Policy)

- **Subject** – The active entity requesting access. Usually a process (e.g., `httpd_t`).  
- **Object** – The passive resource being accessed. Can be a file, directory, socket, network port, etc.  
- **Action** – The operation the subject wants to perform (e.g., `read`, `write`, `execute`, `connect`).  
- **Policy** – The set of rules that defines allowed interactions between subjects and objects.

---

## 3. Main Access Control Models (DAC, MAC, RBAC, ABAC)

### 3.1 DAC – Discretionary Access Control

**Concept:** Resource owners decide who can access their resources. Linux traditional permissions (user/group/other) and ACLs are DAC.  

**Example:** A user `alice` owns `file.txt`. Using `chmod`, she can give read access to her group and revoke it from everyone else.  

**Problem:** If `alice` makes a mistake or her account is compromised, an attacker can use her permissions to access sensitive resources.

### 3.2 MAC – Mandatory Access Control

**Concept:** A central authority (system administrator) defines a global policy that overrides owner discretion. Subjects and objects are assigned **labels**; the kernel enforces rules based on these labels.  

**Examples:** SELinux, AppArmor, Smack.  

**Advantage:** Even if a process runs as `root` or a user misconfigures permissions, MAC can still block malicious actions.  

**Example:** Apache (`httpd_t`) cannot read `/etc/shadow` (labelled `shadow_t`), regardless of Unix permissions.

### 3.3 RBAC – Role‑Based Access Control

**Concept:** Permissions are assigned to **roles**, and users are assigned to roles.  

**SELinux’s use** – SELinux integrates RBAC by mapping Linux users to SELinux users (e.g., `unconfined_u`, `user_u`) and associating those with domains (types).  

### 3.4 ABAC – Attribute‑Based Access Control

**Concept:** Access decisions are based on attributes of the subject, object, environment (time, location, etc.).  

SELinux primarily uses Type Enforcement (TE) and RBAC, which can be considered a form of ABAC when combined with MLS (Multi‑Level Security) labels.

---

## 4. SELinux Components – Labels, Contexts, and the Security Server

### 4.1 The SELinux Security Context (Label)

Every process (subject) and object (file, directory, port, etc.) has an associated **SELinux context**, a variable‑length string in the format:

```
user:role:type:level
```

| Field | Meaning | Example |
|-------|---------|---------|
| **User** | SELinux user identity (not the Linux login user). | `unconfined_u` (regular users), `system_u` (system processes) |
| **Role** | Defines which domains a user can enter. Role‑Based Access Control (RBAC). | `object_r` (for files), `system_r` (for processes) |
| **Type** | The core of SELinux **Type Enforcement (TE)**. For processes: *domain*, for files: *type*. Policy rules define which domains can access which types. | `httpd_t`, `sshd_t`, `shadow_t`, `user_home_t` |
| **Level** | MLS / MCS sensitivity. Optional; used for Multi‑Level Security (military contexts). | `s0` (default), `s0:c0.c1023` (sensitivity with categories) |

**Example context for a file:**
```bash
$ ls -Z file1
-rw-rw-r-- user1 group1 unconfined_u:object_r:user_home_t:s0 file1
```
Here, `unconfined_u:object_r:user_home_t:s0` is the full context. In **targeted policy**, the kernel primarily checks the **type** (`user_home_t`) for access decisions.

### 4.2 Viewing Labels with `-Z` Options

| Command | What is displayed |
|---------|-------------------|
| `ls -Z` | SELinux context of files/directories |
| `ps -Z` | SELinux context of running processes |
| `id -Z` | SELinux context of the current user |
| `netstat -Z` | SELinux context of network connections |
| `cp -Z` | Preserve context when copying |
| `rsync -X` | Preserve extended attributes (including SELinux context) |

---

## 5. SELinux Modes (Enforcing, Permissive, Disabled)

| Mode | Behaviour |
|------|-----------|
| **Enforcing** | SELinux policy is fully enforced. Denials are logged and access is blocked. |
| **Permissive** | Policy is **not enforced** – access is allowed, but denials are **logged**. Useful for troubleshooting. |
| **Disabled** | SELinux is turned off entirely. Only DAC rules apply. Discouraged except for very specific scenarios. |

### 5.1 Viewing and Switching Modes (Runtime)

```bash
# Check current mode
getenforce

# Switch to Permissive (no reboot)
sudo setenforce 0

# Switch back to Enforcing
sudo setenforce 1
```

### 5.2 Persistent Mode Changes (Across Reboots)

Edit `/etc/selinux/config` (or the symlink `/etc/sysconfig/selinux`):

```bash
# Set SELinux mode
SELINUX=enforcing     # or permissive or disabled

# Policy type
SELINUXTYPE=targeted  # or strict, mls
```

> ⚠️ **Important:** Switching from **disabled** to **enforcing** requires a full filesystem relabel (`touch /.autorelabel` and reboot). Switching between enforcing and permissive is immediate and safe.

---

## 6. SELinux Policies (Targeted, Strict, MLS)

The `SELINUXTYPE` directive in `/etc/selinux/config` selects which policy is loaded.

### 6.1 Targeted Policy (Default)

- Most processes run **unconfined** (few restrictions).  
- Only specific, network‑facing daemons (e.g., `httpd`, `named`, `dhcpd`) are confined into distinct security domains.  
- Type Enforcement (TE) is the main mechanism.  
- **Best for:** General‑purpose servers, workstations, and most real‑world deployments.

### 6.2 Strict Policy

- **Every** process and subject is confined – there is no `unconfined_t`.  
- Much more restrictive and requires careful policy tuning.  
- Rarely used today, but essential for high‑security environments.

### 6.3 MLS (Multi‑Level Security) Policy

- Adds sensitivity levels (e.g., `s0` to `s15`) and categories to each context.  
- Designed for military or government systems where data classification (Top Secret, Secret, etc.) must be enforced.  
- Not commonly used in commercial cloud engineering.

---

## 7. SELinux Booleans – Runtime Policy Toggles

Booleans are **on/off switches** built into the policy. They allow administrators to modify SELinux behaviour without reloading or recompiling the entire policy.

### 7.1 Listing Booleans

```bash
# Short list (status only)
getsebool -a

# Detailed list (with descriptions, requires selinux-policy-devel)
semanage boolean -l
```

### 7.2 Viewing a Specific Boolean

```bash
getsebool httpd_enable_homedirs
```

### 7.3 Changing Booleans (Temporary)

```bash
# Enable
sudo setsebool httpd_enable_homedirs on

# Disable
sudo setsebool httpd_enable_homedirs off
```

### 7.4 Persistent Changes (Survive Reboot)

```bash
sudo setsebool -P httpd_enable_homedirs on
```

**Example Use Case:** Allow Apache to send email (e.g., from a contact form):

```bash
sudo setsebool -P httpd_can_sendmail on
```

---

## 8. SELinux File System Labeling Management

Files and directories inherit their SELinux type from their parent directory by default. Administrators often need to change or customise these types.

### 8.1 Temporary Changes with `chcon`

`chcon` changes the SELinux context of a file or directory **immediately**, but the change is **lost** on a filesystem relabel (`restorecon`).

```bash
# Change only the type of a file
sudo chcon -t httpd_sys_content_t /var/www/html/index.html

# Recursively change a directory and its contents
sudo chcon -R -t samba_share_t /srv/samba/share
```

**Use case:** Quick testing or debugging before making a permanent change.

### 8.2 Permanent Changes with `semanage fcontext` and `restorecon`

**Best practice:** Use `semanage fcontext` to add a rule to the SELinux policy, then apply it with `restorecon`.

```bash
# Add a rule: all files under /data/web should have type httpd_sys_content_t
sudo semanage fcontext -a -t httpd_sys_content_t "/data/web(/.*)?"

# Apply the rule to existing files
sudo restorecon -Rv /data/web
```

**Key options for `restorecon`:**
- `-R` – recursive
- `-v` – verbose
- `-F` – force reset (even if already correct)
- `-n` – no changes (dry run)

### 8.3 Other Label Management Commands

| Command | Purpose |
|---------|---------|
| `matchpathcon` | Check what context a path would have according to policy. |
| `semanage fcontext -l` | List all custom (local) file context rules. |
| `semanage fcontext -d` | Delete a custom rule. |
| `chcon --reference=ref_file file` | Copy context from another file. |

---

## 9. Troubleshooting SELinux Denials

When SELinux blocks an action, it logs an **AVC (Access Vector Cache)** denial in the audit log. Follow this systematic approach.

### 9.1 Identifying Denials in Audit Logs

```bash
# Search for recent AVC denials
sudo ausearch -m avc -ts recent

# Search by process name
sudo ausearch -c 'httpd' -ts today

# Follow new denials in real time
sudo tail -f /var/log/audit/audit.log | grep AVC
```

### 9.2 Analyzing Denials with `sealert` (setroubleshoot)

Install the necessary packages:

```bash
sudo dnf install setroubleshoot-server policycoreutils-python-utils
```

Run `sealert` on a denial message:

```bash
# Provide the full raw audit message
sealert -l "*"

# Or search for a specific AVC by message ID
sudo ausearch -m avc -ts recent | sealert -l
```

`sealert` gives human‑readable explanations and often suggests a fix (change a boolean, relabel files, or create a custom policy module).

### 9.3 Creating Custom Policy Modules with `audit2allow`

When a denial cannot be resolved by a boolean or file relabel, you may need to create a **local policy module**.

**Step‑by‑step example:**

```bash
# 1. Capture the denial(s)
sudo ausearch -c 'myapp' --raw > myapp_denials.log

# 2. Generate a policy module
sudo audit2allow -i myapp_denials.log -M myapp_policy

# 3. Load the module
sudo semodule -i myapp_policy.pp

# 4. Verify it is loaded
sudo semodule -l | grep myapp_policy
```

**Additional options:**
- `audit2allow -a` – use all audit logs
- `audit2allow -d` – generate dontaudit rules (silent denial)
- `semodule -r mymodule` – remove a custom module

> **Important:** Only use `audit2allow` when you fully understand what access you are granting. Local modules should be treated carefully and reviewed.

---

## 10. Important SELinux Configuration Files and Directories

| Path | Purpose |
|------|---------|
| `/etc/selinux/config` (link: `/etc/sysconfig/selinux`) | Main configuration file – sets `SELINUX` (mode) and `SELINUXTYPE` (policy). |
| `/etc/selinux/targeted/` | Policy store for the `targeted` policy (other policies have similar directories). |
| `/etc/selinux/targeted/contexts/files/file_contexts.local` | Custom file context rules added by `semanage fcontext -a`. |
| `/sys/fs/selinux/` | Runtime SELinux filesystem – reflects current configuration and statistics. |
| `/var/log/audit/audit.log` | The main audit log where SELinux denials are written. |
| `/var/lib/setroubleshoot/setroubleshoot.xml` | Cache for the setroubleshoot daemon (can be cleared for debugging). |

---

## 11. How SELinux Works Under the Hood – LSM, AVC, and Type Enforcement

The Linux kernel includes a framework called **Linux Security Modules (LSM)** that provides hooks at every kernel system call. SELinux is one of several LSM implementations.

### The LSM Hook

1. A process (subject) makes a system call (e.g., `open("/etc/shadow", O_RDONLY)`).
2. The kernel first checks **DAC** (traditional Unix permissions). If DAC denies access, the operation fails immediately.
3. If DAC allows access, the kernel invokes the **LSM hook**, passing the **subject context**, **object context**, and the **action**.
4. The SELinux security server checks the **Access Vector Cache (AVC)** for a cached decision.
5. If not cached, the security server consults the loaded **policy** (rules of the form `allow domain_t type_t:class { permissions };`).
6. The kernel either proceeds (if allowed) or returns **EACCES / Permission denied** and logs an AVC denial.

### Type Enforcement (TE) – The Core

- Every subject (process) has a **domain** (type).
- Every object (file, socket, port) has a **type**.
- The policy contains millions of `allow` rules that specify which domains can access which types, and what operations are permitted.

### The AVC

The AVC caches recently evaluated rules, dramatically speeding up SELinux decisions. When a process tries the same access repeatedly, the AVC returns the answer without re‑scanning the full policy database.

### Transition Rules

When an unconfined user (`unconfined_t`) executes a binary labelled `httpd_exec_t`, the policy defines a **domain transition**:

```
allow unconfined_t httpd_exec_t:process transition;
type_transition unconfined_t httpd_exec_t:process httpd_t;
```
The resulting child process runs in the confined `httpd_t` domain.

---

## 12. Quick Reference Table

| Task | Command |
|------|---------|
| Show SELinux mode | `getenforce` |
| Temporary mode switch (Enforcing ↔ Permissive) | `setenforce 1` or `0` |
| View file context | `ls -Z` |
| View process context | `ps -Z` |
| List all booleans | `getsebool -a` |
| Set boolean (temporary) | `setsebool name on/off` |
| Set boolean (persistent) | `setsebool -P name on/off` |
| Temporarily change file type | `chcon -t type file` |
| Permanently add custom file context rule | `semanage fcontext -a -t type '/path(/.*)?'` |
| Apply permanent file context changes | `restorecon -Rv /path` |
| Search recent SELinux denials | `ausearch -m avc -ts recent` |
| Analyse a denial | `sealert -l "*"` |
| Generate policy module from denial | `ausearch -c 'name' --raw \| audit2allow -M mymodule` |
| Load a custom policy module | `semodule -i mymodule.pp` |
| List loaded modules | `semodule -l` |
| Remove a custom module | `semodule -r mymodule` |

---

## 13. Real‑World Scenario – Deploying a Web Application with SELinux

### Background

You have provisioned a RHEL 9 server to host a new customer portal. The web application files reside in `/webdata/portal` instead of the default `/var/www/html`. The server runs Apache (`httpd`) and must connect to a PostgreSQL database on another host. SELinux is in **enforcing** mode.

As you test the deployment, the Application Team reports that the web pages return "403 Forbidden" errors, and the application cannot connect to the database. Local file permissions appear correct (`755` directories, `644` files, owner `apache`). You suspect SELinux is blocking access.

### Step 1 – Verify SELinux status and web server domain

```bash
getenforce                           # should output Enforcing
sudo systemctl status httpd
ps -Z | grep httpd                   # check domain of httpd processes
```

Output shows `httpd_t` – the web server is confined.

### Step 2 – Identify the file context problem

List the security context of the web root:

```bash
ls -Z /webdata/portal/index.html
# likely shows something like unconfined_u:object_r:default_t:s0
```

Expected context for web content is `httpd_sys_content_t`. The `default_t` type is not accessible to `httpd_t`. Hence the 403 error.

### Step 3 – Examine SELinux denials related to httpd

```bash
sudo ausearch -m avc -c httpd -ts recent
```

You should see lines like:

```
type=AVC msg=audit(1683700000.123:456): avc:  denied  { read } for  pid=1234 comm="httpd" name="index.html" dev="dm-0" ino=78901 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
```

### Step 4 – Get a human‑readable explanation with `sealert`

```bash
sudo sealert -l "*"
```

The output may suggest running `semanage fcontext` to add a new labeling rule.

### Step 5 – Test a temporary fix using `chcon`

To quickly confirm the cause, change the type of the directory temporarily:

```bash
sudo chcon -R -t httpd_sys_content_t /webdata/portal
ls -Z /webdata/portal/index.html     # now shows httpd_sys_content_t
```

Access the site again – the 403 error should be gone. However, this change will be lost after a `restorecon`.

### Step 6 – Implement the permanent fix

Add a custom file context rule and relabel the directory:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/webdata/portal(/.*)?"
sudo restorecon -Rv /webdata/portal
```

Now even after a full relabel or file restore, the correct context persists.

### Step 7 – Enable database connectivity

The web application uses a remote PostgreSQL database on port 5432. By default, `httpd_t` cannot make outbound TCP connections to databases. Check the boolean:

```bash
getsebool httpd_can_network_connect_db
# Probably off
```

Enable it permanently:

```bash
sudo setsebool -P httpd_can_network_connect_db on
```

Restart httpd to apply:

```bash
sudo systemctl restart httpd
```

Now the application should connect to the database.

### Step 8 – (Optional) Simulate a more complex denial and create a custom policy module

Imagine the portal also uses a CGI script in `/webdata/portal/cgi-bin` that needs to write temporary files to `/var/tmp`. This is not allowed by default. You see denials in the audit log:

```bash
sudo ausearch -c 'portal.cgi' -m avc -ts recent
```

Generate a policy module from these denials:

```bash
sudo ausearch -c 'portal.cgi' --raw > portal_denials.log
sudo audit2allow -i portal_denials.log -M portal_policy
# Inspect the generated .te file
less portal_policy.te
```

If the policy looks safe, load it:

```bash
sudo semodule -i portal_policy.pp
```

The custom CGI now works. You can verify with `semodule -l | grep portal`.

### Step 9 – Final verification and monitoring

Check the overall system:

```bash
getenforce
ls -Z /webdata/portal
sudo ausearch -m avc -ts today   # no unexpected denials
```

The portal is fully operational with SELinux enforcing.

---

## 14. Practice Lab – Verify Your Understanding

### Lab 1: Exploring Current SELinux Status
Run the following commands and interpret the output:
```bash
getenforce
sestatus
ls -Z /var/www/html/index.html (or any existing file)
ps -Z | grep sshd
```

### Lab 2: Working with Booleans
```bash
# List all booleans
getsebool -a | grep httpd

# Temporarily allow HTTPD to connect to databases
sudo setsebool httpd_can_network_connect_db on
getsebool httpd_can_network_connect_db

# Reboot the system (or just log out / back in) and check – the change will be lost.
getsebool httpd_can_network_connect_db

# Set it permanently
sudo setsebool -P httpd_can_network_connect_db on
```

### Lab 3: Trigger and Troubleshoot an SELinux Denial
```bash
# Create a test web directory and file with wrong context
sudo mkdir -p /webtest
echo "SELinux test" | sudo tee /webtest/index.html

# Try to serve it via a web server (or simulate with a script)
# Watch the audit log
sudo ausearch -m avc -ts recent

# Analyse the denial
sudo sealert -l "*" | grep -A20 "webtest"

# Fix permanently using semanage
sudo semanage fcontext -a -t httpd_sys_content_t "/webtest(/.*)?"
sudo restorecon -Rv /webtest
```

### Lab 4: Temporary vs Permanent Context Change
```bash
# Temporary change
sudo chcon -t tmp_t /webtest/index.html
ls -Z /webtest/index.html

# After restorecon, the context reverts
sudo restorecon /webtest/index.html
ls -Z /webtest/index.html

# Permanent change (should survive restorecon)
```

### Lab 5: Create a Custom Policy Module (Simulated)
```bash
# Use sample denied messages or generate a test denial (e.g., run a custom script in a confined domain)
# Capture the denial
sudo ausearch -c 'your_process_name' --raw > my_denials.log

# Create module
sudo audit2allow -i my_denials.log -M my_custom_policy

# If any rules are generated, review the .te file
less my_custom_policy.te

# Load it (if non‑empty)
sudo semodule -i my_custom_policy.pp

# Remove it
sudo semodule -r my_custom_policy
```

---

# Complete SELinux Command Reference

This section provides **every** essential SELinux command, organised by category, with all important options and multiple real‑world examples. Use it as your definitive cheat sheet for managing SELinux on RHEL‑based systems.

---

## 1. Mode & Status

| Command | Purpose | Options | Examples |
|---------|---------|---------|----------|
| `getenforce` | Print current SELinux mode | (none) | `getenforce` |
| `setenforce` | Change mode temporarily (Enforcing/Permissive) | `1` / `Enforcing`, `0` / `Permissive` | `sudo setenforce 0` (switch to Permissive) |
| `sestatus` | Show detailed SELinux status and policy info | `-v` (verbose, includes booleans), `-b` (display current booleans) | `sestatus`<br>`sestatus -v` |
| `selinuxenabled` | Exit 0 if SELinux is enabled, else 1. For scripts. | – | `if selinuxenabled; then echo "SELinux active"; fi` |

---

## 2. Context Viewing (`-Z` family)

| Command | What it shows | Options | Examples |
|---------|---------------|---------|----------|
| `ls -Z` | SELinux context of files/directories | `-lZ`, `-dZ` (directory only) | `ls -Z /etc/passwd` |
| `ps -Z` | Context of running processes | `-eZ`, `auxZ` | `ps -eZ \| grep httpd` |
| `id -Z` | Context of current user | – | `id -Z` |
| `ss -Z` / `netstat -Z` | Context of network sockets (ss is modern) | `-tulpnZ` | `sudo ss -tulpnZ \| grep :22` |
| `cp -Z` | Copy file and set destination context to default type | `-a` (implies `-Z`?) use `cp --preserve=context` or `cp -Z` | `cp -Z /etc/hosts /tmp/hosts` (context will match target parent) |
| `rsync -X` | Preserve extended attributes including SELinux context | `-avX` | `rsync -avX /data/ backup:/data/` |

`cp` behaviour:
- `cp -Z` sets the target context to the **default** type for the destination directory (like `restorecon`).  
- `cp --preserve=context` preserves the original context.  
- `cp -a` (archive) preserves context only if `--preserve=context` is included (usually not, so use `cp -a --preserve=context` or `rsync -X`).  

---

## 3. File Context Management

| Command | Purpose | Key Options | Examples |
|---------|---------|-------------|----------|
| `chcon` | **Temporary** context change (lost after `restorecon`) | `-t type`, `-u user`, `-r role`, `-R` recursive, `--reference=ref` | `sudo chcon -t httpd_sys_content_t /var/www/html/index.html`<br>`sudo chcon --reference=/etc/passwd /tmp/testfile` |
| `restorecon` | Restore default context according to policy | `-R` recursive, `-v` verbose, `-F` force reset, `-n` dry run | `sudo restorecon -Rv /var/www/html`<br>`sudo restorecon -n /path/to/check` |
| `matchpathcon` | Show what context a file **should** have (as defined in policy) | `-V` verify (compare actual vs. expected) | `matchpathcon /var/www/html/index.html`<br>`matchpathcon -V /var/www/html/index.html` |
| `fixfiles` | Bulk relabel of filesystem; wrapper around `setfiles`/`restorecon` | `check` (only check), `restore` (fix), `relabel` (create `/.autorelabel` flag) | `sudo fixfiles check`<br>`sudo fixfiles restore`<br>`sudo fixfiles relabel` (then reboot) |
| `setfiles` | Low‑level tool to set contexts using a file_contexts file | `-r rootdir`, `-v` verbose, `-n` dry run | `sudo setfiles /etc/selinux/targeted/contexts/files/file_contexts /mnt` |

**Persistent context changes** should always be done via `semanage fcontext` + `restorecon`, not `chcon`.

---

## 4. Policy Management – `semanage`

`semanage` is the primary tool for managing SELinux policy configuration. It has many subcommands, each with its own options.

**General syntax:**  
`sudo semanage <subcommand> [options]`

### 4.1 Subcommand Overview

| Subcommand | Purpose |
|------------|---------|
| `fcontext` | File context mappings (persistent labelling) |
| `port` | Network port type definitions |
| `boolean` | Manage booleans (description, default, modify) |
| `login` | Map Linux users to SELinux users |
| `user` | SELinux users |
| `permissive` | Put a domain into permissive mode (only that domain) |
| `module` | Install/remove policy modules |
| `node` / `interface` | Network node/interface labelling (rare) |
| `dontaudit` | Toggle dontaudit rules on/off |

### 4.2 `semanage fcontext` – Custom File Labelling

| Operation | Command |
|-----------|---------|
| List local custom rules | `sudo semanage fcontext -l` |
| List all rules (custom + built‑in) | `sudo semanage fcontext -lC` |
| Add a new rule | `sudo semanage fcontext -a -t httpd_sys_content_t '/data/web(/.*)?'` |
| Add with file type (e.g., for directories only) | `sudo semanage fcontext -a -t httpd_sys_content_t -f d '/data/web'` |
| Delete a rule | `sudo semanage fcontext -d -t httpd_sys_content_t '/data/web(/.*)?'` |
| Modify a rule | `sudo semanage fcontext -m -t new_type '/path(/.*)?'` |
| Equivalence (treat path like another) | `sudo semanage fcontext -a -e /var/www/html /data/myweb` |

After adding a rule, apply with `restorecon`.

### 4.3 `semanage port` – Network Port Type

| Operation | Command |
|-----------|---------|
| List ports and types | `sudo semanage port -l` |
| Add a non‑standard SSH port (2222) | `sudo semanage port -a -t ssh_port_t -p tcp 2222` |
| Delete a port | `sudo semanage port -d -t ssh_port_t -p tcp 2222` |
| Modify (rare) | `sudo semanage port -m -t new_type -p tcp 2222` |

### 4.4 `semanage boolean`

| Action | Command |
|--------|---------|
| List all booleans with descriptions | `sudo semanage boolean -l` |
| Modify boolean persistently (same as `setsebool -P`) | `sudo semanage boolean -m --on ftpd_anon_write` |
| Extract boolean definition | `sudo semanage boolean -E -a` (extract all custom boolean modifications) |

Though `setsebool -P` is easier, `semanage boolean` can modify default values.

### 4.5 `semanage login` – User‑to‑SELinux‑User Mapping

| Action | Command |
|--------|---------|
| List mappings | `sudo semanage login -l` |
| Map Linux user `john` to SELinux user `staff_u` | `sudo semanage login -a -s staff_u john` |
| Map with MLS range | `sudo semanage login -a -s user_u -r s0-s0:c0.c1023 john` |
| Delete mapping | `sudo semanage login -d john` |

### 4.6 `semanage user` – SELinux Users

| Action | Command |
|--------|---------|
| List SELinux users | `sudo semanage user -l` |
| Add a constrained user | `sudo semanage user -a -R "guest_r webapp_r" -r s0-s0:c0.c1023 myuser_u` |

### 4.7 `semanage permissive` – Put a Domain in Permissive Mode

| Action | Command |
|--------|---------|
| List permissive domains | `sudo semanage permissive -l` |
| Make `httpd_t` permissive (useful for debugging) | `sudo semanage permissive -a httpd_t` |
| Remove permissive domain | `sudo semanage permissive -d httpd_t` |

---

## 5. Boolean Commands

| Command | Purpose | Options | Examples |
|---------|---------|---------|----------|
| `getsebool` | List boolean states | `-a` (all), boolean name | `getsebool -a`<br>`getsebool httpd_enable_homedirs` |
| `setsebool` | Set boolean on/off | `-P` (permanent across reboots) | `sudo setsebool -P httpd_enable_homedirs on` |
| `semanage boolean -l` | List booleans with descriptions | – | `sudo semanage boolean -l \| grep httpd` |

---

## 6. Audit & Troubleshooting

| Command | Purpose | Options | Examples |
|---------|---------|---------|----------|
| `ausearch` | Query audit daemon logs | `-m avc` (AVC denials), `-c comm` (process name), `-ts recent/today/now`, `--raw` (for passing to audit2allow) | `sudo ausearch -m avc -ts recent`<br>`sudo ausearch -c httpd -m avc --raw > denials.log` |
| `sealert` (setroubleshoot) | Human‑readable denial explanation | `-l "*"` (all alerts), `-a audit.log` | `sealert -a /var/log/audit/audit.log`<br>`sealert -l "*"` |
| `audit2allow` | Generate policy module from denials | `-i input`, `-M modulename`, `-a` (all audit.log), `-d` (dontaudit) | `sudo ausearch -c myapp --raw \| audit2allow -M myapp_policy`<br>`audit2allow -a -M test` |
| `audit2why` | Explain why a denial happened (reads audit.log) | – | `sudo audit2why < /var/log/audit/audit.log` |
| `avcstat` | Display AVC statistics | – | `avcstat` |

---

## 7. Policy Module Management

| Command | Purpose | Options | Examples |
|---------|---------|---------|----------|
| `semodule` | Manage SELinux policy modules | `-l` (list), `-i` (install .pp), `-r` (remove by name), `-e` (enable), `-d` (disable), `-E` (extract), `-X` (set priority) | `sudo semodule -l`<br>`sudo semodule -i myapp.pp`<br>`sudo semodule -r myapp`<br>`sudo semodule -d myapp` (disable) |
| `checkmodule` | Compile policy module (.te → .mod) | `-M` (enable MLS), `-o output.mod` | `checkmodule -M -m -o myapp.mod myapp.te` |
| `semodule_package` | Create policy package (.mod + file contexts → .pp) | `-o output.pp -m module.mod [-f file_contexts]` | `semodule_package -o myapp.pp -m myapp.mod -f myapp.fc` |
| `load_policy` | Load compiled policy binary (rare) | – | `sudo load_policy /etc/selinux/targeted/policy/policy.33` |

---

## 8. Policy Querying – `seinfo` & `sesearch`

These tools belong to the `setools-console` package (`sudo dnf install setools-console`).

| Command | Purpose | Options | Examples |
|---------|---------|---------|----------|
| `seinfo` | Query SELinux policy components | `-t` (types), `-r` (roles), `-u` (users), `-b` (booleans), `-a` (attributes) | `seinfo -t \| grep http`<br>`seinfo -b \| wc -l` |
| `sesearch` | Search policy allow rules | `-A` (allow rules), `-s source`, `-t target`, `-c class`, `-p perm`, `-d` (dontaudit) | `sesearch -A -s httpd_t -t httpd_sys_content_t`<br>`sesearch -A -c process -p transition` |

---

## 9. Miscellaneous

| Command | Purpose | Example |
|---------|---------|---------|
| `fixfiles` | As above (bulk relabel) | `sudo fixfiles check` |
| `setfiles` | As above (low‑level) | `sudo setfiles -r /mnt file_contexts /mnt` |
| `selinuxdefcon`? | Not a command. |

---

## 10. Common Real‑World Sequences

### 10.1 Fix a Web Content Denial

```bash
# Identify
sudo ausearch -m avc -c httpd -ts recent
# Check context
ls -Z /webdata
# Permanent fix
sudo semanage fcontext -a -t httpd_sys_content_t "/webdata(/.*)?"
sudo restorecon -Rv /webdata
# Verify
ls -Z /webdata
```

### 10.2 Allow Apache to Connect to Database

```bash
getsebool httpd_can_network_connect_db
sudo setsebool -P httpd_can_network_connect_db on
```

### 10.3 Custom App Gets Denied Writing to `/opt/myapp/logs`

```bash
# Collect denials
sudo ausearch -c myapp -m avc --raw > myapp_logs.avc
# Generate module
audit2allow -i myapp_logs.avc -M myapp_logs
# Inspect
cat myapp_logs.te
# Install
sudo semodule -i myapp_logs.pp
# Check
sudo semodule -l | grep myapp
```

### 10.4 Temporarily Put httpd_t in Permissive Mode (Debugging)

```bash
sudo semanage permissive -a httpd_t
# ... test ...
sudo semanage permissive -d httpd_t
```

### 10.5 Change SSH Port to 2222

```bash
# Configure sshd to listen on 2222, then:
sudo semanage port -a -t ssh_port_t -p tcp 2222
sudo systemctl restart sshd
```

### 10.6 Quickly Check What Context a File Should Have

```bash
matchpathcon /var/www/html/index.html
```

### 10.7 Relabel Entire Filesystem After Disabling SELinux and Re‑enabling

```bash
sudo fixfiles relabel && sudo reboot
# or
sudo touch /.autorelabel && sudo reboot
```

---

**Date documented:** 2026-05-10  
**Sources:** Red Hat Enterprise Linux SELinux documentation, GitHub Security Lab introduction, man pages for SELinux utilities, NSA SELinux project.