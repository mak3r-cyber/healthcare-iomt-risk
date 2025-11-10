# Case Study - Dr. Martin's Medical Practice

## Context
**Type:** General Practitioner's Office
**Location:** Urban area, France
**Staff:**
- 2 General Practitioners
- 1 Medical Secretary
- 1 Nurse
**Patients:** ~2000 active patients
**IT Infrastructure:** Basic, no dedicated Chief Information Security Officer (CISO)

## Scope of Study

### Critical Assets Identified
| Asset | Type | DITCT Criticality |
|-------|------|-------------------|
| EHR Software (Electronic Health Record) | System | D=High, I=High, C=Very High, T=High |
| Local Windows Server | Infrastructure | D=High, I=High, C=High, T=Medium |
| 3 Physician Workstations | Endpoint | D=Medium, I=High, C=Very High, T=Medium |
| Secretariat Workstation | Endpoint | D=High, I=Medium, C=High, T=Medium |
| Internet Box + WiFi | Network | D=High, I=Medium, C=Medium, T=Low |
| External USB Backup | Storage | D=Medium, I=Very High, C=Very High, T=High |
| Patient Data (2000 files) | Data | D=High, I=Very High, C=Very High, T=Very High |

### Network Architecture
```
Internet
   |[Internet Box]
   |
   +-- WiFi (WPA2) ---------- Consulting Tablet
   |
   +-- Switch
        |
        +-- EHR Server (Windows Server 2019)
        +-- Physician Workstation 1 (Windows 11)
        +-- Physician Workstation 2 (Windows 11)
        +-- Secretariat Workstation (Windows 11)
        +-- Network Printer
```
**Identified Issues:**
- No network segmentation (everything on the same VLAN)
- WiFi accessible with a shared password
- No application firewall
- Irregular manual backups

## Risk Analysis (Top 10)

### R001 - Ransomware on EHR Server
**Asset:** Windows EHR Server
**Threat:** Ransomware (patient data encryption)
**Vulnerability:**
- No EDR antivirus (only Windows Defender)
- SMB ports exposed on the local network
- No segmentation
- Backups permanently connected (external USB)
**Scoring:**
- Probability: 4 (Ransomware highly active in the healthcare sector 2024)
- Impact: 5 (Practice halted, 2000 patients affected, mandatory GDPR notification)
- **Risk: 20 (CRITICAL)**
**Decision:** Immediate Reduction
**Action Plan:**
1. **Short Term (Week 1):**
   - Disconnect USB backup after each backup
   - Activate Windows Server file versioning
   - Block SMB ports on the Internet box
2. **Medium Term (Month 1):**
   - Implement HDS Cloud Backup (e.g., Mailinblack Backup)
   - Test complete restoration
   - Apply 3-2-1 Rule: 3 copies, 2 media types, 1 off-site
3. **Long Term (Month 3):**
   - Deploy EDR (e.g., SentinelOne, CrowdStrike)
   - Network segmentation (isolated medical VLAN)
   - Server hardening (disable unused services)
**Cost:** €3000 Year 1, then €1500/year
---

### R002 - Secretariat Phishing
**Asset:** Secretariat Workstation + EHR credentials
**Threat:** Targeted Phishing (credential theft)
**Vulnerability:**
- No MFA on EHR access
- No cybersecurity training
- Email without anti-phishing filter
**Scoring:**
- Probability: 4 (Phishing is common, secretaries are frequent targets)
- Impact: 4 (Total access to patient records, data modification)
- **Risk: 16 (HIGH)**
**Decision:** Reduction
**Action Plan:**
1. Staff Training (2h) - phishing awareness
2. Deploy MFA on EHR (TOTP or FIDO2 key)
3. Anti-phishing email filter (e.g., Proofpoint, Mailinblack)
4. Quarterly phishing simulation
**Cost:** €1500 Year 1, then €800/year
---

