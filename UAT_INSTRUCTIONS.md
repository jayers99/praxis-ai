# UAT Instructions: Domain-aware Stage Gates in praxis validate

## Overview

This PR implements domain-aware stage gates for the Formalize stage, ensuring that projects cannot progress to or beyond Formalize without the required formalization artifacts. It also adds JSON schema versioning for stability in CI/automation contexts.

## What Changed

### 1. Core Behavior Changes

**Before:** `praxis validate` only checked for artifacts at Commit stage and beyond (4 stages total)

**After:** `praxis validate` now checks for artifacts at Formalize stage and beyond (5 stages total)

Affected domains:
- **Code** → requires `docs/sod.md` at formalize+
- **Create** → requires `docs/brief.md` at formalize+
- **Write** → requires `docs/brief.md` at formalize+
- **Learn** → requires `docs/plan.md` at formalize+
- **Observe** → no artifact required (unchanged)

### 2. JSON Output Versioning

JSON output now includes a `"version": "1.0"` field for schema stability:

```json
{
  "version": "1.0",
  "valid": true,
  "config": { ... },
  "issues": [],
  "tool_checks": []
}
```

### 3. Exit Code Semantics (Documented)

- `0` — Validation passed
- `1` — Validation failed (errors or tool check failures)
- `2` — Usage error (invalid arguments)

## UAT Test Cases

### Test 1: Code Domain at Formalize WITHOUT Artifact (Should Fail)

```bash
# Create test project
mkdir -p /tmp/uat-test-1 && cd /tmp/uat-test-1
cat > praxis.yaml << 'EOF'
domain: code
stage: formalize
privacy_level: personal
environment: Home
EOF

# Run validate (should fail with error about missing docs/sod.md)
praxis validate .
```

**Expected Output:**
```
✗ [ERROR] Stage 'formalize' requires formalization artifact at 'docs/sod.md', but file not found

✗ Validation failed: 1 error(s)
```

**Expected Exit Code:** `1`

### Test 2: Code Domain at Formalize WITH Artifact (Should Pass)

```bash
# Using same project from Test 1, add the artifact
mkdir -p docs
echo "# Solution Overview Document" > docs/sod.md

# Run validate (should pass)
praxis validate .
```

**Expected Output:**
```
✓ Validation passed
```

**Expected Exit Code:** `0`

### Test 3: Create Domain at Formalize WITHOUT Artifact (Should Fail)

```bash
# Create test project
mkdir -p /tmp/uat-test-3 && cd /tmp/uat-test-3
cat > praxis.yaml << 'EOF'
domain: create
stage: formalize
privacy_level: personal
environment: Home
EOF

# Run validate (should fail with error about missing docs/brief.md)
praxis validate .
```

**Expected Output:**
```
✗ [ERROR] Stage 'formalize' requires formalization artifact at 'docs/brief.md', but file not found

✗ Validation failed: 1 error(s)
```

**Expected Exit Code:** `1`

### Test 4: Learn Domain at Formalize WITH Artifact (Should Pass)

```bash
# Create test project
mkdir -p /tmp/uat-test-4 && cd /tmp/uat-test-4
cat > praxis.yaml << 'EOF'
domain: learn
stage: formalize
privacy_level: personal
environment: Home
EOF

# Add the artifact
mkdir -p docs
echo "# Learning Plan" > docs/plan.md

# Run validate (should pass)
praxis validate .
```

**Expected Output:**
```
✓ Validation passed
```

**Expected Exit Code:** `0`

### Test 5: Observe Domain at Formalize (No Artifact Required, Should Pass)

```bash
# Create test project
mkdir -p /tmp/uat-test-5 && cd /tmp/uat-test-5
cat > praxis.yaml << 'EOF'
domain: observe
stage: formalize
privacy_level: personal
environment: Home
EOF

# Run validate (should pass without requiring any artifact)
praxis validate .
```

**Expected Output:**
```
✓ Validation passed
```

**Expected Exit Code:** `0`

### Test 6: Pre-Formalize Stages Do NOT Require Artifacts (Should Pass)

```bash
# Create test project at Shape stage (before Formalize)
mkdir -p /tmp/uat-test-6 && cd /tmp/uat-test-6
cat > praxis.yaml << 'EOF'
domain: code
stage: shape
privacy_level: personal
environment: Home
EOF

# Run validate (should pass even without docs/sod.md)
praxis validate .
```

**Expected Output:**
```
✓ Validation passed
```

**Expected Exit Code:** `0`

### Test 7: JSON Output Includes Version Field

```bash
# Using test project from Test 2 (with valid SOD)
cd /tmp/uat-test-1

# Run validate with --json flag
praxis validate . --json | python3 -m json.tool
```

**Expected Output:** (JSON should include `"version": "1.0"`)
```json
{
  "version": "1.0",
  "valid": true,
  "config": {
    "domain": "code",
    "subtype": null,
    "stage": "formalize",
    "privacy_level": "personal",
    "environment": "Home",
    "coverage_threshold": null
  },
  "issues": [],
  "tool_checks": []
}
```

**Expected Exit Code:** `0`

### Test 8: Strict Mode Treats Warnings as Errors

```bash
# This test requires a project with a warning (e.g., invalid regression)
# For now, verify strict mode is documented and functional via existing tests
praxis validate . --strict
```

**Expected:** Warnings treated as errors (exit code 1)

## Automated Test Coverage

All functionality is covered by automated tests:

```bash
# Run validate feature tests (18 scenarios)
poetry run pytest tests/step_defs/test_validate.py -v

# Run all tests (225 total)
poetry run pytest tests/ -v
```

**Expected:** All tests should pass (225/225)

## Documentation Changes

1. **User Guide** (`docs/guides/user-guide.md`)
   - Expanded `praxis validate` section with:
     - All available options
     - Exit code semantics
     - Validation checks (schema, artifacts, regressions, privacy)
     - JSON output schema with version field
     - Examples
   - Updated stage transition behavior note (formalize+ instead of commit+)

2. **Code Comments**
   - Updated comment in `src/praxis/domain/stages.py` to reflect "formalize+" instead of "commit+"

## Files Modified

- `src/praxis/domain/stages.py` — Added FORMALIZE to REQUIRES_ARTIFACT
- `src/praxis/cli.py` — Added version field to JSON output
- `tests/features/validate.feature` — Added 6 new BDD scenarios
- `tests/step_defs/test_validate.py` — Added step definitions for new scenarios
- `tests/test_domain.py` — Updated unit tests to reflect new behavior
- `docs/guides/user-guide.md` — Comprehensive documentation update

## Backward Compatibility

**Breaking Change:** Projects at Formalize stage that previously passed validation without artifacts will now fail.

**Mitigation:** This is intentional and aligns with the Formalize stage definition. Users must add the required artifact to proceed.

**JSON Schema:** New `version` field is additive and does not break existing JSON parsers.

## Verification Checklist

- [ ] All automated tests pass (225/225)
- [ ] Manual UAT tests 1-7 pass as documented above
- [ ] Linting passes on modified files (`ruff check <files>`)
- [ ] Documentation is clear and accurate
- [ ] JSON output includes version field
- [ ] Exit codes are correct (0=pass, 1=fail)
- [ ] All domains work correctly at Formalize stage

## Notes for Reviewers

1. The implementation is **smaller than originally estimated** because most infrastructure already existed
2. The change is **surgical**: only 1 line added to REQUIRES_ARTIFACT, 1 line for JSON version
3. **All domains** are covered and tested
4. **Documentation** is comprehensive and includes examples
5. **Tests** cover both positive and negative cases for all affected domains
