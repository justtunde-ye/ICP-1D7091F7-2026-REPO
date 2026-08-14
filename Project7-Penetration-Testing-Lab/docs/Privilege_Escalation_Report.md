# Privilege Escalation Assessment

## Project 7: Penetration Testing Lab

**Target:** Metasploitable3 Ubuntu 14.04
**Target IP:** `192.168.56.101`
**Initial User:** `vagrant`
**Assessment Area:** Local Privilege Escalation

---

## 1. Target Session Verification

### Command

```bash
whoami
id
hostname
```

### What it does

* `whoami` identifies the currently authenticated user.
* `id` displays the user's UID, GID, and group memberships.
* `hostname` identifies the system on which the commands are being executed.

### Why we're running it

Before performing privilege-escalation testing, we need to establish the identity and context of the current session. This confirms that the assessment is being performed against the intended Metasploitable3 target rather than the Kali attacker machine.

### Output

```text
whoami
vagrant

id
uid=900(vagrant) gid=900(vagrant) groups=900(vagrant),27(sudo)

hostname
metasploitable3-ub1404
```

### Screenshot

![Privilege escalation target verification](../screenshots/privilege-escalation-target-verification.png)

**Screenshot:** `privilege-escalation-target-verification.png`

### Finding

The authenticated account is `vagrant` on the `metasploitable3-ub1404` target. The account is a member of the `sudo` group, which indicates that further sudo privilege enumeration is warranted.

---

## 2. Sudo Privilege Enumeration

### Command

```bash
sudo -l
```

### What it does

`sudo -l` lists the commands that the current user is permitted to execute through `sudo`, including any restrictions and authentication requirements.

### Why we're running it

We are checking whether the compromised or authenticated `vagrant` account has permissions that could allow local privilege escalation to root.

### Output

```text
Matching Defaults entries for vagrant on
metasploitable3-ub1404:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

User vagrant may run the following commands on
metasploitable3-ub1404:
    (ALL : ALL) ALL
    (ALL : ALL) NOPASSWD: ALL
```

### Screenshot

The `sudo -l` output was captured together with the target verification commands:

![Privilege escalation target verification](../screenshots/privilege-escalation-target-verification.png)

**Screenshot:** `privilege-escalation-target-verification.png`

### Finding

The `vagrant` account has unrestricted sudo privileges.

The important entry is:

```text
(ALL : ALL) NOPASSWD: ALL
```

This means the `vagrant` account can execute commands as any user and group, including `root`, without being required to provide a sudo password.

This represents a **critical privilege-escalation weakness** in the intentionally vulnerable lab environment.

---

## 3. Root Privilege Verification

### Command

```bash
sudo whoami
sudo id
```

### What it does

* `sudo whoami` executes `whoami` with elevated privileges and identifies the effective user.
* `sudo id` displays the UID, GID, and group memberships of the elevated process.

### Why we're running it

The previous `sudo -l` enumeration identified unrestricted passwordless sudo access. These commands safely verify whether that permission actually results in root-level execution.

### Output

```text
sudo whoami
root

sudo id
uid=0(root) gid=0(root) groups=0(root)
```

### Screenshot

![Root privilege verification](../screenshots/privilege-escalation-root-verification.png)

**Screenshot:** `privilege-escalation-root-verification.png`

### Finding

The privilege-escalation condition was successfully verified.

The `sudo whoami` command returned:

```text
root
```

and `sudo id` confirmed:

```text
uid=0(root) gid=0(root) groups=0(root)
```

UID `0` represents the root account on Linux. Therefore, the `vagrant` account can successfully execute commands with root privileges without password authentication.

### Security Impact

If an attacker obtains valid access to the `vagrant` account, the unrestricted `NOPASSWD: ALL` configuration allows immediate execution of commands with root privileges.

This results in complete compromise of the operating system and its data within the scope of this lab.

---

---

## Metasploit Framework Validation

The Metasploit Framework was used to supplement the manual privilege-escalation assessment. The framework was configured to maintain information about the authorized Metasploitable3 target and to support structured host, service, vulnerability, and module enumeration.

The Metasploit-based assessment was performed after the direct SSH privilege-escalation verification. The purpose of this phase was not to replace the manual privilege check, but to demonstrate how Metasploit can be used to organize assessment data and identify relevant modules that may support further investigation.

### Database Connectivity Verification

The Metasploit database connection was verified using the `db_status` command.

#### Command Used

