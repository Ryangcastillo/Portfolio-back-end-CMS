# GitHub AI Agent Instructions: CMS System Startup & Testing

**Target**: Background AI Agent (GitHub Copilot)  
**Objective**: Execute todo list to start CMS system and validate functionality  
**Prerequisites**: Complete Python 3.9 compatibility fixes first  

---

## 🎯 **Mission Overview**

Execute the following todo sequence to restore and test the CMS system:

```
✅ Create run plan
⏳ Start backend server  
⏳ Start Next.js frontend
⏳ Start modular Frontend (Vite)
⏳ Smoke tests
⏳ Collect results & cleanup
```

**Critical Note**: Backend startup is currently **BLOCKED** by Python 3.9 compatibility issues. Complete Phase 0 fixes before proceeding to Phase 1.

---

## 🔧 **Phase 0: MANDATORY Prerequisites (Complete First)**

### **Step 0.1: Fix Python 3.9 Compatibility Issues**

**Problem**: Backend uses Python 3.10+ union syntax (`str | None`) incompatible with Python 3.9

**Required Actions**:

1. **Fix Union Type Syntax in `/backend/security.py`**:
   ```bash
   # Navigate to file
   code backend/security.py
   
   # Find and replace lines 134 and 148:
   # FROM: rt: RefreshToken | None = res.scalar_one_or_none()
   # TO:   rt: Optional[RefreshToken] = res.scalar_one_or_none()
   
   # Add import at top if missing:
   from typing import Optional, Union
   ```

2. **Fix F-String Syntax in `/backend/services/notification_service.py`**:
   ```bash
   # Navigate to file  
   code backend/services/notification_service.py
   
   # Find line 216 and fix quote escaping:
   # FROM: f'<div class="status status-{rsvp.status}"><strong>Your RSVP Status:</strong> {rsvp.status.title()}</div>'
   # TO:   f"<div class=\"status status-{rsvp.status}\"><strong>Your RSVP Status:</strong> {rsvp.status.title()}</div>"
   ```

3. **Comprehensive Backend Audit** (Find all union syntax):
   ```bash
   # Search for additional union type issues
   grep -r "str \| \|int \| \|Optional\[.*\] \|" backend/ --include="*.py" --exclude-dir=venv
   
   # Fix any additional matches by replacing:
   # Type | None  →  Optional[Type]
   # Type | Other →  Union[Type, Other]
   ```

4. **Validate Python Syntax**:
   ```bash
   # Test all backend files compile
   find backend/ -name "*.py" -not -path "*/venv/*" -exec python -m py_compile {} \;
   
   # Expected: No output = success
   # If errors: Fix syntax and repeat
   ```

---

## 📋 **Phase 1: Execute Todo Sequence**

### **Todo 1: ✅ Create Run Plan** 
**Status**: COMPLETED  
**Action**: No action needed - plan already exists  

---

### **Todo 2: 🎯 Start Backend Server**

**Current Status**: BLOCKED until Phase 0 complete  
**Priority**: CRITICAL  

**Instructions**:
```bash
# 1. Navigate to project root
cd /Users/ryan/Desktop/CMS-vercel/CMS/CMS

# 2. Activate Python virtual environment
source backend/venv/bin/activate

# 3. Start FastAPI server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# Expected Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [PID]
# INFO:     Started server process [PID]
# INFO:     Waiting for application startup.
```

**Success Criteria**:
- ✅ Server starts without ImportError or SyntaxError
- ✅ No Python compatibility warnings
- ✅ Process runs in background successfully

**Failure Handling**:
```bash
# If startup fails:
# 1. Check error message for specific file/line
# 2. Return to Phase 0 and fix additional syntax issues
# 3. Re-run syntax validation
# 4. Retry server startup
```

**Validation**:
```bash
# In new terminal, test health endpoint
curl http://localhost:8000/health

# Expected Response:
# {"status": "healthy", "version": "1.0.0"}

# Test API documentation access
curl -I http://localhost:8000/docs
# Expected: HTTP/1.1 200 OK
```

---

### **Todo 3: 🎯 Start Next.js Frontend**

**Prerequisites**: Backend must be running successfully  
**Priority**: HIGH  

