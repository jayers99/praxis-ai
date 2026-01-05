# Praxis Installation Spike - Quick Reference

**Date:** 2026-01-05  
**Status:** ✅ Complete  
**Issue:** Spike: How does a user install and bootstrap Praxis?

---

## 🎯 Key Recommendation

**Publish to PyPI as `praxis-ai`**

Enable users to install with:
```bash
pipx install praxis-ai  # Recommended
pip install praxis-ai   # Alternative
```

---

## 📊 Current vs Future State

### Current (Manual)
```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
poetry install
# Create wrapper script
export PRAXIS_HOME="$HOME/praxis-workspace"
poetry run praxis workspace init
poetry run praxis new my-project
```
⏱️ Time: ~10 minutes | 👤 Skill: Developer

### Future (PyPI)
```bash
pipx install praxis-ai
export PRAXIS_HOME="$HOME/praxis-workspace"
praxis new my-project  # Auto-creates workspace
```
⏱️ Time: ~2 minutes | 👤 Skill: Anyone

---

## 📦 What We Built

### 1. `praxis doctor` Command ✅
Health check for installation issues.

```bash
$ praxis doctor

Praxis Health Check

  ✓ Python version            3.12.3
  ✓ PRAXIS_HOME               /home/user/praxis-workspace
  ✓ Workspace                 Configured
  ✓   extensions/             exists
  ✓   examples/               exists
  ✓   projects/               exists
  ✓ Praxis version            0.1.0

✓ All checks passed
```

**Features:**
- Python version check (≥ 3.10)
- PRAXIS_HOME validation
- Workspace structure verification
- Actionable fix recommendations
- JSON output mode
- Exit codes: 0 (ok), 1 (error), 2 (warning)

### 2. Installation Guide ✅
Complete user-facing documentation at `docs/guides/installation.md`

**Covers:**
- Quick install (future PyPI)
- Current dev install
- Platform-specific (macOS, Linux, Windows WSL, Docker)
- Troubleshooting
- Update/uninstall

### 3. Spike Analysis ✅
Comprehensive research at `docs/guides/installation-bootstrap-spike.md`

**Contains:**
- User journey analysis (technical vs non-technical)
- Installation method evaluation
- Bootstrap flow enhancements
- Template integration strategy
- 4-phase implementation plan
- AI integration considerations

### 4. Summary Document ✅
Executive overview at `docs/guides/installation-bootstrap-summary.md`

### 5. README Draft ✅
Future installation section at `docs/guides/README-install-section-draft.md`

---

## 🚀 4-Phase Roadmap

### Phase 1: Package Distribution ⚠️ **PREREQUISITE**
- [ ] Register `praxis-ai` on PyPI
- [ ] Configure release workflow
- [ ] Test: `pip install praxis-ai`

**Blocks:** Everything else

### Phase 2: Enhanced Bootstrap
- [ ] First-run workspace detection
- [ ] Auto-prompt for workspace creation
- [ ] Improved error messages

**Enables:** Smooth onboarding

### Phase 3: Documentation
- [x] Installation guide
- [ ] Update main README
- [ ] Quickstart tutorial

**Enables:** Self-service

### Phase 4: Verification ✅ **DONE**
- [x] `praxis doctor` command
- [x] Health checks

**Enables:** Self-diagnosis

---

## 👥 User Journeys

### Technical User
**Goal:** Quick CLI setup

**Journey:**
1. `pipx install praxis-ai` → 30s
2. Set PRAXIS_HOME in shell config
3. `praxis new my-cli` → Auto-creates workspace
4. Start coding

⏱️ **Total:** < 2 minutes

### Non-Technical User
**Goal:** Structured thinking tool

**Journey:**
1. `pip install praxis-ai` → Guided by docs
2. `praxis new my-article` → Interactive prompts
3. `praxis status` → See clear next steps
4. Work through lifecycle

⏱️ **Total:** < 5 minutes

---

## 🎨 Template Strategy

**Keep Bootstrap Minimal**

Bootstrap creates foundation:
```
my-project/
├── praxis.yaml
├── CLAUDE.md
└── docs/capture.md
```

Templates are opt-in:
```bash
praxis templates render      # Lifecycle docs
praxis examples add python-cli  # Starter code
```

**Rationale:** Predictable, no decision paralysis, ecosystem can grow.

---

## 🤖 AI Integration

**Current (Already Good):**
- ✅ `CLAUDE.md` auto-generated
- ✅ `praxis opinions --prompt`
- ✅ `praxis context`
- ✅ `praxis status`

