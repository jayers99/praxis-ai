# Praxis Installation Guide

Complete guide to installing and configuring Praxis for your system.

---

## Quick Install (Future - Once on PyPI)

```bash
# Recommended: Install with pipx (isolated)
pipx install praxis-ai

# Alternative: Install with pip
pip install praxis-ai

# Verify installation
praxis --version
```

---

## Current Installation (Development)

Until Praxis is published to PyPI, install from source:

### Prerequisites

- Python 3.10 or higher
- Git
- Poetry (Python package manager)

### Step 1: Install Poetry

If you don't have Poetry installed:

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Or with pip
pip install poetry
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
```

### Step 3: Install Dependencies

```bash
poetry install
```

### Step 4: Verify Installation

```bash
poetry run praxis --version
```

### Step 5: Create CLI Wrapper (Recommended)

For easier access, create a wrapper script:

```bash
# Create bin directory
mkdir -p ~/bin

# Create wrapper script (adjust path to your clone location)
cat > ~/bin/praxis << 'EOF'
#!/bin/bash
exec poetry -C "$HOME/path/to/praxis-ai" run praxis "$@"
EOF

# Make executable
chmod +x ~/bin/praxis

# Add to PATH if not already there (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/bin:$PATH"
```

Restart your shell or source your config file:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can run `praxis` from anywhere:

```bash
praxis --version
```

---

## Post-Installation Setup

### 1. Configure Workspace

Set the `PRAXIS_HOME` environment variable (where your projects will live):

```bash
# Add to ~/.bashrc or ~/.zshrc
export PRAXIS_HOME="$HOME/praxis-workspace"
```

Restart your shell or source the config file.

### 2. Initialize Workspace

Create the workspace structure:

```bash
praxis workspace init
```

This creates:
- `$PRAXIS_HOME/extensions/` - Installed extensions
- `$PRAXIS_HOME/examples/` - Example projects
- `$PRAXIS_HOME/projects/` - Your projects (organized by domain)
- `$PRAXIS_HOME/workspace-config.yaml` - Workspace configuration

### 3. Enable Shell Completion (Optional)

For tab completion of commands and options:

```bash
praxis --install-completion
```

Restart your shell or source your config file.

---

## Verify Installation

Check that everything is working:

```bash
# Check CLI is accessible
praxis --version

# Check workspace is configured
praxis workspace info

# Create a test project
praxis new test-project --domain code --privacy personal

# Check project status
cd $PRAXIS_HOME/projects/code/test-project
praxis status
```

Expected output:
```
Project: test-project
  Domain:  code
  Stage:   capture (1/9)
  Privacy: personal
  Env:     Home
  
Next Stage: sense
  - Create content in docs/capture.md
  
Artifact: ✗ docs/sod.md
  
Validation: ✓ Valid

Next Steps:
  + Create docs/capture.md (Capture document)
  ▶ Run `praxis stage sense` (Advance to Sense stage)
```

---

## Platform-Specific Notes

### macOS

**Homebrew Python:**
If using Homebrew Python, you may need to:

```bash
# Ensure Python 3.10+ is installed
brew install python@3.12

# Use explicit Python version
python3.12 -m pip install poetry
```

**PATH Configuration:**
Add to `~/.zshrc` (macOS default shell):

```bash
export PATH="$HOME/bin:$PATH"
export PRAXIS_HOME="$HOME/praxis-workspace"
```

### Linux

**System Python:**
Most distributions include Python 3.10+. Verify:

```bash
python3 --version
```

If using an older version, install Python 3.10+ via your package manager:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip

# Fedora
sudo dnf install python3.10
```

**PATH Configuration:**
Add to `~/.bashrc`:

```bash
export PATH="$HOME/bin:$PATH"
export PRAXIS_HOME="$HOME/praxis-workspace"
```

### Windows (WSL)

**Use Windows Subsystem for Linux:**

1. Install WSL2 with Ubuntu
2. Follow Linux installation instructions above
3. Access workspace from Windows at: `\\wsl$\Ubuntu\home\<username>\praxis-workspace`

**PATH Configuration:**
Add to `~/.bashrc`:

```bash
export PATH="$HOME/bin:$PATH"
export PRAXIS_HOME="$HOME/praxis-workspace"
```

### Docker

**Run Praxis in a Container:**

