# AI Code Review Optimization Patterns

<!--
metadata:
  id: patterns-git-ai-review-optimization-2026-01-01
  title: AI Code Review Optimization Patterns
  date: 2026-01-01
  status: validated
  topic: patterns
  keywords: [code-review, copilot, ai-agents, conventional-comments, uat, pr-templates, severity-classification, security]
  consensus: medium
  depth: standard
  sources_count: 18
  ccr_status: mitigations-applied
-->

## Executive Summary

- **Copilot review detection**: No dedicated API or webhook; use standard `pull_request_review` event with `user.login` filter
- **Address-or-explain pattern**: Exists in industry (LLVM, GitLab) but lacks standard name; closest is "comply or explain" from corporate governance
- **UAT in PR templates**: Well-established practice; use checkboxes with automated Actions enforcement
- **AI agent response to comments**: Emerging tooling (CodeRabbit CLI, Claude Code @mentions) enables routing comments to agents
- **Severity classification**: Conventional Comments provides labels; simpler 4-level taxonomy may have better adoption

## Consensus Rating

**Medium**: Primary API documentation is sparse for Copilot review detection. Industry patterns for comment resolution exist across multiple authoritative sources (LLVM, GitLab, Google), though terminology varies.

## Critical Caveats (CCR-Verified)

### Copilot Bot Username is Undocumented

The workflow example using `github.event.review.user.login == 'copilot[bot]'` is based on assumption, not verified API behavior. **Validate before implementation.**

### Security Vulnerabilities in AI Agent Auto-Routing

December 2025 "IDEsaster" disclosure: 30+ CVEs affecting AI coding tools including GitHub Copilot. CVE-2025-64660 enables arbitrary code execution via prompt injection in auto-approve scenarios.

**Required Mitigations:**
- Disable auto-approve for all file writes
- Require human approval gate before agent commits
- Implement content sanitization on PR comments before agent processing
- Log all agent actions for audit

### Premium Request Billing

Starting December 2, 2025, GitHub removed default $0 budgets. Automatic Copilot reviews could generate significant costs at $0.04 per premium request.

## Copilot Review Detection

### Detection Strategy

1. **GitHub Actions Workflow**: Trigger on `pull_request_review` event with `submitted` type
2. **API Polling**: Use `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews` endpoint
3. **Filter by Reviewer**: Check `user.login` field for Copilot's bot account

```yaml
name: Handle Copilot Review
on:
  pull_request_review:
    types: [submitted]

jobs:
  process-review:
    runs-on: ubuntu-latest
    if: contains(github.event.review.user.login, 'copilot')
    steps:
      - name: Process Copilot feedback
        run: echo "Copilot review submitted"
```

### Key Behaviors

| Aspect | Behavior |
|--------|----------|
| Review type | Always "Comment" (never Approve/Request Changes) |
| Blocking | Non-blocking; does not count toward required approvals |
| Timing | Usually completes in <30 seconds |
| Customization | `.github/copilot-instructions.md` controls focus areas |

## Address-or-Explain Protocol

The pattern exists in industry practice but lacks a universally recognized name:

- **LLVM**: "Accept or articulate"
- **GitLab**: "Resolve or defer"
- **General**: "Address or justify"

### Implementation Checklist

```markdown
## Review Comment Resolution Policy

For each review comment, the author MUST:

- [ ] **Address**: Make the requested change and indicate completion
- [ ] **OR Explain**: Provide written justification for not making the change
- [ ] **AND Await**: Obtain reviewer acknowledgment of the explanation

Comments without response block merge. Silence is not resolution.
```

## Severity Classification

### Simple Severity Taxonomy (Recommended)

| Level | Label | Response Time | Merge Allowed? |
|-------|-------|---------------|----------------|
| Critical | `blocker` | Immediate | No |
| High | `must-fix` | Before merge | No |
| Medium | `should-fix` | Next iteration | Yes (with ticket) |
| Low | `nit` | Optional | Yes |

### Copilot Severity Configuration

Use `.github/copilot-instructions.md`:

```markdown
## Review Severity Guidelines

When reviewing, classify issues as:
- **critical**: Security vulnerabilities, data loss risks, crashes
- **high**: Bugs, performance issues, missing error handling
- **medium**: Code style, maintainability, test coverage gaps
- **low**: Formatting, naming preferences, minor optimizations

Only flag issues with >80% confidence. Prefix each comment with severity.
```

## UAT in PR Templates

### Template Pattern

```markdown
## UAT Checklist

### Pre-UAT (Author)
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Deployed to staging/UAT environment
- [ ] **Ready for UAT**: @mention QA team

### UAT Results
- [ ] Functional testing: Pass / Fail / N/A
- [ ] Regression testing: Pass / Fail / N/A
- [ ] UAT sign-off: @approver on YYYY-MM-DD
```

### Automation Options

1. **Checkbox Enforcement**: GitHub can require all checkboxes checked before merge
2. **Label Gates**: Use labels like `qa:pending`, `qa:passed`, `qa:failed` with branch protection

## AI Review Tool Selection

| Need | Copilot | CodeRabbit | Claude Code | Qodo |
|------|---------|------------|-------------|------|
| GitHub-native | Best | Good | Good | Good |
| GitLab support | No | Yes | Yes | Yes |
| One-click fixes | Yes | Yes | Yes | Yes |
| Custom rules | Instruction file | Config | CLAUDE.md | Rules |
| Security focus | CodeQL integration | Limited | Manual | Workflow-based |
| Enterprise/SOC2 | Yes | Limited | Via API | Yes |

## Sources

1. [GitHub Copilot Code Review Docs](https://docs.github.com/en/copilot/concepts/agents/code-review) — primary
2. [LLVM Code Review Policy](https://llvm.org/docs/CodeReview.html) — primary
3. [GitLab Code Review Guidelines](https://docs.gitlab.com/development/code_review/) — primary
4. [Google Eng Practices](https://google.github.io/eng-practices/review/reviewer/standard.html) — primary
5. [Conventional Comments](https://conventionalcomments.org/) — primary
6. [The Hacker News - 30+ Flaws in AI Coding Tools](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html) — CCR source

---
_PKDP Status: CCR mitigations applied, HVA validated_
_Ingested: 2026-01-01_
