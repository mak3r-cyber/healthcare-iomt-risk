# Risk Assessment Santé / IoMT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Cybersecurity risk assessment framework for healthcare environments and connected medical devices (IoMT).

## Context

This project provides an **EBIOS Risk Manager Light** methodology tailored for small and medium-sized healthcare organizations (medical offices, clinics, laboratories) that do not have a dedicated Information Security Officer (ISO).

**Developed as part of:**
- RNCP Certification 36924 Level 7 "Cybersecurity and IT Security Expert"
- Master's Degree in Cybersecurity
- Academic project with real professional application

## Objectives

- Identify and assess priority cybersecurity risks in healthcare
- Provide an operational methodology adapted to SMEs (<50 employees)
- Integrate specific IoMT devices (connected medical devices)
- Ensure regulatory compliance (GDPR, HDS, ISO 27001, EU MDR)
- Automated tools for generating risk matrices and reports

## Project Structure
── 01-Research
│   ├── iomt_risk_sources.md
│   └── Sources.md
├── 02-Matrices
│   └── risk_matrix.csv
├── 03-Methodology
│   ├── ebios-rm-light.md
│   └── README.md
├── 04-Planning
│   └── README.md
├── CODEOWNERS
├── CONTRIBUTING.md
├── data
│   └── catalog
│       ├── free-security-resources.md
│       ├── mitre_ics_techniques.csv
│       ├── owasp_iot_top10.csv
│       └── scenarios.csv
├── docs
│   ├── architecture
│   │   └── ADR-0001-scope.md
│   ├── compliance
│   │   ├── iso27002-iomt-mapping.md
│   │   └── mapping.md
│   ├── medical-practice-case-study.md
│   ├── reports
│   │   └── risk_matrix.xlsx
│   ├── resource-catalog.md
│   └── runbooks
├── LICENSE
├── pyproject.toml
├── README.md
├── README.md.old
├── requirements.txt
├── ROADMAP.md
├── SECURITY.md
├── src
│   └── skadia_iomt
│       └── __init__.py
├── tools
│   ├── csv2xlsx.py
│   ├── demo.sh
│   ├── sec_checks.sh
│   └── validate_controls_link.py
└── venv
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── Activate.ps1
    │   ├── normalizer
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.13
    │   ├── python -> /usr/bin/python
    │   ├── python3 -> python
    │   └── python3.13 -> python
    ├── include
    │   └── python3.13
    ├── lib
    │   └── python3.13
    ├── lib64 -> lib
    └── pyvenv.cfg


## Installation

### Prerequisites

- Python 3.8+
- pip

