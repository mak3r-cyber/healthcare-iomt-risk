"""Compliance mapping for healthcare IoMT risk scenarios.

This module provides tools to map risk scenarios (for example those
produced by :mod:`riskops.grc.assessment`) to high-level compliance
requirements across several frameworks:

* ISO/IEC 27001 Annex A controls.
* HIPAA security safeguards (administrative, physical, technical).
* GDPR Article 32 security measures.

The objective is not to provide an exhaustive or authoritative list of
controls, but a pragmatic mapping layer suitable for small and medium
healthcare organisations working with IoMT environments.

Design principles:

* Accept either a pandas DataFrame (typically the output of
  :class:`riskops.grc.assessment.RiskAssessmentEngine`) or a list of
  :class:`RiskScenario` instances.
* Provide deterministic mappings based on simple heuristics using the
  asset and threat description of each scenario.
* Return a structure that can be easily serialised to JSON or further
  processed by reporting modules.

All public functions and methods are fully type-annotated and include
docstrings suitable for strict static analysis.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple, Union

import pandas as pd


class ComplianceMappingError(Exception):
    """Base exception for compliance mapping errors."""


class RiskInputValidationError(ComplianceMappingError):
    """Raised when the risk input structure is invalid or unsupported."""


@dataclass(frozen=True)
class RiskScenario:
    """Representation of a single risk scenario for compliance mapping.

    This dataclass provides a minimal view over the information required
    for compliance mapping. It is compatible with the columns produced by
    :class:`riskops.grc.assessment.RiskAssessmentEngine`.

    Attributes:
        asset: Name or identifier of the asset (for example "Infusion Pump #1").
        threat: Description of the threat or feared event.
        probability: Likelihood score (typically 1-5).
        impact: Impact score (typically 1-5).
        risk_score: Optional numeric risk score (for example probability * impact).
        risk_level: Qualitative risk level (for example "low", "medium",
            "high", "critical").
    """

    asset: str
    threat: str
    probability: Optional[int] = None
    impact: Optional[int] = None
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None


@dataclass(frozen=True)
class ControlMapping:
    """Mapping of a risk domain to compliance controls.

    Attributes:
        iso_27001: Tuple of ISO/IEC 27001 Annex A control identifiers and
            short descriptions.
        hipaa: Tuple of HIPAA safeguard identifiers or categories and
            short descriptions.
        gdpr: Tuple of GDPR Article 32 requirements and descriptions.
    """

    iso_27001: Tuple[str, ...]
    hipaa: Tuple[str, ...]
    gdpr: Tuple[str, ...]


RiskInput = Union[pd.DataFrame, Sequence[RiskScenario]]

GapAnalysisResult = Dict[str, Dict[str, Any]]


def _sanitize_text(value: str) -> str:
    """Sanitise a text value to reduce the risk of CSV/Excel formula injection.

    Args:
        value: Input text.

    Returns:
        Sanitised text, with a leading single quote added if the value
        starts with a spreadsheet formula control character.
    """
    dangerous_prefixes: Tuple[str, ...] = ("=", "+", "-", "@")
    if value and value[0] in dangerous_prefixes and not value.startswith("'"):
        return "'" + value
    return value


class ComplianceMapper:
    """Map risk scenarios to compliance controls and generate gap analyses.

    The mapper uses simple rule-based heuristics based on the asset and
    threat description to associate risk scenarios with relevant
    compliance controls drawn from:

    * ISO/IEC 27001 Annex A.
    * HIPAA administrative, physical, and technical safeguards.
    * GDPR Article 32 security measures.

    This implementation is intentionally pragmatic and focused on
    healthcare / IoMT scenarios. It is not a substitute for a full
    compliance audit and should be reviewed by a qualified professional
    before being used in production.

    Example:
        >>> mapper = ComplianceMapper()
        >>> gaps = mapper.generate_gap_analysis(df, implemented_controls={
        ...     "iso_27001": ["A.5.15", "A.8.16"],
        ...     "hipaa": ["TECH-ACCESS", "ADMIN-RISK-MANAGEMENT"],
        ...     "gdpr": ["ART32-1B"]
        ... })
    """

    # Column names expected from the assessment engine.
    ASSET_COLUMN: str = "Asset"
    THREAT_COLUMN: str = "Threat"
    RISK_LEVEL_COLUMN: str = "RiskLevel"
    RISK_SCORE_COLUMN: str = "Risk"

    def __init__(
        self,
        domain_mappings: Optional[Mapping[str, ControlMapping]] = None,
    ) -> None:
        """Initialise the compliance mapper.

        Args:
            domain_mappings: Optional mapping from domain identifiers
                (for example "access_control", "network_security") to
                :class:`ControlMapping` instances. If omitted, a default
                set tuned for IoMT scenarios is used.
        """
        self._domain_mappings: Dict[str, ControlMapping] = (
            dict(domain_mappings)
            if domain_mappings is not None
            else self._default_domain_mappings()
        )

    @staticmethod
    def _default_domain_mappings() -> Dict[str, ControlMapping]:
        """Return default compliance mappings for common IoMT risk domains.

        The defaults are intentionally concise and focus on typical
        security themes in healthcare IoMT environments: access control,
        network security, device security, data protection, and logging
        or monitoring.

        Returns:
            Dictionary mapping domain identifiers to :class:`ControlMapping`.
        """
        return {
            "access_control": ControlMapping(
                iso_27001=(
                    "A.5.15 - Access control",
                    "A.5.16 - Identity management",
                    "A.8.3 - Secure log-on procedures",
                ),
                hipaa=(
                    "ADMIN-RISK-MANAGEMENT - Security management process",
                    "TECH-ACCESS - Access control (unique user ID, emergency access)",
                ),
                gdpr=(
                    "ART32-1B - Ability to ensure ongoing confidentiality of systems and services",
                ),
            ),
            "network_security": ControlMapping(
                iso_27001=(
                    "A.8.20 - Network security",
                    "A.8.21 - Security of network services",
                ),
                hipaa=(
                    "TECH-TRANSMISSION - Transmission security",
                    "TECH-INTEGRITY - Protection against improper alteration or destruction",
                ),
                gdpr=("ART32-1D - Process for regularly testing and evaluating security measures",),
            ),
            "device_security": ControlMapping(
                iso_27001=(
                    "A.7.8 - Protection of information stored on endpoint devices",
                    "A.7.5 - Secure disposal or re-use of equipment",
                ),
                hipaa=(
                    "PHYS-DEVICE - Device and media controls",
                    "PHYS-WORKSTATION - Workstation security",
                ),
                gdpr=(
                    "ART32-1B - Confidentiality, integrity and availability of processing systems",
                ),
            ),
            "data_protection": ControlMapping(
                iso_27001=(
                    "A.8.10 - Information deletion",
                    "A.8.24 - Cryptographic controls",
                    "A.5.12 - Classification of information",
                ),
                hipaa=(
                    "ADMIN-DATA-GOV - Information access management",
                    "TECH-ENCRYPTION - Encryption and decryption of electronic PHI",
                ),
                gdpr=(
                    "ART32-1A - Pseudonymisation and encryption of personal data",
                    "ART32-1C - Ability to restore availability and access in a timely manner",
                ),
            ),
            "logging_monitoring": ControlMapping(
                iso_27001=(
                    "A.8.15 - Logging",
                    "A.8.16 - Monitoring activities",
                ),
                hipaa=(
                    "TECH-AUDIT - Audit controls",
                    "ADMIN-SECURITY-INCIDENT - Security incident procedures",
                ),
                gdpr=("ART32-1D - Regular testing, assessing and evaluating effectiveness",),
            ),
            "general": ControlMapping(
                iso_27001=(
                    "A.5.1 - Information security policy",
                    "A.5.23 - Information security in use of cloud services",
                ),
                hipaa=("ADMIN-RISK-MANAGEMENT - Risk analysis and risk management",),
                gdpr=("ART32-1 - Appropriate technical and organisational measures based on risk",),
            ),
        }

    @staticmethod
    def _normalize_risk_level(value: Optional[str]) -> Optional[str]:
        """Normalise a risk level string to a canonical lowercase form.

        Args:
            value: Raw risk level string (for example "High", "CRITICAL").

        Returns:
            Normalised risk level or ``None`` if input is falsy.
        """
        if value is None:
            return None
        stripped = value.strip().lower()
        return stripped or None

    @staticmethod
    def _dataframe_from_input(risks: RiskInput) -> pd.DataFrame:
        """Convert a RiskInput (DataFrame or sequence of RiskScenario) to DataFrame.

        Args:
            risks: Either a pandas DataFrame, or a sequence of
                :class:`RiskScenario` instances.

        Returns:
            A pandas DataFrame with at least "Asset" and "Threat" columns.

        Raises:
            RiskInputValidationError: If the input structure is unsupported
                or missing mandatory fields.
        """
        if isinstance(risks, pd.DataFrame):
            if risks.empty:
                raise RiskInputValidationError("Risk DataFrame is empty.")
            # Create a shallow copy to avoid mutating the caller's DataFrame.
            df = risks.copy()
        elif isinstance(risks, Sequence):
            if not risks:
                raise RiskInputValidationError("RiskScenario sequence is empty.")
            if not all(isinstance(item, RiskScenario) for item in risks):
                raise RiskInputValidationError(
                    "When a sequence is provided, all items must be instances of RiskScenario."
                )
            df = pd.DataFrame([asdict(item) for item in risks])
        else:
            raise RiskInputValidationError(
                "Unsupported risk input type. Expected pandas.DataFrame or Sequence[RiskScenario]."
            )

        # Validate mandatory columns.
        for col in ("Asset", "Threat"):
            if col not in df.columns:
                raise RiskInputValidationError(f"Missing required column '{col}' in risk input.")

        # Normalise risk level if present.
        if "RiskLevel" in df.columns:
            df["RiskLevel"] = (
                df["RiskLevel"].astype(str).map(lambda v: ComplianceMapper._normalize_risk_level(v))
            )

        return df

    @staticmethod
    def _classify_domain(asset: str, threat: str, risk_level: Optional[str]) -> str:
        """Classify a risk scenario into a high-level domain.

        The classification is heuristic and based on simple keyword
        matching over the concatenated asset and threat description.

        Args:
            asset: Asset name or description.
            threat: Threat description.
            risk_level: Optional qualitative risk level.

        Returns:
            A domain identifier string that can be used to look up
            compliance mappings (for example "access_control").
        """
        text = f"{asset} {threat}".lower()

        # Access control and identity.
        if any(
            keyword in text
            for keyword in (
                "unauthorized access",
                "unauthorised access",
                "access control",
                "password",
                "credential",
                "login",
                "authentication",
                "mfa",
                "multi-factor",
            )
        ):
            return "access_control"

        # Network security.
        if any(
            keyword in text
            for keyword in (
                "network",
                "wifi",
                "wi-fi",
                "lan",
                "wan",
                "vpn",
                "switch",
                "router",
                "firewall",
                "segmentation",
                "segmented",
            )
        ):
            return "network_security"

        # Device or endpoint security.
        if any(
            keyword in text
            for keyword in (
                "iomt",
                "medical device",
                "infusion pump",
                "ventilator",
                "endpoint",
                "workstation",
                "tablet",
                "laptop",
                "mobile",
                "bedside monitor",
                "pacemaker",
                "scanner",
            )
        ):
            return "device_security"

        # Data protection and cryptography.
        if any(
            keyword in text
            for keyword in (
                "phi",
                "patient data",
                "health record",
                "ehr",
                "emr",
                "database",
                "backup",
                "encryption",
                "crypt",
                "pseudonymisation",
                "pseudonymization",
                "leak",
                "exfiltration",
            )
        ):
            return "data_protection"

        # Logging and monitoring.
        if any(
            keyword in text
            for keyword in (
                "logging",
                "log",
                "monitoring",
                "siem",
                "ids",
                "suricata",
                "alert",
                "detection",
                "soc",
            )
        ):
            return "logging_monitoring"

        # Escalate very high risks to stronger domains if possible.
        if risk_level in {"high", "critical"}:
            # Default to data protection for high impact scenarios if no other match.
            return "data_protection"

        return "general"

    def map_risks_to_controls(self, risks: RiskInput) -> GapAnalysisResult:
        """Map each risk scenario to relevant compliance controls.

        Args:
            risks: Either a pandas DataFrame (typically from
                :class:`riskops.grc.assessment.RiskAssessmentEngine`) or a
            sequence of :class:`RiskScenario` instances.

        Returns:
            Dictionary keyed by a stable risk identifier. Each value is a
            dictionary containing:

            * ``asset``: Asset name.
            * ``threat``: Threat description.
            * ``risk_level``: Optional risk level string.
            * ``domain``: Classified domain identifier.
            * ``recommended_controls``: Dictionary with keys
              ``"iso_27001"``, ``"hipaa"``, and ``"gdpr"``, each mapping to
              a tuple of string identifiers or descriptions.
        """
        df = self._dataframe_from_input(risks)

        risk_level_present = "RiskLevel" in df.columns
        results: GapAnalysisResult = {}

        for _, row in df.iterrows():
            asset_raw = str(row[self.ASSET_COLUMN])
            threat_raw = str(row[self.THREAT_COLUMN])
            asset = _sanitize_text(asset_raw)
            threat = _sanitize_text(threat_raw)

            risk_level_value: Optional[str] = None
            if risk_level_present:
                rl = row.get(self.RISK_LEVEL_COLUMN)
                risk_level_value = (
                    self._normalize_risk_level(str(rl))
                    if rl is not None and str(rl).strip()
                    else None
                )

            domain = self._classify_domain(asset, threat, risk_level_value)
            mapping = self._domain_mappings.get(domain, self._domain_mappings["general"])

            risk_id = f"{asset}::{threat}"
            results[risk_id] = {
                "asset": asset,
                "threat": threat,
                "risk_level": risk_level_value,
                "domain": domain,
                "recommended_controls": {
                    "iso_27001": mapping.iso_27001,
                    "hipaa": mapping.hipaa,
                    "gdpr": mapping.gdpr,
                },
            }

        return results

    def generate_gap_analysis(
        self,
        risks: RiskInput,
        implemented_controls: Optional[Mapping[str, Iterable[str]]] = None,
    ) -> GapAnalysisResult:
        """Generate a gap analysis between risks and implemented controls.

        For each risk scenario, this method identifies which compliance
        controls are recommended (based on the domain mapping) and which
        of those appear to be missing given the set of currently
        implemented controls.

        Args:
            risks: Either a pandas DataFrame (typically from
                :class:`riskops.grc.assessment.RiskAssessmentEngine`) or
                a sequence of :class:`RiskScenario` instances.
            implemented_controls: Optional mapping describing which
                controls are already implemented. Expected keys are
                ``"iso_27001"``, ``"hipaa"``, and ``"gdpr"``, each mapped
                to an iterable of string identifiers (for example
                ``"A.5.15"`` or ``"TECH-ACCESS"``). The comparison is
                case-insensitive and only considers the identifier prefix
                before the first space.

        Returns:
            A dictionary keyed by risk identifier. Each entry contains:

            * ``asset``: Asset name.
            * ``threat``: Threat description.
            * ``risk_level``: Optional risk level.
            * ``domain``: Classified domain.
            * ``recommended_controls``: Recommended controls per framework.
            * ``implemented_controls``: Intersection of recommended and
              implemented controls.
            * ``missing_controls``: Recommended controls that do not
              appear in the implemented set for each framework.

        Raises:
            RiskInputValidationError: If the risk input is invalid.
        """
        recommended = self.map_risks_to_controls(risks)

        # Normalise implemented controls: index by a simple identifier
        # prefix to tolerate descriptive suffixes.
        normalized_implemented: Dict[str, Set[str]] = {
            "iso_27001": set(),
            "hipaa": set(),
            "gdpr": set(),
        }

        if implemented_controls is not None:
            for framework in ("iso_27001", "hipaa", "gdpr"):
                values = implemented_controls.get(framework, [])
                for raw in values:
                    identifier = str(raw).strip()
                    if not identifier:
                        continue
                    token = identifier.split()[0]
                    normalized_implemented[framework].add(token.lower())

        # Compute gaps.
        for risk_id, info in recommended.items():
            recommended_controls = info["recommended_controls"]

            implemented_for_risk: Dict[str, Tuple[str, ...]] = {}
            missing_for_risk: Dict[str, Tuple[str, ...]] = {}

            for framework in ("iso_27001", "hipaa", "gdpr"):
                rec_controls = tuple(recommended_controls.get(framework, ()))
                implemented_subset: List[str] = []
                missing_subset: List[str] = []

                for control in rec_controls:
                    identifier_token = control.split()[0].lower()
                    if identifier_token in normalized_implemented[framework]:
                        implemented_subset.append(control)
                    else:
                        missing_subset.append(control)

                implemented_for_risk[framework] = tuple(implemented_subset)
                missing_for_risk[framework] = tuple(missing_subset)

            info["implemented_controls"] = implemented_for_risk
            info["missing_controls"] = missing_for_risk

        return recommended
