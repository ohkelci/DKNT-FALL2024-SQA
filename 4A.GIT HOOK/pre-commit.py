#!/usr/bin/env python3

import subprocess
import sys
import os
from datetime import datetime
import csv
import json

def check_bandit_installation():
    """Make sure we have our security scanner ready"""
    try:
        subprocess.run(['bandit', '--version'], capture_output=True)
    except FileNotFoundError:
        print("Installing security scanner (bandit)...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'bandit'])
        print("Security scanner installed successfully!")

def get_all_python_files():
    """Find all Python files in our project to scan"""
    python_files = []
    # Get the root directory of the Git repository
    git_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                            capture_output=True, text=True).stdout.strip()
    
    for root, _, files in os.walk(git_root):
        # Skip version control directories
        if '.git' in root or '.svn' in root or '.hg' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                full_path = full_path.replace('\\', '/')
                python_files.append(full_path)
                print(f"Found Python file: {full_path}")
    
    return python_files

def run_security_scan(files):
    """Run the actual security scan on our Python files"""
    if not files:
        return None
    
    try:
        # Run bandit with detailed output
        cmd = ['bandit', '-f', 'json', '-ll', '-i', '-r'] + files
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            return result.stdout
        if result.stderr:
            print(f"Warning during scan: {result.stderr}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Scan failed: {e}")
        return None

def save_results_to_csv(scan_results, output_file='security_results/scan_results.csv'):
    """Save what we found to a CSV file"""
    if not scan_results:
        return
    
    try:
        results = json.loads(scan_results)
        
        # Make sure we have somewhere to save our results
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Open/create our report file
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = [
                'timestamp',
                'filename',
                'issue_severity',
                'issue_confidence',
                'issue_type',
                'line_number',
                'code_line',
                'issue_description'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Write each security issue we found
            for result in results.get('results', []):
                writer.writerow({
                    'timestamp': timestamp,
                    'filename': result['filename'],
                    'issue_severity': result['issue_severity'],
                    'issue_confidence': result['issue_confidence'],
                    'issue_type': result['test_id'],
                    'line_number': result['line_number'],
                    'code_line': result.get('code', '').strip(),
                    'issue_description': result['issue_text']
                })
            
            print(f"\nSecurity scans complete! Check {output_file} for results")
            
    except json.JSONDecodeError:
        print("Error: Couldn't understand scan results")
    except KeyError as e:
        print(f"Error: Missing information in results: {e}")

def main():
    """Main function that runs our security scan"""
    print("\nStarting security scan...")
    
    # First, make sure we have our security scanner
    check_bandit_installation()
    
    # Find all Python files in the project
    print("Looking for Python files...")
    python_files = get_all_python_files()
    
    if not python_files:
        print("No Python files found to scan.")
        sys.exit(0)
    
    print(f"\nFound {len(python_files)} Python files to scan")
    
    # Run the security scan
    print("Running security scan...")
    scan_results = run_security_scan(python_files)
    
    # Save what we found
    save_results_to_csv(scan_results)
    
    sys.exit(0)

if __name__ == '__main__':
    main()