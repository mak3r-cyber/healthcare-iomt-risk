# Project Roadmap

This roadmap outlines the planned development phases for the Healthcare IoMT Risk Assessment Framework.

## v0.1 (Current) — Foundation

This initial release focuses on establishing the project structure and core documentation:
* Structured repository architecture
* Manual risk assessment templates (Excel)
* EBIOS RM methodology documentation (Light adaptation)
* Use case examples (pacemaker, insulin pump)
* ISO 27002 and HDS control mappings

---

## v0.2 — Automation

This phase integrates core automation features, many of which are already complete (csv2xlsx.py):
* Python-based risk scoring engine
* Automated PDF report generation
* **Excel matrix generation from CSV inputs (COMPLETED)**
* Interactive CLI for guided assessments
* Batch processing for multiple assets

---

## v0.3 — Threat Intelligence Integration

Future focus on integrating external security data sources:
* Suricata connector for real-time IoMT traffic analysis
* Lightweight penetration testing module (Nmap integration)
* Auto-updating CVE database for IoMT devices
* Automated alerting for new vulnerabilities affecting assessed assets

---

## v1.0 — Enterprise Platform

The long-term goal for enterprise use and advanced visualization:
* REST API for SIEM and GRC tool integration
* Web dashboard for real-time risk visualization
* HDS certification compliance validation
* Multi-tenant support for consultancies
* Complete operator documentation and training materials
