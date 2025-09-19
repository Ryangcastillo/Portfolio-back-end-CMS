# Stitch CMS

> A modern, extensible Content Management System with integrated governance and AI capabilities.

[![Build Status](https://github.com/Ryangcastillo/CMS/actions/workflows/governance.yml/badge.svg)](https://github.com/Ryangcastillo/CMS/actions)
[![Governance Compliance](https://img.shields.io/badge/Governance-Compliant-green)](#governance-framework)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🏗️ Project Architecture

Stitch CMS is built with a **governance-first** approach, ensuring maintainable, scalable, and well-documented development practices.

### Technology Stack
- **Backend**: FastAPI + SQLAlchemy (async) with PostgreSQL
- **Frontend**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **AI Integration**: Pluggable AI provider system (OpenAI, Anthropic, etc.)
- **Infrastructure**: Docker, GitHub Actions, Vercel deployment

### Core Features
- 📝 **Content Management**: Rich text editing, media handling, versioning
- 👥 **User Management**: Role-based access control, authentication
- 🎉 **Event Management**: Event creation, RSVP tracking, notifications  
- 🔌 **Module System**: Extensible plugin architecture
- 🤖 **AI Assistant**: Integrated AI capabilities for content generation
- 📊 **Analytics**: Usage tracking and performance monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ryangcastillo/CMS.git
   cd CMS
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb stitch_cms
   
   # Run migrations
   alembic upgrade head
   ```

4. **Set up frontend**
   ```bash
   cd ..  # Back to root
   npm install
   # or
   pnpm install
   ```

5. **Start development servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Frontend
   npm run dev
   # or
   pnpm dev
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Governance Framework

Stitch CMS follows a comprehensive governance framework to ensure code quality, maintainability, and team collaboration.

### Key Documents
- **[CONSTITUTION.md](CONSTITUTION.md)**: Core principles and governance rules
- **[PLAN.md](PLAN.md)**: Architectural blueprint and system design
- **[TASKS.md](TASKS.md)**: Development tasks with clear traceability
- **[ENFORCEMENT.md](ENFORCEMENT.md)**: Automated compliance and quality gates
- **[ADR-*.md](.)**: Architecture Decision Records

### Quick Governance Guide

#### For New Contributors
1. **Read the Constitution**: Understand our [12 core principles](CONSTITUTION.md#principles)
2. **Follow the Process**: Constitution → Plan → Tasks → Implementation
3. **Reference Tasks**: All PRs must reference at least one `TASK-###`
4. **Use PR Template**: Our template ensures governance compliance
5. **Pass CI Checks**: Automated validation enforces our standards

#### For Maintainers  
- **Review Process**: Ensure PRs follow governance requirements
- **Traceability**: Verify TASK → PLAN/SPEC → CONST-P# links
- **Quality Gates**: All governance checks must pass before merge
- **Regular Reviews**: Monthly governance health assessments

### Governance Validation
```bash
# Run all governance checks
python scripts/governance/validate_all.py

# Individual validations
python scripts/governance/validate_constitution.py
python scripts/governance/validate_traceability.py
python scripts/governance/validate_pr_references.py
```

## 🛠️ Development Workflow

### 1. Starting New Work
```bash
# Check current tasks
cat TASKS.md | grep "Not Started" -A 3

# Pick a task (e.g., TASK-004)
# Create feature branch
git checkout -b feature/task-004-content-management

# Update task status to "In Progress" in TASKS.md
```

### 2. During Development
- Follow the acceptance criteria in your chosen task
- Write tests for all new functionality
- Maintain API documentation (automatic with FastAPI)
- Update relevant documentation

### 3. Before Submitting PR
```bash
# Run tests
npm run test              # Frontend tests
cd backend && pytest     # Backend tests

# Run governance validation
python scripts/governance/validate_all.py --pr-mode

# Check code quality  
npm run lint              # Frontend linting
cd backend && flake8      # Backend linting
```

### 4. PR Submission
- Use the provided PR template
- Reference your TASK-### in PR description
- Ensure all CI checks pass
- Request review from maintainers

## 🏛️ Constitutional Principles

Our development is guided by [12 core principles](CONSTITUTION.md#principles):

1. **API First** - All capabilities exposed via documented APIs
2. **Async & Non-Blocking** - Prefer async patterns for performance  
3. **Extensibility by Abstraction** - Clear interfaces for future plugins
4. **Separation of Concerns** - Decoupled layers and boundaries
5. **Security & Privacy by Default** - Security built-in, not bolted-on
6. **Spec-Driven Change Flow** - Structured change process
7. **Observability Required** - Comprehensive logging and monitoring
8. **Incremental Hardening** - Continuous security improvements
9. **Testable Units Only** - All work has clear success criteria
10. **Change Traceability** - Full traceability from PR to principles
11. **Minimal Surface Area** - Avoid premature complexity
12. **Fast Feedback & Small Batches** - Quick iterations and reviews

## 📊 Project Status

### Current Sprint Focus
- ✅ Core authentication system (TASK-001 through TASK-003)
- ✅ Governance framework implementation (TASK-016)  
- 🔄 Content management API (TASK-004)
- 🔄 Event management system (TASK-005)
- 📋 Frontend component library (TASK-011)

### Architecture Decisions
- [ADR-0001](ADR-0001.md): FastAPI + SQLAlchemy backend choice
- [ADR-0002](ADR-0002.md): Next.js App Router frontend choice

## 🤝 Contributing

We welcome contributions! Please follow our governance framework:

1. **Read Documentation**: Start with [CONSTITUTION.md](docs/governance/CONSTITUTION.md)
2. **Find a Task**: Check [TASKS.md](TASKS.md) for available work
3. **Follow Process**: Use our [PR template](.github/pull_request_template.md)
4. **Pass Validation**: All governance checks must pass
5. **Get Review**: Maintainer approval required

### New Contributors
- Join our [onboarding process](TASK-018) (coming soon)
- Ask questions in discussions or issues
- Start with small, well-defined tasks
- Follow our [code of conduct](CODE_OF_CONDUCT.md) (coming soon)

## 📚 Documentation

### Core Documentation
- **[README.md](README.md)**: Project overview and quick start (you are here)
- **[TASKS.md](TASKS.md)**: Current development tasks and status
- **[SPECIFY.md](SPECIFY.md)**: System requirements and specifications

### Governance Framework
Located in `/docs/governance/`:
- **[CONSTITUTION.md](docs/governance/CONSTITUTION.md)**: Core principles and decision framework
- **[ENFORCEMENT.md](docs/governance/ENFORCEMENT.md)**: Governance compliance rules and automation
- **[GOVERNANCE_REVIEWS.md](docs/governance/GOVERNANCE_REVIEWS.md)**: Regular review schedules and templates
- **[GOVERNANCE_SUMMARY.md](docs/governance/GOVERNANCE_SUMMARY.md)**: Complete framework overview
- **[TEAM_ADOPTION_GUIDE.md](docs/governance/TEAM_ADOPTION_GUIDE.md)**: Practical workflows and examples

### Architecture Documentation
Located in `/docs/architecture/`:
- **[PLAN.md](docs/architecture/PLAN.md)**: System architecture blueprint
- **[SPECIFICATIONS.md](docs/architecture/SPECIFICATIONS.md)**: Detailed system specifications
- **[ADR-0001.md](docs/architecture/ADR-0001.md)**: Backend technology decision
- **[ADR-0002.md](docs/architecture/ADR-0002.md)**: Frontend technology decision

### For Developers
- **API Documentation**: Available at `/docs` when backend is running
- **Component Library**: Shadcn/ui components in `/components/ui/`
- **Development Workflows**: See [TEAM_ADOPTION_GUIDE.md](docs/governance/TEAM_ADOPTION_GUIDE.md)

## 🔍 Quality Assurance

### Automated Checks
- **CI/CD Pipeline**: GitHub Actions with comprehensive testing
- **Governance Validation**: Automated compliance checking  
- **Code Quality**: ESLint, Prettier, Flake8, mypy
- **Security Scanning**: Automated vulnerability detection
- **Test Coverage**: Minimum 80% coverage required

### Manual Processes  
- **Code Review**: All PRs require maintainer approval
- **Governance Review**: Monthly framework health assessment
- **Architecture Review**: Quarterly strategic alignment check
- **Security Review**: Regular security audits and updates

## 📈 Monitoring & Observability

### Development Metrics
- Governance compliance score
- Test coverage percentage  
- CI success rate
- PR review time

### Application Metrics
- API response times
- User engagement analytics
- System performance monitoring
- Error rates and alerting

## 📞 Support & Community

### Get Help
- **Issues**: [GitHub Issues](https://github.com/Ryangcastillo/CMS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ryangcastillo/CMS/discussions)  
- **Documentation**: Check this README and linked docs first

### Governance Questions
- Review [CONSTITUTION.md](CONSTITUTION.md) for principles
- Check [ENFORCEMENT.md](ENFORCEMENT.md) for specific rules
- Run validation scripts for immediate feedback
- Ask in discussions for complex questions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Metadata
**Version**: 2.0.0  
**Last Updated**: 2025-09-20  
**Governance Status**: ✅ Compliant  
**Architecture**: FastAPI + Next.js + PostgreSQL  
**Governance Framework**: Constitution + Plan + Tasks + ADRs  

**Quick Links**: [Constitution](CONSTITUTION.md) | [Tasks](TASKS.md) | [Plan](PLAN.md) | [Reviews](GOVERNANCE_REVIEWS.md)
