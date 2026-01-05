---
domain: code
version: "1.0"
status: active
---

# Software Design Patterns for Code Domain

> **Scope:** Guidance on applying recognized software design patterns within the Praxis methodology. Patterns are solutions to recurring problems—use them as tools, not rules.
>
> **Reference:** Based on Gang of Four (GoF) Design Patterns, Martin Fowler's patterns, and Domain-Driven Design.

## Core Principles

### 1. Patterns Serve Change, Not Complexity

- **Statement:** Apply patterns to make code easier to change, not to demonstrate knowledge or add structure
- **Rationale:** Patterns add indirection; justify the cost with actual flexibility needs
- **Source:** Martin Fowler (Refactoring), Praxis "Optimize for Change" principle
- **Severity:** must-have

### 2. Recognize Before Applying

- **Statement:** Identify the recurring problem before reaching for a pattern
- **Rationale:** Premature pattern application creates unnecessary complexity
- **Source:** Kent Beck (Simple Design), YAGNI principle
- **Severity:** must-have

### 3. Domain Patterns Over Generic Patterns

- **Statement:** Prefer domain-specific patterns that capture business concepts over generic GoF patterns
- **Rationale:** Domain patterns communicate intent better and align with ubiquitous language
- **Source:** Domain-Driven Design (Eric Evans)
- **Severity:** should-have

### 4. Patterns as Vocabulary, Not Architecture

- **Statement:** Use pattern names to communicate design intent, not as architectural mandates
- **Rationale:** Patterns aid team communication; forcing patterns creates rigid designs
- **Source:** Design Patterns (GoF), Pattern-Oriented Software Architecture
- **Severity:** should-have

### 5. Modern Language Features Supersede Some Patterns

- **Statement:** Recognize when language features provide pattern benefits without pattern complexity
- **Rationale:** First-class functions, decorators, and type systems make some patterns obsolete
- **Source:** Norvig's "Design Patterns in Dynamic Languages"
- **Severity:** should-have

## Patterns Aligned with Praxis Principles

### Strategy Pattern → "Optimize for Change"

**Problem:** Algorithm needs to vary independently from clients that use it

**Praxis Alignment:** Directly supports "Optimize for Change" by isolating variation points

**When to Use:**
- Multiple implementations of same behavior exist or are anticipated
- Behavior selection happens at runtime
- Conditional logic for similar algorithms is spreading

**Example:**
```python
# Strategy for validation rules
class ValidationStrategy(Protocol):
    def validate(self, data: dict) -> list[str]: ...

class StrictValidation:
    def validate(self, data: dict) -> list[str]:
        # Strict rules
        
class LenientValidation:
    def validate(self, data: dict) -> list[str]:
        # Lenient rules

# Client code doesn't change when new strategies added
validator = StrictValidation() if env == "prod" else LenientValidation()
errors = validator.validate(user_data)
```

**Trade-offs:**
- ✅ Easy to add new strategies without modifying existing code
- ✅ Testable in isolation
- ❌ More classes/modules to navigate
- ❌ Overkill if only 2 variants and no growth expected

### Template Method → Lifecycle Stage Patterns

**Problem:** Algorithm structure is fixed but some steps vary

**Praxis Alignment:** Mirrors Praxis lifecycle stages (fixed sequence, variable implementation)

**When to Use:**
- Process has fixed steps but variable implementations
- Avoiding code duplication across similar workflows
- Framework code controlling flow, extension points for users

**Example:**
```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process(self, data: dict) -> dict:
        """Template method defines the algorithm"""
        validated = self.validate(data)
        transformed = self.transform(validated)
        enriched = self.enrich(transformed)
        return self.finalize(enriched)
    
    @abstractmethod
    def validate(self, data: dict) -> dict: ...
    
    @abstractmethod
    def transform(self, data: dict) -> dict: ...
    
    def enrich(self, data: dict) -> dict:
        """Hook method with default implementation"""
        return data
    
    @abstractmethod
    def finalize(self, data: dict) -> dict: ...
```

