#!/usr/bin/env python3
"""
Main governance validation runner.
Executes all governance compliance checks.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import argparse


def run_validation(script_name: str, args: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Run a validation script and return success status and output."""
    script_path = Path(__file__).parent / script_name
    cmd = ["python3", str(script_path)]
    
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        output = result.stdout + result.stderr
        return result.returncode == 0, output
        
    except subprocess.TimeoutExpired:
        return False, f"Validation {script_name} timed out"
    except Exception as e:
        return False, f"Error running {script_name}: {e}"


def main():
    """Main entry point for governance validation."""
    parser = argparse.ArgumentParser(description="Run all governance validation checks")
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")
    parser.add_argument("--pr-mode", action="store_true",
                       help="Run in PR validation mode")
    parser.add_argument("--skip-pr-refs", action="store_true",
                       help="Skip PR reference validation")
    
    args = parser.parse_args()
    
    # Define validation checks to run
    validations = [
        ("Constitution Validation", "validate_constitution.py", 
         ["--strict"] if args.strict else []),
        ("Traceability Validation", "validate_traceability.py", 
         ["--strict"] if args.strict else []),
    ]
    
    # Add PR reference validation if in PR mode
    if args.pr_mode and not args.skip_pr_refs:
        validations.append((
            "PR Reference Validation", "validate_pr_references.py",
            ["--check-commits", "--strict"] if args.strict else ["--check-commits"]
        ))
    
    print("🔍 Running Governance Compliance Checks")
    print("=" * 50)
    
    all_passed = True
    results = []
    
    # Run each validation
    for name, script, script_args in validations:
        print(f"\n📋 {name}")
        print("-" * len(name))
        
        success, output = run_validation(script, script_args)
        results.append((name, success, output))
        
        if success:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            all_passed = False
        
        # Print output (truncated if too long)
        if output.strip():
            lines = output.strip().split('\n')
            if len(lines) > 10:
                print('\n'.join(lines[:5]))
                print(f"... ({len(lines) - 10} more lines)")
                print('\n'.join(lines[-5:]))
            else:
                print(output.strip())
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 GOVERNANCE VALIDATION SUMMARY")
    print("=" * 50)
    
    passed_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    for name, success, _ in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{name}: {status}")
    
    print(f"\nResults: {passed_count}/{total_count} checks passed")
    
    if all_passed:
        print("\n🎉 All governance checks PASSED!")
        sys.exit(0)
    else:
        print("\n💥 Some governance checks FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()