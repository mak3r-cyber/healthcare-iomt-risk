# Healthcare IoMT Risk Assessment Framework

This repository contains the methodology, risk matrix, and technical tools developed for the security assessment of **Internet of Medical Things (IoMT)** devices and associated healthcare information systems (HIS).

The framework is based on a **"Light" adaptation of the EBIOS Risk Manager methodology** (ANSSI, France), specifically tailored for small and medium-sized healthcare facilities (SMEs) without a dedicated Chief Information Security Officer (CISO).

---

## Intellectual Property & Licensing

**This project is proprietary (All Rights Reserved)**. Access, usage, and modification are strictly governed by the [LICENSE] and [CODEOWNERS] files. Unauthorized distribution of the methodology, matrix, or tools is prohibited.

---

## Project Structure

The structure organizes the assessment from high-level research down to technical implementation:

| Folder | Description | Key Files |
| :--- | :--- | :--- |
| **01-Research/** | Regulatory and threat intelligence sources. | [Sources.md] (GDPR, HDS, IoMT threats) |
| **02-Matrices/** | The core Intellectual Property (IP): the risk calculation model. | **(IP Excluded - See .gitignore)** |
| **03-Methodology/** | The EBIOS RM Light process and procedures. | **(IP Excluded - See .gitignore)** |
| **tools/** | Scripts for automation, analysis, and reporting. | [csv2xlsx.py] |
| **docs/** | Output reports, budget estimates, and final management documentation. | `reports/risk_matrix.xlsx` (Generated output) |

---

## Usage and Automation

### Prerequisites

To run the automation tools, ensure you have Python 3.x and the required libraries:

```bash
pip install pandas openpyxl
```

### 1. Generate the Risk Report (Excel)

The `csv2xlsx.py` script automatically reads the risk scores from the locally available CSV, recalculates the risk score (Probability x Impact), sorts the results, and exports them to a report file.

```bash
# Execute the conversion script
python tools/csv2xlsx.py
```

**Note:** You must have a local copy of `02-Matrices/risk_matrix.csv` to run this script.

### 2. Validation and Quality Checks

This repository uses Git hooks via `pre-commit` to enforce code quality and formatting standards (`black`, `ruff`, `mypy`). All contributions must pass these checks.

---

## Code Owners and Contributions

Changes to critical files (Methodology, Matrices, Licensing) must be approved by the designated code owners defined in the [CODEOWNERS] file.

**Primary Contact:** [YOUR NAME / CISO Role]
