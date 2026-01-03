# Domain-Specific Role Variants
**Canonical Reference (v1.0)**

This document defines how core roles adapt across Praxis domains (Code, Create, Write, Learn, Observe).

## Authority

This document is **normative**. When operating in a specific domain, roles should use the appropriate variant terminology and focus areas.

---

## Why Domain Variants?

The core roles (Developer, QA, Architect, etc.) are defined with a Code domain bias. Other domains require adapted terminology and focus:

- A "Developer" in Create domain is a "Maker"
- "Test coverage" in Write domain means "Editorial review"
- "Architecture" in Learn domain means "Learning path design"

Domain variants ensure roles remain meaningful across all Praxis domains.

---

## Domain Variant Matrix

### Core Role Variants

| Base Role | Code | Create | Write | Learn | Observe |
|-----------|------|--------|-------|-------|---------|
| Developer | Developer | Maker | Author | Practitioner | Curator |
| QA | QA/Test Strategist | Critic | Editor | Assessor | Validator |
| Architect | Architect | Creative Director | Structure Editor | Learning Designer | Taxonomist |
| Scrum Master | Scrum Master | Production Manager | Publishing Coordinator | Learning Facilitator | Collection Manager |
| Product Owner | Product Owner | Creative Lead | Editorial Director | Learning Owner | Collection Owner |

### Supporting Role Variants

| Base Role | Code | Create | Write | Learn | Observe |
|-----------|------|--------|-------|-------|---------|
| Security | Security Engineer | Rights Manager | Sensitivity Reviewer | Safety Advisor | Privacy Curator |
| SRE | SRE | Distribution Manager | Publishing Ops | Platform Manager | Archive Manager |
| FinOps | FinOps | Budget Manager | Publishing Economics | Learning Investment | Collection Economics |

---

## Code Domain (Default)

The default role definitions apply. No adaptation needed.

**Key Focus Areas:**
- Functional correctness
- Code quality and maintainability
- Test coverage
- System architecture
- Security vulnerabilities
- Operational reliability

---

## Create Domain

Creative and aesthetic output: visual art, audio, video, interactive, generative, design.

### Role Adaptations

#### Maker (Developer Variant)

**Purpose:** Produce finished creative artifacts.

**Adapted Outputs:**
- Creative artifact (image, audio, video, design)
- Asset files in appropriate formats
- Version history and iterations
- Technical specifications (resolution, format, etc.)

**Adapted Guardrails:**
- Respect creative brief constraints
- Document creative decisions
- Maintain asset organization
- Preserve editability where possible

---

#### Critic (QA Variant)

**Purpose:** Evaluate creative work against brief and quality standards.

**Adapted Focus:**
- Alignment with creative brief
- Technical quality (resolution, color accuracy, audio levels)
- Aesthetic coherence
- Brand consistency
- Accessibility (alt text, captions, contrast)

**Adapted Kickback Triggers:**
- Brief requirements not met
- Technical specs violated
- Aesthetic inconsistency
- Missing accessibility features

---

#### Creative Director (Architect Variant)

**Purpose:** Maintain creative coherence and vision.

**Adapted Outputs:**
- Creative direction documents
- Style guides and mood boards
- Creative decisions with rationale
- Iteration guidance

**Adapted Guardrails:**
- Guide without micromanaging
- Balance vision with practical constraints
- Document creative rationale

---

#### Rights Manager (Security Variant)

**Purpose:** Manage licensing, attribution, and rights.

**Adapted Focus:**
- License compliance (stock assets, fonts, music)
- Attribution requirements
- Usage rights documentation
- Copyright considerations

---

## Write Domain

Structured thought: technical, business, narrative, academic, journalistic.

### Role Adaptations

#### Author (Developer Variant)

**Purpose:** Produce written content.

**Adapted Outputs:**
- Written content (article, documentation, report)
- Supporting materials (bibliography, appendices)
- Version history and drafts
- Source materials and research

**Adapted Guardrails:**
- Follow style guide
- Cite sources appropriately
- Maintain voice consistency
- Respect word count constraints

---

