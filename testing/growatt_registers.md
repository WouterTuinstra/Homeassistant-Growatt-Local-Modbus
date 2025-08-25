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

