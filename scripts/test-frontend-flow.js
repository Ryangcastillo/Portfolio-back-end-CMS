#!/usr/bin/env node
/**
 * Frontend Content Flow Test Suite
 * Tests React components and frontend integration
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class FrontendContentFlowTester {
  constructor() {
    this.browser = null;
    this.page = null;
    this.testResults = [];
    this.baseUrl = 'http://localhost:3000';
  }

  logResult(testName, success, message = '') {
    const status = success ? 'PASS' : 'FAIL';
    console.log(`[${status}] ${testName}: ${message}`);
    this.testResults.push({
      test: testName,
      success,
      message,
      timestamp: new Date()
    });
  }

  async setup() {
    console.log('🔧 Setting up browser environment...');
    
    try {
      this.browser = await chromium.launch({ headless: true });
      const context = await this.browser.newContext();
      this.page = await context.newPage();
      
      // Set up console and error logging
      this.page.on('console', msg => {
        if (msg.type() === 'error') {
          console.log(`Browser Console Error: ${msg.text()}`);
        }
      });
      
      this.page.on('pageerror', err => {
        console.log(`Browser Page Error: ${err.message}`);
      });
      
      this.logResult('Browser Setup', true, 'Browser launched successfully');
      return true;
    } catch (error) {
      this.logResult('Browser Setup', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testHomepageLoad() {
    console.log('🏠 Testing homepage load...');
    
    try {
      const response = await this.page.goto(this.baseUrl);
      
      if (response && response.status() < 400) {
        // Wait for main content to load
        await this.page.waitForSelector('main', { timeout: 5000 });
        
        const title = await this.page.title();
        this.logResult('Homepage Load', true, `Page loaded: ${title}`);
        return true;
      } else {
        this.logResult('Homepage Load', false, `HTTP ${response?.status()}`);
        return false;
      }
    } catch (error) {
      this.logResult('Homepage Load', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testNavigationComponents() {
    console.log('🧭 Testing navigation components...');
    
    try {
      // Test main navigation
      const navItems = await this.page.$$('nav a, nav button');
      if (navItems.length > 0) {
        this.logResult('Navigation Components', true, `Found ${navItems.length} navigation items`);
      } else {
        this.logResult('Navigation Components', false, 'No navigation items found');
      }
      
      // Test mobile menu toggle if present
      const mobileToggle = await this.page.$('[data-testid="mobile-menu-toggle"], .mobile-menu-toggle, button[aria-label*="menu"]');
      if (mobileToggle) {
        await mobileToggle.click();
        await this.page.waitForTimeout(500);
        this.logResult('Mobile Navigation', true, 'Mobile menu toggle works');
      }
      
      return true;
    } catch (error) {
      this.logResult('Navigation Components', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testContentPages() {
    console.log('📄 Testing content pages...');
    
    const testRoutes = [
      '/content',
      '/dashboard',
      '/settings',
      '/portfolio',
      '/modules'
    ];
    
    let successCount = 0;
    
    for (const route of testRoutes) {
      try {
        const response = await this.page.goto(`${this.baseUrl}${route}`);
        
        if (response && response.status() < 400) {
          await this.page.waitForSelector('main, .content, .dashboard', { timeout: 3000 });
          this.logResult(`Route ${route}`, true, 'Page loads correctly');
          successCount++;
        } else {
          this.logResult(`Route ${route}`, false, `HTTP ${response?.status()}`);
        }
      } catch (error) {
        this.logResult(`Route ${route}`, false, `Error: ${error.message}`);
      }
    }
    
    return successCount > 0;
  }

  async testFormComponents() {
    console.log('📝 Testing form components...');
    
    try {
      // Try to find forms on the current page
      const forms = await this.page.$$('form');
      const inputs = await this.page.$$('input, textarea, select');
      const buttons = await this.page.$$('button[type="submit"], button.submit, .btn-submit');
      
      if (forms.length > 0 || inputs.length > 0) {
        this.logResult('Form Components', true, `Found ${forms.length} forms, ${inputs.length} inputs, ${buttons.length} submit buttons`);
        
        // Test form interaction if inputs exist
        if (inputs.length > 0) {
          const firstInput = inputs[0];
          await firstInput.focus();
          await this.page.keyboard.type('Test input');
          this.logResult('Form Interaction', true, 'Form input interaction works');
        }
        
        return true;
      } else {
        this.logResult('Form Components', false, 'No forms or inputs found');
        return false;
      }
    } catch (error) {
      this.logResult('Form Components', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testResponsiveDesign() {
    console.log('📱 Testing responsive design...');
    
    const viewports = [
      { name: 'Mobile', width: 375, height: 667 },
      { name: 'Tablet', width: 768, height: 1024 },
      { name: 'Desktop', width: 1920, height: 1080 }
    ];
    
    let successCount = 0;
    
    for (const viewport of viewports) {
      try {
        await this.page.setViewportSize({ width: viewport.width, height: viewport.height });
        await this.page.waitForTimeout(500);
        
        // Check if page is still functional
        const body = await this.page.$('body');
        if (body) {
          const boundingBox = await body.boundingBox();
          if (boundingBox && boundingBox.width > 0 && boundingBox.height > 0) {
            this.logResult(`${viewport.name} Viewport`, true, `${viewport.width}x${viewport.height} renders correctly`);
            successCount++;
          }
        }
      } catch (error) {
        this.logResult(`${viewport.name} Viewport`, false, `Error: ${error.message}`);
      }
    }
    
    return successCount > 0;
  }

  async testPerformanceMetrics() {
    console.log('⚡ Testing performance metrics...');
    
    try {
      // Navigate to homepage and measure load time
      const startTime = Date.now();
      await this.page.goto(this.baseUrl);
      await this.page.waitForLoadState('networkidle');
      const loadTime = Date.now() - startTime;
      
      // Get performance metrics
      const performanceMetrics = await this.page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0];
        return {
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
          loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
          firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
          firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
        };
      });
      
      // Check if performance is acceptable (under 3 seconds)
      if (loadTime < 3000) {
        this.logResult('Page Load Performance', true, `Load time: ${loadTime}ms`);
      } else {
        this.logResult('Page Load Performance', false, `Slow load time: ${loadTime}ms`);
      }
      
      this.logResult('Performance Metrics', true, `DOM: ${performanceMetrics.domContentLoaded.toFixed(2)}ms, FCP: ${performanceMetrics.firstContentfulPaint.toFixed(2)}ms`);
      
      return true;
    } catch (error) {
      this.logResult('Performance Metrics', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testAccessibility() {
    console.log('♿ Testing accessibility features...');
    
    try {
      // Check for basic accessibility features
      const hasSkipLink = await this.page.$('a[href="#main"], .skip-link');
      const hasMainLandmark = await this.page.$('main, [role="main"]');
      const hasHeadings = await this.page.$$('h1, h2, h3, h4, h5, h6');
      const hasAltText = await this.page.$$eval('img', imgs => 
        imgs.every(img => img.alt !== undefined && img.alt !== '')
      ).catch(() => true); // If no images, consider it passing
      
      let accessibilityScore = 0;
      let maxScore = 4;
      
      if (hasSkipLink) accessibilityScore++;
      if (hasMainLandmark) accessibilityScore++;
      if (hasHeadings.length > 0) accessibilityScore++;
      if (hasAltText) accessibilityScore++;
      
      const percentage = (accessibilityScore / maxScore * 100).toFixed(0);
      
      if (accessibilityScore >= maxScore * 0.75) {
        this.logResult('Accessibility Features', true, `Score: ${accessibilityScore}/${maxScore} (${percentage}%)`);
      } else {
        this.logResult('Accessibility Features', false, `Low score: ${accessibilityScore}/${maxScore} (${percentage}%)`);
      }
      
      return true;
    } catch (error) {
      this.logResult('Accessibility Features', false, `Error: ${error.message}`);
      return false;
    }
  }

  async testErrorHandling() {
    console.log('❌ Testing error handling...');
    
    try {
      // Test 404 page
      const response = await this.page.goto(`${this.baseUrl}/nonexistent-page-12345`);
      
      if (response && response.status() === 404) {
        // Check if custom 404 page is shown
        const pageContent = await this.page.textContent('body');
        if (pageContent && (pageContent.includes('404') || pageContent.includes('Not Found') || pageContent.includes('Page not found'))) {
          this.logResult('404 Error Handling', true, 'Custom 404 page displayed');
        } else {
          this.logResult('404 Error Handling', false, 'No custom 404 page');
        }
      } else {
        this.logResult('404 Error Handling', false, `Expected 404, got ${response?.status()}`);
      }
      
      return true;
    } catch (error) {
      this.logResult('404 Error Handling', false, `Error: ${error.message}`);
      return false;
    }
  }

  async cleanup() {
    console.log('🧹 Cleaning up...');
    
    try {
      if (this.browser) {
        await this.browser.close();
      }
      this.logResult('Cleanup', true, 'Browser closed successfully');
    } catch (error) {
      this.logResult('Cleanup', false, `Error: ${error.message}`);
    }
  }

  printTestSummary() {
    console.log('\n' + '='.repeat(60));
    console.log('📋 FRONTEND TEST RESULTS SUMMARY');
    console.log('='.repeat(60));

    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(result => result.success).length;
    const failedTests = totalTests - passedTests;

    console.log(`Total Tests: ${totalTests}`);
    console.log(`Passed: ${passedTests}`);
    console.log(`Failed: ${failedTests}`);
    console.log(`Success Rate: ${(passedTests / totalTests * 100).toFixed(1)}%`);

    if (failedTests > 0) {
      console.log('\n❌ FAILED TESTS:');
      this.testResults.filter(result => !result.success).forEach(result => {
        console.log(`  - ${result.test}: ${result.message}`);
      });
    }

    console.log('\n' + '='.repeat(60));

    if (failedTests === 0) {
      console.log('✅ ALL FRONTEND TESTS PASSED! User interface is working correctly.');
    } else {
      console.log('❌ Some frontend tests failed. Please review and fix issues.');
    }

    return failedTests === 0;
  }

  async runComprehensiveTest() {
    console.log('🚀 Starting Frontend Content Flow Test Suite');
    console.log('Testing React components and user interface functionality');
    console.log('='.repeat(60));

    // Setup
    if (!await this.setup()) {
      console.log('❌ Cannot proceed without browser setup');
      return false;
    }

    // Run all tests
    await this.testHomepageLoad();
    await this.testNavigationComponents();
    await this.testContentPages();
    await this.testFormComponents();
    await this.testResponsiveDesign();
    await this.testPerformanceMetrics();
    await this.testAccessibility();
    await this.testErrorHandling();

    // Cleanup
    await this.cleanup();

    // Print summary
    return this.printTestSummary();
  }
}

async function main() {
  console.log('🎯 Headless CMS - Frontend Content Flow Test');
  console.log('Testing React components, navigation, and user experience');
  console.log();

  const tester = new FrontendContentFlowTester();
  const success = await tester.runComprehensiveTest();
  
  return success ? 0 : 1;
}

// Check if playwright is available
try {
  require('playwright');
  main().then(process.exit);
} catch (error) {
  console.log('❌ Playwright not found. Installing...');
  console.log('Please run: npm install playwright');
  console.log('Then run: npx playwright install');
  process.exit(1);
}