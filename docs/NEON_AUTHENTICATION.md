# Neon Authentication Guide

This document describes the Neon authentication system implemented in the Portfolio CMS backend.

## Overview

The system has been updated to:
- **Disable traditional admin login** via username/password
- **Enable Neon-based authentication** for administrative access

## Configuration

### Environment Variables

Add these environment variables to enable Neon authentication:

```bash
# Required for Neon authentication
NEON_DATABASE_URL=postgresql://user:password@hostname/database?sslmode=require
NEON_API_KEY=your_neon_api_key_here
NEON_PROJECT_ID=your_neon_project_id
NEON_BRANCH=main
USE_NEON_AUTH=true

# Optional: Override default database URL
DATABASE_URL=postgresql://user:password@localhost/stitch_cms
```

## Authentication Methods

### 1. Regular User Authentication (Unchanged)

**Endpoint**: `POST /api/auth/token`

```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=editor_user&password=password123"
```

**Response**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_token": "MZk..."
}
```

**Note**: Users with `role="admin"` will receive HTTP 403 Forbidden.

### 2. Neon Authentication (New)

**Endpoint**: `POST /api/auth/neon-auth`

```bash
curl -X POST "http://localhost:8000/api/auth/neon-auth" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "your-neon-project-id",
    "api_key": "your-neon-api-key",
    "branch": "main"
  }'
```

**Response**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "neon_project_id": "your-neon-project-id",
  "neon_branch": "main"
}
```

## How It Works

### Admin Login Disabled

1. When a user with `role="admin"` attempts to login via `/api/auth/token`
2. The system returns HTTP 403 with message: "Admin login has been disabled. Please use alternative authentication method."
3. Regular users (editor, viewer) continue to work normally

### Neon Authentication Process

1. **Validation**: System validates Neon credentials against Neon Console API
2. **User Creation**: If valid, creates/updates user with username pattern `neon_{project_id}`
3. **Admin Role**: Grants admin role to Neon-authenticated users
4. **Enhanced JWT**: Token includes additional claims:
   - `neon_project_id`: The authenticated Neon project
   - `neon_branch`: The database branch used
   - `auth_method`: Set to "neon"

### Database Connection

When `USE_NEON_AUTH=true` and `NEON_DATABASE_URL` is provided:
- System automatically uses Neon database for connections
- Falls back to regular `DATABASE_URL` if Neon is not configured

## Security Considerations

### Benefits
- **Centralized Access**: Admin access controlled through Neon project credentials
- **Dynamic Users**: Automatic user provisioning for valid Neon projects
- **Audit Trail**: Clear authentication method tracking in JWT tokens
- **Separation**: Regular users unaffected by admin authentication changes

### Best Practices
- Store Neon API keys securely (environment variables, secrets management)
- Use specific Neon branches for different environments
- Monitor authentication logs for security events
- Regularly rotate Neon API keys

## Error Handling

### Common Errors

**Admin Login Blocked**:
```json
{
  "error": {
    "message": "Admin login has been disabled. Please use alternative authentication method.",
    "status": 403
  }
}
```

**Invalid Neon Credentials**:
```json
{
  "error": {
    "message": "Neon authentication failed: Neon API returned status 401",
    "status": 401
  }
}
```

**Network Issues**:
```json
{
  "error": {
    "message": "Neon authentication failed: Failed to connect to Neon API: Connection timeout",
    "status": 401
  }
}
```

## Migration Guide

### For Existing Admin Users

1. **Before**: Admin users logged in with username/password
2. **After**: Admin users must use Neon authentication
3. **Action Required**: 
   - Obtain Neon project credentials
   - Use `/api/auth/neon-auth` endpoint instead of `/api/auth/token`

### For Regular Users

No changes required. Continue using `/api/auth/token` as before.

## Development & Testing

### Local Development

For local development without real Neon credentials:

```bash
# Use SQLite for development
DATABASE_URL=sqlite+aiosqlite:///./stitch_cms.db
USE_NEON_AUTH=false
```

### Testing Neon Authentication

```bash
# Test with dummy credentials (will fail validation)
curl -X POST "http://localhost:8000/api/auth/neon-auth" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "test-project",
    "api_key": "test-key",
    "branch": "main"
  }'
```

Expected response: HTTP 401 with Neon API error.

## API Documentation

The Neon authentication endpoint is automatically included in the OpenAPI documentation at:
- Interactive docs: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Look for the `/api/auth/neon-auth` endpoint in the Authentication section.