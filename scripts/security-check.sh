#!/bin/bash

# Security check script for CMS project
# This script runs security scans on Python dependencies

set -e

echo "🔍 Running security scan for CMS project..."
echo "=============================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📂 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  No virtual environment found. Consider creating one with: python -m venv .venv"
fi

# Check if safety is installed
if ! command -v safety &> /dev/null; then
    echo "📦 Installing safety package..."
    pip install safety
fi

# Run security scan
echo "🔐 Scanning backend dependencies for vulnerabilities..."
safety check -r backend/requirements.txt

echo ""
echo "✅ Security scan completed!"
echo ""
echo "💡 To update packages to latest secure versions:"
echo "   pip install -r backend/requirements.txt --upgrade"
echo ""
echo "📋 Recently fixed vulnerabilities (September 2025):"
echo "   - python-jose: Updated to 3.4.0 (from 3.3.0) - Fixed CVE-2024-33663, CVE-2024-33664"
echo "   - python-multipart: Updated to 0.0.18 (from 0.0.6) - Fixed DoS vulnerability"
echo "   - cryptography: Updated to 44.0.1 (from 42.0.5) - Fixed OpenSSL vulnerabilities"