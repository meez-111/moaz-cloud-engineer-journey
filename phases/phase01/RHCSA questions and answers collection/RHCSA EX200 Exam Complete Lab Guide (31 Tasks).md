
## Table of Contents

**Node 1 (servera.lab.example.com)**  
1. Network Configuration  
2. Configure Repositories  
3. HTTP Content on Port 82  
4. Users and Groups  
5. Collaborative Directory  
6. AutoFS (NFS Auto‑mount)  
7. Crontab  
8. ACLs on `/var/tmp/fstab`  
9. NTP Client (Chrony)  
10. Find and Copy Large Files  
11. User with Specific UID  
12. Create a Tar Archive  
13. Umask for User `natasha`  
14. Password Expiration for New Users  
15. Sudo Without Password for Group `admin`  
16. Script: `gofind.sh`  
17. Script: `check_auth.sh`  
18. Flatpak (Two Methods: `flatpak remote-add` + `.flatpakrepo` file)

**Node 2 (serverb.lab.example.com)**  
19. Reset Root Password (Two Methods: `rd.break` and `init=/bin/bash`)  
20. Create a Swap Partition  
21. LVM Logical Volume `database`  
22. VDO Volume (LVM‑integrated)  
23. Extend a Logical Volume  
24. Tuned Profile  
25. Container as a Service (Old Systemd + New Quadlet)  
26. Run a Script Inside an Existing Container  
27. Build a Container Image from a Dockerfile  
28. Systemd Timer (Run Every 3 Minutes)  
29. Restricted User (rachel) – Only `passwd` Command  
30. Find a Specific String in a File  
31. Download a Dockerfile from a Remote Server and Build

---

# Node 1 (servera.lab.example.com)

## 1. Network Configuration

**Solution:**
```bash
hostnamectl set-hostname servera.lab.example.com
nmcli connection modify "System eth0" ipv4.addresses 192.168.1.150/24 ipv4.gateway 192.168.1.1 ipv4.dns 192.168.1.100 ipv4.method static
nmcli connection up "System eth0"
```

**Verification:**
```bash
ip a | grep 192.168.1.150
ping -c3 192.168.1.1
```

---

## 2. Configure Repositories

**Solution:**
```bash
vim /etc/yum.repos.d/exam.repo
```
Paste:
```
[BaseOS]
name=BaseOS
baseurl=http://repo.lab.example.com/rocky9.5/repo/BaseOS
enabled=1
gpgcheck=0

[AppStream]
name=AppStream
baseurl=http://repo.lab.example.com/rocky9.5/repo/AppStream/
enabled=1
gpgcheck=0
```
```bash
dnf repolist
```

---

## 3. HTTP Content on Port 82

**Solution:**
```bash
dnf install httpd -y
systemctl enable --now httpd
sed -i 's/Listen 80/Listen 82/' /etc/httpd/conf/httpd.conf
systemctl restart httpd
semanage port -a -t http_port_t -p tcp 82
firewall-cmd --permanent --add-port=82/tcp
firewall-cmd --reload
```

**Verification:**
```bash
curl http://localhost:82/
```

---

## 4. Users and Groups

**Solution:**
```bash
groupadd admin
useradd -G admin harry
useradd -G admin natasha
useradd -s /sbin/nologin sarah
echo password | passwd --stdin harry
echo password | passwd --stdin natasha
echo password | passwd --stdin sarah
```

**Verification:**
```bash
groups harry
grep sarah /etc/passwd
```

---

## 5. Collaborative Directory

**Solution:**
```bash
mkdir -p /common/admin
chgrp admin /common/admin
chmod 2770 /common/admin
```

**Verification:**
```bash
ls -ld /common/admin
touch /common/admin/testfile
ls -l /common/admin/testfile
```

---

## 6. AutoFS (NFS Auto‑mount)

