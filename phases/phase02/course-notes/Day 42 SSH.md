# Day 42. SSH (Secure Shell)

## Table of Contents

- [Day 42. SSH (Secure Shell)](#day-42-ssh-secure-shell)
  - [Table of Contents](#table-of-contents)
  - [1. What is SSH? Why Do We Need It?](#1-what-is-ssh-why-do-we-need-it)
  - [2. SSH Architecture – Client‑Server Model](#2-ssh-architecture--clientserver-model)
  - [3. SSH Authentication Methods](#3-ssh-authentication-methods)
    - [3.1 Password Authentication](#31-password-authentication)
    - [3.2 Public Key Authentication (Recommended)](#32-public-key-authentication-recommended)
    - [3.3 Host‑Based Authentication](#33-hostbased-authentication)
  - [4. SSH Key Management](#4-ssh-key-management)
    - [4.1 Generating SSH Keys (`ssh-keygen`)](#41-generating-ssh-keys-ssh-keygen)
    - [4.2 Copying Public Keys (`ssh-copy-id`)](#42-copying-public-keys-ssh-copy-id)
    - [4.3 Managing Multiple Keys](#43-managing-multiple-keys)
  - [5. Essential SSH Commands](#5-essential-ssh-commands)
    - [5.1 `ssh` – Remote Login](#51-ssh--remote-login)
    - [5.2 `scp` – Secure Copy](#52-scp--secure-copy)
    - [5.3 `sftp` – Secure File Transfer (Interactive)](#53-sftp--secure-file-transfer-interactive)
    - [5.4 `ssh-agent` – Key Management (Single Sign‑On)](#54-ssh-agent--key-management-single-signon)
    - [5.5 `ssh-add` – Add Keys to Agent](#55-ssh-add--add-keys-to-agent)
  - [6. SSH Configuration Files](#6-ssh-configuration-files)
    - [6.1 Client Configuration (`~/.ssh/config`)](#61-client-configuration-sshconfig)
    - [6.2 Server Configuration (`/etc/ssh/sshd_config`)](#62-server-configuration-etcsshsshd_config)
  - [7. SSH Port Forwarding (Tunneling)](#7-ssh-port-forwarding-tunneling)
    - [7.1 Local Port Forwarding](#71-local-port-forwarding)
    - [7.2 Remote Port Forwarding](#72-remote-port-forwarding)
    - [7.3 Dynamic Port Forwarding (SOCKS Proxy)](#73-dynamic-port-forwarding-socks-proxy)
  - [8. SSH Security Hardening](#8-ssh-security-hardening)
  - [9. SSH Troubleshooting](#9-ssh-troubleshooting)
  - [10. SSH in Cloud Engineering](#10-ssh-in-cloud-engineering)
  - [11. Quick Reference Table](#11-quick-reference-table)
  - [12. Practice Lab – Verify Your Understanding](#12-practice-lab--verify-your-understanding)

---

## 1. What is SSH? Why Do We Need It?

**SSH (Secure Shell)** is a cryptographic network protocol used to securely access and manage remote systems over an unsecured network. It provides:

- **Secure remote command‑line access** (`ssh`).
- **Secure file transfer** (`scp`, `sftp`).
- **Port forwarding / tunneling** (encrypted tunnels).
- **X11 forwarding** (run GUI apps remotely).

**Analogy:** SSH is like a secure, encrypted tunnel from your computer to a remote server. Everything you send through the tunnel is scrambled so that even if intercepted, it cannot be read.

**Why SSH matters for cloud engineers:**
- You will use SSH **daily** to manage EC2 instances, containers, VMs, and on‑prem servers.
- SSH is the primary way to access Linux servers securely.
- Many cloud services (AWS Systems Manager, Azure Bastion) are built on SSH.

**Key point:** SSH uses **strong encryption** and **public key cryptography** to protect against eavesdropping, connection hijacking, and man‑in‑the‑middle attacks.

---

## 2. SSH Architecture – Client‑Server Model

SSH follows a **client‑server** model:

- **SSH Client** – the tool you use to connect (e.g., `ssh`, `scp`, `sftp`, `ssh-agent`).
- **SSH Server** – the daemon (`sshd`) running on the remote machine, listening on port **22** (default).

**SSH Connection Phases:**

| Phase | Description |
|-------|-------------|
| **1. TCP Handshake** | Client connects to server on port 22. |
| **2. Protocol Version Exchange** | Both sides agree on SSH protocol version (SSH‑2 only today). |
| **3. Key Exchange** | Diffie‑Hellman (or similar) establishes a shared session key. |
| **4. Encryption Negotiation** | Client and server agree on encryption, MAC, compression algorithms. |
| **5. Server Authentication** | Client verifies the server's host key (first connection prompts for fingerprint). |
| **6. Client Authentication** | Client proves its identity (password or public key). |
| **7. Session Establishment** | A secure channel is opened; shell or command is executed. |

---

## 3. SSH Authentication Methods

### 3.1 Password Authentication

- User provides a password when prompted.
- **Weakness:** Passwords can be guessed or brute‑forced.
- **Default:** Enabled (but should be disabled for public‑facing servers).

**Example:**
```bash
ssh alice@server.example.com
# Prompt for password
```

### 3.2 Public Key Authentication (Recommended)

- Uses a **key pair**: private key (kept secret) and public key (copied to the server).
- Server challenges the client to prove possession of the private key.
- **Advantages:** No password transmitted; can be used with `ssh-agent` for password‑less logins.

**How it works:**
1. Client generates a key pair (`ssh-keygen`).
2. Client copies the public key to `~/.ssh/authorized_keys` on the server (`ssh-copy-id`).
3. When connecting, the server sends a challenge encrypted with the public key.
4. Client decrypts the challenge with the private key and returns it.
5. Server verifies the response → access granted.

### 3.3 Host‑Based Authentication

- Relies on the client's host key.
- Rarely used in modern environments – less secure than public key.

---

## 4. SSH Key Management

### 4.1 Generating SSH Keys (`ssh-keygen`)

**Syntax:** `ssh-keygen [options]`

| Option | Meaning | Example |
|--------|---------|---------|
| `-t rsa` | RSA key type | `-t rsa -b 4096` |
| `-t ed25519` | Ed25519 (recommended) | `-t ed25519` |
| `-b bits` | Key length (RSA only) | `-b 4096` |
| `-C "comment"` | Add a comment (e.g., email) | `-C "alice@example.com"` |
| `-f file` | Output file name | `-f ~/.ssh/mykey` |
| `-N passphrase` | Set a passphrase (or `""` for empty) | `-N "secret"` |

**Examples:**

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "alice@cloud-journey"

# Generate RSA 4096 key
ssh-keygen -t rsa -b 4096 -C "bob@example.com"

# Generate with specific filename and no passphrase
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N ""
```

**Key files:**
- **Private key:** `~/.ssh/id_ed25519` (keep secret, `600` permissions).
- **Public key:** `~/.ssh/id_ed25519.pub` (copy to servers).

### 4.2 Copying Public Keys (`ssh-copy-id`)

Automatically copies your public key to the remote server's `~/.ssh/authorized_keys`.

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@server.example.com
```

If you don't specify `-i`, it uses the default keys.

### 4.3 Managing Multiple Keys

- You can have multiple key pairs (e.g., one for personal, one for work, one for GitHub).
- Use the `-i` option to specify which key to use:
  ```bash
  ssh -i ~/.ssh/work_key alice@work-server.com
  ```
- Use `~/.ssh/config` to specify keys per host (see section 6.1).

---

## 5. Essential SSH Commands

### 5.1 `ssh` – Remote Login

**Syntax:** `ssh [options] [user@]host [command]`

| Option | Meaning | Example |
|--------|---------|---------|
| `-p port` | Specify port (default 22) | `-p 2222` |
| `-i identity_file` | Use specific private key | `-i ~/.ssh/mykey` |
| `-l user` | Login as user | `-l alice` |
| `-v` (verbose) | Debug connection | `-vvv` for more |
| `-N` | Do not execute remote command | For port forwarding |
| `-X` | Forward X11 (GUI apps) | `-X` |
| `-A` | Forward authentication agent | `-A` |

**Examples:**
```bash
# Basic connection
ssh alice@192.168.1.10

# Custom port and key
ssh -p 2222 -i ~/.ssh/mykey bob@server.example.com

# Run a command without interactive shell
ssh alice@webserver "ls -la /var/log"

# Verbose debugging
ssh -vvv user@host
```

### 5.2 `scp` – Secure Copy

Copies files securely between hosts.

**Syntax:** `scp [options] source destination`

| Option | Meaning | Example |
|--------|---------|---------|
| `-r` | Recursive (copy directories) | `-r` |
| `-P port` | Specify SSH port | `-P 2222` |
| `-i key` | Use specific private key | `-i ~/.ssh/mykey` |
| `-p` | Preserve timestamps/permissions | `-p` |
| `-C` | Enable compression | `-C` |

**Examples:**
```bash
# Copy local file to remote
scp file.txt alice@server:/home/alice/

# Copy remote file to local
scp alice@server:/remote/file.txt .

# Copy directory recursively
scp -r myfolder/ alice@server:/backups/

# Copy with custom port
scp -P 2222 -i ~/.ssh/mykey data.bin user@server:~
```

### 5.3 `sftp` – Secure File Transfer (Interactive)

Interactive file transfer session over SSH.

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

**Example:**
```bash
sftp alice@server
sftp> cd /var/log
sftp> get messages
sftp> put localfile.txt
sftp> exit
```

### 5.4 `ssh-agent` – Key Management (Single Sign‑On)

`ssh-agent` holds decrypted private keys in memory so you don't have to enter passphrases repeatedly.

**Start agent and add key:**
```bash
eval $(ssh-agent)          # start agent in background
ssh-add ~/.ssh/id_ed25519  # add key (prompts for passphrase once)
```

Now any `ssh` connection in that shell will use the agent.

**Common `ssh-agent` commands:**

| Command | Purpose |
|---------|---------|
| `ssh-add -l` | List loaded keys |
| `ssh-add -D` | Delete all keys |
| `ssh-add -d key` | Delete a specific key |
| `ssh-agent -k` | Stop the agent |

**Forward agent to remote host:** `ssh -A user@host` – allows remote server to use your local keys (use with caution).

### 5.5 `ssh-add` – Add Keys to Agent

```bash
ssh-add ~/.ssh/id_ed25519
ssh-add -t 3600 ~/.ssh/id_rsa   # add with 1-hour timeout
```

---

## 6. SSH Configuration Files

### 6.1 Client Configuration (`~/.ssh/config`)

Per‑user client configuration simplifies repeated connections.

**Syntax:**
```
Host alias
    HostName real-hostname
    User username
    Port port
    IdentityFile ~/.ssh/special-key
    ForwardAgent yes/no
    Compression yes
```

**Example `~/.ssh/config`:**
```
Host prod
    HostName 192.168.1.100
    User deploy
    Port 2222
    IdentityFile ~/.ssh/deploy_key

Host dev
    HostName dev.internal.com
    User myuser
    ForwardAgent yes

Host *
    ServerAliveInterval 60
    Compression yes
```

Now you can connect simply as `ssh prod` or `ssh dev`.

### 6.2 Server Configuration (`/etc/ssh/sshd_config`)

The SSH daemon configuration file. Key directives:

| Directive | Recommended Value | Explanation |
|-----------|-------------------|-------------|
| `Port` | `22` (or change) | Listening port. |
| `PermitRootLogin` | `prohibit-password` or `no` | Never allow root with password. |
| `PasswordAuthentication` | `no` | Force key‑based authentication. |
| `PubkeyAuthentication` | `yes` | Enable public key login. |
| `ChallengeResponseAuthentication` | `no` | Disable less secure methods. |
| `AllowUsers` | `alice bob` | Restrict which users can SSH in. |
| `DenyUsers` | `baduser` | Explicitly block users. |
| `AllowGroups` | `sshusers` | Only users in this group can log in. |
| `MaxAuthTries` | `3` | Limit failed attempts. |
| `ClientAliveInterval` | `300` | Send keepalive every 5 minutes. |
| `ClientAliveCountMax` | `2` | Disconnect after 10 minutes of no response. |
| `Banner` | `/etc/issue.net` | Display a warning banner before login. |
| `LogLevel` | `VERBOSE` | Log authentication successes and failures. |
| `Protocol` | `2` | Only SSH‑2 (SSH‑1 is insecure). |

After editing `sshd_config`, reload:
```bash
sudo systemctl reload sshd
```

---

## 7. SSH Port Forwarding (Tunneling)

SSH can forward network traffic through an encrypted tunnel.

### 7.1 Local Port Forwarding

Forwards traffic from a local port to a remote destination.

**Syntax:** `ssh -L local_port:destination_host:destination_port user@ssh_server`

**Example:** Forward local port `8080` to `remote_server:80` via `jump_host`.

```bash
ssh -L 8080:remote_server:80 user@jump_host
```

Now `http://localhost:8080` is securely tunneled to `remote_server:80`.

### 7.2 Remote Port Forwarding

Forwards traffic from a remote port to a local destination.

**Syntax:** `ssh -R remote_port:local_host:local_port user@ssh_server`

**Example:** Expose a local web server on port `8000` to the remote server's port `9000`.

```bash
ssh -R 9000:localhost:8000 user@remote_server
```

Now anyone accessing `remote_server:9000` sees the local server.

### 7.3 Dynamic Port Forwarding (SOCKS Proxy)

Creates a SOCKS proxy that forwards traffic through the SSH server.

**Syntax:** `ssh -D local_port user@ssh_server`

**Example:** Open a SOCKS proxy on `localhost:1080`.

```bash
ssh -D 1080 user@ssh_server
```

Configure your browser to use `localhost:1080` as a SOCKS proxy.

---

## 8. SSH Security Hardening

| Action | Configuration / Command |
|--------|-------------------------|
| Disable root login | `PermitRootLogin no` |
| Disable password auth | `PasswordAuthentication no` |
| Use key‑only auth | `PubkeyAuthentication yes` |
| Limit users | `AllowUsers alice bob` |
| Limit groups | `AllowGroups sshusers` |
| Change port (optional) | `Port 2222` (update firewall) |
| Set max auth tries | `MaxAuthTries 3` |
| Idle timeout | `ClientAliveInterval 300` & `ClientAliveCountMax 2` |
| Disable empty passwords | `PermitEmptyPasswords no` |
| Disable .rhosts (obsolete) | `IgnoreRhosts yes` |
| Disable host‑based auth | `HostbasedAuthentication no` |
| Use `fail2ban` | Blocks repeated failed attempts |

After changes: `sudo systemctl reload sshd`

---

## 9. SSH Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| **Connection refused** | Server not running / firewall | Check `systemctl status sshd`, `sudo ufw allow 22`, `netstat -tlnp \| grep :22` |
| **Permission denied (publickey)** | Wrong key, `authorized_keys` missing | Verify client key (`ssh -v`), check server `~/.ssh/authorized_keys`, permissions `700` for `.ssh`, `600` for `authorized_keys`. |
| **Permission denied (password)** | Password auth disabled | Enable password temporarily, or use key. |
| **Host key verification failed** | Server host key changed | Remove old entry: `ssh-keygen -R hostname`, then reconnect. |
| **Too many authentication failures** | Client offers too many keys | Force specific key: `ssh -i ~/.ssh/correct_key`, or set `IdentitiesOnly yes` in `~/.ssh/config`. |
| **Agent refused operation** | `ssh-agent` not running or key not added | Start agent: `eval $(ssh-agent)`, add key: `ssh-add`. |

---

## 10. SSH in Cloud Engineering

| Cloud Service | SSH Use Case |
|---------------|--------------|
| **AWS EC2** | Default key pair for login. Store private key locally; use `ssh -i key.pem ec2-user@ip`. |
| **Azure VM** | Use SSH keys for Linux VMs. Azure generates a key pair or you can upload your own. |
| **GCP Compute Engine** | SSH keys stored in project metadata. Use `gcloud compute ssh` or standard `ssh`. |
| **AWS Systems Manager Session Manager** | SSH‑like access without opening port 22 (no public IP needed). |
| **Azure Bastion** | Managed SSH/RDP gateway (no public IP on VMs). |
| **GitHub / GitLab** | SSH keys for `git clone`, `push`. |

**Cloud best practices:**
- Never store private keys in repos or S3 buckets.
- Use **SSH Agent Forwarding** sparingly (risky).
- Use **AWS EC2 Instance Connect** or **Session Manager** for temporary access without managing keys.
- Rotate keys periodically.

---

## 11. Quick Reference Table

| Task | Command / Configuration |
|------|--------------------------|
| Generate Ed25519 key | `ssh-keygen -t ed25519 -C "comment"` |
| Copy public key to server | `ssh-copy-id user@host` |
| Connect to server | `ssh user@host` |
| Connect with custom port/key | `ssh -p 2222 -i ~/.ssh/mykey user@host` |
| Copy file (scp) | `scp file.txt user@host:/path/` |
| Interactive file transfer | `sftp user@host` |
| Add key to agent | `ssh-add ~/.ssh/id_ed25519` |
| Local port forwarding | `ssh -L 8080:dest:80 user@host` |
| Remote port forwarding | `ssh -R 9000:localhost:8000 user@host` |
| Client config file | `~/.ssh/config` |
| Server config file | `/etc/ssh/sshd_config` |
| Check SSH version | `ssh -V` |
| Debug connection | `ssh -vvv user@host` |
| Remove host key | `ssh-keygen -R hostname` |

---

## 12. Practice Lab – Verify Your Understanding

1. **Generate a new SSH key:**
   - Generate an Ed25519 key with your email as comment.
   - List the files created (`~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`).

2. **Copy your public key to a remote server:**
   - Use `ssh-copy-id` to copy your key to a test server (or localhost if you have SSH enabled).

3. **Test key‑based login:**
   - Connect using `ssh user@host` – you should not be prompted for a password.

4. **Use `ssh-agent`:**
   - Start the agent, add your key, and verify it's loaded (`ssh-add -l`).
   - Connect to the server again – still no password.

5. **Client configuration:**
   - Create a `~/.ssh/config` entry for your test server with a custom alias.

6. **File transfer:**
   - Use `scp` to copy a file from your local machine to the server.
   - Use `sftp` to browse and download a file from the server.

7. **Port forwarding:**
   - Set up local port forwarding to access a remote service (e.g., `localhost:8888` → `server:80`).

8. **Server hardening (simulate):**
   - Edit `/etc/ssh/sshd_config` to disable root login and password authentication.
   - Reload and test.

---

**Date documented:** 2026-06-16  
**Sources:** OpenSSH documentation, RFC 4253 (SSH), cloud provider documentation

---