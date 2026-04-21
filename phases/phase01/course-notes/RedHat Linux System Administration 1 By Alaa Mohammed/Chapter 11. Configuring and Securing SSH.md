
# Chapter 11: Configuring and Securing SSH

## 1. What is SSH?

**SSH (Secure Shell)** is a cryptographic network protocol used to securely access and manage remote systems over an unsecured network. It provides:

- Remote command‑line access (`ssh`)
- Secure file transfer (`scp`, `sftp`)
- All communication is encrypted, protecting against eavesdropping and man‑in‑the‑middle attacks.

---

## 2. Authentication Methods

### 2.1 Symmetric Encryption

- Same key encrypts and decrypts data.
- Used *during* the SSH session (after key exchange) to encrypt the channel.
- Example algorithms: AES, ChaCha20.

### 2.2 Asymmetric Encryption (Public‑Key Authentication)

- Uses a **key pair**: private key (kept secret) and public key (shared).
- The server stores the public key in `~/.ssh/authorized_keys`.
- During login, the server challenges the client to prove possession of the private key without revealing it.

---

## 3. SSH Protocol Phases

| Phase | Description |
|-------|-------------|
| **TCP handshake** | Client connects to server on port 22. |
| **Version exchange** | Both sides identify SSH protocol version (SSH‑2 only today). |
| **Key exchange** | Diffie‑Hellman establishes a shared session key. |
| **Encryption negotiation** | Client and server agree on ciphers, MAC, compression. |
| **Server authentication** | Client verifies server's host key (first connection prompts for fingerprint). |
| **Client authentication** | Client proves identity (password or public‑key). |
| **Session establishment** | Secure channel opens; shell or command executes. |

---

## 4. SSH Key Pair Algorithms

| Algorithm | Command | Key Size | Recommended |
|-----------|---------|----------|-------------|
| **Ed25519** | `ssh-keygen -t ed25519` | 256 bits | **Yes** – strongest and fastest. |
| **RSA** | `ssh-keygen -t rsa -b 4096` | 4096 bits | Good, widely compatible. |
| **ECDSA** | `ssh-keygen -t ecdsa -b 256` | 256/384/521 | Acceptable. |
| **DSA** | `ssh-keygen -t dsa` | 1024 | **Avoid** – deprecated and weak. |

**Best practice:** Use Ed25519 unless you need compatibility with very old systems.

---

## 5. SSH File Locations

### On the Client

| File/Directory | Purpose | Permissions |
|----------------|---------|-------------|
| `~/.ssh/id_ed25519` | Private key | `600` (strict) |
| `~/.ssh/id_ed25519.pub` | Public key (share with servers) | `644` |
| `~/.ssh/known_hosts` | Stores trusted server host keys | `644` |
| `~/.ssh/config` | Per‑user client configuration | `600` or `644` |
| `~/.ssh/authorized_keys` | (Rarely on client; usually on server) | `600` |

### On the Server (CentOS)

| File/Directory | Purpose |
|----------------|---------|
| `/etc/ssh/sshd_config` | SSH daemon configuration (server settings) |
| `~/.ssh/authorized_keys` | List of public keys allowed to log in as that user |
| `/etc/ssh/ssh_host_*_key` | Server’s private host keys (Ed25519, RSA, etc.) |
| `/etc/ssh/ssh_host_*_key.pub` | Server’s public host keys |
| `/etc/issue.net` | Optional banner file displayed before authentication |
| `/var/log/secure` | Authentication log file (CentOS/RHEL) |

---

## 6. Server Configuration – `/etc/ssh/sshd_config`

Key directives for a secure SSH server on CentOS.

| Directive | Recommended Value | Explanation |
|-----------|-------------------|-------------|
| `PermitRootLogin` | `no` | Disable direct root login via SSH. |
| `PasswordAuthentication` | `no` | Force key‑based authentication only. |
| `PubkeyAuthentication` | `yes` | Enable public key login. |
| `ChallengeResponseAuthentication` | `no` | Disable keyboard‑interactive (often used for passwords). |
| `MaxAuthTries` | `3` | Limit failed attempts per connection. |
| `ClientAliveInterval` | `300` | Send keepalive every 5 minutes. |
| `ClientAliveCountMax` | `2` | Disconnect after 2 missed keepalives (10 minutes idle). |
| `Banner` | `/etc/issue.net` | Display a warning banner before authentication. |
| `LogLevel` | `VERBOSE` | Log authentication successes and failures. |

