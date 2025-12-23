#!/usr/bin/env python3
"""
Process Epic clinic notes exported as tab-separated text files.
Each file contains a header line followed by one or more data rows.
Converts multiple files into a single CSV or JSON output.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def parse_note_file(file_path: Path) -> List[Dict[str, str]]:
    """
    Parse a single note file with tab-separated headers and values.

    Args:
        file_path: Path to the note file

    Returns:
        List of dictionaries, one per data row
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) < 2:
            print(f"Warning: {file_path.name} has fewer than 2 lines, skipping", file=sys.stderr)
            return []

        # Parse headers
        headers = lines[0].strip().split('\t')

        # Parse all data rows (lines 1 onwards)
        records = []
        for line_num, line in enumerate(lines[1:], start=2):
            # Skip empty lines
            if not line.strip():
                continue

            values = line.strip().split('\t')

            # Handle mismatched lengths
            if len(headers) != len(values):
                print(f"Warning: {file_path.name} line {line_num} has {len(headers)} headers but {len(values)} values",
                      file=sys.stderr)
                # Pad with empty strings if needed
                if len(values) < len(headers):
                    values.extend([''] * (len(headers) - len(values)))
                else:
                    values = values[:len(headers)]

            # Create dictionary for this row
            records.append(dict(zip(headers, values)))

        return records

    except Exception as e:
        print(f"Error processing {file_path.name}: {e}", file=sys.stderr)
        return []


def process_directory(input_dir: Path, pattern: str = "*.txt") -> List[Dict[str, str]]:
    """
    Process all matching files in a directory.

    Args:
        input_dir: Directory containing note files
        pattern: Glob pattern for matching files (default: *.txt)

    Returns:
        List of dictionaries, one per data row across all files
    """
    files = sorted(input_dir.glob(pattern))

    if not files:
        print(f"Warning: No files matching '{pattern}' found in {input_dir}", file=sys.stderr)
        return []

    print(f"Processing {len(files)} files...", file=sys.stderr)

    records = []
    for file_path in files:
        file_records = parse_note_file(file_path)
        records.extend(file_records)

    print(f"Successfully processed {len(records)} records from {len(files)} files", file=sys.stderr)
    return records


def write_csv(records: List[Dict[str, str]], output_path: Path):
    """Write records to CSV file."""
    if not records:
        print("No records to write", file=sys.stderr)
        return
    
    # Get all unique fieldnames from all records
    fieldnames = []
    seen = set()
    for record in records:
        for key in record.keys():
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"CSV written to {output_path}", file=sys.stderr)


def write_json(records: List[Dict[str, str]], output_path: Path, pretty: bool = True):
    """Write records to JSON file."""
    if not records:
        print("No records to write", file=sys.stderr)
        return
    
    with open(output_path, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(records, f, indent=2, ensure_ascii=False)
        else:
            json.dump(records, f, ensure_ascii=False)
    
    print(f"JSON written to {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Epic clinic notes from tab-separated text files to CSV or JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert to CSV
  %(prog)s input_notes/ -o output.csv
  
  # Convert to JSON
  %(prog)s input_notes/ -o output.json
  
  # Process specific file pattern
  %(prog)s input_notes/ -o output.csv -p "note_*.txt"
  
  # Compact JSON output
  %(prog)s input_notes/ -o output.json --compact
        """
    )
    
    parser.add_argument(
        'input_dir',
        type=Path,
        help='Directory containing the note text files'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Output file path (extension determines format: .csv or .json)'
    )
    
    parser.add_argument(
        '-p', '--pattern',
        default='*.txt',
        help='Glob pattern for input files (default: *.txt)'
    )
    
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Use compact JSON formatting (only applies to JSON output)'
    )
    
    args = parser.parse_args()
    
    # Validate input directory
    if not args.input_dir.exists():
        print(f"Error: Input directory '{args.input_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not args.input_dir.is_dir():
        print(f"Error: '{args.input_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    # Process files
    records = process_directory(args.input_dir, args.pattern)
    
    if not records:
        print("No records to write. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Determine output format and write
    output_ext = args.output.suffix.lower()
    
    if output_ext == '.csv':
        write_csv(records, args.output)
    elif output_ext == '.json':
        write_json(records, args.output, pretty=not args.compact)
    else:
        print(f"Error: Unsupported output format '{output_ext}'. Use .csv or .json", 
              file=sys.stderr)
        sys.exit(1)
    
    print("Done!", file=sys.stderr)


if __name__ == '__main__':
    main()
