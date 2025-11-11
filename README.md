# RiskOps Health / IoMT — Open-source Toolkit

**License**: MIT  
**Python**: 3.8+

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Context

RiskOps Health / IoMT is a cybersecurity risk assessment framework designed specifically for small and medium-sized healthcare organizations (medical offices, clinics, laboratories). The goal is to enable these organizations to assess the risks of IoMT (Internet of Medical Things) devices without relying on external consultants.

### Why This Project?
Small and medium-sized healthcare organizations typically lack the necessary resources to manage the cybersecurity risks associated with connected medical devices. This project provides a simple, automated methodology that ensures alignment with key security standards while being highly accessible to these organizations.

## Current Features
- **Risk Matrix**: Automatically generated from CSV to XLSX via GitHub Actions.
- **HL7/DICOM Detection Rules**: Pilot phase.
- **Compliance**: HDS, ISO 27001.
- **SAFE Pentest**: In design.
- **Detection**: Pilot phase (HL7/DICOM rules).

## Objectives

- Identify and assess the priority cybersecurity risks in healthcare.
- Provide an operational methodology for SMEs.
- Integrate IoMT devices (monitors, pumps, etc.).
- Ensure compliance with regulations (GDPR, HDS, ISO 27001, EU MDR).
- Automate the generation of risk matrices and reports.
- Provide light pentest (SAFE) methodology and detection rules.

## Quickstart (3 commandes)

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
riskops validate risk samples/healthcare/risk_sample.json
```

### Project Structure

```bash
.
├── 01-Research
├── 02-Matrices
├── 03-Methodology
├── 04-Planning
├── CODEOWNERS
├── CONTRIBUTING.md
├── current_requirements.txt
├── data
├── docs
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
├── ROADMAP.md
├── SECURITY.md
├── src
├── tools
└── venv

```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Install dependencies

Clone the repository and install the dependencies:

```bash
git clone https://github.com/mak3r-cyber/healthcare-iomt-risk.git
cd healthcare-iomt-risk
pip install -r requirements.txt
```

### Usage

1. Generate the Risk Matrix in Excel

Run the following command to generate the risk matrix in an Excel file:

```bash
python3 tools/csv2xlsx.py
```

This will create the file "02-Matrices/risk_matrix.xlsx" with 3 sheets:

Risk Matrix: Fully scored and color-coded table.
Heatmap: Visualization of Probability × Impact.
Dashboard: Statistical summary and top critical risks.

2. Customize the Risk Matrix

Edit the "02-Matrices/risk_matrix.csv" file to add your own data:

Example entry:

```bash
ID,Asset,Threat,Vulnerability,Probability,Impact,Risk,Decision,Recommendation
R026,Medical device,Intrusion,Unauthorized access,3,4,12,Reduce,Specific recommendation
```
Probability: 1-5 (Very low → Very high)
Impact: 1-5 (Negligible → Catastrophic)
Risk: Automatically calculated (P × I)
Decision: Avoid / Reduce / Transfer / Accept

3. Apply the Methodology

Follow the steps outlined in the "03-Methodology/ebios-rm-light.md" file. This includes:

Phase 1: Define scope (2-4 hours)
Phase 2: Identify threats (4-6 hours)
Phase 3: Assess vulnerabilities (6-8 hours)
Phase 4: Score risks (4-6 hours)
Phase 5: Risk treatment plan (8-12 hours)
Phase 6: Validation and follow-up (ongoing)

Estimated total effort for SMEs (10-20 people): approximately 30-40 hours for the initial analysis.
---

## Case Studies

### 1. General Medical Practice (Fictional)

Context: 2 doctors, 2,000 patients/year.
Security budget: €13,700 for year 1, then €3,200/year ongoing.
ROI: Positive after 3 years.

### 2. Cardiology Clinic with IoMT (Fictional)

Context: 4 cardiologists, 5,000 patients/year, 30 beds.
IoMT Devices: Patient monitors, defibrillators, infusion pumps.
Security budget: €85,000 for year 1, then €25,000/year recurring.
Risks: 15 IoMT-specific risks (malicious firmware, parameter manipulation, etc.)

Do you have a real-world case? Share it anonymously via issue #1.

## Regulatory Compliance

This methodology covers the following regulations:

GDPR Article 32: Appropriate technical and organizational measures.
ISO 27001: Risk analysis (Clause 6.1.2) and Annex A controls.
HDS: Health data hosting security requirements (CNIL guidelines).
EU MDR 2017/745: Medical device cybersecurity (Annex I).
NIS2 Directive: Critical health infrastructure (if applicable).

## Documented Sources

The project is based on  verified sources, including:

Regulations: CNIL, ANSSI, GDPR, EU MDR.
Standards: ISO 27001/27002/27005/27799/81001, NIST SP 800-30/800-66.
Medical Devices: FDA Cybersecurity, IEC 62304/80001, CVE database.
Protocols: HL7 FHIR, DICOM, Bluetooth LE, 802.1X.

## Technologies Used

Python 3.8+: Main programming language.
Pandas: CSV data manipulation.
Openpyxl: Excel file generation with formatting.
Markdown: Documentation.
Git: Version control.

### Contribution Areas:

New sector-specific risk scenarios
Case studies for other healthcare structures
Python tool improvements
Translation to English
Bug fixes / corrections

## Roadmap

### Version 1.0 (Current)

Complete EBIOS RM Light methodology.
25 health/IoMT risk scenarios.
Python tool for Excel generation.
2 detailed fictional case studies.

### Version 1.1 (January 2025)

Case study for medical laboratory analysis.
Management report template (PDF).
Illustrated user guide.
Health incident stats for 2024-2025.
Recent CVE list for medical devices.

### Version 2.0 (Q2 2025)

Interactive web interface (Streamlit/Dash).
Automated PDF report export.
Expanded risk scenario library (50+).
Integrated GDPR compliance module.
Multi-language support (FR/EN).

## Contribution

Contributions are welcome. To contribute:

Fork the project.
Create a branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push the branch (git push origin feature/your-feature).
Open a pull request.

## Contribution Areas:

New sector-specific risk scenarios.
Case studies for other healthcare structures.
Python tool improvements.
English translation.
Bug fixes.

## Free use for:

Academic use
Professional use
Modification and adaptation
Commercial use (with attribution)

## Author

Kamilia Meliani & Lazreg Meliani
Cybersecurity - Lead implementation - Purple-team
Specialties: GRC, ISO 27001/27002, EBIOS RM, Security Audits

## Certifications:

Lead Implemention (in progress)
ISO 27001 Lead Implementer (planned)
EBIOS Risk Manager (planned)
Cisco, Linux

## Acknowledgements

This project is inspired by:

ANSSI - EBIOS Risk Manager methodology
CNIL - Practical guides for the healthcare sector
CERT Santé - Threat monitoring
Cybersecurity health community - Feedback and insights

## Contact & Support

Questions, suggestions, collaborations:

GitHub Issues: Open a ticket
LinkedIn: Kamilia Meliani (coming soon publication)
Signalement vulnérabilités: git-healthcareframe.mascot374@passmail.com 
Délai de divulgation responsable: 90 jours (par défaut). 
Branches supportées: main. Pas de données réelles dans les issues.

If this project helps you, feel free to star it!

Last update: November 2024
Version: 1.0
Status: Active - Continuous development


