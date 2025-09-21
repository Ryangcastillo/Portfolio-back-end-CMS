#!/bin/bash
# Complete End-to-End Test Orchestrator
# Runs comprehensive tests for the entire CMS system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test and track results
run_test_suite() {
    local test_name="$1"
    local test_command="$2"
    local required="${3:-true}"
    
    print_status "Running $test_name..."
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command"; then
        print_success "$test_name completed successfully"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        if [ "$required" = "true" ]; then
            print_error "$test_name failed (required)"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 1
        else
            print_warning "$test_name failed (optional)"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 0
        fi
    fi
}

# Function to check if services are running
check_services() {
    print_status "Checking required services..."
    
    # Check if backend is running
    if curl -s http://localhost:8000/docs >/dev/null 2>&1; then
        print_success "Backend API is running on port 8000"
        BACKEND_RUNNING=true
    else
        print_warning "Backend API not running on port 8000"
        BACKEND_RUNNING=false
    fi
    
    # Check if frontend is running
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend is running on port 3000"
        FRONTEND_RUNNING=true
    else
        print_warning "Frontend not running on port 3000"
        FRONTEND_RUNNING=false
    fi
}

# Function to start services if needed
start_services() {
    print_status "Starting services if needed..."
    
    # Start backend if not running
    if [ "$BACKEND_RUNNING" = false ]; then
        print_status "Starting backend service..."
        cd "$PROJECT_ROOT/backend"
        
        if [ -d "venv" ]; then
            source venv/bin/activate
            nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
            BACKEND_PID=$!
            echo $BACKEND_PID > ../logs/backend.pid
            print_success "Backend started with PID $BACKEND_PID"
            sleep 5  # Give it time to start
        else
            print_error "Python virtual environment not found"
            return 1
        fi
    fi
    
    # Start frontend if not running
    if [ "$FRONTEND_RUNNING" = false ]; then
        print_status "Starting frontend service..."
        cd "$PROJECT_ROOT"
        
        if [ -f "package.json" ]; then
            nohup npm run dev > logs/frontend.log 2>&1 &
            FRONTEND_PID=$!
            echo $FRONTEND_PID > logs/frontend.pid
            print_success "Frontend started with PID $FRONTEND_PID"
            sleep 10  # Give it time to start
        else
            print_error "Frontend package.json not found"
            return 1
        fi
    fi
}