### Install dependencies
```bash
git clone https://github.com/mak3r-cyber/risk-assessment-sante-iomt.git
cd risk-assessment-sante-iomt
pip install pandas openpyxl

Usage
1. Generate the risk matrix in Excel

python3 tools/csv2xlsx.py

Output: 02-Matrices/risk_matrix.xlsx with 3 sheets:
Risk Matrix: Fully scored and color-coded table
Heatmap: Visualization of Probability × Impact
Dashboard: Statistical summary and top critical risks

2. Customize for your structure

Edit 02-Matrices/risk_matrix.csv:

ID,Asset,Threat,Vulnerability,Probability,Impact,Risk,Decision,Recommendation
R026,Your asset,Your threat,Your vulnerability,3,4,12,Reduce,Your recommendation

Columns:

Probability: 1-5 (Very low → Very high)
Impact: 1-5 (Negligible → Catastrophic)
Risk: Automatically calculated (P × I)
Decision: Avoid / Reduce / Transfer / Accept

Regenerate the matrix:

python3 tools/csv2xlsx.py

3. Apply the methodology

Follow the guide in 03-Methodology/Methodology.md:

Phase 1: Identify the scope (2-4 hours)
Phase 2: Identify threats (4-6 hours)
Phase 3: Assess vulnerabilities (6-8 hours)
Phase 4: Score risks (4-6 hours)
Phase 5: Risk treatment plan (8-12 hours)
Phase 6: Validation & follow-up (ongoing)

Total effort for SMEs (10-20 people): 30-40 hours for the initial analysis

Case Studies Included
1. General Medical Office

Context: 2 doctors, 2000 patients, basic IT infrastructure

Analyzed Risks: 10 scenarios (ransomware, phishing, data theft...)

Security Budget: 13,700€ in year 1, then 3,200€/year

ROI: Positive from year 3

📄 See the full case study

2. Cardiology Clinic IoMT

Context: 4 cardiologists, 5000 patients/year, 30 beds, critical connected devices

IoMT Devices: Patient monitors, defibrillators, infusion pumps, telemetry 24/7

Analyzed Risks: 15 IoMT-specific scenarios (parameter manipulation, malicious firmware...)

Security Budget: 85k€ in year 1, then 25k€/year recurring

📄 See the full case study

Regulatory Compliance

This methodology covers:

GDPR Article 32 - Appropriate technical and organizational measures

ISO 27001 - Risk analysis (Clause 6.1.2) + Annex A controls

HDS - Health data hosting security requirements (CNIL guidelines)

EU MDR 2017/745 - Medical device cybersecurity (Annex I)

NIS2 Directive - Critical health infrastructure (if applicable)

Documented Sources

100+ verified sources in 01-Research/Sources.md:

Regulatory: CNIL, ANSSI, GDPR, Public Health Code, EU MDR
Standards: ISO 27001/27002/27005/27799/81001, NIST SP 800-30/800-66
Methodologies: EBIOS RM (ANSSI), ISO 31000
Medical Devices: FDA Cybersecurity, IEC 62304/80001, CVE database
Threats: CERT Santé, Cyble, Recorded Future, IBM Cost of Breach
Protocols: HL7 FHIR, DICOM, Bluetooth LE, 802.1X

Technologies Used

Python 3.8+ - Automation

pandas - CSV data manipulation

openpyxl - Excel generation with formatting

Markdown - Documentation

Git - Versioning

Roadmap
Version 1.0 (Current)

 Complete EBIOS RM Light methodology

 25 health/IoMT risk scenarios matrix

 Python tool for Excel generation

 2 detailed case studies

 100+ source documentation base

Version 1.1 (January 2025)

 Case study for medical laboratory analysis

 Management report template (PDF)

 Illustrated user guide

 Health incident stats 2024-2025

 Recent CVE list for medical devices

Version 2.0 (Q2 2025)

 Interactive web interface (Streamlit/Dash)

 Automated PDF report export

 Expanded risk scenario library (50+)

 Integrated GDPR compliance module

 Multi-language support (FR/EN)

Contribution

This project is academic, but contributions are welcome:

Fork the project

Create a branch (git checkout -b feature/AmazingFeature)

Commit (git commit -m 'Add AmazingFeature')

Push (git push origin feature/AmazingFeature)

Open a Pull Request

Contribution Areas:

New sector-specific risk scenarios

Case studies for other healthcare structures

Python tool improvements

Translation to English

Bug fixes / corrections

License

Distributed under the MIT License. See LICENSE for more information.

Free use for:

Academic use

Professional use

Modification and adaptation

Commercial use (with attribution)

Author

Kamilia Meliani

Lead SMSI Implementation - Hardis Group (Apprenticeship)

Master's Degree in Cybersecurity

Specialties: GRC, ISO 27001/27002, EBIOS RM, Security Audits

Certifications:

ISO 27001 Lead Implementer (in progress)

EBIOS Risk Manager (planned for 2026)

Cisco, Linux

Project developed in the context of:

RNCP Certification 36924 Level 7 "Cybersecurity Expert"

Healthcare sector expertise (personal motivation: medical data security)

Acknowledgements

ANSSI - EBIOS Risk Manager methodology

CNIL - Practical guides for the healthcare sector

CERT Santé - Threat monitoring

Cybersecurity health community - Feedback and insights

Contact & Support

Questions, suggestions, collaborations:

GitHub Issues: Open a ticket

LinkedIn: Kamilia Meliani
 (coming soon publication)

If this project helps you, feel free to star it!

Last update: November 2024
Version: 1.0
Status: Active - Continuous development