**Solution:**
```bash
dnf install autofs -y
systemctl enable --now autofs
echo "/automount /etc/auto.nfs --timeout=30" >> /etc/auto.master
echo "public -ro nfsserver.lab.example.com:/public" >> /etc/auto.nfs
echo "private -rw nfsserver.lab.example.com:/private" >> /etc/auto.nfs
systemctl restart autofs
```

**Verification:**
```bash
cd /automount/public && ls
cd /automount/private && ls
```

---

## 7. Crontab

**Solution:**
```bash
crontab -u harry -l 2>/dev/null | { cat; echo "30 12 * * * /bin/echo EX200"; } | crontab -u harry -
echo "natasha" >> /etc/cron.deny
```

**Verification:**
```bash
crontab -u harry -l
su - natasha -c "crontab -l" 2>&1 | head -1
```

---

## 8. ACLs on `/var/tmp/fstab`

**Solution:**
```bash
cp /etc/fstab /var/tmp/fstab
setfacl -m u:harry:rw /var/tmp/fstab
setfacl -m u:natasha:--- /var/tmp/fstab
```

**Verification:**
```bash
getfacl /var/tmp/fstab
```

---

## 9. NTP Client (Chrony)

**Solution:**
```bash
dnf install chrony -y
sed -i 's/^pool.*/server ntp.lab.example.com iburst/' /etc/chrony.conf
systemctl restart chronyd
```

**Verification:**
```bash
chronyc sources -v
```

---

## 10. Find and Copy Large Files

**Solution:**
```bash
mkdir -p /find/largefiles
find /etc -type f -size +4M -exec cp {} /find/largefiles/ \;
```

**Verification:**
```bash
ls -lh /find/largefiles/
```

---

## 11. User with Specific UID

**Solution:**
```bash
useradd -u 6969 billy
echo password | passwd --stdin billy
```

**Verification:**
```bash
id billy
```

---

## 12. Create a Tar Archive

**Solution:**
```bash
tar -czvf /root/ex200.tar.gz /var/tmp
```

**Verification:**
```bash
tar -tzvf /root/ex200.tar.gz | head -5
```

---

## 13. Umask for User `natasha`

**Solution:**
```bash
su - natasha -c "echo 'umask 0277' >> ~/.bash_profile"
```

**Verification:**
```bash
su - natasha -c "touch testfile && mkdir testdir && ls -ld testfile testdir"
```

---

## 14. Password Expiration for New Users

**Solution:**
```bash
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 20/' /etc/login.defs
```

**Verification:**
```bash
grep PASS_MAX_DAYS /etc/login.defs
```

---

## 15. Sudo Without Password for Group `admin`

**Solution:**
```bash
echo "%admin ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/admin
chmod 440 /etc/sudoers.d/admin
```

**Verification:**
```bash
visudo -c
sudo -l -U harry
```

---

## 16. Script: `gofind.sh`

**Solution:**
```bash
mkdir -p /root/find
vim /root/gofind.sh
```
Inside vim paste:
```bash
#!/bin/bash
find /usr/share -type f -size -1M -exec cp {} /root/find/ \;
```
Save and exit.
```bash
chmod +x /root/gofind.sh
/root/gofind.sh
```

**Verification:**
```bash
ls -l /root/find/
```

---

## 17. Script: `check_auth.sh`

**Solution:**
```bash
vim /usr/local/bin/check_auth.sh
```
Inside vim paste:
```bash
#!/bin/bash
if [ -z "$1" ]; then
    echo "Please provide a username"
    exit 1
fi
if id "$1" &>/dev/null; then
    echo "User found"
else
    echo "User not found"
fi
```
Save and exit.
```bash
chmod 755 /usr/local/bin/check_auth.sh
```

**Verification:**
```bash
/usr/local/bin/check_auth.sh root
/usr/local/bin/check_auth.sh nosuchuser
```

---

## 18. Flatpak (Two Methods)

### Method A – Using `flatpak remote-add` (command line)
```bash
dnf install flatpak -y
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.obsproject.Studio -y
```