**Example secure configuration snippet:**

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no

MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

Banner /etc/issue.net
LogLevel VERBOSE
```

**Apply changes:**
```bash
sudo systemctl reload sshd
```

---

## 7. Client Configuration – `~/.ssh/config`

Per‑user client configuration simplifies repeated connections.

**Syntax:**
```
Host alias
    HostName real-hostname-or-ip
    User username
    Port port
    IdentityFile ~/.ssh/special-key
    ServerAliveInterval 60
    Compression yes
    IdentitiesOnly yes
```

**Example `~/.ssh/config`:**
```
Host server1
    HostName 192.168.1.100
    User john
    IdentityFile ~/.ssh/id_ed25519_server1
    IdentitiesOnly yes
    ServerAliveInterval 60
```

Now connect with: `ssh server1`

---

## 8. SSH Commands Reference

### 8.1 `ssh` – Remote Login

| Option | Meaning |
|--------|---------|
| `-p port` | Specify port (default 22) |
| `-i identity_file` | Use a specific private key |
| `-v` / `-vvv` | Verbose output for debugging |
| `user@host command` | Execute a command remotely |

**Examples:**
```bash
ssh john@192.168.1.100
ssh -p 2222 -i ~/.ssh/mykey bob@server.example.com
ssh server1 "df -h"
ssh -vvv server1   # debug connection issues
```

### 8.2 `ssh-keygen` – Generate Key Pairs

| Option | Meaning |
|--------|---------|
| `-t ed25519` / `-t rsa` | Key type |
| `-b 4096` | Key length (RSA only) |
| `-C "comment"` | Add identifying comment |
| `-f filename` | Specify output file |
| `-N passphrase` | Provide passphrase (use `""` for empty) |
| `-p` | Change passphrase of existing key |
| `-l` | Show fingerprint of public key |
| `-y` | Read private key and output public key |

**Examples:**
```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "john@client" -f ~/.ssh/id_ed25519_server1

# Generate RSA 4096 key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mykey

# Show fingerprint
ssh-keygen -l -f ~/.ssh/id_ed25519_server1.pub

# Change passphrase
ssh-keygen -p -f ~/.ssh/id_ed25519_server1

# Extract public key from private key
ssh-keygen -y -f ~/.ssh/id_ed25519_server1 > recovered.pub
```

### 8.3 `ssh-copy-id` – Deploy Public Key to Server

**Syntax:** `ssh-copy-id [-i identity_file] [user@]host`

**Example:**
```bash
ssh-copy-id -i ~/.ssh/id_ed25519_server1.pub john@192.168.1.100
```

This appends the public key to `~/.ssh/authorized_keys` on the server and sets correct permissions.

### 8.4 `ssh-agent` – Cache Passphrases

`ssh-agent` holds decrypted private keys in memory so you don't have to re‑enter passphrases.

```bash
eval $(ssh-agent)                 # start agent
ssh-add ~/.ssh/id_ed25519_server1 # add key (prompts for passphrase once)
ssh server1                       # no passphrase prompt
```

**Other agent commands:**
| Command | Action |
|---------|--------|
| `ssh-add -l` | List loaded keys |
| `ssh-add -D` | Remove all keys |
| `ssh-agent -k` | Kill the agent |

### 8.5 `scp` – Secure Copy

```bash
# Copy local file to remote
scp file.txt server1:/home/john/

# Copy remote file to local
scp server1:/var/log/messages ./logs/

