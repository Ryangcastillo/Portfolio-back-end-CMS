#!/usr/bin/env python3
"""
Learning documentation automation scripts for Stitch CMS development.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Optional
import argparse


def get_learning_docs_path():
    """Get the path to learning documentation."""
    return os.path.join(os.getcwd(), "docs", "learning")


def ensure_learning_docs_exist():
    """Ensure learning documentation directory exists."""
    path = get_learning_docs_path()
    os.makedirs(path, exist_ok=True)
    return path


def add_daily_log_entry(focus: str, hours: Optional[float] = None):
    """Add a daily learning log entry."""
    learning_log_path = os.path.join(get_learning_docs_path(), "LEARNING_LOG.md")
    
    if not os.path.exists(learning_log_path):
        print(f"❌ Learning log not found at {learning_log_path}")
        return False
    
    today = datetime.now()
    day_entry = f"""
### {today.strftime('%Y-%m-%d')} - Day {today.timetuple().tm_yday}
**Focus**: {focus}
**Time Spent**: {hours or 'TBD'} hours

**Learned**:
- [Key concept or skill learned today]
- [Important insight gained]

**Built**:
- [Code written or feature implemented]
- [Configuration or setup completed]

**Struggled With**:
- [Challenge faced today]
- [Confusion or error encountered]

**Solution**:
- [How challenge was resolved]
- [Resources that helped]

**Tomorrow's Focus**:
- [Next learning priority]

---
"""
    
    # Read current content
    with open(learning_log_path, 'r') as f:
        content = f.read()
    
    # Find insertion point (after "## 🔄 Process Reflections")
    insertion_point = content.find("## 🔄 Process Reflections")
    if insertion_point == -1:
        # Fallback: add at end
        content += day_entry
    else:
        content = content[:insertion_point] + day_entry + content[insertion_point:]
    
    # Write updated content
    with open(learning_log_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Added daily log entry for {today.strftime('%Y-%m-%d')}")
    print(f"📝 Focus: {focus}")
    if hours:
        print(f"⏱️  Hours: {hours}")
    return True


def add_mistake_entry(title: str, category: str, severity: str = "Medium"):
    """Add a new mistake entry."""
    mistakes_log_path = os.path.join(get_learning_docs_path(), "MISTAKES_LOG.md")
    
    if not os.path.exists(mistakes_log_path):
        print(f"❌ Mistakes log not found at {mistakes_log_path}")
        return False
    
    today = datetime.now()
    
    # Read current content to get next mistake number
    with open(mistakes_log_path, 'r') as f:
        content = f.read()
    
    # Find highest mistake number (simple approach)
    mistake_count = content.count("### MISTAKE-") + 1
    
    mistake_entry = f"""
### MISTAKE-{mistake_count:03d}: {title}
**Date**: {today.strftime('%Y-%m-%d')}
**Category**: {category}
**Severity**: {severity}
**Context**: [What you were trying to accomplish]

**The Mistake**:
[Detailed description of what went wrong]

**Impact**:
[How this affected your work]

**Root Cause**:
[Why this mistake happened]

**Solution**:
[Step-by-step fix]

**Prevention Strategy**:
[How to avoid this in the future]

**Related References**:
- CONST-P# (if applicable)
- TASK-### (if applicable)
- Documentation links

**Status**: [Resolved/Learning/Monitoring]

---
"""
    
    # Find insertion point (after "## 🔍 Detailed Mistake Entries")
    insertion_point = content.find("### Template for New Mistakes")
    if insertion_point == -1:
        content += mistake_entry
    else:
        content = content[:insertion_point] + mistake_entry + content[insertion_point:]
    
    # Write updated content
    with open(mistakes_log_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Added mistake entry MISTAKE-{mistake_count:03d}: {title}")
    print(f"📂 Category: {category}")
    print(f"⚠️  Severity: {severity}")
    print(f"📝 Please edit {mistakes_log_path} to complete the details")
    return True


def add_pattern_entry(name: str, category: str, status: str = "Learning"):
    """Add a new pattern to the pattern library."""
    pattern_lib_path = os.path.join(get_learning_docs_path(), "PATTERN_LIBRARY.md")
    
    if not os.path.exists(pattern_lib_path):
        print(f"❌ Pattern library not found at {pattern_lib_path}")
        return False
    
    today = datetime.now()
    
    # Read current content to get next pattern number
    with open(pattern_lib_path, 'r') as f:
        content = f.read()
    
    # Find highest pattern number
    pattern_count = content.count("### PATTERN-") + 1
    
    pattern_entry = f"""
