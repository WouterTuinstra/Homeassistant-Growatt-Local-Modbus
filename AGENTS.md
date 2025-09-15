Nieuw
+42-0
# Agent Instructions

This repository tracks work on expanding Growatt inverter support for Home Assistant, focusing on the MIN 6000XH-TL inverter with battery. The register map is complete as far as currently determined (see `testing/growatt_registers.md`).

## Workflow / Tasks

1. **Normalize protocol specification**
  - Parse `testing/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.txt` into a structured register table (`registers.json`).
  - Record register number, function code, length, scale, unit, and description.
  - Document the script that generates the table in `testing/README.md`.

2. **Complete TL-XH register mapping**
  - Add attribute constants for unmapped registers in `custom_components/growatt_local/API/device_type/base.py`.
  - Update `custom_components/growatt_local/API/device_type/storage_120.py` so the `STORAGE_INPUT_REGISTERS_120_TL_XH` and `STORAGE_HOLDING_REGISTERS_120` structures cover all known registers.

3. **Surface registers as Home Assistant entities**
  - Extend `sensor_types/storage.py` (and `switch.py` if required) with sensor or switch descriptions for each new attribute.
  - Provide translations for each new entity in `translations/*.json`.

4. **Validate against hardware**
  - Use or extend `testing/read_registers.py` to poll added ranges and verify scaling on real hardware.
  - Compare results with external references and document discrepancies in `testing/growatt_registers.md`.

5. **Broker usage policy**
  - Keep this repo simulator-only. The external broker now lives beside this repository at `../growatt-rtu-broker` (under `external/`) and is used to create datasets or proxy live hardware; never add runtime dependencies on it inside `custom_components/growatt_local`.
  - When hardware access is required, run the broker (for example via its included Docker setup) and connect Home Assistant using TCP mode. All developer tests remain backed by `testing/modbus_simulator.py`.
  - Capture sessions with the broker's JSONL logging, convert them via `testing/compact_capture.py`, and commit only the curated datasets here.
  - Planned features such as virtual tty fan-out or capture helpers belong in the broker repo. This repository should only document how to consume them.

These steps are iterative; each commit should leave the repository in a working state with tests executed. For full developer and usage instructions, see the updated `README.md` and `testing/README.md`.
