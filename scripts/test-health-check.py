#!/usr/bin/env python3
"""
Health Check Endpoint Tests
Validates TASK-008 implementation
"""

import asyncio
import httpx
import json
import time
from typing import Dict, Any

# Test configuration
API_BASE_URL = "http://localhost:8000"

class HealthCheckTester:
    def __init__(self):
        self.test_results = []
        self.client = None

    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })

    async def test_quick_health_endpoint(self):
        """Test the quick health check endpoint"""
        try:
            response = await self.client.get("/health/quick")
            if response.status_code == 200:
                data = response.json()
                required_fields = ["status", "timestamp", "version"]
                
                if all(field in data for field in required_fields):
                    self.log_result("Quick Health Endpoint", True, "All required fields present")
                else:
                    self.log_result("Quick Health Endpoint", False, "Missing required fields")
            else:
                self.log_result("Quick Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Quick Health Endpoint", False, f"Error: {str(e)}")

    async def test_comprehensive_health_endpoint(self):
        """Test the comprehensive health check endpoint"""
        try:
            response = await self.client.get("/health")
            
            # Accept both 200 (healthy/degraded) and 503 (unhealthy)
            if response.status_code in [200, 503]:
                if response.status_code == 503:
                    # For 503, data is in 'detail' field
                    data = response.json().get("detail", {})
                else:
                    data = response.json()
                
                required_fields = ["status", "timestamp", "version", "checks"]
                
                if all(field in data for field in required_fields):
                    checks = data.get("checks", {})
                    required_checks = ["database", "external_services", "resources", "response_time_ms"]
                    
                    if all(check in checks for check in required_checks):
                        self.log_result("Comprehensive Health Endpoint", True, "All checks present")
                        
                        # Validate database check structure
                        db_check = checks.get("database", {})
                        if "status" in db_check:
                            self.log_result("Database Health Check", True, f"Status: {db_check['status']}")
                        else:
                            self.log_result("Database Health Check", False, "Missing status field")
                        
                        # Validate resources check
                        resources = checks.get("resources", {})
                        resource_fields = ["cpu_percent", "memory_percent", "memory_used_mb", "memory_total_mb"]
                        if all(field in resources for field in resource_fields):
                            self.log_result("Resource Monitoring", True, f"CPU: {resources['cpu_percent']}%, Memory: {resources['memory_percent']}%")
                        else:
                            self.log_result("Resource Monitoring", False, "Missing resource fields")
                            
                    else:
                        self.log_result("Comprehensive Health Endpoint", False, "Missing required checks")
                else:
                    self.log_result("Comprehensive Health Endpoint", False, "Missing required fields")
            else:
                self.log_result("Comprehensive Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Comprehensive Health Endpoint", False, f"Error: {str(e)}")

    async def test_database_health_endpoint(self):
        """Test the database-specific health check endpoint"""
        try:
            response = await self.client.get("/health/database")
            
            # Accept both 200 (healthy) and 503 (unhealthy)
            if response.status_code in [200, 503]:
                if response.status_code == 503:
                    data = response.json().get("detail", {})
                else:
                    data = response.json()
                
                if "status" in data:
                    self.log_result("Database Health Endpoint", True, f"Status: {data['status']}")
                else:
                    self.log_result("Database Health Endpoint", False, "Missing status field")
            else:
                self.log_result("Database Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Database Health Endpoint", False, f"Error: {str(e)}")

    async def test_resources_health_endpoint(self):
        """Test the resources-specific health check endpoint"""
        try:
            response = await self.client.get("/health/resources")
            
            # Accept 200, 503 status codes
            if response.status_code in [200, 503]:
                if response.status_code == 503:
                    data = response.json().get("detail", {})
                else:
                    data = response.json()
                
                required_fields = ["status", "resources", "timestamp"]
                if all(field in data for field in required_fields):
                    self.log_result("Resources Health Endpoint", True, "All fields present")
                else:
                    self.log_result("Resources Health Endpoint", False, "Missing required fields")
            else:
                self.log_result("Resources Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Resources Health Endpoint", False, f"Error: {str(e)}")

    async def test_status_codes(self):
        """Test that appropriate HTTP status codes are returned"""
        try:
            response = await self.client.get("/health")
            
            if response.status_code in [200, 503]:
                self.log_result("HTTP Status Codes", True, f"Appropriate status code: {response.status_code}")
            else:
                self.log_result("HTTP Status Codes", False, f"Unexpected status code: {response.status_code}")
        except Exception as e:
            self.log_result("HTTP Status Codes", False, f"Error: {str(e)}")

    async def run_all_tests(self):
        """Run all health check tests"""
        print("🏥 Health Check Endpoints Test Suite")
        print("Testing TASK-008 implementation")
        print("=" * 50)
        
        try:
            # Create HTTP client
            timeout = httpx.Timeout(30.0)  # 30 second timeout
            self.client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=timeout)
            
            # Run all tests
            await self.test_quick_health_endpoint()
            await self.test_comprehensive_health_endpoint()
            await self.test_database_health_endpoint()
            await self.test_resources_health_endpoint()
            await self.test_status_codes()
            
        finally:
            if self.client:
                await self.client.aclose()
        
        # Print summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        
        if passed_tests == total_tests:
            print("\n✅ ALL HEALTH CHECK TESTS PASSED!")
            print("TASK-008 implementation is working correctly.")
            return True
        else:
            print("\n❌ Some health check tests failed.")
            print("Please review the implementation.")
            return False

async def main():
    """Main test execution"""
    print("Starting Health Check Tests...")
    print("Make sure the backend server is running on http://localhost:8000")
    
    tester = HealthCheckTester()
    success = await tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)