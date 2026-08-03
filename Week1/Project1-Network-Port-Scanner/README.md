# Advanced Network Port Scanner

A Python-based TCP Network Port Scanner developed as part of the **InternCareerPath Cyber Security Self-Learning Internship**.

## Project Overview

This project scans a target host for open TCP ports within a user-defined range. It resolves hostnames, attempts TCP connections, and displays the service running on each open port.

The scanner is intended for educational purposes and should only be used on systems you own or have permission to test.

---

## Features

- Scan any valid IPv4 address or hostname
- Scan a custom TCP port range
- Detect open TCP ports
- Display common service names
- Resolve hostnames to IP addresses
- Display scan start time and total scan duration
- Built using Python's standard library (no external dependencies)

---

## Technologies Used

- Python 3
- Socket Programming
- TCP/IP Networking
- Git & GitHub

---

## Project Structure

```
Project1-Network-Port-Scanner/
├── scanner.py
├── README.md
├── requirements.txt
├── docs/
└── screenshots/
    └── scanner-output.png
```

---

## How to Run

Clone the repository and navigate to the project directory.

```bash
python3 scanner.py
```

Example:

```
Target: scanme.nmap.org
Starting Port: 20
Ending Port: 100
```

---

## Sample Output

```
Scanning target: 45.33.32.156

[OPEN] Port 21    Service: ftp
[OPEN] Port 22    Service: ssh
[OPEN] Port 80    Service: http

Scan completed successfully.
```

---

## Screenshot

A sample execution screenshot is available in:

```
screenshots/scanner-output.png
```

---

## Future Improvements

- Multithreaded scanning
- Command-line arguments
- Colored terminal output
- Export scan results to a file
- Banner grabbing
- UDP port scanning

---

## Disclaimer

This tool is provided for educational purposes only. Only scan systems that you own or have explicit authorization to test.