### PATTERN-{pattern_count:03d}: {name}
**Status**: {status}
**Category**: {category}
**Confidence**: Beginner
**Last Used**: {today.strftime('%Y-%m-%d')}

**Problem Solved**:
[What issue does this pattern address?]

**Implementation**:
```typescript
// Code example showing the pattern
```

**When to Use**:
[Scenarios where this pattern is appropriate]

**When NOT to Use**:
[Anti-patterns or inappropriate scenarios]

**Benefits**:
- [Advantage 1]
- [Advantage 2]

**Drawbacks**:
- [Limitation 1]
- [Limitation 2]

**Common Mistakes**:
- [Mistake 1 and how to avoid]
- [Mistake 2 and how to avoid]

**Variations**:
- [Alternative approach 1]
- [Alternative approach 2]

**Related Patterns**:
- [Pattern that works well with this one]
- [Pattern that might conflict]

**Resources**:
- [Link to documentation]
- [Tutorial or example]

---
"""
    
    # Find insertion point (after existing patterns)
    insertion_point = content.find("## 📝 Code Snippets Library")
    if insertion_point == -1:
        content += pattern_entry
    else:
        content = content[:insertion_point] + pattern_entry + content[insertion_point:]
    
    # Write updated content
    with open(pattern_lib_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Added pattern PATTERN-{pattern_count:03d}: {name}")
    print(f"📂 Category: {category}")
    print(f"📊 Status: {status}")
    print(f"📝 Please edit {pattern_lib_path} to complete the implementation details")
    return True


def create_weekly_retrospective():
    """Create a weekly retrospective template."""
    retro_path = os.path.join(get_learning_docs_path(), "RETROSPECTIVES.md")
    
    if not os.path.exists(retro_path):
        print(f"❌ Retrospectives document not found at {retro_path}")
        return False
    
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    retro_entry = f"""
## Weekly Retrospective: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}

#### 🎯 Goals vs. Outcomes
**This Week's Goals**:
- [ ] [Goal 1] - [Status: Complete/Partial/Not Started]
- [ ] [Goal 2] - [Status: Complete/Partial/Not Started]
- [ ] [Goal 3] - [Status: Complete/Partial/Not Started]

**Completion Rate**: [X]% ([X] of [Y] goals completed)

#### 🚀 What Went Well (Keep Doing)
- [Specific success or positive outcome]
- [Process or tool that worked effectively]
- [Learning breakthrough or insight gained]

#### 🔧 What Could Be Improved (Start Doing)
- [Process bottleneck or inefficiency identified]
- [Skill gap or knowledge area needing focus]
- [Tool or practice to try next week]

#### 🛑 What Didn't Work (Stop Doing)
- [Practice or approach that hindered progress]
- [Time waster or distraction to eliminate]
- [Tool or process that created friction]

#### 📚 Learning Highlights
- **New Skills/Knowledge**: [What you learned this week]
- **Mistakes Made**: [Reference to MISTAKES_LOG entries]
- **Patterns Discovered**: [Reference to PATTERN_LIBRARY additions]

#### ⏱️ Time Allocation Analysis
| Activity | Planned Hours | Actual Hours | Variance | Notes |
|----------|---------------|--------------|----------|-------|
| Planning | X | X | +/- X | [Observation] |
| Coding | X | X | +/- X | [Observation] |
| Learning | X | X | +/- X | [Observation] |
| Documentation | X | X | +/- X | [Observation] |
| Debugging | X | X | +/- X | [Observation] |

