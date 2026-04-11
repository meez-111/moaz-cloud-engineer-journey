
### 📘 The Ultimate Documentation System (Your Public Portfolio)

Before you write a single line of code, you will build your public brand. Create a single, well-organized GitHub repository named: **`moaz-cloud-engineer-journey`** .

This repository will be the central hub for your entire journey and your primary showcase for recruiters. Use this exact structure:

- `README.md`: A compelling overview of your journey, your goal, and a table of contents linking to everything below.
- `roadmap/`: The exact roadmap we are creating, with a checklist to track your progress.
- `phases/`: 
	- `phase no./`:
		- `topics notes/`
		- `course notes/`
		- `projects/`
- `ksa-compliance/`: Your detailed research on PDPL, NCA, etc., applied to your projects.
- `interview-prep/`: A living document of questions, answers, and your project explanations.

---

### Phase 1: Linux Fundamentals & OverTheWire Bandit Challenges 1m

- **🎓 Detailed Topics**: Filesystem hierarchy, permissions (`chmod`, `chown`), user/group management, process management (`ps`, `top`, `kill`), `systemd` (`systemctl`, `journalctl`), package managers (`apt`, `dnf`), cron jobs, basic text editors (`vim`, `nano`), and essential commands (`grep`, `awk`, `sed`, `find`).
- **🔗 Free Complete YouTube Course**:
	- [RedHat Linux System Administration I](https://www.youtube.com/playlist?list=PLvbyo73L4vfvxbFgbbCSNNWqO1HGvrws9). 15h
	- [RedHat Linux System Administration II](https://www.youtube.com/playlist?list=PLvbyo73L4vfslrED-KLJUyXOTDhIzvlCk). 10h
- **💀 OverTheWire Bandit (Bonus)**: Alongside the course, tackle the **Bandit wargame**. It's a series of ~30 challenges that teach real command-line skills through problem-solving.
- **🕹️ 3 Independent Mini-Projects**:
  1. **System Health Monitor**: A Bash script that logs CPU, memory, and disk usage every hour and alerts you if thresholds are exceeded.
  2. **Automated Backup Script**: Compresses a specified directory into a timestamped `.tar.gz` archive, moves it to a `/backups` folder, and deletes backups older than 7 days.
  3. **Log File Analyzer**: Scans a log file for a keyword like "ERROR" and outputs the count and the last 5 matching lines.

---

### Phase 2: Networking Fundamentals

- **🎓 Detailed Topics**: OSI model (focus on L4/TCP-UDP, L7/HTTP), IPv4 subnetting (CIDR), private vs. public IPs, DNS records (A, CNAME, MX), TCP 3-way handshake, UDP vs. TCP, HTTP methods and status codes, NAT, routing, ARP, and key troubleshooting tools (`ping`, `traceroute`, `dig`, `curl`, `tcpdump`).
- **🔗 Free Complete YouTube Course**: 
	- [CCNA](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ).
	- [ Every Networking Concept Explained In 20 Minutes](https://www.youtube.com/watch?v=xj_GjnD4uyI)
	- [Learn Networking In 25 MINUTES Networking Fundamentals + Cloud Networking Concepts](https://www.youtube.com/watch?v=bEFAFHIahXk)
- **What to watch (do not watch the full course)**:

| Order | Topic                          | Day(s)      | Estimated Video Time | Cloud Engineer Relevance                          | My Recommendation      |
|-------|--------------------------------|-------------|----------------------|---------------------------------------------------|------------------------|
| 1     | Network Devices                | Day 1      | 30 minutes          | Basics of routers, switches, firewalls            | Must Watch            |
| 2     | TCP/IP Model                   | Day 3      | 42 minutes          | Core networking model                             | Must Watch            |
| 3     | IPv4 Addressing                | Day 7–8    | 55 minutes          | Foundation for understanding IPs                  | Must Watch            |
| 4     | Routing                        | Day 11     | 40 minutes          | How routing and gateways work                     | Must Watch            |
| 5     | Life of a Packet               | Day 12     | 20 minutes          | Great visualization of traffic flow               | Must Watch            |
| 6     | Subnetting                     | Day 13–15  | 80 minutes          | **Most important** skill (CIDR for VPCs)          | Must Watch + Practice |
| 7     | VLANs                          | Day 16     | 35 minutes          | Cisco switching concept                           | **Skip for now**      |
| 8     | TCP & UDP                      | Day 30     | 38 minutes          | Ports, 3-way handshake, reliability               | Must Watch            |
| 9     | IPv6                           | Day 31     | 32 minutes          | Future-proofing, but rarely used early            | Optional / Skim       |
| 10    | DNS                            | Day 38     | 33 minutes          | DNS records & resolution (very useful)            | Must Watch            |
| 11    | DHCP                           | Day 39     | 28 minutes          | How IPs are assigned automatically                | Skim / Optional       |
| 12    | SSH                            | Day 42     | 30 minutes          | Daily tool for accessing Linux/EC2 servers        | Recommended           |
| 13    | NAT                            | Day 44–45  | 65 minutes          | Private vs Public IPs – critical for cloud        | Must Watch            |

### Total Estimated Time
- **All 13 items**: **≈ 8 hours 8 minutes** (about **8–9 hours** including short breaks or rewatching difficult parts)
- 
- Spend extra time on **Subnetting (Days 13–15)** and **NAT (Days 44–45)** — these two will help you the most in AWS VPC design later.

- **🕹️ 3 Independent Mini-Projects**:
  1. **Network Scanner**: A Bash script to `ping` sweep a local subnet and discover all active hosts.
  2. **DNS Lookup Tool**: A Bash script that takes a domain name and prints its A and AAAA records using `dig`.
  3. **Port Scanner**: A Bash script using `nc` (netcat) to check if specific ports (e.g., 22, 80, 443) are open on a target host.

---

### Phase 3: Database Administration

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
- **🔗 Free Complete YouTube Course**: [Git & GitHub Crash Course for Beginners 2026](https://www.youtube.com/watch?v=mAFoROnOfHs). 1.20h
- **🕹️ 3 Independent Mini-Projects**:
  1. **Repo Setup**: Create a local repo, add a `README.md`, commit, and push to GitHub.
  2. **Feature Branch Workflow**: Create a branch, add a new file, and merge it back to `main`.
  3. **Simulate Merge Conflict**: Create a conflict on purpose and resolve it manually.

---

### Phase 5: Bash Scripting for System Automation

- **🎓 Detailed Topics**: Shebang, variables, command-line arguments, conditionals (`if`), loops (`for`, `while`), functions, exit codes, text processing (`grep`, `sed`, `awk`), and scheduling with `cron`.
- **🔗 Free Complete YouTube Course**: [Bash Scripting Tutorial for Beginners by nana](https://www.youtube.com/watch?v=PNhq_4d-5ek)1:05h.
- **🕹️ 3 Attractive Mini-Projects**:
  1. **Intelligent Backup Rotator**: Instead of just deleting old backups, this script compresses directories, moves them to a `/backups` folder, **and** keeps a configurable number of the most recent backups (e.g., keep last 5). It logs all actions.
  2. **Automated Server Hardening Toolkit**: A script that asks for a username, creates the user, adds them to the `sudo` group, disables root SSH login, and sets up a basic firewall (`ufw`) with only SSH and HTTP allowed.
  3. **Custom System Report Generator**: A script that generates a beautiful HTML report (using `echo` and HTML tags) showing system uptime, memory usage, disk usage, and logged-in users.

---

### Phase 6: Python (6+ Projects)

- **🎓 Detailed Topics**: Python data types, lists, dictionaries, loops, functions, file I/O (`open`, `read`, `write`), the `requests` library for APIs, `json` parsing, error handling (`try/except`).
- **🔗 Free Complete YouTube Course**:
	- [Python Tutorial for Beginners](https://www.youtube.com/watch?v=t8pPdKYpowI) 5:30h
	- https://www.youtube.com/playlist?list=PLtGOJcWqvbqdzCjZAcXF02h4cWiPVnpyD
	- https://www.youtube.com/playlist?list=PLiEts138s9P0aG6soKBoMsmJrwIOPXoXR
	- https://www.youtube.com/watch?v=WYp0dmZOHXM
	- https://www.youtube.com/watch?v=ng2o98k983k
	- https://www.youtube.com/watch?v=taL3r_JpwBg
	- https://www.youtube.com/watch?v=XVv6mJpFOb0
	- https://www.youtube.com/watch?v=UOsRrxMKJYk
	- https://www.youtube.com/watch?v=1kOU-i4jNas
	- https://www.youtube.com/watch?v=jNoTEiI2cVU
	- https://www.youtube.com/watch?v=NB8OceGZGjA
	- https://www.youtube.com/playlist?list=PLqXS1b2lRpYSkvxnk3quzKL08oRJiP9LA
	- https://www.youtube.com/watch?v=mBoX_JCKZTE

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
- **🔗 Free Complete YouTube Course**:
- [شرح تفصيلي لل Cloud Computing وازاي تبدأ فيه في أقل من 20 دقيقة](https://www.youtube.com/watch?v=nlZunZM92_A)
- [Cloud Computing Explained: The Most Important Concepts To Know](https://www.youtube.com/watch?v=ZaA0kNm18pE) 45m
- **🕹️ 3 Mini-Projects**:
  1. **Service Model Comparison**: Markdown table with IaaS/PaaS/SaaS examples and responsibility division.
  2. **DR Plan**: Write a DR plan for an e-commerce site (RTO=2h, RPO=15min).
  3. **Cost Analysis**: Compare On-Demand vs Reserved Instance pricing.

---

### Phase 8: AWS Cloud Practitioner (freeCodeCamp)

- **🎓 Detailed Topics**: AWS Global Infrastructure (Regions, AZs), Compute (EC2, Lambda), Networking (VPC, Route 53, CloudFront), Storage (S3, EBS, EFS), Databases (RDS, DynamoDB), Security (IAM, KMS, CloudTrail), Billing & Pricing, Well-Architected Framework.
- **🔗 Free Complete YouTube Course**: [ AWS Certified Cloud Practitioner Certification Course (CLF-C02) - Pass the Exam](https://www.youtube.com/watch?v=NhDYbskXRgc) 14h
- https://www.exampro.co/aws-choose-an-exam
- **🕹️ 3 Mini-Projects**:
  1. **S3 Static Website**: Host an `index.html` on S3 with public read policy.
  2. **EC2 Web Server**: Launch `t2.micro`, install Nginx, serve "Hello from EC2".
  3. **IAM User & Group**: Create "Developers" group with `ReadOnlyAccess` to EC2.


---

### Phase 9: AWS Solutions Architect Associate (freeCodeCamp)

- **🎓 Detailed Topics**: S3 (lifecycle policies, versioning, replication), VPC (custom VPC, public/private subnets, IGW, NAT Gateway), EC2 (instance families, pricing models), RDS (read replicas, Multi-AZ) vs DynamoDB, ALB, Auto Scaling Groups.
- **🔗 Free Complete YouTube Course**: [AWS Solutions Architect Associate Certification (SAA-C03) – Full Course to PASS the Exam](https://www.youtube.com/watch?v=c3Cn4xYfxJY). 50h
- **🕹️ 3 Mini-Projects**:
  1. **HA with ALB + ASG**: ASG with 2 instances across 2 AZs behind an ALB.
  2. **Custom VPC**: VPC with public/private subnets, IGW, NAT Gateway.
  3. **Serverless Lambda + DynamoDB**: Lambda writes a test item to DynamoDB.

---

### Phase 10: Python for cloud automation (boto3)

- **🎓 Detailed Topics**: Boto3.
- **🔗 Free Complete YouTube Course**: 
- [Automate AWS Infrastructure Provisioning using boto3](https://www.youtube.com/playlist?list=PL2qzCKTbjutJ1zZFYNImrHNbzs6XgIHbI)
- [  Hands-on Python With AWS Boto3 | AWS Infrastructure Automation | CI CD](https://www.youtube.com/watch?v=iLv1vJd4URg) 2h
- [ Day 13 Python For DevOps  Boto3 Begineer to Advanced Guide with Projects](https://www.youtube.com/watch?v=3ExnySHBO6k) 1:48h
- **🕹️ 3 Mini-Projects**:
  1. **IAM Security Auditor**: A Python script that audits your AWS account and finds:
	- Users with **admin privileges**
	- **Unused IAM users**
	- **Old access keys (>90 days)**
	- Overly permissive policies (`*:*`)
  2. **EC2 Cost Optimizer**: Script that:
	- Lists all EC2 instances
	- Detects:
	    - **Stopped instances**
	    - **Low CPU usage (idle)**
	- Suggests or automatically:
	    - Stops them
	    - Tags them for cleanup
  3. **S3 Smart Backup & Compliance Tool**: A script that:
	- Uploads files to S3
	- Ensures:
	    - **Encryption enabled**
	    - **Versioning ON**
	- Applies:
	    - Lifecycle policy (auto-delete after X days)

---

### Phase 11: Virtualization & DevOps Principles

- **🎓 Detailed Topics**: Virtualization (VMs vs Containers, hypervisors), DevOps principles (CI/CD pipeline, The Three Ways).
- **🔗 Free Resources**: YouTube search "Virtualization vs Containerization", "DevOps Principles for Beginners".
- **🕹️ 3 Mini-Projects**:
  1. **VirtualBox Lab**: Set up a Linux VM, install a web server, access from host.
  2. **Concept Map**: Markdown document with diagram comparing VMs and containers.
  3. **DevOps in a Nutshell**: Blog post explaining DevOps lifecycle, CI/CD, IaC, Monitoring.

---

### Phase 12: Containers & Orchestration (Docker & Kubernetes)

- **🎓 Detailed Topics**: Docker (`Dockerfile`, images, containers, volumes, Docker Compose). Kubernetes (Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Persistent Volumes).
- **🔗 Free Complete YouTube Course**: 
	- [Docker Tutorial for Beginners FULL COURSE in 3 Hours](https://www.youtube.com/watch?v=3c-iBn73dDE)
	- [Kubernetes Tutorial for Beginners FULL COURSE in 4 Hours](https://www.youtube.com/watch?v=X48VuDVv0do)
- **🕹️ 3 Mini-Projects**:
  1. **Containerize a Python App**: Write `Dockerfile`, build, run locally.
  2. **Local K8s with Minikube**: Deploy app as Deployment, expose via NodePort Service.
  3. **ConfigMap & Secret**: Deploy app reading config from ConfigMap and password from Secret.

---

### Phase 13: Infrastructure as Code (IaC) with Terraform

- **🎓 Detailed Topics**: Declarative syntax, HCL, providers, resources, variables, outputs, `terraform plan/apply/destroy`, state management, modules.
- **🔗 Free Complete YouTube Course**:
	- [Terraform explained in 15 mins | Terraform Tutorial for Beginners](https://www.youtube.com/watch?v=l5k1ai_GBDE)
	- [Complete Terraform Course - From BEGINNER to PRO! (Learn Infrastructure as Code)](https://www.youtube.com/watch?v=7xngnjfIlK4)
	- [Terraform Course - Automate your AWS cloud infrastructure](https://www.youtube.com/watch?v=SLB_c_ayRMo)
	- [Terraform Tutorial for Beginners + Labs: Complete Step by Step Guide!](https://www.youtube.com/watch?v=YcJ9IeukJL8)
- **🕹️ 3 Mini-Projects**:
  1. **Codify a Single EC2 Instance**: Terraform to launch EC2 with SSH security group.
  2. **Codify the Custom VPC**: Terraform for VPC, subnets, IGW, NAT.
  3. **Terraform Modules**: Refactor VPC into reusable module for dev/staging.

---

### Phase 14: CI/CD & Automation (GitHub Actions)

- **🎓 Detailed Topics**: YAML workflows, triggers, jobs, steps, actions, secrets, artifacts.
- **🔗 Free Complete YouTube Course**:
	- [GitHub Actions Tutorial - Basic Concepts and CI/CD Pipeline with Docker](https://www.youtube.com/watch?v=R8_veQiYBjI)
	- [ Complete GitHub Actions Course - From BEGINNER to PRO](https://www.youtube.com/watch?v=Xwpi0ITkL3U)
- **🕹️ 3 Mini-Projects**:
  1. **Simple Linter**: Workflow that runs `pylint` on every push.
  2. **Auto-Deploy to S3**: Workflow that builds static site and syncs to S3 on push to `main`.
  3. **Terraform CI/CD**: Workflow that runs `plan` on PRs and `apply` on merge to `main`.

---

### Phase 15: Monitoring, Observability & Logging (Prometheus & Grafana)

- **🎓 Detailed Topics**: Metrics, logs, traces. Prometheus (metrics collection, PromQL), Grafana (dashboards, alerting).
- **🔗 Free Complete YouTube Course**:
	- Monitoring and Observability concepts:
		- [0Observability vs Monitoring - Whats the difference?](https://www.youtube.com/watch?v=ytx6jr2TyxI)
		- [Observability vs Monitoring](https://www.youtube.com/watch?v=VzmM5iHqq8w)
		- [Observability vs Monitoring vs APM vs Logging vs Alerting](https://www.youtube.com/watch?v=TYE2u7QZNVA)
		- [monitoring & Observability Explained: Metrics, Logging & Tracing for Beginners](https://www.youtube.com/watch?v=C0BJb-VWt1I)
		- [observability vs. APM vs. Monitoring](https://www.youtube.com/watch?v=CAQ_a2-9UOI)
		- [OBSERVABILITY FROM SCRATCH بالعربي](https://www.youtube.com/playlist?list=PLTRDUPO2OmImfWPK4cSusvHoEV6KWeXNm)
		- [Monitoring & Observability - تيك بودكاست بالعربي](https://www.youtube.com/watch?v=iNO1bNaYAAU)
	- Prometheus & Grafana:
		- [How Prometheus Monitoring works | Prometheus Architecture explained](https://www.youtube.com/watch?v=h4Sl21AKiDg)
		- [ Prometheus and Grafana for Monitoring and Observability - For Beginners](https://www.youtube.com/watch?v=L-dDeZjZUiA)
		- [Observability Zero to Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvJUIfwmmVDoPYqXXUNbdBmb)
		- [Prometheus Fundamentals](https://www.youtube.com/playlist?list=PLyBW7UHmEXgylLwxdVbrBQJ-fJ_jMvh8h)
- **🕹️ 3 Mini-Projects**:
  1. **Local Prometheus + Grafana Stack**: Docker Compose to spin up both.
  2. **Monitor a Local App**: Configure Prometheus to scrape metrics from EC2, visualize in Grafana.
  3. **Set Up an Alert**: Grafana alert for CPU >80% with test notification.

---

### Phase 16: The 3 Major Capstone Projects

1. **Official Cloud Resume Challenge**: S3 + CloudFront + API Gateway + Lambda + DynamoDB + Terraform + GitHub Actions.
2. **Secure 3‑Tier Production App**: VPC with public/private subnets, ALB, ASG, RDS Multi-AZ, KMS encryption, least-privilege IAM.
3. **Serverless Event‑Driven Backend**: S3 trigger → Lambda (process file) → DynamoDB + SNS notification.

---

### Phase 17: Saudi Arabia Regulations & Compliance

- **🎓 Detailed Topics**: PDPL (data localization, consent, breach notification), NCA (ECC, CCC), CST regulations, use of `me-south-1` region.
- **🔗 Free Resources**: YouTube search “Saudi PDPL overview 2025”, “NCA ECC explained”.
- **🕹️ 3 Mini Compliance Projects**:
  1. **Region Compliance Checker**: Python + boto3 script flags non-`me-south-1` resources.
  2. **PDPL Compliance Guide**: Markdown document for data encryption, access logging, retention.
  3. **NCA ECC Mapper**: Spreadsheet mapping ECC controls to AWS services.

---

### Phase 18: Certifications

- **AWS Cloud Practitioner (CLF-C02)** – free AWS Skill Builder + freeCodeCamp practice.
- **AWS Solutions Architect – Associate (SAA-C03)** – after projects.

---

### Phase 19: Professional CV, LinkedIn, Job Hunting & Expanded Interview Prep

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

### Phase 20: Multi-Cloud with Azure

- **🎓 Detailed Topics**: Azure fundamentals (Resource Groups, VMs, Blob Storage, VNet, Azure AD), comparison with AWS, Azure Arc.
- **🔗 Free Complete YouTube Course**:
	- [90% Of Azure EXPLAINED In 20 Minutes | COMPLETE Crash Course For Beginners](https://www.youtube.com/watch?v=liRgZeF6mbk)
	- [Microsoft Azure Fundamentals Certification Course (AZ-900) UPDATED – Pass the exam in 8 hours!](https://www.youtube.com/watch?v=5abffC-K40c)
	- [Microsoft Azure Fundamentals (AZ-900) Full Course](https://www.youtube.com/playlist?list=PLGjZwEtPN7j-Q59JYso3L4_yoCjj2syrM)
- **🕹️ 3 Mini-Projects**:
  1. **Azure VM with Web Server**: Launch VM, configure NSG, install Nginx.
  2. **Azure Blob Storage Static Site**: Host static HTML with static website hosting.
  3. **Comparison Whitepaper**: Markdown document comparing AWS vs Azure core services.

---

### Phase 21: Read and Learn from AWS Architecture Diagrams

- **🎓 Detailed Topics**: Reading AWS architecture diagrams, Well-Architected Framework, common patterns (three-tier, microservices, event-driven), tools (draw.io, Miro).
- **🔗 Free Resources**:
- [How to Create Engaging Architecture Diagrams Using AWS](https://www.youtube.com/watch?v=eEbstFkbl9w)
- [AWS Architecture Diagramming For Beginners | How to Draw Cloud Architecture Diagrams AWS](https://www.youtube.com/watch?v=tSqEljKKiU0)
- [How to Create AWS Architecture Diagrams | Lucidchart Demo](https://www.youtube.com/watch?v=5oonyR-CyME)
- [Real Life AWS Project Architectures](https://www.youtube.com/playlist?list=PL9nWRykSBSFgPhu5u5-ci5U45OOO9np5q)
- [AWS Interview Prep: Designing an eCommerce Architecture from Scratch](https://www.youtube.com/watch?v=f-rl_4Pd8dw)
- [AWS Reference Architecture Diagrams](https://aws.amazon.com/architecture/reference-architecture-diagrams/?solutions-all.sort-by=item.additionalFields.sortDate&solutions-all.sort-order=desc&whitepapers-main.sort-by=item.additionalFields.sortDate&whitepapers-main.sort-order=desc&awsf.whitepapers-tech-category=*all&awsf.whitepapers-industries=*all)
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/)
- [This is My Architecture](https://www.youtube.com/playlist?list=PLhr1KZpdzukdeX8mQ2qO73bg6UKQHYsHb)
- [AWS re:Invent 2021 - AWS Security Reference Architecture: Visualize your security](https://www.youtube.com/watch?v=-_LzB1uibAs)
- **🕹️ 3 Mini-Projects**:
  1. **Re-draw a Sample Diagram**: Re-create a three-tier web app diagram using draw.io.
  2. **Document Your Capstone Architecture**: Create professional diagram for your Secure 3-Tier project.
  3. **Analyze a Real Architecture**: Write analysis of a reference architecture (e.g., serverless web app).


---

### Phase 22: Specialization - Cloud Security

- **🎓 Detailed Topics**: IAM advanced policies, VPC Flow Logs, WAF/Shield, KMS/CloudHSM, Config/Security Hub, GuardDuty/Inspector.
- **🔗 Free Resources**:
- [AWS Cloud Security Full Course for Beginners2026](https://www.youtube.com/watch?v=XsRBDJ5hcdg)
- [AWS Cloud Security Crash Course | Free Cloud Security Training | Security Assessment](https://www.youtube.com/watch?v=amCrXVFX1C4)
- [AWS re:Inforce 2019: The Fundamentals of AWS Cloud Security (FND209-R)](https://www.youtube.com/watch?v=-ObImxw1PmI)
- [Intro to Cloud Security | AWS Cloud Security Fundamentals](https://www.youtube.com/watch?v=lwzvr0s9jO4)
- [AWS Cloud Security BootCamp 2023](https://www.youtube.com/playlist?list=PLrU93JvkXVl5TamdCdCwzqFs6vt5vySFi)
- [AWS Security Specialty Certification Full Course](https://www.youtube.com/watch?v=9CoMa2D7LwI)
- 
- **🕹️ 3 Mini-Projects**:
  1. **IAM Policy Validator**: Python script flags overly permissive policies.
  2. **VPC Flow Logs Analyzer**: Parse logs, identify anomalous traffic.
  3. **Automated Compliance Scanner**: Python + boto3 checks resources against NCA ECC.

---

