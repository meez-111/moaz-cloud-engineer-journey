
### Phase 1: Linux Fundamentals & OverTheWire Bandit Challenges

- **🎓 Detailed Topics**: Filesystem hierarchy, permissions (`chmod`, `chown`), user/group management, process management (`ps`, `top`, `kill`), `systemd` (`systemctl`, `journalctl`), package managers (`apt`, `dnf`), cron jobs, basic text editors (`vim`, `nano`), and essential commands (`grep`, `awk`, `sed`, `find`).
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Linux for Beginners” (≈5h).
- **💀 OverTheWire Bandit (Bonus)**: Alongside the course, tackle the **Bandit wargame**. It's a series of ~30 challenges that teach real command-line skills through problem-solving.
- **🕹️ 3 Independent Mini-Projects**:
  1. **System Health Monitor**: A Bash script that logs CPU, memory, and disk usage every hour and alerts you if thresholds are exceeded.
  2. **Automated Backup Script**: Compresses a specified directory into a timestamped `.tar.gz` archive, moves it to a `/backups` folder, and deletes backups older than 7 days.
  3. **Log File Analyzer**: Scans a log file for a keyword like "ERROR" and outputs the count and the last 5 matching lines.

---

### Phase 2: Networking Fundamentals

- **🎓 Detailed Topics**: OSI model (focus on L4/TCP-UDP, L7/HTTP), IPv4 subnetting (CIDR), private vs. public IPs, DNS records (A, CNAME, MX), TCP 3-way handshake, UDP vs. TCP, HTTP methods and status codes, NAT, routing, ARP, and key troubleshooting tools (`ping`, `traceroute`, `dig`, `curl`, `tcpdump`).
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Computer Networking Course” (≈8h).
- **🕹️ 3 Independent Mini-Projects**:
  1. **Network Scanner**: A Bash script to `ping` sweep a local subnet and discover all active hosts.
  2. **DNS Lookup Tool**: A Bash script that takes a domain name and prints its A and AAAA records using `dig`.
  3. **Port Scanner**: A Bash script using `nc` (netcat) to check if specific ports (e.g., 22, 80, 443) are open on a target host.

---

### Phase 3: Database Administration & Knowledge

- **🎓 Detailed Topics**:
  - **Database Fundamentals**: What is a DBMS? Why do we need databases? ACID properties (Atomicity, Consistency, Isolation, Durability) and their importance for reliable transactions.
  - **Relational Data Model**: Understanding tables, rows, columns, primary keys, foreign keys, and relationships (one-to-one, one-to-many, many-to-many).
  - **SQL (Structured Query Language)** : The standard language for relational databases. Learn `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN` (INNER, LEFT, RIGHT), `GROUP BY`, `ORDER BY`, and aggregate functions (`COUNT`, `SUM`, `AVG`).
  - **Database Design & Normalization**: Organizing data to reduce redundancy and improve integrity. Understanding 1NF, 2NF, and 3NF normal forms.
  - **Indexing & Performance**: How indexes speed up queries, and the trade-offs of using them.
  - **Backup & Recovery**: Strategies for protecting data, including full backups, incremental backups, and point-in-time recovery.
  - **Database Administration in the Cloud**: Introduction to managed database services like AWS RDS, including automated backups, patching, and scaling.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Master Database Management Systems” course.
- **🕹️ 3 Independent Mini-Projects**:
  1. **Library Database Schema Design**: Design a normalized database schema for a library system (books, members, loans). Implement it using SQLite or PostgreSQL locally, write queries to find overdue books and popular authors.
  2. **Employee Directory API**: Set up a local MySQL/PostgreSQL database, create an `employees` table, and write SQL queries to insert, update, and query employee data. Export the data to a CSV file using a Python script.
  3. **Backup Automation Script**: Write a Bash script that uses `mysqldump` or `pg_dump` to automatically back up a local database daily, compress the backup, and rotate old backups (keeping only the last 7 days).

---

### Phase 4: Git & Version Control

