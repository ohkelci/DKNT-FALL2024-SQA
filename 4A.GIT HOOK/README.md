# Git Hook Security Scanner

This security scanner automatically checks Python files for potential security vulnerabilities whenever changes are committed. The scanner uses Bandit, a tool designed to find common security issues in Python code.

## Setup Instructions

1. Navigate to your repository's .git/hooks directory:
```bash
cd .git/hooks
```

2. Copy these files to your .git/hooks directory:
   - `pre-commit` - The wrapper script that triggers our security scanner
   - `pre-commit.py` - The main security scanning script

3. Install required dependencies:
```bash
pip install bandit
```

## How It Works

The security scanner:
- Runs automatically when you commit Python files
- Scans all Python files in your project
- Generates a detailed CSV report of any security issues found
- Saves results in security_results/scan_results.csv

The CSV report includes:
- Timestamp of the scan
- Filename where issue was found
- Severity of the security issue
- Type of security vulnerability
- Line number where the issue occurs
- Description of the security concern

## Example Output

When you commit Python files, the scanner will run automatically and generate a report like this:
```
timestamp,filename,issue_severity,issue_confidence,issue_type,line_number,code_line,issue_description
2024-12-05 16:45:23,test.py,HIGH,HIGH,B102,3,eval(user_input),Use of eval found
```

## Implementation Details

The scanner is implemented using:
- Python's subprocess module for running Git commands
- Bandit security scanner for identifying vulnerabilities
- CSV output for easy analysis of results

## Testing

To test the scanner, commit a Python file with known security issues:
```python
# Example of unsafe code
password = "hardcoded_password"  # This will trigger a warning
user_input = input("Enter command: ")
eval(user_input)  # This will trigger a critical security warning
```
