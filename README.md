# Stitch CMS - Headless CMS Architecture

> A modern, modular **Headless Content Management System** with integrated AI capabilities, designed for scalability and multi-frontend flexibility.

[![Build Status](https://github.com/Ryangcastillo/CMS/actions/workflows/governance.yml/badge.svg)](https://github.com/Ryangcastillo/CMS/actions)
[![Governance Compliance](https://img.shields.io/badge/Governance-Compliant-green)](#governance-framework)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🏗️ Headless CMS Architecture

Stitch CMS implements a **headless CMS architecture** that separates content management from content presentation, enabling:
- 🎯 **Content-first approach** with API-driven architecture
- 🔌 **Modular frontend applications** that can be easily added, swapped, or removed
- 🚀 **Scalable infrastructure** with independent frontend and backend deployments
- 🛡️ **Centralized content governance** with distributed presentation layers

### Architecture Components

#### 1. **Backend + CMS Admin Interface** (Control Center)
- **Location**: `/app` - Next.js 14+ Admin Dashboard
- **Purpose**: Content creation, management, and system administration
- **Features**: Authentication, content CRUD, analytics, AI integration, module management

#### 2. **Headless CMS API** (Data Layer)
- **Location**: `/backend` - FastAPI with SQLAlchemy
- **Purpose**: Serve content via RESTful APIs to multiple frontend applications
- **Features**: Public APIs (no auth), admin APIs (authenticated), real-time updates

#### 3. **Modular Frontend Applications** (Presentation Layer)
- **Location**: `/Frontend` and additional frontend modules
- **Purpose**: Public-facing websites, portfolios, landing pages, web applications
- **Features**: React SPAs, static sites, e-commerce frontends, marketing sites

### Technology Stack
- **Backend API**: FastAPI + SQLAlchemy (async) with PostgreSQL
- **Admin Interface**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **Frontend Modules**: React, Vue, Next.js, or any framework that consumes APIs
- **AI Integration**: Pluggable AI provider system (OpenAI, Anthropic, etc.)
- **Infrastructure**: Docker, GitHub Actions, Vercel/cloud deployment

### Core Features
- 📝 **Headless Content Management**: API-first content creation and management
- 🔌 **Plugin Frontend Architecture**: Easy addition/removal of frontend applications
- 👥 **Centralized User Management**: Role-based access control across all applications
- 🎉 **Event Management**: Event creation with multi-frontend distribution
- 🤖 **AI Assistant**: Integrated AI capabilities accessible across all frontends
- 📊 **Unified Analytics**: Performance tracking across all connected applications
- 🎨 **Component Library**: Reusable components for consistent UI across frontends

## 🚀 Quick Start - Headless CMS Setup

### Prerequisites
- Python 3.11+ (Backend API)
- Node.js 18+ (Admin Interface)  
- PostgreSQL 14+ (Database)
- Git (Version Control)

### Architecture-Specific Setup

#### Step 1: Backend CMS API Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment configuration
cp .env.example .env
# Configure database URL and other settings in .env
```

#### Step 2: Database Migration
```bash
# Create PostgreSQL database
createdb stitch_cms

# Run migrations for headless CMS models
alembic upgrade head
```

#### Step 3: Admin Interface Setup
```bash
# From project root
npm install
# or
pnpm install

# Configure admin environment
cp .env.local.example .env.local
# Set API endpoints and authentication settings
```

#### Step 4: Frontend Module Setup (Optional)
```bash
cd Frontend
npm install

# Configure API connection
cp .env.example .env.local
# Set REACT_APP_API_URL to your backend API
```

### Running the Headless CMS

#### Start Backend API Server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
# API available at http://localhost:8000
# OpenAPI docs at http://localhost:8000/docs
```

#### Start Admin Interface  
```bash
# From project root
npm run dev
# Admin interface at http://localhost:3000
```

#### Start Frontend Module (Optional)
```bash
cd Frontend
npm start
# Public website at http://localhost:3001
```

## 🏗️ Architecture Overview

### 📖 Comprehensive Documentation
For detailed technical specifications, data models, API documentation, and deployment strategies, see:
- **[HEADLESS_CMS_ARCHITECTURE.md](HEADLESS_CMS_ARCHITECTURE.md)** - Complete technical architecture guide
- **[CONSTITUTION.md](CONSTITUTION.md)** - Core principles and governance rules  
- **[components.md](components.md)** - Component library documentation
- **[backend_api_catalog.md](backend_api_catalog.md)** - API endpoint specifications

### System Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                       HEADLESS CMS ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐  │
│  │   Admin Interface│    │  Headless API   │    │  Frontend Modules│  │
│  │   (Next.js)     │────│   (FastAPI)     │────│   (React/Vue)   │  │
│  │                 │    │                 │    │                  │  │
│  │ • Content CRUD  │    │ • Public APIs   │    │ • Portfolios     │  │
│  │ • User Management│    │ • Admin APIs    │    │ • Landing Pages │  │
│  │ • Analytics     │    │ • Authentication│    │ • E-commerce    │  │
│  │ • Module Manager│    │ • Real-time     │    │ • Blogs         │  │
│  └─────────────────┘    └─────────────────┘    └──────────────────┘  │
│           │                       │                       │          │
│           └───────────────────────┼───────────────────────┘          │
│                                   │                                  │
│                        ┌─────────────────┐                          │
│                        │   PostgreSQL    │                          │
│                        │   Database      │                          │
│                        │                 │                          │
│                        │ • Content Models│                          │
│                        │ • User Data     │                          │
│                        │ • Analytics     │                          │
│                        │ • Configuration │                          │
│                        └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Benefits
- **🔄 Content Once, Display Everywhere**: Create content in admin interface, consume via APIs
- **🔌 Modular Frontends**: Add/remove website modules without affecting backend
- **📱 Multi-Channel Distribution**: Same content across web, mobile, IoT devices
- **🚀 Independent Scaling**: Scale admin, API, and frontends independently
- **🛡️ Centralized Governance**: Unified content workflow with distributed presentation

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

Our headless CMS development is guided by [12 core principles](CONSTITUTION.md#principles):

1. **API First** - All capabilities exposed via documented APIs for headless architecture
2. **Async & Non-Blocking** - Prefer async patterns for high-performance content delivery  
3. **Extensibility by Abstraction** - Clear interfaces for modular frontend plugins
4. **Separation of Concerns** - Decoupled CMS, API, and presentation layers
5. **Security & Privacy by Default** - Secure content management across all endpoints
6. **Spec-Driven Change Flow** - Structured change process for system architecture
7. **Observability Required** - Monitoring across admin, API, and frontend modules
8. **Incremental Hardening** - Continuous improvements to CMS security
9. **Testable Units Only** - All CMS functionality has clear success criteria
10. **Change Traceability** - Full traceability from PR to architectural principles
11. **Minimal Surface Area** - Lean headless architecture avoiding complexity
12. **Fast Feedback & Small Batches** - Rapid iterations for CMS improvements

## 📊 Project Status - Headless CMS Implementation

### ✅ **Completed Milestones**
- **Backend CMS API**: Complete data models, public/admin endpoints
- **Admin Interface**: Portfolio management, content CRUD operations
- **Modular Architecture**: Plugin-style frontend component system
- **Documentation**: Comprehensive architecture and implementation guides
- **Data Models**: Portfolio, skills, projects, testimonials, experiences
- **API Integration**: Frontend services with fallback mechanisms

### 🔄 **Current Development Phase**
- **System Testing**: End-to-end content flow validation
- **Performance Optimization**: API response times and caching
- **Additional Modules**: Blog system, e-commerce integration preparation

### � **Next Phase: Multi-Frontend Expansion**
- **Landing Page Builder**: Dynamic page creation system
- **Blog Module**: Article management with categories and tags  
- **E-commerce Module**: Product catalog and order management
- **Analytics Dashboard**: Cross-platform performance tracking

### Architecture Status
- **🏗️ Headless CMS Core**: Production-ready
- **🔌 Plugin System**: Functional and documented
- **📊 Admin Interface**: Complete with portfolio management
- **🌐 Frontend Modules**: React components with API integration
- **📚 Documentation**: Comprehensive technical specifications

## 🤝 Contributing to the Headless CMS

We welcome contributions to expand our modular CMS architecture! Please follow our governance framework:

1. **Read Architecture**: Start with [HEADLESS_CMS_ARCHITECTURE.md](HEADLESS_CMS_ARCHITECTURE.md)
2. **Understand Governance**: Review [CONSTITUTION.md](CONSTITUTION.md)
3. **Choose Module**: Backend API, admin interface, or frontend modules
4. **Follow Patterns**: Use established patterns for new content types
5. **Test Integration**: Ensure end-to-end content flow works
6. **Document Changes**: Update relevant architecture documentation

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
### Development Workflow

#### Adding New Content Types
```bash
# 1. Define data model
# Edit: backend/models/portfolio_models.py

# 2. Create database migration
cd backend
alembic revision --autogenerate -m "Add new content type"
alembic upgrade head

# 3. Add API endpoints
# Edit: backend/routers/public_portfolio.py
# Edit: backend/routers/portfolio_admin.py

# 4. Create admin interface
# Add components to: components/portfolio/
# Update: app/portfolio/page.tsx

# 5. Create frontend components
# Add to: Frontend/components/
# Update: Frontend/services/portfolioAPI.js
```

#### Adding New Frontend Modules
```bash
# 1. Create module structure
mkdir Frontend/NewModule
cd Frontend/NewModule

# 2. Set up API integration
cp ../services/portfolioAPI.js services/newModuleAPI.js
# Customize API endpoints

# 3. Create components
mkdir components
# Build React components

# 4. Configure routing  
# Add routes to App.jsx or create separate router

# 5. Test integration
npm start
# Verify API connectivity and data flow
```

## 🚀 Deployment Architecture

### Production Setup
- **Backend API**: Deploy FastAPI to cloud platform (AWS, GCP, Azure)
- **Admin Interface**: Deploy Next.js to Vercel or similar platform  
- **Frontend Modules**: Deploy independently to CDN or hosting platform
- **Database**: Managed PostgreSQL service

### Environment Configuration
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret-key
AI_PROVIDER_API_KEY=your-ai-key

# Admin Interface (.env.local)  
NEXTAUTH_SECRET=your-nextauth-secret
NEXT_PUBLIC_API_URL=https://your-api-domain.com
DATABASE_URL=your-database-url

# Frontend Modules (.env.local)
REACT_APP_API_URL=https://your-api-domain.com
```

## 📈 Monitoring & Analytics

### Headless CMS Metrics
- **Content Creation Rate**: New content items per day/week
- **API Performance**: Response times across public/admin endpoints
- **Frontend Module Usage**: Traffic distribution across connected sites
- **Admin Interface Activity**: Content management operations

### Cross-Platform Analytics
- **Multi-Frontend Tracking**: Unified analytics across all connected sites
- **Content Performance**: Which content performs best across platforms
- **User Journey Analysis**: From content creation to public consumption
- **System Health**: API uptime, database performance, frontend availability

## 📞 Support & Community

### Headless CMS Resources
- **Architecture Guide**: [HEADLESS_CMS_ARCHITECTURE.md](HEADLESS_CMS_ARCHITECTURE.md)
- **API Documentation**: `/backend/routers/` for endpoint specifications
- **Component Library**: [components.md](components.md) for UI components
- **Backend Catalog**: [backend_api_catalog.md](backend_api_catalog.md)

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/Ryangcastillo/CMS/issues) for bugs and features
- **Discussions**: [GitHub Discussions](https://github.com/Ryangcastillo/CMS/discussions) for architecture questions
- **Documentation**: Check architecture documentation for technical details
- **Examples**: See `/Frontend` folder for implementation patterns

### Contributing Guidelines
- **New Content Types**: Follow data model → API → admin → frontend pattern
- **Frontend Modules**: Use established API integration patterns
- **Documentation**: Update architecture docs for significant changes
- **Testing**: Ensure end-to-end content flow from admin to public site

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏷️ Project Metadata

**Project Type**: Headless Content Management System  
**Architecture**: API-First with Modular Frontend Architecture  
**Version**: 2.0.0 - Headless CMS Implementation  
**Last Updated**: 2025-01-XX  
**Status**: ✅ Production-Ready Core + Expanding Module Ecosystem  

**Technology Stack**: FastAPI (Backend) + Next.js (Admin) + React (Frontends) + PostgreSQL  
**Governance Framework**: Constitution + Architecture Documentation + Component Specifications  

### Quick Navigation
**Architecture**: [Headless CMS Architecture](HEADLESS_CMS_ARCHITECTURE.md) | [Component Library](components.md)  
**Governance**: [Constitution](CONSTITUTION.md) | [Specifications](SPECIFY.md)  
**APIs**: [Backend Catalog](backend_api_catalog.md) | [OpenAPI Docs](http://localhost:8000/docs)  
**Development**: [Development Setup](#quick-start---headless-cms-setup) | [Contributing Guidelines](#contributing-to-the-headless-cms)
