# UAT Instructions: Librarian Query API Enhancements

## Overview

This PR implements the Librarian Query API enhancements as specified in issue #[issue-number]. The implementation adds natural language query capabilities to the research library.

## What Was Implemented

### New Functions

1. **`query_library(question, library_path)`** - Answer questions using library artifacts
2. **`get_artifact_summary(artifact_id, library_path)`** - Extract Executive Summary from artifacts
3. **`get_citations(artifact_id, library_path)`** - Return formatted citations
4. **`assess_coverage(query, library_path)`** - Assess coverage level with reasoning
5. **`extract_keywords(question)`** - Extract searchable keywords from questions

### New Dataclasses

1. **`LibraryResponse`** - Complete query response with coverage, summary, sources, and gaps
2. **`Citation`** - Artifact citation with metadata and key findings
3. **`CoverageAssessment`** - Coverage level assessment with reasoning
4. **`CoverageLevel`** - Literal type: "good" | "partial" | "limited" | "none"

## UAT Testing Instructions

### Prerequisites

```bash
cd praxis-ai
poetry install
```

### Test 1: Basic Query Functionality

```python
from pathlib import Path
from praxis.infrastructure.librarian import query_library

library_path = Path("research-library")
response = query_library("What are praxis roles?", library_path)

# Verify:
assert response.query == "What are praxis roles?"
assert response.coverage.level in ["good", "partial", "limited", "none"]
assert len(response.sources) >= 0
print(f"✓ Coverage: {response.coverage.level}")
print(f"✓ Sources: {len(response.sources)}")
```

### Test 2: Artifact Summary Extraction

```python
from pathlib import Path
from praxis.infrastructure.librarian import get_artifact_summary

library_path = Path("research-library")
summary = get_artifact_summary("roles-rationale-2025-12-28", library_path)

# Verify:
assert summary != ""
assert "Praxis Roles" in summary or "normative" in summary
print(f"✓ Summary extracted: {len(summary)} chars")
print(f"✓ First line: {summary.split(chr(10))[0][:60]}...")
```

### Test 3: Coverage Assessment

```python
from pathlib import Path
from praxis.infrastructure.librarian import assess_coverage

library_path = Path("research-library")
assessment = assess_coverage("roles scrum", library_path)

# Verify:
assert assessment.level in ["good", "partial", "limited", "none"]
assert assessment.match_count >= 0
assert assessment.avg_relevance >= 0.0
print(f"✓ Level: {assessment.level}")
print(f"✓ Matches: {assessment.match_count}")
print(f"✓ Reasoning: {assessment.reasoning}")
```

### Test 4: Citation Formatting

```python
from pathlib import Path
from praxis.infrastructure.librarian import get_citations

library_path = Path("research-library")
citations = get_citations("roles-rationale-2025-12-28", library_path)

# Verify:
assert len(citations) == 1
citation = citations[0]
assert citation.artifact_id == "roles-rationale-2025-12-28"
assert citation.title != ""
assert citation.consensus == "High"
print(f"✓ Citation: {citation.title}")
print(f"✓ Consensus: {citation.consensus}")
```

### Test 5: Error Handling

```python
from pathlib import Path
from praxis.infrastructure.librarian import (
    query_library,
    get_artifact_summary,
    get_citations,
)

library_path = Path("research-library")

# Empty query
response = query_library("", library_path)
assert response.coverage.level == "none"
print("✓ Empty query handled")

# Non-existent artifact
summary = get_artifact_summary("non-existent-id", library_path)
assert summary == ""
print("✓ Non-existent artifact handled")

citations = get_citations("non-existent-id", library_path)
assert citations == []
print("✓ Non-existent citation handled")
```

### Test 6: Keyword Extraction

```python
from praxis.infrastructure.librarian import extract_keywords

# Test stop word removal
keywords = extract_keywords("What are the praxis roles?")
assert "what" not in keywords
assert "are" not in keywords
assert "the" not in keywords
assert "praxis" in keywords
assert "roles" in keywords
print(f"✓ Keywords extracted: {keywords}")
```

## Running Automated Tests

```bash
# Run all librarian tests
poetry run pytest tests/test_librarian.py -v

# Run with coverage
poetry run pytest tests/test_librarian.py -v --cov=praxis.infrastructure.librarian

# Run linter
poetry run ruff check src/praxis/infrastructure/librarian.py

# Run type checker
poetry run mypy src/praxis/infrastructure/librarian.py
```

## Expected Results

- All 21 unit tests should pass
- Linter (ruff) should report no errors
- Type checker (mypy) should report no errors
- No regressions in existing tests

## Coverage Thresholds Verification

Test that coverage levels are assigned correctly:

```python
from pathlib import Path
from praxis.infrastructure.librarian import assess_coverage

library_path = Path("research-library")

# Test various queries
queries = [
    ("roles", ["good", "partial", "limited"]),  # well-covered
    ("lifecycle", ["good", "partial", "limited"]),  # well-covered
    ("zzznonsense123", ["limited", "none"]),  # not covered
]

for query, expected_levels in queries:
    assessment = assess_coverage(query, library_path)
    assert assessment.level in expected_levels
    print(f"✓ {query}: {assessment.level}")
```

## Non-Goals Verification

Verify that the following were NOT implemented (as per requirements):

- ❌ CLI commands (separate ticket)
- ❌ Semantic/vector search (future enhancement)
- ❌ External API integration
- ❌ Research library modification capabilities
- ❌ Advanced NLP question parsing

## Files Changed

- `src/praxis/infrastructure/librarian.py` - Added 329 lines (new functions and dataclasses)
- `tests/test_librarian.py` - Added 231 lines (21 comprehensive tests)

## Acceptance Criteria Met

All Gherkin scenarios from the issue have been verified:

- ✅ Query library with matching artifacts
- ✅ Query library with no matches
- ✅ Get artifact summary
- ✅ Get artifact summary when section missing
- ✅ Get artifact summary for non-existent artifact
- ✅ Assess coverage with high-relevance matches
- ✅ Assess coverage with low-relevance matches
- ✅ Handle empty query gracefully

## Reviewer Notes

1. The implementation follows the proposed approach from the issue
2. All dataclasses use proper type hints including `Literal` for `CoverageLevel`
3. Coverage thresholds are exactly as specified in the requirements
4. Error handling is defensive and graceful (no exceptions thrown, empty returns)
5. Code follows existing patterns in the codebase (hexagonal architecture)
6. All functions have comprehensive docstrings

## Questions or Issues?

If you encounter any issues during UAT, please comment on the PR with:
- The test case that failed
- Expected vs actual behavior
- Any error messages or stack traces
