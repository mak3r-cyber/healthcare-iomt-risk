"""Tests for riskops.grc.compliance.ComplianceMapper.

These tests focus on behaviour and structure rather than the exact
container types used internally (list/tuple/set).
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd
import pytest

from riskops.grc.assessment import RiskAssessmentEngine
from riskops.grc.compliance import (
    ComplianceMapper,
    ComplianceMappingError,
    RiskInputValidationError,
    RiskScenario,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_risk_df(tmp_path: Path) -> pd.DataFrame:
    """Create a small IoMT risk matrix and process it with RiskAssessmentEngine.

    Using the real assessment engine ensures the DataFrame structure is
    compatible with the compliance mapper (columns, types, risk levels).

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        DataFrame with calculated scores and qualitative risk levels.
    """
    csv_path = tmp_path / "risk_matrix.csv"
    csv_content = (
        "Asset,Threat,Probability,Impact,Risk\n"
        "Bluetooth Insulin Pump,Communication Interception,4,5,20\n"
        "PACS Imaging Server,Ransomware,3,5,15\n"
    )
    csv_path.write_text(csv_content, encoding="utf-8")

    engine = RiskAssessmentEngine()
    df = engine.load_csv(csv_path)
    scored_df = engine.calculate_scores(df)
    return scored_df


# ---------------------------------------------------------------------------
# map_risks_to_controls
# ---------------------------------------------------------------------------


def test_map_risks_to_controls_from_dataframe_basic(
    sample_risk_df: pd.DataFrame,
) -> None:
    """Map a DataFrame of risks to compliance controls.

    Verifies:
        - The result is a dict keyed by risk identifier.
        - Each entry exposes required metadata fields.
        - Recommended controls are present for all frameworks.
    """
    mapper = ComplianceMapper()

    mapping = mapper.map_risks_to_controls(sample_risk_df)

    assert isinstance(mapping, dict)
    assert len(mapping) == len(sample_risk_df)

    risk_id, info = next(iter(mapping.items()))

    # Basic structure
    assert isinstance(risk_id, str)
    assert "asset" in info and info["asset"]
    assert "threat" in info and info["threat"]
    assert "risk_level" in info
    assert "domain" in info
    assert "recommended_controls" in info

    # Recommended controls structure
    rec = info["recommended_controls"]
    assert set(rec.keys()) == {"iso_27001", "hipaa", "gdpr"}

    # Accept list/tuple/set; enforce that we have an iterable of strings
    for fw in ("iso_27001", "hipaa", "gdpr"):
        value = rec[fw]
        assert isinstance(value, (list, tuple, set))
        for c in value:
            assert isinstance(c, str)


def test_map_risks_to_controls_from_scenarios(
    sample_risk_df: pd.DataFrame,
) -> None:
    """Map a list of RiskScenario objects and compare to DataFrame mapping.

    The goal is not strict equality but to ensure both input forms are
    supported and produce the same number of mapped risks.
    """
    mapper = ComplianceMapper()

    mapping_df = mapper.map_risks_to_controls(sample_risk_df)

    scenarios: List[RiskScenario] = []
    for _, row in sample_risk_df.iterrows():
        scenarios.append(
            RiskScenario(
                asset=str(row["Asset"]),
                threat=str(row["Threat"]),
                probability=int(row["Probability"]),
                impact=int(row["Impact"]),
                risk_score=float(row["Risk"]),
                risk_level=str(row.get("RiskLevel", "")),
            )
        )

    mapping_scenarios = mapper.map_risks_to_controls(scenarios)

    assert len(mapping_scenarios) == len(mapping_df)


def test_map_risks_to_controls_invalid_input_type() -> None:
    """Invalid input types must raise a RiskInputValidationError."""
    mapper = ComplianceMapper()

    with pytest.raises(RiskInputValidationError):
        # type: ignore[arg-type] - deliberately wrong type for the test
        mapper.map_risks_to_controls({"asset": "invalid"})  # noqa: ERA001


# ---------------------------------------------------------------------------
# generate_gap_analysis
# ---------------------------------------------------------------------------


def test_generate_gap_analysis_without_implemented(
    sample_risk_df: pd.DataFrame,
) -> None:
    """Gap analysis with no implemented controls.

    When implemented_controls is None, all recommended controls should appear
    in the "missing_controls" set and none in "implemented_controls".
    """
    mapper = ComplianceMapper()
    gaps = mapper.generate_gap_analysis(sample_risk_df)

    assert len(gaps) == len(sample_risk_df)

    _, info = next(iter(gaps.items()))

    for section in ("recommended_controls", "implemented_controls", "missing_controls"):
        assert set(info[section].keys()) == {"iso_27001", "hipaa", "gdpr"}

    for fw in ("iso_27001", "hipaa", "gdpr"):
        recommended_iter = info["recommended_controls"][fw]
        implemented_iter = info["implemented_controls"][fw]
        missing_iter = info["missing_controls"][fw]

        # Convert to lists to be agnostic to internal container type
        recommended = list(recommended_iter)
        implemented = list(implemented_iter)
        missing = list(missing_iter)

        # With no implemented controls, all recommended controls are missing.
        assert implemented == []
        assert sorted(recommended) == sorted(missing)


def test_generate_gap_analysis_all_controls_implemented(
    sample_risk_df: pd.DataFrame,
) -> None:
    """Gap analysis when all recommended controls are implemented.

    Build implemented_controls dynamically from the mapper's own output, but
    alter case and add suffix text to verify prefix/case-insensitive matching.
    """
    mapper = ComplianceMapper()
    compliance_map = mapper.map_risks_to_controls(sample_risk_df)

    # Aggregate all recommended controls by framework
    aggregated: Dict[str, set[str]] = {"iso_27001": set(), "hipaa": set(), "gdpr": set()}
    for info in compliance_map.values():
        rec = info["recommended_controls"]
        for fw in ("iso_27001", "hipaa", "gdpr"):
            for c in rec.get(fw, []):
                aggregated[fw].add(str(c))

    # Create implemented_controls with different case and suffixes
    implemented_controls: Dict[str, List[str]] = {}
    for fw, controls in aggregated.items():
        unique_controls = sorted(controls)
        implemented_controls[fw] = [f"{c.upper()} EXTRA" for c in unique_controls]

    gaps = mapper.generate_gap_analysis(
        sample_risk_df,
        implemented_controls=implemented_controls,
    )

    # All recommended controls should now be implemented, none missing.
    for info in gaps.values():
        for fw in ("iso_27001", "hipaa", "gdpr"):
            recommended_tokens = sorted(list(info["recommended_controls"][fw]))
            implemented_tokens = sorted(list(info["implemented_controls"][fw]))
            missing_tokens = list(info["missing_controls"][fw])

            assert recommended_tokens == implemented_tokens
            assert not missing_tokens


def test_generate_gap_analysis_invalid_input_type() -> None:
    """generate_gap_analysis must also validate its risk input."""
    mapper = ComplianceMapper()

    with pytest.raises(ComplianceMappingError):
        # type: ignore[arg-type] - deliberately wrong type for the test
        mapper.generate_gap_analysis({"asset": "invalid"})  # noqa: ERA001