# Copy entire directory recursively
scp -r myproject/ server1:/home/john/
```

### 8.6 `sftp` – Secure FTP Interactive Session

```bash
sftp server1
sftp> ls
sftp> get remote_file
sftp> put local_file
sftp> exit
```

---

## 9. Troubleshooting SSH

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| `Connection refused` | sshd not running or firewall blocking | `sudo systemctl status sshd`; `sudo firewall-cmd --list-all` (CentOS) |
| `Permission denied (publickey)` | Wrong key, permissions, or not in `authorized_keys` | Client: `ssh -vvv server1`; Server: `sudo tail /var/log/secure`; verify `~/.ssh` (700) and `authorized_keys` (600) |
| `Host key verification failed` | Server reinstalled or IP reused | `ssh-keygen -R hostname_or_ip` then reconnect |
| `Too many authentication failures` | Client offers too many keys | Use `IdentitiesOnly yes` and `IdentityFile` in config, or `ssh -i key -o IdentitiesOnly=yes` |
| Banner not showing | `Banner` directive missing or file not readable | Ensure `Banner /etc/issue.net` and file exists with correct permissions |

---

## 10. Complete CentOS SSH Hardening Scenario

This scenario covers **every SSH file** on both client and server, following a logical step‑by‑step workflow. It assumes a CentOS server and a Linux client.

### Environment

- **Server:** CentOS 7/8/9, hostname `server1`, IP `192.168.1.100` (adjust as needed).
- **Client:** Any Linux distribution with OpenSSH client.
- **Server user:** `john` (regular user with sudo privileges).

### Step 1: Initial Server State Verification

On the server, verify SSH is running and the firewall allows port 22.

```bash
sudo systemctl status sshd
sudo firewall-cmd --list-all
```

If port 22 is not allowed, add it:
```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### Step 2: Create a Regular User on the Server

```bash
sudo useradd -m -s /bin/bash john
sudo passwd john
```

Optionally grant sudo access:
```bash
sudo usermod -aG wheel john   # 'wheel' group grants sudo on CentOS
```

### Step 3: Generate SSH Key Pair on the Client

On your client machine:

```bash
ssh-keygen -t ed25519 -C "john@client-for-server1" -f ~/.ssh/id_ed25519_server1
```

**Files created:**
- `~/.ssh/id_ed25519_server1` (private key, permissions `600`)
- `~/.ssh/id_ed25519_server1.pub` (public key)

### Step 4: Copy Public Key to the Server

Use `ssh-copy-id` to install the public key on the server for user `john`.

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_server1.pub john@192.168.1.100
```

You will be prompted for `john`'s password once.

**What happens on the server:**
- `~/.ssh/` directory is created with permissions `700`.
- `~/.ssh/authorized_keys` is created (or appended) with the public key, permissions `600`.

**Verify on the server:**
```bash
ls -la /home/john/.ssh/
cat /home/john/.ssh/authorized_keys
```

### Step 5: Test Key‑Based Login

From the client:

```bash
ssh -i ~/.ssh/id_ed25519_server1 john@192.168.1.100
```

Enter the key's passphrase if you set one. You should be logged in without `john`'s password.

**Note:** The first connection will prompt you to accept the server's host key fingerprint. Type `yes`. This adds the server's public host key to `~/.ssh/known_hosts` on the client.

### Step 6: Harden SSH Server Configuration

On the server, edit `/etc/ssh/sshd_config` with `sudo`.

```bash
sudo vi /etc/ssh/sshd_config
```

Set the following directives (uncomment or add as needed):

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no

MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

Banner /etc/issue.net
LogLevel VERBOSE
```

**Create the banner file:**

```bash
sudo tee /etc/issue.net <<EOF
*****************************************************************
*  WARNING: This system is for authorized users only.            *
*  All activities are monitored and logged.                      *
*  Unauthorized access is prohibited and will be prosecuted.     *
*****************************************************************
EOF
```

**Test the configuration syntax:**

```bash
sudo sshd -t
```

If no errors, reload the SSH daemon:

```bash
sudo systemctl reload sshd
```

### Step 7: Verify Hardening

Open a **new terminal** on the client (keep the old session open as a fallback) and test:

1. **Successful key login:**
   ```bash
   ssh -i ~/.ssh/id_ed25519_server1 john@192.168.1.100
   ```
   The banner should appear, then you are logged in.

2. **Password authentication rejected:**
   ```bash
   ssh -o PreferredAuthentications=password john@192.168.1.100
   ```
   Expected: `Permission denied (publickey).`

