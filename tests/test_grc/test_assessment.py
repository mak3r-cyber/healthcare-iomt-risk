"""Tests for riskops.grc.assessment.RiskAssessmentEngine."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import riskops.grc.assessment as assessment_module
from riskops.grc.assessment import (
    RiskAssessmentEngine,
    RiskAssessmentError,
    RiskMatrixValidationError,
)


@pytest.fixture
def engine() -> RiskAssessmentEngine:
    """Return a fresh RiskAssessmentEngine instance."""
    return RiskAssessmentEngine()


@pytest.fixture
def valid_csv_path(tmp_path: Path) -> Path:
    """Create a valid CSV risk matrix file.

    Columns:
        Asset, Threat, Probability, Impact

    Returns:
        Path to the created CSV file.
    """
    content = "\n".join(
        [
            "Asset,Threat,Probability,Impact",
            "Infusion Pump,Malware infection,4,5",
            "Ventilator,Network outage,2,4",
            "EHR Database,Unauthorized access,5,4",
        ]
    )
    csv_path = tmp_path / "valid_risks.csv"
    csv_path.write_text(content, encoding="utf-8")
    return csv_path


@pytest.fixture
def csv_with_injection(tmp_path: Path) -> Path:
    """Create a CSV file containing potential CSV injection payloads."""
    content = "\n".join(
        [
            "Asset,Threat,Probability,Impact",
            "=InjectedAsset,+SUM(A1:A2),3,3",
            "-AnotherAsset,@HACK(),2,2",
        ]
    )
    csv_path = tmp_path / "injection_risks.csv"
    csv_path.write_text(content, encoding="utf-8")
    return csv_path


@pytest.fixture
def csv_missing_columns(tmp_path: Path) -> Path:
    """Create a CSV file missing required columns."""
    content = "\n".join(
        [
            "Asset,Threat,Probability",
            "Server,Malware,4",
        ]
    )
    csv_path = tmp_path / "missing_columns.csv"
    csv_path.write_text(content, encoding="utf-8")
    return csv_path


@pytest.fixture
def csv_non_numeric_probability(tmp_path: Path) -> Path:
    """Create a CSV file with non-numeric probability values."""
    content = "\n".join(
        [
            "Asset,Threat,Probability,Impact",
            "Server,Malware,not_a_number,5",
        ]
    )
    csv_path = tmp_path / "non_numeric_probability.csv"
    csv_path.write_text(content, encoding="utf-8")
    return csv_path


@pytest.fixture
def csv_out_of_range_values(tmp_path: Path) -> Path:
    """Create a CSV file with out-of-range probability/impact values."""
    content = "\n".join(
        [
            "Asset,Threat,Probability,Impact",
            "Server,Malware,6,5",
        ]
    )
    csv_path = tmp_path / "out_of_range.csv"
    csv_path.write_text(content, encoding="utf-8")
    return csv_path


def test_load_csv_valid(engine: RiskAssessmentEngine, valid_csv_path: Path) -> None:
    """load_csv should load a valid CSV and normalise structure."""
    df = engine.load_csv(valid_csv_path)

    assert not df.empty
    assert set(["Asset", "Threat", "Probability", "Impact"]).issubset(df.columns)
    # Probability and Impact should be convertible to numeric for later steps.
    assert pd.to_numeric(df["Probability"], errors="coerce").notna().all()
    assert pd.to_numeric(df["Impact"], errors="coerce").notna().all()


def test_calculate_scores_basic(engine: RiskAssessmentEngine, valid_csv_path: Path) -> None:
    """calculate_scores should compute numeric scores and qualitative levels."""
    df = engine.load_csv(valid_csv_path)
    scored = engine.calculate_scores(df)

    assert "Risk" in scored.columns
    assert "RiskLevel" in scored.columns

    # First row: 4 * 5 = 20 -> critical (threshold > 16).
    first = scored.iloc[0]
    assert first["Risk"] == 4 * 5
    assert first["RiskLevel"] == "critical"

    # Second row: 2 * 4 = 8 -> medium.
    second = scored.iloc[1]
    assert second["Risk"] == 2 * 4
    assert second["RiskLevel"] == "medium"


def test_calculate_scores_thresholds(engine: RiskAssessmentEngine) -> None:
    """Risk levels should follow the configured thresholds on boundaries."""
    df = pd.DataFrame(
        {
            "Asset": ["A1", "A2", "A3", "A4"],
            "Threat": ["T1", "T2", "T3", "T4"],
            "Probability": [1, 3, 4, 5],
            "Impact": [4, 3, 4, 5],
        }
    )
    scored = engine.calculate_scores(df)

    # Scores: 4 (low), 9 (medium), 16 (high), 25 (critical).
    levels = list(scored["RiskLevel"])
    assert levels == ["low", "medium", "high", "critical"]


def test_export_csv_roundtrip(
    engine: RiskAssessmentEngine,
    valid_csv_path: Path,
    tmp_path: Path,
) -> None:
    """export_csv should write a CSV that can be read back."""
    df = engine.load_csv(valid_csv_path)
    scored = engine.calculate_scores(df)

    output_path = tmp_path / "scored.csv"
    written_path = engine.export_csv(scored, output_path)

    assert written_path.exists()
    loaded = pd.read_csv(written_path)
    assert "Risk" in loaded.columns
    assert "RiskLevel" in loaded.columns


def test_export_csv_overwrite_protection(
    engine: RiskAssessmentEngine,
    valid_csv_path: Path,
    tmp_path: Path,
) -> None:
    """export_csv should refuse to overwrite existing files unless allowed."""
    df = engine.load_csv(valid_csv_path)
    scored = engine.calculate_scores(df)

    output_path = tmp_path / "scored.csv"
    engine.export_csv(scored, output_path)
    assert output_path.exists()

    # Second call without overwrite should raise.
    with pytest.raises(RiskAssessmentError):
        engine.export_csv(scored, output_path)

    # Overwrite explicitly allowed.
    engine.export_csv(scored, output_path, overwrite=True)
    assert output_path.exists()


def test_export_csv_missing_directory(
    engine: RiskAssessmentEngine,
    valid_csv_path: Path,
    tmp_path: Path,
) -> None:
    """export_csv should fail if the output directory does not exist."""
    df = engine.load_csv(valid_csv_path)
    scored = engine.calculate_scores(df)

    non_existent_dir = tmp_path / "does_not_exist"
    output_path = non_existent_dir / "scored.csv"

    with pytest.raises(RiskAssessmentError):
        engine.export_csv(scored, output_path)


def test_load_csv_missing_file(engine: RiskAssessmentEngine, tmp_path: Path) -> None:
    """load_csv should raise FileNotFoundError for non-existing files."""
    missing = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        engine.load_csv(missing)


def test_load_csv_missing_required_columns(
    engine: RiskAssessmentEngine,
    csv_missing_columns: Path,
) -> None:
    """load_csv should raise RiskMatrixValidationError if mandatory columns are missing."""
    with pytest.raises(RiskMatrixValidationError):
        engine.load_csv(csv_missing_columns)


def test_load_csv_non_numeric_probability(
    engine: RiskAssessmentEngine,
    csv_non_numeric_probability: Path,
) -> None:
    """load_csv should reject non-numeric probability/impact columns."""
    with pytest.raises(RiskMatrixValidationError):
        engine.load_csv(csv_non_numeric_probability)


def test_calculate_scores_out_of_range_values(
    engine: RiskAssessmentEngine,
    csv_out_of_range_values: Path,
) -> None:
    """calculate_scores should enforce the 1-5 range for probability/impact."""
    df = engine.load_csv(csv_out_of_range_values)
    with pytest.raises(RiskMatrixValidationError):
        engine.calculate_scores(df)


def test_calculate_scores_null_values(engine: RiskAssessmentEngine) -> None:
    """calculate_scores should reject null or non-numeric values."""
    df = pd.DataFrame(
        {
            "Asset": ["Device1", "Device2"],
            "Threat": ["T1", "T2"],
            "Probability": [1, None],
            "Impact": [3, 4],
        }
    )
    with pytest.raises(RiskMatrixValidationError):
        engine.calculate_scores(df)


def test_load_csv_injection_sanitisation(
    engine: RiskAssessmentEngine,
    csv_with_injection: Path,
) -> None:
    """load_csv should sanitise potential CSV injection payloads."""
    df = engine.load_csv(csv_with_injection)

    # String values starting with = + - @ should be prefixed with a single quote.
    assert df.loc[0, "Asset"].startswith("'")
    assert df.loc[0, "Threat"].startswith("'")
    assert df.loc[1, "Asset"].startswith("'")
    assert df.loc[1, "Threat"].startswith("'")


def test_export_csv_injection_sanitisation(
    engine: RiskAssessmentEngine,
    tmp_path: Path,
) -> None:
    """export_csv should sanitise values before writing to disk."""
    df = pd.DataFrame(
        {
            "Asset": ["=InjectedAsset"],
            "Threat": ["+SUM(A1:A2)"],
            "Probability": [3],
            "Impact": [3],
        }
    )
    scored = engine.calculate_scores(df)

    output_path = tmp_path / "injection_scored.csv"
    engine.export_csv(scored, output_path)

    content = output_path.read_text(encoding="utf-8")
    # Check that dangerous prefixes are guarded with a single quote.
    assert "'=InjectedAsset" in content
    assert "'+SUM(A1:A2)" in content


def test_load_csv_empty_file(engine: RiskAssessmentEngine, tmp_path: Path) -> None:
    """load_csv should raise an error for completely empty files."""
    empty_path = tmp_path / "empty.csv"
    empty_path.touch()

    # pandas raises EmptyDataError for a 0-byte CSV file.
    with pytest.raises(pd.errors.EmptyDataError):
        engine.load_csv(empty_path)


def test_load_csv_wrong_format_no_data(engine: RiskAssessmentEngine, tmp_path: Path) -> None:
    """load_csv should report a clear error if there are headers but no data rows."""
    # Single-line text becomes header only and yields an empty DataFrame.
    bad_path = tmp_path / "bad.csv"
    bad_path.write_text("not,really,a,header", encoding="utf-8")

    with pytest.raises(RiskMatrixValidationError):
        engine.load_csv(bad_path)


def test_load_csv_enforces_size_limit(
    engine: RiskAssessmentEngine,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """load_csv should enforce the maximum file size limit."""
    # Create a small but non-empty file.
    path = tmp_path / "big.csv"
    path.write_text(
        "Asset,Threat,Probability,Impact\nDevice,Threat,3,3\n",
        encoding="utf-8",
    )

    # Force a very small limit so that this file exceeds it.
    monkeypatch.setattr(assessment_module, "_MAX_FILE_SIZE_BYTES", 1)

    with pytest.raises(RiskAssessmentError):
        engine.load_csv(path)


def test_export_csv_resolves_output_path(
    engine: RiskAssessmentEngine,
    valid_csv_path: Path,
    tmp_path: Path,
) -> None:
    """export_csv should work with relative output paths under an existing directory."""
    df = engine.load_csv(valid_csv_path)
    scored = engine.calculate_scores(df)

    # Use a relative path inside tmp_path.
    relative_path = tmp_path / "subdir" / "scored.csv"
    relative_path.parent.mkdir(parents=True, exist_ok=True)

    written_path = engine.export_csv(scored, relative_path)
    assert written_path.exists()
    # Ensure resolve() was applied (absolute path).
    assert written_path.is_absolute()


def test_calculate_scores_direct_dataframe(engine: RiskAssessmentEngine) -> None:
    """calculate_scores should operate correctly on a manually created DataFrame."""
    df = pd.DataFrame(
        {
            "Asset": ["DeviceA"],
            "Threat": ["ThreatA"],
            "Probability": [5],
            "Impact": [5],
        }
    )
    scored = engine.calculate_scores(df)
    assert scored.loc[0, "Risk"] == 25
    assert scored.loc[0, "RiskLevel"] == "critical"