**Trade-offs:**
- ✅ Reuses common workflow structure
- ✅ Enforces consistent process
- ❌ Inheritance creates tight coupling
- ❌ Harder to reuse individual steps

**Modern Alternative:** Composition with Pipeline pattern

### Builder → Incremental Construction

**Problem:** Constructing complex objects requires many steps or configurations

**Praxis Alignment:** Supports "Work in Small, Reversible Increments"

**When to Use:**
- Object creation has many optional parameters
- Construction process is complex
- Different representations of object needed

**Example:**
```python
class QueryBuilder:
    def __init__(self):
        self._select: list[str] = []
        self._where: list[str] = []
        self._order: list[str] = []
    
    def select(self, *fields: str) -> "QueryBuilder":
        self._select.extend(fields)
        return self
    
    def where(self, condition: str) -> "QueryBuilder":
        self._where.append(condition)
        return self
    
    def order_by(self, field: str) -> "QueryBuilder":
        self._order.append(field)
        return self
    
    def build(self) -> str:
        query = f"SELECT {', '.join(self._select)}"
        if self._where:
            query += f" WHERE {' AND '.join(self._where)}"
        if self._order:
            query += f" ORDER BY {', '.join(self._order)}"
        return query

# Usage: incremental, readable construction
query = (QueryBuilder()
    .select("name", "email")
    .where("active = true")
    .order_by("created_at")
    .build())
```

**Trade-offs:**
- ✅ Readable, self-documenting construction
- ✅ Easy to add new construction options
- ❌ More verbose than simple constructors
- ❌ Mutable state during construction

**Modern Alternative:** Dataclasses with defaults, keyword arguments

### Repository → Domain/Infrastructure Boundary

**Problem:** Separate domain logic from data access concerns

**Praxis Alignment:** Praxis uses hexagonal architecture; Repository is the persistence adapter

**When to Use:**
- Domain model should be persistence-ignorant
- Multiple data sources possible (DB, API, cache)
- Testing domain logic without database

**Example:**
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    """Domain-level abstraction"""
    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None: ...
    
    @abstractmethod
    def save(self, user: User) -> None: ...

# Infrastructure implementation
class PostgresUserRepository(UserRepository):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def find_by_id(self, user_id: str) -> User | None:
        # SQL implementation
        
    def save(self, user: User) -> None:
        # SQL implementation

# Domain services depend on abstraction, not implementation
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
```

**Trade-offs:**
- ✅ Domain remains testable and portable
- ✅ Can swap data sources
- ❌ Additional abstraction layer
- ❌ May expose domain concepts in query interface

### Facade → Simplify Complex Subsystems

**Problem:** Complex subsystem with many components needs simple interface

**Praxis Alignment:** Supports "Make Behavior Explicit" by hiding incidental complexity

**When to Use:**
- Subsystem has many interdependent classes
- Clients need only a subset of functionality
- Migrating from legacy system

**Example:**
```python
# Complex subsystem
class VideoEncoder: ...
class AudioExtractor: ...
class MetadataParser: ...
class ThumbnailGenerator: ...

# Facade provides simple interface
class MediaProcessor:
    def __init__(self):
        self.encoder = VideoEncoder()
        self.audio = AudioExtractor()
        self.metadata = MetadataParser()
        self.thumbs = ThumbnailGenerator()
    
    def process_video(self, file_path: str) -> ProcessedVideo:
        """Single method hides complex orchestration"""
        meta = self.metadata.parse(file_path)
        audio = self.audio.extract(file_path)
        encoded = self.encoder.encode(file_path, meta.settings)
        thumb = self.thumbs.generate(encoded, timestamp=meta.highlight)
        return ProcessedVideo(encoded, audio, thumb, meta)
