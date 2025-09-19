# Team Adoption Guide

> Practical guide for adopting and working with the Stitch CMS governance framework.

## 🎯 Quick Start for New Team Members

### Day 1: Essential Reading (30 minutes)
1. **[README.md](README.md)**: Project overview and quick start
2. **[CONSTITUTION.md](CONSTITUTION.md)**: Core principles (focus on principles 1, 6, 9, 10)
3. **This document**: Practical workflows and examples

### Day 2: Hands-On Practice (1 hour)
1. **Set up development environment** (follow README)
2. **Run governance validation**: `python scripts/governance/validate_all.py`
3. **Pick a small task** from [TASKS.md](TASKS.md) (marked as "Good First Issue")
4. **Create your first PR** using our template

### Week 1: Deep Dive
1. **Read [PLAN.md](PLAN.md)**: Understand system architecture
2. **Review [ADR documents](.)**: See how we make decisions
3. **Attend governance review meeting**: Learn our processes
4. **Complete your first task** with full governance compliance

## 📚 Core Concepts Explained

### The Governance Hierarchy
```
CONSTITUTION (principles) ←── ADRs (decisions)
    ↓                              ↓
PLAN (architecture)          ←── SPEC (requirements)
    ↓                              ↓
TASKS (implementation units) → CODE (actual work)
```

**Simple Rule**: Every line of code traces back to a constitutional principle.

### Document IDs and References
| Document | ID Format | Example | Purpose |
|----------|-----------|---------|---------|
| Constitution | `CONST-P#` | `CONST-P1` | Core principles |
| Plans | `PLAN-###` | `PLAN-001` | Architecture decisions |
| Tasks | `TASK-###` | `TASK-004` | Work units |
| Specifications | `SPEC-###` | `SPEC-001` | Requirements |
| ADRs | `ADR-####` | `ADR-0001` | Architecture decisions |

### Traceability Chain Example
```
Code Change → TASK-004 → PLAN-002 → CONST-P1 (API First)
                ↓
              SPEC-002 (Content Management Requirements)
```

## 🛠️ Daily Workflows

### Starting New Work

#### 1. Find Your Task
```bash
# List available tasks
grep -A 5 "Status.*Not Started" TASKS.md

# Pick a task, e.g., TASK-007
```

#### 2. Update Task Status
Edit `TASKS.md`:
```diff
### TASK-007 Set up Structured Logging
- **Status**: Not Started
+ **Status**: In Progress
  **Assignee**: Your Name
```

#### 3. Create Feature Branch
```bash
# Use task ID in branch name
git checkout -b feature/task-007-structured-logging
```

#### 4. Implement and Test
- Follow the task's acceptance criteria
- Write tests for your code
- Maintain documentation

### Creating Pull Requests

#### 1. Use the PR Template
Our template is automatically loaded. Key sections:
- **Task References**: Must reference your TASK-###
- **Constitutional Principles**: Check relevant principles
- **Acceptance Criteria**: Verify all criteria met

#### 2. Example PR Description
```markdown
## Description
Implements structured logging system with JSON output and request correlation.

## Governance Compliance
### Task References  
- [x] TASK-007: Set up Structured Logging

### Constitutional Principles
- [x] CONST-P7: Observability Required
- [x] CONST-P2: Async & Non-Blocking Core

### Acceptance Criteria
- [x] JSON-formatted log output
- [x] Request correlation IDs throughout request lifecycle
- [x] Log levels appropriately set for different environments
- [x] Integration with Python logging module
- [x] Performance metrics logging for slow operations
```

#### 3. Pre-PR Checklist
```bash
# Run governance validation
python scripts/governance/validate_all.py --pr-mode

# Run tests
npm run test && cd backend && pytest

# Check code quality
npm run lint && cd backend && flake8
```

### During Code Review

#### For Authors
- **Respond to governance feedback promptly**
- **Update TASKS.md if scope changes**
- **Maintain traceability in discussions**

#### For Reviewers  
- **Verify task references are valid**
- **Check constitutional principle alignment**
- **Ensure acceptance criteria are met**
- **Validate traceability chain**