- **🎓 Detailed Topics**: Core commands (`init`, `add`, `commit`, `push`, `pull`, `clone`), branching (`branch`, `checkout`, `merge`), resolving merge conflicts, `.gitignore`, and GitHub workflows (forking, pull requests).
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Git and GitHub for Beginners” (≈2h).
- **🕹️ 3 Independent Mini-Projects**:
  1. **Repo Setup**: Create a local repo, add a `README.md`, commit, and push to GitHub.
  2. **Feature Branch Workflow**: Create a branch, add a new file, and merge it back to `main`.
  3. **Simulate Merge Conflict**: Create a conflict on purpose and resolve it manually.

---

### Phase 5: Bash Scripting for System Automation

- **🎓 Detailed Topics**: Shebang, variables, command-line arguments, conditionals (`if`), loops (`for`, `while`), functions, exit codes, text processing (`grep`, `sed`, `awk`), and scheduling with `cron`.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Bash Scripting Full Course” (≈3h).
- **🕹️ 3 Attractive Mini-Projects**:
  1. **Intelligent Backup Rotator**: Instead of just deleting old backups, this script compresses directories, moves them to a `/backups` folder, **and** keeps a configurable number of the most recent backups (e.g., keep last 5). It logs all actions.
  2. **Automated Server Hardening Toolkit**: A script that asks for a username, creates the user, adds them to the `sudo` group, disables root SSH login, and sets up a basic firewall (`ufw`) with only SSH and HTTP allowed.
  3. **Custom System Report Generator**: A script that generates a beautiful HTML report (using `echo` and HTML tags) showing system uptime, memory usage, disk usage, and logged-in users.

---

### Phase 6: Python for Cloud Automation (6+ Projects)

- **🎓 Detailed Topics**: Python data types, lists, dictionaries, loops, functions, file I/O (`open`, `read`, `write`), the `requests` library for APIs, `json` parsing, error handling (`try/except`), and an intro to `boto3` (AWS SDK).
- **🔗 Free Complete YouTube Course**: freeCodeCamp – **"Learn Python - Full Course for Beginners"** .
- **🕹️ 6 Independent Mini-Projects** (Build at least 4):
  1. **Weather CLI App**: Use `requests` to fetch live weather from a free API and display current conditions.
  2. **Automated File Organizer**: Monitor a `Downloads` folder and move files into subfolders by extension.
  3. **Log File Parser**: Read an Apache access log, count requests per IP, output top 10 IPs.
  4. **To-Do List CLI**: Store tasks in `tasks.json` with add/list/complete/delete commands.
  5. **JSON Configuration Manager**: Read a `config.json`, validate keys, create a backup before changes.
  6. **CSV to JSON Converter**: Convert a CSV file to JSON format.

---

### Phase 7: Core Cloud Concepts (Provider Agnostic)

- **🎓 Detailed Topics**: NIST definition of cloud computing, IaaS/PaaS/SaaS, public/private/hybrid clouds, the Shared Responsibility Model, High Availability (HA), Fault Tolerance (FT), Disaster Recovery (DR), RPO/RTO.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Cloud Computing Full Course” (select conceptual chapters).
- **🕹️ 3 Mini-Projects**:
  1. **Service Model Comparison**: Markdown table with IaaS/PaaS/SaaS examples and responsibility division.
  2. **DR Plan**: Write a DR plan for an e-commerce site (RTO=2h, RPO=15min).
  3. **Cost Analysis**: Compare On-Demand vs Reserved Instance pricing.

---

### Phase 8: AWS Cloud Practitioner (freeCodeCamp)

- **🎓 Detailed Topics**: AWS Global Infrastructure (Regions, AZs), Compute (EC2, Lambda), Networking (VPC, Route 53, CloudFront), Storage (S3, EBS, EFS), Databases (RDS, DynamoDB), Security (IAM, KMS, CloudTrail), Billing & Pricing, Well-Architected Framework.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “AWS Certified Cloud Practitioner Certification Course (CLF-C02)” (≈14h).
- **🕹️ 3 Mini-Projects**:
  1. **S3 Static Website**: Host an `index.html` on S3 with public read policy.
  2. **EC2 Web Server**: Launch `t2.micro`, install Nginx, serve "Hello from EC2".
  3. **IAM User & Group**: Create "Developers" group with `ReadOnlyAccess` to EC2.

---

### Phase 9: AWS Solutions Architect (freeCodeCamp)