### Method B – Using a `.flatpakrepo` file (exam style)
```bash
dnf install flatpak -y
mkdir -p /etc/flatpak/remotes.d
vim /etc/flatpak/remotes.d/flathub.flatpakrepo
```
Paste:
```
[Flatpak Repo]
Url=https://dl.flathub.org/repo/
Title=Flathub
Comment=Flathub repository
Description=Flatpak applications and runtimes from Flathub
GPGKey=https://dl.flathub.org/repo/flathub.gpg
```
Save and exit.
```bash
flatpak remote-modify --enable flathub
flatpak install flathub com.obsproject.Studio -y
```

**Verification (after either method):**
```bash
flatpak remotes -d
flatpak list --app
```

---

# Node 2 (serverb.lab.example.com)

## 19. Reset Root Password (Two Methods)

### Method A: `rd.break` (RHEL 9.1+)
1. Interrupt GRUB → press `e`
2. On the line starting with `linux`, append `rd.break console=tty0`
3. `Ctrl+X` to boot
4. `mount -o remount,rw /sysroot`
5. `chroot /sysroot`
6. `passwd root` → set `redhat`
7. `touch /.autorelabel`
8. `exit` → `reboot`

### Method B: `init=/bin/bash` (Universal)
1. Interrupt GRUB → press `e`
2. On the line starting with `linux`, replace `rhgb quiet` with `init=/bin/bash`
3. `Ctrl+X` to boot
4. `mount -o remount,rw /`
5. `passwd root` → set `redhat`
6. `touch /.autorelabel`
7. `/usr/sbin/reboot -f`

**Verification:** After reboot, login as root with `redhat`.

---

## 20. Create a Swap Partition

**Solution:**
```bash
fdisk /dev/sdb
```
Inside `fdisk`: `n` → `p` → `1` → Enter → `+512M` → `t` → `82` → `w`
```bash
mkswap /dev/sdb1
swapon /dev/sdb1
echo "/dev/sdb1 swap swap defaults 0 0" >> /etc/fstab
```

**Verification:**
```bash
swapon --show
free -h
```

---

## 21. LVM Logical Volume `database`

**Solution:**
```bash
pvcreate /dev/sdb2
vgcreate -s 8M datastore /dev/sdb2
lvcreate -l 50 -n database datastore
mkfs.ext3 /dev/datastore/database
mkdir -p /mnt/database
mount /dev/datastore/database /mnt/database
echo "/dev/datastore/database /mnt/database ext3 defaults 0 0" >> /etc/fstab
```

**Verification:**
```bash
lvs
df -h /mnt/database
```

---

## 22. VDO Volume (LVM‑integrated)

**Solution:**
```bash
dnf install vdo -y
lvcreate --type vdo -L 5G -n vdopool datastore
lvcreate --type vdo -V 50G -n vdoLV datastore/vdopool
mkfs.xfs -K /dev/datastore/vdoLV
mkdir /data
mount /dev/datastore/vdoLV /data
echo "/dev/datastore/vdoLV /data xfs defaults 0 0" >> /etc/fstab
```

**Verification:**
```bash
lvs -a | grep vdo
df -h /data
```

---

## 23. Extend a Logical Volume

**Solution:**
```bash
lvextend -l +100 -r /dev/datastore/database
```

**Verification:**
```bash
lvs /dev/datastore/database
df -h /mnt/database
```

---

## 24. Tuned Profile

**Solution:**
```bash
dnf install tuned -y
systemctl enable --now tuned
tuned-adm profile $(tuned-adm recommend)
```

**Verification:**
```bash
tuned-adm active
```

---

## 25. Container as a Service (Old + Quadlet)

**Prerequisites:**
```bash
dnf install podman container-tools -y
podman login registry.access.redhat.com --tls-verify=false
mkdir -p /home/student/webserver
echo "Hello from container" > /home/student/webserver/index.html
```

