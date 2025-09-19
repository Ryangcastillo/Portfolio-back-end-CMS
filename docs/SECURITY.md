# Security Policy

> Vulnerability reporting, security practices, and protection guidelines for Stitch CMS

**Reference**: CONST-P9 (Security & Privacy), CONST-P8 (Quality Assurance)

## 🛡️ Our Security Commitment

Security is a top priority for Stitch CMS. We are committed to protecting our users, contributors, and the integrity of the platform through comprehensive security practices, responsible disclosure, and continuous improvement.

## 📊 Supported Versions

We provide security updates for the following versions of Stitch CMS:

| Version | Supported          | Support Period |
| ------- | ------------------ | -------------- |
| 1.x.x   | ✅ Full Support    | Current        |
| 0.9.x   | ⚠️ Limited Support | 6 months       |
| 0.8.x   | ❌ No Support     | End of Life    |

**Note**: We recommend always running the latest stable version to ensure you have the most recent security updates.

## 🚨 Reporting Security Vulnerabilities

### 📧 How to Report

**DO NOT** report security vulnerabilities through public GitHub issues, discussions, or pull requests.

Instead, please report security vulnerabilities through one of these secure channels:

#### **Preferred Method: GitHub Security Advisories**
1. Navigate to the [Security tab](https://github.com/stitchcms/stitch-cms/security) of our repository
2. Click "Report a vulnerability"
3. Fill out the vulnerability details using our template
4. Submit the advisory

#### **Alternative Methods**
- **Email**: security@stitchcms.dev
- **GPG Encrypted Email**: Use our [public GPG key](./security/pgp-key.asc) for sensitive reports
- **Private Disclosure Platforms**: We also monitor HackerOne and other responsible disclosure platforms

### 📝 What to Include

When reporting a security vulnerability, please include:

#### **Essential Information**
- **Vulnerability Type**: SQL injection, XSS, authentication bypass, etc.
- **Affected Components**: Specific files, endpoints, or features affected
- **Severity Assessment**: Your assessment of the impact and exploitability
- **Environment Details**: Version, configuration, deployment type
- **Steps to Reproduce**: Detailed reproduction steps
- **Proof of Concept**: Code, screenshots, or demo (if safe to share)

#### **Additional Context**
- **Impact Analysis**: Who could be affected and how
- **Potential Fixes**: Suggested remediation approaches (optional)
- **Timeline**: Any urgent timeline considerations
- **Discoverer Information**: How you'd like to be credited (if applicable)

#### **Security Report Template**
```markdown
# Security Vulnerability Report

## Summary
Brief description of the vulnerability

## Vulnerability Details
- **Type**: [e.g., SQL Injection, XSS, CSRF, etc.]
- **Severity**: [Critical/High/Medium/Low]
- **Affected Component**: [Specific file/endpoint/feature]
- **Version**: [Affected version(s)]

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Proof of Concept
[Include safe demonstration if possible]

## Impact
Description of potential impact if exploited

## Suggested Fix
[Optional: Your suggestions for remediation]

## Reporter Information
- Name: [How you'd like to be credited]
- Email: [Contact information]
- Disclosure Timeline: [Any timing considerations]
```

### ⏱️ Response Timeline

We commit to the following response timeline for security reports:

| Timeline | Action |
| -------- | ------ |
| **24 hours** | Initial acknowledgment of report |
| **72 hours** | Preliminary assessment and severity classification |
| **1 week** | Detailed investigation and reproduction |
| **2 weeks** | Fix development and testing |
| **30 days** | Public disclosure (coordinated with reporter) |

**Note**: Timeline may vary based on complexity. We'll keep you informed throughout the process.

## 🔒 Security Practices

### 🏗️ Secure Development

#### **Code Security Standards**
Following our governance framework (CONST-P9):

```python
# Input validation example
from pydantic import BaseModel, validator
from typing import Optional
import re

class ContentRequest(BaseModel):
    title: str
    content: str
    author_id: int
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title too long')
        # Prevent XSS in title
        if re.search(r'<script|javascript:|data:|vbscript:', v, re.IGNORECASE):
            raise ValueError('Invalid characters in title')
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v):
        # Content sanitization handled by frontend
        # but we validate length and basic structure
        if len(v) > 100000:  # 100KB limit
            raise ValueError('Content too large')
        return v
```

#### **Authentication Security**
```python
# JWT token security
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Strong password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Use strong secret key and algorithm
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm="HS256"
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

#### **Database Security**
```python
# SQL injection prevention
from sqlalchemy.orm import Session
from sqlalchemy import text

# ✅ Safe: Using SQLAlchemy ORM
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ✅ Safe: Parameterized queries
def get_content_by_status(db: Session, status: str, limit: int):
    return db.execute(
        text("SELECT * FROM content WHERE status = :status LIMIT :limit"),
        {"status": status, "limit": limit}
    ).fetchall()

# ❌ Dangerous: Never do this
# query = f"SELECT * FROM users WHERE email = '{email}'"  # SQL injection risk
```

### 🌐 Frontend Security

#### **XSS Prevention**
```typescript
// Content sanitization
import DOMPurify from 'dompurify';

// Sanitize HTML content before rendering
const sanitizeHTML = (dirty: string): string => {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
    ALLOWED_ATTR: ['href', 'title'],
    ALLOW_DATA_ATTR: false
  });
};