**Instructions**:
```bash
# 1. Open new terminal window/tab
# 2. Navigate to project root
cd /Users/ryan/Desktop/CMS-vercel/CMS/CMS

# 3. Install dependencies (if not already done)
npm install

# 4. Start Next.js development server
npm run dev

# Expected Output:
# ▲ Next.js 14.2.32
# - Local:        http://localhost:3000
# - Ready in 2.1s
```

**Success Criteria**:
- ✅ Server starts on port 3000
- ✅ No TypeScript compilation errors
- ✅ No React component errors
- ✅ Frontend accessible in browser

**Validation**:
```bash
# Test frontend accessibility
curl -I http://localhost:3000

# Expected Response:
# HTTP/1.1 200 OK
# Content-Type: text/html

# Check for JavaScript console errors in browser:
# 1. Open http://localhost:3000 in browser
# 2. Open Developer Tools (F12)
# 3. Check Console tab for errors
# 4. Look for API connectivity issues
```

---

### **Todo 4: 🎯 Start Modular Frontend (Vite)**

**Prerequisites**: Backend running, Next.js running  
**Priority**: MEDIUM (Optional for basic functionality)  

**Instructions**:
```bash
# 1. Open new terminal window/tab
# 2. Navigate to Frontend directory
cd /Users/ryan/Desktop/CMS-vercel/CMS/CMS/Frontend

# 3. Install dependencies (if not already done)
npm install

# 4. Start Vite development server
npm run dev

# Expected Output:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose
```

**Success Criteria**:
- ✅ Server starts on port 5173
- ✅ No build errors
- ✅ Modular components accessible

**Port Conflict Resolution**:
```bash
# If port 5173 is occupied:
npm run dev -- --port 5174

# Or modify package.json:
# "dev": "vite --port 5174"
```

---

### **Todo 5: 🎯 Smoke Tests**

**Prerequisites**: All servers running successfully  
**Priority**: HIGH  

**Test Sequence**:

#### **Test 5.1: Backend Health Checks**
```bash
# Health endpoint
curl -f http://localhost:8000/health
# Expected: {"status": "healthy", "version": "1.0.0"}

# API documentation
curl -I http://localhost:8000/docs  
# Expected: HTTP/1.1 200 OK

# OpenAPI schema
curl -f http://localhost:8000/openapi.json > /dev/null
# Expected: No error (file downloads successfully)
```

#### **Test 5.2: Frontend Accessibility**
```bash
# Next.js frontend
curl -I http://localhost:3000
# Expected: HTTP/1.1 200 OK, Content-Type: text/html

# Vite frontend (if running)
curl -I http://localhost:5173  
# Expected: HTTP/1.1 200 OK, Content-Type: text/html
```

#### **Test 5.3: API Integration**
```bash
# Test API endpoint accessibility from frontend
curl -f http://localhost:3000/api/health 2>/dev/null
# May fail if proxy not configured - check browser console instead
```

#### **Test 5.4: Database Connection**
```bash
# Check if backend connects to database (look for startup logs)
# In backend terminal, look for messages like:
# "Database connection established"
# "Tables created/migrated successfully"
```

**Browser Integration Tests**:
1. **Frontend Load Test**:
   - Open http://localhost:3000 in browser
   - Verify page loads without errors
   - Check Developer Console for JavaScript errors
   - Look for network errors to backend API

2. **API Connectivity Test**:
   - In browser console, run: `fetch('/api/health').then(r => r.json()).then(console.log)`
   - Expected: Health status response or CORS error (indicates backend reachable)

---

### **Todo 6: 🎯 Collect Results & Cleanup**

**Priority**: LOW (Organizational)  

