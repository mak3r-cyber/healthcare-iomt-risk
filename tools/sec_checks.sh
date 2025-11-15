#!/usr/bin/env bash
# Optional security checks for CI.
# If syft or trivy are not installed, we log and exit successfully.

set -u  # on garde juste -u pour éviter les variables non définies

echo "[security] Starting optional security checks"

# --- Syft: SBOM generation ---------------------------------------------------
if command -v syft >/dev/null 2>&1; then
    echo "[security] syft found, running SBOM scan"
    # Exemple de commande (à adapter plus tard si besoin)
    syft dir:. || echo "[security] syft scan failed (non-blocking)"
else
    echo "[security] syft not found, skipping SBOM generation"
fi

# --- Trivy: vulnerability scan -----------------------------------------------
if command -v trivy >/dev/null 2>&1; then
    echo "[security] trivy found, running vulnerability scan"
    # Exemple de commande (non bloquante)
    trivy fs --exit-code 0 --severity HIGH,CRITICAL . \
        || echo "[security] trivy scan failed (non-blocking)"
else
    echo "[security] trivy not found, skipping vulnerability scan"
fi

echo "[security] Optional security checks completed"
