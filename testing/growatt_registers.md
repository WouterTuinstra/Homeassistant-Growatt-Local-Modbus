# Growatt MIN 6000TL-XH Register Mapping (Modbus v1.20 / v1.24)

This document provides an expanded overview of the Growatt MIN 6000TL-XH inverter register map (protocol v1.20/v1.24), focusing on **all available holding and input registers up to ~3280** (beyond which BDC/BMS details exist but are not currently relevant).

Registers are clearly split between **Holding Registers (FC=03/06/16)** and **Input Registers (FC=04)**.

---

## 📖 Function Codes
- **Input Registers (Read-only)** – Function code 04
- **Holding Registers (Read/Write)** – Function codes 03 (read), 06 (write single), 16 (write multiple)

Reference: [Ozeki Modbus function codes](https://ozeki.hu/p_5873-modbus-function-codes.html)

---

# Holding Registers (FC=03/06/16)

### General Device Info (0–50)
| Register | Description | Unit | Integration Attribute | Notes |
|----------|-------------|------|------------------------|-------|
| 0        | Remote On/Off | - | `ATTR_INVERTER_ENABLED` | 0=Off, 1=On |
| 3        | Max active power % | % | - | Found active (100) |
| 5        | Power factor ×10000 | - | - | Found active |
| 7–8      | Normal power setting | VA | - | |
| 9–11     | Firmware version | ASCII | `ATTR_FIRMWARE` | high/mid/low |
| 12–14    | Control firmware version | ASCII | - | |
| 15       | LCD language | code | - | Found active (1=English) |
| 17       | PV start voltage | V | - | Found active (1000=100.0V) |
| 18       | Start time | s | - | Found active (60) |
| 19       | Restart delay after fault | s | - | Found active (60) |
| 20–21    | Power slope settings | %/s | - | Found active |
| 22       | Baud rate selection | - | - | 0=9600, 1=38400 |
| 23–27    | Serial number (ASCII) | str | `ATTR_SERIAL_NUMBER` | Found active |
| 28–29    | Inverter model | str | `ATTR_INVERTER_MODEL` | Parsed via `model()` |
| 30       | Communication address | - | - | Found active (1) |
| 31       | Flash update trigger | - | - | |

### Manufacturer / Type Info
| Register | Description | Attribute |
|----------|-------------|-----------|
| 34–41    | Manufacturer info | - |
| 43       | Device type code | `ATTR_DEVICE_TYPE_CODE` |
| 44       | Tracker + phase count | `ATTR_NUMBER_OF_TRACKERS_AND_PHASES` |

### System Time (45–50)
| Register | Description | Unit | Integration |
|----------|-------------|------|-------------|
| 45–50    | Device system time (Y/M/D/H/M/S) | - | Used in `get_device_info` |

### Grid Protection Settings (52–80)
Registers 52–80 define Vac/Freq protections, cycle times, and thresholds. These exist but are not yet mapped in HA.

### Firmware & Modbus
| Register | Description | Attribute |
|----------|-------------|-----------|
| 82–87    | FW build numbers (ASCII) | - |
| 88       | Modbus version ×100 | `ATTR_MODBUS_VERSION` |

### Country/Grid Codes & PF/QV Models (89–120+)
Various PF/Q(V) models, grid curves, and frequency derating settings appear here. These are advanced features not yet mapped.

---

# Input Registers (FC=04)

### Core PV/AC Measurements (0–124)
| Register | Description | Unit | Integration Attribute | Notes |
|----------|-------------|------|------------------------|-------|
| 0        | Status code | int | `ATTR_STATUS_CODE` |
| 1–2      | Total PV input power | W | `ATTR_INPUT_POWER` |
| 3–6      | PV1 V/A/P | V/A/W | `ATTR_INPUT_1_*` |
| 7–10     | PV2 V/A/P | V/A/W | `ATTR_INPUT_2_*` |
| 35       | Output power | W | `ATTR_OUTPUT_POWER` |
| 37       | Grid frequency | Hz | `ATTR_GRID_FREQUENCY` |
| 38–40    | AC1 V/A/P | V/A/W | `ATTR_OUTPUT_1_*` |
| 53–54    | Today’s output energy | kWh | `ATTR_OUTPUT_ENERGY_TODAY` |
| 55–56    | Total output energy | kWh | `ATTR_OUTPUT_ENERGY_TOTAL` |
| 57–58    | Operation hours | h | `ATTR_OPERATION_HOURS` |
| 59–66    | PV1+PV2 today & total energy | kWh | `ATTR_INPUT_*_ENERGY_*` |
| 91–92    | PV total energy | kWh | `ATTR_INPUT_ENERGY_TOTAL` |
| 93       | Inverter temp | °C | `ATTR_TEMPERATURE` |
| 94       | IPM temp | °C | `ATTR_IPM_TEMPERATURE` |
| 98       | P-bus voltage | V | `ATTR_P_BUS_VOLTAGE` |
| 99       | N-bus voltage | V | `ATTR_N_BUS_VOLTAGE` |
| 101      | Output % | % | `ATTR_OUTPUT_PERCENTAGE` |
| 104      | Derating mode | - | `ATTR_DERATING_MODE` |
| 105      | Fault code | - | `ATTR_FAULT_CODE` |
| 110      | Warning code | - | `ATTR_WARNING_CODE` |

### Extended Measurements (3000–3124)
Mirror of 0–124, but also includes:
- 3021: Reactive power → `ATTR_OUTPUT_REACTIVE_POWER`
- 3047: Operation hours (duplicate)
- 3067–3074: To-user / To-grid energy stats → `ATTR_ENERGY_TO_*`

### Battery & Hybrid (3125–3249)
| Register | Description | Unit | Attribute |
|----------|-------------|------|-----------|
| 3125–3126| Battery discharge today | kWh | `ATTR_DISCHARGE_ENERGY_TODAY` |
| 3127–3128| Battery discharge total | kWh | `ATTR_DISCHARGE_ENERGY_TOTAL` |
| 3129–3130| Battery charge today | kWh | `ATTR_CHARGE_ENERGY_TODAY` |
| 3131–3132| Battery charge total | kWh | `ATTR_CHARGE_ENERGY_TOTAL` |
| 3164     | BDC new flag | - | `ATTR_BDC_NEW_FLAG` |
| 3171     | Battery SOC % | % | `ATTR_SOC_PERCENTAGE` |
| 3176     | Battery temp A | °C | `ATTR_BATTERY_TEMPERATURE_A` |
| 3177     | Battery temp B | °C | `ATTR_BATTERY_TEMPERATURE_B` |
| 3178–3179| Battery discharge power | W | `ATTR_DISCHARGE_POWER` |
| 3180–3181| Battery charge power | W | `ATTR_CHARGE_POWER` |

### Reserved / Misc (3250–3280)
Registers are undocumented in spec but active in scans (SOC, currents, extra power flows). Candidate mapping area for future attributes.

---

# ✅ Attributes To Add (from scans & spec)

These registers should eventually be mapped in HA:
- `ATTR_INPUT_3_*`, `ATTR_INPUT_4_*` … up to PV8 (addresses 11–33, 61–89)
- `ATTR_OUTPUT_2_*`, `ATTR_OUTPUT_3_*` (AC2/AC3 volt/amp/power)
- `ATTR_ENERGY_TO_USER_TODAY` / `_TOTAL` (3067–3070)
- `ATTR_ENERGY_TO_GRID_TODAY` / `_TOTAL` (3071–3074)
- `ATTR_DISCHARGE_ENERGY_TODAY` / `_TOTAL` (3125–3128)
- `ATTR_CHARGE_ENERGY_TODAY` / `_TOTAL` (3129–3132)
- `ATTR_BDC_NEW_FLAG` (3164)
- `ATTR_SOC_PERCENTAGE` (3171)
- `ATTR_BATTERY_TEMPERATURE_A/B` (3176–3177)
- `ATTR_DISCHARGE_POWER` (3178)
- `ATTR_CHARGE_POWER` (3180)

---

📌 With this mapping, you now have a **nearly complete overview** of MIN 6000TL-XH registers (input & holding), up to 3280. BDC/BMS registers >4000 are ignored for now.


---

# 🔄 Update: TL‑XH Input vs Holding, Expanded Ranges (up to 3280)

## Function Codes & Access

- **Input registers (FC=04)**: read‑only measurements & counters.
- **Holding registers (FC=03)**: readable configuration/state; write via **FC=06** (single) or **FC=16** (multiple). Matches Growatt v1.24 and standard Modbus usage.

## Scope & Ranges (MIN 6000TL‑XH observed)

- **Input (RO)**: `0–124`, and **TL‑XH input blocks `≥3000`**: `3000–3124`, `3125–3249`, `3250–3280` (observed active). *All input registers ≥3000 are treated as TL‑XH sets.*
- **Holding (R/W)**: `0–120+` core, plus model/feature blocks (e.g., `28–31`, `34–45`, `52–80`, `88–99`) and **TL‑XH holding blocks `≥3000`** (e.g., `3001+`, `3049`).

---


# Input Registers (RO)

## (0–124)

| Register | Name / Description        | Unit   | Integration Attribute | Register Set |
|----------|---------------------------|--------|------------------------|--------------|
| 0        | Status code               | –      | `ATTR_STATUS_CODE`     | INPUT_REGISTERS_120 |
| 1–2      | PV total input power      | W      | `ATTR_INPUT_POWER`     | INPUT_REGISTERS_120 |
| 3        | PV1 voltage               | V      | `ATTR_INPUT_1_VOLTAGE` | INPUT_REGISTERS_120 |
| 4        | PV1 current               | A      | `ATTR_INPUT_1_AMPERAGE`| INPUT_REGISTERS_120 |
| 5–6      | PV1 power                 | W      | `ATTR_INPUT_1_POWER`   | INPUT_REGISTERS_120 |
| 7        | PV2 voltage               | V      | `ATTR_INPUT_2_VOLTAGE` | INPUT_REGISTERS_120 |
| 8        | PV2 current               | A      | `ATTR_INPUT_2_AMPERAGE`| INPUT_REGISTERS_120 |
| 9–10     | PV2 power                 | W      | `ATTR_INPUT_2_POWER`   | INPUT_REGISTERS_120 |
| 11       | PV3 voltage               | V      | `ATTR_INPUT_3_VOLTAGE` | INPUT_REGISTERS_120 |
| 12       | PV3 current               | A      | `ATTR_INPUT_3_AMPERAGE`| INPUT_REGISTERS_120 |
| 13–14    | PV3 power                 | W      | `ATTR_INPUT_3_POWER`   | INPUT_REGISTERS_120 |
| 15       | PV4 voltage               | V      | `ATTR_INPUT_4_VOLTAGE` | INPUT_REGISTERS_120 |
| 16       | PV4 current               | A      | `ATTR_INPUT_4_AMPERAGE`| INPUT_REGISTERS_120 |
| 17–18    | PV4 power                 | W      | `ATTR_INPUT_4_POWER`   | INPUT_REGISTERS_120 |
| 35       | Output (AC) power         | W      | `ATTR_OUTPUT_POWER`    | INPUT_REGISTERS_120 |
| 37       | Grid frequency            | Hz     | `ATTR_GRID_FREQUENCY`  | INPUT_REGISTERS_120 |
| 38       | AC1 voltage               | V      | `ATTR_OUTPUT_1_VOLTAGE`| INPUT_REGISTERS_120 |
| 39       | AC1 current               | A      | `ATTR_OUTPUT_1_AMPERAGE`| INPUT_REGISTERS_120 |
| 40–41    | AC1 power                 | W      | `ATTR_OUTPUT_1_POWER`  | INPUT_REGISTERS_120 |
| 42–48    | AC2/AC3 (3‑phase models)  | –      | `ATTR_OUTPUT_2_*`, `ATTR_OUTPUT_3_*` | INPUT_REGISTERS_120 |
| 53–54    | Today’s output energy     | kWh    | `ATTR_OUTPUT_ENERGY_TODAY` | INPUT_REGISTERS_120 |
| 55–56    | Total output energy       | kWh    | `ATTR_OUTPUT_ENERGY_TOTAL` | INPUT_REGISTERS_120 |
| 57–58    | Operation hours           | h      | `ATTR_OPERATION_HOURS` | INPUT_REGISTERS_120 |
| 59–60    | PV1 today’s energy        | kWh    | `ATTR_INPUT_1_ENERGY_TODAY` | INPUT_REGISTERS_120 |
| 61–62    | PV1 total energy          | kWh    | `ATTR_INPUT_1_ENERGY_TOTAL` | INPUT_REGISTERS_120 |
| 63–64    | PV2 today’s energy        | kWh    | `ATTR_INPUT_2_ENERGY_TODAY` | INPUT_REGISTERS_120 |
| 65–66    | PV2 total energy          | kWh    | `ATTR_INPUT_2_ENERGY_TOTAL` | INPUT_REGISTERS_120 |
| 91–92    | PV total energy           | kWh    | `ATTR_INPUT_ENERGY_TOTAL` | INPUT_REGISTERS_120 |
| 93       | Inverter temperature      | °C     | `ATTR_TEMPERATURE`     | INPUT_REGISTERS_120 |
| 94       | IPM temperature           | °C     | `ATTR_IPM_TEMPERATURE` | INPUT_REGISTERS_120 |
| 98       | DC bus voltage P          | V      | `ATTR_P_BUS_VOLTAGE`   | INPUT_REGISTERS_120 |
| 99       | DC bus voltage N          | V      | `ATTR_N_BUS_VOLTAGE`   | INPUT_REGISTERS_120 |
| 101      | Real output %             | %      | `ATTR_OUTPUT_PERCENTAGE` | INPUT_REGISTERS_120 |
| 104      | Derating mode             | –      | `ATTR_DERATING_MODE`   | INPUT_REGISTERS_120 |
| 105      | Fault code                | –      | `ATTR_FAULT_CODE`      | INPUT_REGISTERS_120 |
| 110      | Warning code              | –      | `ATTR_WARNING_CODE`    | INPUT_REGISTERS_120 |

---

## (3000–3124)

(Primarily mirrors 0–124 with hybrid/energy‑flow stats.)

| Register | Name / Description         | Unit | Integration Attribute | Register Set |
|----------|----------------------------|------|------------------------|--------------|
| 3000     | Status code                | –    | `ATTR_STATUS_CODE`     | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3001–3002| PV total input power       | W    | `ATTR_INPUT_POWER`     | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3021     | Output reactive power      | Var  | `ATTR_OUTPUT_REACTIVE_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3023–3024| Output (AC) power          | W    | `ATTR_OUTPUT_POWER`    | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3025     | Grid frequency             | Hz   | `ATTR_GRID_FREQUENCY`  | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3026     | AC1 voltage                | V    | `ATTR_OUTPUT_1_VOLTAGE`| STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3027     | AC1 current                | A    | `ATTR_OUTPUT_1_AMPERAGE`| STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3028–3029| AC1 power                  | W    | `ATTR_OUTPUT_1_POWER`  | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3041–3042| Power to user (instant)    | W    | `ATTR_POWER_TO_USER`   | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3043–3044| Power to grid (instant)    | W    | `ATTR_POWER_TO_GRID`   | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3045–3046| User load power (instant)  | W    | `ATTR_POWER_USER_LOAD` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3047–3048| Operation hours            | h    | `ATTR_OPERATION_HOURS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3049–3050| Today’s output energy      | kWh  | `ATTR_OUTPUT_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3051–3052| Total output energy        | kWh  | `ATTR_OUTPUT_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3053–3054| Total PV input energy      | kWh  | `ATTR_INPUT_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3055–3062| PV1/PV2 energy today/total | kWh  | `ATTR_INPUT_*_ENERGY_*`| STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3067–3068| Energy to user today       | kWh  | `ATTR_ENERGY_TO_USER_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3069–3070| Energy to user total       | kWh  | `ATTR_ENERGY_TO_USER_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3071–3072| Energy to grid today       | kWh  | `ATTR_ENERGY_TO_GRID_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3073–3074| Energy to grid total       | kWh  | `ATTR_ENERGY_TO_GRID_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3093     | Inverter temperature       | °C   | `ATTR_TEMPERATURE`     | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3094     | IPM temperature            | °C   | `ATTR_IPM_TEMPERATURE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3098     | DC bus voltage P           | V    | `ATTR_P_BUS_VOLTAGE`   | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3099     | DC bus voltage N           | V    | `ATTR_N_BUS_VOLTAGE`   | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3100–3101| Real output %              | %    | `ATTR_OUTPUT_PERCENTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3105     | Fault code                 | –    | `ATTR_FAULT_CODE`      | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3110     | Warning code               | –    | `ATTR_WARNING_CODE`    | STORAGE_INPUT_REGISTERS_120_TL_XH |

---

## (3125–3249) — TL‑XH Battery Block

| Register | Name / Description            | Unit | Integration Attribute              | Register Set |
|----------|-------------------------------|------|------------------------------------|--------------|
| 3125–3126| Discharge energy today        | kWh  | `ATTR_DISCHARGE_ENERGY_TODAY`      | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3127–3128| Discharge energy total        | kWh  | `ATTR_DISCHARGE_ENERGY_TOTAL`      | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3129–3130| Charge energy today           | kWh  | `ATTR_CHARGE_ENERGY_TODAY`         | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3131–3132| Charge energy total           | kWh  | `ATTR_CHARGE_ENERGY_TOTAL`         | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3161     | Battery rated capacity (?)    | –    | –                                  | – |
| 3163     | Battery nominal voltage (?)   | V    | –                                  | – |
| 3164     | BDC new flag                  | –    | `ATTR_BDC_NEW_FLAG`                | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3165–3166| BMS/BDC status code(s) (?)    | –    | –                                  | – |
| 3169–3170| Battery model/code / flags (?)| –    | –                                  | – |
| 3171     | SoC                           | %    | `ATTR_SOC_PERCENTAGE`              | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3172–3173| Battery voltages (A/B) (?)    | V    | – (`ATTR_BATTERY_VOLTAGE` pending) | – |
| 3174–3175| Pack string count / status (?)| –    | –                                  | – |
| 3176     | Battery temperature A         | °C   | `ATTR_BATTERY_TEMPERATURE_A`       | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3177     | Battery temperature B         | °C   | `ATTR_BATTERY_TEMPERATURE_B`       | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3178–3179| Discharge power (instant)     | W    | `ATTR_DISCHARGE_POWER`             | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3180–3181| Charge power (instant)        | W    | `ATTR_CHARGE_POWER`                | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3183–3185| Battery V/I derived fields (?)| –    | –                                  | – |
| 3190–3195| SoH/limits/status (observed)  | –    | –                                  | – |
| 3200–3201| Charge/discharge limit (%) (?)| %    | –                                  | – |
| 3212     | Battery cycles (observed)     | –    | –                                  | – |
| 3215–3224| BMS power/energy caps (obs.)  | –    | –                                  | – |
| 3227     | Rated power (?)               | W    | –                                  | – |
| 3230–3235| BMS flags / pack count (obs.) | –    | –                                  | – |
| 3241–3248| Model & version (echo)        | –    | –                                  | – |

### Spec‑documented TL‑XH debug/diagnostic inputs (examples)

> Per the v1.24 spec, many addresses in this area are **documented** as diagnostic or reserved. Notable examples you observed:

| Register | Name (per v1.24)                                 | Note |
|----------|--------------------------------------------------|------|
| 3069–3070| 32‑bit field (pair)                              | Your scan shows 3070 populated; treat 3069–3070 as one 32‑bit value.
| 3097     | Communication board temperature                  | Observed non‑zero in scan.
| 3111     | PresentFFTValue \[CHANNEL_A]                     | Diagnostic FFT bin.
| 3115     | Inverter start delay time                        | Matches observed value.

**32‑bit convention:** For these TL‑XH input blocks, 32‑bit values are exposed as **two consecutive 16‑bit words**. The integration already combines pairs as `(hi<<16) + lo` (big‑endian words), consistent with your scan and current code.

---
-------|-------------------------------|------|------------------------------------|--------------|
| 3125–3126| Discharge energy today        | kWh  | `ATTR_DISCHARGE_ENERGY_TODAY`      | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3127–3128| Discharge energy total        | kWh  | `ATTR_DISCHARGE_ENERGY_TOTAL`      | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3129–3130| Charge energy today           | kWh  | `ATTR_CHARGE_ENERGY_TODAY`         | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3131–3132| Charge energy total           | kWh  | `ATTR_CHARGE_ENERGY_TOTAL`         | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3161     | Battery rated capacity (?)    | –    | –                                  | – |
| 3163     | Battery nominal voltage (?)   | V    | –                                  | – |
| 3164     | BDC new flag                  | –    | `ATTR_BDC_NEW_FLAG`                | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3165–3166| BMS/BDC status code(s) (?)    | –    | –                                  | – |
| 3169–3170| Battery model/code / flags (?)| –    | –                                  | – |
| 3171     | SoC                           | %    | `ATTR_SOC_PERCENTAGE`              | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3172–3173| Battery voltages (A/B) (?)    | V    | – (`ATTR_BATTERY_VOLTAGE` pending) | – |
| 3174–3175| Pack string count / status (?)| –    | –                                  | – |
| 3176     | Battery temperature A         | °C   | `ATTR_BATTERY_TEMPERATURE_A`       | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3177     | Battery temperature B         | °C   | `ATTR_BATTERY_TEMPERATURE_B`       | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3178–3179| Discharge power (instant)     | W    | `ATTR_DISCHARGE_POWER`             | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3180–3181| Charge power (instant)        | W    | `ATTR_CHARGE_POWER`                | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3183–3185| Battery V/I derived fields (?)| –    | –                                  | – |
| 3190–3195| SoH/limits/status (observed)  | –    | –                                  | – |
| 3200–3201| Charge/discharge limit (%) (?)| %    | –                                  | – |
| 3212     | Battery cycles (observed)     | –    | –                                  | – |
| 3215–3224| BMS power/energy caps (obs.)  | –    | –                                  | – |
| 3227     | Rated power (?)               | W    | –                                  | – |
| 3230–3235| BMS flags / pack count (obs.) | –    | –                                  | – |
| 3241–3248| Model & version (echo)        | –    | –                                  | – |

> **Note**: Items marked **(?)** are observed active but not explicitly named in v1.24 public tables. Keep them listed so we can bind once clarified; see **Attributes to Add**.

---

## (3250–3280 observed)

| Register | Name / Description | Unit | Integration Attribute | Register Set |
|----------|--------------------|------|------------------------|--------------|
| 3250–3280| Reserved/Hybrid ext. (active on TL‑XH, details TBD) | – | – | – |

> Current integration: no attributes bound in this block; keep for future use.

---

# Holding Registers (R/W)

## Core (0–120+)

| Register | Name / Description                       | Unit | Integration Attribute          | Register Set |
|----------|------------------------------------------|------|--------------------------------|--------------|
| 0        | Remote On/Off (Inverter/BDC)             | –    | `ATTR_INVERTER_ENABLED`        | HOLDING_REGISTERS_120 |
| 1        | Safety function enable bits              | –    | –                              | HOLDING_REGISTERS_120 |
| 2        | PF CMD memory state                      | –    | –                              | HOLDING_REGISTERS_120 |
| 3        | Active P rate (limit %)                  | %    | –                              | HOLDING_REGISTERS_120 |
| 4        | Reactive P rate (limit %)                | %    | –                              | HOLDING_REGISTERS_120 |
| 5        | Power factor ×10000                      | –    | –                              | HOLDING_REGISTERS_120 |
| 6–7      | Pmax (high/low)                          | VA   | –                              | HOLDING_REGISTERS_120 |
| 8        | Vnormal (PV work voltage)                | V    | –                              | HOLDING_REGISTERS_120 |
| 9–11     | Firmware version (H/M/L)                 | –    | `ATTR_FIRMWARE`                | HOLDING_REGISTERS_120 |
| 12–14    | Control FW version (H/M/L)               | –    | –                              | HOLDING_REGISTERS_120 |
| 15       | LCD language                             | –    | –                              | HOLDING_REGISTERS_120 |
| 16       | Country selected                         | –    | –                              | HOLDING_REGISTERS_120 |
| 17       | PV start voltage                         | V    | –                              | HOLDING_REGISTERS_120 |
| 18–19    | Start / Restart delay                    | s    | –                              | HOLDING_REGISTERS_120 |
| 20–21    | Power start / restart slope              | 0.1% | –                              | HOLDING_REGISTERS_120 |
| 22       | Baudrate select (0=9600,1=38400)         | –    | –                              | HOLDING_REGISTERS_120 |
| 23–27    | Serial number (1–10)                     | –    | `ATTR_SERIAL_NUMBER`           | HOLDING_REGISTERS_120 |
| 28–29    | Inverter Module (model code)             | –    | `ATTR_INVERTER_MODEL`          | HOLDING_REGISTERS_120 |
| 30       | Modbus address                           | –    | –                              | HOLDING_REGISTERS_120 |
| 31       | FlashStart (FW update)                   | –    | –                              | HOLDING_REGISTERS_120 |
| 32–33    | Reset user info / factory                | –    | –                              | HOLDING_REGISTERS_120 |
| 34–41    | Manufacturer info (8..1)                 | –    | –                              | HOLDING_REGISTERS_120 |
| 42       | G100 fail safe                           | –    | –                              | HOLDING_REGISTERS_120 |
| 43       | Device Type Code                         | –    | `ATTR_DEVICE_TYPE_CODE`        | HOLDING_REGISTERS_120 |
| 44       | Trackers & phases                        | –    | `ATTR_NUMBER_OF_TRACKERS_AND_PHASES` | HOLDING_REGISTERS_120 |
| 45–51    | System time (Y/M/D/h/m/s/weekday)        | –    | –                              | HOLDING_REGISTERS_120 |
| 52–67    | Grid protection limits                   | –    | –                              | HOLDING_REGISTERS_120 |
| 68–79    | Grid protection times                    | –    | –                              | HOLDING_REGISTERS_120 |
| 80–81    | 10‑min voltage / PV over‑V fault         | –    | –                              | HOLDING_REGISTERS_120 |
| 82–87    | FW build numbers                         | –    | –                              | HOLDING_REGISTERS_120 |
| 88       | Modbus version ×100                      | –    | `ATTR_MODBUS_VERSION`          | HOLDING_REGISTERS_120 |
| 89–99    | PF/Q(V)/derating controls                | –    | –                              | HOLDING_REGISTERS_120 |

> Your scan also shows active blocks in 120+, 125+, 142+, 176+, 209+, and 3001+ (serial echo). Keep these logged; most are model/protection profiles.

## Hybrid / Extended Holding (TL‑XH)

For TL‑XH systems we should introduce a dedicated holding set:

- **Set name**: `STORAGE_HOLDING_REGISTERS_120_TL_XH`
- Purpose: all holding registers ≥3000 for TL‑XH hybrid inverters.

| Register | Name / Description             | Unit | Integration Attribute       | Notes |
|----------|--------------------------------|------|-----------------------------|-------|
| 3001–3015| Serial number (ASCII, 15 words)| –    | `ATTR_SERIAL_NUMBER`        | Already used by integration (mappable to TL‑XH set)
| 3049     | AC charge enable               | –    | `ATTR_AC_CHARGE_ENABLED`    | Move here from generic storage holding

---

# Attributes to Add / Bind (TL‑XH)

Use the list below to extend tables in your device modules (copy/paste). **All registers ≥3000 are mapped to TL‑XH sets**:

- `ATTR_POWER_TO_USER` → **3041–3042** (W), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_POWER_TO_GRID` → **3043–3044** (W), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_POWER_USER_LOAD` → **3045–3046** (W), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_ENERGY_TO_USER_TODAY` → **3067–3068** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_ENERGY_TO_USER_TOTAL` → **3069–3070** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_ENERGY_TO_GRID_TODAY` → **3071–3072** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_ENERGY_TO_GRID_TOTAL` → **3073–3074** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_OUTPUT_REACTIVE_POWER` → **3021** (Var), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_SOC_PERCENTAGE` → **3171** (%), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_BDC_NEW_FLAG` → **3164** (–), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_BATTERY_TEMPERATURE_A` → **3176** (°C), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_BATTERY_TEMPERATURE_B` → **3177** (°C), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_DISCHARGE_POWER` → **3178–3179** (W), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_CHARGE_POWER` → **3180–3181** (W), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_DISCHARGE_ENERGY_TODAY` → **3125–3126** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_DISCHARGE_ENERGY_TOTAL` → **3127–3128** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_CHARGE_ENERGY_TODAY` → **3129–3130** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`
- `ATTR_CHARGE_ENERGY_TOTAL` → **3131–3132** (kWh), set: `STORAGE_INPUT_REGISTERS_120_TL_XH`

**Candidates (confirm spec / add new attributes if missing):**

- `ATTR_BATTERY_VOLTAGE` / `ATTR_BATTERY_CURRENT` around **3172–3175**, **3183–3185**
- `ATTR_BATTERY_CYCLE_COUNT` at **3212**; charge/discharge limits around **3200–3201**
- Extended hybrid block **3250–3280** (reserve until named by a newer spec)

---

# Mirror Index (Inputs): Confirmed 1:1 Pairs

> These pairs have matching values in your scans and should map to the **same attributes**.

| Low Range | High Range | Attribute / Meaning                 |
|-----------|------------|-------------------------------------|
| 0         | 3000       | `ATTR_STATUS_CODE`                  |
| 1–2       | 3001–3002  | `ATTR_INPUT_POWER` (PV total W)     |
| 3         | 3003       | `ATTR_INPUT_1_VOLTAGE`              |
| 4         | 3004       | `ATTR_INPUT_1_AMPERAGE`             |
| 5–6       | 3005–3006  | `ATTR_INPUT_1_POWER`                |
| 7         | 3007       | `ATTR_INPUT_2_VOLTAGE`              |
| 8         | 3008       | `ATTR_INPUT_2_AMPERAGE`             |
| 9–10      | 3009–3010  | `ATTR_INPUT_2_POWER`                |
| 35        | 3023       | `ATTR_OUTPUT_POWER`                 |
| 37        | 3025       | `ATTR_GRID_FREQUENCY`               |
| 38        | 3026       | `ATTR_OUTPUT_1_VOLTAGE`             |
| 39        | 3027       | `ATTR_OUTPUT_1_AMPERAGE`            |
| 40–41     | 3028–3029  | `ATTR_OUTPUT_1_POWER`               |
| 53–54     | 3049–3050  | `ATTR_OUTPUT_ENERGY_TODAY`          |
| 55–56     | 3051–3052  | `ATTR_OUTPUT_ENERGY_TOTAL`          |
| 59–60     | 3055–3056  | `ATTR_INPUT_1_ENERGY_TODAY`         |
| 61–62     | 3057–3058  | `ATTR_INPUT_1_ENERGY_TOTAL`         |
| 63–64     | 3059–3060  | `ATTR_INPUT_2_ENERGY_TODAY`         |
| 65–66     | 3061–3062  | `ATTR_INPUT_2_ENERGY_TOTAL`         |
| 91–92     | 3053–3054  | `ATTR_INPUT_ENERGY_TOTAL`           |
| 93        | 3093       | `ATTR_TEMPERATURE` (inverter °C)    |
| 94        | 3094       | `ATTR_IPM_TEMPERATURE`              |
| 98        | 3098       | `ATTR_P_BUS_VOLTAGE`                |
| 99        | 3099       | `ATTR_N_BUS_VOLTAGE`                |
| 101       | 3100–3101  | `ATTR_OUTPUT_PERCENTAGE`            |
| 104       | 3086       | `ATTR_DERATING_MODE`                |
| 105       | 3105       | `ATTR_FAULT_CODE`                   |
| 110       | 3110       | `ATTR_WARNING_CODE`                 |

> Hybrid‑only metrics (power/energy to user/grid) exist **only** in ≥3000.

---

# Observed Undocumented Registers (for reverse‑engineering)

Below are registers that returned non‑zero in your scans and are **not yet mapped** in the integration. Where the v1.24 spec provides names, we’ve promoted them to the main tables (and removed from this list). What remains here are still‑unnamed items to revisit.

## Inputs (RO)

> **Note:** You indicated that **all TL‑XH input registers up to 3280 are documented** in v1.24 (some as debug/reserved). We therefore removed items like **182 (DSP067 Debug Data1)**, **189 (Debug Data8)**, **3097 (Comm board temperature)**, **3111 (PresentFFTValue A)**, **3115 (inv start delay)** from this “undocumented” list and reflected them in the main sections.

| Register | Observed Value | Comment |
|----------|----------------|---------|
| 285 | 6 | Likely debug counter (spec may define; pending review)
| 287 | 6 | ″
| 289 | 8 | ″
| 291 | 6 | ″
| 293 | 16 | ″
| 295 | 23 | ″
| 297 | 23 | ″
| 299 | 22 | ″
| 301 | 26 | ″
| 303 | 31 | ″
| 305 | 32 | ″
| 307 | 32 | ″
| 309 | 18 | ″
| 311 | 4  | ″
| 313 | 2  | ″
| 315 | 2  | ″
| 317 | 3  | ″
| 319 | 2  | ″
| 321 | 2  | ″
| 323 | 2  | ″
| 325 | 2  | ″
| 327 | 2  | ″
| 329 | 5  | ″
| 331 | 5  | ″
| 333 | 275| ″
| 335 | 268| ″
| 337 | 258| ″
| 339 | 225| ″
| 341 | 142| ″
| 343 | 99 | ″
| 345 | 248| ″
| 347 | 1267| ″
| 349 | 6772| ″
| 351 | 5659| ″
| 365 | 341| ″
| 376 | 14039| ″
| 802 | 1  | ″
| 815 | 6829| ″

**TL‑XH input (≥3000) pairs / reserved values (kept for tracking even if named in spec):**

| Register(s) | Observed Value | Comment |
|-------------|----------------|---------|
| 3069–3070   | 1643           | 32‑bit value (pair) — keep visible for correlation tests |
| 3072        | 181            | Likely part of a series of debug counters |
| 3074        | 6425           | ″ |
| 3076        | 118            | ″ |
| 3078        | 9968           | ″ |
| 3084        | 287            | ″ |
| 3087        | -6             | ″ |
| 3122        | 7144           | ″ |
| 3124        | 290            | ″ |
| 3126        | 53             | ″ |
| 3128        | 2240           | ″ |
| 3130        | 50             | ″ |
| 3132        | 2381           | ″ |
| 3136        | 44             | ″ |
| 3138        | 14799          | ″ |
| 3140        | 109            | ″ |
| 3142        | 8376           | ″ |
| 3161        | 10000          | ″ (may be rated capacity) |
| 3163        | 3900           | ″ (nominal voltage?) |
| 3165        | 22             | ″ (status code?) |
| 3166        | 513            | ″ |
| 3169        | 21017          | ″ (model/code?) |
| 3170        | 33             | ″ |
| 3172        | 3899           | ″ |
| 3173        | 1988           | ″ |
| 3174        | 15             | ″ |
| 3175        | 15             | ″ |
| 3179        | 7080           | ″ |
| 3183        | 2240           | ″ |
| 3185        | 2381           | ″ |
| 3187        | 3              | ″ |
| 3188        | 1911           | ″ |
| 3189        | 59             | ″ |
| 3190        | 41             | ″ |
| 3192        | 310            | ″ |
| 3193        | 287            | ″ |
| 3194        | 2              | ″ |
| 3195        | 14             | ″ |
| 3198        | 1              | ″ |
| 3200        | 50             | ″ |
| 3201        | 50             | ″ |
| 3212        | 2              | ″ (cycles?) |
| 3215        | 63             | ″ |
| 3216        | 21000          | ″ |
| 3217        | -340           | ″ |
| 3218        | 480            | ″ |
| 3219        | 2500           | ″ |
| 3220        | 2500           | ″ |
| 3222        | 100            | ″ |
| 3223        | 22720          | ″ |
| 3224        | 18880          | ″ |
| 3227        | 10536          | ″ |
| 3230        | 3269           | ″ |
| 3231        | 3265           | ″ |
| 3232        | 21010          | ″ |
| 3234        | 1              | ″ |
| 3235        | 1              | ″ |
| 3241        | 26             | ″ |
| 3242        | 35             | ″ |
| 3243        | 375            | ″ |
| 3244        | 6000           | ″ |
| 3245        | 1              | ″ |
| 3246        | 9              | ″ |
| 3247        | 7              | ″ |
| 3248        | 2              | ″ |

## Holdings (R/W) — observed but not yet mapped / named

(*Excludes documented items like 3001–3015 serial and 3049 AC charge enable that we already handle.*)

| Register | Observed Value |
|----------|----------------|
| 3017 | 500 |
| 3019 | 400 |
| 3020 | -30207 |
| 3022 | 5500 |
| 3024 | 600 |
| 3030 | 5800 |
| 3036 | 15 |
| 3037 | 15 |
| 3038 | -32768 |
| 3039 | 5947 |
| 3041 | 59 |
| 3043 | 59 |
| 3047 | 50 |
| 3048 | 90 |
| 3079 | 1 |
| 3087 | 20817 |
| 3088 | 19249 |
| 3089 | 12336 |
| 3090 | 12336 |
| 3091 | 12850 |
| 3092 | 12338 |
| 3093 | 12336 |
| 3094 | 14667 |
| 3096 | 23109 |
| 3097 | 16961 |
| 3099 | 22083 |
| 3100 | 16705 |
| 3101 | 2 |
| 3102 | 2616 |
| 3103 | 2 |
| 3104 | 2 |
| 3105 | 732 |
| 3108 | 16 |
| 3109 | 1024 |
| 3111 | 48 |
| 3113 | 257 |
| 3114 | 10 |
| 3125 | 22616 |
| 3126 | 22616 |
| 3127 | 22616 |
| 3128 | 22616 |
| 3136 | 8224 |
| 3137 | 8224 |


(*Excludes documented items like 3001–3015 serial and 3049 AC charge enable that we already handle.*)

| Register | Observed Value |
|----------|----------------|
| 3017 | 500 |
| 3019 | 400 |
| 3020 | -30207 |
| 3022 | 5500 |
| 3024 | 600 |
| 3030 | 5800 |
| 3036 | 15 |
| 3037 | 15 |
| 3038 | -32768 |
| 3039 | 5947 |
| 3041 | 59 |
| 3043 | 59 |
| 3047 | 50 |
| 3048 | 90 |
| 3079 | 1 |
| 3087 | 20817 |
| 3088 | 19249 |
| 3089 | 12336 |
| 3090 | 12336 |
| 3091 | 12850 |
| 3092 | 12338 |
| 3093 | 12336 |
| 3094 | 14667 |
| 3096 | 23109 |
| 3097 | 16961 |
| 3099 | 22083 |
| 3100 | 16705 |
| 3101 | 2 |
| 3102 | 2616 |
| 3103 | 2 |
| 3104 | 2 |
| 3105 | 732 |
| 3108 | 16 |
| 3109 | 1024 |
| 3111 | 48 |
| 3113 | 257 |
| 3114 | 10 |
| 3125 | 22616 |
| 3126 | 22616 |
| 3127 | 22616 |
| 3128 | 22616 |
| 3136 | 8224 |
| 3137 | 8224 |

> These ≥3000 holding registers look TL‑XH‑specific (device/capability descriptors, thresholds, or BDC/BMS config). We’ll try to correlate with battery state, grid‑tie mode, and charge/backup settings during tests.

