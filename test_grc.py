from __future__ import annotations

from pathlib import Path

from riskops.grc.assessment import RiskAssessmentEngine


def main() -> None:
    """Quick manual check for the GRC risk assessment engine."""
    engine = RiskAssessmentEngine()

    csv_path = Path("02-Matrices/risk_matrix.csv").resolve()
    df = engine.load_csv(csv_path)
    print(f"Loaded {len(df)} risk scenarios")

    scored_df = engine.calculate_scores(df)
    print("Calculated risk scores")
    print(scored_df[["Asset", "Threat", "Risk", "RiskLevel"]].head())

    output = engine.export_csv(
        scored_df,
        Path("/tmp/risk_scored.csv"),
        overwrite=True,
    )
    print(f"Exported to {output}")


if __name__ == "__main__":
    main()
