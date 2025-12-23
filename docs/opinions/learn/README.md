# Learn Domain Opinions

When `praxis.yaml` has `domain: learn`, load this file into context.

## Available Opinions

| Opinion | Triggers | Summary |
|---------|----------|---------|

## How This Works

1. This README is loaded when domain = learn
2. If conversation matches any **trigger** keywords, load **all** matching detail files
3. If a file extends another, load the base file too
4. Apply all loaded opinions to your reasoning and suggestions

Multiple opinions can apply simultaneously. Base opinions provide general best practices; extended opinions add specific tooling and patterns.

## Maintenance

When an opinion file changes, ask AI to regenerate its row in the table above. AI will read the detail file and extract updated triggers and summary.
