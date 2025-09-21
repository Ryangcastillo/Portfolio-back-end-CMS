# Pattern Library

> Collection of mastered code patterns, examples, and best practices for Stitch CMS development

**Reference**: CONST-P4 (Separation of Concerns), CONST-P9 (Testable Units), CONST-P11 (Minimal Surface Area)

## 🎯 Purpose

This library captures proven code patterns, architectural decisions, and implementation examples as they are learned and mastered. It serves as a personal reference and accelerates future development.

---

## 📊 Pattern Mastery Status

### Frontend Patterns
| Pattern | Status | Last Updated | Usage Count | Confidence |
|---------|--------|--------------|-------------|------------|
| React Components | Learning | 2025-09-20 | 0 | Beginner |
| Next.js Routing | Learning | 2025-09-20 | 0 | Beginner |
| Form Handling | Future | N/A | 0 | None |
| State Management | Future | N/A | 0 | None |
| Error Boundaries | Future | N/A | 0 | None |

### Backend Patterns
| Pattern | Status | Last Updated | Usage Count | Confidence |
|---------|--------|--------------|-------------|------------|
| FastAPI Routes | Learning | 2025-09-20 | 0 | Beginner |
| Database Models | Learning | 2025-09-20 | 0 | Beginner |
| Authentication | Future | N/A | 0 | None |
| API Documentation | Future | N/A | 0 | None |
| Error Handling | Future | N/A | 0 | None |

### Development Patterns
| Pattern | Status | Last Updated | Usage Count | Confidence |
|---------|--------|--------------|-------------|------------|
| Git Workflows | Learning | 2025-09-20 | 1 | Beginner |
| Testing Patterns | Future | N/A | 0 | None |
| Documentation | Learning | 2025-09-20 | 1 | Beginner |
| CI/CD | Future | N/A | 0 | None |

**Status Legend**:
- **Mastered**: Confident, can teach others
- **Practiced**: Comfortable, few mistakes
- **Learning**: Understanding basics, needs practice
- **Future**: Not yet attempted

---

## 🏗️ Architectural Patterns

### PATTERN-001: Layered Architecture
**Status**: Learning  
**Category**: Architecture  
**Confidence**: Beginner

**Description**:
Clean separation between frontend, API, business logic, and data layers.

**Implementation Example**:
```
frontend/          # Next.js React components
├── app/           # App Router pages
├── components/    # Reusable UI components
└── lib/           # Client-side utilities

backend/           # FastAPI application
├── routers/       # API route handlers
├── models/        # Database models
├── services/      # Business logic
└── database.py    # Data layer configuration
```

**When to Use**:
- Building scalable web applications
- Need clear separation of concerns
- Multiple developers working on project

**Benefits**:
- Easy to maintain and extend
- Clear boundaries between responsibilities
- Testable components

**Common Mistakes**:
- Mixing business logic in route handlers
- Direct database access from components
- Coupling frontend to specific backend structure

**Related Patterns**:
- API-First Development (PATTERN-002)
- Service Layer Pattern (PATTERN-TBD)

---

### PATTERN-002: API-First Development
**Status**: Learning  
**Category**: Architecture  
**Confidence**: Beginner

**Description**:
Design and implement API endpoints before building frontend components.

**Implementation Example**:
```python
# 1. Define the API endpoint first
@router.post("/content", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    current_user: User = Depends(get_current_user)
) -> ContentResponse:
    """Create new content item."""
    pass

# 2. Then build the frontend component
function ContentForm() {
  const handleSubmit = async (data) => {
    await fetch('/api/v1/content', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  };
}
```

**When to Use**:
- Building applications with multiple frontends
- Need API documentation before implementation
- Want to enable automation and integration

**Benefits**:
- Clear contracts between frontend/backend
- Enables parallel development
- Self-documenting through OpenAPI

**Related Patterns**:
- Layered Architecture (PATTERN-001)
- Documentation-Driven Development (PATTERN-TBD)

---

## 🧩 Component Patterns

