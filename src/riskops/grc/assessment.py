"""Risk assessment engine for healthcare IoMT using EBIOS RM Light.

This module implements the :class:`RiskAssessmentEngine` used to load,
validate, score, and export risk matrices for healthcare / IoMT contexts.

The implementation is intentionally self-contained and uses only the
standard library and pandas so it can be reused from the CLI layer
without importing additional project modules.

The risk model is inspired by an EBIOS RM Light style approach:

* Each risk scenario is characterised at minimum by:
  - An asset (target of the risk).
  - A threat (or feared event).
  - A probability / likelihood score (1-5).
  - An impact score (1-5).

* The intrinsic risk score is computed as:

    intrinsic_risk = probability * impact

* The intrinsic risk score is then mapped to qualitative levels:

    1-4   -> "low"
    5-9   -> "medium"
    10-16 -> "high"
    17-25 -> "critical"

These thresholds are common for 5x5 risk matrices and compatible with
a simple EBIOS RM Light style analysis where likelihood and impact are
scored on a 1-5 scale.

The engine provides:

* Safe CSV loading with file size checks and path resolution.
* Basic validation of the risk matrix structure.
* Intrinsic risk score calculation.
* Risk level categorisation.
* Safe CSV export with basic CSV injection hardening.

All functions are type-annotated and documented to comply with strict
typing and documentation requirements.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd

# Hard limit for CSV files used for risk assessment (10 MiB).
_MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024


class RiskAssessmentError(Exception):
    """Base exception for risk assessment related errors."""


class RiskMatrixValidationError(RiskAssessmentError):
    """Raised when the input risk matrix is structurally invalid."""


@dataclass(frozen=True)
class RiskThresholds:
    """Risk score thresholds for qualitative levels.

    Attributes:
        low_max: Inclusive upper bound for the "low" level.
        medium_max: Inclusive upper bound for the "medium" level.
        high_max: Inclusive upper bound for the "high" level.

    Notes:
        Scores strictly greater than ``high_max`` are considered "critical".
    """

    low_max: int = 4
    medium_max: int = 9
    high_max: int = 16

    def level_for_score(self, score: int) -> str:
        """Return the qualitative risk level for a given score.

        Args:
            score: Numeric risk score (typically probability * impact).

        Returns:
            The risk level as one of "low", "medium", "high", or "critical".

        Raises:
            ValueError: If ``score`` is less than 0.
        """
        if score < 0:
            raise ValueError("Risk score cannot be negative.")

        if score <= self.low_max:
            return "low"
        if score <= self.medium_max:
            return "medium"
        if score <= self.high_max:
            return "high"
        return "critical"


class RiskAssessmentEngine:
    """Engine for loading and scoring risk matrices.

    This class encapsulates the logic for:

    * Securely loading CSV-based risk matrices.
    * Validating the required columns.
    * Calculating intrinsic risk scores (probability * impact).
    * Assigning qualitative risk levels.
    * Exporting the enriched matrix back to CSV.

    The engine is designed to be used both from a CLI (Typer) layer and
    programmatically from other modules.

    Example:
        >>> from pathlib import Path
        >>> engine = RiskAssessmentEngine()
        >>> df = engine.load_csv(Path("risk_matrix.csv"))
        >>> scored_df = engine.calculate_scores(df)
        >>> engine.export_csv(scored_df, Path("risk_matrix_scored.csv"))
    """

    # Canonical column names used by this engine.
    ASSET_COLUMN: str = "Asset"
    THREAT_COLUMN: str = "Threat"
    PROBABILITY_COLUMN: str = "Probability"
    IMPACT_COLUMN: str = "Impact"
    SCORE_COLUMN: str = "Risk"
    LEVEL_COLUMN: str = "RiskLevel"

    # Alternative names that may appear in CSV files and will be normalised.
    _LIKELIHOOD_ALIASES: Tuple[str, ...] = ("Likelihood", "Probabilité", "Probabilite")
    _IMPACT_ALIASES: Tuple[str, ...] = ("Severity", "ImpactBusiness", "Gravité", "Gravite")

    def __init__(self, thresholds: Optional[RiskThresholds] = None) -> None:
        """Initialise the risk assessment engine.

        Args:
            thresholds: Optional custom risk thresholds. If not provided,
                default thresholds are used.

        """
        self._thresholds: RiskThresholds = thresholds or RiskThresholds()

    @staticmethod
    def _resolve_path(path: Path) -> Path:
        """Resolve a filesystem path safely.

        Args:
            path: Path to resolve.

        Returns:
            The resolved absolute path.

        Raises:
            FileNotFoundError: If the path does not exist.
            RiskAssessmentError: If the path cannot be resolved.
        """
        try:
            resolved = path.expanduser().resolve(strict=True)
        except FileNotFoundError:
            raise
        except OSError as exc:  # Includes PermissionError and other OS errors.
            raise RiskAssessmentError(f"Unable to resolve path '{path}': {exc}") from exc
        return resolved

    @staticmethod
    def _enforce_size_limit(path: Path) -> None:
        """Ensure the file at ``path`` does not exceed the size limit.

        Args:
            path: Path to a file that must not exceed the configured size limit.

        Raises:
            RiskAssessmentError: If the file is larger than the allowed limit.
        """
        try:
            size = path.stat().st_size
        except OSError as exc:
            raise RiskAssessmentError(f"Unable to read file metadata for '{path}': {exc}") from exc

        if size > _MAX_FILE_SIZE_BYTES:
            raise RiskAssessmentError(
                f"File '{path}' is too large for processing ({size} bytes > {_MAX_FILE_SIZE_BYTES} bytes)."
            )

    @staticmethod
    def _sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Sanitise a DataFrame to mitigate CSV formula injection risks.

        Any string cells starting with one of ``=``, ``+``, ``-``, or ``@`` are
        prefixed with a single quote. This is primarily intended for data
        that might later be exported to CSV or Excel and opened in a
        spreadsheet application.

        Args:
            df: Input DataFrame.

        Returns:
            A copy of ``df`` with potentially dangerous cells sanitised.
        """
        dangerous_prefixes: Tuple[str, ...] = ("=", "+", "-", "@")

        def _sanitize_value(value: object) -> object:
            if isinstance(value, str) and value:
                if value[0] in dangerous_prefixes and not value.startswith("'"):
                    return "'" + value
            return value

        sanitized = df.copy()
        for column in sanitized.columns:
            if pd.api.types.is_object_dtype(sanitized[column].dtype):
                sanitized[column] = sanitized[column].map(_sanitize_value)
        return sanitized

    def _normalise_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise column names to the engine's canonical naming.

        This allows slight variations in input CSV headers (for example
        "Likelihood" instead of "Probability") while preserving a
        predictable internal representation.

        Args:
            df: Input DataFrame.

        Returns:
            A new DataFrame with normalised column names.
        """
        rename_map: Dict[str, str] = {}

        columns_lower: Dict[str, str] = {col.lower(): col for col in df.columns}

        # Map likelihood / probability aliases.
        for alias in (self.PROBABILITY_COLUMN,) + self._LIKELIHOOD_ALIASES:
            lower_alias = alias.lower()
            if lower_alias in columns_lower:
                rename_map[columns_lower[lower_alias]] = self.PROBABILITY_COLUMN
                break

        # Map impact / severity aliases.
        for alias in (self.IMPACT_COLUMN,) + self._IMPACT_ALIASES:
            lower_alias = alias.lower()
            if lower_alias in columns_lower:
                rename_map[columns_lower[lower_alias]] = self.IMPACT_COLUMN
                break

        # Ensure we keep asset and threat names predictable if present.
        # We only rename if present with different capitalisation.
        for canonical in (self.ASSET_COLUMN, self.THREAT_COLUMN):
            lower_canonical = canonical.lower()
            if lower_canonical in columns_lower and columns_lower[lower_canonical] != canonical:
                rename_map[columns_lower[lower_canonical]] = canonical

        if rename_map:
            df = df.rename(columns=rename_map)

        return df

    def load_csv(self, path: Path, encoding: str = "utf-8", delimiter: str = ",") -> pd.DataFrame:
        """Load and validate a CSV-based risk matrix.

        The CSV file is loaded using pandas with basic safety checks:

        * Path resolution (prevents accidental use of non-existent paths).
        * File size limitation (10 MiB by default).
        * CSV injection hardening for string cells.

        The resulting DataFrame will have normalised column names suitable
        for subsequent risk calculations.

        Args:
            path: Path to the CSV file containing the risk matrix.
            encoding: Text encoding used by the CSV file.
            delimiter: Delimiter character used in the CSV (default ",").

        Returns:
            A sanitised and normalised DataFrame representing the risk matrix.

        Raises:
            FileNotFoundError: If the file does not exist.
            RiskAssessmentError: If the file cannot be read or is too large.
            RiskMatrixValidationError: If mandatory columns are missing.
        """
        resolved = self._resolve_path(path)
        self._enforce_size_limit(resolved)

        try:
            df = pd.read_csv(resolved, encoding=encoding, delimiter=delimiter)
        except (OSError, pd.errors.ParserError) as exc:
            raise RiskAssessmentError(f"Failed to read CSV file '{resolved}': {exc}") from exc

        if df.empty:
            raise RiskMatrixValidationError(f"CSV file '{resolved}' does not contain any data.")

        df = self._sanitize_dataframe(df)
        df = self._normalise_columns(df)
        self._validate_structure(df)

        return df

    def _validate_structure(self, df: pd.DataFrame) -> None:
        """Validate that the DataFrame has the required structure.

        Args:
            df: DataFrame to validate.

        Raises:
            RiskMatrixValidationError: If required columns are missing or invalid.
        """
        required_columns = (
            self.ASSET_COLUMN,
            self.THREAT_COLUMN,
            self.PROBABILITY_COLUMN,
            self.IMPACT_COLUMN,
        )

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise RiskMatrixValidationError(
                "Risk matrix is missing required columns: " + ", ".join(missing)
            )

        # Basic type / value checks for probability and impact.
        for col in (self.PROBABILITY_COLUMN, self.IMPACT_COLUMN):
            if not pd.api.types.is_numeric_dtype(df[col]):
                # Attempt coercion to numeric; invalid parsing results become NaN.
                coerced = pd.to_numeric(df[col], errors="coerce")
                if coerced.isna().any():
                    raise RiskMatrixValidationError(
                        f"Column '{col}' must contain only numeric values in the risk matrix."
                    )

    def calculate_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate risk scores and qualitative levels for a risk matrix.

        The following columns are added (or overwritten) in the returned
        DataFrame:

        * ``Risk``: Intrinsic risk score, defined as Probability * Impact.
        * ``RiskLevel``: Qualitative level (low, medium, high, critical).

        Args:
            df: Input risk matrix DataFrame. Must contain at least the
            columns "Asset", "Threat", "Probability", and "Impact".

        Returns:
            A new DataFrame with additional scoring columns.

        Raises:
            RiskMatrixValidationError: If the structure is invalid or if
                probability / impact values are out of the accepted range.
        """
        self._validate_structure(df)

        scored = df.copy()

        # Ensure numeric dtype for calculations.
        for col in (self.PROBABILITY_COLUMN, self.IMPACT_COLUMN):
            scored[col] = pd.to_numeric(scored[col], errors="coerce")

        if scored[self.PROBABILITY_COLUMN].isna().any() or scored[self.IMPACT_COLUMN].isna().any():
            raise RiskMatrixValidationError(
                "Probability and Impact columns must not contain null or non-numeric values."
            )

        # Enforce 1-5 range typical for EBIOS RM Light style scoring.
        for col in (self.PROBABILITY_COLUMN, self.IMPACT_COLUMN):
            if not ((scored[col] >= 1) & (scored[col] <= 5)).all():
                raise RiskMatrixValidationError(
                    f"Column '{col}' contains values outside the allowed 1-5 range."
                )

        scored[self.SCORE_COLUMN] = scored[self.PROBABILITY_COLUMN].astype(int) * scored[
            self.IMPACT_COLUMN
        ].astype(int)

        # Map numerical scores to qualitative levels.
        scored[self.LEVEL_COLUMN] = (
            scored[self.SCORE_COLUMN].astype(int).map(self._thresholds.level_for_score)
        )

        return scored

    def export_csv(
        self,
        df: pd.DataFrame,
        output_path: Path,
        *,
        encoding: str = "utf-8",
        delimiter: str = ",",
        overwrite: bool = False,
    ) -> Path:
        """Export a risk matrix DataFrame to a CSV file.

        The exported CSV will be sanitised to mitigate spreadsheet formula
        injection risks.

        Args:
            df: DataFrame to export. Typically the output of
                :meth:`calculate_scores`.
            output_path: Destination path for the CSV file.
            encoding: Text encoding to use when writing the CSV.
            delimiter: Delimiter character to use in the CSV (default ",").
            overwrite: Whether to overwrite an existing file. If ``False``
                and the file exists, :class:`RiskAssessmentError` is raised.

        Returns:
            The resolved path of the written CSV file.

        Raises:
            RiskAssessmentError: If the file already exists and overwrite is
                disabled, or if the data cannot be written.
        """
        output_path = output_path.expanduser()
        resolved_parent = output_path.parent.resolve()

        if not resolved_parent.exists():
            raise RiskAssessmentError(f"Output directory does not exist: '{resolved_parent}'")

        resolved_output = (resolved_parent / output_path.name).resolve()

        if resolved_output.exists() and not overwrite:
            raise RiskAssessmentError(
                f"Refusing to overwrite existing file '{resolved_output}'. "
                "Pass overwrite=True to allow this."
            )

        sanitized = self._sanitize_dataframe(df)

        try:
            sanitized.to_csv(
                resolved_output,
                index=False,
                encoding=encoding,
                sep=delimiter,
            )
        except OSError as exc:
            raise RiskAssessmentError(
                f"Failed to write CSV file '{resolved_output}': {exc}"
            ) from exc

        return resolved_output
