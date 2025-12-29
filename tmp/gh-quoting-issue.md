## Problem

When creating or editing GitHub issues via `gh issue create` or `gh issue edit`, complex markdown bodies with backticks, quotes, and special characters cause shell quoting issues (`dquote>` prompts, stuck commands).

## Current Workaround

Write issue body to a file first, then use `--body-file`:

```bash
# Write body to temp file
cat > tmp/issue-body.md << 'EOF'
## Issue content here
With backticks and "quotes" safely
EOF

# Use file for issue
gh issue edit NN --body-file tmp/issue-body.md
```

## Desired Outcome

Document a reliable pattern for creating/editing issues with complex markdown from agent workflows.

## Tasks

- [ ] Document escaping rules for inline `--body`
- [ ] Create helper script or function for issue creation
- [ ] Test with various markdown content (code blocks, quotes, backticks)
- [ ] Add to multi-agent workflow docs

## Notes

This is infrastructure work to support agent-driven issue management.
