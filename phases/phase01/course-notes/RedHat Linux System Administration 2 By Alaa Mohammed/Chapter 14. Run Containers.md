# Chapter 14: Run Containers – RHCSA Complete Guide

## Table of Contents

- [Chapter 14: Run Containers – RHCSA Complete Guide](#chapter-14-run-containers--rhcsa-complete-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Containers vs. VMs vs. Bare Metal (Exam Context)](#1-containers-vs-vms-vs-bare-metal-exam-context)
  - [2. Core Technologies: cgroups and Namespaces](#2-core-technologies-cgroups-and-namespaces)
  - [3. Podman – The RHCSA Container Engine](#3-podman--the-rhcsa-container-engine)
    - [3.1 Basic Container Lifecycle](#31-basic-container-lifecycle)
    - [3.2 Running Containers – Important Options](#32-running-containers--important-options)
    - [3.3 Interactive Shell and Command Execution](#33-interactive-shell-and-command-execution)
    - [3.4 Container Naming and Labels](#34-container-naming-and-labels)
  - [4. Rootless Containers (Default in RHCSA)](#4-rootless-containers-default-in-rhcsa)
  - [5. Container Images and Registries](#5-container-images-and-registries)
  - [6. Container Networking and Port Publishing](#6-container-networking-and-port-publishing)
  - [7. Persistent Data: Volumes and Bind Mounts](#7-persistent-data-volumes-and-bind-mounts)
    - [7.1 Named Volumes (Managed by Podman)](#71-named-volumes-managed-by-podman)
    - [7.2 Bind Mounts (Host Directory)](#72-bind-mounts-host-directory)
  - [8. Managing Containers with Systemd (Quadlet)](#8-managing-containers-with-systemd-quadlet)
    - [Method 1: `podman generate systemd` (older)](#method-1-podman-generate-systemd-older)
    - [Method 2: Quadlet (modern, simpler – RHEL 9.3+)](#method-2-quadlet-modern-simpler--rhel-93)
  - [9. Buildah – Building Images from Scratch](#9-buildah--building-images-from-scratch)
  - [10. Skopeo – Inspecting and Copying Remote Images](#10-skopeo--inspecting-and-copying-remote-images)
  - [11. Real‑World Scenario – Deploying a Containerised Web Application for a Small Team](#11-realworld-scenario--deploying-a-containerised-web-application-for-a-small-team)
    - [Background](#background)
    - [Step‑by‑Step Implementation](#stepbystep-implementation)
      - [1. Create the Dockerfile and application files](#1-create-the-dockerfile-and-application-files)
      - [2. Build the container image with Buildah](#2-build-the-container-image-with-buildah)
      - [3. Prepare persistent storage](#3-prepare-persistent-storage)
      - [4. Run the container with the correct mounts and port publishing](#4-run-the-container-with-the-correct-mounts-and-port-publishing)
      - [5. Test data persistence](#5-test-data-persistence)
      - [6. Inspect the image remotely with Skopeo (simulate checking for updates)](#6-inspect-the-image-remotely-with-skopeo-simulate-checking-for-updates)
      - [7. Create a Quadlet unit for automatic startup](#7-create-a-quadlet-unit-for-automatic-startup)
      - [8. Verify the service and reboot test](#8-verify-the-service-and-reboot-test)
    - [Result](#result)
  - [12. RHCSA Practice Lab – Containers](#12-rhcsa-practice-lab--containers)
    - [Lab 1: Basic Container Operations](#lab-1-basic-container-operations)
    - [Lab 2: Web Server Container with Port Publishing](#lab-2-web-server-container-with-port-publishing)
    - [Lab 3: Persistent Data with Volumes](#lab-3-persistent-data-with-volumes)
    - [Lab 4: Bind Mount with SELinux (`:Z`)](#lab-4-bind-mount-with-selinux-z)
    - [Lab 5: Rootless Systemd Service with Quadlet](#lab-5-rootless-systemd-service-with-quadlet)
    - [Lab 6: Build an Image with Buildah](#lab-6-build-an-image-with-buildah)
    - [Lab 7: Inspect Remote Image with Skopeo](#lab-7-inspect-remote-image-with-skopeo)
  - [13. Quick Reference Table (Exam Cram)](#13-quick-reference-table-exam-cram)

---

## 1. Containers vs. VMs vs. Bare Metal (Exam Context)

You only need to understand the basic differences for RHCSA:

- **Containers** share the host kernel, start in milliseconds, and use **namespaces** (isolation) and **cgroups** (resource limits).
- **Virtual Machines** require a hypervisor and a full guest OS. Stronger isolation, heavier.
- **Bare metal** is a physical server with no virtualization.

The exam expects you to know that containers are lightweight and that **Podman** is the tool used on RHEL 9.

---

## 2. Core Technologies: cgroups and Namespaces

For RHCSA, you should understand conceptually:

- **Namespaces** provide isolation (PID, NET, MNT, UTS, IPC, USER). Each container sees its own process tree, network stack, and filesystem.
- **cgroups** control resource usage (CPU, memory, I/O). They prevent one container from starving the host.

You do **not** need to manipulate cgroups directly; Podman handles them.

---

## 3. Podman – The RHCSA Container Engine

Podman is **daemonless** and can run containers **rootlessly** (default). Its CLI is almost identical to Docker’s, so Docker experience transfers easily.

### 3.1 Basic Container Lifecycle

| Operation | Command | Example |
|-----------|---------|---------|
| Pull an image | `podman pull` | `podman pull ubi9` |
| List images | `podman images` | |
| Run a container | `podman run` | `podman run -d --name web nginx` |
| List running containers | `podman ps` | `podman ps -a` (all, including stopped) |
| Stop a container | `podman stop` | `podman stop web` |
| Start a stopped container | `podman start` | `podman start web` |
| Remove a container | `podman rm` | `podman rm web` |
| Remove an image | `podman rmi` | `podman rmi nginx` |
| Show logs | `podman logs` | `podman logs web` |
| Execute command inside running container | `podman exec` | `podman exec -it web /bin/bash` |

### 3.2 Running Containers – Important Options

| Option | Effect |
|--------|--------|
| `-d` | Detach (run in background) |
| `-it` | Interactive + allocate pseudo‑TTY (use with `/bin/bash`) |
| `--name` | Assign a name (otherwise random) |
| `--rm` | Automatically remove container when it exits |
| `-p host:container` | Publish port (e.g., `-p 8080:80`) |
| `-v` | Mount volume or bind mount |
| `-e` | Set environment variable |
| `--restart` | Restart policy (`always`, `on-failure`) |

**Examples:**

```bash
# Run a web server in the background, name it "web", publish port 8080
podman run -d --name web -p 8080:80 nginx

# Run an interactive shell in a UBI9 container
podman run -it ubi9 /bin/bash

# Run a one‑off command and delete the container after exit
podman run --rm ubi9 echo "Hello"
```

### 3.3 Interactive Shell and Command Execution

```bash
# Get a shell inside a running container
podman exec -it web /bin/bash

# Run a single command without entering shell
podman exec web ls -l /var/log
```

### 3.4 Container Naming and Labels

- **Name**: Assigned with `--name`. Must be unique per user.
- **ID**: A long hash; you can use the first 12 characters as a shortcut.
- **Labels**: Key‑value metadata (e.g., `--label version=1.0`). Not heavily tested.

---

## 4. Rootless Containers (Default in RHCSA)

Podman runs containers **as your non‑root user** by default. This is a key security feature.

- No `sudo` needed for basic operations (`pull`, `run`, `ps`, `stop`, `rm`).
- Rootless containers cannot bind to privileged ports (<1024) – use higher ports like `8080`.
- Volumes and storage are stored under `~/.local/share/containers/`.

**Check if you are rootless:** `podman info | grep rootless` should output `rootless: true`.

---

## 5. Container Images and Registries

Images are stored in **registries**. Default is Docker Hub (`docker.io`). RHEL provides the **Red Hat Container Catalog** (`registry.access.redhat.com` or `registry.redhat.io`).

**Pull an image from Docker Hub:**
```bash
podman pull nginx
```

**Pull from Red Hat registry:**
```bash
podman pull registry.access.redhat.com/ubi9/ubi
```

**List local images:**
```bash
podman images
```

**Remove an image:**
```bash
podman rmi nginx
```

**Tag an image for your own registry:**
```bash
podman tag myapp:latest myregistry.local:5000/myapp:1.0
podman push myregistry.local:5000/myapp:1.0
```

---

## 6. Container Networking and Port Publishing

Each container gets its own network namespace (by default). Use `-p` to publish a container port to the host.

**Examples:**

```bash
# Map host port 8080 to container port 80
podman run -d -p 8080:80 --name web nginx

# Map random host port to container port 80 (use podman ps to see mapping)
podman run -d -P --name web2 nginx

# Map multiple ports
podman run -d -p 8080:80 -p 8443:443 nginx
```

**List ports of running containers:**
```bash
podman port web
```

**Rootless note:** You cannot bind to ports below 1024. Use `8080`, `8443`, etc.

---

## 7. Persistent Data: Volumes and Bind Mounts

Containers are ephemeral – data written inside disappears when the container is removed. Use volumes to persist data.

### 7.1 Named Volumes (Managed by Podman)

```bash
# Create a volume
podman volume create mydata

# Run container using the volume
podman run -d --name db -v mydata:/var/lib/mysql mysql

# List volumes
podman volume ls

# Inspect volume
podman volume inspect mydata

# Remove volume
podman volume rm mydata
```

### 7.2 Bind Mounts (Host Directory)

Mount a directory from the host into the container.

```bash
podman run -d --name web -v /home/user/website:/usr/share/nginx/html:Z nginx
```

**The `:Z` option** (and `:z`) is critical for SELinux:

- `:Z` – Private label: relabel the host directory so **only this container** can access it.
- `:z` – Shared label: multiple containers can access the directory.

Without `:Z` or `:z`, SELinux will deny access.

**RHCSA exam tip:** Always use `:Z` when binding a host directory to a container.

---

## 8. Managing Containers with Systemd (Quadlet)

RHCSA expects you to know how to make a container start automatically at boot.

### Method 1: `podman generate systemd` (older)

```bash
# Create a container (not systemd yet)
podman run -d --name myapp -p 8080:80 nginx

# Generate systemd unit file
podman generate systemd --name myapp --files

# Move the unit to systemd directory
sudo mv container-myapp.service /etc/systemd/system/

# Reload systemd and enable
sudo systemctl daemon-reload
sudo systemctl enable --now container-myapp.service
```

### Method 2: Quadlet (modern, simpler – RHEL 9.3+)

Create a `.container` file in `~/.config/containers/systemd/` (rootless) or `/etc/containers/systemd/` (system).

Example `~/config/containers/systemd/web.container`:

```ini
[Unit]
Description=My Web Container

[Container]
Image=nginx:latest
ContainerName=web
PublishPort=8080:80

[Service]
Restart=always

[Install]
WantedBy=default.target
```

Then start it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now web.service
```

**For rootful containers** (system‑wide), place the file in `/etc/containers/systemd/` and use `sudo systemctl enable web.service`.

---

## 9. Buildah – Building Images from Scratch

Buildah builds OCI container images **without a running container engine** or Dockerfile.

**Build from a Containerfile:**
```bash
buildah bud -t myapp:latest .
```

**Build from scratch (custom image):**
```bash
# Create a working container
ctr=$(buildah from scratch)

# Mount its root filesystem
mnt=$(buildah mount $ctr)

# Copy files
cp /path/to/binary $mnt/bin/
cp -r /path/to/config $mnt/etc/

# Configure
buildah config --entrypoint "/bin/myapp" $ctr

# Commit
buildah commit $ctr myapp:latest
```

**RHCSA scope:** You should be able to build a simple image from a Dockerfile using `buildah bud`.

---

## 10. Skopeo – Inspecting and Copying Remote Images

Skopeo works with remote images **without pulling** them locally.

**Inspect an image:**
```bash
skopeo inspect docker://nginx:latest
```

**Copy an image between registries:**
```bash
skopeo copy docker://nginx:latest docker://myregistry.local/nginx:latest
```

**RHCSA scope:** Skopeo appears in the exam objectives, but you mainly need to know that it can inspect remote images.

---

## 11. Real‑World Scenario – Deploying a Containerised Web Application for a Small Team

### Background

Your team develops a Python Flask application called `myapp`. You need to deploy it on a shared RHEL 9 development server as a container, using Podman rootless mode for security. The application must:

- Run with a custom image built from a Dockerfile using Buildah.
- Be accessible on host port **8085**.
- Persist uploaded files in a named volume, because those files must survive container recreation.
- Mount a host directory for static assets (images, CSS) with proper SELinux labelling.
- Start automatically when the server boots, using a Quadlet systemd unit.
- Be inspectable without pulling via Skopeo (for verifying available updates).

You are logged in as the user `developer`.

### Step‑by‑Step Implementation

#### 1. Create the Dockerfile and application files

```bash
mkdir ~/myapp && cd ~/myapp
```

Create `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from myapp container"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Create `Dockerfile`:
```
FROM registry.access.redhat.com/ubi9/ubi
RUN dnf install -y python3-pip && pip3 install flask
RUN mkdir -p /data/uploads && mkdir -p /data/static
COPY app.py /app/app.py
EXPOSE 5000
CMD ["python3", "/app/app.py"]
```

#### 2. Build the container image with Buildah

```bash
buildah bud -t myapp:1.0 .
```

Verify the image:
```bash
podman images | grep myapp
```

#### 3. Prepare persistent storage

Create a named volume for uploads:
```bash
podman volume create myapp_uploads
```

Create a host directory for static files:
```bash
mkdir -p ~/static_assets
echo "Static content" > ~/static_assets/index.html
```

#### 4. Run the container with the correct mounts and port publishing

```bash
podman run -d \
  --name myapp \
  -p 8085:5000 \
  -v myapp_uploads:/data/uploads \
  -v ~/static_assets:/data/static:Z \
  myapp:1.0
```

- `-v myapp_uploads:/data/uploads` uses the named volume.
- `-v ~/static_assets:/data/static:Z` uses a bind mount with SELinux relabel.

Verify with `curl http://localhost:8085`.

#### 5. Test data persistence

Inside the container, create a test file in `/data/uploads`:
```bash
podman exec myapp touch /data/uploads/test.txt
```

Stop and remove the container:
```bash
podman stop myapp
podman rm myapp
```

Run a new container from the same image, mounting the same volume:
```bash
podman run -d --name myapp -p 8085:5000 -v myapp_uploads:/data/uploads myapp:1.0
```

Check that the file still exists:
```bash
podman exec myapp ls /data/uploads/test.txt
```

#### 6. Inspect the image remotely with Skopeo (simulate checking for updates)

```bash
skopeo inspect docker://myregistry.local:5000/myapp:1.0
```

(If no registry is available, you can inspect the local image via `docker-daemon` transport, but for remote inspection, use a registry URL.)

#### 7. Create a Quadlet unit for automatic startup

Create the file `~/.config/containers/systemd/myapp.container`:

```ini
[Unit]
Description=My Flask Application

[Container]
Image=myapp:1.0
ContainerName=myapp
PublishPort=8085:5000
Volume=myapp_uploads:/data/uploads
Volume=%h/static_assets:/data/static:Z

[Service]
Restart=always

[Install]
WantedBy=default.target
```

Reload and enable the user service:

```bash
systemctl --user daemon-reload
systemctl --user enable --now myapp.service
```

#### 8. Verify the service and reboot test

Check the service status:
```bash
systemctl --user status myapp
```

Reboot the server (or simulate by stopping all user services and re‑logging). After logging back in, the container should be running automatically.

### Result

The Flask application is deployed in a secure, rootless container that persists data, automatically starts on boot, and can be inspected without pulling. All RHCSA container objectives are demonstrated in a single, realistic workflow.

---

## 12. RHCSA Practice Lab – Containers

### Lab 1: Basic Container Operations

1. Pull the `registry.access.redhat.com/ubi9/ubi` image.
2. Run a container named `test1` from that image that prints “Hello RHCSA” and exits.
3. Run a container named `shell` from the same image with an interactive bash session. Inside, run `cat /etc/os-release` to verify it’s RHEL 9. Exit.
4. List all containers (including stopped).
5. Remove the `test1` container.

### Lab 2: Web Server Container with Port Publishing

1. Pull the `nginx` image from Docker Hub.
2. Run a container named `web` in the background, publishing host port `8080` to container port `80`.
3. Verify the web server is accessible: `curl localhost:8080` (you should see the default Nginx page).
4. View the container logs.
5. Stop and remove the container.

### Lab 3: Persistent Data with Volumes

1. Create a named volume `html-data`.
2. Run an `nginx` container with the volume mounted to `/usr/share/nginx/html`.
3. Write a custom `index.html` file using `podman exec` (e.g., `podman exec web sh -c "echo 'Custom page' > /usr/share/nginx/html/index.html"`).
4. Stop and remove the container.
5. Run a **new** `nginx` container using the same volume. Verify the custom page still appears.

### Lab 4: Bind Mount with SELinux (`:Z`)

1. Create a host directory `~/website` and put an `index.html` file inside.
2. Run an `nginx` container mounting that directory to `/usr/share/nginx/html` **with** the `:Z` option.
3. Access via browser / curl. If you forget `:Z`, note the permission denied error, then add `:Z` and re‑run.
4. Check the SELinux context of the directory with `ls -Z` – it should be `container_file_t`.

### Lab 5: Rootless Systemd Service with Quadlet

1. Create a Quadlet `.container` file for the `nginx` image (publish port `8081:80`).
2. Place it in `~/.config/containers/systemd/web.container`.
3. Reload systemd user daemon, enable and start the service.
4. Verify the container runs automatically: `podman ps` and `curl localhost:8081`.
5. Check the service status: `systemctl --user status web`.
6. Reboot (or simulate by killing user services) and verify the container restarts.

### Lab 6: Build an Image with Buildah

1. Create a directory `~/build` with a `Dockerfile`:
   ```
   FROM registry.access.redhat.com/ubi9/ubi
   RUN dnf install -y httpd && dnf clean all
   RUN echo "Built with Buildah" > /var/www/html/index.html
   EXPOSE 80
   CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
   ```
2. Build the image with `buildah bud -t myhttpd .`
3. Run a container from this image, publish port `8082:80`, and test with `curl`.

### Lab 7: Inspect Remote Image with Skopeo

1. Use `skopeo inspect` to display the architecture and layers of the `nginx:alpine` image (without pulling it locally).

---

## 13. Quick Reference Table (Exam Cram)

| Task | Command |
|------|---------|
| Pull image | `podman pull nginx` |
| Run detached container with port | `podman run -d --name web -p 8080:80 nginx` |
| Run interactive shell | `podman run -it ubi9 /bin/bash` |
| List running containers | `podman ps` |
| List all containers | `podman ps -a` |
| Stop container | `podman stop web` |
| Remove container | `podman rm web` |
| Remove image | `podman rmi nginx` |
| View logs | `podman logs web` |
| Execute command | `podman exec -it web /bin/bash` |
| Create named volume | `podman volume create mydata` |
| Bind mount with SELinux | `-v /host/path:/container/path:Z` |
| Create systemd unit (Podman) | `podman generate systemd --name web --files` |
| Quadlet file location | `~/.config/containers/systemd/app.container` |
| Build image from Dockerfile | `buildah bud -t myapp .` |
| Inspect remote image | `skopeo inspect docker://nginx` |

---

**Date documented:** 2026-05-17  
**RHCSA Exam Objectives covered:** Run containers, manage container images, rootless containers, persistent storage, integrate containers with systemd, SELinux for containers.