#### Editor (QA Variant)

**Purpose:** Ensure quality, clarity, and correctness.

**Adapted Focus:**
- Grammatical correctness
- Clarity and readability
- Structural coherence
- Factual accuracy
- Style guide compliance
- Audience appropriateness

**Adapted Kickback Triggers:**
- Unclear or confusing passages
- Factual errors
- Style guide violations
- Missing citations
- Inappropriate tone

---

#### Structure Editor (Architect Variant)

**Purpose:** Design document structure and flow.

**Adapted Outputs:**
- Outline and structure recommendations
- Section organization
- Information architecture
- Navigation design (for longer works)

---

#### Sensitivity Reviewer (Security Variant)

**Purpose:** Review for sensitive content, bias, and appropriateness.

**Adapted Focus:**
- Bias detection
- Sensitive topic handling
- Legal liability (defamation, privacy)
- Inclusive language
- Content warnings

---

## Learn Domain

Skill formation: skill, concept, practice, course, exploration.

### Role Adaptations

#### Practitioner (Developer Variant)

**Purpose:** Execute learning activities and produce evidence of learning.

**Adapted Outputs:**
- Practice exercises completed
- Projects and artifacts
- Reflection notes
- Skill demonstrations

**Adapted Guardrails:**
- Focus on learning goals, not just completion
- Document struggles and insights
- Seek feedback actively

---

#### Assessor (QA Variant)

**Purpose:** Evaluate learning progress and competency.

**Adapted Focus:**
- Learning objective achievement
- Skill demonstration quality
- Knowledge retention
- Application capability
- Gap identification

**Adapted Kickback Triggers:**
- Learning objectives not measurable
- Assessment criteria vague
- No evidence of understanding (just memorization)

---

#### Learning Designer (Architect Variant)

**Purpose:** Design learning paths and experiences.

**Adapted Outputs:**
- Learning path design
- Prerequisite mapping
- Activity sequencing
- Assessment strategy
- Resource recommendations

---

#### Safety Advisor (Security Variant)

**Purpose:** Ensure learning environment safety.

**Adapted Focus:**
- Physical safety (for hands-on learning)
- Psychological safety
- Appropriate challenge level
- Support resources available

---

## Observe Domain

Raw capture: notes, bookmarks, clips, logs, captures.

### Role Adaptations

#### Curator (Developer Variant)

**Purpose:** Capture and organize observations.

**Adapted Outputs:**
- Captured content with metadata
- Tags and categorization
- Links and relationships
- Context notes

**Adapted Guardrails:**
- Capture quickly, organize later
- Preserve source information
- Don't over-process raw observations

---

#### Validator (QA Variant)

**Purpose:** Verify capture quality and completeness.

**Adapted Focus:**
- Source preserved
- Metadata complete
- Findability (tags, search)
- No data loss

---

#### Taxonomist (Architect Variant)

**Purpose:** Design organization schemes.

**Adapted Outputs:**
- Tagging taxonomy
- Category structure
- Naming conventions
- Relationship types

---

#### Privacy Curator (Security Variant)

**Purpose:** Manage privacy of captured content.

**Adapted Focus:**
- Personal information handling
- Third-party content rights
- Appropriate sharing levels
- Retention policies

---

## Using Domain Variants

### Automatic Detection

When a project has a `domain` specified in `praxis.yaml`, role invocations should automatically use the appropriate variant terminology.

### Explicit Override

To invoke a specific variant:
```
[ROLE: Maker]  # Create domain Developer variant
[DOMAIN: create]
[PHASE: Execute]
Produce the hero image for the landing page.
```

### Mixed-Domain Projects

Some projects span multiple domains. In these cases:
1. Identify the primary domain for the artifact in question
2. Use the appropriate variant for that artifact
3. Document which variant is being used

---

## Extending Domain Variants

When adding variants for a new domain or role:

1. Identify the core role being adapted
2. Define the domain-specific purpose
3. Adapt outputs to domain artifacts
4. Adapt guardrails to domain constraints
5. Adapt kickback triggers to domain quality standards
6. Add to this document and update the variant matrix
