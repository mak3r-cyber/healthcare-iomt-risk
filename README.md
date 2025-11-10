# Healthcare IoMT Risk Assessment Framework

![csv-to-xlsx](https://github.com/mak3r-cyber/healthcare-iomt-risk/actions/workflows/csv2xlsx.yml/badge.svg)

Open-source toolkit to structure risk assessment in healthcare environments and medical IoT (IoMT).  
Goal: give small teams an auditable baseline they can actually run.

## Why this exists
- Patient safety: connected devices can harm if tampered.
- Compliance pressure: ISO 27001/27002/27005 + GDPR/HDS are hard to operationalize.
- Resource gap: many orgs have no budget for heavy GRC platforms.

## Scope (v0.1 → v0.2)
- **Now**: CSV “source of truth” → CI generates XLSX matrix, method notes (EBIOS RM Light), remediation skeleton (Mermaid).
- **Next**: risk scoring CLI + schema checks; report template; initial control mappings.

## Non-goals
- No production pentest tooling here.
- No real patient/PII data.
- No promises of regulatory certification.

## Modules roadmap (incremental)
1) **GRC core**  
   - Risk inventory schema (CSV)  
   - Matrix generation (XLSX via CI)  
   - Method notes (EBIOS RM Light)  
2) **Detection-lite** *(planned)*  
   - Basic parsers for IoMT network artifacts (offline samples)  
   - Mapping to risks to update likelihood  
3) **Pentest-light** *(planned)*  
   - Safe checklists and synthetic examples only  
   - No exploitation code

## Repository layout
- `02-Matrices/` → risk matrix CSV (source of truth) → **XLSX artifact in `docs/reports/`**  
- `03-Methodology/` → EBIOS RM Light adaptation notes  
- `04-Planning/` → remediation roadmap (Mermaid)  
- `tools/` → CSV→XLSX converter and future utilities

## Quick start
```bash
# edit the CSV
nano 02-Matrices/risk_matrix.csv

# local build
python3 tools/csv2xlsx.py
# result
ls -l docs/reports/risk_matrix.xlsx