# Function to stop services
cleanup_services() {
    print_status "Cleaning up services..."
    
    if [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
        BACKEND_PID=$(cat "$PROJECT_ROOT/logs/backend.pid")
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            print_success "Backend service stopped"
        fi
        rm -f "$PROJECT_ROOT/logs/backend.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat "$PROJECT_ROOT/logs/frontend.pid")
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            print_success "Frontend service stopped"
        fi
        rm -f "$PROJECT_ROOT/logs/frontend.pid"
    fi
}

# Function to run dependency tests
test_dependencies() {
    print_status "Testing dependency management system..."
    run_test_suite "Dependency System Tests" "$SCRIPT_DIR/test-dependency-system.sh" true
}

# Function to run backend API tests
test_backend_api() {
    print_status "Testing backend API endpoints..."
    
    if [ "$BACKEND_RUNNING" = true ] || [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
        # Install required Python packages for testing
        cd "$PROJECT_ROOT/backend"
        source venv/bin/activate
        pip install httpx pytest-asyncio >/dev/null 2>&1 || true
        
        run_test_suite "Backend Content Flow Tests" "python3 $SCRIPT_DIR/test-content-flow.py" true
    else
        print_warning "Backend not running, skipping API tests"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to run frontend tests
test_frontend() {
    print_status "Testing frontend components and UI..."
    
    if [ "$FRONTEND_RUNNING" = true ] || [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
        cd "$PROJECT_ROOT"
        
        # Check if playwright is installed
        if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
            run_test_suite "Frontend Component Tests" "node $SCRIPT_DIR/test-frontend-flow.js" false
        else
            print_warning "Playwright not found, installing..."
            npm install playwright >/dev/null 2>&1 || true
            npx playwright install >/dev/null 2>&1 || true
            run_test_suite "Frontend Component Tests" "node $SCRIPT_DIR/test-frontend-flow.js" false
        fi
    else
        print_warning "Frontend not running, skipping UI tests"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to run integration tests
test_integration() {
    print_status "Testing system integration..."
    
    if [ "$BACKEND_RUNNING" = true ] && [ "$FRONTEND_RUNNING" = true ]; then
        # Test API-Frontend integration
        print_status "Testing API-Frontend integration..."
        
        # Simple integration test
        if curl -s http://localhost:3000 >/dev/null && curl -s http://localhost:8000/docs >/dev/null; then
            print_success "Basic integration test passed"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            print_error "Basic integration test failed"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        
    else
        print_warning "Both services not running, skipping integration tests"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
    fi
}

# Function to generate comprehensive test report
generate_test_report() {
    print_status "Generating comprehensive test report..."
    
    local report_file="$PROJECT_ROOT/reports/e2e_test_report_$(date +%Y%m%d_%H%M%S).md"
    mkdir -p "$PROJECT_ROOT/reports"
    
    cat > "$report_file" << EOF
# End-to-End Test Report

**Generated:** $(date)
**Total Duration:** $(date -d@$SECONDS -u +%H:%M:%S)

## Summary
- **Total Tests:** $TOTAL_TESTS
- **Passed:** $PASSED_TESTS  
- **Failed:** $FAILED_TESTS
- **Success Rate:** $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%

## Test Results

### ✅ Dependency Management
- Dependency system validation
- Script functionality
- Configuration validation

### 🔧 Backend API Testing
- Content CRUD operations
- Authentication flow
- AI integration
- Dashboard endpoints

### 🎨 Frontend Testing  
- Component rendering
- Navigation functionality
- Responsive design
- Performance metrics

### 🔗 Integration Testing
- API-Frontend communication
- Service connectivity
- End-to-end workflows

## System Status
- **Backend API:** $([ "$BACKEND_RUNNING" = true ] && echo "✅ Running" || echo "❌ Not Running")
- **Frontend UI:** $([ "$FRONTEND_RUNNING" = true ] && echo "✅ Running" || echo "❌ Not Running")

## Recommendations
$(if [ $FAILED_TESTS -eq 0 ]; then
    echo "- ✅ System is fully operational and ready for production"
    echo "- Consider setting up automated testing in CI/CD pipeline"
    echo "- Monitor system performance in production environment"
else
    echo "- ❌ Address failed tests before deploying to production" 
    echo "- Review error logs for detailed failure information"
    echo "- Run individual test suites for focused debugging"
fi)

## Next Steps
- Set up continuous integration with these tests
- Schedule regular health checks
- Monitor system performance metrics
- Plan for future enhancements based on test coverage

---
*Report generated by automated E2E testing suite*
EOF

    print_success "Test report generated: $report_file"
}

# Main execution function
main() {
    print_status "🚀 Starting Comprehensive End-to-End Test Suite"
    echo "Testing complete CMS system: Dependencies → Backend → Frontend → Integration"
    echo "=" * 80
    
    # Create logs directory
    mkdir -p "$PROJECT_ROOT/logs"
    
    # Record start time
    START_TIME=$(date +%s)
    
    # Check current service status
    check_services
    
    # Start services if needed (optional)
    if [ "${1:-}" = "--start-services" ]; then
        start_services
    fi
    
    # Run test suites
    echo ""
    print_status "Running test suites..."
    
    # 1. Test dependency management
    test_dependencies
    
    # 2. Test backend API
    test_backend_api
    
    # 3. Test frontend
    test_frontend
    
    # 4. Test integration
    test_integration
    
    # Calculate duration
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    # Generate test report
    generate_test_report
    
    # Print final summary
    echo ""
    echo "=" * 80
    print_status "FINAL TEST RESULTS"
    echo "=" * 80
    echo "Total Tests: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    echo "Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"
    echo "Duration: $(date -d@$DURATION -u +%H:%M:%S)"
    echo "=" * 80
    
    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "🎉 ALL TESTS PASSED! CMS system is fully operational."
        echo ""
        echo "✅ Content flow working correctly"
        echo "✅ Dependencies properly managed"  
        echo "✅ Frontend components functional"
        echo "✅ Backend API responding"
        echo "✅ Integration layer working"
        echo ""
        print_success "System ready for production deployment!"
    else
        print_error "❌ Some tests failed. System needs attention before production deployment."
        echo ""
        echo "Please review:"
        echo "- Individual test outputs for specific failures"
        echo "- Generated test report for detailed analysis"
        echo "- Service logs in the logs/ directory"
    fi
    
    # Cleanup if we started services
    if [ "${1:-}" = "--start-services" ]; then
        cleanup_services
    fi
    
    # Return appropriate exit code
    if [ $FAILED_TESTS -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Trap to ensure cleanup on exit
trap cleanup_services EXIT

# Execute main function
main "$@"