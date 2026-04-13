---
name: parser-self-heal
description: Analyze and self-correct fixed-width file parser by extracting filed layouts from documentation and comparing against code implementation. Identifies mismatches in field positions, lengths, and data types, and generates suggeted corrections to align code with documentation.
---

# Parser Self-Heal

## Goal

Detect and fix parsing errors in fixed-width file processors by comparing code against documentation and suggesting corrections to field positions, lengths, and data types.

## Workflow

1. Read documentation to extract expected field layouts (positions, lengths, data types).
2. If not already extracted, extract the PDF and ship a machine-readable file in references/ as a json with the field layouts.
3. Compare extracted layouts against the current code implementation.
4. Identify mismatches in field positions, lengths, and data types.
5. Generate suggested corrections to align code with documentation.
6. Apply corrections and validate the updated parser.

## Output format

Provide:
- Field layout extracted from documentation (field name, position, length, data type) stored in the reference folder as a json file.
- Apply code corrections to fix the mismatches.
- Create a file named "{parser}_analysis" with a list of identified mismatches with details (field name, expected vs actual positions, lengths, data types).
- Summary of changes made to the parser.

## Constraints

- Do not introduce new features or change existing functionality beyond correcting parsing errors.
- Ignore the existance of a legacy short version of the parser and only focus on the current implementation.
- Preserve code style and structure while applying corrections.
- Ensure that the corrected parser still passes all existing tests.
- Do not verge from the documented field layouts when suggesting corrections.
- Only read the documentation from the reference folder.

## Example triggers
- “Fix this fixed-width parser using the provided documentation.”
- “Detect parsing error and inconsistencies with the documentation, then suggest fixes.”
- $parser-self-heal: "Analyze the IRS parser code against the IRS documentation and correct any mismatches in field layouts."