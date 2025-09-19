# Stitch CMS Documentation

> Comprehensive documentation for the Stitch CMS project

## 📁 Documentation Structure

### `/docs/governance/`
**Governance Framework Documents**
- `CONSTITUTION.md` - Core principles and decision framework
- `ENFORCEMENT.md` - Governance compliance rules and automation  
- `GOVERNANCE_REVIEWS.md` - Regular review schedules and templates
- `GOVERNANCE_SUMMARY.md` - Complete framework overview
- `TEAM_ADOPTION_GUIDE.md` - Practical workflows and examples for team members

### `/docs/architecture/`
**System Architecture Documentation**
- `PLAN.md` - System architecture blueprint and design decisions
- `SPECIFICATIONS.md` - Detailed system specifications and requirements
- `ADR-0001.md` - Backend technology decision record
- `ADR-0002.md` - Frontend technology decision record
- Additional ADR files for future architectural decisions

## 🎯 Quick Navigation

### New Team Members
1. Start with [../README.md](../README.md) for project overview
2. Read [governance/TEAM_ADOPTION_GUIDE.md](governance/TEAM_ADOPTION_GUIDE.md) for workflows
3. Review [governance/CONSTITUTION.md](governance/CONSTITUTION.md) for principles
4. Check [../TASKS.md](../TASKS.md) for current work items

### Developers
1. Architecture: [architecture/PLAN.md](architecture/PLAN.md)
2. Requirements: [architecture/SPECIFICATIONS.md](architecture/SPECIFICATIONS.md)
3. Technology Decisions: [architecture/ADR-0001.md](architecture/ADR-0001.md) and [architecture/ADR-0002.md](architecture/ADR-0002.md)
4. Tasks: [../TASKS.md](../TASKS.md)

### Maintainers
1. Framework Overview: [governance/GOVERNANCE_SUMMARY.md](governance/GOVERNANCE_SUMMARY.md)
2. Compliance Rules: [governance/ENFORCEMENT.md](governance/ENFORCEMENT.md)
3. Review Process: [governance/GOVERNANCE_REVIEWS.md](governance/GOVERNANCE_REVIEWS.md)

## 📊 Document Status

| Document | Status | Last Updated | Owner |
|----------|---------|--------------|-------|
| CONSTITUTION.md | ✅ Active | 2025-09-20 | Team |
| PLAN.md | ✅ Active | 2025-09-20 | Architecture Team |
| TASKS.md | ✅ Active | 2025-09-20 | Development Team |
| SPECIFICATIONS.md | ✅ Active | 2025-09-20 | Architecture Team |
| ADR-0001.md | ✅ Active | 2025-09-20 | Architecture Team |
| ADR-0002.md | ✅ Active | 2025-09-20 | Architecture Team |
| ENFORCEMENT.md | ✅ Active | 2025-09-20 | Governance Team |
| GOVERNANCE_REVIEWS.md | ✅ Active | 2025-09-20 | Governance Team |
| GOVERNANCE_SUMMARY.md | ✅ Active | 2025-09-20 | Governance Team |
| TEAM_ADOPTION_GUIDE.md | ✅ Active | 2025-09-20 | Governance Team |

## 🔄 Maintenance

### Document Review Schedule
- **Weekly**: TASKS.md updates
- **Monthly**: Governance process effectiveness review
- **Quarterly**: Constitutional and architectural review
- **As Needed**: ADR creation for significant decisions

### Update Process
1. All documentation changes follow governance processes
2. Significant changes require PR with governance validation
3. Documentation must maintain traceability to constitutional principles
4. Regular reviews ensure currency and relevance

## 🛠️ Contributing to Documentation

### Adding New Documents
1. Determine appropriate folder (`governance/` or `architecture/`)
2. Follow existing document format and structure
3. Update this README.md with new document information
4. Ensure governance validation passes
5. Submit PR with proper task references

### Updating Existing Documents
1. Follow standard PR process
2. Reference relevant TASK in commit message
3. Ensure governance traceability is maintained
4. Run `python3 scripts/governance/validate_all.py` before committing

---

## Metadata
**Directory**: `/docs/`  
**Purpose**: Central documentation hub  
**Maintenance**: Development Team  
**Last Updated**: 2025-09-20  
**Next Review**: 2025-10-20