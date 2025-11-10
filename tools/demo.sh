#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import pandas as pd; df=pd.read_csv("data/risk_matrix.csv"); print(df.head())
PY