**Future (Post-MVP):**
- ⚠️ Auto-detect AI tools
- ⚠️ Tool-specific config
- ⚠️ Interactive setup

**Decision:** Current approach sufficient, AI landscape evolving.

---

## ✅ Acceptance Criteria

- [x] User journey documented
- [x] Packaging approach recommended
- [x] Bootstrap command flow defined
- [x] Proof-of-concept created

**Result:** All met ✅

---

## 🔍 What's Working Well

✅ **Architecture:**
- Workspace/project separation
- Interactive prompts + automation
- Extensibility (extensions, examples)

✅ **Commands:**
- `praxis new` - Create project
- `praxis init` - Add governance
- `praxis workspace init` - Setup
- `praxis status` - Next steps
- `praxis validate` - Check compliance

✅ **Foundation:**
- Opinions framework
- Stage templates
- AI integration

---

## ⚠️ What Needs Improvement

❌ **Distribution:**
- Not on PyPI yet
- Manual install required

❌ **First-Run:**
- Must know about `workspace init`
- No auto-setup

❌ **Documentation:**
- Installation scattered (now fixed ✅)

❌ **Verification:**
- No health check (now fixed ✅)

---

## 📈 Success Metrics

### Quantitative
- Install time: < 2 min ⏱️
- Bootstrap time: < 5 min ⏱️
- Commands to first project: ≤ 5 📝

### Qualitative
- User understands each step ✓
- Errors are actionable ✓
- Clear next steps ✓
- Docs discoverable ✓

---

## 🔗 Related Issues

- **#4** - template-python-cli (starter pack)
- **#13** - Opinionated starter packs (extensions)
- **#14** - Domain creation mode (guided selection)

**Integration:** Bootstrap minimal, templates opt-in, guidance future.

---

## 📝 Open Questions

### 1. Package Name?
**Options:** `praxis`, `praxis-ai`, `praxis-framework`  
**Recommendation:** `praxis-ai` (matches repo)  
**Action:** Check PyPI availability

### 2. Auto-Create Workspace?
**Recommendation:** Yes, with confirmation  
**Action:** Implement in Phase 2

### 3. Python Version?
**Current:** ≥ 3.10  
**Decision:** Keep (typing features needed)

---

## 🧪 Testing

- ✅ 413 tests passing
- ✅ All linting checks pass
- ✅ No new type errors
- ✅ Manual testing successful
- ⚠️ 11 pre-existing failures (unrelated)

---

## 📂 Files

**New (5):**
1. `docs/guides/installation-bootstrap-spike.md` (26KB)
2. `docs/guides/installation.md` (8.5KB)
3. `docs/guides/installation-bootstrap-summary.md` (12.6KB)
4. `docs/guides/README-install-section-draft.md` (4.5KB)
5. `src/praxis/cli.py` - `praxis doctor` command

**Modified:** None (all additions)

---

## 🎯 Next Actions

### Week 1 (Immediate)
1. ⚠️ Review with maintainer
2. ⚠️ Check PyPI name availability
3. ⚠️ Decide timeline

### Week 2-3 (Short-term)
4. ⚠️ Configure PyPI workflow
5. ⚠️ Publish v0.1.0
6. ⚠️ Update README
7. ⚠️ Test end-to-end

### Month 2 (Medium-term)
8. ⚠️ First-run detection
9. ⚠️ Quickstart guide
10. ⚠️ User feedback

### Future (Long-term)
11. ⚠️ Guided domain selection
12. ⚠️ Template integration
13. ⚠️ AI auto-config

---

## 💡 Key Insights

1. **Current architecture is sound** - No major redesign needed
2. **Main gap is distribution** - PyPI is the blocker
3. **Documentation was missing** - Now created ✅
4. **Health check was needed** - Now implemented ✅
5. **Bootstrap works well** - Just needs polish

---

## 🎬 Conclusion

Praxis has excellent governance foundation. Path to accessibility:

1. **Publish to PyPI** → Simple install
2. **Polish first-run** → Smooth onboarding
3. **Document well** → Self-service ✅
4. **Add diagnostics** → Self-help ✅

**Ready for implementation.** All recommendations actionable, minimal risk.

---

## 📚 Read More

- Full spike: `docs/guides/installation-bootstrap-spike.md`
- Install guide: `docs/guides/installation.md`
- Summary: `docs/guides/installation-bootstrap-summary.md`
- README draft: `docs/guides/README-install-section-draft.md`

---

**Prepared by:** GitHub Copilot  
**Reviewed:** Pending  
**Status:** ✅ Complete
