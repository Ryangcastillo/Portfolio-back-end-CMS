#!/bin/bash
# Learning Tools Shortcuts for Stitch CMS Development

# Set base directory
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

# Learning tool shortcuts
alias learn-status="python3 $SCRIPTS_DIR/learning_tools.py status"
alias learn-log="python3 $SCRIPTS_DIR/learning_tools.py daily-log"
alias learn-mistake="python3 $SCRIPTS_DIR/learning_tools.py add-mistake"
alias learn-pattern="python3 $SCRIPTS_DIR/learning_tools.py add-pattern"
alias learn-retro="python3 $SCRIPTS_DIR/learning_tools.py weekly-retro"

# Quick navigation
alias goto-learning="cd $PROJECT_ROOT/docs/learning"
alias edit-log="code $PROJECT_ROOT/docs/learning/LEARNING_LOG.md"
alias edit-mistakes="code $PROJECT_ROOT/docs/learning/MISTAKES_LOG.md"
alias edit-patterns="code $PROJECT_ROOT/docs/learning/PATTERN_LIBRARY.md"
alias edit-retros="code $PROJECT_ROOT/docs/learning/RETROSPECTIVES.md"

# Validation shortcuts
alias validate-all="cd $PROJECT_ROOT && python3 scripts/governance/validate_all.py"
alias validate-constitution="cd $PROJECT_ROOT && python3 scripts/governance/validate_constitution.py"

# Git shortcuts with learning integration
learn-commit() {
    if [ -z "$1" ]; then
        echo "Usage: learn-commit 'commit message' [TASK-###]"
        echo "Example: learn-commit 'feat: add user auth' TASK-001"
        return 1
    fi
    
    local message="$1"
    local task_ref="$2"
    
    if [ -n "$task_ref" ]; then
        git commit -m "$message

Refs: $task_ref"
    else
        git commit -m "$message"
    fi
    
    echo "💡 Remember to update your learning log with: learn-log 'what you worked on'"
}

# Quick learning session starter
learn-session() {
    local focus="$1"
    if [ -z "$focus" ]; then
        echo "Usage: learn-session 'session focus'"
        echo "Example: learn-session 'React components'"
        return 1
    fi
    
    echo "🎯 Starting learning session: $focus"
    echo "📝 Adding to learning log..."
    python3 "$SCRIPTS_DIR/learning_tools.py" daily-log "$focus"
    
    echo "📊 Current learning status:"
    python3 "$SCRIPTS_DIR/learning_tools.py" status
    
    echo ""
    echo "🚀 Ready to learn! Remember to:"
    echo "  - Document mistakes: learn-mistake 'title' 'category'"
    echo "  - Capture patterns: learn-pattern 'name' 'category'"  
    echo "  - Commit with references: learn-commit 'message' 'TASK-###'"
}

# End of day learning wrap-up
learn-wrap() {
    echo "📝 End of day learning wrap-up"
    echo "=============================="
    
    echo "📊 Today's learning status:"
    python3 "$SCRIPTS_DIR/learning_tools.py" status
    
    echo ""
    echo "💭 Don't forget to update your daily log entry with:"
    echo "  - What you learned today"
    echo "  - What you built"
    echo "  - What you struggled with"
    echo "  - Solutions you found"
    echo "  - Tomorrow's focus"
    
    echo ""
    echo "📂 Quick edit commands:"
    echo "  edit-log     - Open learning log"
    echo "  edit-mistakes - Open mistakes log"  
    echo "  edit-patterns - Open pattern library"
}

# Weekly learning review
learn-weekly() {
    echo "📅 Weekly learning review"
    echo "========================"
    
    echo "📝 Creating weekly retrospective..."
    python3 "$SCRIPTS_DIR/learning_tools.py" weekly-retro
    
    echo ""
    echo "📊 Current documentation status:"
    python3 "$SCRIPTS_DIR/learning_tools.py" status
    
    echo ""
    echo "🎯 Weekly review tasks:"
    echo "  1. Complete the weekly retrospective"
    echo "  2. Review mistake patterns"
    echo "  3. Update pattern library"
    echo "  4. Plan next week's learning goals"
    echo ""
    echo "📂 Open retrospective with: edit-retros"
}

# Help function
learn-help() {
    echo "🎓 Learning Tools Help"
    echo "====================="
    echo ""
    echo "📝 Daily Learning:"
    echo "  learn-session 'focus'   - Start a learning session"
    echo "  learn-log 'focus'       - Add daily log entry"
    echo "  learn-wrap              - End of day wrap-up"
    echo ""
    echo "📊 Documentation:"
    echo "  learn-mistake 'title' 'category' - Document a mistake"
    echo "  learn-pattern 'name' 'category'  - Add a new pattern"
    echo "  learn-status            - Show documentation status"
    echo ""
    echo "🔄 Reviews:"
    echo "  learn-retro             - Create weekly retrospective"
    echo "  learn-weekly            - Full weekly review process"
    echo ""
    echo "📂 Navigation:"
    echo "  goto-learning           - Go to learning docs folder"
    echo "  edit-log               - Edit learning log"
    echo "  edit-mistakes          - Edit mistakes log"
    echo "  edit-patterns          - Edit pattern library"
    echo "  edit-retros            - Edit retrospectives"
    echo ""
    echo "⚡ Git Integration:"
    echo "  learn-commit 'msg' TASK-### - Commit with task reference"
    echo ""
    echo "🔍 Validation:"
    echo "  validate-all           - Run all governance checks"
    echo "  validate-constitution  - Check constitutional compliance"
}

echo "🎓 Learning tools loaded! Type 'learn-help' for available commands."