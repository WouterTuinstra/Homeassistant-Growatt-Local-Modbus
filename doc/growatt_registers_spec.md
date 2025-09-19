# Growatt Modbus Register Map (Protocol v1.24)

This file is generated from `growatt_registers_spec.json` (parsed from the official Modbus RTU protocol) and cross-references the Home Assistant `growatt_local` integration.

**Legend**: Access = spec write flag (`R`, `W`, `R/W`). “Range/Unit” merges the spec range column with the unit, when available. “Attributes” lists the integration attribute(s) mapped to the register; “Sensors” lists Home Assistant sensor entities exposing the attribute. Rows without attributes are not currently surfaced by the integration (typically configuration or reserved registers).

*Descriptions and notes are copied verbatim from the PDF specification. Some spacing may appear collapsed due to automated extraction; consult the original document when exact phrasing is required.*

## Coverage Summary
| Section | Spec Registers | Covered | Missing |
| --- | --- | --- | --- |
| Common Holding Registers (0–124) | 100 | 8 | 92 |
| TL-X/TL-XH Holding Registers (3000–3124) | 78 | 0 | 78 |
| TL-XH US Holding Registers (3125–3249) | 5 | 0 | 5 |
| TL-XH BDC Metadata Mirrors (5000–5039) | 1 | 0 | 1 |
| TL3/MAX/MID/MAC Holding Registers (125–249) | 80 | 0 | 80 |
| Storage Holding Registers (1000–1124) | 35 | 0 | 35 |
| Storage Holding Registers (1125–1249) | 15 | 0 | 15 |
| Common Input Registers (0–124) | 66 | 66 | 0 |
| TL-X/TL-XH Input Registers (3000–3124) | 55 | 55 | 0 |
| TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249) | 52 | 52 | 0 |
| TL-X/TL-XH Extended Input Registers (3250–3374) | 0 | 0 | 0 |
| Storage Input Registers (1000–1124) | 0 | 0 | 0 |
| Storage Input Registers (1125–1249) | 0 | 0 | 0 |
| Storage Input Registers (2000–2124) | 0 | 0 | 0 |
| Storage TL-XH Input Registers (3041–3231) | 81 | 62 | 19 |
| Offgrid SPF Input Registers | 175 | 25 | 150 |

## Common Holding Registers (0–124)
Applies to TL-X/TL-XH, TL3/MAX/MID/MAC, and MIX/SPA/SPH storage families.

**Applies to:** TL-X/TL-XH/TL-XH US, TL3-X/MAX/MID/MAC, Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Inverter Enabled | Bitfield controlling remote enable of the inverter (bit 0) and the battery DC converter or BDC ready mode (bit 1). Write the combined value 0-3; 1 turns on the inverter, 2 turns on only the BDC, 3 turns on both. | W | — | 1 | Home Assistant preserves other control bits when toggling this value. | tlx:inverter_enabled, tl3:inverter_enabled | — |
| 1 | Safety function enable flags | Bit mask that enables regional grid-protection functions. Set a bit to 1 to enable the corresponding feature (SPI, LVFRT, DRMS, Volt-Var, ROCOF, recovery, split-phase). | W | — | — | Bits 0-3 cover CEI 0-21 compliance; bits 4-6 cover AS/NZS/SAA requirements; bits 11-15 are reserved. | — | — |
| 2 | Persist power-factor commands | Choose whether the power-factor and derating commands in registers 3, 4, 5, and 99 are stored to NVRAM (1) or revert to defaults after the next restart (0). | W | — | 0 | — | — | — |
| 3 | Active power limit setpoint | Maximum active power output as a percentage of rated power. Values 0-100 cap the output; 255 removes the limit. | W | — % | 255 | — | — | — |
| 4 | Reactive power limit setpoint | Maximum reactive power magnitude as a percent of rated capacity. Negative values request capacitive (leading) support, positive values inductive (lagging). 255 removes the limit. | W | — % | 255 | — | — | — |
| 5 | Power factor target | Requested power factor multiplied by 10,000 (e.g. 9900 equals 0.99). Values below 10,000 lead (capacitive); values above 10,000 lag (inductive). | W | — | 0 | — | — | — |
| 6 | Rated apparent power | Apparent power capability encoded as an unsigned 32-bit value with 0.1 VA resolution (register 6 is the high word, register 7 the low word). | R | — VA | — | — | — | — |
| 8 | Nominal PV voltage | Target PV input voltage for maximum power point tracking, stored in 0.1 V increments. | R | — V | — | — | — | — |
| 9 | Firmware | Six registers containing ASCII characters that describe the running firmware. Registers 9-11 hold the DSP identifier; registers 12-14 hold the control-board identifier. Home Assistant reads the combined 12-character string for the reported firmware version. | R | — ASCII | — | — | tlx:firmware, tl3:firmware, storage:firmware | — |
| 15 | LCD language selection | Language index used by the local LCD interface: 0=Italian, 1=English, 2=German, 3=Spanish, 4=French, 5=Chinese, 6=Polish, 7=Portuguese, 8=Hungarian. | W | — | — | — | — | — |
| 16 | Country profile configured | Indicates whether a regional grid profile has been selected (1) or still needs to be chosen (0). | W | — | — | — | — | — |
| 17 | PV start voltage threshold | Minimum DC input voltage required before the inverter starts, stored in 0.1 V increments. | W | — V | — | — | — | — |
| 18 | Start-up delay | Delay between meeting the PV start voltage and enabling the inverter output, measured in seconds. | W | — s | — | — | — | — |
| 19 | Restart delay | Time to wait after a fault clears before restarting the inverter, in seconds. | W | — s | — | — | — | — |
| 20 | Active power ramp rate (startup) | Slope for increasing active power after startup in 0.1% increments per second (1-1000). | W | — %/s | — | — | — | — |
| 21 | Active power ramp rate (restart) | Slope for returning to full power after curtailment or a cleared fault, expressed in 0.1% per second. | W | — %/s | — | — | — | — |
| 22 | Modbus RTU baud rate | Selects the RS-485 serial line baud rate: 0=9600 bps, 1=38400 bps. | W | — | 0 | — | — | — |
| 23 | Serial Number | ASCII-encoded 10-character serial number spanning registers 23-27. | R | — ASCII | — | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | tlx:serial number, tl3:serial number | — |
| 28 | Inverter Model | 32-bit hardware option mask encoded as eight nibbles (A, B, D, T, P, U, M, S). Register 28 holds the high word and register 29 the low word. | R | — | — | Home Assistant renders this value as the string A# B# D# T# P# U# M# S# via the integration's model() helper. | tlx:Inverter model, tl3:Inverter model, storage:Inverter model | — |
| 30 | Modbus slave address | RS-485/Modbus RTU slave ID. Set a value between 1 and 254; 0 is reserved for broadcast frames. | W | — | — | — | — | — |
| 31 | Firmware update trigger | Write 1 to arm the serial firmware update procedure. The inverter clears the flag after the bootloader handshake starts. | W | — | — | — | — | — |
| 32 | Reset user configuration | Writing 1 clears user-configurable settings such as communication parameters and regional profiles. | W | — | — | Use with caution; the inverter immediately reboots and loses provisioning data. | — | — |
| 33 | Factory reset | Writing 1 restores full factory defaults and restarts the inverter. | W | — | — | Equivalent to the front-panel factory reset. Requires re-commissioning afterwards. | — | — |
| 34 | Manufacturer information string | Sixteen ASCII characters written at production time (batch, plant, or custom identifiers). | R | — ASCII | — | The original table lists these words as Manufacturer Info 8–1 (high/middle/low); combine them to read the full string. | — | — |
| 42 | G 100 failsafe enable | Enable (1) or disable (0) the UK G 98/G 100 failsafe watchdog. | W | — | — | Leave off unless the interconnection agreement requires the G 100 failsafe mode. | — | — |
| 43 | Device Type Code | Encodes the inverter family and tracker count. See data type for supported values. | R | — | — | — | tlx:device type code, tl3:device type code, storage:device type code | — |
| 44 | Number Of Trackers And Phases | High byte holds the number of PV trackers; low byte holds the number of output phases. | R | — | — | — | tlx:number of trackers and phases, tl3:number of trackers and phases, storage:number of trackers and phases | — |
| 45 | System clock year | Calendar year stored by the internal real-time clock. | W | — | — | Write the full year (for example 2024). | — | — |
| 46 | System clock month | Calendar month for the internal clock. | W | — | — | — | — | — |
| 47 | System clock day | Day of month for the internal clock. | W | — | — | — | — | — |
| 48 | System clock hour | Hour of day in 24-hour format. | W | — | — | — | — | — |
| 49 | System clock minute | Minute component of the internal clock. | W | — | — | — | — | — |
| 50 | System clock second | Second component of the internal clock. | W | — | — | — | — | — |
| 51 | System clock weekday | Day-of-week index for the internal clock (0=Sunday, 6=Saturday). | W | — | — | — | — | — |
| 52 | Stage 1 undervoltage limit | Grid voltage threshold for stage 1 undervoltage protection, stored in 0.1 V increments. Delay configured by register 68. | W | — V | — | — | — | — |
| 53 | Stage 1 overvoltage limit | Grid voltage threshold for stage 1 overvoltage protection (0.1 V increments). Delay configured by register 69. | W | — V | — | — | — | — |
| 54 | Stage 1 underfrequency limit | Grid frequency threshold for stage 1 underfrequency protection (0.01 Hz increments). Delay configured by register 72. | W | — Hz | — | — | — | — |
| 55 | Stage 1 overfrequency limit | Grid frequency threshold for stage 1 overfrequency protection (0.01 Hz increments). Delay configured by register 73. | W | — Hz | — | — | — | — |
| 56 | Stage 2 undervoltage limit | Grid voltage threshold for stage 2 undervoltage protection, stored in 0.1 V increments. Delay configured by register 70. | W | — V | — | — | — | — |
| 57 | Stage 2 overvoltage limit | Grid voltage threshold for stage 2 overvoltage protection (0.1 V increments). Delay configured by register 71. | W | — V | — | — | — | — |
| 58 | Stage 2 underfrequency limit | Grid frequency threshold for stage 2 underfrequency protection (0.01 Hz increments). Delay configured by register 74. | W | — Hz | — | — | — | — |
| 59 | Stage 2 overfrequency limit | Grid frequency threshold for stage 2 overfrequency protection (0.01 Hz increments). Delay configured by register 75. | W | — Hz | — | — | — | — |
| 60 | Stage 3 undervoltage limit | Grid voltage threshold for stage 3 undervoltage protection, stored in 0.1 V increments. Delay configured by register 76. | W | — V | — | — | — | — |
| 61 | Stage 3 overvoltage limit | Grid voltage threshold for stage 3 overvoltage protection (0.1 V increments). Delay configured by register 77. | W | — V | — | — | — | — |
| 62 | Stage 3 underfrequency limit | Grid frequency threshold for stage 3 underfrequency protection (0.01 Hz increments). Delay configured by register 78. | W | — Hz | — | — | — | — |
| 63 | Stage 3 overfrequency limit | Grid frequency threshold for stage 3 overfrequency protection (0.01 Hz increments). Delay configured by register 79. | W | — Hz | — | — | — | — |
| 64 | Reconnect undervoltage limit | Minimum grid voltage (0.1 V increments) required before reconnecting after a trip. | W | — V | — | — | — | — |
| 65 | Reconnect overvoltage limit | Maximum grid voltage (0.1 V increments) allowed when reconnecting after a trip. | W | — V | — | — | — | — |
| 66 | Reconnect underfrequency limit | Minimum grid frequency (0.01 Hz increments) required for reconnection. | W | — Hz | — | — | — | — |
| 67 | Reconnect overfrequency limit | Maximum grid frequency (0.01 Hz increments) allowed when reconnecting. | W | — Hz | — | — | — | — |
| 68 | Stage 1 undervoltage trip delay | Number of cycles grid voltage must stay below the stage 1 undervoltage limit (register 52) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 69 | Stage 1 overvoltage trip delay | Cycles grid voltage must stay above the stage 1 overvoltage limit (register 53) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 70 | Stage 2 undervoltage trip delay | Cycles grid voltage must stay below the stage 2 undervoltage limit (register 56) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 71 | Stage 2 overvoltage trip delay | Cycles grid voltage must stay above the stage 2 overvoltage limit (register 57) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 72 | Stage 1 underfrequency trip delay | Cycles grid frequency must stay below the stage 1 underfrequency limit (register 54) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 73 | Modbus Version | Cycles grid frequency must stay above the stage 1 overfrequency limit (register 55) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | tl3:modbus version | — |
| 74 | Stage 2 underfrequency trip delay | Cycles grid frequency must stay below the stage 2 underfrequency limit (register 58) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 75 | Stage 2 overfrequency trip delay | Cycles grid frequency must stay above the stage 2 overfrequency limit (register 59) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 76 | Stage 3 undervoltage trip delay | Cycles grid voltage must stay below the stage 3 undervoltage limit (register 60) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 77 | Stage 3 overvoltage trip delay | Cycles grid voltage must stay above the stage 3 overvoltage limit (register 61) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 78 | Stage 3 underfrequency trip delay | Cycles grid frequency must stay below the stage 3 underfrequency limit (register 62) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 79 | Stage 3 overfrequency trip delay | Cycles grid frequency must stay above the stage 3 overfrequency limit (register 63) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 80 | Ten-minute overvoltage limit | Maximum RMS grid voltage averaged over 10 minutes (0.1 V increments) before the inverter trips. | W | — V | — | — | — | — |
| 81 | PV input high-voltage fault | PV array voltage threshold that triggers a DC over-voltage fault (0.1 V increments). | W | — V | — | — | — | — |
| 82 | Controller firmware build string | Twelve ASCII characters summarising model and controller build revisions (model letters, DSP 1, DSP 2/M 0, CPLD/AFCI, M 3). | R | — ASCII | — | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP 1 build, 6-7 DSP 2/M 0 build, 8-9 CPLD/AFCI build, 10-11 M 3 build. | — | — |
| 88 | Modbus Version | Modbus register map revision encoded as an integer (e.g. 207 equals version 2.07). | R | — | — | — | tlx:modbus version, storage:modbus version | — |
| 89 | Power-factor control mode | Selects the reactive power or power-factor control curve. | W | — | — | 0=Unity PF, 1=Fixed PF setpoint, 2=Default PF line, 3=User-defined PF line, 4=Under-excited reactive power, 5=Over-excited reactive power, 6=Q(V) curve, 7=Direct control, 8=Static capacitive QV, 9=Static inductive QV. | — | — |
| 90 | GPRS modem IP/status flags | Lower nibble reports the IP configuration handshake; upper nibble reports modem status. | W | — | — | Bit 0-3: 0=idle, 1=IP read requested, 2=set IP succeeded; Bit 4-7: 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. | — | — |
| 91 | Frequency derating start | Grid frequency at which active power derating begins (0.01 Hz increments). | W | — Hz | — | — | — | — |
| 92 | Frequency derating slope | Slope of the frequency-based active power derating curve. Divide by 10 to obtain percent per hertz. | W | — %/Hz | — | — | — | — |
| 93 | CEI 0-21 Q(V) point V 1 S | Upper voltage limit V 1 S for the CEI 0-21 Q(V) curve (0.1 V increments). | W | — V | — | — | — | — |
| 94 | CEI 0-21 Q(V) point V 2 S | Upper voltage limit V 2 S for the CEI 0-21 Q(V) curve (0.1 V increments). | W | — V | — | — | — | — |
| 95 | CEI 0-21 Q(V) point V 1 L | Lower voltage limit V 1 L for the CEI 0-21 Q(V) curve (0.1 V increments). | W | — V | — | — | — | — |
| 96 | CEI 0-21 Q(V) point V 2 L | Lower voltage limit V 2 L for the CEI 0-21 Q(V) curve (0.1 V increments). | W | — V | — | — | — | — |
| 97 | Q(V) lock-in active power | Active power percentage (0-100%) that enables CEI 0-21 Q(V) operation. | W | — % | — | — | — | — |
| 98 | Q(V) lock-out active power | Active power percentage (0-100%) below which CEI 0-21 Q(V) control is disabled. | W | — % | — | — | — | — |
| 99 | Power-factor curve lock-in voltage | Voltage threshold (0.1 V increments) for entering the CEI 0-21 power-factor curve. | W | — V | — | — | — | — |
| 100 | Power-factor curve lock-out voltage | Voltage threshold (0.1 V increments) for leaving the CEI 0-21 power-factor curve. | W | — V | — | — | — | — |
| 101 | Power-factor adjust value 1 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 102 | Power-factor adjust value 2 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 103 | Power-factor adjust value 3 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 104 | Power-factor adjust value 4 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 105 | Power-factor adjust value 5 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 106 | Power-factor adjust value 6 | Fixed-point gain (1/4096 increments) applied when constructing the user-defined PF curve. | W | — | — | — | — | — |
| 107 | Q(V) response delay | Delay before applying the Q(V) reactive power response, expressed in whole seconds. | W | — s | — | — | — | — |
| 108 | Over-frequency derating delay | Delay before reducing power once frequency exceeds the derating start, in 50 ms increments. | W | — s | — | — | — | — |
| 109 | Maximum reactive power magnitude | Upper bound for reactive power commands when using the Q(V) curve, stored in 0.1% increments of rated power. | W | — % | — | — | — | — |
| 110 | PF curve point 1 load | Active power percentage for this PF curve waypoint. 255 disables the point. | W | — % | — | — | — | — |
| 111 | PF curve point 1 target | Power-factor target for this PF curve waypoint (value / 10,000). Values below 1 are capacitive (leading). | W | — | — | — | — | — |
| 112 | PF curve point 2 load | Active power percentage for this PF curve waypoint. 255 disables the point. | W | — % | — | — | — | — |
| 113 | PF curve point 2 target | Power-factor target for this PF curve waypoint (value / 10,000). Values below 1 are capacitive (leading). | W | — | — | — | — | — |
| 114 | PF curve point 3 load | Active power percentage for this PF curve waypoint. 255 disables the point. | W | — % | — | — | — | — |
| 115 | PF curve point 3 target | Power-factor target for this PF curve waypoint (value / 10,000). Values below 1 are capacitive (leading). | W | — | — | — | — | — |
| 116 | PF curve point 4 load | Active power percentage for this PF curve waypoint. 255 disables the point. | W | — % | — | — | — | — |
| 117 | PF curve point 4 target | Power-factor target for this PF curve waypoint (value / 10,000). Values below 1 are capacitive (leading). | W | — | — | — | — | — |
| 118 | Marketing module string | Eight ASCII characters that form the marketing SKU (segments for M, P, U, T, D, B, S codes). | R | — ASCII | — | Matches the printed module string pattern (e.g. Sxx Bxx, Dxx Txx, Pxx Uxx, Mxxxx Power) used on data labels. | — | — |
| 122 | Export limit enable mode | Selects the export limiting method: disabled, RS-485 meter, RS-232 meter, or CT clamp. | R/W | — | — | 0=Disabled, 1=RS-485 meter, 2=RS-232 meter, 3=External CT. | — | — |
| 123 | Export limit power setpoint | Active power limit applied by the export control subsystem, stored in 0.1% of rated power (negative values allow controlled export). | R/W | — % | — | — | — | — |
| 124 | Tracker coupling mode | Defines how the PV trackers are electrically coupled: 0=Independent, 1=DC source sharing, 2=Parallel. | W | — | — | — | — | — |
| 11 | 22~1124 Bat Serial NO. Produ | / ct serial number of / | / | — | — | reserve | — | — |

