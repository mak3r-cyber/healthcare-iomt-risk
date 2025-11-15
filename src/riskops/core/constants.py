"""Core constants for RiskOps package.

This module contains all shared constants used across the RiskOps package.
"""

# Security: File size limits
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Security: Characters that can trigger CSV injection in Excel
DANGEROUS_CHARS = ["=", "+", "-", "@", "\t", "\r"]

# Risk Matrix Colors (Hex codes for Excel/PDF)
RISK_COLORS = {
    "low": "C6EFCE",  # Light Green
    "medium": "FFEB9C",  # Yellow
    "high": "FFC7CE",  # Light Red
    "critical": "FF0000",  # Red
}

# Risk Score Thresholds (based on Probability x Impact)
RISK_THRESHOLDS = {
    "low": (1, 6),  # 1-6: LOW
    "medium": (7, 12),  # 7-12: MEDIUM
    "high": (13, 14),  # 13-14: HIGH
    "critical": (15, 25),  # 15-25: CRITICAL
}

# Risk Assessment Scales
PROBABILITY_SCALE = {
    1: "Very Low",
    2: "Low",
    3: "Medium",
    4: "High",
    5: "Very High",
}

IMPACT_SCALE = {
    1: "Negligible",
    2: "Minor",
    3: "Moderate",
    4: "Major",
    5: "Catastrophic",
}

# Risk Treatment Decisions
RISK_DECISIONS = {
    "avoid": "Avoid",
    "reduce": "Reduce",
    "transfer": "Transfer",
    "accept": "Accept",
}

# Required CSV Columns for Risk Matrix
REQUIRED_RISK_COLUMNS = [
    "ID",
    "Asset",
    "Threat",
    "Vulnerability",
    "Probability",
    "Impact",
    "Risk",
    "Decision",
    "Recommendation",
]

# HTTP Request Configuration (for link validation)
REQUEST_TIMEOUT = 10  # seconds
REQUEST_HEADERS = {"User-Agent": "RiskOps-LinkValidator/1.0"}
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Allowed directories for file operations (security whitelist)
ALLOWED_DIRS = [
    "docs/compliance",
    "docs/architecture",
    "docs/cces",
    "05-Business-Processes",
    "02-Matrices",
    "samples",
]

# Excel/PDF Report Configuration
EXCEL_SHEET_NAMES = {
    "matrix": "Risk_Matrix",
    "heatmap": "Heatmap",
    "dashboard": "Dashboard",
}

# Header styling for Excel
HEADER_STYLE = {
    "fill_color": "4472C4",  # Blue background
    "font_color": "FFFFFF",  # White text
    "font_size": 11,
    "bold": True,
}

# EBIOS RM Phases
EBIOS_PHASES = {
    1: "Scope Identification",
    2: "Threat Identification",
    3: "Vulnerability Assessment",
    4: "Risk Scoring",
    5: "Risk Treatment",
    6: "Validation and Follow-up",
}

# File Extensions
SUPPORTED_INPUT_FORMATS = [".csv", ".json", ".xlsx"]
SUPPORTED_OUTPUT_FORMATS = [".xlsx", ".pdf", ".json", ".csv"]
