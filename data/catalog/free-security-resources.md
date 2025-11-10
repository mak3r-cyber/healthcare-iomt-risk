# GRC/IoMT Reference Catalog (Official and Actionable Resources)

**Objective:** To demystify cybersecurity for small healthcare organizations. This catalog proves that a professional strategy can be built using only **FREE, OFFICIAL, and CLEAR** resources.

# LEGAL DISCLAIMER AND LIMITATION OF LIABILITY

## 1. NATURE OF THE PROJECT (FOR EDUCATIONAL USE ONLY)

This project, "Healthcare IoMT Risk Assessment Framework," and all accompanying documentation, methodologies, and code examples (the "Resources") are provided **SOLELY FOR EDUCATIONAL, RESEARCH, AND NON-COMMERCIAL USE**.

The Resources are designed to demonstrate cybersecurity concepts, methodologies (such as EBIOS RM and NIST CSF), and the application of open-source tools (Nmap, Greenbone, Wazuh, etc.) in a hypothetical healthcare context.

## 2. NO GUARANTEE OR WARRANTY ("AS IS")

THE RESOURCES ARE PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

We make **NO GUARANTEE** regarding the completeness, accuracy, security, or reliability of the information, methodologies, or tools listed. Cybersecurity threats evolve constantly, and the information provided may become outdated.

## 3. NO PROFESSIONAL OR LEGAL ADVICE

The Resources do **NOT** constitute professional security advice, legal advice, or compliance certification.

* **Security Advice:** Always consult with certified cybersecurity professionals to implement and validate security controls in a live healthcare environment.
* **Legal/Compliance:** Always consult with qualified legal counsel regarding regulatory compliance, including HIPAA, HDS, GDPR, and the European Cyber Resilience Act (CRA).

## 4. HEALTHCARE AND PATIENT SAFETY WARNING (CRITICAL)

**DO NOT USE** the methodologies or tools contained herein on any live, production, or patient-facing network or device (IoMT, EMR systems, etc.) without explicit, written authorization and supervision from qualified technical and clinical staff.

ANY DIRECT OR INDIRECT USE of the tools (such as Nmap scans or Greenbone vulnerability checks) on operational medical systems carries a high risk of service disruption, device malfunction, data corruption, or interference with patient care.

## 5. LIMITATION OF LIABILITY

## 5. LIABILITY WAIVER AND LIMITATION

IN NO EVENT SHALL THE PROJECT AUTHORS, CONTRIBUTORS, OR MAINTAINERS BE LIABLE FOR ANY DAMAGES, LOSSES, OR CLAIMS (INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES) ARISING FROM THE USE or MISUSE OF THESE RESOURCES.

The liability is strictly limited to the fullest extent permitted by law.
---

## 1. GRC and Compliance Foundations (The Strategy)

This is the basis of the approach. It ensures regulatory alignment and rigor for auditing purposes.

| Resource | Type | Value and Action (For Your Clinic) | Official Link |
| :--- | :--- | :--- | :--- |
| **EBIOS Risk Manager (ANSSI)** | Risk Methodology | **The "How-to".** This is the French reference method. It provides the process for assessing device risks (the framework's **brain**). | https://cyber.gouv.fr/la-methode-ebios-risk-manager |
| **NIST CSF 2.0** | Cybersecurity Framework | **The "What-to-do".** Global standard for organizing security: Identify, Protect, Detect, Respond. Use it to structure and organize your security efforts. | https://www.nist.gov/cyberframework |
| **CIS Controls v8 (IG1)** | Prioritized Controls | **The "Where to start".** Lists the 18 most critical actions to implement first, blocking 80% of threats. Ideal for teams with limited resources. | https://www.cisecurity.org/controls/cis-controls-list |
| **NIST SP 800-37 (RMF)** | Risk Standard | **The Legal Structure.** International standard for risk management. Provides **free templates** for your risk documentation. | https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final |

---

## 2. Threat Intelligence and Monitoring

Understand who is attacking you, how, and what the vulnerabilities of your medical devices are.

| Resource | Type | Value and Action (For Your Clinic) | Official Link |
| :--- | :--- | :--- | :--- |
| **CERT-Santé** | Sectoral Monitoring | **French-specific Alerts.** Incident bulletins and alerts specific to French healthcare facilities. Subscribe to the mailing list for real-time threat context. | https://cyberveille.esante.gouv.fr/?utm_source=chatgpt.com |
| **MITRE ATT&CK for ICS** | Attack Model | **Real-world Scenarios.** Catalog of tactics and techniques used to attack Industrial Control Systems (ICS), which include medical devices. Useful for threat modeling. | https://attack.mitre.org/matrices/ics/ |
| **US-CERT Medical Advisories** | Manufacturer Alerts | **Official Flaws.** Direct alerts from CISA (US authority) on vulnerabilities by device manufacturer/model. Consult before purchasing new equipment. | https://www.cisa.gov/uscert/ics/advisories |
| **OWASP IoT Top 10** | Generic Vulnerabilities | **Quality Control.** List of the 10 worst security errors on connected devices (weak passwords, lack of secure updates, etc.). | https://owasp.org/www-project-internet-of-things/ |

---

## 3. Open Source Operational Tools

Moving from theory to action. These tools are free but require technical skills for initial setup.

Open-source tools **Wazuh**, **Suricata**, and **Greenbone Community Edition (GCE)** are free, but their **installation** and **maintenance** require non-trivial Linux/network skills.  
For small clinics, plan an initial setup by a **freelance consultant**, then an **internal handover**.  
This upfront effort fits the **“Minimal”** budget referenced in this catalog.


### A. Light Pentest and Audit (Offensive)

| Tool | Function (GRC -> Technical) | Value and Action (For Your Clinic) | Technical Credibility Link |
| :--- | :--- | :--- | :--- |
| **Nmap** | Asset Inventory | **The Basic Scan.** Used to inventory connected devices, find open ports, and identify services running on your equipment (Control 8.1). | https://nmap.org/ |
| **Greenbone Community Edition** | Vulnerability Scan | **The Light Pentest.** Free alternative to commercial scanners (Nessus). Use it to check if machines (servers, workstations) have known flaws (Control 8.8). | https://greenbone.github.io/docs/latest/22.4/container/index.html |

### B. Detection and Monitoring (Defensive)

| Tool | Function (GRC -> Technical) | Value and Action (For Your Clinic) | Technical Credibility Link |
| :--- | :--- | :--- | :--- |
| **Wazuh** | SIEM/Log Management | **The "Logbook".** Tool for collecting and analyzing server logs. Essential for compliance proof and intrusion detection (Control 8.16). | https://wazuh.com/ |
| **Suricata** | IDS (Detection) | **The Network Alarm.** Real-time analysis of your network traffic. Indispensable for *Light Detection* on IoMT device segments (Control 8.16). | https://docs.suricata.io/ |
