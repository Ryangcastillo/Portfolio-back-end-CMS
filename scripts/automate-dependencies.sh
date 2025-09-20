#!/bin/bash
# Automated Dependency Update and Security Scanner
# Runs scheduled updates and security checks for the Headless CMS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[AUTOMATION]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

print_status "Starting automated dependency management..."

# Create reports directory with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORTS_DIR="$PROJECT_ROOT/reports/automated_$TIMESTAMP"
mkdir -p "$REPORTS_DIR"

# Function to send notification (placeholder for future integration)
send_notification() {
    local message="$1"
    local level="${2:-info}"
    
    echo "[$level] $message" >> "$REPORTS_DIR/notifications.log"
    print_status "Notification: $message"
}

# Function to check for critical vulnerabilities
check_critical_vulnerabilities() {
    print_status "Scanning for critical vulnerabilities..."
    
    local critical_found=false
    
    # Backend vulnerability check
    if [ -d "$PROJECT_ROOT/backend/venv" ]; then
        cd "$PROJECT_ROOT/backend"
        source venv/bin/activate
        
        if command -v safety >/dev/null 2>&1; then
            if ! safety check --json --output "$REPORTS_DIR/backend_vulnerabilities.json"; then
                critical_found=true
                print_error "Critical vulnerabilities found in backend dependencies!"
                send_notification "Critical backend vulnerabilities detected" "critical"
            fi
        fi
    fi
    
    # Frontend vulnerability check
    cd "$PROJECT_ROOT"
    if [ -f "package.json" ]; then
        if npm audit --audit-level high --json > "$REPORTS_DIR/frontend_vulnerabilities.json"; then
            print_success "No high-severity frontend vulnerabilities found"
        else
            critical_found=true
            print_error "High-severity vulnerabilities found in frontend dependencies!"
            send_notification "Critical frontend vulnerabilities detected" "critical"
        fi
    fi
    
    if [ "$critical_found" = true ]; then
        send_notification "URGENT: Critical vulnerabilities require immediate attention" "critical"
        return 1
    fi
    
    return 0
}

# Function to update dependencies with safety checks
safe_update_dependencies() {
    print_status "Performing safe dependency updates..."
    
    # Create backup of current dependency files
    backup_dir="$REPORTS_DIR/backup"
    mkdir -p "$backup_dir"
    
    # Backup backend requirements
    if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
        cp "$PROJECT_ROOT/backend/requirements.txt" "$backup_dir/"
    fi
    if [ -f "$PROJECT_ROOT/backend/requirements-dev.txt" ]; then
        cp "$PROJECT_ROOT/backend/requirements-dev.txt" "$backup_dir/"
    fi
    
    # Backup frontend package files
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        cp "$PROJECT_ROOT/package.json" "$backup_dir/"
        cp "$PROJECT_ROOT/package-lock.json" "$backup_dir/" 2>/dev/null || true
        cp "$PROJECT_ROOT/pnpm-lock.yaml" "$backup_dir/" 2>/dev/null || true
    fi
    
    # Run dependency updates
    if ! "$SCRIPT_DIR/manage-dependencies.sh" all > "$REPORTS_DIR/update_log.txt" 2>&1; then
        print_error "Dependency update failed! Restoring backup..."
        
        # Restore from backup
        cp "$backup_dir"/* "$PROJECT_ROOT/" 2>/dev/null || true
        cp "$backup_dir"/requirements*.txt "$PROJECT_ROOT/backend/" 2>/dev/null || true
        
        send_notification "Dependency update failed - backup restored" "error"
        return 1
    fi
    
    print_success "Dependencies updated successfully!"
    send_notification "All dependencies updated successfully" "success"
    return 0
}

# Function to generate comprehensive report
generate_comprehensive_report() {
    print_status "Generating comprehensive dependency report..."
    
    local report_file="$REPORTS_DIR/dependency_report.md"
    
    cat > "$report_file" << EOF
# Automated Dependency Management Report
Generated: $(date)

## Summary
- **Status**: $([ $? -eq 0 ] && echo "✅ Success" || echo "❌ Failed")
- **Timestamp**: $TIMESTAMP
- **Reports Directory**: $REPORTS_DIR

## Backend Dependencies
$(if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
    echo "### Current Python Dependencies"
    echo "\`\`\`"
    cat "$PROJECT_ROOT/backend/requirements.txt"
    echo "\`\`\`"
fi)

## Frontend Dependencies
$(if [ -f "$PROJECT_ROOT/package.json" ]; then
    echo "### Current Node.js Dependencies"
    echo "\`\`\`json"
    cat "$PROJECT_ROOT/package.json" | jq '.dependencies // {}'
    echo "\`\`\`"
fi)

## Security Status
$(if [ -f "$REPORTS_DIR/backend_vulnerabilities.json" ]; then
    echo "### Backend Vulnerabilities"
    echo "See: \`backend_vulnerabilities.json\`"
fi)

$(if [ -f "$REPORTS_DIR/frontend_vulnerabilities.json" ]; then
    echo "### Frontend Vulnerabilities"
    echo "See: \`frontend_vulnerabilities.json\`"
fi)

## Recommendations
- Review all dependency updates before deploying to production
- Run full test suite after dependency updates
- Monitor application performance post-update
- Schedule next automated scan for $(date -d '+1 week' '+%Y-%m-%d')

## Files Generated
$(find "$REPORTS_DIR" -type f -name "*.json" -o -name "*.txt" -o -name "*.log" | sed 's|.*/||' | sort)
EOF

    print_success "Comprehensive report generated: $report_file"
}

# Main execution flow
main() {
    print_status "Starting automated dependency management workflow..."
    
    # Step 1: Check for critical vulnerabilities first
    if ! check_critical_vulnerabilities; then
        print_error "Critical vulnerabilities found - stopping automated updates"
        send_notification "Automated updates halted due to critical vulnerabilities" "critical"
        exit 1
    fi
    
    # Step 2: Perform safe dependency updates
    if safe_update_dependencies; then
        # Step 3: Re-check vulnerabilities after updates
        print_status "Re-scanning for vulnerabilities after updates..."
        check_critical_vulnerabilities || print_warning "New vulnerabilities detected after update"
        
        # Step 4: Generate reports
        generate_comprehensive_report
        
        print_success "Automated dependency management completed successfully!"
        send_notification "Automated dependency management cycle completed" "success"
    else
        print_error "Automated dependency management failed"
        send_notification "Automated dependency management failed" "error"
        exit 1
    fi
}

# Execute main function
main "$@"