### R003 - Consulting Tablet Theft
**Asset:** Physician's Tablet (patient consultation)
**Threat:** Tablet theft/loss
**Vulnerability:**
- No disk encryption
- EHR session remains connected
- Local data storage
**Scoring:**
- Probability: 3 (Theft possible in a medical practice)
- Impact: 3 (Exposure of 50-100 recent patient files)
- **Risk: 9 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Activate tablet encryption (BitLocker if Windows)
2. Automatic EHR session timeout (15 min)
3. MDM (Mobile Device Management) with remote wipe
4. Equipment theft insurance
**Cost:** €500 configuration + €200/year MDM
---

### R004 - Backup Failure
**Asset:** External USB Backup
**Threat:** Data loss (failure, crypto, deletion)
**Vulnerability:**
- Irregular manual backup (1x/week)
- Never tested (restoration)
- Single media type
- Permanently connected (ransomware vulnerable)
**Scoring:**
- Probability: 2 (Rare but possible)
- Impact: 5 (Total loss of patient data in case of incident)
- **Risk: 10 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Daily automatic backup (script)
2. HDS cloud backup (duplicate)
3. Monthly restoration test (sample)
4. Restoration procedure documentation
**Cost:** Included in R001 (HDS cloud)
---

### R005 - Insecure WiFi
**Asset:** Practice WiFi Network
**Threat:** Traffic interception / network access
**Vulnerability:**
- WPA2 (vulnerable to KRACK)
- Shared password for everyone (doctors + waiting room patients)
- No client isolation
- Full access to the medical network
**Scoring:**
- Probability: 3 (Possible attack from parking lot, neighboring building)
- Impact: 3 (Internal network access, traffic eavesdropping)
- **Risk: 9 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Create 2 separate SSIDs:
   - WiFi-Medical (WPA3-Enterprise, certificates)
   - WiFi-Patients (WPA2, captive portal, isolated)
2. VLAN Segmentation
3. Inter-VLAN Firewall (block patient access → server)
**Cost:** €800 (new professional access point) + €200 config
---

### R006 - Unauthorized EHR Access
**Asset:** EHR Software
**Threat:** Unauthorized access (curiosity, malice)
**Vulnerability:**
- No fine-grained access traceability
- Secretary has full access (unnecessary)
- No rights review
**Scoring:**
- Probability: 2 (Small staff, trust)
- Impact: 4 (Confidentiality breach, CNIL)
- **Risk: 8 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Principle of least privilege:
   - Secretary: read-only + appointments
   - Physicians: full access
2. Access logs activated (who consults which file)
3. Semi-annual rights review
4. Alert for access to VIP/sensitive files
**Cost:** Software configuration (included)
---

### R007 - EHR Software Flaw
**Asset:** EHR Software (third-party vendor)
**Threat:** Vulnerability exploitation
**Vulnerability:**
- 2-year-old version (no update)
- Vendor slow with security patches
- Local network exposure
**Scoring:**
- Probability: 2 (Exploitation requires skills)
- Impact: 5 (Access to patient data, modification)
- **Risk: 10 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Update EHR to the latest version
2. Vendor maintenance subscription
3. Network isolation of the EHR server (firewall)
4. Vulnerability monitoring (NVD, CERT)
**Cost:** €1200/year vendor maintenance
---

### R008 - Server Failure
**Asset:** Windows EHR Server
**Threat:** Hardware failure (disk, power supply)
**Vulnerability:**
- 5-year-old server (aging)
- No redundancy
- No hardware support contract
**Scoring:**
- Probability: 2 (MTBF ~5 years)
- Impact: 4 (Practice halted 24-48h, patients rescheduled)
- **Risk: 8 (MEDIUM)**
**Decision:** Acceptance + Contingency Plan
**Action Plan:**
1. Degraded mode procedure (paper for 48h)
2. Stock critical parts (spare disk)
3. Hardware support contract (D+1)
4. Plan server replacement (Budget N+1)
**Cost:** €500/year support + €3000 server N+1
---

### R009 - GDPR Non-Compliance
**Asset:** Patient Data Processing
**Threat:** GDPR Non-compliance (CNIL penalty)
**Vulnerability:**
- No processing register
- No DPO (Data Protection Officer)
- Incomplete patient information
- No procedure for exercising rights
**Scoring:**
- Probability: 3 (CNIL control possible)
- Impact: 3 (€20k penalty + reputation damage)
- **Risk: 9 (MEDIUM)**
**Decision:** Reduction
**Action Plan:**
1. Appoint mutualized external DPO (medical association)
2. Create processing register
3. Update patient information notices
4. Procedure for exercising rights (access, rectification, deletion)
5. Data Protection Impact Assessment (DPIA) if necessary
**Cost:** €800/year mutualized DPO + €500 compliance setup
---

