# Security Policy

## Supported Versions

Praxis is currently in early-stage development.

| Version | Support Status | Python Requirement |
|---------|----------------|-------------------|
| `main` branch (latest commit) | ✅ Supported | >=3.10 |
| Tagged releases | ❌ Not yet available | N/A |
| Older commits | ⚠️ Best-effort only | >=3.10 |

**Support policy:**
- Security fixes will be applied to the `main` branch
- Once stable releases begin, we will support the latest minor version
- If you need a formal release/support policy for your organization, please open an issue

**End-of-life:** Python versions below 3.10 are not supported. When Python 3.10 reaches EOL, we will update the minimum version requirement.

## Reporting a Vulnerability

**Please DO NOT open a public GitHub issue for suspected security vulnerabilities.**

### How to Report

Report privately by emailing:

**Security contact:** jayers (at) users.noreply.github.com

### What to Include

When reporting a vulnerability, please include:

1. **Description:** Clear summary of the issue and its impact
2. **Reproduction steps:** Ideally a minimal proof-of-concept
3. **Affected versions/commits:** If known (e.g., `main` as of commit abc123)
4. **Impact assessment:** What data or behavior is affected?
5. **Proposed mitigation:** If you have suggestions (optional but appreciated)
6. **Disclosure preferences:** How you'd like to be credited (if at all)

### What to Expect

**Response timeline:**
- **Acknowledgment:** Within 5 business days (best-effort)
- **Initial assessment:** Within 10 business days
- **Fix timeline:** Depends on severity and complexity
  - **Critical:** Prioritized immediately
  - **High:** Within 30 days
  - **Medium/Low:** Scheduled with regular development

**Disclosure timeline:**
- We will work with you to determine an appropriate disclosure timeline
- Default: Public disclosure after fix is merged and deployed
- Coordinated disclosure is preferred (90 days from initial report)

**Credit:**
- We will credit you in the fix commit message and any security advisories (unless you prefer anonymity)
- Security researchers may be acknowledged in a SECURITY-CREDITS.md file (future)

## Coordinated Disclosure Policy

- We aim to acknowledge vulnerability reports when possible
- We will work with you to validate the report and determine severity
- Once a fix is ready, we will coordinate public disclosure
- Security advisories will be published via GitHub Security Advisories (when stable releases begin)

## Security Notes and Clarifications

### Privacy Level Enforcement

Privacy levels in Praxis are **intent declarations**, not runtime enforcement barriers:

- ✅ **What IS enforced:** Privacy level validation, downgrade warnings, schema validation
- ❌ **What is NOT enforced:** AI tool selection, network access, data persistence restrictions

**If you believe Praxis behavior could cause unintended disclosure** (e.g., unsafe prompt materialization, privacy level bypass), **please report it as a security issue.**

### Known Limitations

**Current security posture:**
- No artifact signing or provenance attestation
- No SBOM (Software Bill of Materials) generation
- No automated dependency vulnerability scanning in CI
- No secrets detection in commits
- Privacy levels rely on user compliance, not technical enforcement

**Planned improvements:** See "Future Security Roadmap" below.

### Threat Model

**What Praxis protects:**
- Governance correctness (lifecycle rules, required artifacts)
- Privacy intent tracking and validation
- Deterministic policy resolution

**What Praxis does NOT protect against:**
- Data exfiltration through AI tools
- Malicious AI behavior
- Supply chain attacks (no signing/provenance yet)
- Secrets committed to project files

**Praxis is a governance framework, not a security sandbox.** Users are responsible for:
- Selecting appropriate AI tools for their privacy level
- Not committing secrets or sensitive data
- Validating external tool behavior (tests, linters, formatters)

### Dependency Security

**Current approach:**
- Dependencies locked in `poetry.lock`
- Manual updates with review
- Transitive dependencies inherited from Poetry's resolver

**Recommendations for consumers:**
- Run `poetry update` periodically to get security patches
- Review `poetry.lock` changes in PRs
- Use `poetry show --tree` to audit dependency tree
- Consider `pip-audit` or `safety` for vulnerability scanning (not integrated yet)

## Future Security Roadmap

Planned security enhancements:

- [ ] **CI/CD automation:** GitHub Actions for tests, linting, type checking
- [ ] **Dependency scanning:** Automated vulnerability checks (Dependabot or similar)
- [ ] **Artifact signing:** GPG or Sigstore for release integrity
- [ ] **SBOM generation:** Provide Software Bill of Materials for releases
- [ ] **Provenance attestation:** SLSA-compliant build provenance
- [ ] **Privacy enforcement:** Runtime AI tool restrictions based on privacy level
- [ ] **Secrets detection:** Pre-commit hooks for secrets scanning
- [ ] **Security advisories:** Formal CVE publication for critical issues

**Want to help?** Security-related contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security Contact

For security-related questions that are not vulnerabilities (e.g., architecture review, threat modeling discussion), you may open a public issue labeled `security` and `question`.
