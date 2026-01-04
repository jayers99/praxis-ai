# Capture — Raw Notes

**Stage:** Capture  
**Date:** 2025-01-15

---

## Initial thoughts

- Testing in production gets a bad rap, but it's actually essential for modern systems
- You can't fully replicate production conditions in staging—different data, different scale, different user behavior
- Need to distinguish between "cowboy TiP" (reckless) and "disciplined TiP" (pragmatic)

## Supporting links

- https://example.com/google-sre-testing-in-prod
- https://example.com/charity-majors-observability
- https://example.com/progressive-delivery-patterns

## Personal experiences

- At previous company, staging environment was always 6 months behind prod
- Feature flags saved us when a "tested" feature broke in prod
- Best bugs were found by real users, not QA

## Potential angles

- Historical: how we got to TiP (monoliths → microservices)
- Technical: specific techniques (canaries, feature flags, observability)
- Management: risk/value tradeoff, maturity model
- Cultural: shifting from "prevent all failures" to "fail safely"

## Audience possibilities

- Developers (technical deep-dive)
- Engineering managers (risk/value argument)
- QA teams (evolving role)

---

**Next:** Synthesize this into a coherent understanding (Sense stage)
