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
- `normalize_register_spec.py` – cleans the spec JSON and enriches it with
  integration attribute metadata.
- `build_register_data_types.py` – derives reusable data type/scale definitions
  from the integration mapping.
- `growatt_register_data_types.json` – output catalogue produced by
  `build_register_data_types.py`.
- `growatt_registers_spec.md` – rendered human-friendly reference. Generated via
  `python render_register_spec.py` and should not be edited by hand.

## Updating / regenerating the documentation

The JSON files were produced by parsing the PDF tables and normalising them
into register records. The Markdown output is rendered programmatically to stay
in sync with those JSON sources.

1. Modify `growatt_registers_spec.json` and/or `growatt_local_registers.json` as
   required (or refresh them from the PDF extraction pipeline).
2. Run `python normalize_register_spec.py` to tidy the JSON and attach updated
   attribute mappings.
3. Run `python build_register_data_types.py` if the type catalogue needs to be
   refreshed.
4. Run `python render_register_spec.py` from this directory (or inside the
   `script/bootstrap` virtualenv).
5. Commit the updated JSON artefacts and the regenerated Markdown together.

Regenerating each time keeps the Markdown and the source JSON in sync.
