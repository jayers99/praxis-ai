# Security Policy

## Supported versions

Praxis is currently early-stage.

- **Supported**: the latest commit on `main`
- **Python**: `>=3.10` (per `pyproject.toml`)

If you need a formal release/support policy, please open an issue.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for suspected security vulnerabilities.

Instead, report privately by emailing:

- **security contact**: jayers (at) users.noreply.github.com

Include:

- A description of the issue and impact
- Steps to reproduce (ideally a minimal PoC)
- Affected versions/commits (if known)
- Any proposed mitigation

## Coordinated disclosure

- We will acknowledge receipt when possible.
- We will work with you to validate the report and determine severity.
- If a fix is required, we’ll aim to publish it as soon as practical and credit you if desired.

## Security notes

- Privacy levels in Praxis are treated as real constraints, but enforcement may vary by domain/stage and may evolve.
- If you believe Praxis behavior could cause unintended disclosure (e.g., unsafe prompt materialization), please report it as a security issue.
