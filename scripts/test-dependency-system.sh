#!/bin/bash
# Comprehensive Dependency Management Test Suite
# Tests all aspects of the dependency management system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    print_status "Running test: $test_name"
    
    if eval "$test_command"; then
        print_success "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        print_error "$test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Test 1: Verify script files exist and are executable
test_script_files() {
    [ -x "$SCRIPT_DIR/manage-dependencies.sh" ] && 
    [ -x "$SCRIPT_DIR/automate-dependencies.sh" ] &&
    [ -f "$SCRIPT_DIR/dependency-config.ini" ]
}

# Test 2: Verify backend requirements files
test_backend_requirements() {
    [ -f "$PROJECT_ROOT/backend/requirements.in" ] &&
    [ -f "$PROJECT_ROOT/backend/requirements-dev.in" ] &&
    grep -q "fastapi" "$PROJECT_ROOT/backend/requirements.in" &&
    grep -q "pytest" "$PROJECT_ROOT/backend/requirements-dev.in"
}

# Test 3: Verify frontend package configuration
test_frontend_package() {
    [ -f "$PROJECT_ROOT/package.json" ] &&
    [ -f "$PROJECT_ROOT/Frontend/package.json" ] &&
    [ -f "$PROJECT_ROOT/Frontend/vite.config.js" ] &&
    [ -f "$PROJECT_ROOT/Frontend/.eslintrc.json" ]
}

# Test 4: Test dependency management script syntax
test_dependency_script_syntax() {
    bash -n "$SCRIPT_DIR/manage-dependencies.sh" &&
    bash -n "$SCRIPT_DIR/automate-dependencies.sh"
}

# Test 5: Test dependency management help command
test_dependency_help() {
    "$SCRIPT_DIR/manage-dependencies.sh" --help > /dev/null 2>&1 ||
    "$SCRIPT_DIR/manage-dependencies.sh" help > /dev/null 2>&1 ||
    "$SCRIPT_DIR/manage-dependencies.sh" > /dev/null 2>&1
}

# Test 6: Verify GitHub workflow exists
test_github_workflow() {
    [ -f "$PROJECT_ROOT/.github/workflows/dependency-management.yml" ]
}

# Test 7: Test Python environment creation (dry run)
test_python_env_creation() {
    if [ ! -d "$PROJECT_ROOT/backend/venv" ]; then
        cd "$PROJECT_ROOT/backend"
        python3 -m venv test_venv --upgrade-deps
        local result=$?
        rm -rf test_venv
        return $result
    else
        return 0  # Environment already exists
    fi
}

# Test 8: Verify documentation exists
test_documentation() {
    [ -f "$PROJECT_ROOT/docs/DEPENDENCY_MANAGEMENT.md" ] &&
    grep -q "dependency management" "$PROJECT_ROOT/docs/DEPENDENCY_MANAGEMENT.md"
}

# Test 9: Test configuration file parsing
test_config_parsing() {
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "
import configparser
config = configparser.ConfigParser()
config.read('$SCRIPT_DIR/dependency-config.ini')
assert 'backend' in config.sections()
assert 'frontend' in config.sections()
assert 'security' in config.sections()
"
    else
        # Basic text validation if Python not available
        grep -q "\[backend\]" "$SCRIPT_DIR/dependency-config.ini" &&
        grep -q "\[frontend\]" "$SCRIPT_DIR/dependency-config.ini" &&
        grep -q "\[security\]" "$SCRIPT_DIR/dependency-config.ini"
    fi
}

# Test 10: Verify Node.js compatibility
test_nodejs_compatibility() {
    if command -v node >/dev/null 2>&1; then
        cd "$PROJECT_ROOT"
        node -e "
const pkg = require('./package.json');
if (!pkg.dependencies || !pkg.devDependencies) {
    process.exit(1);
}
console.log('Package.json is valid');
"
    else
        print_warning "Node.js not available, skipping compatibility test"
        return 0
    fi
}

# Main test execution
main() {
    print_status "Starting Dependency Management Test Suite"
    print_status "Project Root: $PROJECT_ROOT"
    echo ""
    
    # Run all tests
    run_test "Script files exist and are executable" "test_script_files"
    run_test "Backend requirements files are valid" "test_backend_requirements"
    run_test "Frontend package configuration is complete" "test_frontend_package"
    run_test "Dependency scripts have valid syntax" "test_dependency_script_syntax"
    run_test "Dependency management help works" "test_dependency_help"
    run_test "GitHub workflow exists" "test_github_workflow"
    run_test "Python environment can be created" "test_python_env_creation"
    run_test "Documentation exists and is valid" "test_documentation"
    run_test "Configuration file can be parsed" "test_config_parsing"
    run_test "Node.js package compatibility" "test_nodejs_compatibility"
    
    # Print summary
    echo ""
    print_status "Test Results Summary:"
    echo "  Total Tests: $TESTS_RUN"
    echo "  Passed: $TESTS_PASSED"
    echo "  Failed: $TESTS_FAILED"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "All tests passed! Dependency management system is ready."
        
        echo ""
        print_status "Next steps:"
        echo "  1. Run: ./scripts/manage-dependencies.sh all"
        echo "  2. Test the system with: ./scripts/automate-dependencies.sh"
        echo "  3. Review reports in the generated reports directory"
        echo "  4. Set up automated scheduling (crontab or CI/CD)"
        
        return 0
    else
        print_error "Some tests failed. Please review and fix issues before using the system."
        return 1
    fi
}

# Execute main function
main "$@"