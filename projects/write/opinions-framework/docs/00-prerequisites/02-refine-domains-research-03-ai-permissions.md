# Spike: AI Permission Matrices by Domain


**Issue:** #82
**Type:** Research Spike
**Time Box:** 30 minutes
**Status:** Complete

---

## Spike Intent

Research what AI operations should be allowed in each domain.

---

## Research Findings

### 1. VS Code/GitHub Copilot Security Model

VS Code defines multiple trust boundaries and permission scopes:

| Scope | Description |
|-------|-------------|
| Session-level | Temporary access for current session |
| Workspace-level | Project-specific trust |
| User-level | Broader permissions across projects |

**Key security principles:**
- Workspace-limited file access (AI can only read/write within project)
- Explicit user approval for tool invocations
- User-in-the-loop design for review/rejection of AI output

**Source:** [VS Code Copilot Security](https://code.visualstudio.com/docs/copilot/security)

---

### 2. AI Code Generation Security Risks

Common security issues in AI-generated code:
- IAM policies with overly permissive permissions
- Hardcoded secrets in functions
- Resources deployed with public exposure by default
- API endpoints lacking authentication

**Insight:** AI operations in Code domain need stricter validation than in creative domains.

**Source:** [AI-Generated Code Security Guidelines – AppSecEngineer](https://www.appsecengineer.com/blog/ai-generated-code-needs-its-own-secure-coding-guidelines)

---

### 3. EU AI Act Code of Practice (2025)

The EU's General-Purpose AI Code of Practice covers:
- **Transparency:** Disclosure of AI involvement
- **Copyright:** Respect for training data rights
- **Safety and Security:** Risk mitigation for AI outputs

**Relevance:** Different domains have different transparency and safety requirements.

**Source:** [EU AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai)

---

### 4. Domain-Specific AI Copilot Patterns

Industry examples of domain-specific AI permissions:

| Tool | Domain | Permission Model |
|------|--------|------------------|
| GitHub Copilot | Code | Organization-wide policy enforcement |
| Grammarly | Write | User-controlled suggestion acceptance |
| Adobe Firefly | Create | Content credential watermarking |
| Notion AI | Observe/Write | Context-limited to current document |

**Pattern:** More structured domains (Code) have stricter permission models than creative domains.

**Source:** [Securing AI Coding Tools – Brian Gershon](https://www.briangershon.com/blog/securing-ai-coding-tools/)

---

## Proposed AI Operations Taxonomy

### AI Operation Categories

| Operation | Description | Risk Level |
|-----------|-------------|------------|
| `suggest` | Propose content for human review | Low |
| `complete` | Auto-complete in-progress work | Medium |
| `generate` | Create new content from prompt | Medium |
| `transform` | Modify existing content | High |
| `execute` | Run generated code/commands | Critical |
| `publish` | Make content externally visible | Critical |

---

## Domain × AI Operation Permission Matrix

### Default Permissions (Privacy: Personal, Environment: Home)

| Operation | Code | Create | Write | Learn | Observe |
|-----------|:----:|:------:|:-----:|:-----:|:-------:|
| `suggest` | Yes | Yes | Yes | Yes | Yes |
| `complete` | Yes | Yes | Yes | Yes | No* |
| `generate` | Ask | Yes | Ask | Yes | No |
| `transform` | Ask | Yes | Ask | Yes | No |
| `execute` | Ask | N/A | N/A | N/A | N/A |
| `publish` | Ask | Ask | Ask | Ask | Ask |

**Legend:**
- **Yes** – Allowed by default
- **Ask** – Requires explicit user confirmation
- **No** – Blocked by default
- **N/A** – Not applicable to domain

*Observe domain blocks AI completion to preserve raw, unfiltered capture.

---

### Permission Modifiers by Privacy Level

| Privacy Level | Modifier |
|---------------|----------|
| Public | All `generate`/`transform` → Ask, `publish` → Yes |
| Public-Trusted | Default permissions |
| Personal | Default permissions |
| Confidential | All operations → Ask |
| Restricted | All `generate`/`transform` → No, `execute` → No |

---

### Permission Modifiers by Environment

| Environment | Modifier |
|-------------|----------|
| Home | Default permissions |
| Work | `execute` → Ask, `publish` → Ask |

---

## Risk Considerations by Domain

### Code Domain (High Risk)

| Risk | Mitigation |
|------|------------|
| Security vulnerabilities | Require review before commit |
| Leaked secrets | Block patterns matching credentials |
| License contamination | Disclose AI-generated code |
| Runaway execution | Sandbox generated scripts |

### Create Domain (Medium Risk)

| Risk | Mitigation |
|------|------------|
| Copyright infringement | Content credential metadata |
| Style plagiarism | Reference image attribution |
| Deepfakes | Watermarking requirement |

### Write Domain (Medium Risk)

| Risk | Mitigation |
|------|------------|
| Plagiarism | AI content disclosure |
| Misinformation | Fact-check suggestions |
| Voice loss | Limit full-generation, prefer suggestions |

### Learn Domain (Low Risk)

| Risk | Mitigation |
|------|------------|
| Over-reliance | Encourage retrieval before generation |
| Incorrect information | Mark AI content as provisional |

### Observe Domain (Minimal AI Role)

| Risk | Mitigation |
|------|------------|
| Contaminated capture | Block AI generation/transformation |
| Lost authenticity | Preserve original timestamps |

---

## Privacy Level × AI Permission Philosophy

| Privacy Level | Philosophy |
|---------------|------------|
| Public | AI helps polish for public consumption |
| Public-Trusted | AI assists with trusted collaborators |
| Personal | AI augments personal work freely |
| Confidential | AI access minimized, human approval required |
| Restricted | AI access severely limited, audit all interactions |

---

## Definition of Done Checklist

- [x] AI permissions defined for each of 5 domains
- [x] Permission matrix created
- [x] Risk considerations documented
- [x] Ready for PR

---

## Follow-Up Considerations

1. **Granular operations:** Should `transform` be split into `rewrite`, `summarize`, `expand`?
2. **Audit logging:** What AI operations should be logged for compliance?
3. **Override mechanism:** How can users temporarily elevate/restrict permissions?
4. **Model-specific permissions:** Should permissions vary by AI model capability?

---

## Handoff Summary

**Researched:** AI permission patterns across Praxis domains, drawing from VS Code/Copilot security model, EU AI Act, and industry practices.

**Key findings:**
- 6 AI operation categories identified: suggest, complete, generate, transform, execute, publish
- Permission matrix varies by domain, with Code having strictest controls and Create most permissive
- Observe domain should block AI generation to preserve raw capture authenticity
- Privacy level and environment modify base permissions
- Each domain has specific risks requiring tailored mitigations

**Confidence:** High for Code domain (well-documented industry practices). Medium for creative domains (fewer established patterns).

**Time spent:** Within 30-minute time box.
=======
**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Medium  
**Priority:** Medium

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| **Medium** | **60 min** | **~50 queries** |
| Large | 120 min | ~100 queries |

*This spike is Medium.*

---

## Spike Intent

Research what AI operations should be allowed in each domain. Different domains have different risk profiles for AI assistance.

---

## Research Questions

1. What AI operations are allowed in each domain?
2. How do creative domains (Create) differ from technical (Code)?
3. What AI governance patterns exist in industry?
4. How do ethical considerations differ by domain?
5. What's the relationship between privacy level and AI permissions?

---

## Where to Look

- AI governance literature
- Creative AI ethics (copyright, authorship)
- AI-assisted development best practices
- Enterprise AI policy frameworks

---

## Output Artifacts

1. Research report → `02-refine-domains-research-03-ai-permissions-report.md`
2. Permission matrix (Domain × AI Operation)
3. Risk assessment per domain
4. Follow-up stories if needed

---

## Definition of Done

- [ ] AI permissions defined for each of 5 domains
- [ ] Permission matrix created
- [ ] Risk considerations documented
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 60-minute time box
3. Commit changes to your branch with message: `docs: spike ai permissions research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: AI Permission Matrices by Domain" --body-file <handoff.md> --base main
   ```
5. Include "Closes #XX" in your PR body

---

## Handoff Template

```markdown
## Summary
What you researched and key findings

## Files Changed
- List of files created/modified

## Decisions Made
- Key choices and rationale

## Open Questions
- What remains unknown

## Time Spent
- Actual time vs budget

## Follow-Up Needed
- Recommended next spikes/stories

Closes #XX
```

