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

## (3000–3124) — TL‑XH Input Detailed Map

| Reg(s) | Spec Name / Description | Scale / Unit | Attribute | Register Set |
|---|---|---|---|---|
| 3000 | Inverter Status (hi=mode, lo=status) | – | `ATTR_STATUS_CODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3001–3002 | PV total power (Ppv H/L) | 0.1 W | `ATTR_INPUT_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3003 | PV1 voltage (Vpv1) | 0.1 V | `ATTR_INPUT_1_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3004 | PV1 current (Ipv1) | 0.1 A | `ATTR_INPUT_1_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3005–3006 | PV1 power (Ppv1 H/L) | 0.1 W | `ATTR_INPUT_1_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3007 | PV2 voltage (Vpv2) | 0.1 V | `ATTR_INPUT_2_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3008 | PV2 current (Ipv2) | 0.1 A | `ATTR_INPUT_2_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3009–3010 | PV2 power (Ppv2 H/L) | 0.1 W | `ATTR_INPUT_2_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3011 | PV3 voltage | 0.1 V | `ATTR_INPUT_3_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3012 | PV3 current | 0.1 A | `ATTR_INPUT_3_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3013–3014 | PV3 power | 0.1 W | `ATTR_INPUT_3_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3015 | PV4 voltage | 0.1 V | `ATTR_INPUT_4_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3016 | PV4 current | 0.1 A | `ATTR_INPUT_4_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3017–3018 | PV4 power | 0.1 W | `ATTR_INPUT_4_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3019–3020 | System output power (Psys H/L) | 0.1 W | `ATTR_OUTPUT_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3021–3022 | Reactive power (Qac H/L) | 0.1 Var | `ATTR_OUTPUT_REACTIVE_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3023–3024 | AC output power (Pac H/L) | 0.1 W | `ATTR_OUTPUT_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3025 | Grid frequency (Fac) | 0.01 Hz | `ATTR_GRID_FREQUENCY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3026 | AC1 voltage (Vac1) | 0.1 V | `ATTR_OUTPUT_1_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3027 | AC1 current (Iac1) | 0.1 A | `ATTR_OUTPUT_1_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3028–3029 | AC1 apparent power (Pac1 H/L) | 0.1 VA | `ATTR_OUTPUT_1_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3030 | AC2 voltage (Vac2) | 0.1 V | `ATTR_OUTPUT_2_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3031 | AC2 current (Iac2) | 0.1 A | `ATTR_OUTPUT_2_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3032–3033 | AC2 power (Pac2 H/L) | 0.1 VA | `ATTR_OUTPUT_2_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3034 | AC3 voltage (Vac3) | 0.1 V | `ATTR_OUTPUT_3_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3035 | AC3 current (Iac3) | 0.1 A | `ATTR_OUTPUT_3_AMPERAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3036–3037 | AC3 power (Pac3 H/L) | 0.1 VA | `ATTR_OUTPUT_3_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3038 | Vac_RS (line voltage) | 0.1 V | `ATTR_VAC_RS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3039 | Vac_ST (line voltage) | 0.1 V | `ATTR_VAC_ST` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3040 | Vac_TR (line voltage) | 0.1 V | `ATTR_VAC_TR` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3041–3042 | Total forward power (Ptouser total H/L) | 0.1 W | `ATTR_POWER_TO_USER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3043–3044 | Total reverse power (Ptogrid total H/L) | 0.1 W | `ATTR_POWER_TO_GRID` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3045–3046 | Total load power (Ptoload total H/L) | 0.1 W | `ATTR_POWER_USER_LOAD` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3047–3048 | Work time total (Time total H/L) | 0.5 s | `ATTR_OPERATION_HOURS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3049–3050 | Today AC energy (Eac today H/L) | 0.1 kWh | `ATTR_OUTPUT_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3051–3052 | Total AC energy (Eac total H/L) | 0.1 kWh | `ATTR_OUTPUT_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3053–3054 | PV energy total (Epv total H/L) | 0.1 kWh | `ATTR_INPUT_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3055–3056 | PV1 energy today (H/L) | 0.1 kWh | `ATTR_INPUT_1_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3057–3058 | PV1 energy total (H/L) | 0.1 kWh | `ATTR_INPUT_1_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3059–3060 | PV2 energy today (H/L) | 0.1 kWh | `ATTR_INPUT_2_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3061–3062 | PV2 energy total (H/L) | 0.1 kWh | `ATTR_INPUT_2_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3063–3064 | PV3 energy today (H/L) | 0.1 kWh | `ATTR_INPUT_3_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3065–3066 | PV3 energy total (H/L) | 0.1 kWh | `ATTR_INPUT_3_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3067–3068 | Today energy to user (H/L) | 0.1 kWh | `ATTR_ENERGY_TO_USER_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3069–3070 | Total energy to user (H/L) | 0.1 kWh | `ATTR_ENERGY_TO_USER_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3071–3072 | Today energy to grid (H/L) | 0.1 kWh | `ATTR_ENERGY_TO_GRID_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3073–3074 | Total energy to grid (H/L) | 0.1 kWh | `ATTR_ENERGY_TO_GRID_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3075–3076 | Today energy of user load (H/L) | 0.1 kWh | `ATTR_ENERGY_LOAD_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3077–3078 | Total energy of user load (H/L) | 0.1 kWh | `ATTR_ENERGY_LOAD_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3079–3082 | PV4 energy today/total (H/L pairs) | 0.1 kWh | `ATTR_INPUT_4_ENERGY_TODAY/TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3083–3084 | PV energy today (H/L) | 0.1 kWh | `ATTR_INPUT_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3085 | Reserved | – | – | – |
| 3086 | DeratingMode | enum | `ATTR_DERATING_MODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3087 | PV ISO value (ISO) | kΩ | `ATTR_PV_ISO_VALUE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3088 | DCI_R | 0.1 mA | `ATTR_DCI_R` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3089 | DCI_S | 0.1 mA | `ATTR_DCI_S` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3090 | DCI_T | 0.1 mA | `ATTR_DCI_T` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3091 | GFCI current | 1 mA | `ATTR_GFCI_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3092 | Total bus voltage | 0.1 V | `ATTR_TOTAL_BUS_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3093 | Inverter temperature (Temp1) | 0.1 °C | `ATTR_TEMPERATURE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3094 | IPM temperature (Temp2) | 0.1 °C | `ATTR_IPM_TEMPERATURE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3095 | Boost temperature (Temp3) | 0.1 °C | `ATTR_BOOST_TEMPERATURE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3096 | Temp4 (Reserved) | 0.1 °C | – | – |
| 3097 | Communication board temperature (Temp5) | 0.1 °C | `ATTR_COMM_BOARD_TEMPERATURE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3098 | P Bus voltage | 0.1 V | `ATTR_P_BUS_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3099 | N Bus voltage | 0.1 V | `ATTR_N_BUS_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3100 | Inverter output PF now (IPF) | 0–20000 | `ATTR_OUTPUT_PF` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3101 | Real output power percent | 1 % | `ATTR_OUTPUT_PERCENTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3102–3103 | Output max power limit (OPFullwatt H/L) | 0.1 W | `ATTR_OUTPUT_MAX_POWER_LIMIT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3104 | StandbyFlag (bitfield) | – | `ATTR_STANDBY_FLAGS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3105 | Fault maincode | – | `ATTR_FAULT_CODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3106 | Warn maincode | – | `ATTR_WARNING_CODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3107 | Fault subcode (bitfield) | – | `ATTR_FAULT_SUBCODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3108 | Warn subcode (bitfield)  | – | `ATTR_WARNING_SUBCODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3110 | Warning code             | – | `ATTR_WARNING_CODE`    | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3111 | PresentFFTValue [CHANNEL_A] | – | `ATTR_PRESENT_FFT_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3112 | AFCI Status | enum | `ATTR_AFCI_STATUS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3113 | AFCI Strength [CHANNEL_A] | – | `ATTR_AFCI_STRENGTH_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3114 | AFCI SelfCheck [CHANNEL_A] | – | `ATTR_AFCI_SELF_CHECK_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3115 | Inverter start delay time | 1 s | `ATTR_INV_START_DELAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3118 | BDC connect state | enum | `ATTR_BDC_ONOFF_STATE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3119 | DryContactState (0=off,1=on) | – | `ATTR_DRY_CONTACT_STATE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3121–3122 | Self‑use power (Pself H/L) | 0.1 W | `ATTR_SELF_USE_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3123–3124 | System energy today (Esys_today H/L) | 0.1 kWh | `ATTR_SYSTEM_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |

---

## (3125–3249) — TL‑XH Battery / System Block

| Reg(s) | Spec Name / Description | Scale / Unit | Attribute | Register Set |
|---|---|---|---|---|
| 3125–3126 | Today discharge energy (Edischr_today H/L) | 0.1 kWh | `ATTR_DISCHARGE_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3127–3128 | Total discharge energy (Edischr_total H/L) | 0.1 kWh | `ATTR_DISCHARGE_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3129–3130 | Charge energy today (Echr_today H/L) | 0.1 kWh | `ATTR_CHARGE_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3131–3132 | Charge energy total (Echr_total H/L) | 0.1 kWh | `ATTR_CHARGE_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3133–3134 | Today energy of AC charge (Eacchr_today H/L) | 0.1 kWh | `ATTR_AC_CHARGE_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3135–3136 | Total energy of AC charge (Eacchr_total H/L) | 0.1 kWh | `ATTR_AC_CHARGE_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3137–3138 | Total energy of system output (Esys_total H/L) | 0.1 kWh | `ATTR_SYSTEM_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3139–3140 | Today energy of Self output (Eself_today H/L) | 0.1 kWh | `ATTR_SELF_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3141–3142 | Total energy of Self output (Eself_total H/L) | 0.1 kWh | `ATTR_SELF_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3143 | Reserved | – | – | – |
| 3144 | Priority Word Mode (0:LoadFirst,1:BatteryFirst,2:GridFirst) | enum | `ATTR_PRIORITY_MODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3145 | EPS frequency (UPS Fac) | 0.01 Hz | `ATTR_EPS_FREQUENCY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3146 | EPS Vac1 (phase R) | 0.1 V | `ATTR_EPS_VOLTAGE_R` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3147 | EPS Iac1 (phase R) | 0.1 A | `ATTR_EPS_CURRENT_R` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3148–3149 | EPS Pac1 (phase R H/L) | 0.1 VA | `ATTR_EPS_POWER_R` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3150 | EPS Vac2 (phase S) | 0.1 V | `ATTR_EPS_VOLTAGE_S` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3151 | EPS Iac2 (phase S) | 0.1 A | `ATTR_EPS_CURRENT_S` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3152–3153 | EPS Pac2 (phase S H/L) | 0.1 VA | `ATTR_EPS_POWER_S` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3154 | EPS Vac3 (phase T) | 0.1 V | `ATTR_EPS_VOLTAGE_T` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3155 | EPS Iac3 (phase T) | 0.1 A | `ATTR_EPS_CURRENT_T` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3156–3157 | EPS Pac3 (phase T H/L) | 0.1 VA | `ATTR_EPS_POWER_T` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3158–3159 | EPS total output power (H/L) | 0.1 VA | `ATTR_EPS_POWER_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3160 | Load percent of UPS output | 0.10 % | `ATTR_EPS_LOAD_PERCENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3161 | Power factor | 0.1 | `ATTR_POWER_FACTOR` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3162 | DC voltage | 1 mV | `ATTR_DC_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3163 | Reserved | – | – | – |
| 3164 | NewBdcFlag (parse BDC separately) | – | `ATTR_BDC_NEW_FLAG` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3165 | BDCDeratingMode (see spec list) | enum | `ATTR_BDC_DERATING_MODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3166 | SysState_Mode (mode/status) | enum | `ATTR_SYSTEM_STATE_MODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3167 | Storage fault code | – | `ATTR_STORAGE_FAULT_CODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3168 | Storage warning code | – | `ATTR_STORAGE_WARNING_CODE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3169 | Battery voltage (Vbat) | 0.01 V | `ATTR_BATTERY_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3170 | Battery current (Ibat) | 0.1 A | `ATTR_BATTERY_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3171 | SOC | 1 % | `ATTR_SOC_PERCENTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3172 | Vbus1 total BUS | 0.1 V | `ATTR_VBUS1_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3173 | Vbus2 on BUS | 0.1 V | `ATTR_VBUS2_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3174 | BUCK‑BOOST current (Ibb) | 0.1 A | `ATTR_BUCK_BOOST_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3175 | LLC current (Illc) | 0.1 A | `ATTR_LLC_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3176 | Temperature A | 0.1 °C | `ATTR_BATTERY_TEMPERATURE_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3177 | Temperature B | 0.1 °C | `ATTR_BATTERY_TEMPERATURE_B` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3178–3179 | Discharge power (H/L) | 0.1 W | `ATTR_DISCHARGE_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3180–3181 | Charge power (H/L) | 0.1 W | `ATTR_CHARGE_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3182–3183 | Discharge total energy of storage (H/L) | 0.1 kWh | `ATTR_DISCHARGE_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3184–3185 | Charge total energy of storage (H/L) | 0.1 kWh | `ATTR_CHARGE_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3186 | Reserved | – | – | – |
| 3187 | BDC1_Flag (bitfield) | – | `ATTR_BDC_FLAGS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3188 | Lower BUS voltage (Vbus2) | 0.1 V | `ATTR_VBUS2_LOWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3189 | BmsMaxVoltCellNo | – | `ATTR_BMS_MAX_VOLT_CELL_NO` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3190 | BmsMinVoltCellNo | – | `ATTR_BMS_MIN_VOLT_CELL_NO` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3191 | BmsBatteryAvgTemp | – | `ATTR_BMS_AVG_TEMP_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3192 | BmsMaxCellTemp | 0.1 °C | `ATTR_BMS_MAX_CELL_TEMP_A` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3193 | BmsBatteryAvgTemp | – | `ATTR_BMS_AVG_TEMP_B` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3194 | BmsMaxCellTemp | – | `ATTR_BMS_MAX_CELL_TEMP_B` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3195 | BmsBatteryAvgTemp | – | `ATTR_BMS_AVG_TEMP_C` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3196 | BmsMaxSOC | 1 % | `ATTR_BMS_MAX_SOC` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3197 | BmsMinSOC | 1 % | `ATTR_BMS_MIN_SOC` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3198 | ParallelBatteryNum | – | `ATTR_PARALLEL_BATTERY_NUM` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3199 | BmsDerateReason | – | `ATTR_BMS_DERATE_REASON` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3200 | BmsGaugeFCC (Ah) | Ah | `ATTR_BMS_GAUGE_FCC_AH` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3201 | BmsGaugeRM (Ah) | Ah | `ATTR_BMS_GAUGE_RM_AH` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3202 | BMS Protect1 | – | `ATTR_BMS_PROTECT1` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3203 | BMS Warn1 | – | `ATTR_BMS_WARN1` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3204 | BMS Fault1 | – | `ATTR_BMS_FAULT1` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3205 | BMS Fault2 | – | `ATTR_BMS_FAULT2` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3206–3209 | Reserved | – | – | – |
| 3210 | Battery ISO detection status | – | `ATTR_BAT_ISO_STATUS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3211 | Battery work request flags | bitfield | `ATTR_BATT_REQUEST_FLAGS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3212 | BMS status | enum | `ATTR_BMS_STATUS` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3213 | BMS Protect2 | – | `ATTR_BMS_PROTECT2` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3214 | BMS Warn2 | – | `ATTR_BMS_WARN2` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3215 | BMS SOC | 1 % | `ATTR_BMS_SOC` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3216 | BMS BatteryVolt | 0.01 V | `ATTR_BMS_BATTERY_VOLTAGE` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3217 | BMS BatteryCurr | 0.01 A | `ATTR_BMS_BATTERY_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3218 | Battery cell max temperature | 0.1 °C | `ATTR_BMS_CELL_MAX_TEMP` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3219 | Maximum charging current | 0.01 A | `ATTR_BMS_MAX_CHARGE_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3220 | Maximum discharge current | 0.01 A | `ATTR_BMS_MAX_DISCHARGE_CURRENT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3221 | BMS Cycle count | 1 | `ATTR_BMS_CYCLE_COUNT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3222 | BMS SOH | 1 | `ATTR_BMS_SOH` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3223 | Battery charging voltage limit | 0.01 V | `ATTR_BMS_CHARGE_VOLT_LIMIT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3224 | Battery discharge voltage limit | 0.01 V | `ATTR_BMS_DISCHARGE_VOLT_LIMIT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3225 | BMS Warn3 | – | `ATTR_BMS_WARN3` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3226 | BMS Protect3 | – | `ATTR_BMS_PROTECT3` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3227–3229 | Reserved | – | – | – |
| 3230 | BMS Battery SingleVoltMax | 0.001 V | `ATTR_BMS_CELL_VOLT_MAX` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3231 | BMS Battery SingleVoltMin | 0.001 V | `ATTR_BMS_CELL_VOLT_MIN` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3232 | Battery LoadVolt | 0.01 V | `ATTR_BAT_LOAD_VOLT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3233 | – | – | – | – |
| 3234–3249 | Debug data1..16 | – | `ATTR_DEBUG_DATA_[1..16]` | STORAGE_INPUT_REGISTERS_120_TL_XH |

### Spec‑documented TL‑XH debug/diagnostic inputs (examples)

> Per the v1.24 spec, many addresses in this area are **documented** as diagnostic or reserved. Notable examples you observed:

| Register | Name (per v1.24)                                 | Note |
|----------|--------------------------------------------------|------|
| 3069–3070| 32‑bit field (pair)                              | Your scan shows 3070 populated; treat 3069–3070 as one 32‑bit value.
| 3097     | Communication board temperature                  | Observed non‑zero in scan.
| 3111     | PresentFFTValue \[CHANNEL_A]                     | Diagnostic FFT bin.
| 3115     | Inverter start delay time                        | Matches observed value.

**32‑bit convention:** For these TL‑XH input blocks, 32‑bit values are exposed as **two consecutive 16‑bit words**. The integration already combines pairs as `(hi<<16) + lo` (big‑endian words), consistent with your scan and current code.


## (3250–3280) — TL‑XH Extension Inputs

| Reg(s) | Spec Name / Description | Scale / Unit | Attribute | Register Set |
|---|---|---|---|---|
| 3250–3251 | PV inverter 1 output power (Pex1 H/L) | 0.1 W | `ATTR_EXT_PV1_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3252–3253 | PV inverter 2 output power (Pex2 H/L) | 0.1 W | `ATTR_EXT_PV2_POWER` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3254–3255 | PV inverter 1 energy today (Eex1Today H/L) | 0.1 kWh | `ATTR_EXT_PV1_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3256–3257 | PV inverter 2 energy today (Eex2Today H/L) | 0.1 kWh | `ATTR_EXT_PV2_ENERGY_TODAY` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3258–3259 | PV inverter 1 energy total (Eex1Total H/L) | 0.1 kWh | `ATTR_EXT_PV1_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3260–3261 | PV inverter 2 energy total (Eex2Total H/L) | 0.1 kWh | `ATTR_EXT_PV2_ENERGY_TOTAL` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3262 | Battery pack number (uwBatNo) | – | `ATTR_BAT_PACK_COUNT` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3263–3270 | Battery pack serials SN[0..15] (pairs) | – | `ATTR_BAT_PACK_SERIAL_[1..8]` | STORAGE_INPUT_REGISTERS_120_TL_XH |
| 3271–3279 | Reserved | – | – | – |
| 3280 | Clear day data flag (bClrTodayDataFlag) | – | `ATTR_CLEAR_DAY_DATA_FLAG` | STORAGE_INPUT_REGISTERS_120_TL_XH |

---

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