```dockerfile
FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Clone and install Praxis
RUN git clone https://github.com/jayers99/praxis-ai.git /opt/praxis-ai
WORKDIR /opt/praxis-ai
RUN poetry install

# Set up workspace
ENV PRAXIS_HOME=/workspace
RUN mkdir -p /workspace

# Entrypoint
ENTRYPOINT ["poetry", "run", "praxis"]
```

Build and run:

```bash
docker build -t praxis-ai .
docker run -it -v $(pwd):/workspace praxis-ai --help
```

---

## Troubleshooting

### Command not found: praxis

**Problem:** Shell can't find the `praxis` command.

**Solutions:**

1. **Using Poetry directly:**
   ```bash
   poetry run praxis --version
   ```

2. **Check wrapper script:**
   ```bash
   which praxis
   ls -l ~/bin/praxis
   ```

3. **Verify PATH:**
   ```bash
   echo $PATH | grep "$HOME/bin"
   ```

4. **Add to PATH (if missing):**
   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

### PRAXIS_HOME not set

**Problem:** Workspace commands fail with "PRAXIS_HOME not set".

**Solution:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export PRAXIS_HOME="$HOME/praxis-workspace"

# Apply immediately
source ~/.bashrc  # or source ~/.zshrc
```

### Python version too old

**Problem:** `praxis` requires Python 3.10+.

**Solution:**

```bash
# Check current version
python3 --version

# Install newer Python (method varies by platform)
# Ubuntu/Debian:
sudo apt install python3.10

# macOS (Homebrew):
brew install python@3.12

# Use specific Python version with Poetry
poetry env use python3.10
poetry install
```

### Poetry not found

**Problem:** `poetry: command not found`

**Solution:**

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Or with pip
pip install --user poetry

# Add to PATH (location varies)
export PATH="$HOME/.local/bin:$PATH"
```

### Permission denied

**Problem:** Can't create files in workspace or install location.

**Solution:**

```bash
# Fix workspace permissions
mkdir -p $PRAXIS_HOME
chmod u+w $PRAXIS_HOME

# Don't use sudo with Poetry
# Poetry installs to user directory, no sudo needed
```

### Import errors after installation

**Problem:** Python can't find `praxis` module.

**Solution:**

```bash
# Reinstall dependencies
cd /path/to/praxis-ai
poetry install

# Verify environment
poetry env info
poetry show
```

---

## Updating Praxis

### From PyPI (Future)

```bash
# With pipx
pipx upgrade praxis-ai

# With pip
pip install --upgrade praxis-ai
```

### From Source (Current)

```bash
cd /path/to/praxis-ai

# Pull latest changes
git pull origin main

# Update dependencies
poetry install

# Verify update
poetry run praxis --version
```

### Update Extensions

```bash
praxis extensions update
```

---

## Uninstalling

### Remove PyPI Installation (Future)

```bash
# With pipx
pipx uninstall praxis-ai

# With pip
pip uninstall praxis-ai
```

### Remove Source Installation (Current)

```bash
# Remove repository
rm -rf /path/to/praxis-ai

# Remove wrapper script
rm ~/bin/praxis

# Remove workspace (WARNING: deletes your projects)
rm -rf $PRAXIS_HOME

# Remove environment variables from shell config
# Edit ~/.bashrc or ~/.zshrc and remove:
# export PRAXIS_HOME="$HOME/praxis-workspace"
# export PATH="$HOME/bin:$PATH"
```

---

## Environment Variables Reference

| Variable | Purpose | Default |
|----------|---------|---------|
| `PRAXIS_HOME` | Workspace root directory | Not set (required for workspace features) |
| `PATH` | Include `~/bin` for CLI access | System default |

---

## Next Steps

After installation:

1. **Read the User Guide:** [docs/guides/user-guide.md](user-guide.md)
2. **Create your first project:** `praxis new my-project`
3. **Explore examples:** `praxis examples list`
4. **Configure AI assistant:** [docs/guides/ai-setup.md](ai-setup.md)
5. **Learn the lifecycle:** `praxis guide lifecycle`

---

## Getting Help

- **Documentation:** [docs/guides/](.)
- **Issues:** [GitHub Issues](https://github.com/jayers99/praxis-ai/issues)
- **Check health:** `praxis doctor`
- **Show commands:** `praxis --help`
- **Command help:** `praxis <command> --help`

---

## Version History

This guide is for Praxis 0.1.0. Installation process will simplify once published to PyPI.