// React component with safe rendering
const ContentDisplay = ({ content }: { content: string }) => {
  const sanitizedContent = sanitizeHTML(content);
  
  return (
    <div 
      dangerouslySetInnerHTML={{ __html: sanitizedContent }}
      className="content-display"
    />
  );
};
```

#### **CSRF Protection**
```typescript
// CSRF token handling
const API_BASE = process.env.NEXT_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true, // Include cookies
});

// Request interceptor to add CSRF token
api.interceptors.request.use((config) => {
  const csrfToken = getCsrfToken(); // Get from meta tag or cookie
  if (csrfToken) {
    config.headers['X-CSRF-Token'] = csrfToken;
  }
  return config;
});

// Get CSRF token from DOM
const getCsrfToken = (): string | null => {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : null;
};
```

### 🔐 Infrastructure Security

#### **Environment Variables**
```bash
# .env.example - Template for environment variables
# Never commit actual .env files!

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/stitch_cms"

# Authentication
SECRET_KEY="your-super-secret-key-change-this"
JWT_SECRET="your-jwt-secret-change-this"
ACCESS_TOKEN_EXPIRE_MINUTES=15

# API Keys (never commit real keys)
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"

# Security
ALLOWED_HOSTS="localhost,127.0.0.1"
CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
```

#### **Docker Security**
```dockerfile
# Security-hardened Dockerfile
FROM node:18-alpine AS base

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Set security headers
LABEL security.no-new-privileges=true

# Install dependencies as root
COPY package*.json ./
RUN npm ci --only=production

# Copy application files
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

# Expose only necessary port
EXPOSE 3000

# Use exec form for proper signal handling
CMD ["npm", "start"]
```

### 🛡️ Runtime Security

#### **Rate Limiting**
```python
# FastAPI rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    # Login logic with rate limiting
    pass

@app.get("/api/content")
@limiter.limit("100/minute")  # Higher limit for content access
async def get_content(request: Request, db: Session = Depends(get_db)):
    # Content retrieval logic
    pass
```

#### **Input Validation**
```python
# Comprehensive input validation
from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional
import re

class CreateUserRequest(BaseModel):
    email: str
    password: str
    username: str
    role: str = "user"
    
    @validator('email')
    def validate_email(cls, v):
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_regex.match(v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be 3-20 characters')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username contains invalid characters')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['user', 'editor', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v
```

## 🔍 Security Monitoring

### 📊 Logging and Monitoring

#### **Security Event Logging**
```python
# Security event logging
import logging
from datetime import datetime
from typing import Optional

security_logger = logging.getLogger('security')

def log_security_event(
    event_type: str,
    user_id: Optional[int],
    ip_address: str,
    details: dict,
    severity: str = 'INFO'
):
    """Log security-related events for monitoring"""
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': ip_address,
        'details': details,
        'severity': severity
    }
    
    security_logger.info(f"SECURITY_EVENT: {log_data}")