- **🎓 Detailed Topics**: S3 (lifecycle policies, versioning, replication), VPC (custom VPC, public/private subnets, IGW, NAT Gateway), EC2 (instance families, pricing models), RDS (read replicas, Multi-AZ) vs DynamoDB, ALB, Auto Scaling Groups.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “AWS Solutions Architect Associate Certification (SAA-C03)” (≈24h).
- **🕹️ 3 Mini-Projects**:
  1. **HA with ALB + ASG**: ASG with 2 instances across 2 AZs behind an ALB.
  2. **Custom VPC**: VPC with public/private subnets, IGW, NAT Gateway.
  3. **Serverless Lambda + DynamoDB**: Lambda writes a test item to DynamoDB.

---

### Phase 10: Virtualization & DevOps Principles

- **🎓 Detailed Topics**: Virtualization (VMs vs Containers, hypervisors), DevOps principles (CI/CD pipeline, The Three Ways).
- **🔗 Free Resources**: YouTube search "Virtualization vs Containerization", "DevOps Principles for Beginners".
- **🕹️ 3 Mini-Projects**:
  1. **VirtualBox Lab**: Set up a Linux VM, install a web server, access from host.
  2. **Concept Map**: Markdown document with diagram comparing VMs and containers.
  3. **DevOps in a Nutshell**: Blog post explaining DevOps lifecycle, CI/CD, IaC, Monitoring.

---

### Phase 11: Containers & Orchestration (Docker & Kubernetes)

- **🎓 Detailed Topics**: Docker (`Dockerfile`, images, containers, volumes, Docker Compose). Kubernetes (Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Persistent Volumes).
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Kubernetes Course - Full Beginners Tutorial” (≈2-3h).
- **🕹️ 3 Mini-Projects**:
  1. **Containerize a Python App**: Write `Dockerfile`, build, run locally.
  2. **Local K8s with Minikube**: Deploy app as Deployment, expose via NodePort Service.
  3. **ConfigMap & Secret**: Deploy app reading config from ConfigMap and password from Secret.

---

### Phase 12: Infrastructure as Code (IaC) with Terraform

- **🎓 Detailed Topics**: Declarative syntax, HCL, providers, resources, variables, outputs, `terraform plan/apply/destroy`, state management, modules.
- **🔗 Free Complete YouTube Course**: freeCodeCamp – “Terraform Course - Automate your AWS cloud infrastructure”.
- **🕹️ 3 Mini-Projects**:
  1. **Codify a Single EC2 Instance**: Terraform to launch EC2 with SSH security group.
  2. **Codify the Custom VPC**: Terraform for VPC, subnets, IGW, NAT.
  3. **Terraform Modules**: Refactor VPC into reusable module for dev/staging.

---

### Phase 13: CI/CD & Automation (GitHub Actions)

- **🎓 Detailed Topics**: YAML workflows, triggers, jobs, steps, actions, secrets, artifacts.
- **🔗 Free Complete YouTube Course**: Search “GitHub Actions Tutorial” on freeCodeCamp.
- **🕹️ 3 Mini-Projects**:
  1. **Simple Linter**: Workflow that runs `pylint` on every push.
  2. **Auto-Deploy to S3**: Workflow that builds static site and syncs to S3 on push to `main`.
  3. **Terraform CI/CD**: Workflow that runs `plan` on PRs and `apply` on merge to `main`.

---

### Phase 14: Monitoring, Observability & Logging (Prometheus & Grafana)

- **🎓 Detailed Topics**: Metrics, logs, traces. Prometheus (metrics collection, PromQL), Grafana (dashboards, alerting).
- **🔗 Free Complete YouTube Course**: Search “Prometheus & Grafana Tutorial” on freeCodeCamp.
- **🕹️ 3 Mini-Projects**:
  1. **Local Prometheus + Grafana Stack**: Docker Compose to spin up both.
  2. **Monitor a Local App**: Configure Prometheus to scrape metrics from EC2, visualize in Grafana.
  3. **Set Up an Alert**: Grafana alert for CPU >80% with test notification.

---

### Phase 15: The 3 Major Capstone Projects

