# Sustain Stage Checklist — Code Domain Addendum

This addendum provides Code-specific guidance for the Sustain stage.

## Code Domain: Additional Sustain Activities

- [ ] Monitor application performance and errors
- [ ] Apply security patches and dependency updates
- [ ] Review and address technical debt
- [ ] Maintain test coverage as code evolves
- [ ] Update documentation as features change
- [ ] Monitor and respond to production incidents

## Code-Specific Guidance

For the Code domain, Sustain means **active maintenance and operations**. Code is never truly "done"—it requires ongoing care, updates, and governance.

### Key Activities

1. **Bug Fixes & Patches**
   - Fix reported defects
   - Address edge cases discovered in production
   - Maintain backward compatibility

2. **Dependency Management**
   - Update libraries and frameworks
   - Apply security patches promptly
   - Manage version compatibility

3. **Performance Optimization**
   - Monitor performance metrics
   - Identify and fix bottlenecks
   - Optimize resource usage

4. **Feature Additions (Within Scope)**
   - Add features that fit the existing contract
   - Extend existing capabilities
   - Improve user experience

5. **Technical Debt Management**
   - Refactor to improve code quality
   - Document known limitations
   - Plan debt paydown

6. **Monitoring & Operations**
   - Monitor application health
   - Respond to production incidents
   - Maintain uptime and reliability

### When to Regress to Formalize

Watch for these signals that indicate you're changing the contract:

**Contract Change (Regress to Formalize):**
- Major new feature that changes the core problem you're solving
- Significant architecture change (e.g., monolith → microservices)
- New user personas or audiences not in original SOD
- Fundamental shift in success criteria or goals
- Platform migration that changes constraints

**Implementation Refinement (Stay in Sustain):**
- Bug fixes and patches
- Performance improvements
- Code quality refactoring
- Dependency updates
- Feature additions within existing scope
- UI/UX improvements that don't change core functionality

### Testing & Quality

Maintain quality standards during Sustain:
- [ ] Test coverage remains above threshold
- [ ] All changes have tests
- [ ] Regression testing on updates
- [ ] Documentation stays current

### Version Management

Consider versioning strategy:
- **Semantic Versioning:** MAJOR.MINOR.PATCH
  - PATCH: Bug fixes (Sustain)
  - MINOR: Backward-compatible features (Sustain)
  - MAJOR: Breaking changes (New iteration → Formalize)

### Operations & Monitoring

For production code:
- [ ] Logging and error tracking configured
- [ ] Performance monitoring in place
- [ ] Alerting for critical issues
- [ ] Incident response process defined
- [ ] Backup and recovery tested

## Sustain → Close Triggers

When to move to Close:
- Application is being replaced
- No longer maintained or used
- Sunset decision made
- Migration to new system complete

## References

- [Lifecycle Spec: Sustain Stage](../spec/lifecycle.md#8-sustain)
- [Lifecycle Spec: Iteration vs. Sustain](../spec/lifecycle.md#iteration-vs-sustain)
- [Semantic Versioning](https://semver.org/)
- [ITIL Service Operation](https://en.wikipedia.org/wiki/ITIL)
