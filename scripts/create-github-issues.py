#!/usr/bin/env python3
"""
Parse phase files and create GitHub issues with all metadata.
Each issue includes: Story, Acceptance Criteria, Files, Dependencies, Testing, and sections for Clarifications and Plan.
"""

import os
import re
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class IssueParser:
    """Parse issue blocks from phase files."""
    
    def __init__(self, phase_file: Path):
        self.phase_file = phase_file
        self.phase_name = phase_file.stem
        self.content = phase_file.read_text()
        
    def extract_issues(self) -> List[Dict]:
        """Extract all issues from the phase file."""
        issues = []
        
        # Pattern to match issue blocks (### M#-#: Title ... until next ### or end)
        pattern = r"^###\s+(M\d+-\d+):\s*(.+?)$(?:\n((?:(?!^###).)*))"
        matches = re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            issue_ref = match.group(1)  # e.g., "M0-1"
            title = match.group(2).strip()
            issue_block = match.group(3) or ""
            
            issue_data = self._parse_issue_block(issue_ref, title, issue_block)
            issues.append(issue_data)
        
        return issues
    
    def _parse_issue_block(self, issue_ref: str, title: str, block: str) -> Dict:
        """Parse a single issue block into structured data."""
        
        def extract_field(pattern: str) -> Optional[str]:
            match = re.search(pattern, block, re.DOTALL)
            return match.group(1).strip() if match else None
        
        # Extract fields
        issue_type = extract_field(r"\*\*Type\*\*:\s*`([^`]+)`")
        priority = extract_field(r"\*\*Priority\*\*:\s*`([^`]+)`")
        effort = extract_field(r"\*\*Effort\*\*:\s*`([^`]+)`")
        depends_on = extract_field(r"\*\*Depends On\*\*:\s*(.+?)(?:\n\*\*|$)")
        blocks = extract_field(r"\*\*Blocks\*\*:\s*(.+?)(?:\n\*\*|$)")
        
        description = extract_field(r"\*\*Description\*\*:\s*\n(.+?)(?=\n\*\*Acceptance|\Z)")
        acceptance = extract_field(r"\*\*Acceptance Criteria\*\*:\s*\n(.+?)(?=\n\*\*Files|\Z)")
        files = extract_field(r"\*\*Files to Create[^:]*\*\*:\s*\n(.+?)(?=\n\n|\n\*\*|$)")
        testing = extract_field(r"\*\*Testing\*\*:\s*\n(.+?)(?=\n\*\*|$)")
        story = extract_field(r"\*\*Story\*\*:\s*\n```\n(.+?)\n```")
        
        return {
            "ref": issue_ref,
            "title": title,
            "type": issue_type or "type:feature",
            "priority": priority or "P2",
            "effort": effort or "effort:small",
            "depends_on": depends_on or "None",
            "blocks": blocks or "None",
            "description": description or "",
            "acceptance": acceptance or "",
            "files": files or "",
            "testing": testing or "",
            "story": story or "",
            "phase_name": self.phase_name,
        }


def get_milestone_number(phase_name: str) -> int:
    """Map phase name to milestone number (as displayed in GH API response)."""
    mapping = {
        "phase-0-prerequisites": 1,  # Milestone 0
        "phase-1-project-setup": 2,  # Milestone 1
        "phase-2-frontend-stack": 3,  # Milestone 2
        "phase-3-database-models": 4,  # Milestone 3
        "phase-4-search": 5,  # Milestone 4
        "phase-5-controllers-routing": 6,  # Milestone 5
        "phase-6-layout-components": 7,  # Milestone 6
        "phase-7-recipe-views": 8,  # Milestone 7
        "phase-8-cookbook-views": 9,  # Milestone 8
        "phase-9-interactivity": 10,  # Milestone 9
        "phase-10-asset-pipeline": 11,  # Milestone 10
        "phase-11-seeding": 12,  # Milestone 11
        "phase-12-testing": 13,  # Milestone 12
        "phase-13-security": 14,  # Milestone 13
        "phase-14-performance": 15,  # Milestone 14
        "phase-15-cicd": 16,  # Milestone 15
        "phase-16-deployment": 17,  # Milestone 16
    }
    return mapping.get(phase_name, 1)


