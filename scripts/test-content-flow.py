#!/usr/bin/env python3
"""
End-to-End Content Flow Test Suite
Tests the complete content lifecycle from creation to delivery
"""

import asyncio
import httpx
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "test_user",
    "email": "test@example.com", 
    "password": "test_password_123",
    "full_name": "Test User"
}

class ContentFlowTester:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=API_BASE_URL)
        self.auth_token = None
        self.test_results = []
        self.created_content_ids = []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        # Cleanup created content
        await self.cleanup_test_data()
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now()
        })
    
    async def setup_test_user(self):
        """Setup test user and authentication"""
        print("🔧 Setting up test user and authentication...")
        
        # Try to register user (might fail if already exists)
        try:
            response = await self.client.post("/api/auth/register", json=TEST_USER)
            if response.status_code == 201:
                self.log_result("User Registration", True, "Test user created")
            else:
                self.log_result("User Registration", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("User Registration", False, f"Error: {str(e)}")
        
        # Login
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            response = await self.client.post("/api/auth/token", data=login_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data["access_token"]
                self.client.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                self.log_result("User Login", True, "Authentication successful")
                return True
            else:
                self.log_result("User Login", False, f"Login failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("User Login", False, f"Login error: {str(e)}")
            return False
    
    async def test_content_creation(self) -> Dict[str, Any] | None:
        """Test content creation workflow"""
        print("📝 Testing content creation...")
        
        content_data = {
            "title": "End-to-End Test Article",
            "content_type": "article",
            "body": "This is a test article created during end-to-end testing of the CMS content flow.",
            "excerpt": "Test article for E2E testing",
            "meta_title": "E2E Test Article - CMS",
            "meta_description": "Test article created for end-to-end content flow testing",
            "meta_keywords": "test, e2e, cms, article",
            "status": "draft"
        }
        
        try:
            response = await self.client.post("/api/content/", json=content_data)
            
            if response.status_code == 201:
                created_content = response.json()
                self.created_content_ids.append(created_content["id"])
                self.log_result("Content Creation", True, f"Created content ID: {created_content['id']}")
                return created_content
            else:
                self.log_result("Content Creation", False, f"Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.log_result("Content Creation", False, f"Error: {str(e)}")
            return None
    
    async def test_content_retrieval(self, content_id: int):
        """Test content retrieval"""
        print("📖 Testing content retrieval...")
        
        try:
            response = await self.client.get(f"/api/content/{content_id}")
            
            if response.status_code == 200:
                content = response.json()
                self.log_result("Content Retrieval", True, f"Retrieved content: {content['title']}")
                return content
            else:
                self.log_result("Content Retrieval", False, f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("Content Retrieval", False, f"Error: {str(e)}")
            return None
    
    async def test_content_list_filtering(self):
        """Test content listing and filtering"""
        print("📋 Testing content listing and filtering...")
        
        # Test basic listing
        try:
            response = await self.client.get("/api/content/")
            if response.status_code == 200:
                content_list = response.json()
                self.log_result("Content Listing", True, f"Retrieved {len(content_list)} items")
            else:
                self.log_result("Content Listing", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("Content Listing", False, f"Error: {str(e)}")
        
        # Test filtering by content type
        try:
            response = await self.client.get("/api/content/?content_type=article")
            if response.status_code == 200:
                filtered_content = response.json()
                self.log_result("Content Filtering", True, f"Filtered results: {len(filtered_content)} articles")
            else:
                self.log_result("Content Filtering", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("Content Filtering", False, f"Error: {str(e)}")
        
        # Test search functionality
        try:
            response = await self.client.get("/api/content/?search=End-to-End")
            if response.status_code == 200:
                search_results = response.json()
                self.log_result("Content Search", True, f"Search results: {len(search_results)} items")
            else:
                self.log_result("Content Search", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("Content Search", False, f"Error: {str(e)}")
    
    async def test_content_editing(self, content_id: int):
        """Test content editing workflow"""
        print("✏️ Testing content editing...")
        
        update_data = {
            "title": "Updated End-to-End Test Article",
            "body": "This article has been updated during the end-to-end testing process.",
            "meta_description": "Updated test article for comprehensive flow testing"
        }
        
        try:
            response = await self.client.put(f"/api/content/{content_id}", json=update_data)
            
            if response.status_code == 200:
                updated_content = response.json()
                self.log_result("Content Editing", True, f"Updated content: {updated_content['title']}")
                return updated_content
            else:
                self.log_result("Content Editing", False, f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("Content Editing", False, f"Error: {str(e)}")
            return None
    
    async def test_content_publishing(self, content_id: int):
        """Test content publishing workflow"""
        print("🚀 Testing content publishing...")
        
        publish_data = {"status": "published"}
        
        try:
            response = await self.client.put(f"/api/content/{content_id}", json=publish_data)
            
            if response.status_code == 200:
                published_content = response.json()
                if published_content["status"] == "published":
                    self.log_result("Content Publishing", True, "Content successfully published")
                    return published_content
                else:
                    self.log_result("Content Publishing", False, "Status not updated to published")
                    return None
            else:
                self.log_result("Content Publishing", False, f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("Content Publishing", False, f"Error: {str(e)}")
            return None
    
    async def test_ai_integration(self, content_id: int):
        """Test AI integration features"""
        print("🤖 Testing AI integration...")
        
        try:
            response = await self.client.post(f"/api/content/{content_id}/ai-suggestions")
            
            if response.status_code == 200:
                suggestions = response.json()
                self.log_result("AI Suggestions", True, "AI suggestions generated successfully")
                return suggestions
            else:
                self.log_result("AI Suggestions", False, f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("AI Suggestions", False, f"Error: {str(e)}")
            return None
    
    async def test_dashboard_integration(self):
        """Test dashboard data integration"""
        print("📊 Testing dashboard integration...")
        
        # Test dashboard stats
        try:
            response = await self.client.get("/api/dashboard/stats")
            if response.status_code == 200:
                stats = response.json()
                self.log_result("Dashboard Stats", True, f"Stats retrieved: {stats.get('total_content', 0)} total content")
            else:
                self.log_result("Dashboard Stats", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("Dashboard Stats", False, f"Error: {str(e)}")
        
        # Test analytics
        try:
            response = await self.client.get("/api/dashboard/analytics")
            if response.status_code == 200:
                analytics = response.json()
                self.log_result("Dashboard Analytics", True, "Analytics data retrieved")
            else:
                self.log_result("Dashboard Analytics", False, f"Failed: {response.status_code}")
        except Exception as e:
            self.log_result("Dashboard Analytics", False, f"Error: {str(e)}")
    
    async def test_portfolio_integration(self):
        """Test portfolio content integration"""
        print("🎨 Testing portfolio integration...")
        
        # Test getting public portfolio data (no auth required)
        client_no_auth = httpx.AsyncClient(base_url=API_BASE_URL)
        
        try:
            response = await client_no_auth.get("/api/public/profile")
            if response.status_code == 200 or response.status_code == 404:
                self.log_result("Portfolio Public API", True, "Public profile endpoint accessible")
            else:
                self.log_result("Portfolio Public API", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_result("Portfolio Public API", False, f"Error: {str(e)}")
        finally:
            await client_no_auth.aclose()
    
    async def test_content_deletion(self, content_id: int):
        """Test content deletion (cleanup)"""
        print("🗑️ Testing content deletion...")
        
        try:
            response = await self.client.delete(f"/api/content/{content_id}")
            
            if response.status_code == 200:
                self.log_result("Content Deletion", True, "Content deleted successfully")
                return True
            else:
                self.log_result("Content Deletion", False, f"Failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Content Deletion", False, f"Error: {str(e)}")
            return False
    
    async def cleanup_test_data(self):
        """Cleanup any remaining test data"""
        print("🧹 Cleaning up test data...")
        
        for content_id in self.created_content_ids:
            try:
                await self.client.delete(f"/api/content/{content_id}")
            except:
                pass  # Ignore cleanup errors
    
    async def run_comprehensive_test(self):
        """Run the complete end-to-end test suite"""
        print("🚀 Starting End-to-End Content Flow Test Suite")
        print("=" * 60)
        
        # Setup
        if not await self.setup_test_user():
            print("❌ Cannot proceed without authentication")
            return False
        
        # Test content creation
        created_content = await self.test_content_creation()
        if not created_content:
            print("❌ Cannot proceed without created content")
            return False
        
        content_id = created_content["id"]
        
        # Test content retrieval
        await self.test_content_retrieval(content_id)
        
        # Test content listing and filtering
        await self.test_content_list_filtering()
        
        # Test content editing
        await self.test_content_editing(content_id)
        
        # Test content publishing
        await self.test_content_publishing(content_id)
        
        # Test AI integration
        await self.test_ai_integration(content_id)
        
        # Test dashboard integration
        await self.test_dashboard_integration()
        
        # Test portfolio integration
        await self.test_portfolio_integration()
        
        # Test content deletion
        await self.test_content_deletion(content_id)
        
        # Print summary
        self.print_test_summary()
        
        return all(result["success"] for result in self.test_results)
    
    def print_test_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
        
        if failed_tests == 0:
            print("✅ ALL TESTS PASSED! Content flow is working correctly.")
        else:
            print("❌ Some tests failed. Please review and fix issues.")
        
        return failed_tests == 0


async def main():
    """Main test execution"""
    print("🎯 Headless CMS - End-to-End Content Flow Test")
    print("Testing complete content lifecycle: Create → Read → Update → Publish → Delete")
    print()
    
    async with ContentFlowTester() as tester:
        success = await tester.run_comprehensive_test()
        return 0 if success else 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)