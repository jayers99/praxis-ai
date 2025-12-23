# Opinion: Production CLI Tool

> Unix philosophy, 10-year maintenance horizon, CI/CD safe

## Design Constraints

- Follow the Unix philosophy and GNU coreutils conventions
- Match the UX patterns of HashiCorp, Docker, and AWS CLI tools
- Prefer explicit commands over implicit behavior
- Optimize for composability, predictability, and script safety
- Backwards compatibility is a first-class concern
- Errors must be actionable and non-ambiguous

## Requirements

- Safe to use in shell pipelines
- Separate stdout (data) from stderr (diagnostics)
- Deterministic, stable output
- Meaningful exit codes
- Boring, explicit behavior over cleverness

## Anti-Patterns

- Hidden state
- Clever but surprising behavior
- Overloaded or ambiguous flags
- Implicit destructive actions
- Breaking changes without clear migration paths

## Assumed Context

- Used daily by experienced engineers
- Embedded in CI/CD automation
- Maintained for 10+ years

## Summary

Treat user trust, predictability, and automation safety as first-order design constraints.
