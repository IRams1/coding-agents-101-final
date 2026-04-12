# Conversion Parsers

This repository contains a small Python CLI that parses IRS fixed-width input files and exports normalized CSV output with the option to add extra parsers.

## What The IRS Parser Does

- Reads IRS input records from a text file (`T`, `A`, `B`, `C`, `F` record types)
- Parses payer and payee information from fixed-width fields
- Writes the final output to `output/irs_output.csv`

## Project Structure

- `conversions.py`: CLI entrypoint
- `src/parsers/irs.py`: IRS parser implementation
- `src/file_handler.py`: File read/write helpers
- `input/`: Sample input files (for example `irs_full.txt`)
- `output/`: Generated CSV output
- `tests/`: Integration test fixtures and tests

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run The Conversion

From the repository root (`coding-agents-101-final`), run:

```bash
python -m conversions -r <provider> -f <filename>
```

| Flag | Description |
|------|-------------|
| `-r` / `--provider` | The parser to use. Currently supported: `irs` |
| `-f` / `--filename` | Path to the fixed-width input file to parse |

**Example:**

```bash
python -m conversions -r irs -f input/irs_full.txt
```

## Output

After running, the generated file is:

- `output/irs_output.csv`
