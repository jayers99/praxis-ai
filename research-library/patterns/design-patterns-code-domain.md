# Software Design Patterns for Praxis Code Domain

**Date:** 2026-01-05
**Topic:** Software design patterns
**Consensus:** High
**Keywords:** design-patterns, GoF, architecture, code-domain, refactoring

---

## Purpose

Document recognized software design patterns and provide guidance on their application within the Praxis methodology, particularly for the Code domain.

## Research Questions

1. Which classical design patterns are most relevant to Praxis principles?
2. How do modern language features affect pattern applicability?
3. What anti-patterns emerge from pattern misuse?
4. How should patterns be applied at different lifecycle stages?

## Key Findings

### 1. Patterns Align with Praxis Principles

Several classical patterns directly support Praxis core principles:

| Pattern | Praxis Principle | Alignment |
|---------|------------------|-----------|
| Strategy | Optimize for Change | Isolates variation points, easy to extend |
| Template Method | Lifecycle Stages | Fixed process with variable steps |
| Builder | Work in Small Increments | Incremental, readable construction |
| Repository | Design for Feedback | Testable domain isolated from infrastructure |
| Adapter | Design for Feedback | Integration without modifying existing code |
| Facade | Make Behavior Explicit | Simplifies complex subsystems |

### 2. Architectural Patterns Match Praxis Structure

Praxis itself uses hexagonal architecture:
- **Domain:** Pure business logic (`src/praxis/domain/`)
- **Application:** Use cases and orchestration (`src/praxis/application/`)
- **Infrastructure:** External concerns (`src/praxis/infrastructure/`)

This pattern enables:
- Testability without external dependencies
- Swappable implementations (filesystem → database)
- Clear separation of concerns

### 3. Pattern Overuse is an Anti-Pattern

Research from GoF, Fowler, and Beck emphasizes:
- **Patterns solve recurring problems** — not decoration
- **Start simple, refactor to patterns** — not patterns-first
- **Domain patterns > generic patterns** — business concepts matter more
- **Modern languages internalize patterns** — some patterns now obsolete

### 4. Stage-Specific Pattern Guidance

| Stage | Pattern Guidance |
|-------|------------------|
| Explore/Shape | Identify problems, avoid premature patterns |
| Formalize | Document pattern choices in SOD |
| Execute | Implement patterns, extract from duplication |
| Sustain | Evolve patterns as needs change |

## Classical Pattern Catalog

### Creational Patterns (5)
1. **Singleton** — One instance only (use sparingly)
2. **Factory Method** — Interface for object creation
3. **Abstract Factory** — Families of related objects
4. **Builder** — Step-by-step construction
5. **Prototype** — Clone existing objects

### Structural Patterns (7)
1. **Adapter** — Make incompatible interfaces work
2. **Bridge** — Separate abstraction from implementation
3. **Composite** — Treat objects and compositions uniformly
4. **Decorator** — Add responsibilities dynamically
5. **Facade** — Simplified interface to subsystem
6. **Flyweight** — Share state for efficiency
7. **Proxy** — Placeholder for another object

### Behavioral Patterns (11)
1. **Chain of Responsibility** — Pass requests along chain
2. **Command** — Encapsulate requests as objects
3. **Interpreter** — Define grammar for language
4. **Iterator** — Sequential access without exposing structure
5. **Mediator** — Encapsulate object interactions
6. **Memento** — Capture/restore state
7. **Observer** — One-to-many notifications
8. **State** — Behavior changes with state
9. **Strategy** — Interchangeable algorithms
10. **Template Method** — Algorithm skeleton with variable steps
11. **Visitor** — Separate algorithms from structure

### Architectural Patterns
1. **Repository** — Mediate between domain and data
2. **Service Layer** — Application boundary
3. **Domain Model** — Business logic with data
4. **Layered Architecture** — Separation by abstraction level
5. **Hexagonal Architecture** — Isolate business logic (Ports & Adapters)
6. **CQRS** — Separate reads from writes
7. **Event Sourcing** — State as event sequence

## Anti-Patterns to Avoid

### 1. Pattern Overuse (Golden Hammer)
- **Problem:** Applying patterns everywhere
- **Detection:** More pattern code than business logic
- **Solution:** Start simple, refactor when needed

### 2. Singleton Abuse
- **Problem:** Global state masquerading as pattern
- **Detection:** Hard to test, hidden dependencies
- **Solution:** Dependency injection

### 3. Anemic Domain Model
- **Problem:** Domain objects just data, all logic in services
- **Detection:** Getters/setters only, no behavior
- **Solution:** Rich domain models with behavior

### 4. Deep Inheritance Hierarchies
- **Problem:** 4+ levels of inheritance
- **Detection:** Fragile base class, hard to trace behavior
- **Solution:** Composition over inheritance

### 5. Premature Abstraction
- **Problem:** Creating patterns before second use case
- **Detection:** Abstract interfaces with single implementation
- **Solution:** Rule of Three—abstract on third repetition

## Pattern Selection Heuristics

**Before applying a pattern:**

