# Week 2 – Network Scanning & Enumeration

## Professional Network Assessment Report

## Project Overview

This project demonstrates a comprehensive network scanning and enumeration assessment conducted against a Metasploitable3 virtual machine using Kali Linux. The objective was to identify live hosts, discover open ports, enumerate running services, identify the target operating system, and collect information that could support a penetration testing engagement.

All testing was performed in a controlled lab environment with authorization. Industry-standard tools such as Nmap and the Nmap Scripting Engine (NSE) were used to perform reconnaissance and service enumeration while documenting the findings in a professional report.

## Objectives

- Verify target host availability.
- Discover open TCP and UDP ports.
- Identify running services and software versions.
- Perform operating system fingerprinting.
- Enumerate services using Nmap NSE scripts.
- Assess potential vulnerabilities.
- Document findings in a professional technical report.

## Lab Environment

| Component | Details |
|-----------|---------|
| Attacker Machine | Kali Linux |
| Target Machine | Metasploitable3 |
| Virtualization Platform | Oracle VirtualBox |
| Network Configuration | Host-Only Network |
| Primary Tool | Nmap 7.98 |
| Assessment Type | Authorized Lab Assessment |

## Table of Contents

- [Executive Summary](#executive-summary)
- [Engagement Overview](#engagement-overview)
- [Assessment Methodology](#assessment-methodology)
- [Lab Environment](#lab-environment)
- [Reconnaissance and Host Discovery](#reconnaissance-and-host-discovery)
- [TCP Port Scanning](#tcp-port-scanning)
- [Service Enumeration](#service-enumeration)
- [Operating System Detection](#operating-system-detection)
- [NSE Script Scanning](#nse-script-scanning)
- [UDP Port Scanning](#udp-port-scanning)
- [Web Enumeration](#web-enumeration)
- [SMB Enumeration](#smb-enumeration)
- [FTP Enumeration](#ftp-enumeration)
- [SSH Enumeration](#ssh-enumeration)
- [Vulnerability Assessment](#vulnerability-assessment)
- [Findings Summary](#findings-summary)
- [Recommendations](#recommendations)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendix](#appendix)

---

# Executive Summary

This assessment documents a structured network scanning and enumeration exercise performed against an intentionally vulnerable Metasploitable3 laboratory system. The objective was to identify active services, determine exposed network ports, enumerate service information, identify the underlying operating system, and assess potential security weaknesses within the authorized laboratory environment.

The assessment identified several exposed services, including FTP, SSH, HTTP, SMB, and IPP. Further enumeration revealed legacy service versions, exposed web resources, directory listings, administrative interfaces, weak authentication configurations, and potentially insecure cryptographic settings. Nmap NSE vulnerability assessment also identified potential CSRF and SQL injection conditions, a likely Slowloris denial-of-service condition, and an SMB denial-of-service vulnerability.

Additional service-specific enumeration identified significant security weaknesses, including successful authentication using default FTP credentials, anonymous SMB enumeration, weak SMB password policies, exposed web applications, and support for deprecated SSH cryptographic algorithms.

The findings demonstrate the importance of systematic reconnaissance, service enumeration, vulnerability identification, secure configuration, patch management, and access control. The assessment provides a structured basis for prioritizing remediation and conducting further controlled validation within an authorized penetration testing environment.

---

The engagement was conducted as an authorized network security assessment within an isolated virtual laboratory environment. The assessment targeted a Metasploitable3 virtual machine configured to simulate a deliberately vulnerable Linux-based system.

The primary objective was to perform systematic network reconnaissance and enumeration to identify the target's exposed attack surface, including active services, open TCP and UDP ports, software versions, operating system characteristics, service configurations, web resources, and potential security weaknesses.

The assessment was performed from a Kali Linux virtual machine using Nmap and its Nmap Scripting Engine (NSE), supported by additional enumeration tools including WhatWeb, Nikto, Gobuster, Enum4linux, and standard network utilities. Testing progressed from basic host discovery through service-specific enumeration and vulnerability assessment.

### Scope

| Item | Details |
| --- | --- |
| Assessment Type | Network Scanning and Enumeration |
| Target | Metasploitable3 |
| Target IP | `192.168.56.101` |
| Attacker Platform | Kali Linux |
| Network | Isolated Host-Only Virtual Network |
| Primary Tool | Nmap 7.98 |
| Supporting Tools | Nmap NSE, WhatWeb, Nikto, Gobuster, Enum4linux, Netcat, FTP client |
| Authorization | Controlled laboratory environment |
| Assessment Focus | Network services, service configuration, web resources, SMB, FTP, SSH, and potential vulnerabilities |

### Assessment Boundaries

The assessment was limited to the authorized Metasploitable3 laboratory system. No external production systems, third-party infrastructure, or unauthorized hosts were targeted.

The assessment focused primarily on reconnaissance, enumeration, vulnerability identification, and security analysis. Automated vulnerability findings were treated as potential indicators and were not considered confirmed exploitable vulnerabilities without additional manual validation.

The information collected during the engagement was used to document the target's security posture and develop appropriate defensive recommendations.

# Assessment Methodology

*To be completed.*

## Table of Contents

- [Executive Summary](#executive-summary)
- [Engagement Overview](#engagement-overview)
- [Assessment Methodology](#assessment-methodology)
- [Lab Environment](#lab-environment)
- [Reconnaissance and Host Discovery](#reconnaissance-and-host-discovery)
- [TCP Port Scanning](#tcp-port-scanning)
- [Service Enumeration](#service-enumeration)
- [Operating System Detection](#operating-system-detection)
- [NSE Script Scanning](#nse-script-scanning)
- [UDP Port Scanning](#udp-port-scanning)
- [Web Enumeration](#web-enumeration)
- [SMB Enumeration](#smb-enumeration)
- [FTP Enumeration](#ftp-enumeration)
- [SSH Enumeration](#ssh-enumeration)
- [Vulnerability Assessment](#vulnerability-assessment)
- [Findings Summary](#findings-summary)
- [Recommendations](#recommendations)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendix](#appendix)