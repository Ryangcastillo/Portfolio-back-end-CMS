# Headless CMS Dependency Management Guide

## 🎯 Overview

This guide covers comprehensive dependency management for the Stitch Headless CMS, ensuring consistent environments, security, and up-to-date packages across backend and frontend modules.

## 🏗️ Architecture

### Backend Dependencies (Python)
- **Location**: `/backend/`
- **Tools**: pip-tools, uv, virtual environments
- **Files**: `requirements.in`, `requirements-dev.in`, compiled `.txt` files

### Frontend Dependencies (Node.js)
- **Admin Interface**: Root `package.json` (Next.js)
- **Frontend Modules**: `/Frontend/package.json` (React modules)
- **Tools**: npm, pnpm, audit tools

## 🚀 Quick Start

### Initial Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/Ryangcastillo/CMS.git
cd CMS

# 2. Backend setup
cd backend
python3 -m venv venv --upgrade-deps
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# 3. Install dependency management tools
pip install --upgrade pip pip-tools uv

# 4. Compile and install dependencies
pip-compile requirements.in
pip-compile requirements-dev.in
pip-sync requirements.txt
pip install -r requirements-dev.txt  # For development

# 5. Frontend setup (Admin Interface)
cd ..
npm install  # or pnpm install

# 6. Frontend modules setup
cd Frontend
npm install
```

## 🔧 Automated Management

The system includes comprehensive automation tools:

### Management Scripts
- `./scripts/manage-dependencies.sh` - Main dependency management
- `./scripts/automate-dependencies.sh` - Automated updates with safety checks
- `./scripts/test-dependency-system.sh` - Comprehensive test suite

### Usage Examples
```bash
# Update all dependencies
./scripts/manage-dependencies.sh all

# Update only backend
./scripts/manage-dependencies.sh backend

# Security audit only
./scripts/manage-dependencies.sh security

# Run automated system
./scripts/automate-dependencies.sh

# Test the system
./scripts/test-dependency-system.sh
```

### Features
- ✅ Automated dependency updates
- ✅ Security vulnerability scanning
- ✅ Rollback on failure
- ✅ Comprehensive reporting
- ✅ GitHub Actions integration
- ✅ Configuration management

## 🔧 Daily Operations

### Using the Management Script

```bash
# Update all dependencies
./scripts/manage-dependencies.sh all

# Update only backend
./scripts/manage-dependencies.sh backend

# Update only frontend
./scripts/manage-dependencies.sh frontend

# Development mode (includes dev tools)
./scripts/manage-dependencies.sh dev

# Security audit only
./scripts/manage-dependencies.sh security

# Generate dependency reports
./scripts/manage-dependencies.sh reports
```

### Manual Operations

#### Backend (Python)

```bash
cd backend
source venv/bin/activate

# Check current environment
pip --version
python --version

# Update pip-tools
pip install --upgrade pip pip-tools uv

# Compile requirements (update dependencies)
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in

# Sync environment (install/remove to match requirements)
pip-sync requirements.txt

# Check for outdated packages
pip list --outdated

# Security audit
bandit -r . -f json
safety check
```

#### Frontend (Node.js)

```bash
# Admin Interface (Next.js)
npm update
npm audit fix
npm outdated

# Or with pnpm
pnpm update
pnpm audit --fix
pnpm outdated

# Frontend Modules (React)
cd Frontend
npm update
npm audit fix
npm outdated
```

## 📋 File Structure

```
CMS/
├── backend/
│   ├── requirements.in          # Main dependencies (human-readable)
│   ├── requirements.txt         # Compiled/locked dependencies
│   ├── requirements-dev.in      # Dev dependencies (human-readable)
│   ├── requirements-dev.txt     # Compiled dev dependencies
│   └── venv/                    # Virtual environment
├── package.json                 # Admin Interface dependencies
├── Frontend/
│   └── package.json             # React module dependencies
├── scripts/
│   └── manage-dependencies.sh   # Automated management script
└── reports/                     # Generated dependency reports
    ├── python-dependencies.json
    ├── python-outdated.json
    ├── nodejs-dependencies.json
    └── nodejs-outdated.json
```

## 🔒 Security Management

### Automated Security Audits

```bash
# Python security scanning
cd backend
source venv/bin/activate
bandit -r . -ll  # High/medium severity only
safety check     # Known vulnerabilities

# Node.js security scanning
npm audit
npm audit fix    # Auto-fix if possible

# Generate security reports
./scripts/manage-dependencies.sh security
```

### Manual Security Reviews

1. **Review dependency updates**: Check changelogs for breaking changes
2. **Verify sources**: Ensure packages come from trusted repositories
3. **Monitor advisories**: Subscribe to security advisories for used packages
4. **Regular audits**: Run security scans weekly

## 🤖 Automated Management

### GitHub Actions Integration

The repository includes automated dependency management via GitHub Actions:

- **Weekly Updates**: Automatically checks for and creates PRs with dependency updates
- **Security Scanning**: Runs on every push and PR
- **Multi-version Testing**: Tests against multiple Python and Node.js versions
- **Automated Reports**: Generates and uploads dependency reports

### Dependabot Configuration

Add to `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
    reviewers:
      - "Ryangcastillo"
    
  # Node.js dependencies (Admin Interface)
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "Ryangcastillo"
      
  # Node.js dependencies (Frontend Modules)
  - package-ecosystem: "npm"
    directory: "/Frontend"
    schedule:
      interval: "weekly"
    reviewers:
      - "Ryangcastillo"
