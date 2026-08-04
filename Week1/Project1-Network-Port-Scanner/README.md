# Advanced Network Port Scanner

A Python-based TCP Network Port Scanner developed as part of the **InternCareerPath Cyber Security Self-Learning Internship**.

## Project Overview

This application scans a target host for open TCP ports within a user-defined range. It resolves hostnames, identifies open ports, attempts service detection, and generates a professional scan report.

The project demonstrates fundamental cybersecurity concepts including network enumeration, socket programming, service identification, and multithreaded scanning.

---

## Features

- TCP port scanning
- Hostname to IP resolution
- Service detection
- Multithreaded scanning using ThreadPoolExecutor
- Automatic scan report generation
- Professional scan summary
- Error handling for invalid hostnames
- Clean and modular Python code

---

## Technologies Used

- Python 3
- Socket Programming
- Concurrent Futures (ThreadPoolExecutor)
- Git & GitHub
- Kali Linux

---

## Project Structure

```
Project1-Network-Port-Scanner/
│
├── docs/
├── screenshots/
├── README.md
├── requirements.txt
├── scanner.py
├── scanner_v1.py
└── scan_results.txt (generated automatically)
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/justtunde-ye/ICP-1D7091F7-2026-REPO.git
```

Navigate to the project:

```bash
cd ICP-1D7091F7-2026-REPO/Week1/Project1-Network-Port-Scanner
```

Run the scanner:

```bash
python3 scanner.py
```

---

## Example Usage

Target:

```
scanme.nmap.org
```

Port Range:

```
20
100
```

Example Output:

```
[OPEN] Port 21    Service: ftp
[OPEN] Port 22    Service: ssh
[OPEN] Port 80    Service: http
```

---

## Scan Report

The scanner automatically creates:

```
scan_results.txt
```

The report contains:

- Target Host
- Target IP
- Open Ports
- Detected Services
- Total Ports Scanned
- Scan Duration

---

## Skills Demonstrated

- Python Programming
- Socket Programming
- TCP/IP Networking
- Network Enumeration
- Service Detection
- Multithreading
- Report Generation
- Git Version Control
- GitHub Project Management

---

## Future Improvements

- UDP scanning
- Banner grabbing
- OS detection
- Command-line arguments
- Export reports to CSV
- Export reports to JSON
- Progress bar
- Colorized terminal output

---

## Disclaimer

This tool is intended for educational purposes only.

Only scan systems you own or have explicit authorization to test.

---

## Author

**Babatunde Eletu**

InternCareerPath Cyber Security Self-Learning Internship

2026