# Documentation assets

This directory collects the source specification and machine-readable material
for Growatt's “Inverter Modbus RTU Protocol v1.24”, along with generated
reference docs for the Home Assistant `growatt_local` integration.

## Files

- `Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf` – original vendor
  specification. This is the canonical source for all other artefacts here.
- `growatt_registers_spec.json` – canonical extraction of the PDF register
  tables. Edits should be made here when updating the specification.
- `Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json` – raw
  per-row table export retained for traceability/debugging.
- `growatt_local_registers.json` – snapshot of the integration's register
  mappings, used when cross-referencing coverage.
- `render_register_spec.py` – regeneration script for the Markdown document.
- `growatt_registers_spec.md` – rendered human-friendly reference. Generated via
  `python render_register_spec.py` and should not be edited by hand.

## Updating / regenerating the documentation

The JSON files were produced by parsing the PDF tables and normalising them
into register records. The Markdown output is rendered programmatically to stay
in sync with those JSON sources.

1. Modify `growatt_registers_spec.json` and/or `growatt_local_registers.json` as
   required.
2. Run `python render_register_spec.py` from this directory (or `script/bootstrap`
   activated environment).
3. Commit the updated JSON and the regenerated Markdown together.

Regenerating each time keeps the Markdown and the source JSON in sync.
