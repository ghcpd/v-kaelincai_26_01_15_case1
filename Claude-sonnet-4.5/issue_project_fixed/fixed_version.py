#!/usr/bin/env python3
"""
Fix Script for Issue #307: Remove Trailing Spaces from User Agent Strings

This script reads the original browsers.json file from the issue_project,
removes trailing spaces from all User Agent strings, and saves the fixed
version to the issue_project_fixed directory.

Author: Fixed Version Team
Date: 2026-01-15
"""

import json
import os
import sys
from pathlib import Path


def fix_browsers_json(input_file, output_file):
    """
    Remove trailing spaces from User Agent strings in browsers.json
    
    Args:
        input_file (str): Path to the original browsers.json file
        output_file (str): Path to save the fixed browsers.json file
    
    Returns:
        dict: Statistics about the fix operation
    """
    print("=" * 70)
    print("Fix Script for Issue #307")
    print("=" * 70)
    print()
    
    # Read the original file
    print(f"Reading original file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_count = len(lines)
    fixed_count = 0
    fixed_data = []
    
    print(f"Total User Agents found: {total_count}")
    print()
    print("Processing User Agents...")
    print("-" * 70)
    
    # Process each line
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # Parse JSON
        data = json.loads(line)
        
        # Check if useragent has trailing spaces
        original_ua = data.get('useragent', '')
        fixed_ua = original_ua.rstrip()
        
        if original_ua != fixed_ua:
            fixed_count += 1
            print(f"[{i:3d}] Fixed: {data.get('browser', 'unknown')} {data.get('version', 'N/A')} "
                  f"({data.get('os', 'unknown')}) - Removed {len(original_ua) - len(fixed_ua)} trailing space(s)")
            data['useragent'] = fixed_ua
        
        fixed_data.append(data)
    
    # Save fixed data to output file
    print()
    print("-" * 70)
    print(f"Saving fixed data to: {output_file}")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for data in fixed_data:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    # Calculate statistics
    fix_percentage = (fixed_count / total_count * 100) if total_count > 0 else 0
    
    print()
    print("=" * 70)
    print("Fix Completion Report")
    print("=" * 70)
    print(f"[SUCCESS] Fix Completed!")
    print(f"  - Original UA Count:  {total_count}")
    print(f"  - Fixed UA Count:     {fixed_count}")
    print(f"  - Fix Ratio:          {fix_percentage:.1f}%")
    print(f"  - Unchanged UAs:      {total_count - fixed_count}")
    print()
    print("Verification:")
    print(f"  - All {total_count} User Agents processed")
    print(f"  - {fixed_count} User Agents had trailing spaces removed")
    print(f"  - {total_count - fixed_count} User Agents were already clean")
    print()
    print("Output file saved successfully!")
    print("=" * 70)
    
    return {
        'total': total_count,
        'fixed': fixed_count,
        'unchanged': total_count - fixed_count,
        'percentage': fix_percentage
    }


def main():
    """Main function to run the fix script"""
    # Get the script directory
    script_dir = Path(__file__).parent
    
    # Define paths relative to workspace root
    workspace_root = script_dir.parent.parent
    input_file = workspace_root / 'issue_project' / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    output_file = script_dir / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        print("Please ensure the issue_project directory is in the correct location.")
        sys.exit(1)
    
    # Run the fix
    stats = fix_browsers_json(str(input_file), str(output_file))
    
    # Return success
    return 0


if __name__ == '__main__':
    sys.exit(main())
