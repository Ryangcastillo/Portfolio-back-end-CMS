# Learning System Quick Reference

> Essential commands and workflows for your learning journey

## 🚀 Daily Workflow

### Start Your Day
```bash
# Start a focused learning session
learn-session "Today I'm learning React hooks"

# Check your current status
learn-status
```

### During Development
```bash
# Document mistakes as you encounter them
learn-mistake "Forgot useState import" "Code Quality"

# Capture new patterns you discover
learn-pattern "Custom React Hook" "Frontend"

# Commit with proper traceability  
learn-commit "feat: implement user login" TASK-001
```

### End Your Day
```bash
# Wrap up and reflect
learn-wrap

# Quick edit your daily log
edit-log
```

## 📅 Weekly Routine

### Friday Review
```bash
# Generate weekly retrospective
learn-weekly

# Complete your retrospective
edit-retros
```

## 🛠️ All Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `learn-session 'focus'` | Start learning session | `learn-session 'GraphQL basics'` |
| `learn-log 'focus'` | Add daily entry | `learn-log 'API development'` |
| `learn-mistake 'title' 'cat'` | Document mistake | `learn-mistake 'Wrong endpoint' 'API'` |
| `learn-pattern 'name' 'cat'` | Add new pattern | `learn-pattern 'Error Handler' 'Backend'` |
| `learn-commit 'msg' TASK-#` | Commit with reference | `learn-commit 'fix: auth bug' TASK-042` |
| `learn-retro` | Weekly retrospective | - |
| `learn-weekly` | Full weekly review | - |
| `learn-wrap` | End of day summary | - |
| `learn-status` | Show current status | - |
| `learn-help` | Show all commands | - |

## 📂 Quick Navigation

| Shortcut | Destination | Purpose |
|----------|-------------|---------|
| `goto-learning` | Learning docs folder | Navigate to learning files |
| `edit-log` | Learning log | Edit daily progress |
| `edit-mistakes` | Mistakes log | Document errors/solutions |
| `edit-patterns` | Pattern library | Add new code patterns |
| `edit-retros` | Retrospectives | Weekly/monthly reviews |

## 🔍 Validation & Quality

```bash
# Check governance compliance
validate-all

# Check constitutional alignment
validate-constitution
```

## 📊 Learning Categories

### Mistake Categories
- **Setup** - Environment, configuration issues
- **Code Quality** - Syntax, logic errors
- **Process** - Git, workflow mistakes
- **Security** - Authentication, data protection

### Pattern Categories  
- **Frontend** - React, Next.js patterns
- **Backend** - FastAPI, database patterns
- **Architecture** - System design patterns
- **Testing** - Unit, integration test patterns

## 💡 Pro Tips

1. **Start Every Session**: Use `learn-session` to set focus and track time
2. **Document Immediately**: Capture mistakes while fresh in memory
3. **Pattern Everything**: If you solve it twice, make it a pattern
4. **Review Weekly**: Friday retrospectives prevent knowledge loss
5. **Commit with Context**: Always reference TASK numbers
6. **Small Steps**: Document small wins and incremental learning

## 🎯 Learning Goals Template

```markdown
### This Week I Want To:
- [ ] Master [specific skill/concept]
- [ ] Build [specific feature/component] 
- [ ] Fix [specific issue/bug]
- [ ] Document [X] new patterns

### Success Criteria:
- Can explain concept to someone else
- Can implement without referring to docs
- Can identify common mistakes and solutions
- Have working code examples
```

## 🔄 Setup Reminder

If shortcuts aren't working, run:
```bash
source ~/.zshrc
# or restart your terminal
```

---

**Keep this reference handy** - bookmark it or print it out!  
**Location**: `/docs/learning/QUICK_REFERENCE.md`