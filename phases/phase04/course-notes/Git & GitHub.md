# Git & GitHub

## Table of Contents

- [Git \& GitHub](#git--github)
  - [Table of Contents](#table-of-contents)
  - [1. What is Version Control? Why Do We Need It?](#1-what-is-version-control-why-do-we-need-it)
  - [2. Git vs. GitHub – The Difference](#2-git-vs-github--the-difference)
  - [3. Core Concepts – Local and Remote](#3-core-concepts--local-and-remote)
  - [4. The Three Local States – Working Directory, Staging, Commit](#4-the-three-local-states--working-directory-staging-commit)
  - [5. Installing Git](#5-installing-git)
  - [6. Creating a Local Repository (`git init`)](#6-creating-a-local-repository-git-init)
  - [7. Connecting to a Remote Repository (GitHub)](#7-connecting-to-a-remote-repository-github)
    - [7.1 Creating a Remote Repo on GitHub](#71-creating-a-remote-repo-on-github)
    - [7.2 Cloning a Remote Repo (`git clone`)](#72-cloning-a-remote-repo-git-clone)
  - [8. Tracking Changes – `git status` and `git add`](#8-tracking-changes--git-status-and-git-add)
    - [`git status` – See what has changed](#git-status--see-what-has-changed)
    - [`git add` – Move changes to the staging area](#git-add--move-changes-to-the-staging-area)
    - [Unstage (`git reset`)](#unstage-git-reset)
    - [Remove file from working directory and stage (`git rm`)](#remove-file-from-working-directory-and-stage-git-rm)
  - [9. Committing Changes – `git commit`](#9-committing-changes--git-commit)
    - [Basic commit:](#basic-commit)
    - [Configure your identity (required before first commit):](#configure-your-identity-required-before-first-commit)
    - [Amend the last commit (if you forgot to include a file):](#amend-the-last-commit-if-you-forgot-to-include-a-file)
  - [10. Viewing Commit History – `git log`](#10-viewing-commit-history--git-log)
    - [Full log:](#full-log)
    - [Compact one‑line view:](#compact-oneline-view)
    - [Show changes in a commit:](#show-changes-in-a-commit)
  - [11. Branching – `git branch` and `git checkout` / `git switch`](#11-branching--git-branch-and-git-checkout--git-switch)
    - [View branches:](#view-branches)
    - [Create a new branch:](#create-a-new-branch)
    - [Switch to another branch:](#switch-to-another-branch)
    - [Create and switch in one command:](#create-and-switch-in-one-command)
    - [Rename a branch:](#rename-a-branch)
    - [Delete a branch:](#delete-a-branch)
  - [12. Merging Branches – `git merge` and Resolving Conflicts](#12-merging-branches--git-merge-and-resolving-conflicts)
    - [Merge a branch into the current branch:](#merge-a-branch-into-the-current-branch)
    - [Merge Conflicts – When Git Can't Automatically Merge](#merge-conflicts--when-git-cant-automatically-merge)
  - [13. Rebasing – `git rebase` (Clean History)](#13-rebasing--git-rebase-clean-history)
  - [14. Undoing Changes – `git reset`, `git revert`, `git restore`](#14-undoing-changes--git-reset-git-revert-git-restore)
  - [15. Stashing Unfinished Work – `git stash`](#15-stashing-unfinished-work--git-stash)
    - [Save changes:](#save-changes)
    - [List stashes:](#list-stashes)
    - [Apply and remove the most recent stash:](#apply-and-remove-the-most-recent-stash)
    - [Apply without removing:](#apply-without-removing)
    - [Apply a specific stash:](#apply-a-specific-stash)
    - [Drop a specific stash:](#drop-a-specific-stash)
    - [Clear all stashes:](#clear-all-stashes)
  - [16. Remote Workflows – `git push`, `git pull`, `git fetch`](#16-remote-workflows--git-push-git-pull-git-fetch)
    - [`git push` – Upload local commits to remote](#git-push--upload-local-commits-to-remote)
    - [`git pull` – Download and merge remote changes](#git-pull--download-and-merge-remote-changes)
    - [`git fetch` – Download remote changes without merging](#git-fetch--download-remote-changes-without-merging)
  - [17. Comparing Commits – `git diff`](#17-comparing-commits--git-diff)
    - [Compare working directory with staging:](#compare-working-directory-with-staging)
    - [Compare staged changes with last commit:](#compare-staged-changes-with-last-commit)
    - [Compare two commits:](#compare-two-commits)
    - [Compare two branches:](#compare-two-branches)
  - [18. Collaboration with Pull Requests (PRs)](#18-collaboration-with-pull-requests-prs)
  - [19. Git in Cloud Engineering – Why It Matters](#19-git-in-cloud-engineering--why-it-matters)
  - [20. Quick Reference Table](#20-quick-reference-table)
  - [21. Practice Lab – Verify Your Understanding](#21-practice-lab--verify-your-understanding)

---

## 1. What is Version Control? Why Do We Need It?

**Version control** (also called source control) is a system that records changes to a file or set of files over time so that you can recall specific versions later.

**Why we need it:**
- **Track history** – See who changed what, when, and why.
- **Rollback** – Revert to a previous state if something breaks.
- **Collaboration** – Multiple developers can work on the same project simultaneously.
- **Branching** – Experiment with new features without affecting the main codebase.
- **Backup** – Remote repositories act as a safe backup.

**Examples of version control systems:**
- **Git** – distributed, most popular (used by GitHub, GitLab, Bitbucket).
- **SVN (Subversion)** – centralised (older).
- **Mercurial** – distributed (less common).

---

## 2. Git vs. GitHub – The Difference

| **Git** | **GitHub** |
|---------|------------|
| A **distributed version control system** (DVCS) that runs locally on your machine. | A **cloud‑based hosting service** for Git repositories. |
| Tracks changes, manages branches, commits, and history. | Provides a central server for collaboration, code review, CI/CD, and project management. |
| Works offline – all operations (commit, branch, log) are local. | Requires an internet connection for `push`, `pull`, and `clone`. |
| Command‑line tool (also GUI clients available). | Web interface with issues, pull requests, actions, and project boards. |

**Other Git hosting services:** GitLab, Bitbucket, Azure DevOps, AWS CodeCommit.

---

## 3. Core Concepts – Local and Remote

```
┌─────────────────────────────────────────────────────────────┐
│                        LOCAL (your computer)                │
│  ┌───────────────┐    ┌───────────────┐    ┌─────────────┐ │
│  │ Working       │    │    Staging    │    │   Local     │ │
│  │ Directory     │───▶│    Area       │───▶│ Repository  │ │
│  │ (files you    │    │  (index)      │    │  (commits)  │ │
│  │ are editing)  │    │               │    │             │ │
│  └───────────────┘    └───────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ push / pull
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        REMOTE (GitHub / GitLab)             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Remote Repository                     │ │
│  │  (shared with team, backed up, accessible from anywhere)│ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

- **Working Directory** – the files you are currently editing on your machine.
- **Staging Area (Index)** – a temporary holding area where you prepare changes before committing.
- **Local Repository** – the `.git` directory that stores your commit history on your local machine.
- **Remote Repository** – a copy of the repository hosted on a server (e.g., GitHub, GitLab).

---

## 4. The Three Local States – Working Directory, Staging, Commit

```
1. Working Directory        2. Staging Area             3. Local Repository
   (modified files)    →     (staged files)        →     (committed snapshots)
```

| State | Description | Command to Move |
|-------|-------------|-----------------|
| **Modified** | Files have changed in the working directory. | `git add` → stages changes |
| **Staged** | Changes are marked to be included in the next commit. | `git commit` → saves to repo |
| **Committed** | Changes are permanently saved in the local repository. | (already committed) |

**One‑liner:**  
`git add` moves changes from **modified** to **staged**.  
`git commit` moves changes from **staged** to **committed**.

---

## 5. Installing Git

**Linux (RHEL / CentOS / Fedora):**
```bash
sudo dnf install git
```

**Linux (Ubuntu / Debian):**
```bash
sudo apt install git
```

**macOS (Homebrew):**
```bash
brew install git
```

**Windows:** Download from [git-scm.com](https://git-scm.com/) – includes Git Bash (a Unix‑like shell).

**Verify installation:**
```bash
git --version
# Example output: git version 2.43.0
```

---

## 6. Creating a Local Repository (`git init`)

**Initialize a new repository:**

```bash
mkdir git-one
cd git-one
touch 1.txt 2.txt
mkdir myfolder
cd myfolder
touch 3.txt
cd ..
```

```bash
git init
# Initialized empty Git repository in /path/to/git-one/.git
```

A hidden `.git` folder is created – this contains all the repository metadata. **Do not delete it.**

**Check status:**
```bash
git status
# On branch master
# No commits yet
# Untracked files: 1.txt, 2.txt, myfolder/
```

---

## 7. Connecting to a Remote Repository (GitHub)

### 7.1 Creating a Remote Repo on GitHub

1. Log in to [GitHub.com](https://github.com).
2. Click **New repository** (green button).
3. Give it a name (e.g., `my-first-repo`).
4. Choose **Public** or **Private**.
5. **Do not** initialize with README, .gitignore, or license (if you want to push an existing local repo).
6. Click **Create repository**.

### 7.2 Cloning a Remote Repo (`git clone`)

If you are **starting from a remote repo** (instead of creating locally first):

```bash
git clone https://github.com/yourusername/repo-name.git
```

This creates a local copy with the remote automatically configured.

---

## 8. Tracking Changes – `git status` and `git add`

### `git status` – See what has changed

```bash
git status
```

**Typical output:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
    1.txt
    2.txt
    myfolder/
```

### `git add` – Move changes to the staging area

| Command | Effect |
|---------|--------|
| `git add file.txt` | Stage a specific file. |
| `git add *.txt` | Stage all .txt files. |
| `git add .` | Stage all changes in the **current directory and subdirectories**. |
| `git add -A` or `git add --all` | Stage all changes in the **entire project** (including deletions). |

**Examples:**
```bash
git add 1.txt
git add *.txt
git add myfolder/
git add -A                # stage everything
```

### Unstage (`git reset`)

```bash
git reset                # unstage all staged files
git reset file.txt       # unstage a specific file
```

### Remove file from working directory and stage (`git rm`)

```bash
git rm file.txt          # remove file and stage the deletion
git rm -r folder/        # remove folder and all contents
```

---

## 9. Committing Changes – `git commit`

Once files are staged, you commit them to the local repository.

### Basic commit:

```bash
git commit -m "Add initial project files"
```

### Configure your identity (required before first commit):

```bash
git config --global user.email "your.email@example.com"
git config --global user.name "Your Name"
```

- **`--global`** – applies to all repositories on this machine.
- **`--local`** – applies only to the current repository (override global).

### Amend the last commit (if you forgot to include a file):

```bash
git add forgotten-file.txt
git commit --amend -m "Updated commit message"
```

---

## 10. Viewing Commit History – `git log`

### Full log:

```bash
git log
```

### Compact one‑line view:

```bash
git log --oneline
# Example output:
# a1b2c3d Add project files
# e4f5g6h Initial commit
```

### Show changes in a commit:

```bash
git show commit_id
```

---

## 11. Branching – `git branch` and `git checkout` / `git switch`

**Branching** allows you to work on features isolated from the main codebase.

### View branches:

```bash
git branch
# * main   ← indicates current branch
```

### Create a new branch:

```bash
git branch feature-login
```

### Switch to another branch:

```bash
git checkout feature-login
# or (modern Git):
git switch feature-login
```

### Create and switch in one command:

```bash
git checkout -b feature-login
```

### Rename a branch:

```bash
git branch -m old-name new-name
```

### Delete a branch:

```bash
git branch -d feature-login        # safe delete (only if merged)
git branch -D feature-login        # force delete (unmerged)
```

---

## 12. Merging Branches – `git merge` and Resolving Conflicts

### Merge a branch into the current branch:

```bash
git checkout main
git merge feature-login
```

### Merge Conflicts – When Git Can't Automatically Merge

Conflicts happen when two branches modify the **same lines** in the **same file**.

**Conflict markers in the file:**

```
<<<<<<< HEAD
This is the main branch version
=======
This is the feature branch version
>>>>>>> feature-login
```

**How to resolve:**
1. Open the file in your editor.
2. Choose which version to keep (or combine them).
3. Delete the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Save the file.
5. `git add` the resolved file.
6. `git commit` to complete the merge.

---

## 13. Rebasing – `git rebase` (Clean History)

**Rebasing** rewrites commit history to make it linear, avoiding merge commits.

```bash
git checkout feature
git rebase main
```

This takes the commits from `feature` and replays them on top of the latest `main`.

**When to use:**
- To keep a clean, linear history.
- Before merging a feature branch into `main`.

**Difference:**
- `merge` – preserves the branching structure, creates a merge commit.
- `rebase` – rewrites history, no merge commit, linear.

**Best practice:** Do not rebase branches that others are working on (shared branches). Only rebase local, private branches.

---

## 14. Undoing Changes – `git reset`, `git revert`, `git restore`

| Command | Effect | Use Case |
|---------|--------|----------|
| `git restore file.txt` | Discard changes in working directory. | Undo uncommitted changes. |
| `git restore --staged file.txt` | Unstage a file (but keep changes). | Remove from staging. |
| `git reset HEAD~` | Undo the last commit (keep changes in working directory). | "Soft" reset. |
| `git reset --hard HEAD~` | Undo the last commit **and** discard changes. | Dangerous – permanent loss. |
| `git revert commit_id` | Create a new commit that undoes a previous commit. | Safest way to undo a pushed commit. |

**Visual:**
```
Before: A → B → C (head)
git revert C → creates new commit D that undoes C
A → B → C → D

git reset --hard HEAD~1
A → B   (C is removed)
```

**Recover a lost commit:** Use `git reflog` to find the commit hash and `git reset --hard hash`.

---

## 15. Stashing Unfinished Work – `git stash`

Stashing saves your uncommitted changes so you can switch branches without losing work.

### Save changes:

```bash
git stash
```

### List stashes:

```bash
git stash list
# stash@{0}: WIP on feature: a1b2c3d Add new feature
```

### Apply and remove the most recent stash:

```bash
git stash pop
```

### Apply without removing:

```bash
git stash apply
```

### Apply a specific stash:

```bash
git stash pop stash@{1}
```

### Drop a specific stash:

```bash
git stash drop stash@{0}
```

### Clear all stashes:

```bash
git stash clear
```

---

## 16. Remote Workflows – `git push`, `git pull`, `git fetch`

### `git push` – Upload local commits to remote

```bash
git push origin main
```
- `origin` = default name for the remote repository.
- `main` = branch name.

**First push (set upstream):**
```bash
git push -u origin main
```

### `git pull` – Download and merge remote changes

```bash
git pull origin main
```
This is equivalent to `git fetch` + `git merge`.

### `git fetch` – Download remote changes without merging

```bash
git fetch origin
```
Fetch downloads the latest commits from the remote but does **not** merge them. You can inspect them before merging.

---

## 17. Comparing Commits – `git diff`

### Compare working directory with staging:

```bash
git diff
```

### Compare staged changes with last commit:

```bash
git diff --staged
```

### Compare two commits:

```bash
git diff commit_id1 commit_id2
```

### Compare two branches:

```bash
git diff main..feature
```

---

## 18. Collaboration with Pull Requests (PRs)

A **Pull Request** is a GitHub feature that allows developers to propose changes and request review before merging into the main branch.

**Workflow:**

```
1. Fork the repository (create your own copy).
2. Clone your fork locally.
3. Create a feature branch.
4. Make changes, commit, push to your fork.
5. Open a Pull Request on the original repo.
6. Team reviews, discusses, requests changes.
7. Once approved, merge the PR (or squash and merge).
```

**PR benefits:**
- Code review (catches bugs early).
- Automated CI/CD checks (tests, linting, security scans).
- Documentation of changes.

**PR types on GitHub:**
- **Merge commit** – preserves all commits.
- **Squash and merge** – condenses all commits into one.
- **Rebase and merge** – linear history.

---

## 19. Git in Cloud Engineering – Why It Matters

| Cloud Context | Git Role |
|---------------|----------|
| **Infrastructure as Code (IaC)** | Store Terraform, CloudFormation, Ansible code in Git. |
| **CI/CD Pipelines** | Git triggers builds, tests, and deployments (GitHub Actions, GitLab CI). |
| **Collaboration** | Teams collaborate on infrastructure code via PRs. |
| **Audit and Compliance** | Git history provides an audit trail of who changed what. |
| **Rollback** | Revert to a known‑good state after failed deployments. |

**Example:** A GitHub Actions workflow that runs `terraform plan` on PRs and `terraform apply` on merge to `main`.

---

## 20. Quick Reference Table

| Task | Command |
|------|---------|
| Initialize a repo | `git init` |
| Clone a repo | `git clone <url>` |
| Check status | `git status` |
| Stage all changes | `git add -A` |
| Stage specific file | `git add file.txt` |
| Unstage | `git reset` |
| Commit | `git commit -m "message"` |
| View commit log | `git log --oneline` |
| Create a branch | `git branch feature` |
| Switch branch | `git checkout feature` or `git switch feature` |
| Merge branch | `git merge feature` |
| Rebase branch | `git rebase main` |
| Resolve merge conflicts | Manual edit + `git add` + `git commit` |
| Undo commit (soft) | `git reset HEAD~` |
| Undo commit (hard) | `git reset --hard HEAD~` |
| Revert commit | `git revert commit_id` |
| Stash changes | `git stash` |
| Apply stash | `git stash pop` |
| Push to remote | `git push origin main` |
| Pull from remote | `git pull origin main` |
| Fetch remote changes | `git fetch origin` |
| Compare branches | `git diff main..feature` |
| View reflog | `git reflog` |

---

## 21. Practice Lab – Verify Your Understanding

1. **Initialize a repo:** Create a directory `git-lab`, `git init`. Create `README.md` and `app.py`. Stage and commit.

2. **Branching:** Create a branch `feature`. Add a new file `helper.py` and commit. Switch back to `main`.

3. **Merge:** Merge `feature` into `main`. Resolve any conflict (create one intentionally).

4. **Remote:** Create a repository on GitHub. Connect your local repo (`git remote add origin <url>`). Push `main`.

5. **Pull Request:** Create a new branch `update-readme`, make changes, push to GitHub, open a PR, then merge.

6. **Stash:** Make changes to `app.py` (uncommitted). Stash them. Make a different change and commit. Then pop the stash.

7. **Rebase:** Create a branch `rebased-feature`, make two commits. Rebase onto `main`. Verify the history is linear.

8. **Reset vs. Revert:** Make three commits. Use `git revert` on the middle commit. Use `git reset --hard` on the last commit. Compare the result.

---

**Date documented:** 2026-06-17  
**Sources:** Git documentation, GitHub Guides, Pro Git book

---