# Code Domain Opinions

When `praxis.yaml` has `domain: code`, load this file into context.

## Available Opinions

| Opinion | Triggers | Summary |
|---------|----------|---------|
| [cli](cli.md) | CLI, command-line, terminal, Unix, GNU, coreutils, HashiCorp, Docker, AWS CLI, shell, pipeline, stdout, stderr, exit codes, automation, scripting, CI/CD, backwards compatibility, long-term maintenance | Production CLI: Unix philosophy, pipeline safety, explicit behavior, meaningful exit codes, 10-year maintainability |
| [cli-python](cli-python.md) | Python, Poetry, Typer, pytest, pytest-bdd, BDD, TDD, hexagonal, ports and adapters, ruff, mypy, pyproject.toml, console script | Python CLI: hexagonal architecture, Poetry, Typer, BDD/TDD testing, ruff/mypy |
| [gui](gui.md) | GUI, graphical, desktop, web app, UI, UX, interface, window, dialog, button, form, accessibility, responsive | GUI apps: responsive, accessible, clear feedback, forgiving interactions |
| [gui-web](gui-web.md) | web, browser, HTML, CSS, JavaScript, TypeScript, React, Vue, Angular, Svelte, frontend, SPA, PWA, responsive, mobile-first, WCAG, ARIA, CSP | Web GUI: performance, cross-browser, security, accessibility, component-based |

## How This Works

1. This README is loaded when domain = code
2. If conversation matches any **trigger** keywords, load **all** matching detail files
3. If a file extends another (e.g., `cli-python` extends `cli`), load the base file too
4. Apply all loaded opinions to your reasoning and suggestions

Multiple opinions can apply simultaneously. Base opinions provide general best practices; extended opinions add specific tooling and patterns.

## Maintenance

When an opinion file changes, ask AI to regenerate its row in the table above. AI will read the detail file and extract updated triggers and summary.
