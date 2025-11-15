# RiskOps Health / IoMT — Open-source Toolkit

**License:** MIT  
**Python:** 3.9+

RiskOps Health / IoMT is an open-source cybersecurity toolkit focused on **risk management for connected medical devices (IoMT)** in small and medium-sized healthcare organizations (medical practices, clinics, laboratories).

The goal is to give these organizations a **concrete, scriptable framework** to assess risks, map them to regulations, and prepare detection / pentest-light activities without needing heavy consulting or tools.

---

## Context

Small and medium-sized healthcare structures usually lack:

- time and budget for full-blown GRC programs,
- internal security staff (CISO, SOC),
- dedicated tools for IoMT risk management.

RiskOps Health / IoMT provides:

- a **lightweight EBIOS RM-inspired method**,
- a **Python engine** to score and manipulate risks,
- a **compliance mapping layer** (ISO 27001 / HIPAA / GDPR),
- a **detection / pentest-light skeleton** oriented IoMT.

---

## Current Capabilities

### 1. GRC — Risk & Compliance Engine

Implemented in `src/riskops/grc/`:

- **RiskAssessmentEngine**
  - Load and validate risk matrices from CSV.
  - Compute risk scores (Probability × Impact).
  - Enforce constraints:
    - numeric ranges (e.g. 1–5),
    - mandatory columns,
    - maximum file size,
    - basic CSV injection sanitisation.
  - Works directly on `pandas.DataFrame` for integration with other tools.

- **ComplianceMapper**
  - Map risk scenarios to high-level controls:
    - **ISO/IEC 27001 Annex A** controls,
    - **HIPAA** safeguards (administrative / physical / technical),
    - **GDPR** Article 32 security measures.
  - Produce a **gap analysis**:
    - Recommended controls (per framework),
    - Already implemented controls (optional input),
    - Missing controls per framework.

- **Test coverage**
  - Dedicated tests in `tests/test_grc/`.
  - Coverage for GRC module > **90 %** (pytest + coverage).

### 2. Detection — HL7 / DICOM (Pilot)

Detection-related content is being structured in:

- `docs/` (runbooks, architecture, reports),
- placeholders under `src/riskops/soc/` or equivalent for future logic,
- first **HL7 / DICOM-oriented detection rules** (pilot phase).

Objectives:

- document typical IoMT data flows (PACS, RIS, HIS),
- prepare rule templates that connect:
  - risk scenarios → detection logic → SOC use cases.

This part is still experimental and not considered stable.

### 3. Pentest Light — SAFE Approach (Design Phase)

The **SAFE pentest** component is designed to stay:

- **non-intrusive** for medical devices,
- aligned with **risk scenarios** instead of pure “CTF style” tests,
- usable as a **checklist** for small organizations.

Current status:

- structure and documentation prepared under `docs/` and `src/riskops/pentest/`,
- focus on:
  - attack surface review (network / exposed services),
  - configuration / hardening checks,
  - linkage to risks and compliance controls.

Implementation is in-progress and not yet published as a stable module.

---

## Project Status

RiskOps Health / IoMT is under **active development**.

- The **GRC engine (assessment + compliance)** is implemented and tested.
- Detection and pentest-light parts are in **pilot / design** phase.
- The repository is suitable for:
  - reading the code,
  - running tests locally,
  - using the risk engine in small experiments.

Some components are still experimental and may change between versions.

---

## Quality & Security of the Code

The project enforces a strict quality pipeline:

- **Type checking:** `mypy`
- **Linting:** `ruff`
- **Formatting:** `black`
- **Tests:** `pytest` with coverage (GRC module > 90 %)

Security helpers:

- `tools/sec_checks.sh`
  - Optional security checks using:
    - **syft** (SBOM generation),
    - **trivy** (vulnerability scan).
  - If these tools are missing (e.g., on GitHub runners), the script logs and exits successfully without failing the CI.

GitHub Actions:

- QA workflow (lint / type check / tests),
- Optional security workflow (SBOM + vuln scan),
- Build-artifacts workflow for packaging.

---

## Quickstart (local)