## TL-X/TL-XH Holding Registers (3000–3124)
Additional holding registers for TL-X/TL-XH hybrids (MIN series).

**Applies to:** TL-X/TL-XH/TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | Export-limit fallback cap | Percentage of rated output supplied when the export-limit controller is unavailable. Values are stored in 0.1% steps. | R/W | — % | — | Use this to keep the hybrid running at a safe output level whenever the export-limiting meter stops responding. | — | — |
| 3001 | Serial Number | Thirty-character TL-XH serial string. Mirrors the 23-27 holding-register block on legacy models. | R | — ASCII | — | — | — | — |
| 3016 | Dry-contact enable | Enable (1) or disable (0) the dry-contact output. | R/W | — | — | — | — | — |
| 3017 | Dry-contact close threshold | Dry contact engages when inverter output exceeds this percentage of rated power. | R/W | — % | — | — | — | — |
| 3018 | Hybrid work mode | Select default operation, system retrofit mode, or multi-parallel control for dual-CT installs. | R/W | — | — | — | — | — |
| 3019 | Dry-contact release threshold | Dry contact opens when output power falls below this percentage of rated power. | R/W | — % | — | — | — | — |
| 3020 | Off-grid box control | Vendor-specific control word used by the external off-grid communication box. | R/W | — | — | Leave at factory value unless instructed by Growatt support. | — | — |
| 3021 | External off-grid enable | Allow an external communications module to force the inverter into off-grid mode. | R/W | — | — | — | — | — |
| 3022 | BDC stop-work bus voltage | DC bus voltage below which the battery DC converter halts charging or discharging. | R | — V | — | — | — | — |
| 3023 | Grid topology selection | Declare single-phase, three-phase, or split-phase wiring for hybrid operation. | R/W | — | — | — | — | — |
| 3024 | Float-charge current limit | Maximum battery current during float charge, stored in 0.1 A steps. | R/W | — A | — | — | — | — |
| 3025 | Battery-low warning setpoint | Voltage that raises a "battery low" warning for lead-acid profiles. | R/W | — V | — | — | — | — |
| 3026 | Battery-low warning clear | Voltage that clears the "battery low" warning after recovery. | R/W | — V | — | — | — | — |
| 3027 | Battery discharge cutoff | Voltage where discharge stops to protect the battery. | R/W | — V | — | — | — | — |
| 3028 | Battery charge stop voltage | Upper battery voltage limit for charge termination (0.01 V resolution). | R/W | — V | — | — | — | — |
| 3029 | Battery discharge start voltage | Voltage above which discharge may resume (0.01 V resolution). | R/W | — V | — | — | — | — |
| 3030 | Battery constant-charge voltage | Constant-voltage target during absorption/boost charge (0.01 V resolution). | R/W | — V | — | — | — | — |
| 3031 | Discharge low temperature limit | Minimum battery temperature for discharge. Values 0-200 map to 0-20°C; add 1000 to encode negative values. | R/W | — °C | — | — | — | — |
| 3032 | Discharge high temperature limit | Maximum battery temperature for discharge (0.1°C resolution). | R/W | — °C | — | — | — | — |
| 3033 | Charge low temperature limit | Minimum battery temperature for charge. Values ≥1000 indicate negative limits. | R/W | — °C | — | — | — | — |
| 3034 | Charge high temperature limit | Maximum battery temperature for charge (0.1°C resolution). | R/W | — °C | — | — | — | — |
| 3035 | Under-frequency discharge delay | Delay before discharge stops during under-frequency events (0.05 s steps). | R/W | — s | — | — | — | — |
| 3036 | Grid-first discharge rate | Requested discharge power when running in grid-first mode. Values are stored as whole percentages; 255 disables the limit. | R/W | — % | — | — | — | — |
| 3037 | Grid-first stop SOC | State-of-charge threshold that ends discharge while in grid-first mode. | R/W | — % | — | — | — | — |
| 3038 | Grid-first period 1 control | Packed control word for the first grid-first schedule period (minutes, hour, priority, enable flag). | R/W | — | — | Bits 0-7: start minute; 8-12: start hour; 13-14: priority (0 load, 1 battery, 2 grid); bit 15: enable. | — | — |
| 3039 | Grid-first period 1 end | Packed end-time word for grid-first period 1 (minutes/hours). | R/W | — | — | — | — | — |
| 3040 | Grid-first period 2 control | Packed control word for the second grid-first schedule period. | R/W | — | — | — | — | — |
| 3041 | Power to user | Real-time active power routed to on-site loads (mirrors input registers 3041-3042). | R | — W | — | Home Assistant exposes this as `power_to_user` for TL-XH devices. | — | — |
| 3043 | Power to grid | Instantaneous export power flowing to the grid (mirrors input registers 3043-3044). | R | — W | — | Mapped to `power_to_grid` in the integration. | — | — |
| 3045 | Load demand power | Measured power demanded by local loads (mirrors input registers 3045-3046). | R | — W | — | Used for `power_user_load` in Home Assistant. | — | — |
| 3047 | Total operation time | Cumulative inverter run time. Value/7200 yields hours with 0.5 s resolution. | R | — h | — | — | — | — |
| 3049 | AC Charge Enabled | Enable (1) or disable (0) AC-side charging when running in TL-XH hybrid mode. | R/W | — | — | Home Assistant exposes this as the TL-XH `AC Charge` switch. | — | — |
| 3051 | AC energy total | Lifetime AC energy delivered by the inverter (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3053 | PV energy total | Lifetime PV energy harvested (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3055 | PV 1 energy today | Energy produced by tracker 1 today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3057 | PV 1 energy total | Lifetime energy from tracker 1 (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3059 | PV 2 energy today | Energy produced by tracker 2 today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3061 | PV 2 energy total | Lifetime energy from tracker 2 (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3063 | PV 3 energy today | Energy produced by tracker 3 today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3065 | PV 3 energy total | Lifetime energy from tracker 3 (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3067 | Energy to user today | Energy routed to on-site loads today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3069 | Energy to user total | Lifetime energy routed to on-site loads (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3071 | Energy to grid today | Energy exported to the grid today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3073 | Energy to grid total | Lifetime grid export energy (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3075 | Load energy today | Energy consumed by site loads today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3077 | Load energy total | Lifetime energy consumed by site loads (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3079 | PV 4 energy today | Energy produced by tracker 4 today (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3081 | PV 4 energy total | Lifetime energy from tracker 4 (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3083 | PV energy today (all) | Aggregate PV energy generated today across all trackers (0.1 k Wh increments). | R | — k Wh | — | — | — | — |
| 3085 | Modbus slave address | RS-485 Modbus address (1-254). | R/W | — | — | — | — | — |
| 3086 | RS-485 baud rate | Communication baud rate for the Modbus interface. | R/W | — | — | — | — | — |
| 3087 | Battery rack serial | Battery rack serial number string reported by the BMS (16 ASCII characters). | R | — ASCII | — | — | — | — |
| 3095 | BDC reset command | Issue resets to the battery DC converter: 0 invalid, 1 reset settings, 2 reset calibration, 3 clear historical power. | R/W | — | — | — | — | — |
| 3096 | BDC monitoring code | Four-character identifier for the BDC monitoring firmware (e.g. ZEBA). | R | — ASCII | — | — | — | — |
| 3098 | BDC DTC code | Latest diagnostic trouble code reported by the BDC controller. | R | — | — | — | — | — |
| 3099 | DSP firmware code | Identifier for the inverter DSP firmware build. | R | — ASCII | — | — | — | — |
| 3101 | DSP firmware version | Human-readable DSP firmware version string. | R | — ASCII | — | — | — | — |
| 3102 | Bus voltage reference | Minimum DC bus voltage used for battery charge/discharge control. | R | — V | — | — | — | — |
| 3103 | BDC monitor firmware | BDC monitoring firmware version identifier. | R | — ASCII | — | — | — | — |
| 3104 | BMS MCU hardware version | Hardware revision reported by the BMS MCU. | R | — ASCII | — | — | — | — |
| 3105 | BMS firmware version | Software revision reported by the BMS firmware. | R | — ASCII | — | — | — | — |
| 3106 | BMS manufacturer | Manufacturer name reported by the connected BMS. | R | — ASCII | — | — | — | — |
| 3107 | BMS communication interface | Indicates whether the BMS link uses RS-485 (0) or CAN (1). | R | — | — | — | — | — |
| 3108 | BDC module identifier 4 | ASCII token describing the fourth BDC module slot (if present). | R/W | — ASCII | — | — | — | — |
| 3109 | BDC module identifier 3 | ASCII token describing the third BDC module slot. | R/W | — ASCII | — | — | — | — |
| 3110 | BDC module identifier 2 | ASCII token describing the second BDC module slot. | R/W | — ASCII | — | — | — | — |
| 3111 | BDC module identifier 1 | ASCII token describing the first BDC module slot. | R/W | — ASCII | — | — | — | — |
| 3112 | Reserved | Reserved; reported as zero on known firmware. | R | — | — | — | — | — |
| 3113 | BDC protocol version | BDC protocol version word (high byte = major, low byte = minor). | R | — | — | — | — | — |
| 3114 | BDC certification version | Certification profile identifier for the BDC firmware. | R | — | — | — | — | — |
| 3115 | Reserved | Reserved for future use. | R | — | — | — | — | — |
| 3116 | Reserved | Reserved for future use. | R | — | — | — | — | — |
| 3117 | Reserved | Reserved for future use. | R | — | — | — | — | — |
| 3118 | BDC on/off state | Indicates whether the battery DC converter is currently running (1) or idle (0). | R | — | — | — | — | — |
| 3119 | Dry contact state | Current state of the dry-contact output (0 = open, 1 = closed). | R | — | — | — | — | — |
| 3120 | Reserved | Reserved; reported as zero on TL-XH firmware. | R | — | — | — | — | — |
| 3121 | Self-use power | Instantaneous self-consumption power (0.1 W resolution). | R | — W | — | Not yet surfaced by the Home Assistant integration. | — | — |
| 3123 | System energy today | Energy delivered by the overall system today (0.1 k Wh increments). | R | — k Wh | — | Available in firmware but not yet exposed as an integration attribute. | — | — |

## TL-XH US Holding Registers (3125–3249)
US-specific time schedule and dry-contact configuration registers.

**Applies to:** TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3125 | Us Tou Month Groups | Four registers enabling groups of nine US time-of-use slots by month range and enable flag. | R/W | — | — | us_tou_month_range_block; Stored as `us_tou_month_range_block`; each word selects the start/end month and enable bit for nine slots. | — | — |
| 3129 | Us Tou Slot Table | Complete table of 36 US time-of-use slots defining start/stop times, priority mode, and day grouping. | R/W | — | — | us_tou_schedule_table; Stored as `us_tou_schedule_table`; each slot uses two registers (start word with enable/mode, end word with stop time and day selection). | — | — |
| 3201 | Us Tou Special Day 1 | Override date and up to nine slots applied on the first special day. | R/W | — | — | us_special_day_definition; Stored as `us_special_day_definition`; the first register enables the override and sets month/day, followed by nine optional slots. | — | — |
| 3220 | Us Tou Special Day 2 | Override date and up to nine slots applied on the second special day. | R/W | — | — | us_special_day_definition; Stored as `us_special_day_definition`; mirrors the special day 1 layout for the second override. | — | — |
| 3239 | Us Tou Reserved Block | Reserved registers within the US time-of-use scheduler range. | R/W | — | — | Vendor documentation marks these addresses as reserved; observed values remain zero on known firmware. | — | — |

## TL-XH BDC Metadata Mirrors (5000–5039)
Per-BDC mirror blocks replicating the configuration range at 3085–3124 for each battery DC converter.

**Applies to:** TL-XH hybrids

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5000 | Bdc Slot 1 Metadata | Mirror of registers 3085–3124 for the first battery DC converter (BDC). | R/W | — | — | bdc_metadata_block; Repeat for additional BDCs at 40-register strides (5040–5079, 5080–5119, …). Stored as `bdc_metadata_block`. | — | — |

## TL3/MAX/MID/MAC Holding Registers (125–249)
Three-phase inverter specific holding registers.

**Applies to:** TL3-X/MAX/MID/MAC

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 125 | Inverter type identifier | Sixteen-character ASCII string identifying the inverter hardware variant (register 125 high word, 132 low word). | R | — ASCII | — | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | — | — |
| 133 | Bootloader identifier string | Eight ASCII characters recorded by the bootloader package. The words are ordered high to low across registers 133-136. | R | — ASCII | — | Usually reserved; populated only on development or service firmware builds. | — | — |
| 137 | Reactive power direct-control setpoint | Signed 32-bit reactive power request used when the inverter operates in direct control mode (register 89 = 7). Values are stored in 0.1 var increments. | R/W | — var | — | Positive values command inductive (lagging) vars; negative values request capacitive (leading) vars. | — | — |
| 139 | Reactive priority enable | Enable (1) to prioritise reactive power commands ahead of active power limits when they conflict. Disable (0) to favour active power output. | R/W | — | — | — | — | — |
| 140 | Reactive priority ratio | Dimensionless scaling factor applied when reactive priority is enabled. Divide the register value by 10 to obtain the active-to-reactive trade-off ratio. | R/W | — | — | Tune together with the direct-control setpoint to limit how much active power is sacrificed for reactive support. | — | — |
| 141 | Night reactive support (SVG) | Allows the inverter to remain energised overnight to provide reactive (static var generator) support. Set to 1 to enable, 0 to disable. | R/W | — | — | Enabling consumes a small amount of standby power and should only be used when mandated by the grid operator. | — | — |
| 142 | Frequency-watt boost start | Grid frequency (in 0.01 Hz increments) below which the inverter begins boosting active power according to the frequency-watt curve. | R/W | — Hz | — | Pair with registers 151, 175, and 176 to set the under-frequency support profile. | — | — |
| 143 | Over-frequency recovery point | Frequency threshold (0.01 Hz increments) at which active power recovers to nominal after an over-frequency derate event. | R/W | — Hz | — | Works with registers 154-155 and the recovery delay in register 144. | — | — |
| 144 | Over-frequency recovery delay | Time to wait, in 50 ms increments, before restoring power once the frequency has dropped back below the recovery point (register 143). | R/W | — s | — | — | — | — |
| 145 | Zero-current detection enable | Enable the anti-islanding zero-current detection routine (1) or leave it disabled (0). | R/W | — | — | Disable only when local interconnection rules explicitly forbid the zero-current method. | — | — |
| 146 | Zero-current low voltage | Lower grid voltage limit for zero-current detection, stored in 0.1 V increments. | R/W | — V | 115.0 | — | — | — |
| 147 | Zero-current high voltage | Upper grid voltage limit for zero-current detection, stored in 0.1 V increments. | R/W | — V | 276.0 | — | — | — |
| 148 | High-voltage derate start | Grid voltage at which active power begins to derate because of over-voltage, stored in 0.1 V increments. | R/W | — V | — | — | — | — |
| 149 | High-voltage derate end | Grid voltage at which the high-voltage derating curve reaches its minimum active power output. | R/W | — V | — | Configure together with register 148 to define the slope of the derating curve. | — | — |
| 150 | Q(V) stabilisation time | Settling time applied when the inverter follows the Q(V) curve, in 0.1 s increments. | R/W | — s | — | — | — | — |
| 151 | Frequency-watt boost stop | Upper frequency (0.01 Hz increments) where the under-frequency boost tapers back to nominal power. | R/W | — Hz | — | Defines the end point of the frequency-watt boost region together with register 142. | — | — |
| 152 | CEI under-frequency ramp start | Start frequency for the CEI 0-21 under-frequency active power ramp (0.01 Hz increments). | R/W | — Hz | 49.80 | Applies when the CEI 0-21 grid profile is selected. | — | — |
| 153 | CEI under-frequency ramp end | End frequency for the CEI 0-21 under-frequency ramp (0.01 Hz increments). | R/W | — Hz | 49.10 | — | — | — |
| 154 | CEI over-frequency ramp start | Start frequency for the CEI 0-21 over-frequency derating ramp (0.01 Hz increments). | R/W | — Hz | 50.20 | — | — | — |
| 155 | CEI over-frequency ramp end | End frequency for the CEI 0-21 over-frequency ramp (0.01 Hz increments). | R/W | — Hz | 51.50 | — | — | — |
| 156 | CEI undervoltage ramp start | Start voltage for CEI 0-21 undervoltage load-shedding, stored in 0.1 V increments. | R/W | — V | 220.0 | — | — | — |
| 157 | CEI undervoltage ramp end | End voltage for CEI 0-21 undervoltage load-shedding (0.1 V increments). | R/W | — V | 207.0 | — | — | — |
| 158 | CEI overvoltage ramp start | Start voltage for CEI 0-21 overvoltage load reduction (0.1 V increments). | R/W | — V | 230.0 | — | — | — |
| 159 | CEI overvoltage ramp end | End voltage for CEI 0-21 overvoltage load reduction (0.1 V increments). | R/W | — V | 245.0 | — | — | — |
| 160 | Nominal grid voltage selection | Selects the nominal grid voltage preset used by the UL ride-through tables. | R/W | — | — | Mappings follow the UL parameter tables (e.g. 0=240 V split-phase, 1=208 V three-phase, 2=480 V three-phase, 3=reserved). | — | — |
| 161 | Grid watt restoration delay | Delay before resuming active power export after a grid event, expressed in 20 ms increments. | R/W | — s | — | — | — | — |
| 162 | Reconnect ramp slope | Slope of the active power ramp applied when reconnecting to the grid (value / 10 gives percent per second). | R/W | — %/s | — | — | — | — |
| 163 | LFRT stage 1 frequency | Low-frequency ride-through stage 1 trigger, stored in 0.01 Hz increments (UL profile). | R/W | — Hz | — | — | — | — |
| 164 | LFRT stage 1 duration | Ride-through time for LFRT stage 1, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 165 | LFRT stage 2 frequency | Low-frequency ride-through stage 2 trigger (0.01 Hz increments). | R/W | — Hz | — | — | — | — |
| 166 | LFRT stage 2 duration | Ride-through time for LFRT stage 2, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 167 | HFRT stage 1 frequency | High-frequency ride-through stage 1 trigger (0.01 Hz increments). | R/W | — Hz | — | — | — | — |
| 168 | HFRT stage 1 duration | Ride-through time for HFRT stage 1, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 169 | HFRT stage 2 frequency | High-frequency ride-through stage 2 trigger (0.01 Hz increments). | R/W | — Hz | — | — | — | — |
| 170 | HFRT stage 2 duration | Ride-through time for HFRT stage 2, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 171 | HVRT stage 1 voltage | High-voltage ride-through stage 1 trigger expressed in per-unit (value / 1000). | R/W | — pu | — | — | — | — |
| 172 | HVRT stage 1 duration | Ride-through time for HVRT stage 1, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 173 | HVRT stage 2 voltage | High-voltage ride-through stage 2 trigger in per-unit (value / 1000). | R/W | — pu | — | — | — | — |
| 174 | HVRT stage 2 duration | Ride-through time for HVRT stage 2, recorded in 20 ms increments. | R/W | — s | — | — | — | — |
| 175 | Under-frequency boost delay | Delay applied before increasing power during an under-frequency event, in 50 ms increments. | R/W | — s | 0 | — | — | — |
| 176 | Under-frequency boost rate | Slope of the frequency-watt boost curve. Vendor documentation does not specify the unit; values are proportional to percent power per hertz. | R/W | — | — | Empirically values around 50 correspond to approximately 5% per hertz, but confirm on-site before changing. | — | — |
| 177 | Grid restart high-frequency limit | Frequency threshold (0.01 Hz increments) above which reconnect is inhibited after a trip. | R/W | — Hz | — | — | — | — |
| 178 | Over-frequency derate response time | Time constant controlling how quickly the inverter reduces power during an over-frequency event (0-500 steps). | R/W | — | — | Growatt documentation implies steps of roughly 0.1 s; confirm on-site before changing. | — | — |
| 179 | Under-frequency boost response time | Time constant controlling how quickly the inverter increases power during an under-frequency event (0-500 steps). | R/W | — | — | Steps are vendor-defined; treat as a tuning knob for the frequency-watt boost ramp rate. | — | — |
| 180 | Meter link status | Indicates whether an external energy meter is detected on the communication bus (0=not detected, 1=detected). | R/W | — | — | — | — | — |
| 181 | Optimizer count | Number of optimisers currently paired with the inverter (0-64). | R/W | — | — | Used with Growatt smart optimiser strings. | — | — |
| 182 | Optimizer configuration flag | Reports whether optimiser configuration has completed successfully (0=not configured, 1=complete). | R/W | — | — | — | — | — |
| 183 | PV string scan mode | Number of PV strings supported by the connected optimiser system (0=not supported, 8/16/32 = string count). | R/W | — | — | — | — | — |
| 184 | BDC parallel count | Number of battery DC converters (BDC) linked in parallel with the inverter. | R/W | — | — | — | — | — |
| 185 | Battery pack count | Total number of battery packs discovered across all connected BDCs. | R | — | — | — | — | — |
| 186 | Reserved | Reserved by the protocol for future use. | R | — | — | No documented function. | — | — |
| 187 | VPP function enable status | Indicates whether the virtual power plant (VPP) interface is active (1) or disabled (0). | R | — | — | — | — | — |
| 188 | Datalogger server status | State of the data logger connection to the remote server (0=connection succeeded, 1=connection failed). | R | — | — | — | — | — |
| 200 | PID control reserved | Placeholder register reserved for future PID mitigation features. | R | — | — | No documented behaviour in protocol v 1.24. | — | — |
| 201 | PID operating mode | Selects how the PID (potential induced degradation) mitigation circuit runs. | W | — | — | 0=Automatic on demand, 1=Continuous, 2=All-night forced run. | — | — |
| 202 | PID breaker control | Engage (0) or disengage (1) the PID mitigation hardware. | W | — | — | Leave enabled unless servicing the PID circuit. | — | — |
| 203 | PID output voltage setpoint | Target voltage for the PID mitigation supply in volts. | W | — V | — | — | — | — |
| 209 | Alternate serial number | Extended 30-character serial number buffer stored as ASCII across registers 209-223. | R | — ASCII | — | Used by newer dataloggers; apply via commissioning tools when required. | — | — |
| 229 | Energy calibration factor | Incremental calibration coefficient for the cumulative energy counters (0.1% increments). | R/W | — % | — | Adjust only during factory calibration; value / 10 applies as a percent multiplier. | — | — |
| 230 | Anti-islanding override | Disables anti-islanding protection when set to 1. Intended solely for laboratory diagnostics. | W | — | 0 | Never disable anti-islanding on a grid-connected installation unless explicitly authorised. | — | — |
| 231 | Fan self-test trigger | Write 1 to start the inverter cooling-fan diagnostic cycle. | W | — | — | The inverter clears the flag automatically once the test completes. | — | — |
| 232 | Neutral line monitoring enable | Enable (1) or disable (0) neutral-line monitoring for split-phase grids. | W | — | — | — | — | — |
| 233 | Hardware warning flags | Bitfield reporting hardware self-check issues (GFCI, SPS, EEPROM warnings). | R | — | — | — | — | — |
| 234 | Hardware warning flags (reserved word) | Reserved second word for hardware diagnostics; values currently undocumented. | R | — | — | Monitor for future firmware updates. | — | — |
| 235 | Neutral-to-ground detection | Enable (1) or disable (0) detection of unintended neutral-to-ground connections. | W | — | 1 | Should remain enabled for safety compliance. | — | — |
| 236 | Non-standard voltage range | Selects alternative grid voltage windows for special approvals. | W | — | 0 | 0=Standard range, 1=Voltage grade 1, 2=Voltage grade 2. | — | — |
| 237 | Appointed spec override | Enable (1) to apply a pre-programmed regional specification override. | W | — | — | Use only when instructed by Growatt support. | — | — |
| 238 | Fast MPPT mode | Reserved selector for alternate MPPT tracking speeds. | W | — | 0 | Documented as reserved; leave at 0 unless provided specific guidance. | — | — |
| 239 | Reserved | Reserved register with no documented function. | R | — | — | — | — | — |
| 240 | Commissioning step index | Internal step counter used during factory self-check sequences. Installers should leave this value unchanged. | R/W | — | — | — | — | — |
| 241 | Installer longitude word | Longitude component recorded for remote diagnostics. Scaling is vendor-defined and not interpreted by Home Assistant. | R/W | — | — | High byte stores coarse longitude degrees; low byte stores vendor-specific minutes granularity. | — | — |
| 242 | Installer latitude word | Latitude component recorded for remote diagnostics. Scaling is vendor-defined and not interpreted by Home Assistant. | R/W | — | — | High byte stores coarse latitude degrees; low byte stores vendor-specific minutes granularity. | — | — |
| 190 | — | — | — | — | — | — | — | — |
| 192 | — | — | — | — | — | — | — | — |
| 194 | — | — | — | — | — | — | — | — |
| 196 | — | — | — | — | — | — | — | — |
| 198 | — | — | — | — | — | — | — | — |
| 224 | Time 2 | — | — | — | l Day 2_ | Time | — | — |
| 226 | Time 3 | — | — | — | l Day 2_ | Time | — | — |
| 228 | Time 4 | — | — | — | l Day 2_ | Time | — | — |

## Storage Holding Registers (1000–1124)
Storage (MIX/SPA/SPH) battery configuration holding registers.

**Applies to:** Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1070 | Grid-first discharge limit | Maximum discharge power as a percentage of rated output when operating in grid-first mode (0.1% increments). | R/W | — 0.1% | — | — | — | — |
| 1071 | Grid-first stop SOC | State of charge at which grid-first discharge stops (percent). | R/W | — % | — | — | — | — |
| 1080 | Grid-first slot 1 start | Start time for grid-first discharge slot 1. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1081 | Grid-first slot 1 stop | Stop time for grid-first discharge slot 1. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1082 | Grid-first slot 1 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | — | — | — |
| 1083 | Grid-first slot 2 start | Start time for grid-first discharge slot 2. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1084 | Grid-first slot 2 stop | Stop time for grid-first discharge slot 2. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1085 | Grid-first slot 2 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | When set from the LCD, this slot can be tied to the Force Discharge command. | — | — |
| 1086 | Grid-first slot 3 start | Start time for grid-first discharge slot 3. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1087 | Grid-first slot 3 stop | Stop time for grid-first discharge slot 3. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1088 | Grid-first slot 3 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | — | — | — |
| 1090 | Battery-first charge limit | Maximum AC charge power when operating in battery-first mode (0.1% increments of rated power). | R/W | — 0.1% | — | — | — | — |
| 1091 | Battery-first stop SOC | State of charge above which battery-first charging stops (percent). | R/W | — % | — | — | — | — |
| 1092 | Battery-first AC charge enable | Allow AC charging when operating in battery-first mode (1=enable, 0=disable). | R/W | — | — | — | — | — |
| 1100 | Battery-first slot 1 start | Start time for battery-first timeslot 1. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1101 | Battery-first slot 1 stop | Stop time for battery-first timeslot 1. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1102 | Battery-first slot 1 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | — | — | — |
| 1103 | Battery-first slot 2 start | Start time for battery-first timeslot 2. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1104 | Battery-first slot 2 stop | Stop time for battery-first timeslot 2. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1105 | Battery-first slot 2 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | — | — | — |
| 1106 | Battery-first slot 3 start | Start time for battery-first timeslot 3. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1107 | Battery-first slot 3 stop | Stop time for battery-first timeslot 3. | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1108 | Battery-first slot 3 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | — | — | — |
| 1110 | Load-first slot 1 start | Start time for load-first timeslot 1 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1111 | Load-first slot 1 stop | Stop time for load-first timeslot 1 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1112 | Load-first slot 1 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | Available on SPA models. | — | — |
| 1113 | Load-first slot 2 start | Start time for load-first timeslot 2 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1114 | Load-first slot 2 stop | Stop time for load-first timeslot 2 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1115 | Load-first slot 2 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | Available on SPA models. | — | — |
| 1116 | Load-first slot 3 start | Start time for load-first timeslot 3 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1117 | Load-first slot 3 stop | Stop time for load-first timeslot 3 (SPA models only). | R/W | — hh:mm | — | High byte = hour (0-23); low byte = minute (0-59). | — | — |
| 1118 | Load-first slot 3 enable | Enable (1) or disable (0) this schedule slot. | R/W | — | — | Available on SPA models. | — | — |
| 1119 | Energy calculation formula | Selects the firmware energy-calculation formula (0=legacy, 1=new). | R/W | — | — | — | — | — |
| 1120 | Backup enable | Enable backup output mode (MIX/US storage models). | R/W | — | — | Applicable to MIX US models. | — | — |
| 1121 | SGIP enable | Enable SGIP (Self-Generation Incentive Program) export control features (MIX US models). | R/W | — | — | Applicable to MIX US models. | — | — |

## Storage Holding Registers (1125–1249)
Additional SPA/SPH storage configuration registers.

**Applies to:** Storage SPA/SPH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1125 | 8 the f Bat Serial NO. stora | irst PACK of energy ge batteries / | — | — | — | — | — | — |
| 1126 | 7 Bat Serial NO. | — | / | — | — | — | — | — |
| 1127 | 6 Bat Serial NO. | — | / | — | — | — | — | — |
| 1128 | 5 Bat Serial NO. | — | / | — | — | — | — | — |
| 1129 | 4 Bat Serial NO. | — | / | — | — | — | — | — |
| 1130 | 3 Bat Serial NO. | — | / | — | — | — | — | — |
| 1131 | 2 Bat Serial NO. | — | / | — | — | — | — | — |
| 1132 | 1 Bat Serial NO. 8~ | The serial number of the second to tenth packs of | / | — | — | — | — | — |
| 1132 | Bat Serial NO. | the energy storage batte | ry | — | — | — | — | — |
| 1204 | 1 | consists of nine packs, the format of the serial number of each PACK is 1125 to 1132 | and | — | — | — | — | — |
| 1244 | Com version Nam Name H con | e of the battery main trol firmware version | — | — | — | — | — | — |
| 1245 | Com version Nam Name L con | e of the battery main trol firmware version | — | — | — | — | — | — |
| 1246 | Com versio No | n Version of the battery m control firmware | ain | — | — | — | — | — |
| 1247 | Com version Nam Name H mon ver | e of b itoring firm sion | atter ware | — | — | — | — | — |
| 1248 | Com version Nam Name L mon ver | e of b itoring firm sion | atter ware | — | — | — | — | — |
| 1249 | Com versio No | n Battery monitori firmware version | ng | — | — | — | — | — |

## Common Input Registers (0–124)
Applies to TL3/MAX and legacy inverters for basic PV/AC telemetry.

**Applies to:** TL-X/TL-XH (legacy mode), TL3-X/MAX/MID/MAC, Storage MIX/SPA/SPH, Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Inverter status | Operating state reported by the inverter controller (0=waiting, 1=normal, 3=fault, 5=PV charge, 6=AC charge, 7=combined charge, 8=combined charge bypass, 9=PV charge bypass, 10=AC charge bypass, 11=bypass, 12=PV charge + discharge). | R | — | — | inverter_status_code | tlx:status_code, tl3:status_code, offgrid:status_code | Status code |
| 1 | PV input power | Total PV input power summed across all strings (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 3 | PV 1 DC voltage | Instantaneous PV 1 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 4 | PV 1 DC current | Instantaneous PV 1 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_1_amperage, tl3:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 5 | PV 1 DC power | Real-time DC power from PV 1 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_1_power, tl3:input_1_power, offgrid:input_2_power | Input 1 Wattage, Input 2 Wattage, PV1 charge power, PV2 charge power |
| 7 | PV 2 DC voltage | Instantaneous PV 2 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_2_voltage, tl3:input_2_voltage, offgrid:input_1_amperage | Input 1 Amperage, Input 2 voltage, PV1 buck current, PV2 voltage |
| 8 | PV 2 DC current | Instantaneous PV 2 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_2_amperage, tl3:input_2_amperage, offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9 | PV 2 DC power | Real-time DC power from PV 2 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_2_power, tl3:input_2_power, offgrid:output_active_power | Input 2 Wattage, Output active power, PV2 charge power |
| 11 | PV 3 DC voltage | Instantaneous PV 3 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12 | PV 3 DC current | Instantaneous PV 3 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_3_amperage | Input 3 Amperage |
| 13 | PV 3 DC power | Real-time DC power from PV 3 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 15 | PV 4 DC voltage | Instantaneous PV 4 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16 | PV 4 DC current | Instantaneous PV 4 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17 | PV 4 DC power | Real-time DC power from PV 4 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 19 | PV 5 DC voltage | Instantaneous PV 5 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20 | PV 5 DC current | Instantaneous PV 5 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | PV 5 DC power | Real-time DC power from PV 5 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 23 | PV 6 DC voltage | Instantaneous PV 6 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24 | PV 6 DC current | Instantaneous PV 6 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 25 | PV 6 DC power | Real-time DC power from PV 6 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_6_power, offgrid:inverter_temperature | Input 6 Wattage, Temperature |
| 27 | PV 7 DC voltage | Instantaneous PV 7 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_7_voltage, offgrid:load_percent | Input 7 voltage, Inverter load |
| 28 | PV 7 DC current | Instantaneous PV 7 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_7_amperage, tl3:output_energy_total, offgrid:battery_port_voltage | Battery port voltage, Input 7 Amperage, Total energy produced |
| 29 | PV 7 DC power | Real-time DC power from PV 7 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_7_power, offgrid:battery_bus_voltage | Battery bus voltage, Input 7 Wattage |
| 31 | PV 8 DC voltage | Instantaneous PV 8 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_8_voltage | Input 8 voltage |
| 32 | PV 8 DC current | Instantaneous PV 8 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 33 | PV 8 DC power | Real-time DC power from PV 8 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_8_power | Input 8 Wattage |
| 35 | AC output power | Active AC output power delivered by the inverter (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | tlx:output_power | Output power |
| 37 | Grid frequency | Measured grid frequency with 0.01 Hz resolution. | R | — Hz | — | u 16_frequency_centihz | tlx:grid_frequency | AC frequency, Grid frequency |
| 38 | AC phase L 1 voltage | AC output voltage for phase L 1. | R | — V | — | u 16_voltage_decivolt | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 39 | AC phase L 1 current | AC output current for phase L 1. | R | — A | — | u 16_current_deciamp | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 40 | AC phase L 1 power | Active power exported on phase L 1. | R | — W | — | u 32_power_w_decawatt | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 42 | AC phase L 2 voltage | AC output voltage for phase L 2. | R | — V | — | u 16_voltage_decivolt | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 43 | AC phase L 2 current | AC output current for phase L 2. | R | — A | — | u 16_current_deciamp | tlx:output_2_amperage, tl3:n_bus_voltage, offgrid:warning_code | N-bus voltage, Output 2 Amperage, Warning code |
| 44 | AC phase L 2 power | Active power exported on phase L 2. | R | — W | — | u 32_power_w_decawatt | tlx:output_2_power | Output 2 Wattage |
| 46 | AC phase L 3 voltage | AC output voltage for phase L 3. | R | — V | — | u 16_voltage_decivolt | tlx:output_3_voltage | Output 3 voltage |
| 47 | AC phase L 3 current | AC output current for phase L 3. | R | — A | — | u 16_current_deciamp | tlx:output_3_amperage, tl3:derating_mode, offgrid:constant_power | Derating mode, Output 3 Amperage |
| 48 | AC phase L 3 power | Active power exported on phase L 3. | R | — W | — | u 32_power_w_decawatt | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 53 | Output energy today | Energy exported to the AC output today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:output_energy_today | Energy produced today |
| 55 | Output energy total | Lifetime AC output energy (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:output_energy_total | Total energy produced |
| 57 | Run time | Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours). | R | — h | — | u 32_runtime_hours; Raw counter counts seconds; divide by 7200 to obtain hours. | tlx:operation_hours | Running hours |
| 59 | PV 1 energy today | Energy harvested by PV 1 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 61 | PV 1 energy total | Lifetime energy harvested by PV 1. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 63 | PV 2 energy today | Energy harvested by PV 2 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 65 | PV 2 energy total | Lifetime energy harvested by PV 2. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_2_energy_total, tl3:warning_value | Input 2 total energy, PV2 energy produced Lifetime |
| 67 | PV 3 energy today | Energy harvested by PV 3 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_3_energy_today | Input 3 energy today |
| 69 | PV 3 energy total | Lifetime energy harvested by PV 3. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_3_energy_total, offgrid:discharge_power | Battery discharge power, Discharge Power, Input 3 total energy |
| 71 | PV 4 energy today | Energy harvested by PV 4 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_4_energy_today | Input 4 energy today |
| 73 | PV 4 energy total | Lifetime energy harvested by PV 4. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_4_energy_total, offgrid:battery_discharge_amperage | Battery discharge current, Input 4 total energy |
| 75 | PV 5 energy today | Energy harvested by PV 5 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_5_energy_today | Input 5 energy today |
| 77 | PV 5 energy total | Lifetime energy harvested by PV 5. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_5_energy_total, offgrid:battery_power | Battery charging/ discharging(-ve), Input 5 total energy |
| 79 | PV 6 energy today | Energy harvested by PV 6 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_6_energy_today | Input 6 energy today |
| 81 | PV 6 energy total | Lifetime energy harvested by PV 6. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_6_energy_total | Input 6 total energy |
| 83 | PV 7 energy today | Energy harvested by PV 7 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_7_energy_today | Input 7 energy today |
| 85 | PV 7 energy total | Lifetime energy harvested by PV 7. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_7_energy_total | Input 7 total energy |
| 87 | PV 8 energy today | Energy harvested by PV 8 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_8_energy_today | Input 8 energy today |
| 89 | PV 8 energy total | Lifetime energy harvested by PV 8. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_8_energy_total | Input 8 total energy |
| 91 | PV energy total | Total PV energy generated across all strings (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_energy_total | Total energy input |
| 93 | Inverter temperature | Main inverter heatsink temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:inverter_temperature | Temperature |
| 94 | IPM temperature | IPM (power module) temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95 | Boost temperature | Boost inductor temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:boost_temperature | Boost temperature |
| 98 | P-bus voltage | Positive DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:p_bus_voltage | P-bus voltage |
| 99 | N-bus voltage | Negative DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:n_bus_voltage | N-bus voltage |
| 101 | Output power percentage | Instantaneous AC output as a percentage of the inverter's rated power. | R | — % | — | u 16_percent | tlx:real_output_power_percent | Real power output percentage |
| 104 | Derating mode | Active derating reason reported by the inverter controller. | R | — | — | u 16_raw_code | tlx:derating_mode | Derating mode |
| 105 | Fault code | Current inverter fault code (see protocol documentation). | R | — | — | u 16_status_word | tlx:fault_code | Fault code |
| 110 | Warning code | Current inverter warning code (vendor-defined bitmask). | R | — | — | u 16_status_word | tlx:warning_code | Warning code |

## TL-X/TL-XH Input Registers (3000–3124)
Primary TL-X/TL-XH telemetry mirror (PV/AC metrics).

**Applies to:** TL-X/TL-XH/TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | Inverter status | Operating state reported by the inverter controller (0=waiting, 1=normal, 3=fault, 5=PV charge, 6=AC charge, 7=combined charge, 8=combined charge bypass, 9=PV charge bypass, 10=AC charge bypass, 11=bypass, 12=PV charge + discharge). | R | — | — | inverter_status_code | tlx:status_code | Status code |
| 3001 | PV input power | Total PV input power summed across all strings (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | tlx:input_power | Internal wattage |
| 3003 | PV 1 DC voltage | Instantaneous PV 1 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_1_voltage | Input 1 voltage, PV1 voltage |
| 3004 | PV 1 DC current | Instantaneous PV 1 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 3005 | PV 1 DC power | Real-time DC power from PV 1 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_1_power | Input 1 Wattage, PV1 charge power |
| 3007 | PV 2 DC voltage | Instantaneous PV 2 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3008 | PV 2 DC current | Instantaneous PV 2 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 3009 | PV 2 DC power | Real-time DC power from PV 2 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_2_power | Input 2 Wattage, PV2 charge power |
| 3011 | PV 3 DC voltage | Instantaneous PV 3 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_3_voltage | Input 3 voltage |
| 3012 | PV 3 DC current | Instantaneous PV 3 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_3_amperage | Input 3 Amperage |
| 3013 | PV 3 DC power | Real-time DC power from PV 3 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_3_power | Input 3 Wattage |
| 3015 | PV 4 DC voltage | Instantaneous PV 4 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | tlx:input_4_voltage | Input 4 voltage |
| 3016 | PV 4 DC current | Instantaneous PV 4 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | tlx:input_4_amperage | Input 4 Amperage |
| 3017 | PV 4 DC power | Real-time DC power from PV 4 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | tlx:input_4_power | Input 4 Wattage |
| 3021 | Output reactive power | Instantaneous reactive power on the AC output (positive = inductive, negative = capacitive). | R | — var | — | s 32_reactive_power_decivar | tlx:output_reactive_power | Reactive wattage |
| 3023 | AC output power | Active AC output power delivered by the inverter (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | tlx:output_power | Output power |
| 3025 | Grid frequency | Measured grid frequency with 0.01 Hz resolution. | R | — Hz | — | u 16_frequency_centihz | tlx:grid_frequency | AC frequency, Grid frequency |
| 3026 | AC phase L 1 voltage | AC output voltage for phase L 1. | R | — V | — | u 16_voltage_decivolt | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 3027 | AC phase L 1 current | AC output current for phase L 1. | R | — A | — | u 16_current_deciamp | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 3028 | AC phase L 1 power | Active power exported on phase L 1. | R | — W | — | u 32_power_w_decawatt | tlx:output_1_power | Output 1 Wattage |
| 3030 | AC phase L 2 voltage | AC output voltage for phase L 2. | R | — V | — | u 16_voltage_decivolt | tlx:output_2_voltage | Output 2 voltage |
| 3031 | AC phase L 2 current | AC output current for phase L 2. | R | — A | — | u 16_current_deciamp | tlx:output_2_amperage | Output 2 Amperage |
| 3032 | AC phase L 2 power | Active power exported on phase L 2. | R | — W | — | u 32_power_w_decawatt | tlx:output_2_power | Output 2 Wattage |
| 3034 | AC phase L 3 voltage | AC output voltage for phase L 3. | R | — V | — | u 16_voltage_decivolt | tlx:output_3_voltage | Output 3 voltage |
| 3035 | AC phase L 3 current | AC output current for phase L 3. | R | — A | — | u 16_current_deciamp | tlx:output_3_amperage | Output 3 Amperage |
| 3036 | AC phase L 3 power | Active power exported on phase L 3. | R | — W | — | u 32_power_w_decawatt | tlx:output_3_power | Output 3 Wattage |
| 3041 | Load supply power | Real-time active power delivered to on-site (self-consumption) loads. | R | — W | — | u 32_power_w_decawatt | tlx:power_to_user | Power to user |
| 3043 | Grid export power | Active power exported to the utility grid. | R | — W | — | u 32_power_w_decawatt | tlx:power_to_grid | Power to grid |
| 3045 | Home load power | Aggregate instantaneous demand from on-site loads. | R | — W | — | u 32_power_w_decawatt | tlx:power_user_load | Power user load |
| 3047 | Run time | Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours). | R | — h | — | u 32_runtime_hours; Raw counter counts seconds; divide by 7200 to obtain hours. | tlx:operation_hours | Running hours |
| 3049 | Output energy today | Energy exported to the AC output today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:output_energy_today | Energy produced today |
| 3051 | Output energy total | Lifetime AC output energy (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:output_energy_total | Total energy produced |
| 3053 | PV energy total | Total PV energy generated across all strings (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_energy_total | Total energy input |
| 3055 | PV 1 energy today | Energy harvested by PV 1 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 3057 | PV 1 energy total | Lifetime energy harvested by PV 1. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 3059 | PV 2 energy today | Energy harvested by PV 2 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 3061 | PV 2 energy total | Lifetime energy harvested by PV 2. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 3063 | PV 3 energy today | Energy harvested by PV 3 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_3_energy_today | Input 3 energy today |
| 3065 | PV 3 energy total | Lifetime energy harvested by PV 3. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:input_3_energy_total | Input 3 total energy |
| 3067 | Load energy today | Energy delivered to on-site loads today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:energy_to_user_today | Energy To User (Today) |
| 3069 | Load energy total | Lifetime energy delivered to on-site loads (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:energy_to_user_total | Energy To User (Total) |
| 3071 | Export energy today | Energy exported to the grid today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:energy_to_grid_today | Energy To Grid (Today) |
| 3073 | Export energy total | Lifetime energy exported to the grid (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:energy_to_grid_total | Energy To Grid (Total) |
| 3086 | Derating mode | Active derating reason reported by the inverter controller. | R | — | — | u 16_raw_code | tlx:derating_mode | Derating mode |
| 3093 | Inverter temperature | Main inverter heatsink temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:inverter_temperature | Temperature |
| 3094 | IPM temperature | IPM (power module) temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:ipm_temperature | Intelligent Power Management temperature |
| 3095 | Boost temperature | Boost inductor temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:boost_temperature | Boost temperature |
| 3097 | Communication board temperature | Temperature reported by the communication/control board (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:comm_board_temperature | Comm board temperature |
| 3098 | P-bus voltage | Positive DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:p_bus_voltage | P-bus voltage |
| 3099 | N-bus voltage | Negative DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:n_bus_voltage | N-bus voltage |
| 3101 | Output power percentage | Instantaneous AC output as a percentage of the inverter's rated power. | R | — % | — | u 16_percent | tlx:real_output_power_percent | Real power output percentage |
| 3105 | Fault code | Current inverter fault code (see protocol documentation). | R | — | — | u 16_status_word | tlx:fault_code | Fault code |
| 3110 | Warning code | Current inverter warning code (vendor-defined bitmask). | R | — | — | u 16_status_word | tlx:warning_code | Warning code |
| 3111 | Present FFT value (channel A) | Latest Fast Fourier Transform diagnostic value for channel A. | R | — | — | u 16_raw | tlx:present_fft_a | Present FFT A |
| 3115 | Inverter start delay | Seconds remaining before restart once grid conditions recover. | R | — s | — | u 16_raw | tlx:inv_start_delay | Inverter start delay |

## TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249)
Battery energy, power flow, and BMS telemetry for TL-XH hybrids.

**Applies to:** TL-X/TL-XH hybrids, Storage TL-XH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3125 | Battery discharge today | Energy discharged from the battery into the AC system today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:discharge_energy_today, storage:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 3127 | Battery discharge total | Total energy discharged from the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:discharge_energy_total, storage:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 3129 | Battery charge today | Energy charged into the battery today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:charge_energy_today, storage:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 3131 | Battery charge total | Total energy charged into the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | tlx:charge_energy_total, storage:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 3164 | BDC presence flag | Indicates whether a battery DC converter (BDC) has been detected. | R | — | — | u 16_flag | tlx:bdc_new_flag, storage:bdc_new_flag | BDC present |
| 3169 | Battery voltage | Pack voltage reported via the inverter-side measurements (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | tlx:battery_voltage, storage:battery_voltage | Battery voltage |
| 3170 | Battery current | Current flowing between battery and inverter (positive = discharge) with 0.1 A resolution. | R | — A | — | s 16_current_deciamp | tlx:battery_current, storage:battery_current | Battery current |
| 3171 | Battery SOC | Battery state of charge reported by the inverter. | R | — % | — | u 16_percent | tlx:soc, storage:soc | SOC |
| 3172 | VBUS 1 voltage | BDC high-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:vbus1_voltage, storage:vbus1_voltage | VBUS1 voltage |
| 3173 | VBUS 2 voltage | BDC low-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | tlx:vbus2_voltage, storage:vbus2_voltage | VBUS2 voltage |
| 3174 | Buck/boost current | Current through the BDC buck/boost stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | tlx:buck_boost_current, storage:buck_boost_current | Buck/boost current |
| 3175 | LLC stage current | Current through the LLC resonant stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | tlx:llc_current, storage:llc_current | LLC current |
| 3176 | Battery temperature A | Battery temperature sensor A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:battery_temperature_a, storage:battery_temperature_a | Battery temperature A |
| 3177 | Battery temperature B | Battery temperature sensor B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:battery_temperature_b, storage:battery_temperature_b | Battery temperature B |
| 3178 | Battery discharge power | Real-time discharge power flowing from the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | tlx:discharge_power, storage:discharge_power | Battery discharge power, Discharge Power |
| 3180 | Battery charge power | Real-time charge power flowing into the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | tlx:charge_power, storage:charge_power | Battery charge power, Charge Power |
| 3189 | BMS max cell index | Cell index reporting the highest voltage in the battery stack (1-based). | R | — | — | u 16_raw | tlx:bms_max_volt_cell_no, storage:bms_max_volt_cell_no | BMS max volt cell no |
| 3190 | BMS min cell index | Cell index reporting the lowest voltage in the battery stack (1-based). | R | — | — | u 16_raw | tlx:bms_min_volt_cell_no, storage:bms_min_volt_cell_no | BMS min volt cell no |
| 3191 | BMS average temperature A | Average temperature reported by sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_avg_temp_a, storage:bms_avg_temp_a | BMS avg temp A |
| 3192 | BMS max cell temperature A | Maximum cell temperature within sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_max_cell_temp_a, storage:bms_max_cell_temp_a | BMS max cell temp A |
| 3193 | BMS average temperature B | Average temperature reported by sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_avg_temp_b, storage:bms_avg_temp_b | BMS avg temp B |
| 3194 | BMS max cell temperature B | Maximum cell temperature within sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_max_cell_temp_b, storage:bms_max_cell_temp_b | BMS max cell temp B |
| 3195 | BMS average temperature C | Average temperature reported by sensor group C (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_avg_temp_c, storage:bms_avg_temp_c | BMS avg temp C |
| 3196 | BMS max SOC | Highest state of charge observed across battery modules. | R | — % | — | u 16_percent | tlx:bms_max_soc, storage:bms_max_soc | BMS max SOC |
| 3197 | BMS min SOC | Lowest state of charge observed across battery modules. | R | — % | — | u 16_percent | tlx:bms_min_soc, storage:bms_min_soc | BMS min SOC |
| 3198 | Parallel battery count | Number of battery modules detected in parallel. | R | — | — | u 16_raw | tlx:parallel_battery_num, storage:parallel_battery_num | — |
| 3199 | BMS derate reason | Reason code reported by the BMS for power derating. | R | — | — | u 16_raw | tlx:bms_derate_reason, storage:bms_derate_reason | BMS derate reason |
| 3200 | BMS full charge capacity | Full charge capacity (FCC) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | tlx:bms_gauge_fcc_ah, storage:bms_gauge_fcc_ah | BMS full charge capacity |
| 3201 | BMS remaining capacity | Remaining capacity (RM) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | tlx:bms_gauge_rm_ah, storage:bms_gauge_rm_ah | BMS remaining capacity |
| 3202 | BMS protect flags 1 | Protection bitmask word 1 from the battery management system. | R | — | — | u 16_raw | tlx:bms_protect1, storage:bms_protect1 | BMS protect 1 |
| 3203 | BMS warning flags 1 | Warning bitmask word 1 from the battery management system. | R | — | — | u 16_raw | tlx:bms_warn1, storage:bms_warn1 | BMS warn 1 |
| 3204 | BMS fault flags 1 | Fault bitmask word 1 from the battery management system. | R | — | — | u 16_raw | tlx:bms_fault1, storage:bms_fault1 | BMS fault 1 |
| 3205 | BMS fault flags 2 | Fault bitmask word 2 from the battery management system. | R | — | — | u 16_raw | tlx:bms_fault2, storage:bms_fault2 | BMS fault 2 |
| 3210 | Battery insulation status | Isolation detection status reported by the BMS (0 = not detected, 1 = detected). | R | — | — | u 16_raw | tlx:bat_iso_status, storage:bat_iso_status | — |
| 3211 | Battery request flags | Bitmask of requests from the BMS to the inverter (charge/discharge permissions). | R | — | — | u 16_raw | tlx:batt_request_flags, storage:batt_request_flags | — |
| 3212 | BMS status | Overall battery management system status code. | R | — | — | u 16_raw | tlx:bms_status, storage:bms_status | BMS status |
| 3213 | BMS protect flags 2 | Protection bitmask word 2 from the battery management system. | R | — | — | u 16_raw | tlx:bms_protect2, storage:bms_protect2 | BMS protect 2 |
| 3214 | BMS warning flags 2 | Warning bitmask word 2 from the battery management system. | R | — | — | u 16_raw | tlx:bms_warn2, storage:bms_warn2 | BMS warn 2 |
| 3215 | BMS SOC | State of charge reported directly by the BMS. | R | — % | — | u 16_percent | tlx:bms_soc, storage:bms_soc | BMS SOC |
| 3216 | BMS battery voltage | Pack voltage reported by the BMS (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | tlx:bms_battery_voltage, storage:bms_battery_voltage | BMS battery voltage |
| 3217 | BMS battery current | Current reported by the BMS with 0.01 A resolution (positive = discharge). | R | — A | — | s 16_current_centiamp; Positive values indicate discharge from the battery; negative values indicate charging. | tlx:bms_battery_current, storage:bms_battery_current | BMS battery current |
| 3218 | BMS max cell temperature | Maximum cell temperature observed across the battery pack (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | tlx:bms_cell_max_temp, storage:bms_cell_max_temp | BMS cell max temperature |
| 3219 | BMS max charge current | Maximum charge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | tlx:bms_max_charge_current, storage:bms_max_charge_current | BMS max charge current |
| 3220 | BMS max discharge current | Maximum discharge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | tlx:bms_max_discharge_current, storage:bms_max_discharge_current | BMS max discharge current |
| 3221 | BMS cycle count | Total charge/discharge cycles counted by the BMS. | R | — | — | u 16_raw | tlx:bms_cycle_count, storage:bms_cycle_count | BMS cycle count |
| 3222 | BMS state of health | Battery state of health reported by the BMS. | R | — % | — | u 16_percent | tlx:bms_soh, storage:bms_soh | BMS SOH |
| 3223 | BMS charge voltage limit | Maximum pack voltage permitted during charge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | tlx:bms_charge_volt_limit, storage:bms_charge_volt_limit | BMS charge voltage limit |
| 3224 | BMS discharge voltage limit | Minimum pack voltage permitted during discharge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | tlx:bms_discharge_volt_limit, storage:bms_discharge_volt_limit | BMS discharge voltage limit |
| 3225 | BMS warning flags 3 | Warning bitmask word 3 from the battery management system. | R | — | — | u 16_raw | tlx:bms_warn3, storage:bms_warn3 | BMS warn 3 |
| 3226 | BMS protect flags 3 | Protection bitmask word 3 from the battery management system. | R | — | — | u 16_raw | tlx:bms_protect3, storage:bms_protect3 | BMS protect 3 |
| 3230 | BMS max cell voltage | Highest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | tlx:bms_cell_volt_max, storage:bms_cell_volt_max | BMS cell voltage max |
| 3231 | BMS min cell voltage | Lowest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | tlx:bms_cell_volt_min, storage:bms_cell_volt_min | BMS cell voltage min |

## Storage TL-XH Input Registers (3041–3231)
BDC telemetry (battery module data) for TL-XH hybrids.

**Applies to:** Storage TL-XH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3041 | Load supply power | Real-time active power delivered to on-site (self-consumption) loads. | R | — W | — | u 32_power_w_decawatt | storage:power_to_user | Power to user |
| 3043 | Grid export power | Active power exported to the utility grid. | R | — W | — | u 32_power_w_decawatt | storage:power_to_grid | Power to grid |
| 3045 | Home load power | Aggregate instantaneous demand from on-site loads. | R | — W | — | u 32_power_w_decawatt | storage:power_user_load | Power user load |
| 3047 | Run time | Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours). | R | — h | — | u 32_runtime_hours; Raw counter counts seconds; divide by 7200 to obtain hours. | — | — |
| 3049 | Output energy today | Energy exported to the AC output today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3051 | Output energy total | Lifetime AC output energy (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3053 | PV energy total | Total PV energy generated across all strings (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3055 | PV 1 energy today | Energy harvested by PV 1 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3057 | PV 1 energy total | Lifetime energy harvested by PV 1. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3059 | PV 2 energy today | Energy harvested by PV 2 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3061 | PV 2 energy total | Lifetime energy harvested by PV 2. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3063 | PV 3 energy today | Energy harvested by PV 3 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3065 | PV 3 energy total | Lifetime energy harvested by PV 3. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3067 | Load energy today | Energy delivered to on-site loads today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:energy_to_user_today | Energy To User (Today) |
| 3069 | Load energy total | Lifetime energy delivered to on-site loads (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:energy_to_user_total | Energy To User (Total) |
| 3071 | Export energy today | Energy exported to the grid today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:energy_to_grid_today | Energy To Grid (Today) |
| 3073 | Export energy total | Lifetime energy exported to the grid (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:energy_to_grid_total | Energy To Grid (Total) |
| 3086 | Derating mode | Active derating reason reported by the inverter controller. | R | — | — | u 16_raw_code | — | — |
| 3093 | Inverter temperature | Main inverter heatsink temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3094 | IPM temperature | IPM (power module) temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3095 | Boost temperature | Boost inductor temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3097 | Communication board temperature | Temperature reported by the communication/control board (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:comm_board_temperature | Comm board temperature |
| 3098 | P-bus voltage | Positive DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3099 | N-bus voltage | Negative DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3101 | Output power percentage | Instantaneous AC output as a percentage of the inverter's rated power. | R | — % | — | u 16_percent | — | — |
| 3105 | Fault code | Current inverter fault code (see protocol documentation). | R | — | — | u 16_status_word | — | — |
| 3110 | Warning code | Current inverter warning code (vendor-defined bitmask). | R | — | — | u 16_status_word | — | — |
| 3111 | Present FFT value (channel A) | Latest Fast Fourier Transform diagnostic value for channel A. | R | — | — | u 16_raw | storage:present_fft_a | Present FFT A |
| 3115 | Inverter start delay | Seconds remaining before restart once grid conditions recover. | R | — s | — | u 16_raw | storage:inv_start_delay | Inverter start delay |
| 3125 | Battery discharge today | Energy discharged from the battery into the AC system today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 3127 | Battery discharge total | Total energy discharged from the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 3129 | Battery charge today | Energy charged into the battery today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 3131 | Battery charge total | Total energy charged into the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | storage:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 3164 | BDC presence flag | Indicates whether a battery DC converter (BDC) has been detected. | R | — | — | u 16_flag | storage:bdc_new_flag | BDC present |
| 3169 | Battery voltage | Pack voltage reported via the inverter-side measurements (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | storage:battery_voltage | Battery voltage |
| 3170 | Battery current | Current flowing between battery and inverter (positive = discharge) with 0.1 A resolution. | R | — A | — | s 16_current_deciamp | storage:battery_current | Battery current |
| 3171 | Battery SOC | Battery state of charge reported by the inverter. | R | — % | — | u 16_percent | storage:soc | SOC |
| 3172 | VBUS 1 voltage | BDC high-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | storage:vbus1_voltage | VBUS1 voltage |
| 3173 | VBUS 2 voltage | BDC low-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | storage:vbus2_voltage | VBUS2 voltage |
| 3174 | Buck/boost current | Current through the BDC buck/boost stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | storage:buck_boost_current | Buck/boost current |
| 3175 | LLC stage current | Current through the LLC resonant stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | storage:llc_current | LLC current |
| 3176 | Battery temperature A | Battery temperature sensor A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:battery_temperature_a | Battery temperature A |
| 3177 | Battery temperature B | Battery temperature sensor B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:battery_temperature_b | Battery temperature B |
| 3178 | Battery discharge power | Real-time discharge power flowing from the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | storage:discharge_power | Battery discharge power, Discharge Power |
| 3180 | Battery charge power | Real-time charge power flowing into the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | storage:charge_power | Battery charge power, Charge Power |
| 3189 | BMS max cell index | Cell index reporting the highest voltage in the battery stack (1-based). | R | — | — | u 16_raw | storage:bms_max_volt_cell_no | BMS max volt cell no |
| 3190 | BMS min cell index | Cell index reporting the lowest voltage in the battery stack (1-based). | R | — | — | u 16_raw | storage:bms_min_volt_cell_no | BMS min volt cell no |
| 3191 | BMS average temperature A | Average temperature reported by sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_avg_temp_a | BMS avg temp A |
| 3192 | BMS max cell temperature A | Maximum cell temperature within sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_max_cell_temp_a | BMS max cell temp A |
| 3193 | BMS average temperature B | Average temperature reported by sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_avg_temp_b | BMS avg temp B |
| 3194 | BMS max cell temperature B | Maximum cell temperature within sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_max_cell_temp_b | BMS max cell temp B |
| 3195 | BMS average temperature C | Average temperature reported by sensor group C (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_avg_temp_c | BMS avg temp C |
| 3196 | BMS max SOC | Highest state of charge observed across battery modules. | R | — % | — | u 16_percent | storage:bms_max_soc | BMS max SOC |
| 3197 | BMS min SOC | Lowest state of charge observed across battery modules. | R | — % | — | u 16_percent | storage:bms_min_soc | BMS min SOC |
| 3198 | Parallel battery count | Number of battery modules detected in parallel. | R | — | — | u 16_raw | storage:parallel_battery_num | — |
| 3199 | BMS derate reason | Reason code reported by the BMS for power derating. | R | — | — | u 16_raw | storage:bms_derate_reason | BMS derate reason |
| 3200 | BMS full charge capacity | Full charge capacity (FCC) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | storage:bms_gauge_fcc_ah | BMS full charge capacity |
| 3201 | BMS remaining capacity | Remaining capacity (RM) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | storage:bms_gauge_rm_ah | BMS remaining capacity |
| 3202 | BMS protect flags 1 | Protection bitmask word 1 from the battery management system. | R | — | — | u 16_raw | storage:bms_protect1 | BMS protect 1 |
| 3203 | BMS warning flags 1 | Warning bitmask word 1 from the battery management system. | R | — | — | u 16_raw | storage:bms_warn1 | BMS warn 1 |
| 3204 | BMS fault flags 1 | Fault bitmask word 1 from the battery management system. | R | — | — | u 16_raw | storage:bms_fault1 | BMS fault 1 |
| 3205 | BMS fault flags 2 | Fault bitmask word 2 from the battery management system. | R | — | — | u 16_raw | storage:bms_fault2 | BMS fault 2 |
| 3210 | Battery insulation status | Isolation detection status reported by the BMS (0 = not detected, 1 = detected). | R | — | — | u 16_raw | storage:bat_iso_status | — |
| 3211 | Battery request flags | Bitmask of requests from the BMS to the inverter (charge/discharge permissions). | R | — | — | u 16_raw | storage:batt_request_flags | — |
| 3212 | BMS status | Overall battery management system status code. | R | — | — | u 16_raw | storage:bms_status | BMS status |
| 3213 | BMS protect flags 2 | Protection bitmask word 2 from the battery management system. | R | — | — | u 16_raw | storage:bms_protect2 | BMS protect 2 |
| 3214 | BMS warning flags 2 | Warning bitmask word 2 from the battery management system. | R | — | — | u 16_raw | storage:bms_warn2 | BMS warn 2 |
| 3215 | BMS SOC | State of charge reported directly by the BMS. | R | — % | — | u 16_percent | storage:bms_soc | BMS SOC |
| 3216 | BMS battery voltage | Pack voltage reported by the BMS (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | storage:bms_battery_voltage | BMS battery voltage |
| 3217 | BMS battery current | Current reported by the BMS with 0.01 A resolution (positive = discharge). | R | — A | — | s 16_current_centiamp; Positive values indicate discharge from the battery; negative values indicate charging. | storage:bms_battery_current | BMS battery current |
| 3218 | BMS max cell temperature | Maximum cell temperature observed across the battery pack (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | storage:bms_cell_max_temp | BMS cell max temperature |
| 3219 | BMS max charge current | Maximum charge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | storage:bms_max_charge_current | BMS max charge current |
| 3220 | BMS max discharge current | Maximum discharge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | storage:bms_max_discharge_current | BMS max discharge current |
| 3221 | BMS cycle count | Total charge/discharge cycles counted by the BMS. | R | — | — | u 16_raw | storage:bms_cycle_count | BMS cycle count |
| 3222 | BMS state of health | Battery state of health reported by the BMS. | R | — % | — | u 16_percent | storage:bms_soh | BMS SOH |
| 3223 | BMS charge voltage limit | Maximum pack voltage permitted during charge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | storage:bms_charge_volt_limit | BMS charge voltage limit |
| 3224 | BMS discharge voltage limit | Minimum pack voltage permitted during discharge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | storage:bms_discharge_volt_limit | BMS discharge voltage limit |
| 3225 | BMS warning flags 3 | Warning bitmask word 3 from the battery management system. | R | — | — | u 16_raw | storage:bms_warn3 | BMS warn 3 |
| 3226 | BMS protect flags 3 | Protection bitmask word 3 from the battery management system. | R | — | — | u 16_raw | storage:bms_protect3 | BMS protect 3 |
| 3230 | BMS max cell voltage | Highest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | storage:bms_cell_volt_max | BMS cell voltage max |
| 3231 | BMS min cell voltage | Lowest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | storage:bms_cell_volt_min | BMS cell voltage min |

## Offgrid SPF Input Registers
Observed off-grid register map (from integration implementation).

**Applies to:** Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Inverter status | Operating state reported by the inverter controller (0=waiting, 1=normal, 3=fault, 5=PV charge, 6=AC charge, 7=combined charge, 8=combined charge bypass, 9=PV charge bypass, 10=AC charge bypass, 11=bypass, 12=PV charge + discharge). | R | — | — | inverter_status_code | offgrid:status_code | Status code |
| 1 | PV input power | Total PV input power summed across all strings (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 3 | PV 1 DC voltage | Instantaneous PV 1 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 4 | PV 1 DC current | Instantaneous PV 1 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 5 | PV 1 DC power | Real-time DC power from PV 1 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:input_2_power | Input 2 Wattage, PV2 charge power |
| 7 | PV 2 DC voltage | Instantaneous PV 2 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | offgrid:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 8 | PV 2 DC current | Instantaneous PV 2 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9 | PV 2 DC power | Real-time DC power from PV 2 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:output_active_power | Output active power |
| 11 | PV 3 DC voltage | Instantaneous PV 3 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 12 | PV 3 DC current | Instantaneous PV 3 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 13 | PV 3 DC power | Real-time DC power from PV 3 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:charge_power | Battery charge power, Charge Power |
| 15 | PV 4 DC voltage | Instantaneous PV 4 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 16 | PV 4 DC current | Instantaneous PV 4 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 17 | PV 4 DC power | Real-time DC power from PV 4 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:battery_voltage | Battery voltage |
| 19 | PV 5 DC voltage | Instantaneous PV 5 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | offgrid:bus_voltage | Bus voltage |
| 20 | PV 5 DC current | Instantaneous PV 5 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | offgrid:grid_voltage | Grid voltage |
| 21 | PV 5 DC power | Real-time DC power from PV 5 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:grid_frequency | AC frequency, Grid frequency |
| 23 | PV 6 DC voltage | Instantaneous PV 6 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | offgrid:output_frequency | Output frequency |
| 24 | PV 6 DC current | Instantaneous PV 6 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | offgrid:output_dc_voltage | Output DC voltage |
| 25 | PV 6 DC power | Real-time DC power from PV 6 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:inverter_temperature | Temperature |
| 27 | PV 7 DC voltage | Instantaneous PV 7 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | offgrid:load_percent | Inverter load |
| 28 | PV 7 DC current | Instantaneous PV 7 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | offgrid:battery_port_voltage | Battery port voltage |
| 29 | PV 7 DC power | Real-time DC power from PV 7 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | offgrid:battery_bus_voltage | Battery bus voltage |
| 31 | PV 8 DC voltage | Instantaneous PV 8 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 32 | PV 8 DC current | Instantaneous PV 8 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 33 | PV 8 DC power | Real-time DC power from PV 8 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | — | — |
| 35 | AC output power | Active AC output power delivered by the inverter (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | — | — |
| 37 | Grid frequency | Measured grid frequency with 0.01 Hz resolution. | R | — Hz | — | u 16_frequency_centihz | — | — |
| 38 | AC phase L 1 voltage | AC output voltage for phase L 1. | R | — V | — | u 16_voltage_decivolt | — | — |
| 39 | AC phase L 1 current | AC output current for phase L 1. | R | — A | — | u 16_current_deciamp | — | — |
| 40 | AC phase L 1 power | Active power exported on phase L 1. | R | — W | — | u 32_power_w_decawatt | — | — |
| 42 | AC phase L 2 voltage | AC output voltage for phase L 2. | R | — V | — | u 16_voltage_decivolt | offgrid:fault_code | Fault code |
| 43 | AC phase L 2 current | AC output current for phase L 2. | R | — A | — | u 16_current_deciamp | offgrid:warning_code | Warning code |
| 44 | AC phase L 2 power | Active power exported on phase L 2. | R | — W | — | u 32_power_w_decawatt | — | — |
| 46 | AC phase L 3 voltage | AC output voltage for phase L 3. | R | — V | — | u 16_voltage_decivolt | — | — |
| 47 | AC phase L 3 current | AC output current for phase L 3. | R | — A | — | u 16_current_deciamp | offgrid:constant_power | — |
| 48 | AC phase L 3 power | Active power exported on phase L 3. | R | — W | — | u 32_power_w_decawatt | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 53 | Output energy today | Energy exported to the AC output today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 55 | Output energy total | Lifetime AC output energy (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 57 | Run time | Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours). | R | — h | — | u 32_runtime_hours; Raw counter counts seconds; divide by 7200 to obtain hours. | — | — |
| 59 | PV 1 energy today | Energy harvested by PV 1 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 61 | PV 1 energy total | Lifetime energy harvested by PV 1. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 63 | PV 2 energy today | Energy harvested by PV 2 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 65 | PV 2 energy total | Lifetime energy harvested by PV 2. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 67 | PV 3 energy today | Energy harvested by PV 3 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 69 | PV 3 energy total | Lifetime energy harvested by PV 3. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | offgrid:discharge_power | Battery discharge power, Discharge Power |
| 71 | PV 4 energy today | Energy harvested by PV 4 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 73 | PV 4 energy total | Lifetime energy harvested by PV 4. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | offgrid:battery_discharge_amperage | Battery discharge current |
| 75 | PV 5 energy today | Energy harvested by PV 5 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 77 | PV 5 energy total | Lifetime energy harvested by PV 5. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | offgrid:battery_power | Battery charging/ discharging(-ve) |
| 79 | PV 6 energy today | Energy harvested by PV 6 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 81 | PV 6 energy total | Lifetime energy harvested by PV 6. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 83 | PV 7 energy today | Energy harvested by PV 7 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 85 | PV 7 energy total | Lifetime energy harvested by PV 7. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 87 | PV 8 energy today | Energy harvested by PV 8 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 89 | PV 8 energy total | Lifetime energy harvested by PV 8. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 91 | PV energy total | Total PV energy generated across all strings (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 93 | Inverter temperature | Main inverter heatsink temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 94 | IPM temperature | IPM (power module) temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 95 | Boost temperature | Boost inductor temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 98 | P-bus voltage | Positive DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 99 | N-bus voltage | Negative DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 101 | Output power percentage | Instantaneous AC output as a percentage of the inverter's rated power. | R | — % | — | u 16_percent | — | — |
| 104 | Derating mode | Active derating reason reported by the inverter controller. | R | — | — | u 16_raw_code | — | — |
| 105 | Fault code | Current inverter fault code (see protocol documentation). | R | — | — | u 16_status_word | — | — |
| 110 | Warning code | Current inverter warning code (vendor-defined bitmask). | R | — | — | u 16_status_word | — | — |
| 234 | Output reactive power | Instantaneous reactive power on the AC output (positive = inductive, negative = capacitive). | R | — var | — | s 32_reactive_power_decivar | — | — |
| 236 | Reactive energy total | Lifetime accumulated reactive energy (0.1 kvarh resolution). | R | — kvarh | — | u 32_energy_kvarh_decitenth | — | — |
| 3000 | Inverter status | Operating state reported by the inverter controller (0=waiting, 1=normal, 3=fault, 5=PV charge, 6=AC charge, 7=combined charge, 8=combined charge bypass, 9=PV charge bypass, 10=AC charge bypass, 11=bypass, 12=PV charge + discharge). | R | — | — | inverter_status_code | — | — |
| 3001 | PV input power | Total PV input power summed across all strings (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | — | — |
| 3003 | PV 1 DC voltage | Instantaneous PV 1 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3004 | PV 1 DC current | Instantaneous PV 1 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 3005 | PV 1 DC power | Real-time DC power from PV 1 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3007 | PV 2 DC voltage | Instantaneous PV 2 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3008 | PV 2 DC current | Instantaneous PV 2 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 3009 | PV 2 DC power | Real-time DC power from PV 2 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3011 | PV 3 DC voltage | Instantaneous PV 3 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3012 | PV 3 DC current | Instantaneous PV 3 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 3013 | PV 3 DC power | Real-time DC power from PV 3 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3015 | PV 4 DC voltage | Instantaneous PV 4 string voltage measured at the inverter input. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3016 | PV 4 DC current | Instantaneous PV 4 string current flowing into the inverter. | R | — A | — | u 16_current_deciamp | — | — |
| 3017 | PV 4 DC power | Real-time DC power from PV 4 computed from voltage and current readings. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3021 | Output reactive power | Instantaneous reactive power on the AC output (positive = inductive, negative = capacitive). | R | — var | — | s 32_reactive_power_decivar | — | — |
| 3023 | AC output power | Active AC output power delivered by the inverter (0.1 W resolution). | R | — W | — | u 32_power_w_decawatt | — | — |
| 3025 | Grid frequency | Measured grid frequency with 0.01 Hz resolution. | R | — Hz | — | u 16_frequency_centihz | — | — |
| 3026 | AC phase L 1 voltage | AC output voltage for phase L 1. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3027 | AC phase L 1 current | AC output current for phase L 1. | R | — A | — | u 16_current_deciamp | — | — |
| 3028 | AC phase L 1 power | Active power exported on phase L 1. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3030 | AC phase L 2 voltage | AC output voltage for phase L 2. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3031 | AC phase L 2 current | AC output current for phase L 2. | R | — A | — | u 16_current_deciamp | — | — |
| 3032 | AC phase L 2 power | Active power exported on phase L 2. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3034 | AC phase L 3 voltage | AC output voltage for phase L 3. | R | — V | — | u 16_voltage_decivolt | — | — |
| 3035 | AC phase L 3 current | AC output current for phase L 3. | R | — A | — | u 16_current_deciamp | — | — |
| 3036 | AC phase L 3 power | Active power exported on phase L 3. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3041 | Load supply power | Real-time active power delivered to on-site (self-consumption) loads. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3043 | Grid export power | Active power exported to the utility grid. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3045 | Home load power | Aggregate instantaneous demand from on-site loads. | R | — W | — | u 32_power_w_decawatt | — | — |
| 3047 | Run time | Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours). | R | — h | — | u 32_runtime_hours; Raw counter counts seconds; divide by 7200 to obtain hours. | — | — |
| 3049 | Output energy today | Energy exported to the AC output today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3051 | Output energy total | Lifetime AC output energy (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3053 | PV energy total | Total PV energy generated across all strings (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3055 | PV 1 energy today | Energy harvested by PV 1 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3057 | PV 1 energy total | Lifetime energy harvested by PV 1. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3059 | PV 2 energy today | Energy harvested by PV 2 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3061 | PV 2 energy total | Lifetime energy harvested by PV 2. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3063 | PV 3 energy today | Energy harvested by PV 3 today. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3065 | PV 3 energy total | Lifetime energy harvested by PV 3. Values use 0.1 k Wh resolution. | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3067 | Load energy today | Energy delivered to on-site loads today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3069 | Load energy total | Lifetime energy delivered to on-site loads (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3071 | Export energy today | Energy exported to the grid today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3073 | Export energy total | Lifetime energy exported to the grid (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3086 | Derating mode | Active derating reason reported by the inverter controller. | R | — | — | u 16_raw_code | — | — |
| 3093 | Inverter temperature | Main inverter heatsink temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3094 | IPM temperature | IPM (power module) temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3095 | Boost temperature | Boost inductor temperature (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3097 | Communication board temperature | Temperature reported by the communication/control board (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3098 | P-bus voltage | Positive DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3099 | N-bus voltage | Negative DC bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3101 | Output power percentage | Instantaneous AC output as a percentage of the inverter's rated power. | R | — % | — | u 16_percent | — | — |
| 3105 | Fault code | Current inverter fault code (see protocol documentation). | R | — | — | u 16_status_word | — | — |
| 3110 | Warning code | Current inverter warning code (vendor-defined bitmask). | R | — | — | u 16_status_word | — | — |
| 3111 | Present FFT value (channel A) | Latest Fast Fourier Transform diagnostic value for channel A. | R | — | — | u 16_raw | — | — |
| 3115 | Inverter start delay | Seconds remaining before restart once grid conditions recover. | R | — s | — | u 16_raw | — | — |
| 3125 | Battery discharge today | Energy discharged from the battery into the AC system today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3127 | Battery discharge total | Total energy discharged from the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3129 | Battery charge today | Energy charged into the battery today (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3131 | Battery charge total | Total energy charged into the battery (0.1 k Wh resolution). | R | — k Wh | — | u 32_energy_kwh_decitenth | — | — |
| 3164 | BDC presence flag | Indicates whether a battery DC converter (BDC) has been detected. | R | — | — | u 16_flag | — | — |
| 3169 | Battery voltage | Pack voltage reported via the inverter-side measurements (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | — | — |
| 3170 | Battery current | Current flowing between battery and inverter (positive = discharge) with 0.1 A resolution. | R | — A | — | s 16_current_deciamp | — | — |
| 3171 | Battery SOC | Battery state of charge reported by the inverter. | R | — % | — | u 16_percent | — | — |
| 3172 | VBUS 1 voltage | BDC high-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3173 | VBUS 2 voltage | BDC low-side bus voltage (0.1 V resolution). | R | — V | — | u 16_voltage_decivolt | — | — |
| 3174 | Buck/boost current | Current through the BDC buck/boost stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | — | — |
| 3175 | LLC stage current | Current through the LLC resonant stage (0.1 A resolution). | R | — A | — | u 16_current_deciamp | — | — |
| 3176 | Battery temperature A | Battery temperature sensor A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3177 | Battery temperature B | Battery temperature sensor B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3178 | Battery discharge power | Real-time discharge power flowing from the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | — | — |
| 3180 | Battery charge power | Real-time charge power flowing into the battery (0.1 W resolution). | R | — W | — | s 32_power_w_decawatt | — | — |
| 3189 | BMS max cell index | Cell index reporting the highest voltage in the battery stack (1-based). | R | — | — | u 16_raw | — | — |
| 3190 | BMS min cell index | Cell index reporting the lowest voltage in the battery stack (1-based). | R | — | — | u 16_raw | — | — |
| 3191 | BMS average temperature A | Average temperature reported by sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3192 | BMS max cell temperature A | Maximum cell temperature within sensor group A (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3193 | BMS average temperature B | Average temperature reported by sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3194 | BMS max cell temperature B | Maximum cell temperature within sensor group B (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3195 | BMS average temperature C | Average temperature reported by sensor group C (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3196 | BMS max SOC | Highest state of charge observed across battery modules. | R | — % | — | u 16_percent | — | — |
| 3197 | BMS min SOC | Lowest state of charge observed across battery modules. | R | — % | — | u 16_percent | — | — |
| 3198 | Parallel battery count | Number of battery modules detected in parallel. | R | — | — | u 16_raw | — | — |
| 3199 | BMS derate reason | Reason code reported by the BMS for power derating. | R | — | — | u 16_raw | — | — |
| 3200 | BMS full charge capacity | Full charge capacity (FCC) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | — | — |
| 3201 | BMS remaining capacity | Remaining capacity (RM) reported by the battery fuel gauge (Ah). | R | — Ah | — | u 16_ampere_hour | — | — |
| 3202 | BMS protect flags 1 | Protection bitmask word 1 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3203 | BMS warning flags 1 | Warning bitmask word 1 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3204 | BMS fault flags 1 | Fault bitmask word 1 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3205 | BMS fault flags 2 | Fault bitmask word 2 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3210 | Battery insulation status | Isolation detection status reported by the BMS (0 = not detected, 1 = detected). | R | — | — | u 16_raw | — | — |
| 3211 | Battery request flags | Bitmask of requests from the BMS to the inverter (charge/discharge permissions). | R | — | — | u 16_raw | — | — |
| 3212 | BMS status | Overall battery management system status code. | R | — | — | u 16_raw | — | — |
| 3213 | BMS protect flags 2 | Protection bitmask word 2 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3214 | BMS warning flags 2 | Warning bitmask word 2 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3215 | BMS SOC | State of charge reported directly by the BMS. | R | — % | — | u 16_percent | — | — |
| 3216 | BMS battery voltage | Pack voltage reported by the BMS (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | — | — |
| 3217 | BMS battery current | Current reported by the BMS with 0.01 A resolution (positive = discharge). | R | — A | — | s 16_current_centiamp; Positive values indicate discharge from the battery; negative values indicate charging. | — | — |
| 3218 | BMS max cell temperature | Maximum cell temperature observed across the battery pack (0.1 °C resolution). | R | — °C | — | s 16_temperature_decic | — | — |
| 3219 | BMS max charge current | Maximum charge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | — | — |
| 3220 | BMS max discharge current | Maximum discharge current allowed by the BMS (0.01 A resolution). | R | — A | — | u 16_current_centiamp | — | — |
| 3221 | BMS cycle count | Total charge/discharge cycles counted by the BMS. | R | — | — | u 16_raw | — | — |
| 3222 | BMS state of health | Battery state of health reported by the BMS. | R | — % | — | u 16_percent | — | — |
| 3223 | BMS charge voltage limit | Maximum pack voltage permitted during charge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | — | — |
| 3224 | BMS discharge voltage limit | Minimum pack voltage permitted during discharge (0.01 V resolution). | R | — V | — | u 16_voltage_centivolt | — | — |
| 3225 | BMS warning flags 3 | Warning bitmask word 3 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3226 | BMS protect flags 3 | Protection bitmask word 3 from the battery management system. | R | — | — | u 16_raw | — | — |
| 3230 | BMS max cell voltage | Highest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | — | — |
| 3231 | BMS min cell voltage | Lowest individual cell voltage (0.001 V resolution). | R | — V | — | u 16_voltage_millivolt | — | — |

