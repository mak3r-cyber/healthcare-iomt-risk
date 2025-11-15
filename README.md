# RiskOps Health / IoMT — Open-Source Toolkit

License: MIT
Python: 3.9+
Tests
Coverage

### Empowering small healthcare orgs to manage IoMT cybersecurity risks with a lightweight, scriptable framework.

## Overview
Focus: Risk assessment, compliance mapping (ISO 27001, HIPAA, GDPR), and IoMT-focused detection/pentest tools for clinics, labs, and practices.
Inspired by EBIOS RM – no heavy tools or consultants needed.

## Why RiskOps?

Challenges for SMEs: Limited time, budget, staff, and IoMT-specific tools.
Solutions Provided:
Python-based risk scoring engine.
Compliance gap analysis.
Detection rules for HL7/DICOM (pilot).
Non-intrusive pentest checklists (design phase).


## Key Features

### GRC Engine (src/riskops/grc/)

Load/validate CSV risk matrices.
Score risks (Probability × Impact).
Map to controls: ISO 27001, HIPAA, GDPR.
Gap analysis & reports.
90% test coverage.

### Detection (Pilot)

HL7/DICOM rules.
Data flow docs (PACS, RIS, HIS).

### Pentest Light (Design)

SAFE approach: Non-intrusive checks.
Attack surface & hardening reviews.

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
```bash
git clone https://github.com/mak3r-cyber/healthcare-iomt-risk.git
cd healthcare-iomt-risk
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt -e .
pytest tests/test_grc -v
python tools/csv2xlsx.py  # Generates risk_matrix.xlsx
```
Output: Excel with scored matrix, heatmap, dashboard.

## Structure
```text
├── 01-Research/          # IoMT refs
├── 02-Matrices/          # CSV inputs
├── 03-Methodology/       # EBIOS RM docs
├── 04-Planning/          # Org
├── 05-Business-Processes/# ISO/NIS2 processes
├── data/                 # Catalogs
├── docs/                 # Runbooks, reports
├── src/riskops/          # Core code (grc, soc, pentest)
├── tests/                # Unit tests
├── tools/                # Utils (csv2xlsx, sec_checks)
└── LICENSE, ROADMAP.md...
```

## Business Processes
Reusable: Incident Mgmt, Risk Mgmt, Access, ISO 27001, NIS2. See 05-Business-Processes/.

## Methodology
EBIOS RM Light steps:

Scope
Threats
Vulnerabilities
Score risks (automated)
Treatment
Monitor

Covers: GDPR Art.32, ISO 27001, HDS, EU MDR, NIS2.

## Sources

Regulators: CNIL, ANSSI, EU.
Standards: ISO 27k, NIST 800-30/66.
Med Devices: FDA, IEC 62304/80001, CVEs.
Protocols: HL7 FHIR, DICOM, BLE, 802.1X.

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
