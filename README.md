# Epic Clinic Notes Converter

This script converts Epic clinic notes exported as tab-separated text files into CSV or JSON format.

## Input Format

Each text file should contain exactly two lines:
- **Line 1**: Tab-separated column headers
- **Line 2**: Tab-separated values

Example file content:
```
MRN	date	NOTE_ID	Note	Source	rowNum
12345	2024-01-15	N001	Patient presents with mild cough and fever.	Clinic A	1
```

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Usage

### Basic Usage

Convert all .txt files in a directory to CSV:
```bash
python3 process_epic_notes.py /path/to/notes/ -o output.csv
```

Convert all .txt files in a directory to JSON:
```bash
python3 process_epic_notes.py /path/to/notes/ -o output.json
```

### Advanced Options

**Process specific file patterns:**
```bash
python3 process_epic_notes.py /path/to/notes/ -o output.csv -p "note_*.txt"
```

**Compact JSON output (no pretty printing):**
```bash
python3 process_epic_notes.py /path/to/notes/ -o output.json --compact
```

### Command-Line Arguments

- `input_dir` (required): Directory containing the note text files
- `-o, --output` (required): Output file path (.csv or .json extension)
- `-p, --pattern`: Glob pattern for input files (default: `*.txt`)
- `--compact`: Use compact JSON formatting (only for JSON output)

### Help

View all options:
```bash
python3 process_epic_notes.py --help
```

## Examples

### Example 1: Convert all notes to CSV
```bash
python3 process_epic_notes.py ./clinic_notes/ -o all_notes.csv
```

### Example 2: Convert specific notes to JSON
```bash
python3 process_epic_notes.py ./clinic_notes/ -o filtered_notes.json -p "2024_*.txt"
```

### Example 3: Create compact JSON for API use
```bash
python3 process_epic_notes.py ./clinic_notes/ -o api_data.json --compact
```

## Features

- Processes multiple files in batch
- Handles mismatched header/value counts gracefully
- Supports both CSV and JSON output formats
- Maintains column order across files
- Provides detailed error messages
- UTF-8 encoding support for international characters
- Progress reporting during processing

## Error Handling

The script handles various edge cases:
- Files with fewer than 2 lines (skipped with warning)
- Mismatched number of headers and values (padded/truncated with warning)
- Empty directories (exits with error message)
- Invalid file paths (exits with error message)

## Output Formats

### CSV Output
- Standard comma-separated values
- Headers in first row
- UTF-8 encoded
- Compatible with Excel, Google Sheets, pandas, etc.

### JSON Output
- Array of objects
- Each object represents one note
- Pretty-printed by default (use `--compact` for minified output)
- UTF-8 encoded
- Compatible with most JSON parsers

## Troubleshooting

**"No files matching '*.txt' found"**
- Check that your input directory path is correct
- Verify that your files have the .txt extension
- Try using the `-p` option with a specific pattern

**"has X headers but Y values"**
- This warning indicates inconsistent data in a file
- The script will handle it automatically by padding or truncating
- Review the affected file if data integrity is critical

**"Input directory does not exist"**
- Double-check the path to your notes directory
- Use absolute paths if relative paths aren't working