```

## 🧪 Testing Dependencies

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Install test dependencies
pip install -r requirements-dev.txt

# Run tests with current dependencies
pytest

# Test against specific Python versions
tox  # If using tox for multi-version testing
```

### Frontend Testing

```bash
# Admin Interface tests
npm test
npm run build  # Ensure build works

# Frontend Module tests
cd Frontend
npm test
npm run build
```

## 🔄 Version Control Integration

### Pre-commit Hooks

Install pre-commit hooks to check dependencies:

```bash
cd backend
source venv/bin/activate
pip install pre-commit
pre-commit install

# Manual run
pre-commit run --all-files
```

### Git Hooks for Requirements

Add to `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Check if requirements.txt is up to date with requirements.in

cd backend
if [ requirements.in -nt requirements.txt ]; then
    echo "❌ requirements.txt is older than requirements.in"
    echo "Run: pip-compile requirements.in"
    exit 1
fi
```

## 🚨 Troubleshooting

### Common Issues

#### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf backend/venv
cd backend
python3 -m venv venv --upgrade-deps
source venv/bin/activate
pip install -r requirements.txt
```

#### Dependency Conflicts

```bash
# Use pip-tools to resolve conflicts
cd backend
source venv/bin/activate
pip-compile --resolver=backtracking requirements.in
```

#### Node.js Cache Issues

```bash
# Clear npm cache
npm cache clean --force

# Clear pnpm cache
pnpm store prune

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Emergency Recovery

```bash
# Full environment reset
./scripts/manage-dependencies.sh all

# Or manual reset:
cd backend
rm -rf venv
python3 -m venv venv --upgrade-deps
source venv/bin/activate
pip install --upgrade pip pip-tools
pip-compile requirements.in
pip-sync requirements.txt

cd ..
rm -rf node_modules package-lock.json
npm install

cd Frontend
rm -rf node_modules package-lock.json  
npm install
```

## 📊 Monitoring & Reporting

### Weekly Maintenance Routine

1. **Run full dependency check**: `./scripts/manage-dependencies.sh all`
2. **Review security reports**: Check `reports/` directory
3. **Update documentation**: If new dependencies added
4. **Test system**: Run full test suite
5. **Monitor performance**: Check if updates affect performance

### Dependency Reports

The management script generates comprehensive reports:

- **Python dependencies**: Current versions, outdated packages
- **Node.js dependencies**: Package trees, vulnerability reports
- **Security audits**: Known vulnerabilities, recommendations
- **Update logs**: What was changed in last update

## 🎯 Best Practices

### General Guidelines

1. **Pin major versions**: Use `package>=1.0.0,<2.0.0` for stability
2. **Regular updates**: Weekly dependency checks
3. **Test thoroughly**: Always test after updates
4. **Document changes**: Note breaking changes in updates
5. **Security first**: Prioritize security updates

### Backend (Python)

1. **Use requirements.in**: Human-readable dependency specifications
2. **Compile to requirements.txt**: Locked, reproducible installs
3. **Separate dev dependencies**: Keep development tools separate
4. **Virtual environments**: Always use isolated environments
5. **Pin Python version**: Specify Python version in runtime

### Frontend (Node.js)

1. **Lock file versioning**: Commit `package-lock.json` and `pnpm-lock.yaml`
2. **Audit regularly**: Run `npm audit` weekly
3. **Update gradually**: Update dependencies in small batches
4. **Test across environments**: Ensure compatibility across dev/prod
5. **Monitor bundle size**: Watch for bundle size increases

## 🔗 Integration with Headless CMS

### API Compatibility

- **Backend updates**: Ensure API contract stability
- **Frontend updates**: Test all frontend modules after updates
- **Database migrations**: Check if ORM updates require migrations
- **Authentication**: Verify auth system after security updates

### Multi-Frontend Considerations

- **Shared dependencies**: Keep common dependencies in sync
- **Version compatibility**: Ensure all frontend modules work with API
- **Independent deployments**: Each module can have different update cycles
- **Fallback strategies**: Ensure frontend modules degrade gracefully

---

## 📞 Support

For dependency management issues:

1. **Check logs**: Review output from management script
2. **Security alerts**: Monitor GitHub security advisories
3. **Community**: Check package documentation and community forums
4. **Recovery**: Use emergency recovery procedures if needed

**Last Updated**: 2025-09-20  
**Version**: 1.0.0  
**Compatibility**: Python 3.9+, Node.js 18+