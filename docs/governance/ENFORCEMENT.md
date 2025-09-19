# Governance Enforcement

> Automation rules, compliance checks, and quality gates to ensure adherence to Constitutional principles and governance processes.

## Overview
This document defines automated enforcement mechanisms for governance compliance as required by CONST-P6 (Spec-Driven Change Flow) and referenced in Constitution Section 5 (Compliance & Enforcement Hooks).

## Enforcement Categories

### 1. Document Structure Validation
Automated checks for governance document integrity and format compliance.

#### Constitution Compliance Check
**Rule ID**: `ENF-001`  
**Trigger**: Every PR, CI pipeline  
**Implementation**: Python script in `/scripts/governance/`

**Validation Rules**:
- [ ] `CONSTITUTION.md` exists and is valid Markdown
- [ ] All principle IDs (CONST-P#) are unique
- [ ] No duplicate principle numbering
- [ ] Required sections present (Purpose, Principles, Decision Hierarchy, etc.)
- [ ] Version number and effective date present

**Implementation**:
```python
def validate_constitution():
    """Validate CONSTITUTION.md structure and content."""
    # Check file exists
    # Parse markdown and validate structure
    # Extract and validate CONST-P# IDs for uniqueness
    # Validate required sections present
    pass
```

#### Plan Document Validation
**Rule ID**: `ENF-002`  
**Trigger**: Every PR modifying PLAN.md  
**Implementation**: Python script

**Validation Rules**:
- [ ] All PLAN-# IDs are unique and sequential
- [ ] Each plan item references valid CONST-P# principles
- [ ] Status field is valid (Active/Proposed/Deferred/Superseded)
- [ ] Required sections present for each plan item

#### Task Document Validation
**Rule ID**: `ENF-003`  
**Trigger**: Every PR modifying TASKS.md  
**Implementation**: Python script

**Validation Rules**:
- [ ] All TASK-### IDs are unique and follow format
- [ ] Each task references valid PLAN-# or SPEC-# items
- [ ] Acceptance criteria are specific and measurable
- [ ] Status field is valid (Not Started/In Progress/Blocked/Completed)
- [ ] Effort estimation follows guidelines (S/M/L/XL)

### 2. Traceability Enforcement
Ensures proper linking between governance layers per CONST-P10.

#### PR Reference Validation
**Rule ID**: `ENF-004`  
**Trigger**: Every PR submission  
**Implementation**: GitHub Action

**Validation Rules**:
- [ ] PR description contains at least one TASK-### reference
- [ ] Referenced TASK exists in TASKS.md
- [ ] Task status allows for implementation work
- [ ] No orphaned tasks (all reference PLAN/SPEC items)

**GitHub Action Implementation**:
```yaml
name: PR Reference Validation
on: [pull_request]
jobs:
  validate-references:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate PR References
        run: python scripts/governance/validate_pr_references.py
```

#### Code-to-Task Traceability
**Rule ID**: `ENF-005`  
**Trigger**: Code commits  
**Implementation**: Git hooks

**Validation Rules**:
- [ ] Commit messages reference TASK-### when implementing features
- [ ] No implementation without corresponding task
- [ ] Task completion updates when all acceptance criteria met

### 3. Quality Gate Enforcement
Automated quality checks aligned with Constitutional principles.

#### API Documentation Compliance
**Rule ID**: `ENF-006`  
**Trigger**: API endpoint changes  
**Principle**: CONST-P1 (API First)  
**Implementation**: OpenAPI validation

**Validation Rules**:
- [ ] All new API endpoints have OpenAPI documentation
- [ ] Response schemas defined and validated
- [ ] Authentication requirements specified
- [ ] Version compatibility maintained

#### Security Compliance Check
**Rule ID**: `ENF-007`  
**Trigger**: Code changes affecting security  
**Principle**: CONST-P5 (Security by Default)  
**Implementation**: Security scanning tools

**Validation Rules**:
- [ ] No hardcoded secrets or API keys
- [ ] Authentication required for protected endpoints
- [ ] Input validation on all user-facing inputs
- [ ] Sensitive data properly masked in logs

#### Test Coverage Enforcement
**Rule ID**: `ENF-008`  
**Trigger**: Code changes  
**Principle**: CONST-P9 (Testable Units)  
**Implementation**: Coverage tools

**Validation Rules**:
- [ ] Minimum 80% test coverage for new code
- [ ] All new API endpoints have tests
- [ ] Critical business logic has unit tests
- [ ] Integration tests for database operations

### 4. Change Process Enforcement
Validates adherence to governance change flows.

#### ADR Process Validation
**Rule ID**: `ENF-009`  
**Trigger**: Architectural changes  
**Principle**: CONST-P6 (Spec-Driven Change Flow)  
**Implementation**: Manual + automated checks

**Validation Rules**:
- [ ] Significant architectural changes have corresponding ADR
- [ ] ADR follows standard format and sections
- [ ] ADR references affected CONST-P# principles
- [ ] ADR status properly tracked (Proposed → Accepted → Implemented)

#### Constitution Amendment Process
**Rule ID**: `ENF-010`  
**Trigger**: Constitution changes  
**Implementation**: GitHub branch protection + reviews

**Validation Rules**:
- [ ] Changes to CONSTITUTION.md require ADR
- [ ] At least 2 maintainer approvals required
- [ ] All CI checks must pass
- [ ] Impact matrix provided in PR
- [ ] Migration plan for affected documents

## Implementation Scripts

### Core Validation Scripts
Location: `/scripts/governance/`

#### `validate_constitution.py`
```python
#!/usr/bin/env python3
"""Validate CONSTITUTION.md structure and compliance."""

import re
import sys
from pathlib import Path

def main():
    constitution_path = Path("CONSTITUTION.md")
    if not constitution_path.exists():
        print("ERROR: CONSTITUTION.md not found")
        sys.exit(1)
    
    content = constitution_path.read_text()
    
    # Validate principle IDs
    principle_ids = re.findall(r'CONST-P(\d+):', content)
    if len(principle_ids) != len(set(principle_ids)):
        print("ERROR: Duplicate CONST-P# IDs found")
        sys.exit(1)
    
    # Validate required sections
    required_sections = [
        "Purpose", "Principles", "Decision Hierarchy", 
        "Amendment Process", "Compliance & Enforcement"
    ]
    
    for section in required_sections:
        if f"## {section}" not in content and f"# {section}" not in content:
            print(f"ERROR: Required section '{section}' not found")
            sys.exit(1)
    
    print("✅ Constitution validation passed")

if __name__ == "__main__":
    main()
```

#### `validate_traceability.py`
```python
#!/usr/bin/env python3
"""Validate traceability between governance documents."""

import re
import sys
from pathlib import Path

def extract_references(content, pattern):
    """Extract references matching pattern from content."""
    return set(re.findall(pattern, content))

def main():
    # Load all governance documents
    docs = {}
    for doc_name in ["PLAN.md", "TASKS.md", "CONSTITUTION.md"]:
        path = Path(doc_name)
        if path.exists():
            docs[doc_name] = path.read_text()
    
    # Extract all reference IDs
    plan_ids = extract_references(docs.get("PLAN.md", ""), r'PLAN-(\d+)')
    task_ids = extract_references(docs.get("TASKS.md", ""), r'TASK-(\d{3})')
    const_ids = extract_references(docs.get("CONSTITUTION.md", ""), r'CONST-P(\d+)')
    
    # Validate task references
    if "TASKS.md" in docs:
        task_references = extract_references(docs["TASKS.md"], r'PLAN-(\d+)|SPEC-(\d+)')
        orphaned_tasks = []
        
        for task in task_ids:
            task_section = re.search(f'### TASK-{task}.*?(?=### TASK-|\Z)', 
                                   docs["TASKS.md"], re.DOTALL)
            if task_section:
                task_content = task_section.group(0)
                if not re.search(r'PLAN-\d+|SPEC-\d+', task_content):
                    orphaned_tasks.append(f"TASK-{task}")
        
        if orphaned_tasks:
            print(f"ERROR: Tasks without PLAN/SPEC references: {orphaned_tasks}")
            sys.exit(1)
    
    print("✅ Traceability validation passed")

if __name__ == "__main__":
    main()
```

### CI Integration

#### GitHub Actions Workflow
Location: `.github/workflows/governance.yml`

```yaml
name: Governance Compliance

on:
  pull_request:
    paths:
      - 'CONSTITUTION.md'
      - 'PLAN.md'
      - 'TASKS.md'
      - 'ADR-*.md'
      - 'scripts/governance/**'

jobs:
  validate-governance:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyyaml markdown
    
    - name: Validate Constitution
      run: python scripts/governance/validate_constitution.py
    
    - name: Validate Traceability
      run: python scripts/governance/validate_traceability.py
    
    - name: Validate PR References
      run: python scripts/governance/validate_pr_references.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        PR_NUMBER: ${{ github.event.number }}
```

### Manual Enforcement Procedures

#### Constitution Amendment Review
1. **Pre-Review Checklist**:
   - [ ] ADR created and linked to PR
   - [ ] Impact matrix provided
   - [ ] All affected PLAN/SPEC items identified
   - [ ] Migration plan for breaking changes

2. **Review Process**:
   - [ ] Technical review by 2+ maintainers
   - [ ] Governance impact assessment
   - [ ] Community feedback period (48h minimum)
   - [ ] All CI checks passing

3. **Post-Merge Actions**:
   - [ ] Update affected downstream documents
   - [ ] Communicate changes to team
   - [ ] Update enforcement scripts if needed

#### Quality Gate Overrides
**Emergency Override Process**:
- Requires 2 maintainer approvals
- Must create TASK-### for remediation
- Time-boxed exception (max 7 days)
- Documented rationale in PR

## Monitoring and Reporting

### Compliance Dashboard
Track governance health with automated metrics:
- Constitution compliance score
- Traceability coverage percentage
- Orphaned task/plan item count
- ADR completion rate
- Test coverage trends

### Weekly Governance Report
Automated weekly report including:
- Compliance check results
- Outstanding governance tasks
- Document freshness metrics
- Process adherence scores

## Maintenance and Evolution

### Script Updates
- Enforcement scripts versioned with governance documents
- Changes require ADR for significant modifications
- Backward compatibility maintained for 2 versions
- Test coverage required for all enforcement logic

### Process Improvements
- Regular review of enforcement effectiveness
- False positive analysis and rule refinement
- Community feedback integration
- Automation opportunity identification

---

## Quick Reference

### Running Manual Checks
```bash
# Validate all governance documents
python scripts/governance/validate_constitution.py
python scripts/governance/validate_traceability.py

# Check specific document
python scripts/governance/validate_plan.py
python scripts/governance/validate_tasks.py
```

### Bypass Procedures (Emergency Only)
```bash
# Skip governance checks (requires justification)
git commit -m "feat: emergency fix [skip-governance]"

# Override quality gate (creates remediation task)
git push -o skip-ci="governance"
```

### Common Fixes
- **Orphaned Task**: Add PLAN-# or SPEC-# reference to task description
- **Missing ADR**: Create ADR-#### for architectural changes
- **Traceability Break**: Update references to maintain chain
- **Test Coverage**: Add tests before merging feature PRs

---

## Metadata
**Version**: 1.0.0  
**Last Updated**: 2025-09-20  
**Next Review**: Monthly governance review  

**Change Log**:
- 2025-09-20: Initial enforcement framework creation