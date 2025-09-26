
from pathlib import Path
from invoke import task


@task
def setup(c):
    """Setup dev environment: apt-get, npm, Claude, poetry, etc."""
    print("🔧 Setting up dev environment (apt-get, npm, Claude, poetry)...")

    # Ensure apt directories exist with correct permissions
    print("🔧 Ensuring apt directories exist...")
    c.run("sudo mkdir -p /var/lib/apt/lists/partial", warn=True, hide=True)
    c.run("sudo chown -R _apt:root /var/lib/apt/lists/partial", warn=True, hide=True)

    # Update apt packages
    print("📦 Updating package lists...")
    c.run("sudo apt-get update", pty=True)

    # Check if Claude Code is already installed
    result = c.run("source /usr/local/share/nvm/nvm.sh && which claude",
                   warn=True, hide=True, shell='/bin/bash')
    if result.ok:
        print("✅ Claude Code is already installed")
    else:
        # Install Claude Code globally - source NVM first to get npm in PATH
        print("📦 Installing Claude Code...")
        c.run("source /usr/local/share/nvm/nvm.sh && npm install -g @anthropic-ai/claude-code",
              pty=True, shell='/bin/bash')

    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    c.run("poetry install", pty=True)

    print("✅ Dev environment setup complete.")


@task
def install(c):
    """Install project dependencies using poetry."""
    print("📦 Installing dependencies...")
    c.run("poetry install", pty=True)


@task
def lint(c):
    """Run ruff linter on the codebase."""
    print("🔍 Running ruff linter...")
    c.run("poetry run ruff check ib_insync tests", warn=True)


@task
def typecheck(c):
    """Run mypy type checker on the codebase."""
    print("🔍 Running mypy type checker...")
    c.run("poetry run mypy -p ib_insync", warn=True)


@task
def test(c):
    """Run pytest tests."""
    print("🧪 Running tests...")
    c.run("poetry run pytest", warn=True)


@task
def format(c):
    """Format code using ruff."""
    print("🎨 Formatting code with ruff...")
    c.run("poetry run ruff format ib_insync tests", warn=True)


@task
def check(c):
    """Run all checks: lint, typecheck, and tests."""
    print("📋 Running all checks...")
    lint(c)
    typecheck(c)
    test(c)
    print("✅ All checks passed!")


@task
def ci(c):
    """Run comprehensive CI checks: install, lint, typecheck, and test."""
    print("🚀 Running CI pipeline...")

    # Install dependencies first
    print("📦 Installing dependencies...")
    c.run("poetry install", pty=True)

    # Run all checks
    lint(c)
    typecheck(c)
    test(c)

    print("✅ CI pipeline complete!")
