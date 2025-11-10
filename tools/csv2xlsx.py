import pathlib, pandas as pd
src = pathlib.Path("02-Matrices/risk_matrix.csv")
dst_dir = pathlib.Path("docs/reports"); dst_dir.mkdir(parents=True, exist_ok=True)
dst = dst_dir / "risk_matrix.xlsx"
pd.read_csv(src).to_excel(dst, index=False, sheet_name="RiskMatrix")
print(f"Wrote {dst}")
