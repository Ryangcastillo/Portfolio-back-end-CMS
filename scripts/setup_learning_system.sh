#!/bin/bash
# Learning System Setup for Stitch CMS

echo "🎓 Setting up Learning System for Stitch CMS"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LEARNING_DIR="$PROJECT_ROOT/docs/learning"

echo -e "${BLUE}📂 Project Root: $PROJECT_ROOT${NC}"
echo -e "${BLUE}📚 Learning Docs: $LEARNING_DIR${NC}"

# Check if learning documents exist
echo ""
echo "🔍 Checking learning documentation..."

docs_exist=true
required_docs=(
    "LEARNING_LOG.md"
    "MISTAKES_LOG.md"
    "PATTERN_LIBRARY.md"
    "RETROSPECTIVES.md"
)

for doc in "${required_docs[@]}"; do
    if [[ -f "$LEARNING_DIR/$doc" ]]; then
        echo -e "${GREEN}✅ $doc exists${NC}"
    else
        echo -e "${RED}❌ $doc missing${NC}"
        docs_exist=false
    fi
done

if [[ "$docs_exist" = false ]]; then
    echo -e "${RED}❌ Some learning documents are missing. Please ensure all learning docs are created.${NC}"
    exit 1
fi

# Check if Python is available
echo ""
echo "🐍 Checking Python environment..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $python_version${NC}"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.${NC}"
    exit 1
fi

# Test the learning tools script
echo ""
echo "🧪 Testing learning tools..."
if python3 "$SCRIPT_DIR/learning_tools.py" status &> /dev/null; then
    echo -e "${GREEN}✅ Learning tools script working${NC}"
else
    echo -e "${RED}❌ Learning tools script has issues${NC}"
    exit 1
fi

# Add to shell profile
echo ""
echo "⚙️  Setting up shell shortcuts..."

SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
else
    echo -e "${YELLOW}⚠️  Unknown shell: $SHELL${NC}"
    echo "Please manually add the following line to your shell profile:"
    echo "source $SCRIPT_DIR/learning_shortcuts.sh"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    SOURCE_LINE="source $SCRIPT_DIR/learning_shortcuts.sh"
    
    if grep -q "$SOURCE_LINE" "$SHELL_PROFILE" 2>/dev/null; then
        echo -e "${GREEN}✅ Learning shortcuts already in $SHELL_PROFILE${NC}"
    else
        echo -e "${BLUE}📝 Adding learning shortcuts to $SHELL_PROFILE${NC}"
        echo "" >> "$SHELL_PROFILE"
        echo "# Stitch CMS Learning Tools" >> "$SHELL_PROFILE"
        echo "$SOURCE_LINE" >> "$SHELL_PROFILE"
        echo -e "${GREEN}✅ Learning shortcuts added to $SHELL_PROFILE${NC}"
        echo -e "${YELLOW}⚠️  Please run 'source $SHELL_PROFILE' or restart your terminal to use shortcuts${NC}"
    fi
fi

# Create VS Code workspace settings
echo ""
echo "💻 Setting up VS Code integration..."

VSCODE_DIR="$PROJECT_ROOT/.vscode"
SETTINGS_FILE="$VSCODE_DIR/settings.json"

mkdir -p "$VSCODE_DIR"

# Create or update settings.json
if [[ -f "$SETTINGS_FILE" ]]; then
    echo -e "${GREEN}✅ VS Code settings already exist${NC}"
else
    echo -e "${BLUE}📝 Creating VS Code settings...${NC}"
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "files.associations": {
    "LEARNING_LOG.md": "markdown",
    "MISTAKES_LOG.md": "markdown",
    "PATTERN_LIBRARY.md": "markdown",
    "RETROSPECTIVES.md": "markdown"
  },
  "markdown.preview.scrollEditorWithPreview": true,
  "markdown.preview.scrollPreviewWithEditor": true,
  "workbench.quickOpen.includeSymbols": true,
  "search.exclude": {
    "**/node_modules": true,
    "**/.git": true,
    "**/dist": true,
    "**/build": true
  },
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true,
    "**/dist/**": true,
    "**/build/**": true
  }
}
EOF
    echo -e "${GREEN}✅ VS Code settings created${NC}"
fi

# Create launch configuration for debugging
LAUNCH_FILE="$VSCODE_DIR/launch.json"
if [[ ! -f "$LAUNCH_FILE" ]]; then
    echo -e "${BLUE}📝 Creating VS Code debug configuration...${NC}"
    cat > "$LAUNCH_FILE" << 'EOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Learning Tools",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/learning_tools.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "args": ["status"]
    }
  ]
}
EOF
    echo -e "${GREEN}✅ VS Code debug configuration created${NC}"
fi

# Test the setup
echo ""
echo "🧪 Testing complete setup..."

# Source the shortcuts in current session
source "$SCRIPT_DIR/learning_shortcuts.sh" 2>/dev/null

echo -e "${GREEN}✅ Learning system setup complete!${NC}"

echo ""
echo "🎯 Quick Start Guide:"
echo "===================="
echo ""
echo -e "${BLUE}1. Start a learning session:${NC}"
echo "   learn-session 'Today I will learn about React components'"
echo ""
echo -e "${BLUE}2. Document progress throughout the day:${NC}"
echo "   learn-mistake 'Forgot to export component' 'Code Quality'"
echo "   learn-pattern 'React Function Component' 'Frontend'"
echo ""
echo -e "${BLUE}3. Commit work with traceability:${NC}"
echo "   learn-commit 'feat: add login component' TASK-001"
echo ""
echo -e "${BLUE}4. End of day wrap-up:${NC}"
echo "   learn-wrap"
echo ""
echo -e "${BLUE}5. Weekly review:${NC}"
echo "   learn-weekly"
echo ""
echo -e "${YELLOW}💡 Type 'learn-help' for all available commands${NC}"
echo ""
echo -e "${GREEN}Happy learning! 🚀${NC}"

# Final check
echo ""
echo "📊 Final system check:"
python3 "$SCRIPT_DIR/learning_tools.py" status