### R010 - Accidental Deletion (Human Error)
**Asset:** Patient Data
**Threat:** Accidental deletion
**Vulnerability:**
- No trash can (permanent deletion)
- No training
- Fatigue, stress
**Scoring:**
- Probability: 2 (Rare but possible)
- Impact: 3 (Loss of patient file, difficult reconstitution)
- **Risk: 6 (LOW)**
**Decision:** Acceptance + Versioning
**Action Plan:**
1. Activate file versioning (30 days)
2. Data handling training
3. Automatic backup covers this risk
**Cost:** €0 (already covered)
---

## Prioritized Action Plan

### Phase 1 - Urgent (Month 1) - Budget €6000
| Action | Risk Addressed | Cost | Responsible |
|--------|---------------|------|-------------|
| HDS Cloud Backup + Test | R001, R004 | €3000 | IT Provider |
| Staff Cybersecurity Training | R002 | €1500 | Consultant |
| MFA on EHR | R002 | €500 | EHR Vendor |
| Disconnect USB Backup | R001 | €0 | Secretariat |
| EHR Software Update | R007 | €1000 | EHR Vendor |

### Phase 2 - Important (Months 2-3) - Budget €4500
| Action | Risk Addressed | Cost | Responsible |
|--------|---------------|------|-------------|
| WiFi Segmentation + VLAN | R005 | €1000 | Network Provider |
| Tablet Encryption + MDM | R003 | €700 | IT Provider |
| EDR on Server + Workstations | R001 | €2000 | Security Vendor |
| GDPR Compliance (DPO + Register) | R009 | €800 | External DPO |

### Phase 3 - Continuous Improvement (Months 4-12) - Budget €3200/year
| Action | Risk Addressed | Cost/year | Responsible |
|--------|---------------|---------|-------------|
| EHR Maintenance | R007 | €1200 | Vendor |
| EDR Renewal | R001 | €1000 | Security Vendor |
| Mutualized DPO | R009 | €800 | Association |
| Server Hardware Support | R008 | €500 | Manufacturer |
**Total Budget:**
- **Year 1:** €13,700 (Initial Investment)
- **Subsequent Years:** €3,200/year (Recurring)

## Expected Results

### Risk Reduction
| Period | Critical Risks | Medium Risks | Low Risks |
|---------|-------------------|----------------|-----------------|
| Before | 2 (R001, R002) | 6 | 2 |
| After Phase 1 | 0 | 4 | 6 |
| After Phase 2 | 0 | 1 | 9 |

### Compliance
✅ GDPR: Register + DPO + Rights Procedures
✅ Backups: 3-2-1 Rule Respected
✅ Hosting: Certified HDS Cloud
✅ Traceability: Active EHR Access Logs

### ROI (Return on Investment)
**Cost of Incident Avoided:**
- Ransomware: €50,000 (Loss of activity + CNIL + Reputation)
- Data Leak: €20,000 (CNIL + Procedures)
**Expected Incident Probability without Measures:** 40% over 3 years
**Expected Cost without Measures:** €28,000 (€70k × 40%)
**Cost of Measures over 3 Years:** €23,300 (€13.7k + 2×€3.2k)
**ROI:** Positive starting Year 3

## Conclusion
This case study demonstrates that a modest-sized medical practice can:
✅ Identify priority cyber risks
✅ Deploy security measures with a limited budget (~€14k)
✅ Achieve GDPR compliance
✅ Protect data for 2000 patients

**Key Success Factors:**
- Risk prioritization (Critical → Low)
- Budget phasing (spreading investment)
- Staff training (human = weak link)
- Solutions adapted to the structure's size (no "gas factory")

**Transferable to:**
- Dental practices
- Physiotherapists
- Pharmacies
- Medical analysis laboratories
