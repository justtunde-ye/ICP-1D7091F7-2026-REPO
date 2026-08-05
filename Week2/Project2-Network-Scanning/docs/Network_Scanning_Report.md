# Network Scanning and Enumeration Report

## 1. Introduction

### Objective
The objective of this project is to perform network scanning and enumeration against a controlled vulnerable lab environment to identify active hosts, open ports, running services, and potential security weaknesses.

### Target Environment
- Target: Metasploitable Virtual Machine
- Scanner: Kali Linux
- Tools Used:
  - Nmap
  - Netcat
  - NSE Scripts

---

# 2. Host Discovery

## Objective
To determine whether the target system is active on the network.

## Command Used

```bash
ping -c 4 <Target_IP>