3. **Root login rejected:**
   ```bash
   ssh root@192.168.1.100
   ```
   Should fail even if you had a key.

4. **Examine authentication logs:**
   On the server:
   ```bash
   sudo tail -20 /var/log/secure
   ```
   Look for `Accepted publickey for john` and `Failed password`.

### Step 8: Configure Client Alias (`~/.ssh/config`)

On the client, create or edit `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Add:

```
Host server1
    HostName 192.168.1.100
    User john
    IdentityFile ~/.ssh/id_ed25519_server1
    IdentitiesOnly yes
    ServerAliveInterval 60
    Compression yes
```

Now connect simply with:

```bash
ssh server1
```

### Step 9: Use `ssh-agent` for Convenience

If your key has a passphrase, use `ssh-agent` to cache it.

```bash
eval $(ssh-agent)
ssh-add ~/.ssh/id_ed25519_server1
```

Enter the passphrase once. Now `ssh server1` will not prompt for the passphrase.

**Verify loaded keys:**
```bash
ssh-add -l
```

### Step 10: Manage `known_hosts` – Server Host Key Verification

The client's `~/.ssh/known_hosts` file contains the server's public host key. To view it:

```bash
cat ~/.ssh/known_hosts
```

**To verify the server's host key fingerprint manually:**
On the server:
```bash
ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
```

**To remove an old host key (e.g., after reinstalling the server):**
```bash
ssh-keygen -R 192.168.1.100
```

### Step 11: File Transfer Using the Alias

With the alias configured, `scp` and `sftp` also use the settings.

```bash
scp myfile.txt server1:/home/john/
sftp server1
```

### Step 12: Final Verification Checklist

- [ ] Password authentication is disabled; only key works.
- [ ] Root login is disabled.
- [ ] Banner appears before authentication.
- [ ] Client alias `server1` works.
- [ ] `ssh-agent` caches the key.
- [ ] `known_hosts` contains the server's host key.
- [ ] `scp` and `sftp` function correctly.
- [ ] `/var/log/secure` shows successful key authentications.

---

## 11. Practice Lab – Apply the Scenario

Using a CentOS virtual machine (or any Linux VM) and your local client, complete the following tasks:

1. Generate an Ed25519 key pair named `labkey`.
2. Create a user `devops` on the server and set a password.
3. Deploy the public key to `devops` using `ssh-copy-id`.
4. Modify `/etc/ssh/sshd_config` to:
   - Disable password authentication.
   - Disable root login.
   - Set `MaxAuthTries` to `2`.
   - Add a banner.
5. Reload sshd and verify you can still connect with the key.
6. Test that a user without a key cannot connect using a password.
7. Configure a client alias `lab` for this server in `~/.ssh/config`.
8. Start `ssh-agent`, add your key, and connect without a passphrase prompt.
9. Simulate a host key change: delete the server from `known_hosts` (`ssh-keygen -R`) and reconnect.
10. Check `/var/log/secure` to confirm successful and failed attempts.

---

## 12. Quick Reference Cheat Sheet

| Task | Command |
|------|---------|
| Generate Ed25519 key | `ssh-keygen -t ed25519 -C "comment" -f ~/.ssh/keyname` |
| Copy public key to server | `ssh-copy-id -i ~/.ssh/keyname.pub user@host` |
| Start agent and add key | `eval $(ssh-agent); ssh-add ~/.ssh/keyname` |
| Connect using alias | `ssh alias` (after configuring `~/.ssh/config`) |
| Test sshd configuration | `sudo sshd -t` |
| Reload sshd | `sudo systemctl reload sshd` |
| View SSH logs (CentOS) | `sudo tail -f /var/log/secure` |
| Remove old host key | `ssh-keygen -R hostname_or_ip` |
| Debug SSH connection | `ssh -vvv user@host` |
| List loaded keys in agent | `ssh-add -l` |
| Secure copy file | `scp file.txt alias:/path/` |
| Secure FTP session | `sftp alias` |

---

**Date documented:** 2026-04-21  
**Sources:** OpenSSH documentation, Red Hat System Administration, man pages

---
