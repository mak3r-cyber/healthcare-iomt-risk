## [0.2.0] – 2025-11-14

### Added
- New `riskops` Python package with CLI entrypoint.
- `riskops validate csv` to validate healthcare risk matrices.
- `riskops generate matrix` to generate Excel (Risk Matrix + Heatmap + Dashboard).

### Changed
- Project tooling migrated to `pyproject.toml` (mypy, ruff, black, pytest).

### Deprecated
- `tools/csv2xlsx.py` and `tools/validate_controls_link.py` in favor of the `riskops` CLI.