```

**Trade-offs:**
- ✅ Reduces coupling to subsystem internals
- ✅ Easier for clients to use
- ❌ May hide useful subsystem capabilities
- ❌ Can become god object if not careful

### Adapter → Integration Without Modification

**Problem:** Integrate with existing code/libraries that have incompatible interfaces

**Praxis Alignment:** Enables integration testing and feedback loops with external systems

**When to Use:**
- Third-party library has awkward interface
- Legacy code can't be modified
- Multiple implementations with different interfaces

**Example:**
```python
# External library with inconvenient interface
class LegacyEmailSender:
    def send_mail(self, from_addr, to_addr, subj, body, headers):
        # Old interface
        
# Our domain interface
class EmailService(Protocol):
    def send(self, email: Email) -> bool: ...

# Adapter makes legacy code fit our interface
class LegacyEmailAdapter(EmailService):
    def __init__(self, legacy_sender: LegacyEmailSender):
        self.sender = legacy_sender
    
    def send(self, email: Email) -> bool:
        return self.sender.send_mail(
            email.sender,
            email.recipient,
            email.subject,
            email.body,
            email.headers
        )
```

**Trade-offs:**
- ✅ Don't need to modify legacy code
- ✅ Can swap adapters for different implementations
- ❌ Additional layer of indirection
- ❌ Impedance mismatch may leak through

## Architectural Patterns

### Hexagonal Architecture (Ports & Adapters)

**Problem:** Isolate business logic from external concerns (UI, database, APIs)

**Praxis Alignment:** Praxis itself uses hexagonal architecture (domain/application/infrastructure)

**Structure:**
- **Domain:** Pure business logic, no external dependencies
- **Application:** Use cases that orchestrate domain
- **Infrastructure:** External concerns (files, databases, APIs)
- **Ports:** Interfaces defined by domain/application
- **Adapters:** Infrastructure implementations of ports

**Benefits for Praxis:**
- Domain logic testable without infrastructure
- Easy to swap implementations (filesystem → database)
- Supports "Design for Feedback" through isolated testing

### Layered Architecture

**Problem:** Organize code by level of abstraction

**Layers (top to bottom):**
1. **Presentation:** CLI, web UI
2. **Application:** Use cases, orchestration
3. **Domain:** Business logic
4. **Infrastructure:** External systems

**Rules:**
- Each layer depends only on layers below
- Lower layers don't know about upper layers

**Praxis Application:**
```
src/praxis/
  cli.py                 # Presentation layer
  application/           # Application layer (services)
  domain/                # Domain layer (business models)
  infrastructure/        # Infrastructure layer (filesystem, git)
```

## Common Creational Patterns

### Factory Method

**When to Use:**
- Subclasses determine which class to instantiate
- Framework code needs to create objects but doesn't know specific types

**Praxis Example:**
```python
class StageExecutor(ABC):
    @abstractmethod
    def execute(self, context: Context) -> Result: ...

class StageExecutorFactory:
    def create_executor(self, stage: str) -> StageExecutor:
        if stage == "capture":
            return CaptureExecutor()
        elif stage == "sense":
            return SenseExecutor()
        # ... etc
```

**Modern Alternative:** Registry pattern with decorators

### Dependency Injection

**When to Use:** Always (for testability and flexibility)

**Praxis Alignment:** Core to hexagonal architecture

**Example:**
```python
# Don't create dependencies inside classes
class BadService:
    def __init__(self):
        self.repo = PostgresRepository()  # Tight coupling!

# Inject dependencies from outside
class GoodService:
    def __init__(self, repo: Repository):
        self.repo = repo  # Dependency injected
```

**Benefits:**
- Easy to test (inject mocks)
- Easy to change implementations
- Makes dependencies explicit

## Common Behavioral Patterns

### Observer

**When to Use:**
- One object's state changes need to notify many others
- Event-driven architectures
- Publish-subscribe patterns

**Example:**
```python
class StageTransitionSubject:
    def __init__(self):
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def notify(self, event: StageEvent):
        for observer in self._observers:
            observer.update(event)

