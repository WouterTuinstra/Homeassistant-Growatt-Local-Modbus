Nieuw
+42-0
# Agent Instructions

This repository tracks work on expanding Growatt inverter support for Home Assistant.
The following workflow outlines how to progressively map and expose the Growatt
register set, focusing on the MIN 6000TL XH inverter with battery.

## Workflow / Tasks

1. **Normalize protocol specification**
   - Parse `testing/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.txt` into a
     structured register table (`registers.json`).
   - Record register number, function code, length, scale, unit and description.
   - Document the script that generates the table in `testing/README.md`.

2. **Complete TL-XH register mapping**
   - Add attribute constants for unmapped registers in
     `custom_components/growatt_local/API/device_type/base.py`.
   - Update `custom_components/growatt_local/API/device_type/storage_120.py` so the
     `STORAGE_INPUT_REGISTERS_120_TL_XH` and `STORAGE_HOLDING_REGISTERS_120`
     structures cover all known registers.

3. **Surface registers as Home Assistant entities**
   - Extend `sensor_types/storage.py` (and `switch.py` if required) with sensor or
     switch descriptions for each new attribute.
   - Provide translations for each new entity in `translations/*.json`.

4. **Validate against hardware**
   - Use or extend `testing/read_registers.py` to poll added ranges and verify
     scaling on real hardware.
   - Compare results with external references and document discrepancies in
     `testing/growatt_registers.md`.

5. **Debug via Modbus broker**
   - Follow the strategy in `testing/Modbus sniffer adaptation.md`.
   - Run the Home Assistant Pi4 as a man-in-the-middle between the inverter and
     ShineWiFi, acting as the sole RTU master.
   - The Pi exposes a Modbus-TCP endpoint so both Home Assistant and laptop
     scripts in `testing/` can exercise the API without a full HA installation
     while capturing bus traffic for analysis.

These steps are expected to be iterative; each commit should strive to leave the
repository in a working state with tests executed.