# Usage examples
@app.post("/api/auth/login")
async def login(request: Request, credentials: UserLogin):
    ip = get_client_ip(request)
    
    try:
        user = authenticate_user(credentials)
        log_security_event(
            'login_success', 
            user.id, 
            ip, 
            {'username': credentials.username}
        )
        return {"token": create_token(user)}
    except AuthenticationError:
        log_security_event(
            'login_failure',
            None,
            ip,
            {'username': credentials.username},
            severity='WARNING'
        )
        raise HTTPException(401, "Invalid credentials")
```

#### **Automated Security Monitoring**
```python
# Monitor for suspicious patterns
from collections import defaultdict
from datetime import datetime, timedelta

class SecurityMonitor:
    def __init__(self):
        self.failed_logins = defaultdict(list)
        self.rate_limits = defaultdict(list)
    
    def check_brute_force(self, ip_address: str) -> bool:
        """Check for brute force attack patterns"""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=10)
        
        # Clean old entries
        self.failed_logins[ip_address] = [
            t for t in self.failed_logins[ip_address] if t > cutoff
        ]
        
        # Check if too many failures
        if len(self.failed_logins[ip_address]) >= 5:
            log_security_event(
                'brute_force_detected',
                None,
                ip_address,
                {'failed_attempts': len(self.failed_logins[ip_address])},
                severity='CRITICAL'
            )
            return True
        
        return False
    
    def record_failed_login(self, ip_address: str):
        """Record a failed login attempt"""
        self.failed_logins[ip_address].append(datetime.utcnow())

monitor = SecurityMonitor()
```

### 🔔 Alert System

#### **Security Alert Configuration**
```python
# Security alerting system
import smtplib
from email.mime.text import MIMEText
from typing import List

class SecurityAlerts:
    def __init__(self, smtp_config: dict, alert_emails: List[str]):
        self.smtp_config = smtp_config
        self.alert_emails = alert_emails
    
    def send_security_alert(
        self,
        title: str,
        description: str,
        severity: str,
        details: dict
    ):
        """Send security alert to team"""
        subject = f"[SECURITY-{severity}] {title}"
        
        body = f"""
        Security Alert: {title}
        Severity: {severity}
        Time: {datetime.utcnow().isoformat()}
        
        Description:
        {description}
        
        Details:
        {json.dumps(details, indent=2)}
        
        Please investigate immediately if severity is HIGH or CRITICAL.
        """
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.smtp_config['from']
        msg['To'] = ', '.join(self.alert_emails)
        
        try:
            with smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Failed to send security alert: {e}")
```

## 🧪 Security Testing

### 🔒 Automated Security Testing

#### **SAST (Static Application Security Testing)**
```yaml
# .github/workflows/security.yml
name: Security Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit (Python)
        run: |
          pip install bandit
          bandit -r backend/ -f json -o bandit-report.json
      
      - name: Run ESLint Security (JavaScript)
        run: |
          npm install eslint-plugin-security
          npx eslint --ext .js,.jsx,.ts,.tsx --config .eslintrc.security.js .
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
```

#### **Dependency Security Scanning**
```yaml
# .github/workflows/dependency-check.yml
name: Dependency Security Check

on:
  schedule:
    - cron: '0 2 * * 1' # Weekly on Monday
  push:
    paths:
      - 'requirements.txt'
      - 'package.json'
      - 'package-lock.json'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Python Security Check
        run: |
          pip install safety
          safety check -r requirements.txt --json --output safety-report.json
      
      - name: Node.js Security Check
        run: |
          npm audit --audit-level moderate --json > npm-audit.json
      
      - name: Upload Security Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            safety-report.json
            npm-audit.json
```

### 🧪 Manual Security Testing

#### **Security Testing Checklist**
```markdown
# Security Testing Checklist

## Authentication & Authorization
- [ ] Test password strength requirements
- [ ] Verify JWT token expiration and refresh
- [ ] Test role-based access controls
- [ ] Verify session management
- [ ] Test account lockout mechanisms

## Input Validation
- [ ] Test SQL injection on all inputs
- [ ] Test XSS on all user inputs
- [ ] Test file upload security
- [ ] Verify input length limits
- [ ] Test special character handling