def get_phase_number(phase_name: str) -> int:
    """Extract phase number from phase name."""
    match = re.match(r"phase-(\d+)", phase_name)
    return int(match.group(1)) if match else 0


def create_github_issue(issue: Dict) -> Optional[str]:
    """Create a GitHub issue and return the issue number."""
    
    # Build issue body with all sections
    body = f"""## Story
{issue['story'] or 'As a developer...'}

## Acceptance Criteria
{issue['acceptance'] or 'See phase file for details'}

## Files to Create/Modify
{issue['files'] or 'See phase file for details'}

## Dependencies
**Depends On**: {issue['depends_on']}
**Blocks**: {issue['blocks']}

## Testing
{issue['testing'] or 'See phase file for details'}

## Clarifications
*To be filled by clarify-ticket prompt*

## Implementation Plan
*To be filled by plan-ticket prompt with 10 sections*

## Plan Analysis
*To be filled by analyze-plan prompt*
"""
    
    # Extract labels - normalize type labels
    type_label = issue['type']
    if type_label == "type:optimization":
        type_label = "type:performance"  # Map to existing label
    
    labels = [
        f"phase-{get_phase_number(issue['phase_name'])}",
        type_label,
        issue['priority'],
        issue['effort'],
        "ready",  # All new issues start as ready
    ]
    
    # Build gh issue create command
    cmd = [
        "gh", "issue", "create",
        "--title", f"{issue['ref']}: {issue['title']}",
        "--body", body,
    ]
    
    # Add milestone (for now, skip if it fails)
    milestone_num = get_milestone_number(issue['phase_name'])
    
    # Add labels
    for label in labels:
        cmd.extend(["--label", label])
    
    # Execute command without milestone first
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract issue number from output
            match = re.search(r"#(\d+)", result.stdout)
            if match:
                issue_num = match.group(1)
                # Now try to add milestone
                subprocess.run(
                    ["gh", "issue", "edit", issue_num, "--milestone", str(milestone_num)],
                    capture_output=True, text=True, timeout=10
                )
                return issue_num
        else:
            print(f"\n❌ Failed to create {issue['ref']}: {result.stderr[:100]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  Timeout creating {issue['ref']}")
        return None
    except Exception as e:
        print(f"\n❌ Error creating {issue['ref']}: {e}")
        return None


def main():
    """Main entry point."""
    phase_dir = Path("docs/plan")
    all_issues = []
    issue_mapping = {}  # Map M#-# to GitHub issue number
    
    # Parse all phase files
    phase_files = sorted(phase_dir.glob("phase-*.md"))
    for phase_file in phase_files:
        parser = IssueParser(phase_file)
        issues = parser.extract_issues()
        all_issues.extend(issues)
        print(f"✓ Parsed {phase_file.name}: {len(issues)} issues")
    
    print(f"\n📊 Total issues parsed: {len(all_issues)}")
    print(f"🚀 Creating GitHub issues (with rate limiting)...\n")
    
    # Create issues
    import time
    created_count = 0
    for i, issue in enumerate(all_issues, 1):
        print(f"[{i:3d}/{len(all_issues)}] {issue['ref']:8} → ", end="", flush=True)
        
        issue_num = create_github_issue(issue)
        if issue_num:
            issue_mapping[issue['ref']] = issue_num
            created_count += 1
            print(f"#{issue_num}")
        else:
            print("FAILED")
        
        # Rate limiting: 1 second between each issue
        if i < len(all_issues):
            time.sleep(1.0)
    
    print(f"\n✅ Created {created_count}/{len(all_issues)} issues")
    
    # Save mapping for later use
    with open("scripts/issue-mapping.json", "w") as f:
        json.dump(issue_mapping, f, indent=2)
    print(f"💾 Issue mapping saved to scripts/issue-mapping.json")
    
    return issue_mapping


if __name__ == "__main__":
    main()
