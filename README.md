# RiskOps Health / IoMT — Open-Source Cybersecurity Toolkit


## License
MIT License

## Python Version
Python 3.9+ or later

### Empowering small healthcare orgs to manage IoMT cybersecurity risks with a lightweight, scriptable framework.

## Overview
RiskOps Health / IoMT is an open-source cybersecurity toolkit focused on **risk management** for connected medical devices (**IoMT**) in small and medium-sized healthcare organizations (clinics, hospitals, labs).
Inspired by EBIOS RM – no heavy tools or consultants needed.

## Why RiskOps?
Small and medium-sized healthcare organizations (SMEs) typically lack the necessary resources to manage cybersecurity risks associated with connected medical devices. RiskOps Health / IoMT provides an automated, scriptable framework for assessing IoMT risks without needing heavy consulting or tools.
Challenges for SMEs: Limited time, budget, staff, and IoMT-specific tools.
Solutions Provided:
Python-based risk scoring engine.
Compliance gap analysis.
Detection rules for HL7/DICOM (pilot).
Non-intrusive pentest checklists (design phase).


## Key Features

- **GRC Engine**: Automates risk scoring, compliance mapping (ISO 27001, HIPAA, GDPR), and generates reports.
- **HL7/DICOM Detection Rules**: Pilot phase (detection of vulnerabilities in medical device communication protocols).
- **Compliance**: Compliance with ISO 27001, HDS, HIPAA, GDPR.
- **SAFE Pentest**: Non-intrusive pen-test checklist, focused on small healthcare organizations.

## Project Status

Active development: GRC stable; detection/pentest in pilot. Experimental parts may evolve.

## Quality Pipeline

Type: mypy
Lint: ruff
Format: black
Tests: pytest (>90% coverage)
Security: SBOM (syft), scans (trivy) via tools/sec_checks.sh

CI: GitHub Actions for QA, security, builds.

## Quickstart

Follow these steps to get started with the project:

```bash
git clone https://github.com/mak3r-cyber/healthcare-iomt-risk.git
cd healthcare-iomt-risk
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pytest tests/test_grc -v
python tools/csv2xlsx.py  # Generates risk_matrix.xlsx
```

## Structure

```text
├── 01-Research/          # IoMT references, risk sources
├── 02-Matrices/          # Input CSV files for risk matrices
├── 03-Methodology/       # EBIOS RM documentation
├── 04-Planning/          # Project planning and organization
├── 05-Business-Processes/# Processes for ISO 27001, NIS2 compliance
├── data/                 # Supporting catalogs and datasets
├── docs/                 # Documentation (runbooks, reports)
├── src/riskops/          # Core code (GRC, SOC, Pentest)
├── tests/                # Unit tests
├── tools/                # Utilities (CSV to XLSX, security checks)
└── LICENSE, ROADMAP.md...
```

## Business Processes

This project includes reusable business processes aligned with key industry standards such as **ISO 27001** and **NIS2**:

- **Incident Management**: [See 05-Business-Processes/incident-management.md]
- **IoMT Risk Management**: [See 05-Business-Processes/risk-management.md]
- **ISO 27001 Compliance**: [See 05-Business-Processes/iso27001-compliance.md]
- **NIS2 Compliance**: [See 05-Business-Processes/nis2-compliance.md]

## Methodology

RiskOps Health / IoMT follows the **EBIOS RM Light methodology**:

1. **Scope**: Define system boundaries and objectives.
2. **Threats**: Identify and evaluate threats.
3. **Vulnerabilities**: Identify vulnerabilities in the IoMT environment.
4. **Score Risks**: Automatically calculate risk scores based on Probability × Impact.
5. **Treatment**: Propose risk treatment options (e.g., Avoid, Reduce, Transfer).
6. **Monitor**: Track risk status and ensure ongoing mitigation.

**Regulatory Coverage**: 
- GDPR Article 32
- ISO 27001 (Clause 6.1.2)
- HDS (French Health Data Security Requirements)
- EU MDR (Cybersecurity for Medical Devices)
- NIS2 Directive (Critical Health Infrastructure)
Covers: GDPR Art.32, ISO 27001, HDS, EU MDR, NIS2.

## Sources

**Regulators**: CNIL, ANSSI, EU Commission.
**Standards**: ISO/IEC 27001/27002, NIST SP 800-30/66, ISO 80001.
**Medical Devices**: FDA Cybersecurity, IEC 62304/80001, CVE databases.
**Protocols**: HL7 FHIR, DICOM, Bluetooth LE, 802.1X.

## Roadmap

v0.2.x: Stable GRC, 25+ scenarios, Excel tool, HL7 pilot.
Next: Case studies, reports, 50+ risks, enriched modules, FR/EN support.

## Contribute
Welcome! Areas: Risks, cases, tools, docs, fixes.
```bash
git checkout -b feature/xyz
# Code...
git commit -m "feat: xyz"
git push origin feature/xyz
# PR to main
```

## Authors
Kamilia & Lazreg Meliani
Cybersecurity Leads: GRC, ISO, EBIOS, Audits.

## Contact

Issues: GitHub.
LinkedIn: Kamilia Meliani.
Vulnerabilities: git-healthcareframe.mascot374@passmail.com (90-day disclosure).

Updated: November 2025
Status: Active