## API Security
- [ ] Test rate limiting on all endpoints
- [ ] Verify CORS configuration
- [ ] Test API authentication
- [ ] Check for information disclosure
- [ ] Test error message security

## Infrastructure
- [ ] Verify HTTPS configuration
- [ ] Test security headers
- [ ] Check for exposed debug information
- [ ] Verify database security
- [ ] Test backup security
```

## 📋 Incident Response

### 🚨 Security Incident Response Plan

#### **Immediate Response (0-1 hours)**
1. **Assess the Situation**
   - Determine scope and severity
   - Identify affected systems/users
   - Document initial findings

2. **Contain the Incident**
   - Isolate affected systems
   - Revoke compromised credentials
   - Block malicious IP addresses
   - Preserve evidence

3. **Notify Key Stakeholders**
   - Security team
   - System administrators
   - Project maintainers
   - Legal team (if required)

#### **Investigation Phase (1-24 hours)**
1. **Detailed Analysis**
   - Collect logs and evidence
   - Analyze attack vectors
   - Assess data exposure
   - Document timeline

2. **Communication**
   - Update stakeholders
   - Prepare user communications
   - Contact law enforcement (if needed)
   - Notify regulatory bodies (if required)

#### **Recovery Phase (1-7 days)**
1. **System Restoration**
   - Apply security patches
   - Update configurations
   - Restore from clean backups
   - Validate system integrity

2. **User Communication**
   - Notify affected users
   - Provide guidance
   - Reset credentials (if needed)
   - Update security documentation

#### **Post-Incident Review (1-2 weeks)**
1. **Lessons Learned**
   - Conduct thorough review
   - Identify improvement areas
   - Update procedures
   - Enhance monitoring

2. **Prevention Measures**
   - Implement additional controls
   - Update training materials
   - Revise security policies
   - Schedule follow-up assessments

## 📚 Security Resources

### 🎓 Training Materials

#### **For Developers**
- **OWASP Top 10**: Understanding common vulnerabilities
- **Secure Coding Practices**: Language-specific security guidelines
- **Threat Modeling**: Identifying potential attack vectors
- **Security Testing**: Automated and manual testing techniques

#### **For Operations**
- **Infrastructure Security**: Server hardening and monitoring
- **Incident Response**: Handling security breaches effectively
- **Compliance**: Meeting regulatory requirements
- **Business Continuity**: Maintaining operations during incidents

### 🔗 External Resources
- **[OWASP](https://owasp.org/)**: Web application security guidance
- **[CIS Controls](https://www.cisecurity.org/controls)**: Cybersecurity best practices
- **[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)**: Comprehensive security framework
- **[CVE Database](https://cve.mitre.org/)**: Known vulnerabilities database

## 📞 Emergency Contacts

### 🚨 Security Team Contacts
- **Security Lead**: security-lead@stitchcms.dev
- **Technical Lead**: tech-lead@stitchcms.dev
- **Operations**: ops@stitchcms.dev

### 📱 24/7 Emergency Response
- **PagerDuty**: [Integration details]
- **Slack**: #security-alerts channel
- **Phone Tree**: [Emergency contact list]

### 🏛️ External Resources
- **CERT**: [National CERT contact]
- **FBI Cyber Division**: [If applicable]
- **Legal Counsel**: [Law firm contact]

---

## 📝 Security Policy Updates

This security policy is reviewed and updated quarterly or after significant security incidents. All changes are:

1. **Reviewed** by the security team
2. **Approved** by project maintainers
3. **Communicated** to all contributors
4. **Documented** in the change log

**Last Review**: 2025-09-20  
**Next Review**: 2025-12-20  
**Version**: 1.0.0

---

## Metadata
**Document Type**: Security Policy and Guidelines  
**Version**: 1.0.0  
**Last Updated**: 2025-09-20  
**Review Schedule**: Quarterly  
**Owner**: Security Team  

**Change Log**:
- 2025-09-20: Initial security policy with comprehensive coverage of practices, monitoring, and incident response

---

*This security policy is designed to protect the Stitch CMS project, its users, and contributors. If you have questions or suggestions for improvement, please contact the security team.*