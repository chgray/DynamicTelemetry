#!/usr/bin/env python3

import sys
import yaml
from pathlib import Path
from typing import List, Dict
import subprocess
import json

def load_markdownlint_config(config_path: str) -> Dict:
    """Load the markdownlint configuration from yaml file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def find_markdown_files(base_path: str) -> List[Path]:
    """Recursively find all markdown files in the given directory."""
    base = Path(base_path)
    return list(base.rglob("*.md"))

def check_markdown_file(file_path: str, config_path: str) -> List[str]:
    """Check a markdown file against markdownlint rules."""
    try:
        # Run markdownlint-cli with JSON output format
        result = subprocess.run(
            ["markdownlint", "-c", config_path, "--json", file_path],
            capture_output=True,
            text=True
        )

        # If return code is 0, file is compliant
        if result.returncode == 0:
            return []

        # Parse JSON output for violations
        violations = json.loads(result.stdout)
        return [f"Line {v['lineNumber']}: {v['ruleDescription']}" for v in violations]
    except subprocess.CalledProcessError as e:
        return [f"Error checking file: {str(e)}"]
    except json.JSONDecodeError:
        return [f"Error parsing markdownlint output"]

def main():
    # Set paths
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / ".markdownlint.yaml"
    docs_path = repo_root / "docs"

    # Verify markdownlint-cli is installed
    try:
        subprocess.run(["markdownlint", "--version"], capture_output=True)
    except FileNotFoundError:
        print("Error: markdownlint-cli is not installed.")
        print("Please install it using: npm install -g markdownlint-cli")
        sys.exit(1)

    # Load config
    try:
        config = load_markdownlint_config(config_path)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

    # Find all markdown files
    md_files = find_markdown_files(docs_path)

    # Track files with issues
    files_with_issues = False

    # Check each file
    for md_file in md_files:
        violations = check_markdown_file(str(md_file), str(config_path))
        if violations:
            files_with_issues = True
            print(f"\n{md_file}:")
            for violation in violations:
                print(f"  {violation}")

    if not files_with_issues:
        print("All markdown files conform to the style guide.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
