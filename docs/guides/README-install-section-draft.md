# README Installation Section - Future Version (Post-PyPI)

This is a draft of how the installation section of README.md should look once Praxis is published to PyPI.

---

## Quick Start

### 1. Install

```bash
# Recommended: Install with pipx (isolated)
pipx install praxis-ai

# Alternative: Install with pip
pip install praxis-ai

# Verify
praxis --version
```

### 2. Configure shell

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export PRAXIS_HOME="$HOME/praxis-workspace"
```

### 3. Initialize workspace

```bash
praxis workspace init
# Creates: extensions/, examples/, projects/, workspace-config.yaml
```

### 4. Create a project

```bash
praxis new my-project --domain code --privacy personal
# Creates: $PRAXIS_HOME/projects/code/my-project/
```

### 5. Work through the lifecycle

```bash
cd $PRAXIS_HOME/projects/code/my-project

# Check status and get guided next steps
praxis status
# Output includes:
#   Next Steps:
#     + Create docs/capture.md (Capture document)
#     ▶ Run `praxis stage sense` (Advance to Sense stage)
#
#   Legend: + create  ~ edit  ▶ run  ? review  ! fix

# Move through stages
praxis stage sense
praxis stage explore
praxis stage shape
praxis stage formalize  # Creates docs/sod.md template

# Validate before execution
praxis validate --strict
praxis stage commit
praxis stage execute
```

---

## Installation

### Recommended: pipx (Isolated)

```bash
# Install pipx if you don't have it
pip install --user pipx
pipx ensurepath

# Install Praxis
pipx install praxis-ai
```

### Alternative: pip (Global)

```bash
pip install praxis-ai
```

### Development Install

To contribute or use the latest features:

```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
poetry install
poetry run praxis --version
```

See [Installation Guide](docs/guides/installation.md) for detailed instructions, troubleshooting, and platform-specific notes.

---

## Verify Installation

```bash
# Check health of your installation
praxis doctor

# Expected output:
# Praxis Health Check
#
#   ✓ Python version            3.12.3
#   ✓ PRAXIS_HOME               /home/user/praxis-workspace
#   ✓ Workspace                 Configured
#   ✓ Praxis version            0.1.0
#
# ✓ All checks passed
```

---

## Configuration

### Set PRAXIS_HOME

Add to your shell configuration (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PRAXIS_HOME="$HOME/praxis-workspace"
```

Reload your shell:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Initialize Workspace

```bash
praxis workspace init
```

This creates the following structure:

```
$PRAXIS_HOME/
├── extensions/              # Installed extensions
├── examples/                # Installed examples
├── projects/                # Your projects (by domain)
│   ├── code/
│   ├── create/
│   ├── write/
│   ├── learn/
│   └── observe/
└── workspace-config.yaml    # Workspace configuration
```

### Enable Tab Completion (Optional)

```bash
praxis --install-completion
```

Restart your shell to use tab completion.

---

## Next Steps

After installation:

1. **Read the User Guide:** [docs/guides/user-guide.md](docs/guides/user-guide.md)
2. **Create your first project:** `praxis new my-project`
3. **Explore examples:** `praxis examples list`
4. **Configure AI assistant:** [docs/guides/ai-setup.md](docs/guides/ai-setup.md)
5. **Learn the lifecycle:** `praxis guide lifecycle`

---

## Help & Troubleshooting

```bash
# Show all commands
praxis --help

# Show command-specific help
praxis <command> --help

# Check installation health
praxis doctor

# Show workspace info
praxis workspace info
```

For detailed troubleshooting, see the [Installation Guide](docs/guides/installation.md).

---

## Updating Praxis

```bash
# With pipx
pipx upgrade praxis-ai

# With pip
pip install --upgrade praxis-ai
```

---

## Uninstalling

```bash
# With pipx
pipx uninstall praxis-ai

# With pip
pip uninstall praxis-ai

# Optional: Remove workspace (WARNING: deletes your projects!)
rm -rf $PRAXIS_HOME
```

---

## Platform Support

- **macOS:** ✅ Supported
- **Linux:** ✅ Supported  
- **Windows (WSL):** ✅ Supported
- **Docker:** ✅ Container available

See [Installation Guide](docs/guides/installation.md) for platform-specific instructions.

---

## Requirements

- Python 3.10 or higher
- pip or pipx

---

## Getting Help

- **Documentation:** [docs/guides/](docs/guides/)
- **Issues:** [GitHub Issues](https://github.com/jayers99/praxis-ai/issues)
- **Check health:** `praxis doctor`
- **In-terminal guides:** `praxis guide lifecycle|privacy|domain`