```text
db_status
#### What It Does

The `db_status` command reports the current connection status of the Metasploit Framework database. In this assessment, the database connection was confirmed as active and using PostgreSQL.

Metasploit database connectivity allows assessment information such as hosts, services, vulnerabilities, credentials, and sessions to be stored and queried throughout the engagement.

#### Assessment Significance

A functioning database connection provides a centralized way to track information collected during the assessment. This is particularly useful when multiple enumeration activities are performed against the same target because the discovered information can be associated with the authorized Metasploitable3 host.

#### Evidence

`screenshots/metasploit-db-status.png`

---

### Target Host Registration

The authorized Metasploitable3 target was added to the Metasploit database using the `hosts -a` command.

#### Command Used

```text
hosts -a 192.168.56.101
What It Does

The hosts -a command adds a host to the Metasploit database so that the target can be tracked as an assessment asset.

Assessment Significance

Registering the target establishes the IP address within Metasploit and allows subsequent service and vulnerability information to be associated with the correct laboratory system.

Evidence

screenshots/metasploit-host-registration.png

### Metasploit Host Verification

The `hosts` command was used to verify that the authorized Metasploitable3 target had been successfully registered in the Metasploit database.

#### Command Used

```text
hosts
What It Does

The hosts command displays hosts currently stored in the Metasploit database, allowing the assessor to verify that the intended target has been registered.

Finding

The target 192.168.56.101 was successfully displayed in the Metasploit host database.

Assessment Significance

This confirms that the intended Metasploitable3 laboratory system is registered in Metasploit and can be associated with subsequent service and vulnerability information.

Evidence

screenshots/metasploit-hosts-list.png

### Metasploit Service Inventory

The `services` command was used to query the Metasploit database for network services associated with the registered Metasploitable3 target.

#### Command Used

```text
services
What It Does

The services command displays service information stored in the Metasploit database. The results can include the target host, port number, protocol, service name, state, and additional service information.

Why We're Running It

After confirming that the target was registered in the Metasploit database, the next step was to determine which network services had been recorded for that host.

This provides a structured service inventory that can be used to support further assessment and module research.

Finding

The Metasploit database displayed the services associated with the registered target.

The service information corresponds with the services identified during the earlier network-scanning phase, including FTP, SSH, HTTP, SMB, IPP, MySQL, and Jetty-based HTTP services.

Assessment Significance

The service inventory provides a framework-based view of the target's exposed attack surface. It also demonstrates that information collected through Metasploit can be queried after being stored in the database.

Evidence

screenshots/metasploit-services-initial.png

### Metasploit Service and Version Discovery

The `db_nmap` command was used to perform Nmap service and version detection through the Metasploit Framework while recording the results in the Metasploit database.

#### Command Used

```text
db_nmap -sV 192.168.56.101
What It Does

db_nmap allows Nmap to be executed from within Metasploit while automatically importing the scan results into the Metasploit database.

The -sV option enables service and version detection. Rather than identifying only whether a port is open, this scan attempts to determine the service running on each discovered port and, where possible, its software version.

Why We're Running It

The earlier assessment established the target's exposed services using Nmap. Running the service/version scan through Metasploit provides an additional verification and imports the results directly into the Metasploit database.

This is useful because the discovered services can subsequently be queried within Metasploit and used to guide module research.

Findings

The scan identified the following services on the authorized Metasploitable3 target:

Port	Service	Version
21/tcp	FTP	ProFTPD 1.3.5
22/tcp	SSH	OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13
80/tcp	HTTP	Apache httpd 2.4.7
445/tcp	SMB	Samba smbd 3.X - 4.X
631/tcp	IPP	CUPS 1.7
3306/tcp	MySQL	MySQL (unauthorized)
8080/tcp	HTTP	Jetty 8.1.7.v20120910

The target was identified as:

METASPLOITABLE3-UB1404

The service information identified the system as a Unix/Linux host.

Assessment Significance

The results provide a detailed service inventory within the Metasploit database. Version information is particularly useful during penetration testing because specific software versions can be compared against known vulnerabilities and relevant Metasploit modules.

However, service/version detection alone does not prove that a particular vulnerability is exploitable. Any potential vulnerability identified from version information should be manually validated before being classified as confirmed.

Tool Output Note

The scan completed successfully and reported the discovered services. A Ruby regular-expression warning from the Metasploit recog component was also displayed after the scan. This warning did not prevent the Nmap scan from completing or the service results from being recorded.

Evidence

screenshots/metasploit-db-nmap-service-scan.png

### Metasploit Vulnerability Database Review

The Metasploit vulnerability database was queried using the `vulns` command to determine whether any vulnerability records had been associated with the registered Metasploitable3 target.

#### Command Used

```text
vulns

