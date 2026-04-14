
# Creating, Viewing, and Editing Text Files

## 1. The Three Standard Streams

Every Linux command uses three communication "channels" identified by **File Descriptors (FD)**.

| Stream Name | File Descriptor | Description | Typical Source/Destination |
|-------------|----------------|-------------|---------------------------|
| `stdin` (Standard Input) | 0 | Data sent *to* a command | Your keyboard |
| `stdout` (Standard Output) | 1 | Successful output from a command | Your terminal screen |
| `stderr` (Standard Error) | 2 | Error messages (separated from regular output) | Your terminal screen |

---

## 2. Redirection – Changing Where Streams Go

### Output Redirection (`stdout` – FD 1)

| Operator | Description | Example |
|----------|-------------|---------|
| `>` | Overwrite – redirects output to a file, deleting existing content | `ls > files.txt` |
| `>>` | Append – adds output to end of file without deleting | `echo "New log" >> system.log` |

### Input Redirection (`stdin` – FD 0)

| Operator | Description | Example |
|----------|-------------|---------|
| `<` | Feeds a file into a command that expects keyboard input | `mail -s "Subject" user@example.com < message.txt` |

### Error Redirection (`stderr` – FD 2)

| Operator | Description | Example |
|----------|-------------|---------|
| `2>` | Redirect only errors to a file | `ls /root 2> errors.txt` |
| `2>>` | Append errors to a file | `command 2>> error.log` |
| `&>` | Redirect both `stdout` and `stderr` to same file | `command &> all_output.txt` |
| `2>&1` | Send errors to the same place as stdout | `command > output.txt 2>&1` |

**Examples:**

```bash
# Hide all error messages (send to nowhere)
ls /root 2> /dev/null

# Save normal output but see errors on screen
find / -name "*.conf" > found.txt 2> /dev/null

# Both stdout and stderr to same file
make &> build.log
```

---

## 3. Pipelines (`|`) – Connect Commands to Commands

A pipeline connects the `stdout` of one command to the `stdin` of another.

**Syntax:** `command1 | command2 | command3`

**Example:** `cat access.log | grep "ERROR" | wc -l`

| Command | What it does |
|---------|--------------|
| `cat access.log` | Reads the log file |
| `grep "ERROR"` | Filters for lines containing "ERROR" |
| `wc -l` | Counts the lines |

---

## 4. Special Redirection Destinations

### `/dev/null` – The Linux "Black Hole"

Anything sent here disappears forever.

```bash
# Hide all error messages
command 2> /dev/null

# Hide both output and errors
command &> /dev/null
```

### `tee` – T‑junction (send to file AND screen)

Sends output to a file **and** displays it on the terminal at the same time.

```bash
# Save and see output
ls -la | tee output.txt

# Append to file instead of overwrite
echo "New entry" | tee -a log.txt
```

---

## 5. Text Editors in Linux

| Type | Editors |
|------|---------|
| **GUI editors** | `gedit`, `mousepad`, `kate` |
| **Command line editors** | `vi` / `vim` (modern), `nano`, `emacs` |

This guide focuses on **vi/vim** – the default editor on almost all Linux systems.

---

## 6. VI / VIM – Complete Reference

### What is vi?

`vi` (visual editor) is the default editor that comes with Linux/UNIX. `vim` (vi improved) is the modern version with syntax highlighting and more features. On most systems, typing `vi` actually launches `vim`.

### Opening vi

```bash
vi [filename]
```

| Example | Description |
|---------|-------------|
| `vi newfile.txt` | Create a new file (empty) |
| `vi existing.txt` | Open an existing file |

---

## 7. The Three Modes of vi/vim

```
┌─────────────────┐      i, a, o, O, s, R     ┌─────────────────┐
│   COMMAND MODE  │ ─────────────────────────→ │   INSERT MODE   │
│  (default mode) │                            │  (edit text)    │
│                 │ ←───────────────────────── │                 │
└─────────────────┘           Esc             └─────────────────┘
        │
        │ : (colon)
        ↓
┌─────────────────┐
│  LAST LINE MODE │
│  (save, search, │
│   replace, quit)│
└─────────────────┘
```

| Mode | Purpose | How to enter | How to exit |
|------|---------|--------------|-------------|
| **Command Mode** | Navigate, delete, copy, paste | Default when vi starts; press `Esc` | Press `Esc` (stays in command mode) |
| **Insert Mode** | Insert/edit text | `i`, `a`, `o`, `O`, `s`, `R` | Press `Esc` |
| **Last Line Mode** | Save, quit, search, replace | Type `:` while in command mode | Press `Enter` (executes command) or `Esc` to cancel |

---

## 8. Command Mode – Navigation (Moving Around)

### Basic Cursor Movement

| Key | Action |
|-----|--------|
| `h` | Left one character |
| `j` | Down one line |
| `k` | Up one line |
| `l` | Right one character |
| `0` (zero) | Beginning of current line |
| `$` | End of current line |
| `^` | First non‑blank character of line |

### Word Navigation