**Results Collection**:
```bash
# 1. Create results summary
cat > test_results_$(date +%Y%m%d_%H%M%S).md << 'EOF'
# CMS System Startup Test Results

**Date**: $(date)
**Objective**: Validate complete system startup

## Results Summary

### Backend (FastAPI)
- [ ] Server startup: SUCCESS/FAILED
- [ ] Health endpoint: SUCCESS/FAILED  
- [ ] API docs accessible: SUCCESS/FAILED
- [ ] Database connection: SUCCESS/FAILED

### Frontend (Next.js)
- [ ] Server startup: SUCCESS/FAILED
- [ ] Page load: SUCCESS/FAILED
- [ ] Console errors: NONE/PRESENT
- [ ] API connectivity: SUCCESS/FAILED

### Frontend (Vite) - Optional
- [ ] Server startup: SUCCESS/FAILED
- [ ] Components load: SUCCESS/FAILED

### Integration
- [ ] Frontend-Backend communication: SUCCESS/FAILED
- [ ] Authentication flow: SUCCESS/FAILED (if tested)
- [ ] CORS configuration: SUCCESS/FAILED

## Issues Found
[List any issues discovered during testing]

## Next Steps
[Recommendations for fixes or improvements]

EOF
```

**Log Collection**:
```bash
# Capture server logs
# Backend logs (from terminal output)
# Frontend logs (from terminal output and browser console)
# Error logs (if any failures occurred)
```

**Cleanup Process**:
```bash
# 1. Stop all servers gracefully
# In each terminal running servers:
# Press Ctrl+C to stop servers

# 2. Deactivate Python virtual environment
deactivate

# 3. Document any issues for future resolution
# Update COMPREHENSIVE_SYSTEM_REFACTORING_REPORT.md with findings
```

---

## 🚨 **Error Handling & Troubleshooting**

### **Common Issues & Solutions**

1. **Backend Won't Start**:
   - **Cause**: Python 3.9 compatibility issues not fully resolved
   - **Solution**: Return to Phase 0, complete syntax fixes
   - **Debug**: Check error message for specific file/line

2. **Frontend Can't Connect to Backend**:
   - **Cause**: CORS issues or backend not running
   - **Solution**: Verify backend health endpoint, check CORS config
   - **Debug**: Check browser Developer Console Network tab

3. **Port Conflicts**:
   - **Solution**: Use different ports with `--port` flag
   - **Update**: Modify API client baseURL if backend port changes

4. **Database Connection Issues**:
   - **Cause**: PostgreSQL not running or connection config wrong
   - **Solution**: Start PostgreSQL service, verify connection string
   - **Debug**: Check backend startup logs for database errors

### **Success Indicators**

✅ **Complete Success**:
- All servers start without errors
- Health endpoints return 200 status
- Frontend loads in browser without console errors
- API integration works (can be tested via browser console)

✅ **Partial Success** (Acceptable):
- Backend and primary frontend (Next.js) working
- Vite frontend optional
- Minor warnings acceptable if core functionality works

❌ **Failure** (Requires fixes):
- Backend fails to start (Python syntax issues)
- Frontend shows console errors indicating API problems
- Health endpoints not accessible

---

## 📊 **Success Metrics & Reporting**

### **Key Performance Indicators**

1. **Backend Startup**: < 10 seconds
2. **Frontend Startup**: < 15 seconds  
3. **Health Check Response**: < 500ms
4. **Page Load Time**: < 3 seconds
5. **Console Errors**: Zero critical errors

### **Report Template**

```markdown
# CMS System Test Execution Report

**Executed By**: GitHub AI Agent
**Date**: [DATE]
**Duration**: [TIME] 

## Executive Summary
- Overall Status: ✅ SUCCESS / ❌ FAILED / ⚠️ PARTIAL
- Critical Issues: [COUNT]
- Recommendations: [PRIORITY ACTIONS]

## Detailed Results
[Use template from Todo 6]

## Agent Recommendations
[Specific next steps for human developer]
```

---

## 🤖 **AI Agent Execution Notes**

**Agent Capabilities Required**:
- File editing (Python syntax fixes)
- Terminal command execution
- HTTP request testing (curl)
- Error log analysis
- Report generation

**Execution Order** (MANDATORY):
1. **Must complete Phase 0 first** - Backend will not start otherwise
2. Execute todos 2-6 in sequence
3. Stop on critical failures, report issues
4. Collect comprehensive results
5. Provide human-readable summary

**Human Handoff Points**:
- If Phase 0 syntax fixes reveal additional issues
- If database connection problems occur
- If fundamental architecture changes needed
- Upon completion (for result review)

---

*This instruction set enables systematic CMS system restoration and validation by a GitHub background AI agent.*