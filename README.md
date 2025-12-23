# Epic Clinical Data Converter

This repository contains scripts to convert Epic clinical data exported as tab-separated text files into CSV or JSON format.

## Available Scripts

1. **process_epic_notes.py** - General-purpose converter for clinical notes and other data
2. **process_pathology_reports.py** - Specialized converter for pathology reports with automatic record merging

## Input Format

Each text file should contain:
- **Line 1**: Tab-separated column headers
- **Line 2+**: Tab-separated values (one or more data rows)

Example file content:
```
MRN	date	NOTE_ID	Note	Source	rowNum
12345	2024-01-15	N001	Patient presents with mild cough and fever.	Clinic A	1
12345	2024-01-16	N002	Follow-up visit. Patient symptoms improved.	Clinic A	2
```

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

---

## Script 1: process_epic_notes.py

General-purpose converter for clinical notes and other Epic data exports. Outputs all rows individually without merging.

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

---

## Script 2: process_pathology_reports.py

Specialized converter for Epic pathology reports that automatically merges related rows into consolidated records. Pathology reports are often exported with multiple rows per report, with each row containing a fragment of the report text. This script intelligently combines those fragments into complete reports.

### Key Differences from process_epic_notes.py

- **Automatic merging**: Groups rows by report identifiers (MRN, date, LabOrderEpicId, CaseName, SpecimenSource)
- **Ordered concatenation**: Uses ConcatenationLine and ConcatenationSubLine fields to maintain correct text order
- **Consolidated output**: Produces one record per complete pathology report instead of many fragmented rows
- **Cleaner fields**: Removes concatenation metadata fields from final output

### Input Format for Pathology Reports

Pathology report files contain multiple rows for each report:

```
MRN	date	LabOrderEpicId	CaseName	SpecimenSource	SpecimenType	ConcatenationLine	ConcatenationSubLine	ValueText
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	1	1	Bone marrow aspirate and biopsy:
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	1	2	- Findings consistent with diagnosis
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	1	3	- Additional observations noted
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	2	1	Laboratory Results:
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	2	2	WBC: 5.2 THOU/µL
10001	2024-01-15	400000001	SP99-12345	Bone Marrow	Tissue	2	3	HGB: 12.5 g/dL
```

These 6 rows will be merged into a single record with all ValueText concatenated in order.

### Usage

**Basic usage - merge pathology reports:**
```bash
python3 process_pathology_reports.py PathologyReports/ -o pathology_merged.json
```

**Output to CSV:**
```bash
python3 process_pathology_reports.py PathologyReports/ -o pathology_merged.csv
```

**Keep individual rows without merging:**
```bash
python3 process_pathology_reports.py PathologyReports/ -o pathology_raw.json --no-merge
```

**Compact JSON output:**
```bash
python3 process_pathology_reports.py PathologyReports/ -o pathology_merged.json --compact
```

### Command-Line Arguments

- `input_dir` (required): Directory containing pathology report text files
- `-o, --output` (required): Output file path (.csv or .json extension)
- `-p, --pattern`: Glob pattern for input files (default: `*.txt`)
- `--compact`: Use compact JSON formatting (only for JSON output)
- `--no-merge`: Skip merging and output individual rows as-is

### Merged vs Unmerged Output

**Unmerged (6 separate records):**
```json
[
  {
    "MRN": "10001",
    "date": "2024-01-15",
    "LabOrderEpicId": "400000001",
    "CaseName": "SP99-12345",
    "SpecimenSource": "Bone Marrow",
    "SpecimenType": "Tissue",
    "ConcatenationLine": "1",
    "ConcatenationSubLine": "1",
    "ValueText": "Bone marrow aspirate and biopsy:"
  },
  {
    "MRN": "10001",
    "date": "2024-01-15",
    "LabOrderEpicId": "400000001",
    "CaseName": "SP99-12345",
    "SpecimenSource": "Bone Marrow",
    "SpecimenType": "Tissue",
    "ConcatenationLine": "1",
    "ConcatenationSubLine": "2",
    "ValueText": "- Findings consistent with diagnosis"
  }
  ...
]
```

**Merged (1 consolidated record):**
```json
[
  {
    "MRN": "10001",
    "date": "2024-01-15",
    "LabOrderEpicId": "400000001",
    "CaseName": "SP99-12345",
    "SpecimenSource": "Bone Marrow",
    "SpecimenType": "Tissue",
    "ValueText": "Bone marrow aspirate and biopsy:\n- Findings consistent with diagnosis\n- Additional observations noted\nLaboratory Results:\nWBC: 5.2 THOU/µL\nHGB: 12.5 g/dL"
  }
]
```

### Merging Logic

Records are grouped by these key fields:
- **MRN**: Patient medical record number
- **date**: Date of the report
- **LabOrderEpicId**: Lab order identifier
- **CaseName**: Case identifier (e.g., SP99-12345)
- **SpecimenSource**: Specimen source description

Within each group, rows are sorted by `ConcatenationLine` and `ConcatenationSubLine`, then all `ValueText` values are joined with newline characters to reconstruct the complete report.

### When to Use Each Script

**Use process_epic_notes.py when:**
- Processing clinical notes (typically one row per note)
- You want individual rows preserved as separate records
- Data doesn't need to be merged

**Use process_pathology_reports.py when:**
- Processing pathology reports that span multiple rows
- You want complete reports consolidated into single records
- Data has ConcatenationLine/ConcatenationSubLine fields indicating row order
