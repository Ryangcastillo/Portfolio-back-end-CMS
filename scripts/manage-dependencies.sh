#!/bin/bash
# Comprehensive Dependency Management for Headless CMS
# Manages both backend (Python) and frontend (Node.js) dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
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
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/Frontend"

print_status "Headless CMS Dependency Management"
print_status "Project Root: $PROJECT_ROOT"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to manage backend dependencies
manage_backend_deps() {
    print_status "Managing Backend Python Dependencies..."
    
    if [ ! -d "$BACKEND_DIR" ]; then
        print_error "Backend directory not found: $BACKEND_DIR"
        return 1
    fi
    
    cd "$BACKEND_DIR"
    
    # Ensure virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv --upgrade-deps
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install/upgrade pip-tools and uv
    print_status "Installing dependency management tools..."
    pip install --upgrade pip-tools uv
    
    # Compile requirements if .in files exist
    if [ -f "requirements.in" ]; then
        print_status "Compiling production requirements..."
        pip-compile requirements.in --upgrade --resolver=backtracking
    fi
    
    if [ -f "requirements-dev.in" ]; then
        print_status "Compiling development requirements..."
        pip-compile requirements-dev.in --upgrade --resolver=backtracking
    fi
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_status "Installing production dependencies..."
        pip-sync requirements.txt
    fi
    
    if [ "$1" == "dev" ] && [ -f "requirements-dev.txt" ]; then
        print_status "Installing development dependencies..."
        pip install -r requirements-dev.txt
    fi
    
    # Check for outdated packages
    print_status "Checking for outdated packages..."
    pip list --outdated || true
    
    print_success "Backend dependencies updated successfully!"
}

# Function to manage frontend dependencies  
manage_frontend_deps() {
    print_status "Managing Frontend Node.js Dependencies..."
    
    # Check main frontend (Admin Interface)
    if [ -d "$PROJECT_ROOT" ]; then
        cd "$PROJECT_ROOT"
        if [ -f "package.json" ]; then
            print_status "Updating main frontend (Admin Interface) dependencies..."
            
            if command_exists pnpm; then
                print_status "Using pnpm..."
                pnpm update
                pnpm audit --fix || true
            elif command_exists npm; then
                print_status "Using npm..."
                npm update
                npm audit fix || true
            else
                print_warning "Neither npm nor pnpm found!"
                return 1
            fi
        fi
    fi
    
    # Check modular frontend
    if [ -d "$FRONTEND_DIR" ]; then
        cd "$FRONTEND_DIR"
        if [ -f "package.json" ]; then
            print_status "Updating modular frontend dependencies..."
            
            if command_exists npm; then
                npm update
                npm audit fix || true
            else
                print_warning "npm not found for Frontend module!"
            fi
        else
            print_warning "No package.json found in Frontend directory"
        fi
    fi
    
    print_success "Frontend dependencies updated successfully!"
}

# Function to check dependency security
check_security() {
    print_status "Running security checks..."
    
    # Backend security check
    if [ -d "$BACKEND_DIR/venv" ]; then
        cd "$BACKEND_DIR"
        source venv/bin/activate
        
        if pip show bandit >/dev/null 2>&1; then
            print_status "Running Python security audit (bandit)..."
            bandit -r . -f json -o security-report.json || true
        fi
        
        # Safety check for known vulnerabilities
        if command_exists safety; then
            print_status "Checking for known vulnerabilities..."
            safety check || true
        fi
    fi
    
    # Frontend security check
    cd "$PROJECT_ROOT"
    if [ -f "package.json" ]; then
        if command_exists pnpm; then
            pnpm audit || true
        elif command_exists npm; then
            npm audit || true
        fi
    fi
    
    print_success "Security checks completed!"
}

# Function to generate dependency reports
generate_reports() {
    print_status "Generating dependency reports..."
    
    REPORTS_DIR="$PROJECT_ROOT/reports"
    mkdir -p "$REPORTS_DIR"
    
    # Backend report
    if [ -d "$BACKEND_DIR/venv" ]; then
        cd "$BACKEND_DIR"
        source venv/bin/activate
        
        print_status "Generating Python dependency report..."
        pip freeze > "$REPORTS_DIR/python-dependencies.txt"
        pip list --format=json > "$REPORTS_DIR/python-dependencies.json"
        
        # Outdated packages
        pip list --outdated --format=json > "$REPORTS_DIR/python-outdated.json" || true
    fi
    
    # Frontend report
    cd "$PROJECT_ROOT"
    if [ -f "package.json" ]; then
        print_status "Generating Node.js dependency report..."
        
        if command_exists pnpm; then
            pnpm list --json > "$REPORTS_DIR/nodejs-dependencies.json" 2>/dev/null || true
            pnpm outdated --json > "$REPORTS_DIR/nodejs-outdated.json" 2>/dev/null || true
        elif command_exists npm; then
            npm list --json > "$REPORTS_DIR/nodejs-dependencies.json" 2>/dev/null || true
            npm outdated --json > "$REPORTS_DIR/nodejs-outdated.json" 2>/dev/null || true
        fi
    fi
    
    print_success "Dependency reports generated in $REPORTS_DIR"
}

# Main execution
case "${1:-all}" in
    "backend"|"python")
        manage_backend_deps "${2:-}"
        ;;
    "frontend"|"node"|"nodejs")  
        manage_frontend_deps
        ;;
    "security")
        check_security
        ;;
    "reports")
        generate_reports
        ;;
    "dev")
        manage_backend_deps "dev"
        manage_frontend_deps
        ;;
    "all")
        manage_backend_deps
        manage_frontend_deps
        check_security
        generate_reports
        ;;
    *)
        echo "Usage: $0 [backend|frontend|security|reports|dev|all]"
        echo ""
        echo "Commands:"
        echo "  backend     Update Python backend dependencies"
        echo "  frontend    Update Node.js frontend dependencies" 
        echo "  security    Run security audits"
        echo "  reports     Generate dependency reports"
        echo "  dev         Update all dependencies including dev tools"
        echo "  all         Run everything (default)"
        echo ""
        echo "Examples:"
        echo "  $0 backend     # Update only backend"
        echo "  $0 dev         # Update everything including dev dependencies"
        echo "  $0 security    # Run security audits only"
        exit 1
        ;;
esac

print_success "Dependency management completed successfully!"