### PATTERN-003: Form Handling Pattern
**Status**: Future  
**Category**: Frontend  
**Confidence**: None

*This pattern will be documented when implemented*

**Placeholder Structure**:
```typescript
// Form validation pattern
// Error handling pattern  
// Loading states pattern
// Success feedback pattern
```

---

## 📝 Code Snippets Library

### React Components

#### Basic Page Component
```typescript
// Pattern: Standard page layout
import { PageLayout } from '@/components/layouts/PageLayout';

export default function ExamplePage() {
  return (
    <PageLayout title="Example Page">
      <div className="space-y-6">
        {/* Page content */}
      </div>
    </PageLayout>
  );
}
```

#### Loading Component
```typescript
// Pattern: Loading states
export function LoadingSpinner({ size = 'default' }: { size?: 'sm' | 'default' | 'lg' }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    default: 'w-6 h-6',
    lg: 'w-8 h-8'
  };
  
  return (
    <div className={cn(
      'animate-spin rounded-full border-2 border-muted border-t-primary',
      sizeClasses[size]
    )} />
  );
}
```

### FastAPI Routes

#### Standard CRUD Endpoint
```python
# Pattern: RESTful API endpoint
@router.get("/{id}", response_model=ResourceResponse)
async def get_resource(
    id: int,
    current_user: User = Depends(get_current_user)
) -> ResourceResponse:
    """Get a specific resource by ID."""
    resource = await service.get_resource(id, current_user.id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
```

#### Error Handling Pattern
```python
# Pattern: Consistent error responses
try:
    result = await service.perform_operation(data)
    return {"success": True, "data": result}
except ValidationError as e:
    raise HTTPException(status_code=422, detail=str(e))
except PermissionError as e:
    raise HTTPException(status_code=403, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 🔧 Development Patterns

### Git Workflow
```bash
# Pattern: Feature development workflow
git checkout -b feature/new-feature
git add -A
git commit -m "feat: implement new feature

- Add component structure
- Implement basic functionality
- Add tests and documentation

Refs: TASK-123"
git push -u origin feature/new-feature
# Create PR with proper description
```

### Documentation Pattern
```markdown
# Pattern: Component documentation
## ComponentName

Brief description of what this component does.

### Props
- `prop1` (string): Description of prop1
- `prop2` (boolean, optional): Description of prop2

### Usage
```tsx
<ComponentName prop1="value" prop2={true} />
```

### Notes
- Important implementation details
- Known limitations
- Related components
```

---

## 📚 Learning Path

### Next Patterns to Master
1. **Form Validation** - React Hook Form + Zod
2. **Error Boundaries** - Graceful error handling
3. **Authentication Flow** - Login/logout/session management
4. **Testing Patterns** - Unit and integration tests
5. **Performance Optimization** - Memoization, lazy loading

### Pattern Learning Process
1. **Study Examples** - Find 3-5 implementations online
2. **Understand Why** - Learn the problem this pattern solves
3. **Implement Small** - Create minimal working example
4. **Document Learning** - Add to this library with notes
5. **Practice Variations** - Try different approaches
6. **Teach Back** - Explain pattern to AI agent or rubber duck

---

## 🔍 Pattern Analysis Template

```markdown
### PATTERN-XXX: [Pattern Name]
**Status**: [Future/Learning/Practiced/Mastered]
**Category**: [Frontend/Backend/Architecture/Testing/etc.]
**Confidence**: [None/Beginner/Intermediate/Advanced]
**Last Used**: [Date]

**Problem Solved**:
[What issue does this pattern address?]

**Implementation**:
[Code example showing the pattern]

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
```

---

## Metadata
**Document Type**: Pattern Library  
**Version**: 1.0.0  
**Last Updated**: 2025-09-20  
**Review Schedule**: Bi-weekly  
**Owner**: Learning Developer  

**Change Log**:
- 2025-09-20: Initial pattern library structure with first architectural patterns

---

*This pattern library grows with your development experience, capturing proven solutions and implementation strategies for future reference.*