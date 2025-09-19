# Repository Rules & Contribution Guidelines

> Comprehensive guidelines for contributing to Stitch CMS, following constitutional principles

**Reference**: CONST-P10 (Change Traceability), CONST-P6 (Spec-Driven Change Flow)

## 🎯 Overview

These rules define how to manage the Git repository that houses your project. They help ensure a clean history, consistent collaboration and integration with AI‑driven workflows like Spec Kit. All contributions must follow these guidelines and align with our [Constitutional Principles](docs/governance/CONSTITUTION.md).

---

## Version control

1. **Initialize Git immediately** – Commit the initial project scaffolding (including specs, plans and docs) on day one. Enable branch protection on the main branch.
2. **Feature branches** – Create a new branch for every feature, bug fix or documentation change using a clear naming convention such as `feature/<short‑description>`, `bugfix/<issue‑id>` or `docs/<topic>`.
3. **Semantic commit messages** – Write concise messages following Conventional Commits:
    - **Prefix** / **Purpose**
    - `feat` – Adds a new feature
    - `fix` – Bug fix
    - `docs` – Documentation only
    - `style` – Formatting, missing semi colons, etc.
    - `refactor` – Code changes that do not alter functionality
4. **Keep commits small** – Commit at logical breakpoints (after completing a task or small sub‑feature) to simplify reviews and enable easy reverts.
5. **Tag releases** – Use Semantic Versioning to tag significant milestones (e.g., `v1.2.0`). Include release notes summarizing changes and linking to the relevant spec and plan documents.

---

## Pull requests

- **Always open a PR** – Never merge directly into `main`. Open a pull request from your feature branch.
- **Describe the change** – Provide a high‑level summary, list linked issues or tasks, and reference the relevant spec/plan sections. Include screenshots or logs when helpful.
- **Link to tasks** – If you use Spec Kit, link the pull request to the `/tasks` item(s) that this PR implements. This creates traceability from specification → plan → tasks → code.
- **Request review early** – Seek feedback as soon as you have a working slice. Encourage reviewers to compare against the specification and technical plan.
- **Require checks** – Configure branch protection so that all tests, linters and security scanners must pass before merging. Use GitHub Actions to run unit tests, lint checks and style checks automatically.
- **Small, focused PRs** – Avoid large PRs. Each pull request should implement a small set of tasks to ease review and reduce merge conflicts.

---

## Branch workflow

- **Main branch** – Always represents the latest stable release. Protected; only reviewed, passing pull requests may be merged.
- **Develop branch** (optional) – Use if your team prefers GitFlow. Feature branches merge into `develop`; release branches are cut from `develop` and merged back into `develop` and `main`.
- **Hotfix branch** – For urgent fixes to production; branch from `main`, fix, test and merge back into both `main` and `develop`.
- **Release branch** – When preparing a new version, create `release/<version>` from `develop`. Perform final testing and documentation updates here before merging back.

---

## Repository‑level instructions for Copilot and other agents

- **Define instructions in `.github/copilot.md`** – Provide repository‑wide guidance on naming conventions, architecture patterns and prohibited practices. Copilot will use these instructions to generate more relevant suggestions.
- **Keep instructions up to date** – Whenever project rules evolve (e.g., new ESLint rules or changes in architecture), update the Copilot instructions and commit them so that agents always have current context.
- **Exclude sensitive content** – Use `.github/copilot-ignore.txt` or similar mechanisms to exclude secrets or proprietary code from Copilot's context.

---

## Integrating Spec Kit

Spec Kit promotes spec‑driven development and ties documentation to implementation:

1. **Initialize** – Run `uvx --from git+https://github.com/github/spec-kit.git specify init <project-name>` to bootstrap a new project.
2. **Constitution** – Run `/constitution` to create governing principles for code quality, testing, UX and performance. Commit this file (typically under `specs/constitution.md`) to version control.
3. **Specification** – Use `/specify` to describe what you are building stored under `specs/` and treat it as the source of truth.
4. **Plan** – Use `/plan` to produce a technical plan with architecture and constraints under `specs/plan.md` and keep it updated as requirements evolve.
5. **Tasks** – Use `/tasks` to generate a list of actionable tasks. Commit the resulting document. Store it. Create issues or Kanban cards for each task and link them to the spec and plan.
6. **Implementation** – Implement tasks sequentially or in parallel. Commit code with references to the corresponding tasks and update the spec/plan if assumptions change.
7. **By versioning the constitution, spec, plan and tasks alongside your code, you preserve knowledge and ensure AI agents always work from the latest requirements.**

---

## Security and compliance

- **Secret scanning** – Enable GitHub's secret scanning and push protection to prevent committing credentials.
- **Dependency management** – Use Dependabot or Renovate to monitor dependency updates and vulnerabilities. Keep your `package.json` and lockfiles current.
- **Code scanning** – Enable GitHub Advanced Security (or an equivalent scanner) to detect vulnerable patterns. Configure it to run on every pull request.

Following these repository rules ensures a clean, auditable history and smooth collaboration between humans and AI agents.

---

## Metadata
**Document Type**: Repository Guidelines  
**Version**: 1.0.0  
**Last Updated**: 2025-09-20  
**Review Schedule**: Quarterly  
**Owner**: Development Team  

**Change Log**:
- 2025-09-20: Initial repository rules and contribution guidelines creation

---

*These repository rules ensure quality, consistency, and alignment with our constitutional principles while maintaining development velocity and team collaboration.*