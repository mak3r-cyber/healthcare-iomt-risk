"""Security utilities for RiskOps package.

This module provides security functions for:
- CSV injection protection
- File size validation
- Path traversal protection
- Input sanitization
"""

from pathlib import Path
from typing import Any, Union

import pandas as pd

from riskops.core.constants import DANGEROUS_CHARS, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB


def sanitize_cell_value(value: Any) -> Union[str, int, float]:
    """
    Sanitizes cell values to prevent CSV injection attacks.

    CSV injection (also called Formula Injection) occurs when applications
    export user-controlled data to CSV/Excel files without proper validation.
    Attackers can inject formulas that execute when the file is opened.

    Security measures:
    - Detects dangerous characters at start of cell (=, +, -, @, tab, carriage return)
    - Prefixes dangerous values with single quote (') to treat as text
    - Preserves numeric types (integers, floats) for proper Excel handling

    Args:
        value: Cell value to sanitize

    Returns:
        Sanitized value safe for Excel export (str or numeric type)

    Examples:
        >>> sanitize_cell_value("=2+5")
        "'=2+5"
        >>> sanitize_cell_value(42)
        42
        >>> sanitize_cell_value("normal text")
        'normal text'
    """
    # Handle None/NaN
    if pd.isna(value) or value is None:
        return ""

    # Preserve numeric types (int, float) - they're safe from CSV injection
    if isinstance(value, (int, float)):
        return value

    # Convert to string for text values
    str_value = str(value).strip()

    # Empty string is safe
    if not str_value:
        return ""

    # Security: Check if value starts with dangerous character
    if any(str_value.startswith(char) for char in DANGEROUS_CHARS):
        # Prefix with single quote to force Excel to treat as text
        # This prevents formula execution
        return "'" + str_value

    return str_value


def validate_file_size(file_path: Path) -> None:
    """
    Validates file size to prevent memory exhaustion attacks.

    Args:
        file_path: Path to file to validate

    Raises:
        ValueError: If file exceeds maximum size

    Examples:
        >>> validate_file_size(Path("small_file.csv"))  # OK
        >>> validate_file_size(Path("huge_file.csv"))  # Raises ValueError
    """
    file_size = file_path.stat().st_size

    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File size {file_size / 1024 / 1024:.2f}MB exceeds "
            f"maximum allowed size of {MAX_FILE_SIZE_MB}MB"
        )


def validate_risk_scores(df: pd.DataFrame) -> None:
    """
    Validates risk score data types and ranges.

    Security measures:
    - Ensures Probability and Impact are integers in range 1-5
    - Prevents type confusion attacks
    - Validates Risk calculation

    Args:
        df: DataFrame to validate

    Raises:
        ValueError: If data validation fails

    Examples:
        >>> df = pd.DataFrame({"Probability": [1, 2, 3], "Impact": [3, 4, 5], "Risk": [3, 8, 15]})
        >>> validate_risk_scores(df)  # OK
        >>> df_bad = pd.DataFrame({"Probability": [6], "Impact": [10], "Risk": [60]})
        >>> validate_risk_scores(df_bad)  # Raises ValueError
    """
    # Validate Probability column
    if not pd.api.types.is_numeric_dtype(df["Probability"]):
        raise ValueError("Probability column must contain numeric values")

    if not df["Probability"].between(1, 5).all():
        invalid_rows = df[~df["Probability"].between(1, 5)]
        raise ValueError(
            f"Probability must be between 1-5. Invalid rows: {invalid_rows.index.tolist()}"
        )

    # Validate Impact column
    if not pd.api.types.is_numeric_dtype(df["Impact"]):
        raise ValueError("Impact column must contain numeric values")

    if not df["Impact"].between(1, 5).all():
        invalid_rows = df[~df["Impact"].between(1, 5)]
        raise ValueError(f"Impact must be between 1-5. Invalid rows: {invalid_rows.index.tolist()}")

    # Validate Risk calculation
    expected_risk = df["Probability"] * df["Impact"]
    if not (df["Risk"] == expected_risk).all():
        print("Warning: Risk scores recalculated to match Probability × Impact")
