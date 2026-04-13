# IRS Parser Layout Analysis

Source used: `.codex/skills/parser-self-heal/references/irs.pdf` (Publication 1220, Part C record layouts).

## Mismatches Found

1. `T` record `CONTACT NAME`
- Expected: positions `304-343` (length `40`, text)
- Actual (before fix): positions `190-229` (length `40`)
- Impact: parser read company mailing address instead of contact name.

2. `T` record `CONTACT PHONE`
- Expected: positions `344-358` (length `15`, phone/extension text)
- Actual (before fix): positions `267-281` (length `15`)
- Impact: parser read unrelated field region, producing incorrect phone values.

3. `T` record `EMAIL`
- Expected: positions `359-408` (length `50`, alphanumeric)
- Actual (before fix): positions `304-343` (length `40`)
- Impact: parser read contact-name field instead of email and truncated width.

4. `B` record `PAYEE TIN` data type
- Expected: `12-20`, numeric identifier (fixed-width text that may include leading zeros)
- Actual (before fix): converted to `int`
- Impact: possible leading-zero loss and type drift from fixed-width spec semantics.

5. `B` record `PAYEE ZIP CODE` data type
- Expected: `490-498`, alphanumeric/fixed-width text
- Actual (before fix): converted to `int`
- Impact: possible leading-zero loss and inability to preserve non-numeric foreign ZIP/postal values.

## Notes

- Legacy/non-1220 layout branches were not used as the source of truth for this analysis.
- Only documented field position/length/type issues were corrected.