| Key | Action |
|-----|--------|
| `w` | Move to beginning of next word |
| `b` | Move to beginning of previous word |
| `e` | Move to end of current word |
| `W` | Move to next word (ignores punctuation) |
| `B` | Move to previous word (ignores punctuation) |

### Line and Screen Navigation

| Key | Action |
|-----|--------|
| `H` | Move to top of screen |
| `M` | Move to middle of screen |
| `L` | Move to bottom of screen |
| `nH` | Move to nth line from top (e.g., `5H`) |
| `nL` | Move to nth line from bottom |
| `Ctrl+f` | Move forward one full page |
| `Ctrl+b` | Move backward one full page |
| `Ctrl+d` | Move forward half a page |
| `Ctrl+u` | Move backward half a page |
| `Ctrl+e` | Scroll up one line (screen moves, cursor stays) |
| `Ctrl+y` | Scroll down one line |
| `Ctrl+l` | Redraw screen (clears and refreshes) |

### Jump to Specific Line

| Command | Action |
|---------|--------|
| `:n` (last line mode) | Jump to line number `n` (e.g., `:25`) |
| `G` | Jump to last line of file |
| `gg` | Jump to first line of file |
| `nG` | Jump to line `n` (e.g., `15G`) |

### Sentence and Paragraph Navigation

| Key | Action |
|-----|--------|
| `(` | Beginning of current sentence |
| `)` | Beginning of next sentence |
| `{` | Beginning of current paragraph |
| `}` | Beginning of next paragraph |

---

## 9. Command Mode – Inserting Text (Entering Insert Mode)

| Command | Action |
|---------|--------|
| `i` | Insert **before** cursor |
| `I` | Insert at **beginning** of current line |
| `a` | Insert **after** cursor |
| `A` | Insert at **end** of current line |
| `o` | Open new line **below** cursor and enter insert mode |
| `O` | Open new line **above** cursor and enter insert mode |
| `s` | Delete character under cursor and enter insert mode |
| `S` | Delete current line and enter insert mode |
| `cc` | Delete current line and enter insert mode (same as `S`) |
| `C` | Delete from cursor to end of line and enter insert mode |
| `R` | **Replace mode** – overwrite characters without changing insert mode |

---

## 10. Command Mode – Deleting Text

| Command | Action |
|---------|--------|
| `x` | Delete character under cursor |
| `X` (uppercase) | Delete character **before** cursor |
| `dw` | Delete from cursor to end of current word |
| `dW` | Delete to next word (ignores punctuation) |
| `d$` or `D` | Delete from cursor to end of line |
| `d^` | Delete from cursor to beginning of line |
| `dd` | Delete entire current line |
| `ndd` | Delete `n` lines (e.g., `3dd` deletes 3 lines) |
| `dG` | Delete from cursor to end of file |
| `dgg` | Delete from cursor to beginning of file |

---

## 11. Command Mode – Copying (Yanking) and Pasting

| Command | Action |
|---------|--------|
| `yy` or `Y` | Yank (copy) current line |
| `nyy` | Yank `n` lines (e.g., `3yy` copies 3 lines) |
| `yw` | Yank from cursor to end of word |
| `y$` | Yank from cursor to end of line |
| `y^` | Yank from cursor to beginning of line |
| `p` | Paste **after** cursor (or below current line for line yanks) |
| `P` | Paste **before** cursor (or above current line) |

---

## 12. Command Mode – Undo, Redo, Repeat

| Command | Action |
|---------|--------|
| `u` | Undo last change |
| `Ctrl+r` | Redo (undo the undo) |
| `.` (period) | Repeat last command |

---

## 13. Last Line Mode – Saving and Quitting

Enter last line mode by typing `:` from command mode.

| Command | Action |
|---------|--------|
| `:w` | Save (write) file |
| `:w filename` | Save as `filename` |
| `:w!` | Force save (override read‑only) |
| `:q` | Quit (fails if unsaved changes) |
| `:q!` | Quit without saving (discard changes) |
| `:wq` | Save and quit |
| `:x` | Save and quit (same as `:wq`) |
| `ZZ` (command mode) | Save and quit (no colon needed) |
| `ZQ` (command mode) | Quit without saving (no colon needed) |

---

## 14. Last Line Mode – Searching

| Command | Action |
|---------|--------|
| `:/pattern` | Search forward for `pattern` |
| `:?pattern` | Search backward for `pattern` |

**From command mode (faster):**

| Command | Action |
|---------|--------|
| `/pattern` | Search forward for `pattern` |
| `?pattern` | Search backward for `pattern` |
| `n` | Repeat search in same direction |
| `N` | Repeat search in opposite direction |

---

## 15. Last Line Mode – Search and Replace

**Syntax:** `:[range]s/old/new/[options]`

| Range | Meaning |
|-------|---------|
| `(empty)` | Current line only |
| `%` | Entire file |
| `1,5` | Lines 1 through 5 |
| `.,$` | From current line to end |
| `.-3,.` | Current line and 3 lines above |

| Option | Meaning |
|--------|---------|
| `g` | Replace all occurrences on the line (not just first) |
| `c` | Confirm each replacement |
| `i` | Case‑insensitive search |