**Method A – Old (systemd user service):**
```bash
podman run -d --name webserver -p 8080:8080 -v /home/student/webserver:/var/www/html:Z registry.access.redhat.com/ubi9/httpd-24
mkdir -p ~/.config/systemd/user
cd ~/.config/systemd/user
podman generate systemd --new --files --name webserver
systemctl --user daemon-reload
systemctl --user enable --now container-webserver.service
loginctl enable-linger
```

**Method B – New (Quadlet):**
```bash
mkdir -p ~/.config/containers/systemd
vim ~/.config/containers/systemd/webserver.container
```
Paste:
```
[Container]
Image=registry.access.redhat.com/ubi9/httpd-24
PublishPort=8080:8080
Volume=/home/student/webserver:/var/www/html:Z

[Install]
WantedBy=default.target
```
```bash
systemctl --user daemon-reload
systemctl --user enable --now webserver
loginctl enable-linger
```

**Verification:**
```bash
curl http://localhost:8080
systemctl --user status webserver
```

---

## 26. Run a Script Inside an Existing Container

**Solution:**
```bash
echo '#!/bin/bash' > /tmp/hello.sh
echo 'echo "Hello from container"' >> /tmp/hello.sh
chmod +x /tmp/hello.sh
podman cp /tmp/hello.sh TestContainer2:/tmp/
podman exec TestContainer2 /bin/bash /tmp/hello.sh
```

**Verification:**
```bash
podman exec TestContainer2 cat /tmp/hello.sh
```

---

## 27. Build a Container Image from a Dockerfile

**Solution:**
```bash
vim Dockerfile
```
Paste:
```
FROM registry.access.redhat.com/ubi9/httpd-24
COPY index.html /var/www/html/
```
```bash
echo "<h1>Custom</h1>" > index.html
podman build --layers=false -t localhost/dockerfiletest .
```

**Verification:**
```bash
podman images | grep dockerfiletest
```

---

## 28. Systemd Timer (Run Every 3 Minutes)

**Solution:**
```bash
vim /usr/local/bin/testtimer.sh
```
Paste:
```bash
#!/bin/bash
echo "Hello from EX200 script at $(date)" >> /var/log/ex200script.log
```
```bash
chmod +x /usr/local/bin/testtimer.sh

vim /etc/systemd/system/ex200script.service
```
Paste:
```
[Service]
Type=oneshot
ExecStart=/usr/local/bin/testtimer.sh
```
```bash
vim /etc/systemd/system/ex200script.timer
```
Paste:
```
[Timer]
OnCalendar=*:0/3
Persistent=true

[Install]
WantedBy=timers.target
```
```bash
systemctl daemon-reload
systemctl enable --now ex200script.timer
```

**Verification:**
```bash
systemctl list-timers | grep ex200
tail -f /var/log/ex200script.log
```

---

## 29. Restricted User (rachel) – Only `passwd` Command

**Solution:**
```bash
useradd -s /bin/passwd rachel
echo password | passwd --stdin rachel
```

**Verification:**
```bash
grep rachel /etc/passwd
su - rachel -c "exit"
```

---

## 30. Find a Specific String in a File

**Solution:**
```bash
grep "ng" /usr/share/xml/iso-codes/iso_639_3.xml | grep -v '^$' > /root/list
cat -n /root/list
```

**Verification:**
```bash
wc -l /root/list
```

---

## 31. Download a Dockerfile from a Remote Server and Build

**Solution:**
```bash
wget https://raw.githubusercontent.com/docker-library/httpd/master/2.4/Dockerfile -O /tmp/Dockerfile
podman build --layers=false -t localhost/remote-image -f /tmp/Dockerfile .
```

**Verification:**
```bash
podman images | grep remote-image
```

---

## Exam Tips

- **Keyboard layout:** Test passwords by typing them in the username field first.
- **Have a backup keyboard** if possible.
- For root password reset, know **both** `rd.break` and `init=/bin/bash`.
- Practice all tasks on both **servera** and **serverb**.
- Always verify with `ls`, `cat`, `getfacl`, `mount`, etc.

---
