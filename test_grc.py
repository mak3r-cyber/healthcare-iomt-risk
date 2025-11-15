from pathlib import Path
from src.riskops.grc.assessment import RiskAssessmentEngine

# Test basique
engine = RiskAssessmentEngine()

# CORRECTION : utiliser le chemin absolu depuis la racine
csv_path = Path("02-Matrices/risk_matrix.csv").resolve()
print(f"Loading from: {csv_path}")

df = engine.load_csv(csv_path)
print(f"✓ Loaded {len(df)} risk scenarios")

scored_df = engine.calculate_scores(df)
print(f"✓ Calculated risk scores")
print("\nTop 5 risks:")
print(scored_df[['Asset', 'Threat', 'Risk', 'RiskLevel']].head())

# Export
output = engine.export_csv(scored_df, Path("/tmp/risk_scored.csv"), overwrite=True)
print(f"\n✓ Exported to {output}")