**Examples:**

| Command | Action |
|---------|--------|
| `:s/old/new/` | Replace first `old` on current line with `new` |
| `:s/old/new/g` | Replace all `old` on current line |
| `:%s/old/new/g` | Replace all `old` in entire file |
| `:%s/old/new/gc` | Replace all with confirmation |
| `:1,10s/old/new/g` | Replace in lines 1‑10 |
| `:%s/old/new/gi` | Case‑insensitive replace |

---

## 16. Last Line Mode – Reading and Writing Files

| Command | Action |
|---------|--------|
| `:r filename` | Read (insert) contents of `filename` after cursor |
| `:r !command` | Insert output of shell command (e.g., `:r !date`) |
| `:w filename` | Write current buffer to `filename` |
| `:w! filename` | Force write to `filename` |
| `:1,10 w newfile` | Write lines 1‑10 to `newfile` |

---

## 17. Last Line Mode – Block Operations

### Deleting Blocks

| Command | Action |
|---------|--------|
| `:1d` | Delete line 1 |
| `:1,5d` | Delete lines 1 through 5 |
| `:10,$d` | Delete from line 10 to end of file (`$` = last line) |
| `:.,$d` | Delete from current line to end (`.` = current line) |
| `:.-3,.d` | Delete current line and 3 lines above (total 4 lines) |
| `:.,.+4d` | Delete current line and next 4 lines (total 5 lines) |

### Copying (Yanking) Blocks

| Command | Action |
|---------|--------|
| `:1,5 co 10` | Copy lines 1‑5 and place after line 10 |
| `:1,$ co $` | Copy all lines and append to end of file |
| `:.,.+5 co 8` | Copy current line and next 5 lines after line 8 |
| `:-3,. co 10` | Copy current line and 3 lines above after line 10 |

### Moving Blocks

| Command | Action |
|---------|--------|
| `:1,5 mo 9` | Move lines 1‑5 after line 9 |
| `:1,$ mo $` | Move all lines to end (reorders) |
| `:.,.+5 mo 10` | Move current line and next 5 lines after line 10 |
| `:-3,. mo 10` | Move current line and 3 lines above after line 10 |

---

## 18. Last Line Mode – Running Shell Commands

| Command | Action |
|---------|--------|
| `:!command` | Run shell command (e.g., `:!ls -la`) |
| `:r !command` | Insert command output into file |
| `:sh` | Start a subshell (type `exit` to return to vi) |

---

## 19. VI Configuration – `.vimrc`

Create a file `~/.vimrc` to set persistent preferences.

**Common settings:**

```vim
" Enable syntax highlighting
syntax on

" Show line numbers
set number

" Use 4 spaces for tabs
set tabstop=4
set shiftwidth=4
set expandtab

" Enable mouse support
set mouse=a

" Show matching brackets
set showmatch

" Enable auto-indent
set autoindent
```

---

## 20. Quick Reference – Most Common vi Commands

| Task | Command |
|------|---------|
| Open file | `vi filename` |
| Enter insert mode | `i` |
| Save | `:w` |
| Quit | `:q` |
| Save and quit | `:wq` or `ZZ` |
| Quit without saving | `:q!` |
| Delete line | `dd` |
| Copy line | `yy` |
| Paste below | `p` |
| Undo | `u` |
| Search forward | `/pattern` |
| Search backward | `?pattern` |
| Find next | `n` |
| Replace all in file | `:%s/old/new/g` |
| Go to line 42 | `:42` or `42G` |
| Go to end of file | `G` |
| Go to beginning | `gg` |

---

## 21. Nano – A Simpler Alternative

If vi feels overwhelming, `nano` is a beginner‑friendly editor.

```bash
nano filename
```

**Basic nano commands (^ = Ctrl):**

| Shortcut | Action |
|----------|--------|
| `^O` | Save (Write Out) |
| `^X` | Exit |
| `^K` | Cut current line |
| `^U` | Paste |
| `^W` | Search |
| `^_` | Go to line number |
| `^C` | Show cursor position |

---

## Key Takeaways for Cloud Engineering

- **Redirection and pipes** are essential for log processing, automation scripts, and chaining commands on EC2 instances.
- **vi/vim** is the only editor guaranteed to be on every Linux server (no GUI). Mastering basic navigation and editing saves huge time during SSH troubleshooting.
- Knowing `:wq`, `:q!`, `/search`, `dd`, `yy`, `p` covers 90% of daily vi needs.

---

## Practice Check

- [ ] I can redirect `stdout` to a file and `stderr` to `/dev/null` separately
- [ ] I can pipe `grep` output into `wc -l`
- [ ] I can open a file in vi, insert text, save, and quit
- [ ] I can delete 3 lines at once using `3dd`
- [ ] I can copy a line and paste it below
- [ ] I can search for "error" and then replace all occurrences with "warning" across the whole file
- [ ] I can undo my last change with `u`

---

**Date documented:** 2026-04-14  
**Sources:** Linux Administration, GeeksforGeeks, course notes

---