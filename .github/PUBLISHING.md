# Publishing FAPI to PyPI

This document explains how to publish the FAPI package to PyPI using GitHub Actions.

## Overview

The repository is configured with automated PyPI publishing via GitHub Actions. The workflow can be triggered in two ways:

1. **Automatically**: When you create a GitHub Release
2. **Manually**: Via the GitHub Actions UI

## Prerequisites

Before publishing, you need to configure PyPI authentication. We recommend using **Trusted Publishing** (OIDC) for enhanced security.

### Option 1: Trusted Publishing (Recommended)

Trusted Publishing allows GitHub Actions to publish to PyPI without storing any tokens.

**Setup Steps:**

1. **Create the PyPI Project** (first-time only):
   - Go to https://pypi.org
   - Create a new project named `fapi`
   - Or claim it if you have permissions

2. **Configure Trusted Publisher**:
   - Go to https://pypi.org/manage/project/fapi/settings/publishing/
   - Click "Add a new publisher"
   - Fill in the details:
     - **PyPI Project Name**: `fapi`
     - **Owner**: `darbotlabs`
     - **Repository name**: `fapi`
     - **Workflow name**: `publish.yml`
     - **Environment name**: (leave empty)
   - Click "Add"

3. **Done!** No secrets needed. The workflow will authenticate automatically.

### Option 2: API Token (Alternative)

If Trusted Publishing is not available, use an API token:

1. **Generate PyPI API Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Scope: Entire account (or specific to `fapi` project)
   - Copy the token (starts with `pypi-`)

2. **Add to GitHub Secrets**:
   - Go to https://github.com/darbotlabs/fapi/settings/secrets/actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token
   - Click "Add secret"

3. **Update Workflow** (if needed):
   The workflow already supports both methods. If using tokens, ensure the publish step includes:
   ```yaml
   - name: Publish
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## Publishing Process

### Method 1: Via GitHub Release (Recommended)

This is the standard way to publish new versions:

1. **Update Version**:
   ```bash
   # Update version in fapi/__init__.py
   __version__ = "0.122.0"
   ```

2. **Commit and Push**:
   ```bash
   git add fapi/__init__.py
   git commit -m "Bump version to 0.122.0"
   git push origin master
   ```

3. **Create Release Tag**:
   ```bash
   git tag -a v0.122.0 -m "Release v0.122.0"
   git push origin v0.122.0
   ```

4. **Create GitHub Release**:
   - Go to https://github.com/darbotlabs/fapi/releases/new
   - Choose the tag you just created (`v0.122.0`)
   - Release title: `v0.122.0`
   - Description: Describe the changes
   - Click "Publish release"

5. **Automatic Publishing**:
   - GitHub Actions will automatically trigger
   - Watch progress at: https://github.com/darbotlabs/fapi/actions
   - Packages will be published to PyPI: https://pypi.org/project/fapi/

### Method 2: Manual Trigger

For testing or emergency releases:

1. **Go to Actions Tab**:
   - Visit https://github.com/darbotlabs/fapi/actions/workflows/publish.yml

2. **Run Workflow**:
   - Click "Run workflow"
   - Select branch: `master`
   - Choose package: `fapi` or `fapi-slim`
   - Click "Run workflow"

3. **Monitor Progress**:
   - Watch the workflow execution
   - Check PyPI after completion

## What Gets Published

The workflow publishes two packages:

1. **fapi**: The main package with all features
2. **fapi-slim**: A minimal version without optional dependencies

Both are built from the same source using different build configurations.

## Verification

After publishing, verify the package:

```bash
# Create a clean environment
python -m venv test-env
source test-env/bin/activate

# Install from PyPI
pip install fapi

# Test import
python -c "import fapi; print(fapi.__version__)"

# Test CLI
fapi --version
```

## Troubleshooting

### Workflow Fails: "403 Forbidden"

**Solution**: Check that Trusted Publishing is configured correctly, or verify your API token is valid.

### Package Already Exists

**Error**: "File already exists"

**Solution**: You cannot overwrite existing versions on PyPI. Bump the version number in `fapi/__init__.py` and try again.

### Permission Denied

**Solution**: Ensure you have maintainer permissions on the PyPI project, or that the GitHub repository owner matches the Trusted Publisher configuration.

### Build Fails

**Solution**: Run the build locally first to catch errors:
```bash
pip install build
python -m build
```

## Package Versions

Version numbering follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Current version: `0.121.1`

## Links

- **PyPI Package**: https://pypi.org/project/fapi/
- **GitHub Releases**: https://github.com/darbotlabs/fapi/releases
- **Workflow Runs**: https://github.com/darbotlabs/fapi/actions/workflows/publish.yml
- **PyPI Publishing Settings**: https://pypi.org/manage/project/fapi/settings/publishing/

## Support

For issues with publishing:
1. Check the workflow logs
2. Verify PyPI configuration
3. Open an issue: https://github.com/darbotlabs/fapi/issues
