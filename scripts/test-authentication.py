#!/usr/bin/env python3
"""
Authentication System Test Suite
Tests admin login disabled and Neon authentication enabled
"""

import asyncio
import httpx
import json
import sys
from typing import Dict, Any

# Test configuration
API_BASE_URL = "http://localhost:8000"

class AuthenticationTester:
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

    async def test_admin_login_disabled(self):
        """Test that admin users cannot login via regular endpoint"""
        print("\n🔒 Testing Admin Login Disabled...")
        
        # First, register a test user
        try:
            user_data = {
                "email": "test_admin@example.com",
                "username": "test_admin_user",
                "password": "admin_test_123",
                "full_name": "Test Admin User"
            }
            
            response = await self.client.post("/api/auth/register", json=user_data)
            if response.status_code == 201:
                self.log_result("Admin User Registration", True, "Test admin user created")
                
                # Update user role to admin (this would normally be done via database)
                # For this test, we'll assume the user was manually set to admin role
                
                # Try to login with admin credentials
                login_data = {
                    "username": user_data["username"],
                    "password": user_data["password"]
                }
                
                login_response = await self.client.post(
                    "/api/auth/token", 
                    data=login_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                # Since we can't actually modify the user role in this test,
                # we'll test with the known admin user from previous tests
                admin_login_data = {
                    "username": "admin_user",  # From previous test setup
                    "password": "admin123"
                }
                
                admin_response = await self.client.post(
                    "/api/auth/token",
                    data=admin_login_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if admin_response.status_code == 403:
                    error_data = admin_response.json()
                    if "Admin login has been disabled" in error_data.get("error", {}).get("message", ""):
                        self.log_result("Admin Login Blocked", True, "Admin users correctly blocked from login")
                    else:
                        self.log_result("Admin Login Blocked", False, f"Wrong error message: {error_data}")
                else:
                    self.log_result("Admin Login Blocked", False, f"Expected 403, got {admin_response.status_code}")
                    
            else:
                self.log_result("Admin User Registration", False, f"Failed to create test user: {response.status_code}")
                
        except Exception as e:
            self.log_result("Admin Login Disabled Test", False, f"Error: {str(e)}")

    async def test_regular_user_login_works(self):
        """Test that regular users can still login normally"""
        print("\n👤 Testing Regular User Login...")
        
        try:
            # Test with regular user from previous tests
            login_data = {
                "username": "editor_user",
                "password": "editor123"
            }
            
            response = await self.client.post(
                "/api/auth/token",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                required_fields = ["access_token", "token_type", "expires_in", "refresh_token"]
                
                if all(field in token_data for field in required_fields):
                    self.log_result("Regular User Login", True, "Regular users can login successfully")
                else:
                    self.log_result("Regular User Login", False, "Missing token fields in response")
            else:
                self.log_result("Regular User Login", False, f"Login failed with status {response.status_code}")
                
        except Exception as e:
            self.log_result("Regular User Login Test", False, f"Error: {str(e)}")

    async def test_neon_auth_endpoint_exists(self):
        """Test that Neon authentication endpoint is available"""
        print("\n🔗 Testing Neon Authentication Endpoint...")
        
        try:
            # Test with dummy Neon credentials (should fail with auth error, not 404)
            neon_data = {
                "project_id": "test-project-123",
                "api_key": "test-api-key-456",
                "branch": "main"
            }
            
            response = await self.client.post("/api/auth/neon-auth", json=neon_data)
            
            # We expect 401 (auth failed) not 404 (endpoint not found)
            if response.status_code == 401:
                error_data = response.json()
                if "Neon authentication failed" in error_data.get("error", {}).get("message", ""):
                    self.log_result("Neon Auth Endpoint", True, "Endpoint exists and validates credentials")
                else:
                    self.log_result("Neon Auth Endpoint", False, f"Unexpected error message: {error_data}")
            elif response.status_code == 404:
                self.log_result("Neon Auth Endpoint", False, "Endpoint not found")
            else:
                self.log_result("Neon Auth Endpoint", False, f"Unexpected status code: {response.status_code}")
                
        except Exception as e:
            self.log_result("Neon Auth Endpoint Test", False, f"Error: {str(e)}")

    async def test_api_documentation(self):
        """Test that new endpoints are in API documentation"""
        print("\n📚 Testing API Documentation...")
        
        try:
            response = await self.client.get("/openapi.json")
            
            if response.status_code == 200:
                openapi_data = response.json()
                paths = openapi_data.get("paths", {})
                
                # Check if neon-auth endpoint is documented
                if "/api/auth/neon-auth" in paths:
                    self.log_result("API Documentation", True, "Neon auth endpoint documented in OpenAPI")
                else:
                    self.log_result("API Documentation", False, "Neon auth endpoint missing from documentation")
            else:
                self.log_result("API Documentation", False, f"Failed to get OpenAPI spec: {response.status_code}")
                
        except Exception as e:
            self.log_result("API Documentation Test", False, f"Error: {str(e)}")

    async def run_all_tests(self):
        """Run all authentication tests"""
        print("🔐 Authentication System Test Suite")
        print("Testing admin login disabled and Neon authentication enabled")
        print("=" * 60)
        
        try:
            # Create HTTP client
            timeout = httpx.Timeout(30.0)
            self.client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=timeout)
            
            # Run all tests
            await self.test_admin_login_disabled()
            await self.test_regular_user_login_works()
            await self.test_neon_auth_endpoint_exists()
            await self.test_api_documentation()
            
        finally:
            if self.client:
                await self.client.aclose()
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        
        if passed_tests == total_tests:
            print("\n✅ ALL AUTHENTICATION TESTS PASSED!")
            print("Admin login disabled and Neon authentication working correctly.")
            return True
        else:
            print("\n❌ Some authentication tests failed.")
            print("Please review the implementation.")
            
            # Show failed tests
            failed_tests = [r for r in self.test_results if not r["success"]]
            if failed_tests:
                print("\nFailed Tests:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['message']}")
            
            return False

async def main():
    """Main test execution"""
    print("Starting Authentication System Tests...")
    print("Make sure the backend server is running on http://localhost:8000")
    print("And that you have run the previous tests to set up admin/editor users")
    
    tester = AuthenticationTester()
    success = await tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)