```bash
# 1) Clone the repository
git clone https://github.com/mak3r-cyber/healthcare-iomt-risk.git
cd healthcare-iomt-risk

# 2) Create and activate virtual environment
python -m venv venv
. venv/bin/activate

# 3) Install dependencies (dev)
pip install -r requirements.txt
pip install -e .

# 4) Run tests and coverage for the GRC module
pytest tests/test_grc -v
Generate the Excel Risk Matrix
python tools/csv2xlsx.py


This creates 02-Matrices/risk_matrix.xlsx with:

Risk Matrix — scored and colour-coded table.

Heatmap — Probability × Impact visualisation.

Dashboard — summary statistics and top critical risks.

Project Layout (simplified)
.
├── 01-Research/                 # Sources, references, IoMT-specific materials
├── 02-Matrices/                 # CSV risk matrices (input for tools)
├── 03-Methodology/              # EBIOS RM Light documentation
├── 04-Planning/                 # Planning and project organisation
├── 05-Business-Processes/       # Business processes (access, incident, ISO 27001, NIS2, risk mgmt)
├── data/                        # Supporting data/catalogs
├── docs/                        # Architecture, runbooks, reports, case studies
├── src/
│   └── riskops/
│       ├── grc/                 # GRC engine (assessment + compliance)
│       ├── soc/                 # Future detection logic (pilot)
│       └── pentest/             # SAFE pentest-light structure (design phase)
├── tests/
│   └── test_grc/                # Unit tests for GRC module
├── tools/
│   ├── csv2xlsx.py              # CSV → XLSX converter (risk matrix)
│   ├── sec_checks.sh            # Optional SBOM + vulnerability scan
│   └── validate_controls_link.py
└── (standard project files: LICENSE, SECURITY.md, ROADMAP.md, etc.)

Business Process Mapping

The project embeds several business processes aligned with ISO 27001 and NIS2:

Incident Management

IoMT Risk Management

User Access Management

ISO 27001 Compliance

NIS2 Compliance

These processes are documented under 05-Business-Processes/ and can be reused or adapted by SMEs.

Methodology & Use

Methodological backbone: EBIOS RM Light (adapted to IoMT).

High-level steps, documented in 03-Methodology/ebios-rm-light.md:

Define scope

Identify threats

Assess vulnerabilities

Score risks

Define treatment plan

Validate & monitor

The Python engine automates mainly steps 4–5 (scoring + treatment support) and partially step 3 (validation rules).

Regulatory Coverage

The methodology and controls mapping aim at covering:

GDPR Article 32 — appropriate technical and organisational security measures,

ISO/IEC 27001 — risk analysis (Clause 6.1.2) & Annex A controls,

HDS — French health data hosting requirements,

EU MDR 2017/745 — cybersecurity for medical devices,

NIS2 — critical health infrastructure (when applicable).

Documented Sources

The work is based on public and recognised references, including:

Regulators: CNIL, ANSSI, EU Commission.

Standards: ISO/IEC 27001/27002/27005/27799/81001, NIST SP 800-30 / 800-66.

Medical Devices: FDA Cybersecurity, IEC 62304 / 80001, CVE databases.

Protocols: HL7 FHIR, DICOM, Bluetooth LE, 802.1X.

Roadmap (high level)

v0.2.x (current line)

Stable GRC engine (assessment + compliance).

25+ healthcare / IoMT risk scenarios.

Excel generation tool + high coverage tests.

First HL7/DICOM detection rules (pilot).

Next milestones

Additional case studies (labs, hospitals, radiology).

Management report templates (PDF / Markdown).

Extended IoMT risk library (50+ scenarios).

Enriched detection / pentest-light modules.

Multi-language support (FR / EN).

Contribution

Contributions are welcome.

Typical contribution areas:

New sector-specific IoMT risk scenarios,

Additional case studies (other healthcare contexts),

Improvements to the Python tools / CLI,

English / French documentation and examples,

Bug fixes, refactoring, tests.

Workflow:

git checkout -b feature/your-feature
# ... commit your changes ...
git commit -m "feat: add my feature"
git push origin feature/your-feature
# Open a Pull Request to main

Author

Kamilia Meliani & Lazreg Meliani
Cybersecurity – Lead implementation – Purple-team
Specialties: GRC, ISO 27001/27002, EBIOS RM, Security Audits

Contact & Security

Questions, suggestions, collaborations:

GitHub Issues: open a ticket on the repository.

LinkedIn: Kamilia Meliani.

Vulnerability disclosure

Contact: git-healthcareframe.mascot374@passmail.com

Default responsible disclosure period: 90 days.

Supported branches: main.

No real patient data must ever be shared in issues or test cases.

Last update: November 2025
Status: Active – continuous development
