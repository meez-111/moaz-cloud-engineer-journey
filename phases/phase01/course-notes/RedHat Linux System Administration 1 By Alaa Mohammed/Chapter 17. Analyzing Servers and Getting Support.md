# Chapter 17: Analyzing Servers and Getting Support – Complete Professional Guide

## Table of Contents

- [Chapter 17: Analyzing Servers and Getting Support – Complete Professional Guide](#chapter-17-analyzing-servers-and-getting-support--complete-professional-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction: Why Analyze Servers and Get Support?](#1-introduction-why-analyze-servers-and-get-support)
  - [2. Cockpit – Web‑Based Server Management](#2-cockpit--webbased-server-management)
    - [2.1 What is Cockpit / RHEL Web Console?](#21-what-is-cockpit--rhel-web-console)
    - [2.2 Installation and Enabling](#22-installation-and-enabling)
    - [2.3 Accessing the Web Console](#23-accessing-the-web-console)
    - [2.4 What You Can Do in the Cockpit Web Console](#24-what-you-can-do-in-the-cockpit-web-console)
    - [2.5 Cockpit Plugins](#25-cockpit-plugins)
  - [3. Red Hat Customer Portal and Subscription Management](#3-red-hat-customer-portal-and-subscription-management)
    - [3.1 What is the Red Hat Customer Portal?](#31-what-is-the-red-hat-customer-portal)
    - [3.2 Subscription Management Overview](#32-subscription-management-overview)
    - [3.3 Registering a System (CLI)](#33-registering-a-system-cli)
    - [3.4 Managing Subscriptions in the Web Console](#34-managing-subscriptions-in-the-web-console)
  - [4. `sosreport` – Gathering Diagnostic Information](#4-sosreport--gathering-diagnostic-information)
    - [4.1 What is an `sosreport`?](#41-what-is-an-sosreport)
    - [4.2 Installing the `sos` Package](#42-installing-the-sos-package)
    - [4.3 Basic `sos report` Usage](#43-basic-sos-report-usage)
    - [4.4 Advanced `sos report` Options](#44-advanced-sos-report-options)
    - [4.5 Understanding the Output Archive](#45-understanding-the-output-archive)
    - [4.6 Providing an `sosreport` to Red Hat Support](#46-providing-an-sosreport-to-red-hat-support)
    - [4.7 `sos clean` – Obfuscating Sensitive Data](#47-sos-clean--obfuscating-sensitive-data)
    - [4.8 `sos collect` – Gathering Reports from Multiple Nodes](#48-sos-collect--gathering-reports-from-multiple-nodes)
  - [5. `restorecon` Role](#5-restorecon-role)
  - [6. `redhat-support-tool` – Command‑Line Support Access](#6-redhat-support-tool--commandline-support-access)
    - [6.1 What is `redhat-support-tool`?](#61-what-is-redhat-support-tool)
    - [6.2 Installation](#62-installation)
    - [6.3 Basic Usage and Interactive Shell](#63-basic-usage-and-interactive-shell)
    - [6.4 Common Commands and Examples](#64-common-commands-and-examples)
  - [7. Diagnostic Reports in the Web Console (Cockpit)](#7-diagnostic-reports-in-the-web-console-cockpit)
    - [7.1 Generating a Diagnostic Report](#71-generating-a-diagnostic-report)
    - [7.2 Downloading a Diagnostic Report](#72-downloading-a-diagnostic-report)
  - [8. Quick Reference Table](#8-quick-reference-table)
  - [9. Practice Lab – Verify Your Understanding](#9-practice-lab--verify-your-understanding)
  - [10. Real‑World Scenario – Troubleshooting a Production Issue with Support Tools](#10-realworld-scenario--troubleshooting-a-production-issue-with-support-tools)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [1. Initial monitoring via Cockpit](#1-initial-monitoring-via-cockpit)
      - [2. Verify subscription status](#2-verify-subscription-status)
      - [3. Preliminary command‑line investigation](#3-preliminary-commandline-investigation)
      - [4. Search Red Hat Knowledgebase for similar symptoms](#4-search-red-hat-knowledgebase-for-similar-symptoms)
      - [5. Generate a comprehensive sosreport](#5-generate-a-comprehensive-sosreport)
      - [6. Open a support case and attach the sosreport](#6-open-a-support-case-and-attach-the-sosreport)
      - [7. (Alternative) Upload sosreport directly from CLI](#7-alternative-upload-sosreport-directly-from-cli)
      - [8. Generate a diagnostic report via Cockpit for a second perspective](#8-generate-a-diagnostic-report-via-cockpit-for-a-second-perspective)
      - [9. List open cases and check status](#9-list-open-cases-and-check-status)
      - [10. Post‑resolution cleanup](#10-postresolution-cleanup)
    - [Verification Checklist](#verification-checklist)
  - [11. Summary](#11-summary)

---

## 1. Introduction: Why Analyze Servers and Get Support?

As a system administrator, you need to:

- **Monitor** server health (CPU, memory, disk, network).
- **Troubleshoot** issues (service failures, performance degradation, configuration errors).
- **Collect diagnostic data** before contacting support.
- **Interact efficiently** with Red Hat Customer Portal and support tools.

Red Hat provides a complete ecosystem for support:

- **Cockpit** (RHEL Web Console): Graphical remote management.
- **Red Hat Customer Portal**: Knowledgebase, subscriptions, case management.
- **`sosreport`**: Standardised diagnostic data collection.
- **`redhat-support-tool`**: Command‑line interface to Portal and support services.

---

## 2. Cockpit – Web‑Based Server Management

### 2.1 What is Cockpit / RHEL Web Console?

Cockpit is a **lightweight, web‑based graphical interface** for managing and monitoring Linux servers. On RHEL, it is called the **RHEL Web Console**, based on the upstream Cockpit project.

Key capabilities:

| Area | Tasks |
|------|-------|
| **System** | View system information (hostname, CPU, memory, uptime), manage services, review logs. |
| **Storage** | Manage disks, partitions, LVM, NFS, iSCSI. |
| **Networking** | Configure interfaces, bonds, bridges, firewall rules. |
| **Virtualisation** | Create and manage virtual machines (via libvirt). |
| **Containers** | Manage Podman containers and images (via Cockpit podman plugin). |
| **Software updates** | Apply system updates. |
| **Subscriptions** | Register and manage Red Hat subscriptions. |
| **Diagnostic reports** | Generate and download `sosreport` directly from the web UI. |
| **Terminal** | Built‑in web terminal for command‑line access. |

**Why use Cockpit?** It reduces the need to remember commands for routine tasks, provides visual graphs for performance monitoring, and can manage **multiple remote hosts** from a single browser session.

### 2.2 Installation and Enabling

**Installation (if not present):**

```bash
sudo dnf install cockpit
```

Many RHEL 9 installation variants include Cockpit by default. If not, the above command installs it.

**Enabling the service:**

Cockpit uses `cockpit.socket` (socket‑activated). Enable and start it:

```bash
sudo systemctl enable --now cockpit.socket
```

This starts a web server listening on port **9090** on all network interfaces.

**Firewall configuration (if firewalld is active):**

```bash
sudo firewall-cmd --add-service=cockpit --permanent
sudo firewall-cmd --reload
```

The `cockpit` service opens TCP port 9090.

**Verify installation and enablement:**

```bash
sudo systemctl status cockpit.socket
sudo ss -tulpn | grep 9090
```

### 2.3 Accessing the Web Console

Open a web browser and go to:

```
https://<your-server-ip>:9090
```

Use your **standard system username and password** (the same as for SSH). If you have sudo privileges, you will be able to perform administrative tasks.

> **First‑time access:** The browser will show a certificate warning (self‑signed). Accept it.

### 2.4 What You Can Do in the Cockpit Web Console

| Section | Main Tasks |
|---------|------------|
| **Overview** | System information, performance graphs (CPU, memory, disk, network), alerts. |
| **Logs** | Browse, filter, and search system logs (`journald`). |
| **Storage** | Create/remove partitions, configure LVM, format file systems, mount, iSCSI. |
| **Networking** | Manage interfaces, bonds, bridges, VLANs, firewall. |
| **Accounts** | Create/modify/delete users, manage password policies. |
| **Services** | Start/stop/restart systemd services, enable/disable, view logs. |
| **Applications** | Install software via DNF (graphical interface). |
| **Diagnostic Reports** | Generate, download, and manage `sosreport` archives. |
| **Terminal** | Built‑in web terminal (no need for SSH client). |
| **Updates** | Apply package updates. |
| **Subscriptions** | Register system, attach subscriptions, enable repositories. |
| **SELinux** | View status, enforce/permissive mode, troubleshoot denials. |

### 2.5 Cockpit Plugins

Cockpit can be extended with additional plugins. On RHEL 9, many are available in the default repositories:

| Plugin Package | Functionality |
|----------------|----------------|
| `cockpit-storaged` | Enhanced storage management (required for diagnostic reports). |
| `cockpit-podman` | Manage Podman containers and images. |
| `cockpit-machines` | Manage virtual machines (libvirt). |
| `cockpit-sosreport` | Diagnostic report generation (integrated). |
| `cockpit-dashboard` | Multi‑host management dashboard. |

Install with: `sudo dnf install cockpit-<plugin-name>`.

---

## 3. Red Hat Customer Portal and Subscription Management

### 3.1 What is the Red Hat Customer Portal?

The [Red Hat Customer Portal](https://access.redhat.com/) is the central hub for:

- **Knowledgebase** – Solutions, articles, product documentation.
- **Product downloads** – ISOs, packages, container images.
- **Support cases** – Open, update, and manage technical support requests.
- **Subscription management** – View and assign subscriptions to systems.
- **Security advisories** – CVEs, errata, updates.

### 3.2 Subscription Management Overview

RHEL subscriptions provide:

- Access to RHEL repositories (for updates, packages, security fixes).
- Technical support (based on subscription tier).
- Red Hat Insights (proactive analysis).
- Access to the Customer Portal.

Subscription management is handled by **Red Hat Subscription Manager** (`subscription-manager` CLI) and integrated into Cockpit.

### 3.3 Registering a System (CLI)

**CLI method (using `subscription-manager`):**

```bash
# Register with username/password
sudo subscription-manager register --username your_username --password your_password

# Automatically attach a subscription that matches the system
sudo subscription-manager attach --auto

# List available repositories (optional)
sudo subscription-manager repos --list

# Enable specific repositories (e.g., AppStream, BaseOS)
sudo subscription-manager repos --enable rhel-9-for-x86_64-appstream-rpms --enable rhel-9-for-x86_64-baseos-rpms

# See system status
sudo subscription-manager status
```

If you have an **activation key**:

```bash
sudo subscription-manager register --org=<org_id> --activationkey=<key_name>
```

### 3.4 Managing Subscriptions in the Web Console

In Cockpit:

1. Log in to the Web Console.
2. In the **Overview** section, click the **Not registered** warning (or go to **Subscriptions** from the main menu).
3. Click **Register**.
4. Choose registration method:
   - **Username/password** – Enter your Red Hat Customer Portal credentials (optional: organisation ID if your account belongs to multiple organisations).
   - **Activation key** – Enter organisation ID and activation key(s).
5. Optionally disable Red Hat Insights (uncheck the **Insights** checkbox).
6. Click **Register**.

After registration, the Subscriptions page shows:

- Attached subscriptions.
- Consumed entitlements.
- System purpose (role, SLA, usage).

Subscription data is automatically synced with the Customer Portal.

---

## 4. `sosreport` – Gathering Diagnostic Information

### 4.1 What is an `sosreport`?

`sosreport` (also called `sos report`) is a standardised diagnostic tool that collects:

- System configuration details (kernel version, loaded modules, configuration files).
- Logs (`journald`, application logs).
- Command outputs (status of services, network, storage, etc.).
- Installed package list.

This single archive provides Red Hat support engineers with all the necessary information to begin troubleshooting without asking for piecemeal data.

**Important naming:**  
In RHEL 7 and earlier, the command was `sosreport`.  
In RHEL 8+, the command is **`sos report`** (the package is still `sos`). The old `sosreport` command still works but emits a deprecation warning and is redirected.

### 4.2 Installing the `sos` Package

```bash
sudo dnf install sos
```

Verify installation:

```bash
rpm -q sos
# Example output: sos-4.2-15.el9.noarch
```

### 4.3 Basic `sos report` Usage

**Generate a report (interactive):**

```bash
sudo sos report
```

The tool will:
- Prompt for a support case number (optional, can be left empty).
- Collect data from all enabled plugins.
- Create a `.tar.xz` archive in `/var/tmp/`.

**Example output:**

```bash
sosreport-server1-12345678-2026-05-03-tgictvu.tar.xz
```

**Non‑interactive (batch mode):**  
Use `--batch` to skip all prompts (case number will be empty). This is useful for scripts.

```bash
sudo sos report --batch
```

### 4.4 Advanced `sos report` Options

| Option | Meaning | Example |
|--------|---------|---------|
| `--batch` | Non‑interactive mode (no prompts). | `sudo sos report --batch` |
| `--case-id` | Specify support case number. | `sudo sos report --case-id 01234567` |
| `--label` | Arbitrary label to identify the report. | `sudo sos report --label pre-upgrade` |
| `--encrypt-pass` | Encrypt the archive with a password. | `sudo sos report --encrypt-pass` (prompts) |
| `--encrypt-key` | Encrypt using GPG key (path to public key). | `sudo sos report --encrypt-key /path/to/key` |
| `--upload` | Upload report directly to Red Hat (requires `--case-id`). | `sudo sos report --case-id 01234567 --upload` |
| `--ticket-number` | Alias for `--case-id`. | – |
| `--skip-plugins` | Exclude specific plugins (comma‑separated). | `sudo sos report --skip-plugins=auditd,docker` |
| `--only-plugins` | Include only specific plugins. | `sudo sos report --only-plugins=networking,processor` |
| `--since` | Collect logs from a specific time (journalctl format). | `sudo sos report --since "1 hour ago"` |
| `--quiet` | Minimal output (suppress progress). | `sudo sos report --quiet` |
| `-z` | Use maximum compression (xz). | `sudo sos report -z` |
| `--tmp-dir` | Specify alternative temporary directory. | `sudo sos report --tmp-dir /var/sos` |

**Example: Generate a report for case 98765 with encryption, uploading to Red Hat:**

```bash
sudo sos report --case-id 98765 --encrypt-pass --upload
```

### 4.5 Understanding the Output Archive

The report is saved in `/var/tmp/` with the pattern:

```
sosreport-<hostname>-<case-id>-<date>-<random>.tar.xz
```

Also, a `.sha256` checksum file is created for integrity verification.

```bash
ls -la /var/tmp/sosreport*
```

**What is included in the archive?**

- Kernel version, loaded modules.
- System and service configuration files (`/etc/`).
- Logs (`journalctl`, `/var/log/`).
- Output of diagnostic commands (e.g., `df -h`, `ip a`, `systemctl list-units`).
- Installed package list (`rpm -qa`).
- SELinux status and denials.
- Systemd unit status.

All data is collected with minimal impact on system resources. The archive is compressed and ready to be attached to a support case.

### 4.6 Providing an `sosreport` to Red Hat Support

There are several methods:

1. **Upload directly from CLI** (requires `--case-id` and `--upload`):  
   ```bash
   sudo sos report --case-id 01234567 --upload
   ```

2. **Attach to support case via Customer Portal** – Download the archive and upload manually through the Case Details page.

3. **Use `redhat-support-tool`** – See section 6.

4. **Share via secure link** – When creating a case, a secure file upload link is available.

> **Best practice:** Always run `sos report` before opening a support case. Attach the archive to the initial case to accelerate troubleshooting.

### 4.7 `sos clean` – Obfuscating Sensitive Data

`sos clean` is a subcommand that obfuscates potentially sensitive information (IP addresses, hostnames, usernames) from an already generated `sosreport` archive.

```bash
sos clean sosreport-*.tar.xz
```

The command creates a new, obfuscated archive in `/var/tmp/` with `-obfuscated` in the name.

**Useful for:** Environments where logs contain personal data, or when you want to anonymise the report before sharing with third parties.

### 4.8 `sos collect` – Gathering Reports from Multiple Nodes

`sos collect` runs `sos report` on a set of remote hosts (e.g., a cluster) and collects all reports locally.

```bash
sos collect --nodes node1.example.com,node2.example.com --master example.com
```

This is useful for troubleshooting distributed systems (OpenShift, Ceph, Pacemaker). It requires SSH key‑based authentication or a common password.

---

## 5. `restorecon` Role

TK (Placeholder for `restorecon` – presumably part of SELinux context restoration)

---

## 6. `redhat-support-tool` – Command‑Line Support Access

### 6.1 What is `redhat-support-tool`?

`redhat-support-tool` is a command‑line utility that provides **console‑based access to Red Hat Customer Portal services**. It can be used interactively or in scripts to:

- Search the Red Hat Knowledgebase.
- Open, update, and list support cases.
- Download case attachments (including solutions).
- Attach files (such as `sosreport` archives) to existing cases.
- Provide automatic log analysis.

### 6.2 Installation

The tool is included by default on RHEL. If not present:

```bash
sudo dnf install redhat-support-tool
```

### 6.3 Basic Usage and Interactive Shell

**Single command execution:**

```bash
redhat-support-tool <command> [options]
```

**Interactive shell mode:**

```bash
redhat-support-tool shell
```

In shell mode, you get tab completion and a command history. The same commands are available.

### 6.4 Common Commands and Examples

| Command | Purpose | Example |
|---------|---------|---------|
| `search` | Search Knowledgebase for a term. | `redhat-support-tool search "SELinux denial httpd"` |
| `getcase` | Download a support case details and comments. | `redhat-support-tool getcase 01234567` |
| `opencase` | Create a new support case. | `redhat-support-tool opencase --product "Red Hat Enterprise Linux" --version 9` |
| `modifycase` | Update an existing case (add comment). | `redhat-support-tool modifycase 01234567 --addcomment "Please find attached sosreport"` |
| `attach` | Attach a file to a case. | `redhat-support-tool attach -c 01234567 /var/tmp/sosreport-*.tar.xz` |
| `listcases` | List all open cases for your account. | `redhat-support-tool listcases` |
| `config` | View or set configuration (API keys, etc.). | `redhat-support-tool config --list` |

**Example workflow:**

```bash
# 1. Search Knowledgebase for a known issue
redhat-support-tool search "CPU soft lockup RHEL 9"

# 2. Create a new support case (interactive prompts follow)
redhat-support-tool opencase

# 3. Generate sosreport
sudo sos report --case-id 01234567 --batch

# 4. Attach the sosreport to the case
redhat-support-tool attach -c 01234567 /var/tmp/sosreport-*.tar.xz

# 5. Add a comment explaining the issue
redhat-support-tool modifycase 01234567 --addcomment "The issue occurs every night at 2am."
```

> **Note:** The tool uses your Red Hat Customer Portal credentials. You may be prompted for them, or you can configure an API key.

**Viewing case details:**

```bash
redhat-support-tool getcase 01234567
```

**Attaching a file directly from an OpenShift debug pod (advanced):**  
Useful in containerised environments:

```bash
redhat-support-tool attach -c 01234567 --from-pod <pod-name> /path/to/file
```

---

## 7. Diagnostic Reports in the Web Console (Cockpit)

Cockpit provides a graphical interface to generate and download `sosreport` archives without using the command line.

### 7.1 Generating a Diagnostic Report

1. Log in to the RHEL Web Console (`https://<server>:9090`).
2. In the left menu, select **Tools** → **Diagnostic reports**.
3. Click the **Generate report** button (usually a `+` or `Create` icon).
4. Enter a **label** (e.g., "Pre‑upgrade snapshot") – optional.
5. **Optional settings:**
   - **Encryption passphrase** – If provided, the archive will be encrypted with AES‑256.
   - **Obfuscate network addresses, hostnames, and usernames** – Protects sensitive data.
   - **Use verbose logging** – Increases verbosity for debugging.
6. Click **Generate**. The process may take several minutes, depending on system activity.

You can stop the generation at any time using the **Stop** button.

### 7.2 Downloading a Diagnostic Report

After generation (or if previous reports exist):

1. Go to **Tools** → **Diagnostic reports**.
2. Locate the desired report in the list (by label or date).
3. Click the **Download** button (usually a download icon) next to the report.
4. The file is downloaded via your browser.

You can also **delete** old reports from the same page.

These reports are identical to those generated by `sos report` on the command line and can be attached to support cases.

---

## 8. Quick Reference Table

| Task | Command / Action |
|------|------------------|
| Install Cockpit | `sudo dnf install cockpit` |
| Enable Cockpit | `sudo systemctl enable --now cockpit.socket` |
| Open firewall for Cockpit | `sudo firewall-cmd --add-service=cockpit --permanent`<br>`sudo firewall-cmd --reload` |
| Access Cockpit | `https://<server-ip>:9090` |
| Register system (CLI) | `sudo subscription-manager register --username...`<br>`sudo subscription-manager attach --auto` |
| Install `sos` | `sudo dnf install sos` |
| Generate basic sosreport | `sudo sos report --batch` |
| Generate with case ID | `sudo sos report --case-id 01234567` |
| Upload sosreport to Red Hat | `sudo sos report --case-id 01234567 --upload` |
| Obfuscate sensitive data | `sos clean sosreport-*.tar.xz` |
| Install `redhat-support-tool` | `sudo dnf install redhat-support-tool` |
| Search Knowledgebase | `redhat-support-tool search "keyword"` |
| Open a support case (interactive) | `redhat-support-tool opencase` |
| Attach file to case | `redhat-support-tool attach -c 01234567 /path/to/file` |
| Download case details | `redhat-support-tool getcase 01234567` |
| List open cases | `redhat-support-tool listcases` |
| Generate diagnostic report in Cockpit | **Tools** → **Diagnostic reports** → **Generate report** |
| Download report in Cockpit | **Tools** → **Diagnostic reports** → **Download** button |

---

## 9. Practice Lab – Verify Your Understanding

1. **Cockpit installation and access:**
   - Install Cockpit on your RHEL 9 system.
   - Enable the service and open the firewall.
   - Access the web console from a browser.
   - Explore the **Overview** page and note the CPU and memory graphs.

2. **System registration:**
   - If you have a Red Hat subscription, register your system using `subscription-manager`.
   - Attach a subscription and enable the AppStream repository.
   - Verify successful registration with `subscription-manager status` and in Cockpit.

3. **Generate an sosreport:**
   - Create an sosreport with the label `lab-test`.
   - Encrypt the archive with a password.
   - Locate the generated file in `/var/tmp/`.
   - Inspect its contents (you can extract it: `tar -xvf sosreport-*.tar.xz`).

4. **Use `redhat-support-tool`:**
   - Search the Knowledgebase for a relevant topic (e.g., "systemd + journald").
   - If you have an existing support case, list your open cases.

5. **Diagnostic report in Cockpit:**
   - Generate a diagnostic report through the Cockpit web interface.
   - Download it and compare its size/modification time with the CLI‑generated one.

6. **sosreport obfuscation:**
   - Run `sos clean` on your previously generated archive.
   - Verify that a new `-obfuscated` archive is created.

7. **Plugin exploration:**
   - Install an additional Cockpit plugin (e.g., `cockpit-podman` if you use containers).
   - Verify the new section appears in the web console.

---

## 10. Real‑World Scenario – Troubleshooting a Production Issue with Support Tools

### Background

You manage a production RHEL 9 web server (`web‑prod‑01`) that hosts a critical application. The system is registered with a Red Hat subscription. Recently, the application has been experiencing intermittent crashes, and the server’s CPU spikes every few hours. You must diagnose the issue, collect diagnostic data, and involve Red Hat Support if needed.

### Step‑by‑Step Implementation

#### 1. Initial monitoring via Cockpit

Log in to the RHEL Web Console (`https://web-prod-01:9090`).

- Go to **Overview** and examine CPU, memory, and disk performance graphs. Note the time of recent spikes.
- Navigate to **Logs** and filter by `error` or `critical` priority to look for relevant entries (e.g., `OOM`, `segfault`).
- Check the **Services** section to see if the application service (`myapp.service`) has failed or restarted repeatedly.

#### 2. Verify subscription status

```bash
sudo subscription-manager status
```

Ensure the system is registered and the AppStream repository is enabled.

#### 3. Preliminary command‑line investigation

```bash
sudo systemctl status myapp
sudo journalctl -u myapp --since "2 hours ago" -p err
sudo df -hT
sudo free -h
top -b -n 1 | head -20
```

#### 4. Search Red Hat Knowledgebase for similar symptoms

```bash
redhat-support-tool search "RHEL 9 CPU spike application crash"
redhat-support-tool search "systemd service restart loop sosreport"
```

If none of the articles resolve the issue, proceed to open a case.

#### 5. Generate a comprehensive sosreport

Label the report `prod-cpu-issue` and associate it with a case number (if known), or leave the case ID empty for now.

```bash
sudo sos report --label prod-cpu-issue --encrypt-pass
```

Record the generated filename, e.g., `sosreport-web-prod-01-20260504-xxxxxx.tar.xz`.

Optionally, obfuscate sensitive data before sharing externally:

```bash
sos clean sosreport-web-prod-01-20260504-xxxxxx.tar.xz
```

#### 6. Open a support case and attach the sosreport

**Using `redhat-support-tool` (interactive):**

```bash
redhat-support-tool opencase --product "Red Hat Enterprise Linux" --version 9
```

Follow the prompts to describe the issue. Note the case number (e.g., `03123456`).

Attach the sosreport:

```bash
redhat-support-tool attach -c 03123456 /var/tmp/sosreport-web-prod-01-20260504-xxxxxx.tar.xz
```

Add a comment with relevant observations:

```bash
redhat-support-tool modifycase 03123456 --addcomment "CPU spikes correlate with /var/log/myapp/error.log entries about memory allocation failures."
```

#### 7. (Alternative) Upload sosreport directly from CLI

If you already have a case number, you could have done:

```bash
sudo sos report --case-id 03123456 --upload --encrypt-pass
```

#### 8. Generate a diagnostic report via Cockpit for a second perspective

Navigate to **Tools** → **Diagnostic reports** → **Generate report**. Give it the label `pre-support-snapshot`. Download the resulting archive for your own records.

#### 9. List open cases and check status

```bash
redhat-support-tool listcases
redhat-support-tool getcase 03123456
```

#### 10. Post‑resolution cleanup

After Red Hat Support provides a fix (e.g., a kernel update or configuration change), verify that the issue is resolved:

- Monitor CPU and service stability in Cockpit.
- Optionally generate another sosreport (with a new label) to capture the healthy state for future comparison.

### Verification Checklist

- [ ] Cockpit accessible and shows performance graphs.
- [ ] Subscription is active (`subscription-manager status`).
- [ ] `sos report` generated and encrypted (or obfuscated if needed).
- [ ] Support case opened and sosreport attached.
- [ ] Knowledgebase search returns relevant articles.
- [ ] Cockpit diagnostic report generated and downloaded.
- [ ] Case can be tracked via `redhat-support-tool listcases`.
- [ ] Issue resolution verified via monitoring.

---

## 11. Summary

- **Cockpit** provides a user‑friendly web interface for monitoring and managing RHEL systems remotely.
- **Red Hat Subscription Manager** (`subscription-manager`) integrates with the Customer Portal for entitlements and repository access.
- **`sos report`** is the standard diagnostic collection tool—always run it before opening a support case.
- **`redhat-support-tool`** enables direct command‑line interaction with the Customer Portal, including case management and Knowledgebase search.
- **Cockpit's diagnostic reports** offer a graphical alternative to `sos report` for less command‑line‑oriented administrators.

Mastering these tools ensures you can:

- Proactively monitor server health.
- Efficiently gather and provide diagnostic information.
- Leverage Red Hat's support ecosystem to resolve issues quickly.

---

**Date documented:** 2026-05-04  
**Sources:** Red Hat Enterprise Linux 9 documentation, Cockpit project, `sos` utility man pages, Red Hat Customer Portal