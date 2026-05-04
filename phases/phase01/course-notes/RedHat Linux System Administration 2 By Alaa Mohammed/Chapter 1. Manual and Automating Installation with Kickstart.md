## Chapter 1. Manual and Automating Installation with Kickstart

## Table of Contents

- [Chapter 1. Manual and Automating Installation with Kickstart](#chapter-1-manual-and-automating-installation-with-kickstart)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Downloading the RHEL ISO](#2-downloading-the-rhel-iso)
- [3. Installation Methods](#3-installation-methods)
- [4. Manual Installation (Anaconda)](#4-manual-installation-anaconda)
- [5. Semi‑Automatic Installation with Kickstart](#5-semiautomatic-installation-with-kickstart)
  - [5.1 Anatomy of a Kickstart File](#51-anatomy-of-a-kickstart-file)
  - [5.2 Kickstart Commands Reference (Essential)](#52-kickstart-commands-reference-essential)
  - [5.3 Pre‑installation and Post‑installation Scripts](#53-preinstallation-and-postinstallation-scripts)
  - [5.4 Generating a Kickstart File](#54-generating-a-kickstart-file)
  - [5.5 Validating a Kickstart File (`ksvalidator`)](#55-validating-a-kickstart-file-ksvalidator)
  - [5.6 Including External Files (`%include`)](#56-including-external-files-include)
  - [5.7 Publishing a Kickstart File with Apache HTTP Server](#57-publishing-a-kickstart-file-with-apache-http-server)
  - [5.8 Performing a Kickstart Installation](#58-performing-a-kickstart-installation)
  - [5.9 Debugging and Logs](#59-debugging-and-logs)
- [6. Full Automation with PXE](#6-full-automation-with-pxe)
  - [6.1 PXE Boot Process](#61-pxe-boot-process)
  - [6.2 Setting Up a Simple PXE Environment (using `dnsmasq`)](#62-setting-up-a-simple-pxe-environment-using-dnsmasq)
  - [6.3 Network Installation Tree](#63-network-installation-tree)
- [7. Security Considerations](#7-security-considerations)
- [8. Quick Reference Table](#8-quick-reference-table)
- [9. Real‑World Scenario – Building an Automated Deployment Server](#9-realworld-scenario--building-an-automated-deployment-server)
  - [Background](#background)
  - [Step 1 – Prepare the Deployment Server](#step-1--prepare-the-deployment-server)
  - [Step 2 – Set Up the Installation Tree](#step-2--set-up-the-installation-tree)
  - [Step 3 – Create the Kickstart File](#step-3--create-the-kickstart-file)
  - [Step 4 – Validate the Kickstart File](#step-4--validate-the-kickstart-file)
  - [Step 5 – Configure the PXE Environment (dnsmasq)](#step-5--configure-the-pxe-environment-dnsmasq)
  - [Step 6 – Test the Fully Automatic Installation](#step-6--test-the-fully-automatic-installation)
  - [Step 7 – Post‑Deployment Verification](#step-7--postdeployment-verification)
  - [Cleaning Up](#cleaning-up)
- [10. Practice Lab](#10-practice-lab)

---

## 1. Introduction

Red Hat Enterprise Linux supports several installation methods, from fully manual interactive installs to completely hands‑off, network‑based provisioning. The two core technologies for automation are:

- **Kickstart** – a text‑based answer file that defines every installation choice.
- **PXE (Preboot eXecution Environment)** – network booting that allows a machine to start the installer without physical media.

Together, they enable administrators to deploy dozens or hundreds of identical servers quickly, consistently, and with minimal human intervention.

---

## 2. Downloading the RHEL ISO

To perform any installation, you first need the installation image. On the [Red Hat Product Downloads](https://access.redhat.com/downloads/) page, the following ISO types are available:

| ISO Type | File Name | Description |
| :--- | :--- | :--- |
| **"Binary DVD"** | `rhel-<version>-<arch>-dvd.iso` | A full installation image that allows you to complete the installation without network access. Recommended for new users and testing. |
| **"Minimal Boot" ISO** | `rhel-<version>-<arch>-boot.iso` | A minimal image that installs the bootloader and kernel. It then downloads the software packages either from the Red Hat CDN or from a custom network source. |

**Example `curl` command to download the ISO (using a subscription):**

```bash
curl -o /var/tmp/rhel9.iso \
  -k "https://cdn.redhat.com/content/dist/rhel9/9.6/x86_64/isos/rhel-9.6-x86_64-dvd.iso" \
  -u 'username:password'
```

> **Tip:** You may also use the `--cookie` option if you have obtained a session cookie from the Customer Portal.

---

## 3. Installation Methods

| Method | Description |
| :--- | :--- |
| **Manual** | The graphical, step‑by‑step installation performed via the `Anaconda` installer. An answer file (`/root/anaconda-ks.cfg`) is generated at the end, capturing all options selected during the process. |
| **Semi‑Automatic (Kickstart)** | A pre‑written Kickstart file is provided to the installer, which performs the installation automatically. However, this method still requires manual initiation (e.g., booting from an ISO or USB drive and adding the `inst.ks=` parameter). |
| **Full‑Automatic (PXE + Kickstart)** | The system is booted from the network using a PXE server, and the `inst.ks=` boot parameter is passed to the kernel. The installer then automatically retrieves the Kickstart file and performs a completely hands‑free installation. |

---

## 4. Manual Installation (Anaconda)

The following steps are typically performed during a manual installation:

1.  **Language & Time:** Defining the system language, keyboard layout, and time zone.
2.  **Installation Source:** Selecting the location of the packages (e.g., local DVD, network URL).
3.  **Software Selection:** Choosing the base environment (e.g., "Server with GUI", "Minimal Install").
4.  **Installation Destination:** Configuring the disk partitioning scheme (`Standard Partition`, `LVM`, or `LVM Thin Provisioning`).
5.  **Network & Hostname:** Configuring network interfaces and setting the hostname.
6.  **Root Password & User Creation:** Setting the root password and optionally creating a non‑root administrative user (members of the `wheel` group have `sudo` permissions).
7.  **Begin Installation:** Anaconda performs the installation based on the defined settings, then generates the Kickstart answer file (`/root/anaconda-ks.cfg`).

---

## 5. Semi‑Automatic Installation with Kickstart

A Kickstart file is a simple ASCII text file containing a list of configuration items, each identified by a keyword. The Anaconda installer automatically generates a sample `anaconda-ks.cfg` based on the selections made during a manual installation. This file serves as a reference for creating new, custom Kickstart files.

### 5.1 Anatomy of a Kickstart File

| Section | Description |
| :--- | :--- |
| **Command Section** | The main body containing configuration commands for the installation (`lang`, `timezone`, `rootpw`, `url`, `network`, etc.). **Required until the system is fully configured**. |
| `%packages` Section | Defines the software packages to be installed. You can specify individual package names or groups using the `@` prefix (e.g., `@core`, `@web-server`). |
| `%pre` Section | A script that runs before the installer probes the hardware or applies the partitioning layout. It runs in a minimal environment (`/bin/sh`). |
| `%post` Section | A script that runs in the freshly installed system before the first reboot. By default, it runs inside a `chroot` jail where the normal `/bin/bash` environment is available. The `--nochroot` option allows this section to run in the installer environment. |

**Important:** The order of sections is fixed – **installation options first, then `%packages`, and finally `%pre` and `%post` scripts**.

### 5.2 Kickstart Commands Reference (Essential)

Below are some of the most commonly used directives. For a complete list, refer to the Red Hat documentation.

```bash
# System basics
lang en_US.UTF-8
keyboard us
timezone America/New_York --utc
rootpw --iscrypted $6$...   # encrypted password (recommended)
user --name=admin --password=$6$... --groups=wheel

# Clear and partition disks
clearpart --all --initlabel
autopart --type=lvm          # automatic LVM partitioning

# Network configuration
network --bootproto=static --ip=192.168.1.100 --netmask=255.255.255.0 --gateway=192.168.1.1 --nameserver=8.8.8.8 --device=eth0 --hostname=server.example.com

# Installation source and location
url --url="http://reposerver/rhel9/BaseOS/"
repo --name="appstream" --baseurl="http://reposerver/rhel9/AppStream/"

# Restart after installation
reboot
```

**Password encryption** is critical; you can obtain an encrypted password with `python -c 'import crypt; print(crypt.crypt("mypassword"))'` or use `openssl passwd -6`.

### 5.3 Pre‑installation and Post‑installation Scripts

These scripts provide powerful automation.

```bash
%pre
#!/bin/sh
echo "Detecting hardware..." > /tmp/pre.log
# Pre‑install scripts run in a restricted /bin/sh
%end

%post
#!/bin/bash
# This runs inside the installed system (chroot)
echo "Customising system..." >> /root/post-install.log
dnf config-manager --add-repo http://local/repo/custom.repo
dnf install -y my-app
systemctl enable my-app
%end
```

Use `%post --nochroot` to run a script in the installer environment (e.g., to copy files from a USB drive to the installed system).

### 5.4 Generating a Kickstart File

1.  **From a Manual Installation:** Copy and edit the `/root/anaconda-ks.cfg` file.
2.  **Using the Online Kickstart Generator:** On the Red Hat Customer Portal, the "Kickstart Generator" helps create a file via a web form.
3.  **Using the `mkkickstart` command:** This tool generates a Kickstart file from an existing system's configuration (available in some RHEL versions).
4.  **Manual Creation:** Write the file from scratch in a plain text editor.

### 5.5 Validating a Kickstart File (`ksvalidator`)

Always validate the syntax before attempting an installation. The `ksvalidator` tool is part of the `pykickstart` package.

```bash
sudo dnf install pykickstart

# Validate against RHEL 9 syntax
ksvalidator -v RHEL9 /path/to/ks.cfg

# Validate a remote file
ksvalidator http://192.168.1.100/ks.cfg
```

If the syntax is correct, the command returns no output and exits with 0.

### 5.6 Including External Files (`%include`)

To keep Kickstart files modular, you can include other files:

```bash
%include /tmp/disk-setup.cfg
%include http://server/network-config.cfg
```

The included files are merged into the current Kickstart file at that point. This is useful for reusing common setup fragments across different server roles.

### 5.7 Publishing a Kickstart File with Apache HTTP Server

To allow network‑based automated installations, the Kickstart file must be accessible via HTTP.

1.  **Install Apache:**
    ```bash
    dnf install httpd -y
    systemctl enable --now httpd
    ```

2.  **Publish the Kickstart File:**
    ```bash
    mkdir -p /var/www/html/kickstart
    cp /root/anaconda-ks.cfg /var/www/html/kickstart/ks.cfg
    chmod 644 /var/www/html/kickstart/ks.cfg
    ```

3.  **Configure the Firewall:**
    ```bash
    firewall-cmd --add-service=http --permanent
    firewall-cmd --reload
    ```

### 5.8 Performing a Kickstart Installation

Once the file is available, e.g., at `http://yourserver/kickstart/ks.cfg`, you can start an installation by adding the `inst.ks=` boot parameter.

*   **Manual ISO Boot:**  
    At the boot menu, press `Tab` (for BIOS) or `e` (for UEFI). Add to the kernel command line:
    ```
    inst.ks=http://yourserver/kickstart/ks.cfg
    ```
    The installer then automatically retrieves and executes the file.

*   **Via PXE Server:**  
    The `inst.ks` parameter is embedded in the PXE configuration file (`grub.cfg` or `pxelinux.cfg/default`) on the network boot server.

### 5.9 Debugging and Logs

If a Kickstart installation fails, helpful logs are preserved in the installed system or can be viewed during installation:

- On the installed system: `/root/install.log`, `/root/anaconda-ks.cfg` (the generated answer file).
- During installation: switch to virtual terminals (`Ctrl+Alt+F2` to `F5`) to see log messages.
- You can add `inst.debug` to the boot parameters for verbose output.

---

## 6. Full Automation with PXE

PXE enables a machine to boot from the network, completely eliminating the need for physical media.

### 6.1 PXE Boot Process

The process requires three components on the network:

| Component | Role |
| :--- | :--- |
| **DHCP Server** | Assigns IP addresses and provides the address of the TFTP server (next‑server) and the bootloader filename. |
| **TFTP Server** | Serves the network bootloader (e.g., `pxelinux.0` or `bootx64.efi`), kernel (`vmlinuz`), and initial ramdisk (`initrd.img`). |
| **HTTP/HTTPS Server** | Hosts the Kickstart file and optionally the full RHEL installation tree (the contents of the DVD). |

### 6.2 Setting Up a Simple PXE Environment (using `dnsmasq`)

For small labs or testing, `dnsmasq` can provide DHCP, TFTP, and even DNS in a single lightweight package.

```bash
sudo dnf install dnsmasq syslinux -y
```

Example `/etc/dnsmasq.conf` additions:

```ini
interface=eth0
dhcp-range=192.168.1.200,192.168.1.250,12h
dhcp-boot=pxelinux.0
enable-tftp
tftp-root=/var/lib/tftpboot
```

Place the bootloader files in `/var/lib/tftpboot/`:
- `/var/lib/tftpboot/pxelinux.0` (from `syslinux` package)
- `/var/lib/tftpboot/ldlinux.c32`
- `/var/lib/tftpboot/vmlinuz` (kernel from the DVD ISO)
- `/var/lib/tftpboot/initrd.img` (from the DVD ISO)
- `/var/lib/tftpboot/pxelinux.cfg/default` – the PXE configuration file that specifies the kernel boot parameters, including `inst.ks=`.

Example `pxelinux.cfg/default`:
```
default linux
label linux
  kernel vmlinuz
  append initrd=initrd.img inst.ks=http://192.168.1.100/kickstart/ks.cfg
```

### 6.3 Network Installation Tree

For a fully autonomous deployment, you should also serve the entire RHEL installation tree via HTTP. Extract the DVD ISO to a directory and share it:

```bash
mkdir /var/www/html/rhel9
mount -o loop /var/tmp/rhel9.iso /mnt
cp -a /mnt/* /var/www/html/rhel9/
```

Then, in the Kickstart file, point to this repository:
```bash
url --url="http://192.168.1.100/rhel9/"
```

---

## 7. Security Considerations

- **Encrypt the `rootpw`**: Use `--iscrypted` and provide a hashed password.
- **Restrict access to the Kickstart server**: In a production environment, HTTP Basic Authentication or firewall rules should protect the Kickstart file, as it may contain plain‑text credentials (even encrypted passwords can be brute‑forced).
- **Use `inst.ks=` with HTTPS** where possible.
- **Avoid storing unencrypted passwords in version control**; consider using a secrets management tool or encrypting sensitive parts of the Kickstart file.

---

## 8. Quick Reference Table

| Task | Command |
|------|---------|
| Download RHEL ISO (with subscription) | `curl -O -u user:pass https://cdn.redhat.com/.../dvd.iso` |
| Validate Kickstart syntax | `ksvalidator -v RHEL9 ks.cfg` |
| Start manual Kickstart inst. | Add `inst.ks=http://server/path/ks.cfg` to boot line |
| Generate encrypted password | `python -c 'import crypt; print(crypt.crypt("pw"))'` |
| Install `dnsmasq` for simple PXE | `sudo dnf install dnsmasq syslinux` |
| Copy kernel and initrd to TFTP root | `cp /mnt/images/pxeboot/vmlinuz initrd.img /var/lib/tftpboot/` |
| Include external Kickstart fragments | `%include http://server/part.cfg` |

---

## 9. Real‑World Scenario – Building an Automated Deployment Server

### Background

Your organization maintains a fleet of 50 identical web servers that run a custom Java application. To speed up provisioning and ensure consistency, you have been asked to build an automated deployment server. The server will:

- Host the RHEL 9 installation tree via HTTP.
- Provide a generic Kickstart file that configures the system with appropriate partitioning, security settings, and the company’s internal CA certificate.
- Offer PXE booting so that new hardware can be installed without any manual interaction.

Your task is to set up this deployment server on a test machine and perform a fully automatic installation of a test client (or simulate the network boot if hardware is unavailable, by verifying the PXE configuration and the accessible Kickstart).

### Step 1 – Prepare the Deployment Server

1. **Install RHEL 9 on the deployment server** (already done).  
2. **Ensure the server has a static IP** (e.g., `192.168.100.1/24`) on the network that will serve the clients.  
3. **Install required packages:**
   ```bash
   sudo dnf install httpd dnsmasq syslinux pykickstart -y
   sudo systemctl enable --now httpd
   sudo firewall-cmd --add-service={http,dhcp,tftp} --permanent
   sudo firewall-cmd --reload
   ```

### Step 2 – Set Up the Installation Tree

1. **Mount the RHEL 9 DVD ISO** and copy its contents:
   ```bash
   sudo mkdir -p /var/www/html/rhel9
   sudo mount -o loop /var/tmp/rhel9-x86_64-dvd.iso /mnt
   sudo cp -a /mnt/* /var/www/html/rhel9/
   ```
2. **Verify access**: Open a browser at `http://192.168.100.1/rhel9/` and check that the directory listing appears.

### Step 3 – Create the Kickstart File

Create `/var/www/html/kickstart/ks.cfg` with content similar to:

```bash
# System configuration
lang en_US.UTF-8
keyboard us
timezone America/Chicago --utc
rootpw --iscrypted $6$rounds=656000$...yourhash...
user --name=appadmin --password=$6$... --groups=wheel

# Disk setup (LVM)
clearpart --all --initlabel
autopart --type=lvm

# Network (DHCP; hostname can be templated later)
network --bootproto=dhcp --hostname=webXX.example.com

# Installation source and repos
url --url="http://192.168.100.1/rhel9/"
repo --name="appstream" --baseurl="http://192.168.100.1/rhel9/AppStream/"

# Software selection
%packages
@^minimal-environment
@web-server
java-11-openjdk
git
nfs-utils
%end

# Post-installation: add internal CA, enable services
%post
#!/bin/bash
cat > /etc/pki/ca-trust/source/anchors/internal-ca.crt << 'EOF'
-----BEGIN CERTIFICATE-----
...cert content...
-----END CERTIFICATE-----
EOF
update-ca-trust
systemctl enable httpd
%end

reboot
```

**Important**: Generate the hashed passwords with `python -c 'import crypt; print(crypt.crypt("desired_password", crypt.METHOD_SHA512))'`.

### Step 4 – Validate the Kickstart File

```bash
ksvalidator -v RHEL9 /var/www/html/kickstart/ks.cfg
```

### Step 5 – Configure the PXE Environment (dnsmasq)

1. **Edit `/etc/dnsmasq.conf`** (or create a separate config):
   ```ini
   interface=eth0
   dhcp-range=192.168.100.50,192.168.100.100,12h
   dhcp-boot=pxelinux.0
   enable-tftp
   tftp-root=/var/lib/tftpboot
   ```
2. **Prepare the TFTP root**:
   ```bash
   sudo mkdir -p /var/lib/tftpboot/pxelinux.cfg
   sudo cp /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot/
   sudo cp /usr/share/syslinux/ldlinux.c32 /var/lib/tftpboot/
   sudo cp /mnt/images/pxeboot/vmlinuz /var/lib/tftpboot/
   sudo cp /mnt/images/pxeboot/initrd.img /var/lib/tftpboot/
   ```
3. **Create the PXE configuration file** `/var/lib/tftpboot/pxelinux.cfg/default`:
   ```
   default linux
   timeout 1
   label linux
     kernel vmlinuz
     append initrd=initrd.img inst.ks=http://192.168.100.1/kickstart/ks.cfg
   ```
4. **Start dnsmasq**:
   ```bash
   sudo systemctl enable --now dnsmasq
   ```

### Step 6 – Test the Fully Automatic Installation

1. Connect a test client machine (or a VM with PXE boot enabled) to the same network as the deployment server.
2. Boot the client from the network (PXE).  
   - The client receives an IP address from the `dnsmasq` DHCP server.
   - It downloads `pxelinux.0`, then `vmlinuz` and `initrd.img`.
   - The kernel boots with the `inst.ks=` parameter, and Anaconda fetches the Kickstart file and installation tree from the HTTP server.
3. The installation proceeds without any user intervention and reboots into a fully configured system.

### Step 7 – Post‑Deployment Verification

After the client reboots, log in as `appadmin` and verify:

- The internal CA certificate is trusted.
- Required packages (`httpd`, `java-11-openjdk`) are installed.
- The system hostname follows the expected pattern (can be later refined with a `%pre` script that reads a MAC address mapping).

### Cleaning Up

To reset the test environment, you can stop `dnsmasq` and remove the files from `/var/lib/tftpboot/`. The next deployment only requires restarting the services.

---

## 10. Practice Lab

1. **Create a minimal Kickstart file** that installs a RHEL 9 system with a static IP, a minimal package set, and a custom post‑installation script that creates a welcome file in `/root/`. Validate it.
2. **Set up an Apache server** on a VM, serve your Kickstart file, and manually start an installation using the `inst.ks=` boot parameter on another VM.
3. **Implement a simple PXE server** using `dnsmasq` (or separately `dhcp` and `tftp-server`) and test booting a client.
4. **Troubleshoot a Kickstart failure**: deliberately introduce an error into the disk setup, boot, and examine the logs via the installer’s virtual terminals.
5. **Use `%include`** to split your Kickstart into a base file and a network‑specific fragment.

---

**Date documented:** 2026-05-04  
**Sources:** Red Hat Enterprise Linux 9 Installation Guide, Kickstart documentation, `pykickstart` man page, `dnsmasq` documentation

---