# Observers react to stage changes
class MetricsCollector(Observer):
    def update(self, event: StageEvent):
        # Record metrics

class NotificationService(Observer):
    def update(self, event: StageEvent):
        # Send notifications
```

### Command

**When to Use:**
- Need to queue, log, or undo operations
- Decouple invoker from executor

**Example:**
```python
class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

class StageTransition(Command):
    def __init__(self, project: Project, target_stage: str):
        self.project = project
        self.target = target_stage
        self.previous = project.stage
    
    def execute(self):
        self.project.stage = self.target
    
    def undo(self):
        self.project.stage = self.previous
```

## Anti-Patterns

### Pattern Overuse (Golden Hammer)

- **What:** Applying favorite patterns everywhere, regardless of problem
- **Why bad:** Adds complexity without benefit; makes simple code hard to understand
- **Instead:** Start simple; refactor to patterns when pain points emerge
- **Detection:** Code has more pattern infrastructure than business logic

### Singleton Abuse

- **What:** Using Singleton for global state or convenience
- **Why bad:** Hidden dependencies, hard to test, violates single responsibility
- **Instead:** Dependency injection, explicit passing
- **Valid use cases:** Logging, configuration (rarely)

### Anemic Domain Model

- **What:** Domain objects are just data containers; all behavior in services
- **Why bad:** Loses object-oriented benefits, spreads related logic
- **Instead:** Put behavior with data; rich domain models
- **Note:** Sometimes appropriate for CRUD apps with simple logic

### Deep Inheritance Hierarchies

- **What:** 4+ levels of inheritance, overusing Template Method
- **Why bad:** Fragile base class problem, hard to understand behavior
- **Instead:** Composition over inheritance, Strategy pattern

### Premature Abstraction

- **What:** Creating patterns/abstractions before second use case exists
- **Why bad:** Abstract for wrong reasons, harder to change later
- **Instead:** Rule of Three—abstract on third repetition

## Pattern Selection Checklist

Before applying a pattern, ask:

- [ ] What recurring problem am I solving?
- [ ] Have I seen this problem at least twice?
- [ ] Does the pattern make the code easier to change?
- [ ] Can I explain the pattern choice in one sentence?
- [ ] Is there a simpler solution without a pattern?
- [ ] Does my language provide this pattern's benefits natively?

## Stage-Specific Pattern Guidance

### Explore/Shape Stages
- **Avoid:** Applying patterns before understanding problem
- **Focus:** Identify recurring problems that patterns might solve
- **Action:** Spike different approaches

### Formalize/Commit Stages
- **Decision point:** Choose patterns for identified problems
- **Document:** Pattern choices in SOD with rationale
- **Validate:** Patterns support requirements and quality attributes

### Execute Stage
- **Implement:** Apply chosen patterns
- **Refactor:** Extract patterns from emerging duplication
- **Test:** Verify pattern provides expected benefits

### Sustain Stage
- **Evolve:** Refactor to different patterns if needs change
- **Document:** Update pattern usage in architecture docs
- **Review:** Are patterns still serving their purpose?

## AI Guidance for Patterns

### What AI Can Do
- Suggest appropriate patterns for described problems
- Generate pattern implementations in specific languages
- Identify code that could benefit from patterns
- Explain pattern trade-offs

### What AI Should Ask About
- Whether to apply a pattern vs. simpler approach
- Which pattern variant best fits the specific context
- Whether to refactor existing code to use patterns

### What AI Should Avoid
- Applying patterns without clear problem statement
- Choosing complex patterns over simple solutions
- Refactoring working code solely to add patterns

## References

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) — Gang of Four (GoF)
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/books/eaa.html) — Martin Fowler
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) — Eric Evans
- [Refactoring](https://refactoring.com/) — Martin Fowler
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — Robert C. Martin
- [Software Design Patterns (Wikipedia)](https://en.wikipedia.org/wiki/Software_design_pattern)

---

*Last updated: 2026-01-05*