### Completing Work

#### 1. Mark Task Complete
Edit `TASKS.md`:
```diff
### TASK-007 Set up Structured Logging
- **Status**: In Progress
+ **Status**: Completed
```

#### 2. Update Documentation
- Add implementation notes to task
- Update relevant PLAN items if needed
- Document any architectural decisions

## 🚨 Common Scenarios

### Scenario 1: "My PR fails governance validation"

**Problem**: `validate_pr_references.py` fails
**Solution**:
```bash
# Check your PR description includes TASK reference
echo "- [x] TASK-007: Brief description" >> pr-description.md

# Verify task exists
grep "TASK-007" TASKS.md
```

### Scenario 2: "I need to create a new task"

**When**: You discover work not covered by existing tasks
**Process**:
1. **Check if it fits existing task scope** (often it does)
2. **If truly new work**:
   - Add to TASKS.md following the format
   - Reference a PLAN or SPEC item
   - Include acceptance criteria
   - Get maintainer approval

**Template**:
```markdown
### TASK-020 Brief Task Title
**Status**: Not Started
**References**: PLAN-XXX or SPEC-XXX
**Assignee**: Vacant
**Estimated Effort**: S/M/L/XL
**Dependencies**: TASK-XXX (if any)

**Acceptance Criteria**:
- [ ] Specific, measurable outcome 1
- [ ] Specific, measurable outcome 2

**Implementation Notes**: Brief technical approach
```

### Scenario 3: "I want to change the architecture"

**When**: You want to make significant technical changes
**Process**:
1. **Small changes**: Update relevant PLAN item via PR
2. **Significant changes**: Create ADR following ADR-0001 format
3. **Constitutional impact**: Follow amendment process in Constitution

### Scenario 4: "The governance is blocking me"

**Emergency Override** (rare, use sparingly):
```bash
# For true emergencies only
git commit -m "hotfix: critical security patch [skip-governance]"
```
**Must**:
- Create TASK-### for governance remediation
- Explain rationale in commit
- Fix governance within 24 hours

## 🎨 Best Practices

### Writing Good Tasks
```markdown
❌ Bad: "Fix the API"
✅ Good: "Add input validation to content creation endpoints"

❌ Bad: "Make it faster"  
✅ Good: "Reduce average API response time to <200ms for content queries"
```

### Referencing in Code Comments
```python
# TASK-007: Implement structured logging (CONST-P7)
def setup_logging():
    """Set up structured logging with request correlation."""
    pass
```

### Commit Messages
```bash
# Good commit messages
git commit -m "feat(logging): add structured JSON logging (TASK-007)"
git commit -m "fix(auth): resolve JWT validation bug (TASK-001)"
git commit -m "docs: update API documentation (TASK-011)"
```

## 🔧 Tools and Scripts

### Governance Validation
```bash
# Run all validations
python scripts/governance/validate_all.py

# Individual validations
python scripts/governance/validate_constitution.py
python scripts/governance/validate_traceability.py
python scripts/governance/validate_pr_references.py --check-commits

# PR mode (includes commit checking)
python scripts/governance/validate_all.py --pr-mode
```

### Task Management Helpers
```bash
# Find tasks by status
grep -A 3 "Status.*Not Started" TASKS.md
grep -A 3 "Status.*In Progress" TASKS.md

# Find tasks by assignee
grep -A 3 "Assignee.*YourName" TASKS.md

# Find tasks by effort
grep -A 3 "Effort.*S" TASKS.md  # Small tasks
```

### Quick References
```bash
# List all constitutional principles
grep "### CONST-P" CONSTITUTION.md

# List all plan items
grep "### PLAN-" PLAN.md

# Count total tasks
grep "### TASK-" TASKS.md | wc -l

# Find orphaned tasks (tasks without references)
python scripts/governance/validate_traceability.py
```

## 📊 Governance Health Monitoring

### Individual Metrics
Track your governance compliance:
- **Tasks completed this sprint**: X
- **PRs with governance issues**: X/Y
- **Average time to complete governance validation**: X hours

