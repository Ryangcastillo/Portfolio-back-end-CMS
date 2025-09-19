#!/usr/bin/env python3
"""
Validate traceability between governance documents.
Part of the governance enforcement system (ENF-005).
"""

import re
import sys
from pathlib import Path
from typing import Set, Dict, List, Tuple, Optional
import argparse


class TraceabilityValidator:
    """Validates traceability links between governance documents."""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(".")
        self.errors = []
        self.warnings = []
        self.documents = {}
    
    def validate(self) -> bool:
        """Run all traceability validation checks."""
        self.errors.clear()
        self.warnings.clear()
        
        # Load all governance documents
        self._load_documents()
        
        # Run validation checks
        self._validate_task_references()
        self._validate_plan_references()
        self._validate_adr_references()
        self._validate_orphaned_items()
        
        return len(self.errors) == 0
    
    def _load_documents(self):
        """Load content from all governance documents."""
        doc_files = [
            "CONSTITUTION.md",
            "PLAN.md", 
            "TASKS.md",
            "ENFORCEMENT.md",
            "SPECIFICATIONS.md"
        ]
        
        # Also load ADR files
        adr_files = list(self.base_path.glob("ADR-*.md"))
        
        all_files = doc_files + [f.name for f in adr_files]
        
        for filename in all_files:
            filepath = self.base_path / filename
            if filepath.exists():
                try:
                    self.documents[filename] = filepath.read_text(encoding='utf-8')
                except Exception as e:
                    self.warnings.append(f"Could not read {filename}: {e}")
            else:
                if filename in doc_files:  # Only warn for core docs
                    self.warnings.append(f"Core document {filename} not found")
    
    def _extract_references(self, content: str, pattern: str) -> Set[str]:
        """Extract references matching pattern from content."""
        return set(re.findall(pattern, content))
    
    def _validate_task_references(self):
        """Validate that all tasks reference valid PLAN or SPEC items."""
        if "TASKS.md" not in self.documents:
            return
        
        tasks_content = self.documents["TASKS.md"]
        
        # Extract all task IDs
        task_ids = self._extract_references(tasks_content, r'### TASK-(\d{3})')
        
        # Extract available PLAN and SPEC references
        plan_ids = set()
        if "PLAN.md" in self.documents:
            plan_ids = self._extract_references(self.documents["PLAN.md"], r'PLAN-(\d{3})')
        
        # Extract SPEC IDs from SPECIFICATIONS.md
        spec_ids = set()
        if "SPECIFICATIONS.md" in self.documents:
            spec_ids = self._extract_references(self.documents["SPECIFICATIONS.md"], r'SPEC-(\d{3})')
        
        # Check each task for proper references
        orphaned_tasks = []
        invalid_references = []
        
        for task_id in task_ids:
            # Find the task section
            task_pattern = f'### TASK-{task_id}.*?(?=### TASK-|\\Z)'
            task_match = re.search(task_pattern, tasks_content, re.DOTALL)
            
            if not task_match:
                continue
                
            task_section = task_match.group(0)
            
            # Look for PLAN or SPEC references
            plan_refs = self._extract_references(task_section, r'PLAN-(\d{3})')
            spec_refs = self._extract_references(task_section, r'SPEC-(\d{3})')
            
            if not plan_refs and not spec_refs:
                orphaned_tasks.append(f"TASK-{task_id}")
                continue
            
            # Validate that referenced items exist
            for plan_ref in plan_refs:
                if plan_ref not in plan_ids:
                    invalid_references.append(f"TASK-{task_id} references non-existent PLAN-{plan_ref}")
            
            for spec_ref in spec_refs:
                if spec_ref not in spec_ids:
                    # For now, this is a warning since we don't have SPEC docs yet
                    self.warnings.append(f"TASK-{task_id} references SPEC-{spec_ref} but no SPEC documents found")
        
        if orphaned_tasks:
            self.errors.append(f"Tasks without PLAN/SPEC references: {', '.join(orphaned_tasks)}")
        
        if invalid_references:
            self.errors.append(f"Invalid references found: {'; '.join(invalid_references)}")
    
    def _validate_plan_references(self):
        """Validate that PLAN items reference valid CONST-P principles."""
        if "PLAN.md" not in self.documents or "CONSTITUTION.md" not in self.documents:
            return
        
        plan_content = self.documents["PLAN.md"]
        constitution_content = self.documents["CONSTITUTION.md"]
        
        # Extract principle IDs from constitution
        principle_ids = self._extract_references(constitution_content, r'CONST-P(\d+)')
        
        # Extract plan items and their principle references
        plan_ids = self._extract_references(plan_content, r'### PLAN-(\d{3})')
        invalid_principle_refs = []
        
        for plan_id in plan_ids:
            # Find the plan section
            plan_pattern = f'### PLAN-{plan_id}.*?(?=### PLAN-|\\Z)'
            plan_match = re.search(plan_pattern, plan_content, re.DOTALL)
            
            if not plan_match:
                continue
                
            plan_section = plan_match.group(0)
            
            # Look for CONST-P references
            const_refs = self._extract_references(plan_section, r'CONST-P(\d+)')
            
            for const_ref in const_refs:
                if const_ref not in principle_ids:
                    invalid_principle_refs.append(f"PLAN-{plan_id} references non-existent CONST-P{const_ref}")
        
        if invalid_principle_refs:
            self.errors.append(f"Invalid principle references: {'; '.join(invalid_principle_refs)}")
    
    def _validate_adr_references(self):
        """Validate that ADRs properly reference principles."""
        constitution_content = self.documents.get("CONSTITUTION.md", "")
        if not constitution_content:
            return
            
        principle_ids = self._extract_references(constitution_content, r'CONST-P(\d+)')
        
        # Check all ADR documents
        for doc_name, content in self.documents.items():
            if not doc_name.startswith("ADR-"):
                continue
                
            # Look for CONST-P references in ADR
            const_refs = self._extract_references(content, r'CONST-P(\d+)')
            invalid_refs = []
            
            for const_ref in const_refs:
                if const_ref not in principle_ids:
                    invalid_refs.append(f"{doc_name} references non-existent CONST-P{const_ref}")
            
            if invalid_refs:
                self.errors.extend(invalid_refs)
    
    def _validate_orphaned_items(self):
        """Check for items that exist but aren't referenced anywhere."""
        if "PLAN.md" not in self.documents:
            return
            
        plan_content = self.documents["PLAN.md"]
        plan_ids = self._extract_references(plan_content, r'PLAN-(\d{3})')
        
        # Find all PLAN references across all documents
        all_plan_refs = set()
        for doc_name, content in self.documents.items():
            if doc_name == "PLAN.md":  # Don't count self-references
                continue
            refs = self._extract_references(content, r'PLAN-(\d{3})')
            all_plan_refs.update(refs)
        
        # Find orphaned PLAN items (exist but not referenced)
        orphaned_plans = plan_ids - all_plan_refs
        if orphaned_plans:
            orphaned_list = [f"PLAN-{pid}" for pid in sorted(orphaned_plans)]
            self.warnings.append(f"Orphaned PLAN items (not referenced): {', '.join(orphaned_list)}")
    
    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("❌ Traceability validation FAILED")
            print("\nERRORS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ Traceability validation PASSED")
        elif not self.errors:
            print("✅ Traceability validation PASSED (with warnings)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate governance document traceability")
    parser.add_argument("--path", type=Path, help="Path to governance documents", 
                       default=Path("."))
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")
    
    args = parser.parse_args()
    
    validator = TraceabilityValidator(args.path)
    success = validator.validate()
    validator.print_results()
    
    if not success:
        sys.exit(1)
    
    if args.strict and validator.warnings:
        print("\n❌ Strict mode: Warnings treated as errors")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()