1. **Official Cloud Resume Challenge**: S3 + CloudFront + API Gateway + Lambda + DynamoDB + Terraform + GitHub Actions.
2. **Secure 3‑Tier Production App**: VPC with public/private subnets, ALB, ASG, RDS Multi-AZ, KMS encryption, least-privilege IAM.
3. **Serverless Event‑Driven Backend**: S3 trigger → Lambda (process file) → DynamoDB + SNS notification.

---

### Phase 16: Saudi Arabia Regulations & Compliance

- **🎓 Detailed Topics**: PDPL (data localization, consent, breach notification), NCA (ECC, CCC), CST regulations, use of `me-south-1` region.
- **🔗 Free Resources**: YouTube search “Saudi PDPL overview 2025”, “NCA ECC explained”.
- **🕹️ 3 Mini Compliance Projects**:
  1. **Region Compliance Checker**: Python + boto3 script flags non-`me-south-1` resources.
  2. **PDPL Compliance Guide**: Markdown document for data encryption, access logging, retention.
  3. **NCA ECC Mapper**: Spreadsheet mapping ECC controls to AWS services.

---

### Phase 17: Certifications

- **AWS Cloud Practitioner (CLF-C02)** – free AWS Skill Builder + freeCodeCamp practice.
- **AWS Solutions Architect – Associate (SAA-C03)** – after projects.

---

### Phase 18: Professional CV, LinkedIn, Job Hunting & Expanded Interview Prep

- **CV**: 1 page, Projects first, Technical Skills, KSA Compliance line.
- **LinkedIn**: Headline “Cloud Engineer | AWS | Terraform | Python | KSA Compliance Ready”.
- **Target Roles**: Junior Cloud Engineer, AWS Cloud Support Associate, Cloud Operations.
- **Job Platforms**: LinkedIn Jobs, Bayt.com, Indeed.sa.
- **Interview Prep**:
  - Behavioral (STAR method)
  - Technical scenarios (troubleshooting static website, designing HA app, Security Group vs NACL, S3 recovery)
  - KSA-specific questions (PDPL, `me-south-1`, NCA CCC)
  - Live coding (Python/Bash whiteboarding)
- **Salary (2026 KSA entry)** : SAR 8,000 – 15,000/month + benefits.

---

### Phase 19: Multi-Cloud with Azure

- **🎓 Detailed Topics**: Azure fundamentals (Resource Groups, VMs, Blob Storage, VNet, Azure AD), comparison with AWS, Azure Arc.
- **🔗 Free Complete YouTube Course**: Search “Azure Fundamentals AZ-900” on freeCodeCamp.
- **🕹️ 3 Mini-Projects**:
  1. **Azure VM with Web Server**: Launch VM, configure NSG, install Nginx.
  2. **Azure Blob Storage Static Site**: Host static HTML with static website hosting.
  3. **Comparison Whitepaper**: Markdown document comparing AWS vs Azure core services.

---

### Phase 20: Read and Learn from AWS Architecture Diagrams

- **🎓 Detailed Topics**: Reading AWS architecture diagrams, Well-Architected Framework, common patterns (three-tier, microservices, event-driven), tools (draw.io, Miro).
- **🔗 Free Resources**: AWS Architecture Center, YouTube tutorials.
- **🕹️ 3 Mini-Projects**:
  1. **Re-draw a Sample Diagram**: Re-create a three-tier web app diagram using draw.io.
  2. **Document Your Capstone Architecture**: Create professional diagram for your Secure 3-Tier project.
  3. **Analyze a Real Architecture**: Write analysis of a reference architecture (e.g., serverless web app).


---

### Phase 21: Specialization - Cloud Security

- **🎓 Detailed Topics**: IAM advanced policies, VPC Flow Logs, WAF/Shield, KMS/CloudHSM, Config/Security Hub, GuardDuty/Inspector.
- **🔗 Free Resources**: freeCodeCamp security videos, AWS Security Hub.
- **🕹️ 3 Mini-Projects**:
  1. **IAM Policy Validator**: Python script flags overly permissive policies.
  2. **VPC Flow Logs Analyzer**: Parse logs, identify anomalous traffic.
  3. **Automated Compliance Scanner**: Python + boto3 checks resources against NCA ECC.

---