### Team Metrics  
We track at team level:
- **Governance CI failure rate**: <5% target
- **PR compliance rate**: >90% target
- **Task traceability coverage**: >95% target

## 🎓 Training Resources

### Self-Paced Learning
1. **Week 1**: Focus on CONST-P1, P6, P9, P10 (core workflow principles)
2. **Week 2**: Dive into PLAN-001 through PLAN-003 (architecture basics)
3. **Week 3**: Practice with small tasks, focus on traceability
4. **Week 4**: Advanced topics: ADRs, governance reviews, process improvements

### Team Sessions
- **Monthly Governance Review**: First Tuesday of each month
- **New Team Member Onboarding**: On-demand scheduling
- **Architecture Decision Workshops**: Quarterly
- **Process Improvement Sessions**: As needed

### Resources
- **[Constitutional Principles Deep Dive](CONSTITUTION.md)**: Full principle explanations
- **[Architecture Decision Records](.)**: Learn from past decisions
- **[Review Schedule](GOVERNANCE_REVIEWS.md)**: Understand our regular processes
- **Team Wiki**: (Coming soon - TASK-018)

## 🆘 Getting Help

### Governance Questions
1. **Check this guide first** - common scenarios covered above
2. **Run validation scripts** - often provides specific guidance
3. **Review similar PRs** - see how others handled similar situations
4. **Ask in team chat** - governance channel for quick questions
5. **Create discussion issue** - for complex governance questions

### Technical Questions  
1. **API Documentation**: Available at `/docs` when backend running
2. **Architecture Questions**: Review PLAN.md and ADRs
3. **Code Patterns**: Check existing implementation examples
4. **Database Questions**: Review models in `/backend/models/`

### Process Questions
1. **Task Management**: Check TASKS.md format and examples
2. **Review Process**: See PR template and GOVERNANCE_REVIEWS.md
3. **Emergency Procedures**: Check ENFORCEMENT.md override procedures

## ✅ Readiness Checklist

### New Team Member Readiness
After your first week, you should be able to:
- [ ] Find and understand a task in TASKS.md
- [ ] Create a governance-compliant PR
- [ ] Run and interpret validation scripts
- [ ] Explain our traceability model to someone else
- [ ] Complete a small task from start to finish

### Maintainer Readiness
Before becoming a maintainer, you should:
- [ ] Have completed 5+ governance-compliant PRs
- [ ] Understand all constitutional principles
- [ ] Have reviewed others' PRs with governance feedback
- [ ] Participated in monthly governance reviews
- [ ] Demonstrated architecture decision thinking

## 🚀 Advanced Workflows

### Creating Architectural Changes
1. **Identify Impact**: Which CONST-P principles affected?
2. **Research**: Review existing ADRs for similar decisions  
3. **Draft ADR**: Follow ADR-0001 template
4. **Team Discussion**: Present at architecture meeting
5. **Implementation Plan**: Update PLAN items, create TASKs
6. **Documentation**: Update all affected documents

### Process Improvements
1. **Identify Friction**: Where does governance slow us down unnecessarily?
2. **Propose Solution**: Create TASK for governance improvement
3. **Experiment**: Test changes on small scale
4. **Measure Impact**: Track relevant metrics
5. **Iterate**: Refine based on team feedback

---

## 📞 Support Contacts

| Question Type | Contact | Response Time |
|---------------|---------|---------------|
| Urgent governance blocking | @tech-lead (Slack) | <2 hours |
| General governance questions | #governance (Slack) | <4 hours |
| Process improvements | Monthly governance review | Next meeting |
| Architecture decisions | Architecture review meeting | Weekly |

---

## Metadata
**Version**: 1.0.0  
**Last Updated**: 2025-09-20  
**Target Audience**: All team members  
**Prerequisites**: Basic Git/GitHub knowledge  
**Estimated Onboarding Time**: 1 week to proficiency  

**Change Log**:
- 2025-09-20: Initial team adoption guide creation