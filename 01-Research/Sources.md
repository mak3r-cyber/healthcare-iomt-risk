# Sources - IoMT Cyber Risk Assessment

## Regulations & Frameworks (France/EU Focus)

| Source | Link | Notes |
|--------|------|-------|
| CNIL - Health Data | https://www.cnil.fr/fr/sante | Practical guide + FAQ (French DPA) |
| CNIL - Violations 2024 | https://www.cnil.fr/fr/notifications-de-violations-de-donnees-personnelles | Annual incident report (France) |
| CNIL - HDS Framework | https://www.cnil.fr/fr/lagrement-des-hebergeurs-de-donnees-de-sante | Certified Health Data Hosts (HDS) |
| ANSSI - Healthcare Sector | https://cyber.gouv.fr/cybersecurite-du-secteur-sante | Recommendations for healthcare facilities (France) |
| ANSSI - Threat Landscape 2024 | https://cyber.gouv.fr/publications/panorama-de-la-menace-2024 | Annual threat analysis (France) |
| GDPR - Health Data (Art. 9) | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32016R0679 | Special categories of personal data |
| Code Santé Publique L1111-8 | https://www.legifrance.gouv.fr | Legal framework for health data hosting (France) |
| NIS2 Directive | https://digital-strategy.ec.europa.eu/en/policies/nis2-directive | Critical Infrastructure security (EU) |

## International Standards

| Standard | Title | Application |
|-------|-------|-------------|
| ISO/IEC 27001:2022 | ISMS | Foundation for security certification |
| ISO/IEC 27002:2022 | Security Controls | 93 organizational/technical controls |
| ISO/IEC 27005:2022 | IS Risk Management | Risk assessment methodology |
| ISO 27799:2016 | Health informatics - Security management | Healthcare-specific security standard |
| ISO 81001-1:2021 | Health software cybersecurity | Security for medical software |
| NIST SP 800-30 | Risk Assessment Guide | US methodology (widely applicable) |
| NIST SP 800-66 | HIPAA Security Rule | US healthcare compliance |
| NIST Cybersecurity Framework | CSF Healthcare Profile | Sector-specific framework |

## Risk Management Methodologies

| Method | Source | Link |
|---------|--------|------|
| EBIOS Risk Manager | ANSSI | https://cyber.gouv.fr/publications/la-methode-ebios-risk-manager |
| ISO 31000:2018 | ISO | https://www.iso.org/standard/65694.html |
| OCTAVE | SEI Carnegie Mellon | https://www.cisa.gov/resources-tools/services/octave |
| MEHARI | CLUSIF | https://clusif.fr/publications/mehari/ |

## Connected Medical Devices (IoMT)

### Regulations

| Regulation | Link | Scope |
|----------------|------|-------|
| EU MDR 2017/745 | https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32017R0745 | European Medical Device Regulation |
| FDA - Cybersecurity Medical Devices | https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity | US Guidance (best practices) |
| IEC 62304 | https://www.iso.org/standard/38421.html | Software lifecycle for devices |
| IEC 80001 | https://www.iso.org/standard/44863.html | Medical device network standard |

### Documented Vulnerabilities

| Device | CVE/Advisory | Description | Link |
|------------|--------------|-------------|------|
| Medtronic Insulin Pumps | CVE-2019-10961 | Insecure remote service access | https://nvd.nist.gov/vuln/detail/CVE-2019-10961 |
| Implantable Defibrillators | FDA Recall 2021 | Unencrypted Bluetooth connection | https://www.fda.gov/medical-devices/medical-device-recalls |
| Philips Patient Monitors | CVE-2020-12032 | ICEfall - Protocol vulnerabilities | https://www.cisa.gov/news-events/ics-medical-advisories |
| Pacemakers | Multiple CVEs | RF interception, replay attacks | CISA ICS-CERT Search |

**IoMT CVE Research Bases:**
- CISA Medical Device Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories
- NVD (National Vulnerability Database): https://nvd.nist.gov/ → search "medical device," "insulin pump," "pacemaker"
- ICS-CERT Medical: https://www.cisa.gov/topics/industrial-control-systems

## Threats & Incidents 2024-2025

### Healthcare Ransomware

| Source | Link | Key Data |
|--------|------|--------------|
| Cyble - Healthcare Ransomware 2024 | https://cyble.com/blog/ransomware-attacks-on-healthcare-2024/ | Healthcare sector stats |
| Emsisoft - Ransomware Stats | https://www.emsisoft.com/en/blog/statistics/ | Average cost, downtime |
| Recorded Future - Healthcare Threats | https://www.recordedfuture.com/research/healthcare-cyber-threat-landscape | Threat intelligence |
| CERT Santé (France) | https://cert.sante.gouv.fr/ | Reported incidents in France |

### Incident Statistics

| Study | Link | Key Metric |
|-------|------|-----------|
| IBM Cost of Data Breach 2024 | https://www.ibm.com/reports/data-breach | Average cost of healthcare breach: ~M |
| Verizon DBIR 2024 | https://www.verizon.com/business/resources/reports/dbir/ | Healthcare analysis section |
| Ponemon Institute - Healthcare | https://www.ponemon.org/ | Financial + reputational impact |

### Public Use Cases (France)
- CHU Rouen 2019 - Ransomware (Press search)
- AP-HP regular attacks (CERT Santé)
- Testing Laboratories (CNIL notifications)

**Notification Source:** https://www.cnil.fr/fr/notifications-de-violations-de-donnees-personnelles

## Technical Protocols & Standards

### Medical Device Communication

| Protocol | Usage | Security |
|-----------|-------|----------|
| HL7 FHIR | Health data interoperability | https://www.hl7.org/fhir/ - OAuth 2.0, TLS |
| DICOM | Medical imaging | https://www.dicomstandard.org/ - Optional encryption |
| Bluetooth LE (BLE) | Wearable devices | https://www.bluetooth.com/specifications/specs/ - Vulnerable pairing |
| IEEE 802.15.6 | WBAN (Body Area Network) | Healthcare-specific standard |
| 802.1X | Network Authentication | EAP-TLS for medical WiFi |

### Infrastructure

| System | Specific Risks |
|---------|---------------------|
| PACS (Picture Archiving) | Network exposure, lack of legacy encryption |
| EHR/EPR (Patient Record) | Unauthorized access, Web application flaws |
| Imaging Systems (MRI, Scanner) | Obsolete OS (Windows XP/7), lack of network isolation |
| Networked Infusion Pumps | Unpatchable firmware, proprietary protocols |

## Academic Research Papers

**Reference Conferences:**
- IEEE Security & Privacy (symposium)
- USENIX Security
- Black Hat Medical Device Security
- ACM CCS (Computer and Communications Security)

**Search Keywords:**
- "insulin pump vulnerabilities"
- "pacemaker cybersecurity"
- "medical IoT security"
- "healthcare ransomware impact"
- "DICOM security"

**Academic Databases:**
- Google Scholar: https://scholar.google.com
- IEEE Xplore: https://ieeexplore.ieee.org
- ACM Digital Library: https://dl.acm.org

## Research TODO

- [ ] Download ANSSI Panorama 2024 (precise France stats)
- [ ] Extract CNIL health violation figures 2024
- [ ] List 10 CVEs for medical devices 2023-2024
- [ ] Search average hospital ransomware downtime (Emsisoft/Cyble)
- [ ] Find average cost of cyber incident in French healthcare (vs US)
- [ ] Stats on the number of IoMT devices per facility
- [ ] Case study: Documented French hospital incident
- [ ] HDS Compliance: number of certified hosts in France
