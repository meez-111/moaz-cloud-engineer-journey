## 🗺️ The Complete RHCSA Journey

```
[Phase 1: Account Alignment] ──> [Phase 2: The Purchase] ──> [Phase 3: ID Pre-Approval] 
                                                                    │
[Phase 6: Exam Day] <── [Phase 5: The Night Before] <── [Phase 4: Remote Setup]
   │
[Phase 7: Certification Result]

```

---

## Phase 1: Pre-Purchase & Account Matching

**Goal:** Prevent automated fraud detection from locking your account due to your expat status.

* **The Identity Document:** Locate your physical, original **Egyptian Passport** (the information page containing your photo and full name in English). Do not use a copy or a heavily scratched document.
* **The Account Creation:** Go to the Red Hat Customer Portal and click **Register**. Choose a **Personal Account type** (Personal/Individual).
* **Name Matching Rule:** Enter your First, Middle, and Last names **exactly** as they are written on your passport. If your passport says *Mohamed*, do not type *Mohammed* on your profile. A single letter mismatch will block you later.
* **Location Fields:** Select **Saudi Arabia** as your Country of Residence and provide your local Saudi home address (e.g., Unaizah, Qassim region). Red Hat checks your physical location via your internet connection during the test, so this profile country *must* be Saudi Arabia.

---

## Phase 2: Secure the Voucher Payment

**Goal:** Successfully process the payment through the correct regional portal.

* **Verify the Catalog:** Go to the Red Hat training portal. Look at the top right of your screen and confirm the country selector reads **Saudi Arabia**.
* **Understand the Code (`EX200K`):** As you can see in your second screenshot, searching for "EX200" in Saudi Arabia returns exactly one option: **Individual Exam (EX200K)** priced at **USD 500.00**.
> 💡 **Important Technical Note:** In Red Hat's unified scheduling catalog, the **K** suffix stands for Individual Testing. Once you buy this voucher, you will be given a choice in your dashboard to schedule it either as an **On-site Kiosk** or a **Remote Exam from home**. You are buying the correct item!


* **The Checkout:** Click **Add to Cart**, then click **Login or Register**. Log in with the account you verified in Phase 1.
* **Payment Routing:** Complete the billing fields using a credit/debit card enabled for international USD transactions. Once authorized, copy your **Exam Voucher / Authorization ID** from your confirmation screen.

---

## Phase 3: The Mandatory Pre-Approval Identity Upload

**Goal:** Get authorized to view the scheduling calendar. Red Hat will not show you open time slots until your identity is scanned and approved by their AI filter.

1. Log into your Red Hat Certification Central dashboard. Click on the notification banner or navigate to `red.ht/exam_id_upload`.
2. The portal will initialize a secure third-party verification tool (`Incode`).
3. **Take the Selfie:** Follow the prompts to capture a clear live photo of your face using your webcam.
4. **Scan the Passport:** Place your Egyptian Passport flat on the desk under strong, natural lighting (avoid overhead light glare on the plastic laminate). Take a high-resolution snapshot through the interface. Ensure all four corners of the passport page are inside the frame.
5. **The Wait:** The automated system takes anywhere from a few minutes to **3 business days** to change your account status to **Approved**. Monitor your email inbox.

---

## Phase 4: Hardware Acquisition & System Boot Setup

**Goal:** Gather your physical components and configure your hardware for the Red Hat Live environment.

### 1. Gather the Hardware Checklist

You cannot run this exam inside Windows or macOS. You will boot from a custom USB stick. Your machine must meet these strict criteria:

| Component | Strict Rule |
| --- | --- |
| **Processor** | Must be an Intel or AMD x86_64 CPU. **Apple Silicon M1/M2/M3 chips are entirely unsupported.** |
| **External Webcam** | **Mandatory.** You cannot use a laptop's built-in webcam. You must buy a standalone wired USB webcam with a cable at least 1 meter long. |
| **Audio/Microphone** | Your laptop's built-in microphone or the external webcam's microphone is perfectly fine. **No wireless headsets/AirPods allowed.** |
| **Mouse** | Standard wired USB mouse. (Wireless Bluetooth mice are banned). |
| **USB Flash Drive** | A dedicated USB drive with a minimum capacity of **8GB**. |

### 2. Prepare and Flash the Live System

Once your identity is approved in Phase 3, you can select your exam date and time in the scheduler. Immediately after selecting a time slot, complete this technical setup:

1. **Download the ISO:** Inside your Red Hat scheduling dashboard, look for the link to download the **Red Hat Remote Exam Live ISO** image file (`.iso`). Save it to your local machine.
2. **Flash the Media:** Download and install **Fedora Media Writer** on your current operating system. Insert your 8GB USB drive. Open the software, click **Custom Image**, pick the downloaded Red Hat ISO, and click **Write to Disk**.
3. **Change Motherboard Firmware (BIOS/UEFI):**
* Shut down your computer completely. Turn it on while tapping your motherboard's BIOS access key (`F2`, `F12`, `Del`, or `Esc` depending on your laptop brand).
* Navigate to the **Boot Options** or **Security** tab.
* Set the boot style to **UEFI** (Legacy mode is not supported).
* **Disable Secure Boot.** Turn this option off completely, otherwise your computer's motherboard will block the custom Red Hat exam kernel from executing.


4. **Run the Compatibility Check:** Save your changes and reboot your computer directly into the USB drive. Once the Red Hat Live desktop environment loads into your RAM, connect to your internet. Open the **Compatibility Test tool**. Run through the automated camera check, audio check, and network throughput check to confirm your home internet line maintains at least a stable 2 Mbps download / 1 Mbps upload speed.

---

## Phase 5: The Night Before the Exam

* **The Room Sweep:** Clear your testing room. Remove all paper, books, notebooks, pens, and electronic equipment (extra monitors, tablets, smartwatches) away from your desk area.
* **The Boundary Rule:** Pick a room with a solid door that shuts entirely. Tell everyone in your home that they **cannot enter the room for a 4-hour window** tomorrow, and to minimize heavy internet tasks (such as 4K streaming or gaming) while your test is running.
* **Layout Verification:** Ensure your passport and your Saudi Iqama are placed side-by-side right on the edge of your desk.

---

## Phase 6: Exam Day Timeline & Execution

### 🕦 T-Minus 30 Minutes: System Initialization

1. Boot your computer into the **Red Hat Live USB environment**.
2. Plug in your external wired USB webcam and position it to the side or slightly behind your laptop keyboard, angled downward. The proctor needs to see your face, your hands, and your keyboard layout simultaneously in a single frame.
3. Connect your internet line (a physical Ethernet cable is heavily preferred over Wi-Fi to prevent drops). Click **Start Exam** to patch through to your live proctor via chat.

### 🕒 T-Minus 15 Minutes: Security Check-in

1. **The Document Verification:** Hold your physical passport directly up to the lens of your external webcam until the proctor confirms they can read your text clearly.
2. **The Room Scan:** The proctor will ask you to pick up your external webcam and slowly rotate it 360 degrees. Scan the four walls, the ceiling, the floor, your chair, and underneath your desk surface to prove there are no cheat sheets or hidden devices.

### 🏁 The 3-Hour Exam Window

Once cleared, your virtual desktop environments are unlocked.

* **The Interface:** The left side of your screen displays your task objectives (e.g., managing files, creating users, establishing logical volumes, writing shell scripts, adjusting firewalls). The right side displays terminal console instances connected to the target RHEL nodes.
* **Gain Root Privileges Immediately:** Run `sudo -i` or `su -` immediately to avoid local permission issues when modifying core configurations.
* **The Absolute Key to Passing:** **Reboot and Verify.** Red Hat grades using an automated script that evaluates your virtual machines **after a hard reboot**. If you configure everything perfectly but fail to execute `systemctl enable <service>` or make a typo in your `/etc/fstab` persistent storage mounts, your machine will either break during boot or lose the settings. If it breaks, you get **zero points** for that objective. Reboot your target VM frequently during the test and make sure your changes stay active!

---

## Phase 7: Receiving Your Certification

1. **The Auto-Grade:** Once your 3-hour limit expires or you click "Submit", the system terminates your session. You can shut down your machine, remove the USB drive, and boot back into your normal Windows/macOS.
2. **The Score Notification:** Red Hat will automatically process your virtual machine states. Within **3 business days** (frequently within 12–24 hours), you will receive an official email notification.
3. **Claiming the Certificate:** Log into your Red Hat Certification Central profile. If your score is **210 out of 300** or higher, you are officially an RHCSA! You can instantly download your high-resolution PDF certificate and claim your digital badge via **Credly** to showcase your verified system administrator credentials on your CV and LinkedIn.