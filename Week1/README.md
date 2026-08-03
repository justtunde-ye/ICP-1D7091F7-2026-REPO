# Advanced Network Port Scanner

## Overview

This project is a Python-based TCP Network Port Scanner developed as part of the InternCareerPath Cyber Security Internship.

The scanner allows users to scan a target host for open TCP ports within a specified range and identifies common services running on those ports.

---

## Features

- Scan any IPv4 address or hostname
- Scan a custom range of TCP ports
- Detect open ports
- Display common service names
- Measure total scan duration
- Uses only Python's standard library

---

## Technologies Used

- Python 3
- socket
- datetime

---

## How to Run

```bash
python3 scanner.py
```

Example:

```
Target: scanme.nmap.org
Start Port: 20
End Port: 100
```

---

## Sample Output

```
[OPEN] Port 21 Service: ftp
[OPEN] Port 22 Service: ssh
[OPEN] Port 80 Service: http
```

---

## Disclaimer

This tool is intended for educational purposes and authorized security testing only.
