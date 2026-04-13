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

## Coding Agents Assignment

### Problem Solved

At the Vudu team in Vestwell, a couple times a year we receive new fixed-width files that need to be parsed and later stored. Within this repo I created a codex skill that analize fixed-width files, compares them with given documentation and automatically fixes any inconsistency.

### Who is it for?

Any developer that whishes to debug and ensure his/her parsing functions follow a given documentation layout.

### How it works?

The Skill reads provided documentation to extract expected field layouts then it compares the extracted layouts against the current code implementation and identify mismatches in field positions, lengths, and data types. The expected output is that the skill generates suggested corrections to align code with documentation and applies corrections and validate the updated parser.