#### 🎯 Next Week's Focus
- **Priority 1**: [Main goal for next week]
- **Priority 2**: [Secondary goal]  
- **Priority 3**: [Tertiary goal]
- **Learning Target**: [Specific skill to focus on]

#### 📊 Metrics Tracking
- **Commits**: [Number] ([+/-] vs. last week)
- **Lines of Code**: [Number] ([+/-] vs. last week)
- **Documentation Pages**: [Number] ([+/-] vs. last week)
- **Tests Written**: [Number] ([+/-] vs. last week)

---
"""
    
    # Find insertion point (after template)
    with open(retro_path, 'r') as f:
        content = f.read()
    
    insertion_point = content.find("## 📅 Monthly Retrospective Template")
    if insertion_point == -1:
        content += retro_entry
    else:
        content = content[:insertion_point] + retro_entry + content[insertion_point:]
    
    # Write updated content
    with open(retro_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created weekly retrospective for {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
    print(f"📝 Please complete the retrospective in {retro_path}")
    return True


def show_learning_status():
    """Show current learning status and quick stats."""
    learning_path = get_learning_docs_path()
    
    print("📚 Learning Documentation Status")
    print("=" * 40)
    
    # Check which documents exist
    docs = [
        ("Learning Log", "LEARNING_LOG.md"),
        ("Mistakes Log", "MISTAKES_LOG.md"), 
        ("Pattern Library", "PATTERN_LIBRARY.md"),
        ("Retrospectives", "RETROSPECTIVES.md")
    ]
    
    for name, filename in docs:
        path = os.path.join(learning_path, filename)
        if os.path.exists(path):
            # Get basic stats
            with open(path, 'r') as f:
                content = f.read()
                lines = len(content.split('\n'))
                words = len(content.split())
            print(f"✅ {name}: {lines} lines, {words} words")
        else:
            print(f"❌ {name}: Not found")
    
    print("\n🎯 Quick Actions Available:")
    print("- python scripts/learning_tools.py daily-log 'Your focus today'")
    print("- python scripts/learning_tools.py add-mistake 'Title' 'Category'")
    print("- python scripts/learning_tools.py add-pattern 'Pattern Name' 'Category'")
    print("- python scripts/learning_tools.py weekly-retro")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Learning documentation automation tools")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Daily log command
    daily_parser = subparsers.add_parser('daily-log', help='Add daily learning entry')
    daily_parser.add_argument('focus', help='Main focus for the day')
    daily_parser.add_argument('--hours', type=float, help='Hours spent learning')
    
    # Mistake command
    mistake_parser = subparsers.add_parser('add-mistake', help='Add mistake entry')
    mistake_parser.add_argument('title', help='Brief mistake description')
    mistake_parser.add_argument('category', help='Mistake category')
    mistake_parser.add_argument('--severity', default='Medium', help='Severity level')
    
    # Pattern command
    pattern_parser = subparsers.add_parser('add-pattern', help='Add pattern entry')
    pattern_parser.add_argument('name', help='Pattern name')
    pattern_parser.add_argument('category', help='Pattern category')
    pattern_parser.add_argument('--status', default='Learning', help='Pattern status')
    
    # Retrospective command
    subparsers.add_parser('weekly-retro', help='Create weekly retrospective')
    
    # Status command
    subparsers.add_parser('status', help='Show learning documentation status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Ensure learning docs directory exists
    ensure_learning_docs_exist()
    
    # Execute commands
    if args.command == 'daily-log':
        add_daily_log_entry(args.focus, args.hours)
    elif args.command == 'add-mistake':
        add_mistake_entry(args.title, args.category, args.severity)
    elif args.command == 'add-pattern':
        add_pattern_entry(args.name, args.category, args.status)
    elif args.command == 'weekly-retro':
        create_weekly_retrospective()
    elif args.command == 'status':
        show_learning_status()


if __name__ == "__main__":
    main()