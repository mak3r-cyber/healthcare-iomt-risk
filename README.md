# Healthcare IoMT Risk Assessment Framework
![csv-to-xlsx](https://github.com/mak3r-cyber/healthcare-iomt-risk/actions/workflows/csv2xlsx.yml/badge.svg)


Open-source toolkit for risk assessment in healthcare environments and medical IoT (IoMT).

**Focus:** auditable risk matrices, clear methodology, and basic automation for reporting.

## What's included (v0.1)
- Manual risk matrix template (CSV → XLSX via GitHub Actions)
- EBIOS RM Light adaptation notes
- Remediation planning skeleton (Mermaid)

## Repository layout
- `02-Matrices/` → risk matrix CSV (source of truth) → XLSX artifact
- `03-Methodology/` → method notes (EBIOS RM Light, scales, decisions)
- `04-Planning/` → remediation roadmap
- `docs/reports/` → build artifacts

## Usage
Edit `02-Matrices/risk_matrix.csv`, then push.
GitHub Actions builds `docs/reports/risk_matrix.xlsx` as an artifact.

## Scope and ethics
Educational scope only. No patient data. Synthetic samples.

![csv-to-xlsx](https://github.com/mak3r-cyber/healthcare-iomt-risk/actions/workflows/csv2xlsx.yml/badge.svg)