What It Does

The vulns command displays vulnerability information currently stored in the Metasploit database. When vulnerability records are available, the output can include the affected host, service, vulnerability name, timestamp, resource, and associated references.

Why We're Running It

The purpose of this check was to determine whether the information already collected through Metasploit had resulted in vulnerability records being associated with the target.

This provides a useful distinction between vulnerabilities identified during scanning and vulnerabilities that have actually been imported or recorded in the Metasploit database.

Output

The command returned an empty vulnerability table:

# Vulnerabilities

Timestamp  Host  Service  Resource  Name  References

No vulnerability records were displayed.

Finding

The empty result indicates that no vulnerability records were currently associated with 192.168.56.101 in the Metasploit vulnerability database at the time of the assessment.

This does not mean that the Metasploitable3 system has no vulnerabilities. The target is intentionally vulnerable, and vulnerabilities were identified during the earlier Nmap vulnerability-assessment phase.

Instead, the result indicates that those findings were not currently represented as vulnerability records in the Metasploit database.

Assessment Significance

This demonstrates an important distinction between vulnerability discovery and vulnerability database registration. A scanner may identify potential vulnerabilities without those findings automatically appearing in Metasploit's vulns database.

Therefore, the empty vulns result was treated as a database-state observation rather than evidence that the target was secure.

Evidence

screenshots/metasploit-vulns-empty.png

### Metasploit Sudo Module Research

After the direct SSH assessment confirmed that the `vagrant` account possessed unrestricted sudo privileges, the Metasploit module database was queried for sudo-related modules.

#### Command Used

```text
search sudo

What It Does

The search sudo command searches the Metasploit module database for modules whose names or descriptions contain the term sudo.

The results can include exploit modules, post-exploitation modules, payloads, and other supporting modules related to sudo or privilege escalation.

Why We're Running It

The purpose of this search was to determine whether Metasploit contains modules relevant to sudo-based privilege escalation.

This provides supporting evidence that the Framework can be used to research potential privilege-escalation techniques after an elevated-privilege condition has been identified during manual enumeration.

Findings

The search returned multiple sudo-related modules. One relevant result was:

post/multi/manage/sudo

The search also returned other modules associated with sudo or privilege escalation, including modules targeting specific Linux applications and platforms.

Important Validation Note

The presence of a module in the search sudo results does not by itself demonstrate that the module is applicable to the Metasploitable3 target.

The actual privilege-escalation finding was established independently through direct enumeration of the target:

sudo -l

which returned:

(ALL : ALL) NOPASSWD: ALL

Root-level execution was then verified with:

sudo whoami
sudo id

Therefore, the Metasploit module search is supporting evidence demonstrating module discovery and research capability, while the direct SSH commands provide the actual proof of successful privilege escalation.

Assessment Significance

This step demonstrates the complementary roles of manual enumeration and exploitation frameworks.

Manual enumeration identified the exact sudo configuration present on the target, while Metasploit provided a structured mechanism for researching modules that may be relevant to sudo-based privilege escalation.

The assessment therefore did not rely solely on an automated module search to declare the vulnerability confirmed.

Evidence

screenshots/metasploit-sudo-module-search.png

screenshots/metasploit-sudo-module-search2.png

screenshots/metasploit-sudo-module-search3.png

screenshots/metasploit-sudo-module-search4.png

## Privilege Escalation Summary

| Test                         | Result                      | Significance                                   |
| ---------------------------- | --------------------------- | ---------------------------------------------- |
| Target identity verification | Confirmed `vagrant`         | Established initial access context             |
| Group enumeration            | `vagrant` belongs to `sudo` | Indicates elevated privileges may be available |
| `sudo -l`                    | `NOPASSWD: ALL`             | Unrestricted sudo access identified            |
| `sudo whoami`                | `root`                      | Root execution confirmed                       |
| `sudo id`                    | `uid=0(root)`               | Root-level privileges technically verified     |

### Overall Finding

**Critical — Unrestricted Passwordless Sudo Privileges**

The `vagrant` account has unrestricted passwordless sudo permissions, allowing commands to be executed as root. This provides a direct privilege-escalation path from the `vagrant` account to full system-level privileges.

---

## Evidence Files

* `screenshots/privilege-escalation-target-verification.png`
* `screenshots/privilege-escalation-root-verification.png`

## Assessment Note

All privilege-escalation testing documented in this report was performed against the intentionally vulnerable Metasploitable3 laboratory environment.
