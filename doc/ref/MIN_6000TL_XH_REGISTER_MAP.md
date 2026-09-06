# MIN 6000TL-XH register map

This is the resolved, read-only validation reference for the production MIN
6000TL-XH (`SNL0CGV020`). It is intentionally table-specific: FC03 holding
registers and FC04 input registers are separate address spaces even when the
numeric address is identical.

The machine-readable canonical overlay is
[`../min_6000tl_xh_register_map.json`](../min_6000tl_xh_register_map.json),
and the captured raw hardware evidence is
[`../min_6000tl_xh_live_validation.json`](../min_6000tl_xh_live_validation.json).

## Identification

| FC | Registers | Result |
|---|---:|---|
| FC03 | 0–29 | identity/configuration block; serial words 23–27 decode to `SNL0CGV020` |
| FC03 | 43 | `5100` device type code |
| FC03 | 44 | `513` (two trackers, one AC phase) |
| FC03 | 88 | `305` → Modbus version `3.05` |
| FC03 | 9–14 | firmware `AL1.0ZAba` followed by byte `0x1d`; preserve the exact HA value `AL1.0ZAba\u001d` |

## Resolved EMS holding map

The vendor table and OpenInverter agree that holding `3036–3059` is a hybrid
control/schedule area. The schedule words are packed minute/hour/priority/enable
fields; they are not telemetry. The live read was performed only to observe
current values and did not write them.

| FC03 | Meaning | Raw live value(s) |
|---:|---|---:|
| 3036 | Grid-first discharge rate (%) | 70 |
| 3037 | Grid-first stop SOC (%) | 10 |
| 3038–3045 | Grid-first schedule 1–4 start/end words | `14080, 5947, 40960, 1792, 8192, 1083, 0, 0` |
| 3046 | Reserved | 0 |
| 3047 | Battery-first charge rate (%) | 70 |
| 3048 | Battery-first stop SOC (%) | 90 |
| 3049 | AC charge enable | 0 (disabled) |
| 3050–3059 | Battery-first schedule 1–5 start/end words | all zero in read-only capture |
| 3079 | UPS/EPS function enable | 1 |
| 3080 | UPS/EPS voltage selection | 0 |
| 3081 | UPS/EPS frequency selection (`0=50 Hz`, `1=60 Hz`) | 0 |
| 3082 | Load-first stop SOC (%) | 0 |

Important conflict: FC03 `3081` is `UPSFreqSet`; FC04 `3081–3082` is the
high/low word pair for PV4 lifetime energy. The old family-wide manual data
type overlay incorrectly treated holding `3079–3082` as energy words. The
canonical MIN overlay keeps the two namespaces separate.

## Read-only input telemetry

| FC04 registers | Meaning | Encoding |
|---:|---|---|
| 3000 | inverter status | `1` = normal |
| 3001–3002 | total PV/input power | unsigned 32-bit / 10 W |
| 3003–3010 | PV1/PV2 voltage, current and power | voltage/current/power scales 10/10/10 |
| 3023–3024 | AC output power | unsigned 32-bit / 10 W |
| 3025 | grid frequency | / 100 Hz |
| 3026–3029 | single-phase AC voltage/current/power | / 10 V, / 10 A, / 10 W |
| 3041–3042 | power to user / grid import | signed 32-bit / 10 W |
| 3043–3044 | power to grid / export | signed 32-bit / 10 W |
| 3045–3046 | user load power | signed 32-bit / 10 W |
| 3047–3048 | inverter runtime | unsigned 32-bit / 7200 h |
| 3049–3050 | AC energy today | unsigned 32-bit / 10 kWh |
| 3079–3080 | PV4 energy today | unsigned 32-bit / 10 kWh |
| 3081–3082 | PV4 energy total | unsigned 32-bit / 10 kWh |
| 3169 | battery voltage | / 100 V |
| 3170 | battery current | signed / 10 A |
| 3171 | battery SOC | % |
| 3178–3179 | battery discharge power | signed 32-bit / 10 W |
| 3180–3181 | battery charge power | signed 32-bit / 10 W |
| 3212 | BMS status | vendor enum |
| 3215 | BMS SOC | % |
| 3216 | BMS voltage | / 100 V |
| 3217 | BMS current | signed / 100 A |
| 3222 | BMS SOH | % |

The capture window observed status `1`, 50.03 Hz, 211–213 V battery, 92–93%
SOC, 495–2,428 W discharge, 561–2,484.8 W load, and zero import/export.
The values are dynamic; the raw registers and capture windows are authoritative.

## Provenance and remaining uncertainty

Vendor protocol tables provide the primary naming and scale for the MIN/TL-XH
blocks. HA runtime mappings and Grott layouts independently corroborate FC04
telemetry and the 32-bit high/low word order. OpenInverter corroborates the
holding BDC/schedule interpretation and signed power-flow words. For battery
voltage, OpenInverter's `/10` multiplier is rejected for this hardware: the
live raw value `21146` is physically plausible as `211.46 V` using HA's `/100`
scale, while `2114.6 V` is not. Legacy generic storage manual mappings
remain useful for other families but must not override the MIN table-specific
interpretation above.

No writable entity or runtime integration code was changed by this validation.
All hardware access was FC03/FC04 read-only through broker `:5021`.
