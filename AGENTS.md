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
  - The broker project is **not** to be used directly in this repository for development or testing.
  - For dry-run and container testing, always use the Modbus simulator now provided by the broker package (`python -m growatt_broker.simulator.modbus_simulator`).
  - The broker may be used only to generate static datasets for the simulator, which should then be copied into the Growatt repo.
  - Do not add broker dependencies or startup logic to this repository.
  - See `testing/README.md` for simulator usage and dataset provenance.

These steps are iterative; each commit should leave the repository in a working state with tests executed. For full developer and usage instructions, see the updated `README.md` and `testing/README.md`.