1. **Identify recurring problem** — Seen at least twice?
2. **Simpler alternative?** — Can you solve it without a pattern?
3. **Change enablement** — Does pattern make code easier to change?
4. **Language features** — Does your language provide this natively?
5. **Explain in one sentence** — Can you justify the pattern choice clearly?

**Example decision process:**

```
Problem: Multiple validation rules, frequently adding new ones
Pattern considered: Strategy
Simpler alternative: If/else chain
Decision: Strategy—rules growing, need isolation
Justification: Each validator testable in isolation, easy to add new ones
```

## Modern Language Considerations

### Python-Specific

1. **First-class functions** → Replace Strategy pattern
   ```python
   # Instead of Strategy classes
   validators = [validate_email, validate_length, validate_format]
   errors = [v(data) for v in validators if not v(data)]
   ```

2. **Decorators** → Replace Decorator pattern
   ```python
   @cache
   @retry(times=3)
   def expensive_operation(): ...
   ```

3. **Context managers** → Replace Template Method for resource management
   ```python
   with open(file) as f:  # Handles open/close
       process(f)
   ```

4. **Dataclasses** → Replace Builder for simple cases
   ```python
   @dataclass
   class User:
       name: str
       email: str
       role: str = "user"  # Defaults
   ```

### When Patterns Still Matter

Even with modern features, patterns remain valuable for:
- **Communication** — Shared vocabulary ("this uses Repository pattern")
- **Complex cases** — When language features insufficient
- **Framework design** — Extensibility points
- **Cross-team consistency** — Agreed-upon solutions

## Integration with Praxis Opinions

This research informed the creation of:
- `opinions/code/design-patterns.md` — Full pattern guidance
- Updates to `opinions/code/README.md` — Navigation links
- Examples using Praxis architecture as demonstration

## Limitations and Future Work

### Limitations
1. **Language-specific** — Examples focus on Python
2. **Classical patterns** — Could expand to modern patterns (Reactive, CQRS details)
3. **Size constraints** — Not all 23 GoF patterns detailed

### Future Work
- [ ] Add pattern examples in other languages (TypeScript, Go, Rust)
- [ ] Document microservices patterns (Circuit Breaker, Saga, etc.)
- [ ] Create pattern detection tools for code review
- [ ] Expand anti-pattern catalog

## Sources

### Primary Sources
1. **Design Patterns: Elements of Reusable Object-Oriented Software** (1994)
   - Authors: Gamma, Helm, Johnson, Vlissides (Gang of Four)
   - Contribution: 23 classical patterns, pattern format
   - Authority: Foundational text, 500k+ citations

2. **Patterns of Enterprise Application Architecture** (2002)
   - Author: Martin Fowler
   - Contribution: Repository, Service Layer, Domain Model patterns
   - Authority: Industry standard for enterprise patterns

3. **Domain-Driven Design** (2003)
   - Author: Eric Evans
   - Contribution: Emphasis on domain patterns over generic patterns
   - Authority: Created DDD movement

4. **Refactoring** (1999, 2nd ed. 2018)
   - Author: Martin Fowler
   - Contribution: When/how to refactor to patterns
   - Authority: Standard refactoring reference

5. **Clean Architecture** (2017)
   - Author: Robert C. Martin
   - Contribution: Hexagonal/Ports & Adapters architecture
   - Authority: Architecture best practices

### Supporting Sources
6. **Software Design Patterns (Wikipedia)**
   - URL: https://en.wikipedia.org/wiki/Software_design_pattern
   - Contribution: Pattern catalog, modern interpretations
   - Last accessed: 2026-01-05

7. **Design Patterns in Dynamic Languages** (1996)
   - Author: Peter Norvig
   - Contribution: 16 of 23 GoF patterns simplified/invisible in dynamic languages
   - Authority: Lisp pioneer, Google Director of Research

8. **Test-Driven Development** (2002)
   - Author: Kent Beck
   - Contribution: Simple Design, YAGNI, refactor to patterns
   - Authority: Created TDD, XP

## Validation

### Internal Consistency
- ✅ Patterns align with existing Praxis principles
- ✅ Praxis codebase demonstrates patterns (hexagonal architecture)
- ✅ Anti-patterns consistent with "Optimize for Change" principle

### External Validation
- ✅ Classical patterns from GoF (industry standard since 1994)
- ✅ Architectural patterns from Fowler, Martin (industry consensus)
- ✅ Anti-patterns validated by Beck, Fowler (avoid premature patterns)

### Practical Application
- ✅ Praxis uses Repository pattern (see `src/praxis/infrastructure/`)
- ✅ Praxis uses hexagonal architecture (domain/application/infrastructure)
- ✅ Opinion file includes executable Python examples

## Consensus Assessment: **High**

**Rationale:**
- Classical patterns have 30+ years of industry validation
- Praxis already uses recommended patterns (hexagonal architecture)
- Anti-pattern guidance aligns with expert consensus (Fowler, Beck, Evans)
- Modern language considerations well-established (Norvig 1996)

**Counter-Evidence:**
- Some teams over-apply patterns (addressed in anti-patterns)
- Pattern terminology can create communication barriers for juniors (addressed with examples)
- Not all patterns apply to all languages (addressed with modern alternatives)

---

_Cataloged: 2026-01-05_
_Reviewed by: Copilot agent_
