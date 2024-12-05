#!/usr/bin/env python3

import subprocess
import sys
import os
from datetime import datetime
import csv
import json

def check_bandit_installation():
    """checks if bandit is installed"""
    try:
        subprocess.run(['bandit', '--version'], capture_output=True)
    except FileNotFoundError:
        print("installing bandit...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'bandit'])
        print("done")

def get_all_python_files():
    """gets python files from the project"""
    python_files = []
    # get root dir
    git_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                            capture_output=True, text=True).stdout.strip()
    
    for root, _, files in os.walk(git_root):
        # skip git folders
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
    """runs the scan"""
    if not files:
        return None
    
    try:
        # run bandit
        cmd = ['bandit', '-f', 'json', '-ll', '-i', '-r'] + files
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            return result.stdout
        if result.stderr:
            print(f"warning: {result.stderr}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"failed: {e}")
        return None

def save_results_to_csv(scan_results, output_file='security_results/scan_results.csv'):
    """saves results to csv"""
    if not scan_results:
        return
    
    try:
        results = json.loads(scan_results)
        
        # make output folder
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='') as csvfile:
            # csv columns
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
            
            # write the issues
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
            
            print(f"\nresults saved to {output_file}")
            
    except json.JSONDecodeError:
        print("error parsing results")
    except KeyError as e:
        print(f"missing field: {e}")

def main():
    """main function"""
    print("\nstarting scan...")
    
    # check for bandit
    check_bandit_installation()
    
    # get files
    print("looking for python files...")
    python_files = get_all_python_files()
    
    if not python_files:
        print("no python files found")
        sys.exit(0)
    
    print(f"\nfound {len(python_files)} files")
    
    # scan and save
    print("running scan...")
    scan_results = run_security_scan(python_files)
    save_results_to_csv(scan_results)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
