#!/usr/bin/env python3
"""
Validate CONSTITUTION.md structure and compliance.
Part of the governance enforcement system (ENF-001).
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Set
import argparse


class ConstitutionValidator:
    """Validates Constitution document structure and content."""
    
    def __init__(self, constitution_path: Path = Path("CONSTITUTION.md")):
        self.constitution_path = constitution_path
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all validation checks. Returns True if all checks pass."""
        self.errors.clear()
        self.warnings.clear()
        
        if not self.constitution_path.exists():
            self.errors.append(f"CONSTITUTION.md not found at {self.constitution_path}")
            return False
        
        content = self.constitution_path.read_text(encoding='utf-8')
        
        # Run all validation checks
        self._validate_file_structure(content)
        self._validate_principle_ids(content)
        self._validate_required_sections(content)
        self._validate_metadata(content)
        self._validate_version_format(content)
        
        return len(self.errors) == 0
    
    def _validate_file_structure(self, content: str):
        """Validate basic markdown structure."""
        if not content.strip():
            self.errors.append("Constitution file is empty")
            return
        
        if not content.startswith('# '):
            self.errors.append("Constitution must start with a level 1 heading")
        
        # Check for valid markdown structure
        lines = content.split('\n')
        heading_levels = []
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > 6:
                    self.errors.append(f"Invalid heading level at line {line_num}: {line}")
                heading_levels.append(level)
    
    def _validate_principle_ids(self, content: str):
        """Validate principle IDs are unique and properly formatted."""
        # Extract all principle IDs - updated pattern to match actual format
        principle_pattern = r'### (CONST-P(\d+)):'
        matches = re.findall(principle_pattern, content)
        
        if not matches:
            self.errors.append("No principle IDs (CONST-P#) found")
            return
        
        principle_ids = [match[0] for match in matches]
        principle_numbers = [int(match[1]) for match in matches]
        
        # Check for duplicates
        seen_ids = set()
        duplicates = set()
        for pid in principle_ids:
            if pid in seen_ids:
                duplicates.add(pid)
            seen_ids.add(pid)
        
        if duplicates:
            self.errors.append(f"Duplicate principle IDs found: {', '.join(sorted(duplicates))}")
        
        # Check for sequential numbering
        principle_numbers.sort()
        expected_numbers = list(range(1, len(principle_numbers) + 1))
        if principle_numbers != expected_numbers:
            self.warnings.append(f"Principle numbers are not sequential. Found: {principle_numbers}, Expected: {expected_numbers}")
        
        # Validate principle format - principles should have titles after the colon
        for match in re.finditer(principle_pattern, content):
            line_start = content.rfind('\n', 0, match.start()) + 1
            line_end = content.find('\n', match.end())
            if line_end == -1:
                line_end = len(content)
            line_content = content[line_start:line_end].strip()
            
            # Check if there's content after the colon (title)
            if line_content.count(':') == 1 and line_content.endswith(':'):
                self.warnings.append(f"Principle {match.group(1)} has no title after colon")
            elif ':' not in line_content:
                self.errors.append(f"Principle {match.group(1)} heading must contain colon")
    
    def _validate_required_sections(self, content: str):
        """Validate required sections are present."""
        required_sections = [
            "Purpose",
            "Principles", 
            "Decision Hierarchy",
            "Amendment Process",
            "Compliance & Enforcement",
            "Quality Bars",
            "Roles & Responsibilities",
            "Glossary",
            "Non-Negotiables",
            "Effective Date"
        ]
        
        # Extract all section headings
        section_pattern = r'^##?\s+(.+)$'
        found_sections = re.findall(section_pattern, content, re.MULTILINE)
        found_sections = [s.strip() for s in found_sections]
        
        missing_sections = []
        for required in required_sections:
            # Check if section exists (allow for variations)
            found = any(required.lower() in section.lower() for section in found_sections)
            if not found:
                missing_sections.append(required)
        
        if missing_sections:
            self.errors.append(f"Missing required sections: {', '.join(missing_sections)}")
    
    def _validate_metadata(self, content: str):
        """Validate metadata section."""
        required_metadata = ["Version:", "Effective:", "Change Log:"]
        
        for metadata in required_metadata:
            if metadata not in content:
                self.errors.append(f"Missing required metadata: {metadata}")
    
    def _validate_version_format(self, content: str):
        """Validate version follows semantic versioning."""
        version_match = re.search(r'Version:\s*(\d+\.\d+\.\d+)', content)
        if not version_match:
            self.errors.append("Version must follow semantic versioning format (x.y.z)")
        
        effective_match = re.search(r'Effective:\s*(\d{4}-\d{2}-\d{2})', content)
        if not effective_match:
            self.errors.append("Effective date must follow YYYY-MM-DD format")
    
    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("❌ Constitution validation FAILED")
            print("\nERRORS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ Constitution validation PASSED")
        elif not self.errors:
            print("✅ Constitution validation PASSED (with warnings)")
        
        return len(self.errors) == 0


def main():
    """Main function to validate the constitution."""
    base_path = Path(".")
    constitution_path = base_path / "docs/governance/CONSTITUTION.md"
    
    validator = ConstitutionValidator(constitution_path)
    success = validator.validate()
    validator.print_results()
    
    # Exit with error code if validation failed
    if not success:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()