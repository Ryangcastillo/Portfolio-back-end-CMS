#!/usr/bin/env python3
"""
Validate PR references to governance items.
Part of the governance enforcement system (ENF-004).
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Set, List, Optional
import argparse
import subprocess


class PRReferenceValidator:
    """Validates PR references to TASK/PLAN/SPEC items."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_pr(self, pr_description: str, pr_title: str = "") -> bool:
        """Validate PR references."""
        self.errors.clear()
        self.warnings.clear()
        
        # Combine title and description for reference checking
        full_text = f"{pr_title}\n{pr_description}"
        
        # Check for TASK references
        task_refs = self._extract_references(full_text, r'TASK-(\d{3})')
        
        if not task_refs:
            self.errors.append("PR must reference at least one TASK-### item")
            return False
        
        # Validate that referenced tasks exist
        self._validate_task_existence(task_refs)
        
        # Check for proper formatting
        self._validate_reference_format(full_text)
        
        return len(self.errors) == 0
    
    def _extract_references(self, content: str, pattern: str) -> Set[str]:
        """Extract references matching pattern from content."""
        return set(re.findall(pattern, content, re.IGNORECASE))
    
    def _validate_task_existence(self, task_refs: Set[str]):
        """Validate that referenced tasks exist in TASKS.md."""
        tasks_file = Path("TASKS.md")
        if not tasks_file.exists():
            self.warnings.append("TASKS.md not found - cannot validate task references")
            return
        
        try:
            tasks_content = tasks_file.read_text(encoding='utf-8')
            existing_tasks = self._extract_references(tasks_content, r'### TASK-(\d{3})')
            
            invalid_tasks = task_refs - existing_tasks
            if invalid_tasks:
                invalid_list = [f"TASK-{task}" for task in sorted(invalid_tasks)]
                self.errors.append(f"Referenced tasks do not exist: {', '.join(invalid_list)}")
        
        except Exception as e:
            self.warnings.append(f"Could not validate task references: {e}")
    
    def _validate_reference_format(self, content: str):
        """Check for proper reference formatting."""
        # Look for malformed task references
        malformed_patterns = [
            r'\btask[\s-]*(\d{1,2})\b',  # task-1, task 12, etc. (should be TASK-001)
            r'\bTASK[\s-]*(\d{1,2})\b',  # TASK-1, TASK 12, etc. (should be TASK-001)
        ]
        
        malformed_refs = []
        for pattern in malformed_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                malformed_refs.append(f"TASK-{match} (should be TASK-{match.zfill(3)})")
        
        if malformed_refs:
            self.warnings.append(f"Malformed task references found: {', '.join(malformed_refs)}")
    
    def validate_commit_messages(self, commit_range: Optional[str] = None) -> bool:
        """Validate commit message references."""
        try:
            if commit_range:
                cmd = ["git", "log", "--pretty=format:%s", commit_range]
            else:
                # Check last 10 commits on current branch
                cmd = ["git", "log", "--pretty=format:%s", "-10"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            commit_messages = result.stdout.strip().split('\n')
            
            commits_without_refs = []
            for i, message in enumerate(commit_messages):
                if not message.strip():
                    continue
                
                # Skip merge commits and automated commits
                if message.startswith(('Merge ', 'Revert ', 'chore:', 'ci:')):
                    continue
                
                # Look for TASK references
                task_refs = self._extract_references(message, r'TASK-(\d{3})')
                if not task_refs:
                    commits_without_refs.append(f"Commit {i+1}: {message[:50]}...")
            
            if commits_without_refs:
                self.warnings.append(f"Commits without TASK references: {commits_without_refs[:3]}")  # Limit to 3
        
        except subprocess.CalledProcessError as e:
            self.warnings.append(f"Could not validate commit messages: {e}")
        except Exception as e:
            self.warnings.append(f"Error validating commits: {e}")
        
        return True  # Non-fatal for now
    
    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("❌ PR reference validation FAILED")
            print("\nERRORS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ PR reference validation PASSED")
        elif not self.errors:
            print("✅ PR reference validation PASSED (with warnings)")


def get_github_pr_info():
    """Get PR information from GitHub environment variables."""
    pr_number = os.getenv('PR_NUMBER')
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not pr_number or not github_token:
        return None, None
    
    try:
        # Use GitHub CLI to get PR info
        cmd = ["gh", "pr", "view", pr_number, "--json", "title,body"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pr_data = json.loads(result.stdout)
        
        return pr_data.get('title', ''), pr_data.get('body', '')
    
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        # Fallback: try to get from git commit messages
        return None, None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate PR references to governance items")
    parser.add_argument("--pr-description", help="PR description text")
    parser.add_argument("--pr-title", help="PR title")
    parser.add_argument("--check-commits", action="store_true",
                       help="Also validate commit message references")
    parser.add_argument("--commit-range", help="Git commit range to check")
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")
    
    args = parser.parse_args()
    
    validator = PRReferenceValidator()
    success = True
    
    # Get PR info from arguments or environment
    pr_title = args.pr_title or ""
    pr_description = args.pr_description or ""
    
    if not pr_description:
        # Try to get from GitHub environment
        title, description = get_github_pr_info()
        if title or description:
            pr_title = title or pr_title
            pr_description = description or pr_description
    
    # If we still don't have PR info, try to infer from git
    if not pr_description and not pr_title:
        try:
            # Get the last commit message as fallback
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%s%n%b"],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().split('\n')
            pr_title = lines[0] if lines else ""
            pr_description = '\n'.join(lines[1:]) if len(lines) > 1 else ""
        except:
            pass
    
    # Validate PR references if we have content
    if pr_title or pr_description:
        success = validator.validate_pr(pr_description, pr_title)
    else:
        print("⚠ No PR content found - skipping PR reference validation")
    
    # Validate commit messages if requested
    if args.check_commits:
        commit_success = validator.validate_commit_messages(args.commit_range)
        success = success and commit_success
    
    validator.print_results()
    
    if not success:
        sys.exit(1)
    
    if args.strict and validator.warnings:
        print("\n❌ Strict mode: Warnings treated as errors")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()