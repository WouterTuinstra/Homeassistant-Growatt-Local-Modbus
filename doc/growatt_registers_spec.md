# Growatt Modbus Register Map (Protocol v1.24)

This file is generated from `growatt_registers_spec.json` (parsed from the official Modbus RTU protocol) and cross-references the Home Assistant `growatt_local` integration.

**Legend**: Access = spec write flag (`R`, `W`, `R/W`). “Range/Unit” merges the spec range column with the unit, when available. “Attributes” lists the integration attribute(s) mapped to the register; “Sensors” lists Home Assistant sensor entities exposing the attribute. Rows without attributes are not currently surfaced by the integration (typically configuration or reserved registers).

*Descriptions and notes are copied verbatim from the PDF specification. Some spacing may appear collapsed due to automated extraction; consult the original document when exact phrasing is required.*

## Coverage Summary
| Section | Spec Registers | Covered | Missing |
| --- | --- | --- | --- |
| Common Holding Registers (0–124) | 100 | 8 | 92 |
| TL-X/TL-XH Holding Registers (3000–3124) | 109 | 0 | 109 |
| TL-XH US Holding Registers (3125–3249) | 64 | 0 | 64 |
| TL3/MAX/MID/MAC Holding Registers (125–249) | 80 | 0 | 80 |
| Storage Holding Registers (1000–1124) | 99 | 0 | 99 |
| Storage Holding Registers (1125–1249) | 15 | 0 | 15 |
| Common Input Registers (0–124) | 100 | 80 | 20 |
| TL-X/TL-XH Input Registers (3000–3124) | 0 | 0 | 0 |
| TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249) | 0 | 0 | 0 |
| TL-X/TL-XH Extended Input Registers (3250–3374) | 0 | 0 | 0 |
| Storage Input Registers (1000–1124) | 0 | 0 | 0 |
| Storage Input Registers (1125–1249) | 0 | 0 | 0 |
| Storage Input Registers (2000–2124) | 0 | 0 | 0 |
| Storage TL-XH Input Registers (3041–3231) | 0 | 0 | 0 |
| Offgrid SPF Input Registers | 100 | 41 | 59 |

## Common Holding Registers (0–124)
Applies to TL-X/TL-XH, TL3/MAX/MID/MAC, and MIX/SPA/SPH storage families.

**Applies to:** TL-X/TL-XH/TL-XH US, TL3-X/MAX/MID/MAC, Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Inverter and BDC enable | Bitfield controlling remote enable of the inverter (bit 0) and the battery DC converter or BDC ready mode (bit 1). Write the combined value 0-3; 1 turns on the inverter, 2 turns on only the BDC, 3 turns on both. | W | — | 1 | Home Assistant preserves other control bits when toggling this value. | tlx:inverter_enabled, tl3:inverter_enabled | — |
| 1 | Safety function enable flags | Bit mask that enables regional grid-protection functions. Set a bit to 1 to enable the corresponding feature (SPI, LVFRT, DRMS, Volt-Var, ROCOF, recovery, split-phase). | W | — | — | Bits 0-3 cover CEI 0-21 compliance; bits 4-6 cover AS/NZS/SAA requirements; bits 11-15 are reserved. | — | — |
| 2 | Persist power-factor commands | Choose whether the power-factor and derating commands in registers 3, 4, 5, and 99 are stored to NVRAM (1) or revert to defaults after the next restart (0). | W | — | 0 | — | — | — |
| 3 | Active power limit setpoint | Maximum active power output as a percentage of rated power. Values 0-100 cap the output; 255 removes the limit. | W | — % | 255 | — | — | — |
| 4 | Reactive power limit setpoint | Maximum reactive power magnitude as a percent of rated capacity. Negative values request capacitive (leading) support, positive values inductive (lagging). 255 removes the limit. | W | — % | 255 | — | — | — |
| 5 | Power factor target | Requested power factor multiplied by 10,000 (e.g. 9900 equals 0.99). Values below 10,000 lead (capacitive); values above 10,000 lag (inductive). | W | — | 0 | — | — | — |
| 6 | Rated apparent power | Apparent power capability encoded as an unsigned 32-bit value with 0.1 VA resolution (register 6 is the high word, register 7 the low word). | R | — VA | — | — | — | — |
| 8 | Nominal PV voltage | Target PV input voltage for maximum power point tracking, stored in 0.1 V increments. | R | — V | — | — | — | — |
| 9 | Firmware identification string | Six registers containing ASCII characters that describe the running firmware. Registers 9-11 hold the DSP identifier; registers 12-14 hold the control-board identifier. Home Assistant reads the combined 12-character string for the reported firmware version. | R | — ASCII | — | — | tlx:firmware, tl3:firmware, storage:firmware | — |
| 15 | LCD language selection | Language index used by the local LCD interface: 0=Italian, 1=English, 2=German, 3=Spanish, 4=French, 5=Chinese, 6=Polish, 7=Portuguese, 8=Hungarian. | W | — | — | — | — | — |
| 16 | Country profile configured | Indicates whether a regional grid profile has been selected (1) or still needs to be chosen (0). | W | — | — | — | — | — |
| 17 | PV start voltage threshold | Minimum DC input voltage required before the inverter starts, stored in 0.1 V increments. | W | — V | — | — | — | — |
| 18 | Start-up delay | Delay between meeting the PV start voltage and enabling the inverter output, measured in seconds. | W | — s | — | — | — | — |
| 19 | Restart delay | Time to wait after a fault clears before restarting the inverter, in seconds. | W | — s | — | — | — | — |
| 20 | Active power ramp rate (startup) | Slope for increasing active power after startup in 0.1% increments per second (1-1000). | W | — %/s | — | — | — | — |
| 21 | Active power ramp rate (restart) | Slope for returning to full power after curtailment or a cleared fault, expressed in 0.1% per second. | W | — %/s | — | — | — | — |
| 22 | Modbus RTU baud rate | Selects the RS-485 serial line baud rate: 0=9600 bps, 1=38400 bps. | W | — | 0 | — | — | — |
| 23 | Inverter serial number | ASCII-encoded 10-character serial number spanning registers 23-27. | R | — ASCII | — | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | tlx:serial number, tl3:serial number | — |
| 28 | Inverter module code | 32-bit hardware option mask encoded as eight nibbles (A, B, D, T, P, U, M, S). Register 28 holds the high word and register 29 the low word. | R | — | — | Home Assistant renders this value as the string A# B# D# T# P# U# M# S# via the integration's model() helper. | tlx:Inverter model, tl3:Inverter model, storage:Inverter model | — |
| 30 | Modbus slave address | RS-485/Modbus RTU slave ID. Set a value between 1 and 254; 0 is reserved for broadcast frames. | W | — | — | — | — | — |
| 31 | Firmware update trigger | Write 1 to arm the serial firmware update procedure. The inverter clears the flag after the bootloader handshake starts. | W | — | — | — | — | — |
| 32 | Reset user configuration | Writing 1 clears user-configurable settings such as communication parameters and regional profiles. | W | — | — | Use with caution; the inverter immediately reboots and loses provisioning data. | — | — |
| 33 | Factory reset | Writing 1 restores full factory defaults and restarts the inverter. | W | — | — | Equivalent to the front-panel factory reset. Requires re-commissioning afterwards. | — | — |
| 34 | Manufacturer information string | Sixteen ASCII characters written at production time (batch, plant, or custom identifiers). | R | — ASCII | — | The original table lists these words as Manufacturer Info 8–1 (high/middle/low); combine them to read the full string. | — | — |
| 42 | G 100 failsafe enable | Enable (1) or disable (0) the UK G 98/G 100 failsafe watchdog. | W | — | — | Leave off unless the interconnection agreement requires the G 100 failsafe mode. | — | — |
| 43 | Device type code | Encodes the inverter family and tracker count. See data type for supported values. | R | — | — | — | tlx:device type code, tl3:device type code, storage:device type code | — |
| 44 | MPPT trackers and grid phases | High byte holds the number of PV trackers; low byte holds the number of output phases. | R | — | — | — | tlx:number of trackers and phases, tl3:number of trackers and phases, storage:number of trackers and phases | — |
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
| 73 | Stage 1 overfrequency trip delay | Cycles grid frequency must stay above the stage 1 overfrequency limit (register 55) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | tl3:modbus version | — |
| 74 | Stage 2 underfrequency trip delay | Cycles grid frequency must stay below the stage 2 underfrequency limit (register 58) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 75 | Stage 2 overfrequency trip delay | Cycles grid frequency must stay above the stage 2 overfrequency limit (register 59) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 76 | Stage 3 undervoltage trip delay | Cycles grid voltage must stay below the stage 3 undervoltage limit (register 60) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 77 | Stage 3 overvoltage trip delay | Cycles grid voltage must stay above the stage 3 overvoltage limit (register 61) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 78 | Stage 3 underfrequency trip delay | Cycles grid frequency must stay below the stage 3 underfrequency limit (register 62) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 79 | Stage 3 overfrequency trip delay | Cycles grid frequency must stay above the stage 3 overfrequency limit (register 63) before tripping. One AC cycle is 20 ms at 50 Hz (16.7 ms at 60 Hz). | W | — cycles | — | — | — | — |
| 80 | Ten-minute overvoltage limit | Maximum RMS grid voltage averaged over 10 minutes (0.1 V increments) before the inverter trips. | W | — V | — | — | — | — |
| 81 | PV input high-voltage fault | PV array voltage threshold that triggers a DC over-voltage fault (0.1 V increments). | W | — V | — | — | — | — |
| 82 | Controller firmware build string | Twelve ASCII characters summarising model and controller build revisions (model letters, DSP 1, DSP 2/M 0, CPLD/AFCI, M 3). | R | — ASCII | — | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP 1 build, 6-7 DSP 2/M 0 build, 8-9 CPLD/AFCI build, 10-11 M 3 build. | — | — |
| 88 | Modbus protocol version | Modbus register map revision encoded as an integer (e.g. 207 equals version 2.07). | R | — | — | — | tlx:modbus version, storage:modbus version | — |
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
| 3000 | Export Limit Fa T iled Power Rat ex e | he power rate when port Limit failed | — | — | — | The power rate when export Limit failed | — | — |
| 3001 | Serial Number | Serial number 1-2 | — | — | — | The new model uses the following | — | — |
| 3002 | New Serial NO | Serial number 3-4 | — | — | — | registers to record the serial number; The | — | — |
| 3003 | New Serial NO | Serial number 5-6 | — | — | — | representation is the same as the | — | — |
| 3004 | New Serial NO | Serial number 7-8 | — | — | — | original: one register holds two | — | — |
| 3005 | New Serial NO | Serial number 9-10 | — | — | — | characters and the new serial number | — | — |
| 3006 | New Serial NO | Serial number 11-12 | — | — | — | is 30 characters. | — | — |
| 3007 | New Serial NO | Serial number 13-14 | — | — | — | — | — | — |
| 3008 | New Serial NO | Serial number 15-16 | — | — | — | — | — | — |
| 3009 | New Serial NO | Serial number 17-18 | — | — | SCII | — | — | — |
| 3010 | New Serial NO | Serial number 19-20 | — | — | SCII | — | — | — |
| 3011 | New Serial NO | Serial number 21-22 | — | — | SCII | — | — | — |
| 3012 | New Serial NO | Serial number 23-24 | — | — | SCII | — | — | — |
| 3013 | New Serial NO | Serial number 25-26 | — | — | SCII | — | — | — |
| 3014 | New Serial NO | Serial number 27-28 | — | — | SCII | — | — | — |
| 3015 | New Serial NO | Serial number 29-30 | — | — | SCII | — | — | — |
| 3016 | Dry Contact Fu Dr nc En | R y Contact function enable | /W 0: 1: | — | — | Dry Contact function enable | — | — |
| 3017 | Dry Contact On Th Rate dr | e power rate ycontact turn on | of R | — | .1% | The power rate of drycontact turn on | — | — |
| 3018 | b Work Mode | Work Mode----0:default,1: System Retrofit 2: Multi-Parallel | — | — | — | MIN 2.5~6 KTL-XH/ XA Double CT special | — | — |
| 3019 | Dry Contact Of f Rate | Dry Contact Off Rate | — | — | ~100 0 | 0.1% Dry contact closure power pe rcentage | — | — |
| 3020 | Box Ctrl Inv Ord B er | ox Ctrl Inv Order | — | — | — | — | — | — |
| 3021 | Exter Comm Of Ext f Grid En set ena | ernal communication R/W ting manual off-network ble | — | — | — | 0 x 00: Disable; (default) 0 x 01: Enable; | — | — |
| 3022 | uw Bdc Stop W Bdc S ork Of Bus Volt | top Work Of Bus Volt | — | — | — | — | — | — |
| 3023 | b Grid Type | Grid Type---0:Single Phase 1:Three Phase 2:Split Phase | — | — | — | MIN 2.5~6 KTL-XH/ XA Double CT special | — | — |
| 3024 | Float charge current limit | When charge current battery need is lower th this value, enter into f charge | an loat | — | .1 A 60 | 0 CC current | — | — |
| 3025 | Vbat Warning "Ba set | ttery-low" warning up voltage | — | — | Le LV | ad acid battery voltage | — | — |
| 3026 | Vbatlow Warn "Ba Clr cle | ttery-low" warning ar voltage | — | — | Cl vo vo Lo le 45 20 48 <= 49 50 | ear battery low ltage error ltage point ad Percent(only ad-Acid): .5 V(Load < %); .0 V(20%<=Load 50%); .0 V(Load > %); | — | — |
| 3027 | Vbatstopfordi B scharge | attery cut off voltage | — | — | Sh di lo vo le 46 20 44 <= 44 50 | ould stop scharge when wer than this ltage(only ad-Acid): .0 V(Load < %); .8 V(20%<=Load 50%); .2 V(Load > %); | — | — |
| 3028 | Vbat stop for B charge | attery over charge voltage | R/W | — | Sh ch hi vo | ould stop arge when gher than this ltage | — | — |
| 3029 | Vbat start for discharge | Battery start discharge voltage | — | — | Sh di lo vo | ould not scharge when wer than this ltage | — | — |
| 3030 | Vbat constant B charge v | attery constant charge oltage | — | — | CV ca lo vo | voltage(acid) n charge when wer than this ltage | — | — |
| 3031 | Battemp B lower limit d l | attery temperature lower imit for discharge | — | — | 0-2 100 -40 | 00:0-20℃ 0-1400: -0℃ | — | — |
| 3032 | Bat temp B upper limit d l | attery temperature upper imit for discharge | — | — | — | — | — | — |
| 3033 | Bat temp lower limit c | Battery temperature lowe limit for charge | R | — | Bat tem lim 0-2 100 -40 | tery perature lower it 00:0-20℃ 0-1400: -0℃ | — | — |
| 3034 | Bat temp B upper limit c l | attery temperature upper imit for charge | — | — | Bat tem upp | tery perature er limit | — | — |
| 3035 | uw Under Fre D Und ischarge Dely T ime | er Fre Delay Time | — | — | Und Tim | er Fre Delay e | — | — |
| 3036 | Grid First Disch arge Power Rat wh e | Discharge Power Rate en Grid First | — | — | — | — | — | — |
| 3037 | Grid First Stop S OC | Stop Discharge soc when Grid First | — | — | — | — | — | — |
| 3038 | Time 1(xh) | Period 1: [Start Time ~ Time], [Charge/Discharge [Disable/Enable] 3038 enable, charge and discharge, start time, time 3039 | End ], end | — | Bit Bit Bit 0: 1: 2: Bit 0: ena | 0~7: minutes; 8~12: hour; 13~14, load priority; battery priority; Grid priority; 15, prohibited; 1: bled; | — | — |
| 3039 | — | — | — | — | Bit Bit Bit | 0~7: minutes; 8~12: hour; 13~15: reserved | — | — |
| 3040 | Time 2(xh) | Time period 2: [start ti end time], [charge / discharge], [disable enable] 3040 enable, charge and discharge, start time, 3 end time | me ~ / 041 | — | Bit Bit Bit 0: 1: 2: Bit 0: led; | 0~7: minutes; 8~12: hour; 13~14, load priority; battery priority; Grid priority; 15, prohibited; 1: | — | — |
| 3041 | — | — | R/W | — | ~7: mi ~12: h 3~15: | nutes; our; reserved | — | — |
| 3042 | Time 3(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3043 | — | — | R/W | — | Time 1 | — | — | — |
| 3044 | Time 4(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3045 | — | — | R/W | — | Time 1 | — | — | — |
| 3046 | 预留 | — | — | — | — | — | — | — |
| 3047 | Bat First Power C Rate B | harge Power Rate when at First | — | — | — | — | — | — |
| 3048 | w Bat First stop SOC | Stop Charge soc when Bat First | — | — | — | — | — | — |
| 3049 | AC Charge Enabled | harge Enable | — | — | le:1 ble:0 | — | — | — |
| 3050 | Time 5(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3051 | — | — | R/W | — | Time 1 | — | — | — |
| 3052 | Time 6(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3053 | — | — | R/W | — | Time 1 | — | — | — |
| 3054 | Time 7(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3055 | — | — | R/W | — | Time 1 | — | — | — |
| 3056 | Time 8(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3057 | — | — | R/W | — | Time 1 | — | — | — |
| 3058 | Time 9(xh) | With Time 1 | R/W | — | Time 1 | — | — | — |
| 3059 | — | — | R/W | — | Time 1 | — | — | — |
| 3060 | Reserved | — | — | — | — | — | — | — |
| 3069 | — | — | — | — | — | — | — | — |
| 3070 | Battery Type | Battery type choose of buck-boost input | R/W | — | B 0 1 2 | attery type:Lithium:Lead-acid:other | — | — |
| 3071 | Bat Mdl Seria/ Ba Paral Num | t Mdl Seria/Paral Num | R/W | — | B N S T i n s T i n s | at Mdl Seria/Paral um; PH 4-11 K used he upper 8 bits ndicate the umber of series egments; he lower 8 bits ndicate the umber of parallel ections; | — | — |
| 3072 | Reserved | — | — | — | — | — | — | — |
| 3073 | Reserved | — | — | — | — | — | — | — |
| 3074 | Reserved | — | — | — | — | — | — | — |
| 3075 | Reserved | — | — | — | — | — | — | — |
| 3076 | Reserved | — | — | — | — | — | — | — |
| 3077 | Reserved | — | — | — | — | — | — | — |
| 3078 | Reserved | — | — | — | — | — | — | — |
| 3079 | Ups Fun En | Ups function enable or disable | R/W | — | 0 1 | :disable:enable | — | — |
| 3080 | UPSVolt Set | UPS output voltage | R/W | — | 0 1 2 | :230 V:208 V:240 V | — | — |
| 3081 | UPSFreq Set | UPS output frequency | R/W | — | 0 1 | :50 Hz:60 Hz | — | — |
| 3082 | b Load First Sto S p Soc Set | top Soc When Load First | R/W | — | r | atio | — | — |
| 3083 | Reserved | — | — | — | — | — | — | — |
| 3084 | Reserved | — | — | — | — | — | — | — |
| 3085 | Com Address Com | munication addr | R/W | — | 1 a 1 C a | : Communication ddr=1 ~ 254: ommunication ddr=1~254 | — | — |
| 3086 | Baud Rate | Communication Baud Rate | R/W | — | 0 1 | : 9600 bps: 38400 bps | — | — |
| 3087 | Serial NO. 1 | Serial Number 1-2 | R/W | — | F | or battery | — | — |
| 3088 | Serial NO. 2 | Serial Number 3-4 | — | — | — | — | — | — |
| 3089 | Serial NO. 3 | Serial Number 5-6 | — | — | — | — | — | — |
| 3090 | Serial NO. 4 | Serial Number 7-8 | — | — | — | — | — | — |
| 3091 | Serial No. 5 | Serial Number 9-10 | — | — | — | — | — | — |
| 3092 | Serial No.6 | Serial Number 11-12 | — | — | — | — | — | — |
| 3093 | Serial No. 7 | Serial Number 13-14 | — | — | — | — | — | — |
| 3094 | Serial No. 8 | Serial Number 15-16 | — | — | — | — | — | — |
| 3095 | Bdc Reset Cmd BDC | Reset command | — | — | — | 0:Invalid data 1:Reset setting parameters 2:Reset correction parameter 3:Clear historical power | — | — |
| 3096 | ARKM 3 Code BDCM | onitoring software | — | — | — | ZEBA | — | — |
| 3097 | code | — | — | — | — | — | — | — |
| 3098 | DTC | DTC | — | — | — | — | — | — |
| 3099 | FW Code | DSP software code | — | — | — | — | — | — |
| 3100 | — | — | — | — | — | — | — | — |
| 3101 | Processor 1 FW Vision | DSP Software Version | — | — | — | — | — | — |
| 3102 | Bus Volt Ref | Minimum BUS voltage for charging and discharging batteries | — | — | — | — | — | — |
| 3103 | ARKM 3 Ver BMS_MCUVer BMS | BDC monitoring software version hardware ver | sion | — | — | — | — | — |
| 3104 | sion info BMS_FW | rmation BMS software version | R | — | — | — | — | — |
| 3105 | BMS_Info | information BMS Manufacturer Name | R | — | — | — | — | — |
| 3106 | BMSComm Ty BMSCo pe | mm Type | R | — | — | BMSCommunicati on interface type: | — | — |
| 3107 | — | — | — | — | — | 0: RS 485; 1: CAN; | — | — |
| 3108 | Module 4 | BDCmodel (4) | — | — | — | Sxx Bxx | — | — |
| 3109 | Module 3 | BDCmodel (3) | — | — | — | Dxx Txx | — | — |
| 3110 | Module 2 | BDCmodel (2) | — | — | — | Pxx Uxx | — | — |
| 3111 | Module 1 | BDCmodel (1) | — | — | — | Mxxxx | — | — |
| 3112 | Reserved | — | — | — | — | — | — | — |
| 3113 | un Protocol Ve BD r | CProtocol Ver | — | — | — | Bit 8-bit 15 The major version number ranges from 0-256. In principle, it cannot be changed Bit 0-bit 7 Minor version number [0-256]. If the protocol is changed, you need to update this version No. | — | — |
| 3114 | uw Certificatio n Ver | BDC Certification Ver | — | — | — | — | — | — |
| 3115 | Reserved | — | — | — | — | — | — | — |
| 3124 | — | — | — | — | — | — | — | — |

## TL-XH US Holding Registers (3125–3249)
US-specific time schedule and dry-contact configuration registers.

**Applies to:** TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3125 | Time Month 1 Use,Ad | with Time 1-9(us) d month time | R | — | — | bit 0~3:month_L; bit 4~7: month_H bit 8, 0:disable 1:enable Bit 9~15:reserve | — | — |
| 3126 | Time Month 2 Use,Ad | with Time 10-18(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3127 | Time Month 3 Use,Ad | with Time 19-27(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3128 | Time Month 4 Use,Ad | with Time 28-36(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3129 | Time 1(us) | time 1:[starttime~endtime | ] cu [d e | — | :batfi:gridf: anti it 15,:disab:enabl | bit 0~6:min; bit 7~11:hour; bit 12~14, 0:loadfirst; rst; irst; -reflux le; e; | — | — |
| 3130 | — | R/W | — | — | it 0~6: it 7~11 it 12-1:Weekd:Weeke:Wee K it 14~1 | min;:hour; 3, ay nd 5:reserve | — | — |
| 3131 | Time 2(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3133 | Time 3(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3135 | Time 4(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3137 | Time 5(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3139 | Time 6(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3141 | Time 7(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3143 | Time 8(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3145 | Time 9(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3147 | Time 10(us)Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3149 | Time 11(us)Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3151 | Time 12(us)Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3153 | Time 13(us)Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3155 | Time 14(us)Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3157 | Time 15(us) Same as | above R/W | — | — | ame as | Time 1 | — | — |
| 3159 | Time 16(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3161 | Time 17(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3163 | Time 18(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3165 | Time 19(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3167 | Time 20(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3169 | Time 21(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3171 | Time 22(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3173 | Time 23(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3175 | Time 24(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3177 | Time 25(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3179 | Time 26(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3181 | Time 27(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3183 | Time 28(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3185 | Time 29(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3187 | Time 30(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3189 | Time 31(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3191 | Time 32(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3193 | Time 33(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3195 | Time 34(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3197 | Time 35(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3199 | Time 36(us)Same as | above R/W | — | — | s Time | 1 | — | — |
| 3201 | Special Day 1 | Special Day 1(month,Day)R/ | W | — | :day; 4:mont ble 1: | h | — | — |
| 3202 | Special Day 1_ Time 1 | Start time R/W | — | — | :min; 1:hour 14, first; irst; first; i-refl able; ble; | ; ux | — | — |
| 3203 | — | endtime R/W | — | — | :min; 1:hour 15:res | ; erve | — | — |
| 3204 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3206 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3208 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3210 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3212 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3214 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3216 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3218 | Special Day 1_ Same | as above R/W | — | — | s | — | — | — |
| 3220 | Special Day 2 | Special Day 2(month,Day)R/ | W | — | :day; 4:mont ble le | h | — | — |
| 3221 | Special Day 2_ Time 1 | Start time R/W | — | — | : min; 1: hou 14, dfirst first; dfirst i-refl able; ble; | r;;; ux | — | — |
| 3222 | — | endtime R/W | — | — | : min; 1: hou 15:res | r; erve | — | — |
| 3223 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3225 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3227 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3229 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3231 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3233 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3235 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3237 | Special Day 2_ Same | as above R/W | — | — | s | — | — | — |
| 3239 | Reserve | Reserve | — | — | — | — | — | — |

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
| 240 | Commissioning step index | Internal step counter used during factory self-check sequences. Installers should leave this value unchanged. | W | — | — | — | — | — |
| 241 | Installer longitude word | Longitude component recorded for remote diagnostics. Scaling is vendor-defined and not used by Home Assistant. | W | — | — | — | — | — |
| 242 | Installer latitude word | Latitude component recorded for remote diagnostics. Scaling is vendor-defined and not used by Home Assistant. | W | — | — | — | — | — |
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
| 1000 | Float W charge b current t limit i | hen charge current W attery need is lower han this value, enter nto float charge | — | — | CC cur | rent | — | — |
| 1001 | PF CMD Set t memory CMD w state ornot setti value | he following 19-22 W ill be memory (1/0), if not, these ngs are the initial . | 0 | — | Means acting power | these settings will be or not when next on(02 repeat) | — | — |
| 1002 | Vbat Start F LV V or Discharg e | bat R/ | W | — | Lead-a | cid battery LV voltage | — | — |
| 1003 | Vbatlow Wa Load P rn Clr lead- 45.5 V <20% 48.0 V 20%~5 49.0 V >50 | ercent(only W Acid): 0% | — | — | Clear voltag | battery low voltage error e point | — | — |
| 1004 | Vbatstopfo Shou rdischarge when v 4 < 4 2 4 > | ld stop discharge W lower than this oltage(only lead-Acid): 6.0 V 20% 4.8 V 0%~50% 4.2 V 50% | — | — | — | — | — | — |
| 1005 | Vbat stop Shoul for charge when volt | d stop charge higher than this age | W | — | — | — | — | — |
| 1006 | Vbat start Shou for when discharge volta | ld not discharge W lower than this ge | — | — | — | — | — | — |
| 1007 | Vbat c constant t charge | an charge when lower W han this voltage | — | — | CV vol | tage(acid) | — | — |
| 1008 | EESys Info.S Bit ys Set En Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit | 0:Resved; W 1:Resved; 2:Resved; 3:Resved; 4:Resved; 5:b Discharge En; 6:Force Dischr En; 7:Charge En; 8:b Force Chr En; 9:b Back Up En; 10:b Inv Limit Load E; 11:b Sp Limit Load En; 12:b ACCharge En; 13:b PVLoad Limit En; 14,15:Un Used; | — | — | Syst | em Enable | — | — |
| 1009 | Battemp Bat lower limit low d | tery temperature W er limit for discharge | 0 0 1 0 | — | — | — | — | — |
| 1010 | Bat temp Batter upper limit upp d | y temperature W er limit for discharge | 2 | — | — | — | — | — |
| 1011 | Bat temp Batter lower limit low c | y temperature er limit for charge | W 0 0 1 0 | — | Lowe | r temperature limit | — | — |
| 1012 | Bat temp Batter upper limit upp c | y temperature W er limit for charge | 2 | — | per te | mperature limit | — | — |
| 1013 | uw Under Fr Under e Discharge Dely Time | Fre Delay Time | s 0 | — | der Fr | e Delay Time | — | — |
| 1014 | Bat Mdl Seri Batt al Num | ery serial number W | 0 | — | H 4-11 K | used | — | — |
| 1015 | Bat Mdl Para Batt ll Num | ery parallel section W | 0 | — | H 4-11 K | used | — | — |
| 1016 | DRMS_EN / | / | / | — | disabl | e 1:enable | — | — |
| 1017 | Bat First Hi Start Time Low 4 | gh eight:hours eight: minutes | 0 0 | — | — | — | — | — |
| 1018 | Bat First Hig Stop Time Low e 4 | h eight:hours ight: minutes | 0 0 | — | — | — | — | — |
| 1019 | Bat First E on/off D Switch 4 | nable:1 isable:0 | 0 | — | ttery | priority enable 1 | — | — |
| 1020 | Bat First Hi Start Time Low 5 | gh eight:hours eight: minutes | 0 0 | — | — | — | — | — |
| 1021 | Bat First High Stop Time Low e 5 | eight:hours ight: minutes | 0 0 | — | — | — | — | — |
| 1022 | Bat First E on/off D Switch 5 | nable:1 isable:0 | 0 | — | ttery | priority enable 1 | — | — |
| 1023 | Bat First High Start Time Low 6 | eight:hours eight: minutes | 0 0 | — | — | — | — | — |
| 1024 | Bat First High Stop Time Low e 6 | eight:hours ight: minutes | 0 0 | — | — | — | — | — |
| 1025 | Bat First E on/off D Switch 6 | nable:1 isable:0 | 0 | — | ttery | priority enable 1 | — | — |
| 1026 | Grid First High Start Time Low 4 | eight:hours eight: minutes | 0 0 | — | — | — | — | — |
| 1027 | Grid First High Stop Time Low e 4 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1028 | Grid First Enab Stop Disa Switch 4 | le:1 ble:0 | 0 or | — | priori | ty enable | — | — |
| 1029 | Grid First High Start Time Low 5 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1030 | Grid First High Stop Time Low e 5 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1031 | Grid First Enab Stop Disa Switch 5 | le:1 ble:0 | 0 or | — | priori | ty enable | — | — |
| 1032 | Grid First High Start Time Low 6 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1033 | Grid First High Stop Time Low e 6 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1034 | Grid First Enab Stop Disa Switch 6 | le:1 ble:0 | 0 or | — | priori | ty enable | — | — |
| 1035 | Bat First High Start Time Low 4 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1036 | / / | / | / | — | ve | — | — | — |
| 1037 | U b CTMode C C | se the CTMode to W hoose RFCT \ Cable T\METER | 2:ME 1:cW ssCT 0:cW T | — | — | — | — | — |
| 1038 | CTAdjust C | TAdjust enable W | 0:di 1:en | — | — | — | — | — |
| 1039 | / / | / | / | — | ve | — | — | — |
| 1040 | / / | / | / | — | eserve | — | — | — |
| 1041 | / / | / | / | — | eserve | — | — | — |
| 1042 | / / | / | / | — | eserve | — | — | — |
| 1043 | / / | / | / | — | eserve | — | — | — |
| 1044 | Priority F E L f | orce Chr En/Force Dischr R n oad first/bat first /grid irst | 0.L fau att rid | — | Force C /dis | hr En/disb Force Dischr E | — | — |
| 1045 | / / | / | / | — | eserve | — | — | — |
| 1046 | / / | / | / | — | eserve | — | — | — |
| 1047 | Aging Test St Com ep Cmd | mand for aging test | 0: 1: 2: dis | — | md for | aging test | — | — |
| 1048 | Battery Typ Batt e buck | ery type choose of -boost input | 0:L 1:L d 2:o | — | attery | type | — | — |
| 1049 | / / | / | / | — | eserve | — | — | — |
| 1050 | / / | / | / | — | eserve | — | — | — |
| 1051 | / / | / | / | — | eserve | — | — | — |
| 1052 | / / | / | / | — | eserve | — | — | — |
| 1053 | / / | / | / | — | eserve | — | — | — |
| 1054 | / / | / | / | — | eserve | — | — | — |
| 1060 | Buck Ups Fun E Ups n dis | function enable or able | — | — | — | — | — | — |
| 1061 | Buck UPSVolt S UP et | S output voltage | — | — | — | — | — | — |
| 1062 | UPSFreq Set | UPS output frequency | — | — | — | — | — | — |
| 1070 | Grid First Disch arge Power Rat wh e | Discharge Power R en Grid First | ate W | — | charge r Rate Grid First | — | — | — |
| 1071 | Grid First Stop S OC | Stop Discharge soc when W Grid First | — | — | top harge when First | — | — | — |
| 1072 | / | / | / | — | — | reverse | — | — |
| 1079 | — | — | — | — | — | — | — | — |
| 1080 | Grid First Start Time 1 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1081 | Grid First Stop Time 1 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1082 | Grid First Stop Switch 1 | Enable:1 Disable:0 | — | — | First le | — | — | — |
| 1083 | Grid First Start Time 2 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1084 | Grid First Stop Time 2 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1085 | Grid First Stop Switch 2 | Force Discharge.b Switch&L CD_SET_FORCE_TRUE_2)= =LCD_SET_FORCE_TRUE_2 | — | — | First le | Force Discharge; LCD_SET_FORCE_T RUE_2 | — | — |
| 1086 | Grid First Start Time 3 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1087 | Grid First Stop Time 3 | High eight bit:hour Low eight bit:minute | — | — | — | — | — | — |
| 1088 | Grid First Stop Switch 3 | Enable:1 Disable:0 | — | — | First le | — | — | — |
| 1089 | / | / | / | — | — | reserve | — | — |
| 1090 | Bat First Power C Rate B | harge Power Rate when W at First | 0- | — | ge Rate Bat st | — | — | — |
| 1091 | w Bat First stop SOC | Stop Charge soc when Bat W First | 0- | — | p soc Bat st | — | — | — |
| 1092 | AC charge W Switch E D | hen Bat First nable:1 isable:0 | En Di | — | rge e | — | — | — |
| 1093 | — | — | — | — | — | — | — | — |
| 1099 | — | — | — | — | — | — | — | — |
| 1100 | Bat First Start Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1101 | Bat First Stop Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1102 | Bat First on/off Switch 1 | Enable:1 Disable:0 | 0 | — | First 1 | — | — | — |
| 1103 | Bat First Start Time 2 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1104 | Bat First Stop Time 2 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1105 | Bat Firston/off Switch 2 | Enable:1 Disable:0 | 0 | — | First 2 | — | — | — |
| 1106 | Bat First Start Time 3 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1107 | Bat First Stop Time 3 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | — | — | — |
| 1108 | Bat Firston/off Switch 3 | Enable:1 Disable:0 | 0 | — | First 3 | — | — | — |
| 1109 | / | / / | / | — | — | reserve | — | — |
| 1110 | Load First Start Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | SPA/ reserve | — | — |
| 1111 | Load First Stop Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | — | — | SPA/ reserve | — | — |
| 1112 | Load First Switch 1 | Enable:1 Disable:0 | 0 | — | irst S le | PA/ reserve | — | — |
| 1113 | Load First Start Time 2 | High eight bit:hour Low eight bit:minute | — | — | — | SPA/ reserve | — | — |
| 1114 | Load First Stop Time 2 | High eight bit:hour Low eight bit:minute | — | — | — | SPA/ reserve | — | — |
| 1115 | Load First Switch 2 | Enable:1 Disable:0 | — | — | d Firs ble | t SPA/ reserve | — | — |
| 1116 | Load First Start Time 3 | High eight bit:hour Low eight bit:minute | — | — | — | SPA/ reserve | — | — |
| 1117 | Load First Stop Time 3 | High eight bit:hour Low eight bit:minute | — | — | — | SPA/ reserve | — | — |
| 1118 | Load First Switch 3 | Enable:1 Disable:0 | — | — | d Firs ble | t SPA/ reserve | — | — |
| 1119 | New EPower C / alc Flag | — | / | — | — | 0:The old formula 1: The new formula | — | — |
| 1120 | Back Up En | Back Up Enable | — | — | — | MIX US | — | — |
| 1121 | SGIPEn | SGIP Enable | — | — | — | MIX US | — | — |

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
| 0 | Status code | Inverter run state | — | — | — | — | tlx:status_code, tl3:status_code, offgrid:status_code | Status code |
| 1 | Input 1 voltage | Input power (high) | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 2 | Input 2 voltage | Input power (low) | — | — | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3 | Input 1 Wattage | PV 1 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 4 | Input 1 Amperage | PV 1 input current | — | — | — | — | tlx:input_1_amperage, tl3:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 5 | Input 1 Wattage | PV 1 input power(high) | — | — | — | — | tlx:input_1_power, tl3:input_1_power, offgrid:input_2_power | Input 1 Wattage, Input 2 Wattage, PV1 charge power, PV2 charge power |
| 6 | Ppv 1 L | PV 1 input power(low) | — | — | — | — | — | — |
| 7 | Input 1 Amperage | PV 2 voltage | — | — | — | — | tlx:input_2_voltage, tl3:input_2_voltage, offgrid:input_1_amperage | Input 1 Amperage, Input 2 voltage, PV1 buck current, PV2 voltage |
| 8 | Input 2 Amperage | PV 2 input current | — | — | — | — | tlx:input_2_amperage, tl3:input_2_amperage, offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9 | Input 2 Wattage | PV 2 input power (high) | — | — | — | — | tlx:input_2_power, tl3:input_2_power, offgrid:output_active_power | Input 2 Wattage, Output active power, PV2 charge power |
| 10 | . Ppv 2 L | PV 2 input power (low) | — | — | — | — | — | — |
| 11 | Input 3 voltage | PV 3 voltage | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12 | Input 3 Amperage | PV 3 input current | — | — | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 13 | AC frequency | PV 3 input power (high) | — | — | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 14 | Output 1 voltage | PV 3 input power (low) | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 15 | Input 4 voltage | PV 4 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16 | Input 4 Amperage | PV 4 input current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17 | Battery voltage | PV 4 input power (high) | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 18 | Output 2 voltage | PV 4 input power (low) | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 19 | Bus voltage | PV 5 voltage | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20 | Grid voltage | PV 5 input current | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | AC frequency | PV 5 input power(high) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 22 | Output 1 voltage | PV 5 input power(low) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 23 | Input 6 voltage | PV 6 voltage | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24 | Input 6 Amperage | PV 6 input current | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 25 | Input 6 Wattage | PV 6 input power (high) | — | — | — | — | tlx:input_6_power, offgrid:inverter_temperature | Input 6 Wattage, Temperature |
| 26 | DC-DC temperature | PV 6 input power (low) | — | — | — | — | tl3:output_energy_today, offgrid:dc_dc_temperature | DC-DC temperature, Energy produced today |
| 27 | Input 7 voltage | PV 7 voltage | — | — | — | — | tlx:input_7_voltage, offgrid:load_percent | Input 7 voltage, Inverter load |
| 28 | Battery port voltage | PV 7 input current | — | — | — | — | tlx:input_7_amperage, tl3:output_energy_total, offgrid:battery_port_voltage | Battery port voltage, Input 7 Amperage, Total energy produced |
| 29 | Battery bus voltage | PV 7 input power (high) | — | — | — | — | tlx:input_7_power, offgrid:battery_bus_voltage | Battery bus voltage, Input 7 Wattage |
| 30 | Running hours | PV 7 input power (low) | — | — | — | — | tl3:operation_hours, offgrid:operation_hours | Running hours |
| 31 | Input 8 voltage | PV 8 voltage | — | — | — | — | tlx:input_8_voltage | Input 8 voltage |
| 32 | Input 8 Amperage | PV 8 input current | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 33 | Input 8 Wattage | PV 8 input power (high) | — | — | — | — | tlx:input_8_power | Input 8 Wattage |
| 34 | Output 1 Amperage | PV 8 input power (low) | — | — | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35 | Output power | Output power (high) | — | — | — | — | tlx:output_power | Output power |
| 36 | . Pac L | Output power (low) | — | — | — | — | — | — |
| 37 | AC frequency | Grid frequency | — | — | — | — | tlx:grid_frequency | AC frequency, Grid frequency |
| 38 | Output 1 voltage | Three/single phase grid voltage | — | — | — | — | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 39 | Output 1 Amperage | Three/single phase grid output | — | — | — | — | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 40 | Fault code | Three/single phase grid output VA (high) | — | — | — | — | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 41 | Intelligent Power Management temperature | Three/single phase grid output VA(low) | — | — | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 42 | Fault code | Three phase grid voltage | — | — | — | — | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 43 | N-bus voltage | Three phase grid output current | — | — | — | — | tlx:output_2_amperage, tl3:n_bus_voltage, offgrid:warning_code | N-bus voltage, Output 2 Amperage, Warning code |
| 44 | Output 2 Wattage | Three phase grid output power ( | — | — | — | — | tlx:output_2_power | Output 2 Wattage |
| 45 | . Pac 2 L | Three phase grid output power ( | — | — | — | — | — | — |
| 46 | Output 3 voltage | Three phase grid voltage | — | — | — | — | tlx:output_3_voltage | Output 3 voltage |
| 47 | Derating mode | Three phase grid output current | — | — | — | — | tlx:output_3_amperage, tl3:derating_mode, offgrid:constant_power | Derating mode, Output 3 Amperage |
| 48 | Input 1 energy today | Three phase grid output power ( | — | — | — | — | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 49 | . Pac 3 L | Three phase grid output power ( | — | — | — | — | — | — |
| 50 | Input 1 total energy | Three phase grid voltage | — | — ne voltage | — | — | tl3:input_1_energy_total, offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51 | . Vac_ST | Three phase grid voltage | — | — ne voltage | — | — | — | — |
| 52 | Input 2 energy today | Three phase grid voltage | — | — ne voltage | — | — | tl3:input_2_energy_today, offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53 | Energy produced today | Today generate energy (high) | — | — | — | — | tlx:output_energy_today | Energy produced today |
| 54 | Input 2 total energy | Today generate energy (low) | — | — | — | — | tl3:input_2_energy_total, offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55 | Total energy produced | Total generate energy (high) | — | — | — | — | tlx:output_energy_total | Total energy produced |
| 56 | Battery Charged (Today) | Total generate energy (low) | — | — | — | — | tl3:input_energy_total, offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today, Total energy input |
| 57 | Running hours | Work time total (high) | — | — | — | — | tlx:operation_hours | Running hours |
| 58 | Battery Charged (Total) | Work time total (low) | — | — | — | — | tl3:output_reactive_power, offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime, Reactive wattage |
| 59 | Input 1 energy today | PV 1 Energy today(high) | — | — | — | — | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 60 | Battery Discharged (Today) | PV 1 Energy today (low) | — | — | — | — | tl3:output_reactive_energy_today, offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61 | Input 1 total energy | PV 1 Energy total(high) | — | — | — | — | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 62 | Battery Discharged (Total) | PV 1 Energy total (low) | — | — | — | — | tl3:output_reactive_energy_total, offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63 | Input 2 energy today | PV 2 Energy today(high) | — | — | — | — | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 64 | AC Discharged Today | PV 2 Energy today (low) | — | — h | — | — | tl3:warning_code, offgrid:ac_discharge_energy_today | AC Discharged Today, Warning code |
| 65 | Input 2 total energy | PV 2 Energy total(high) | — | — h | — | — | tlx:input_2_energy_total, tl3:warning_value | Input 2 total energy, PV2 energy produced Lifetime |
| 66 | Grid Discharged Lifetime | PV 2 Energy total (low) | — | — h | — | — | tl3:real_output_power_percent, offgrid:ac_discharge_energy_total | Grid Discharged Lifetime, Real power output percentage |
| 67 | Input 3 energy today | PV 3 Energy today(high) | — | — h | — | — | tlx:input_3_energy_today | Input 3 energy today |
| 68 | AC charge battery current | PV 3 Energy today (low) | — | — h | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69 | Battery discharge power | PV 3 Energy total(high) | — | — h | — | — | tlx:input_3_energy_total, offgrid:discharge_power | Battery discharge power, Discharge Power, Input 3 total energy |
| 70 | . Epv 3_total L | PV 3 Energy total (low) | — | — h | — | — | — | — |
| 71 | Input 4 energy today | PV 4 Energy today(high) | — | — h | — | — | tlx:input_4_energy_today | Input 4 energy today |
| 72 | . Epv 4_today L | PV 4 Energy today (low) | — | — h | — | — | — | — |
| 73 | Battery discharge current | PV 4 Energy total(high) | — | — h | — | — | tlx:input_4_energy_total, offgrid:battery_discharge_amperage | Battery discharge current, Input 4 total energy |
| 74 | . Epv 4_total L | PV 4 Energy total (low) | — | — h | — | — | — | — |
| 75 | Input 5 energy today | PV 5 Energy today(high) | — | — h | — | — | tlx:input_5_energy_today | Input 5 energy today |
| 76 | . Epv 5_today L | PV 5 Energy today (low) | — | — h | — | — | — | — |
| 77 | Battery charging/ discharging(-ve) | PV 5 Energy total(high) | — | — h | — | — | tlx:input_5_energy_total, offgrid:battery_power | Battery charging/ discharging(-ve), Input 5 total energy |
| 78 | . Epv 5_total L | PV 5 Energy total (low) | — | — h | — | — | — | — |
| 79 | Input 6 energy today | PV 6 Energy today(high) | — | — h | — | — | tlx:input_6_energy_today | Input 6 energy today |
| 80 | . Epv 6_today L | PV 6 Energy today (low) | — | — h | — | — | — | — |
| 81 | Input 6 total energy | PV 6 Energy total(high) | — | — h | — | — | tlx:input_6_energy_total | Input 6 total energy |
| 82 | . Epv 6_total L | PV 6 Energy total (low) | — | — h | — | — | — | — |
| 83 | Input 7 energy today | PV 7 Energy today(high) | — | — h | — | — | tlx:input_7_energy_today | Input 7 energy today |
| 84 | . Epv 7_today L | PV 7 Energy today (low) | — | — h | — | — | — | — |
| 85 | Input 7 total energy | PV 7 Energy total(high) | — | — h | — | — | tlx:input_7_energy_total | Input 7 total energy |
| 86 | . Epv 7_total L | PV 7 Energy total (low) | — | — h | — | — | — | — |
| 87 | Input 8 energy today | PV 8 Energy today(high) | — | — h | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 88 | . Epv 8_today L | PV 8 Energy today (low) | — | — h | — | — | — | — |
| 89 | Input 8 total energy | PV 8 Energy total(high) | — | — h | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 90 | . Epv 8_total L | PV 8 Energy total (low) | — | — h | — | — | — | — |
| 91 | Total energy input | PV Energy total(high) | — | — h | — | — | tlx:input_energy_total | Total energy input |
| 92 | . Epv_total L | PV Energy total (low) | — | — h | — | — | — | — |
| 93 | Temperature | Inverter temperature | — | — | — | — | tlx:inverter_temperature | Temperature |
| 94 | Intelligent Power Management temperature | The inside IPM in inverter Temp | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95 | Boost temperature | Boost temperature | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 96 | . Temp 4 | — | — | — reserved | — | — | — | — |
| 97 | . uw Bat Volt_DSP | Bat Volt_DSP | — | — Bat Volt(DSP) | — | — | — | — |
| 98 | P-bus voltage | P Bus inside Voltage | — | — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 99 | N-bus voltage | N Bus inside Voltage | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 10 | 0. IPF | Inverter output PF now | — | — | — | — | — | — |
| 10 | 1. Real OPPercent | Real Output power Percent | — | — | — | — | — | — |
| 10 | 2. OPFullwatt H | Output Maxpower Limited high | — | — | — | — | — | — |
| 10 | 3. OPFullwatt L | Output Maxpower Limited low | — | — | — | — | — | — |
| 10 | 4. Derating Mode | Derating Mode 0 1 2 3 4 5 6 7 8 9 B | — | — | — | — | — | — |
| 10 | 5. Fault Maincode | Inverter fault maincode | — | — | — | — | — | — |
| 10 | 6. | — | — | — | — | — | — | — |
| 10 | 7. Fault Subcode | Inverter fault subcode | — | — | — | — | — | — |
| 10 | 8. Remote Ctrl En | / 0 1 | — | — orage Pow (SPA) | — | — | — | — |
| 10 | 9. Remote Ctrl Pow er | / 2 | — | — orage Pow (SPA) | — | — | — | — |
| 11 | Input 3 voltage | Warning bit H | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Inverter warn subcode | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Inverter warn maincode ACCharge energy today | — | — orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | real Power Percent 0 ACCharge energy today | — | — X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | nv start delay time ACCharge energy total | — | — X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | b INVAll Fault Code ACCharge energy total | — | — X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Grid power to local load | — | — orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Grid power to local load | — | — orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | 0:Load First 1:Battery First 2:Grid First | — | — orage Power | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | 0:Lead-acid 1:Lithium battery | — | — Storage Power | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12 | Input 3 Amperage | Aging mode Auto-cal command | — | — Storage Power | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | — | — | — reserved | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | PID PV 1 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | PID PV 1 PE Curr | — | — m A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | PID PV 2 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | PID PV 2 PE Curr | — | — m A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | PID PV 3 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 13 | AC frequency | PID PV 3 PE Curr | — | — m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 4 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 4 PE Curr | — | — m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 5 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 5 PE Curr | — | — m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 6 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 6 PE Curr | — | — m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 7 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 7 PE Curr | — | — m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | AC frequency | PID PV 8 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 14 | Output 1 voltage | PID PV 8 PE Curr | — | — m A | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | Bit 0~7:PID Working Status 1:Wait Status 2:Normal Status 3:Fault Status Bit 8~15:Reversed | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 1 voltage | — | — V | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 1 current | — | — A | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 2 voltage | — | — V | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 2 current | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 3 voltage | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 3 current | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 4 voltage | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | Output 1 voltage | PV String 4 current | — | — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 15 | Input 4 voltage | PV String 5 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 5 current | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 6 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 6 current | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 7 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 7 current | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 8 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 8 current | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 9 voltage | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | Input 4 voltage | PV String 9 current | — | — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16 | Input 4 Amperage | PV String 10 voltage | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 10 current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 11 voltage | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 11 current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 12 voltage | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 12 current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 13 voltage | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 13 current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 14 voltage | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | Input 4 Amperage | PV String 14 current | — | — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17 | Battery voltage | PV String 15 voltage | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | PV String 15 current | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | PV String 16 voltage | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | PV String 16 current | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | Bit 0~15: String 1~16 unmatch | — | — suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | Bit 0~15: String 1~16 current u | — | — suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | Bit 0~15: String 1~16 disconnec | — | — suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | Bit 0:Output over voltage Bit 1: ISO fault Bit 2: BUS voltage abnormal Bit 3~15:reserved | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | String Prompt Bit 0:String Unmatch Bit 1:Str Disconnect Bit 2:Str Current Unblance Bit 3~15:reserved | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | Battery voltage | PV Warning Value | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 18 | Output 2 voltage | DSP 075 Warning Value | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | ult DSP 075 Fault Value | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 1 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 2 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 3 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 4 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 5 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 6 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 7 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 8 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 19 | Bus voltage | g DSP 075 Debug Data 1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 2 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 3 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 4 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 5 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 6 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 7 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | g DSP 075 Debug Data 8 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | USBAging Test Ok Flag 0-1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | Bus voltage | Flash Erase Aging Ok Flag 0-1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20 | Grid voltage | PVISOValue | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | R DCI Curr | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | S DCI Curr | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | T DCI Curr | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | PIDBus Volt | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | GFCI Curr | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | SVG/APF Status+SVGAPFEqual Rat | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | R phase load side current for | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | S phase load side current for | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | T phase load side current for | — | — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | AC frequency | R phase load side output reac power for SVG(High) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | R phase load side output reac power for SVG(low) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | S phase load side output reac power for SVG(High) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | S phase load side output reac power for SVG(low) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | T phase load side output reac power for SVG(High) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | T phase load side output reac power for SVG(low) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | R phase load side harmonic | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | S phase load side harmonic | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | T phase load side harmonic | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | R phase compensate reactive p for SVG(High) | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 22 | Output 1 voltage | R phase compensate reactive p for SVG(low) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate reactive p for SVG(High) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate reactive p for SVG(low) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate reactive p for SVG(High) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate reactive p for SVG(low) | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | R phase compensate harmonic f SVG | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate harmonic f SVG | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate harmonic f SVG | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | RS 232 Aging Test Ok Flag | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | Output 1 voltage | Bit 0: Fan 1 fault bit Bit 1: Fan 2 fault bit Bit 2: Fan 3 fault bit Bit 3: Fan 4 fault bit Bit 4-7: Reserved | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 23 | Input 6 voltage | Output apparent power H | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Output apparent power L | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Real Output Reactive Power H | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Real Output Reactive Power L | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Nominal Output Reactive Power | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Nominal Output Reactive Power | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Reactive power generation | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Reactive power generation | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | 0:Waiting 1:Self-check state 2:Detect pull arc state 3:Fault 4:Update | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | Input 6 voltage | Present FFTValue [CHANNEL_A] | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24 | Input 6 Amperage | Present FFTValue [CHANNEL_B] | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 1 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 2 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 3 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 4 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 5 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 6 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 7 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 8 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | Input 6 Amperage | — | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 87 | Input 8 energy today | PV 9 voltage | — | — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | Input 8 energy today | PV 9 Input current | — | — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | Input 8 energy today | PV 9 input power (High) | — | — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | Input 8 energy today | PV 9 input power (Low) | — | — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | Input 8 energy today | PV 10 voltage | — | — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 88 | 0 PV 10 Curr | PV 10 Input current | — | — | — | — | — | — |
| 88 | 1 Ppv 10 H | PV 10 input power (High) | — | — | — | — | — | — |
| 88 | 2 Ppv 10 L | PV 10 input power (Low) | — | — | — | — | — | — |
| 88 | 3 Vpv 11 | PV 11 voltage | — | — | — | — | — | — |
| 88 | 4 PV 11 Curr | PV 11 Input current | — | — | — | — | — | — |
| 88 | 5 Ppv 11 H | PV 11 input power (High) | — | — | — | — | — | — |
| 88 | 6 Ppv 11 L | PV 11 input power (Low) | — | — | — | — | — | — |
| 88 | 7 Vpv 12 | PV 12 voltage | — | — | — | — | — | — |
| 88 | 8 PV 12 Curr | PV 12 Input current | — | — | — | — | — | — |
| 88 | 9 Ppv 12 H | PV 12 input power (High) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 12 input power (Low) | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 13 voltage | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 13 Input current | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 13 input power (High) | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 13 input power (Low) | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 14 voltage | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 14 Input current | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 14 input power (High) | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 14 input power (Low) | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | Input 8 total energy | PV 15 voltage | — | — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 90 | 0 PV 15 Curr | PV 15 Input current | — | — | — | — | — | — |
| 90 | 1 Ppv 15 H | PV 15 input power (High) | — | — | — | — | — | — |
| 90 | 2 Ppv 15 L | PV 15 input power (Low) | — | — | — | — | — | — |
| 90 | 3 Vpv 16 | PV 16 voltage | — | — | — | — | — | — |
| 90 | 4 PV 16 Curr | PV 16 Input current | — | — | — | — | — | — |
| 90 | 5 Ppv 16 H | PV 16 input power (High) | — | — | — | — | — | — |
| 90 | 6 Ppv 16 L | PV 16 input power (Low) | — | — | — | — | — | — |
| 90 | 7 Epv 9_today H | PV 9 energy today (High) | — | — | — | — | — | — |
| 90 | 8 Epv 9_today L | PV 9 energy today (Low) | — | — | — | — | — | — |
| 90 | 9 Epv 9_total H | PV 9 energy total (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 9 energy total (Low) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 10 energy today (High) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 10 energy today (Low) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 10 energy total (High) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 10 energy total (Low) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 11 energy today (High) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 11 energy today (Low) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 11 energy total (High) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 11 energy total (Low) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 91 | Total energy input | PV 12 energy today (High) | — | — | — | — | tlx:input_energy_total | Total energy input |
| 92 | 0 Epv 12_today L | PV 12 energy today (Low) | — | — | — | — | — | — |
| 92 | 1 Epv 12_total H | PV 12 energy total (High) | — | — | — | — | — | — |
| 92 | 2 Epv 12_total L | PV 12 energy total (Low) | — | — | — | — | — | — |
| 92 | 3 Epv 13_today H | PV 13 energy today (High) | — | — | — | — | — | — |
| 92 | 4 Epv 13_today L | PV 13 energy today (Low) | — | — | — | — | — | — |
| 92 | 5 Epv 13_total H | PV 13 energy total (High) | — | — | — | — | — | — |
| 92 | 6 Epv 13_total L | PV 13 energy total (Low) | — | — | — | — | — | — |
| 92 | 7 Epv 14_today H | PV 14 energy today (High) | — | — | — | — | — | — |
| 92 | 8 Epv 14_today L | PV 14 energy today (Low) | — | — | — | — | — | — |
| 92 | 9 Epv 14_total H | PV 14 energy total (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 14 energy total (Low) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 15 energy today (High) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 15 energy today (Low) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 15 energy total (High) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 15 energy total (Low) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 16 energy today (High) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 16 energy today (Low) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 16 energy total (High) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PV 16 energy total (Low) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 93 | Temperature | PID PV 9 PE Volt/ Flyspan volta (MAX HV) | — | — | — | — | tlx:inverter_temperature | Temperature |
| 94 | Intelligent Power Management temperature | PID PV 9 PE Current | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | + PID PV 10 PE/ Flyspan voltage ( HV) | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 0+ PID PV 10 PE Current | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 1+ PID PV 11 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 1+ PID PV 11 PE Current | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 2+ PID PV 12 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 2+ PID PV 12 PE Current | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 3+ PID PV 13 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 3+ PID PV 13 PE Current | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | Intelligent Power Management temperature | 4+ PID PV 14 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95 | Boost temperature | 4+ PID PV 14 PE Current | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | 5+ PID PV 15 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | 5+ PID PV 15 PE Current | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | 6+ PID PV 16 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | 6+ PID PV 16 PE Current | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | PV String 17 voltage | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | PV String 17 Current | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | PV String 18 voltage | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | PV String 18 Current | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | Boost temperature | PV String 19 voltage | — | — | — | — | tlx:boost_temperature | Boost temperature |
| 96 | 0 Curr _String 19 | PV String 19 Current | — | — | — | — | — | — |
| 96 | 1 V _String 20 | PV String 20 voltage | — | — | — | — | — | — |
| 96 | 2 Curr _String 20 | PV String 20 Current | — | — | — | — | — | — |
| 96 | 3 V _String 21 | PV String 21 voltage | — | — | — | — | — | — |
| 96 | 4 Curr _String 21 | PV String 21 Current | — | — | — | — | — | — |
| 96 | 5 V _String 22 | PV String 22 voltage | — | — | — | — | — | — |
| 96 | 6 Curr _String 22 | PV String 22 Current | — | — | — | — | — | — |
| 96 | 7 V _String 23 | PV String 23 voltage | — | — | — | — | — | — |
| 96 | 8 Curr _String 23 | PV String 23 Current | — | — | — | — | — | — |
| 96 | 9 V _String 24 | PV String 24 voltage | — | — | — | — | — | — |
| 97 | 0 Curr _String 24 | PV String 24 Current | — | — 0.1 A | — | — | — | — |
| 97 | 1 V _String 25 | PV String 25 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 2 Curr _String 25 | PV String 25 Current | — | — 0.1 A | — | — | — | — |
| 97 | 3 V _String 26 | PV String 26 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 4 Curr _String 26 | PV String 26 Current | — | — 0.1 A | — | — | — | — |
| 97 | 5 V _String 27 | PV String 27 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 6 Curr _String 27 | PV String 27 Current | — | — 0.1 A | — | — | — | — |
| 97 | 7 V _String 28 | PV String 28 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 8 Curr _String 28 | PV String 28 Current | — | — 0.1 A | — | — | — | — |
| 97 | 9 V _String 29 | PV String 29 voltage | — | — 0.1 V | — | — | — | — |
| 98 | P-bus voltage | PV String 29 Current | — | — 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 30 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 30 Current | — | — 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 31 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 31 Current | — | — 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 32 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | PV String 32 Current | — | — 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | Bit 0~15: String 17~32 unmatch | — | — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | Bit 0~15:String 17~32 unblance | — | — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | P-bus voltage | Bit 0~15: String 17~32 disconn | — | — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 99 | N-bus voltage | PV Warning Value (PV 9-PV 16) Contains PV 9~16 abnormal, 和 Boost 9~16 Drive anomalies | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | N-bus voltage | string 1~string 16 abnormal | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | N-bus voltage | string 17~string 32 abnormal | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | N-bus voltage | M 3 to DSP system command | — | — system command | — | — | tlx:n_bus_voltage | N-bus voltage |
| 10 | 00. uw Sys Work Mode | System work mode | — | — Theworkingmode displayed by the monitoring to the customer is: 0 x 00: waiting module 0 x 01: Self-test mode, 0 x 03:fault module 0 x 04:flash odule x 05|0 x 06|0 x 07|0 08:normal odule | — | — | — | — |
| 10 | 01. Systemfault word 0 | System fault word 0 | — | — lease refer to hefault escription of ybrid | — | — | — | — |
| 10 | 02. Systemfault word 1 | System fault word 1 | — | — | — | — | — | — |
| 10 | 03. Systemfault word 2 | System fault word 2 | — | — | — | — | — | — |
| 10 | 04. Systemfault word 3 | System fault word 3 | — | — | — | — | — | — |
| 10 | 05. Systemfault word 4 | System fault word 4 | — | — | — | — | — | — |
| 10 | 06. Systemfault word 5 | System fault word 5 | — | — | — | — | — | — |
| 10 | 07. Systemfault word 6 | System fault word 6 | — | — | — | — | — | — |
| 10 | 08. Systemfault word 7 | System fault word 7 | — | — | — | — | — | — |
| 10 | 09. Pdischarge 1 H | Discharge power(high) | — | — | — | — | — | — |
| 10 | 10. Pdischarge 1 L | Discharge power (low) | — | — | — | — | — | — |
| 10 | 11. Pcharge 1 H | Charge power(high) | — | — | — | — | — | — |
| 10 | 12. Pcharge 1 L | Charge power (low) | — | — | — | — | — | — |
| 10 | 13. Vbat | Battery voltage | — | — | — | — | — | — |
| 10 | 14. SOC | State of charge Capacity | — | — ith/leadacid | — | — | — | — |
| 10 | 15. Pactouser R | H AC power to user H | — | — | — | — | — | — |
| 10 | 16. Pactouser R | L AC power to user L | — | — | — | — | — | — |
| 10 | 17. Pactouser S | H Pactouser S H | — | — | — | — | — | — |
| 10 | 18. Pactouser S | L Pactouser S L | — | — | — | — | — | — |
| 10 | 19. Pactouser T | H Pactouser T H | — | — | — | — | — | — |
| 10 | 20. Pactouser T | L Pactouser T H | — | — | — | — | — | — |
| 10 | 21. Pactouser Total H | AC power to user total H | — | — | — | — | — | — |
| 10 | 22. Pactouser Total L | AC power to user total L | — | — | — | — | — | — |
| 10 | 23. Pac to grid R H | AC power to grid H | — | — c output | — | — | — | — |
| 10 | 24. Pac to grid R L | AC power to grid L | — | — | — | — | — | — |
| 10 | 25. Pactogrid S H | — | — | — | — | — | — | — |
| 10 | 26. Pactogrid S L | — | — | — | — | — | — | — |
| 10 | 27. Pactogrid T H | — | — | — | — | — | — | — |
| 10 | 28. Pactogrid T L | — | — | — | — | — | — | — |
| 10 | 29. Pactogrid total H | AC power to grid total H | — | — | — | — | — | — |
| 10 | 30. Pactogrid total L | AC power to grid total L | — | — | — | — | — | — |
| 10 | 31. PLocal Load R | H INV power to local load H | — | — | — | — | — | — |
| 10 | 32. PLocal Load R | L INV power to local load L | — | — | — | — | — | — |
| 10 | 33. PLocal Load S | H | — | — | — | — | — | — |
| 10 | 34. PLocal Load S | L | — | — | — | — | — | — |
| 10 | 35. PLocal Load T H | — | — | — | — | — | — | — |
| 10 | 36. PLocal Load T L | — | — | — | — | — | — | — |
| 10 | 37. PLocal Load total | H INV power to local load tot | — | — | — | — | — | — |
| 10 | 38. PLocal Load total | L INV power to local load tot L | — | — | — | — | — | — |
| 10 | 39. IPM 2 Temperature | REC Temperature | — | — | — | — | — | — |
| 10 | 40. Battery 2 Temperature | Battery Temperature | — | — ithium p | — | — | — | — |
| 10 | 41. SP DSP Status | SP state | — | — | — | — | — | — |
| 10 | 42. SP Bus Volt | SP BUS 2 Volt | — | — | — | — | — | — |
| 10 | 43 | — | — | — | — | — | — | — |
| 10 | 44. Etouser_today H | Energy to user today high | — | — | — | — | — | — |
| 10 | 45. Etouser_today L | Energy to user today low | — | — | — | — | — | — |
| 10 | 46. Etouser_total H | Energy to user total high | — | — | — | — | — | — |
| 10 | 47. Etouser_ total L | Energy to user total high | — | — | — | — | — | — |
| 10 | 48. Etogrid_today H | Energy to grid today high | — | — | — | — | — | — |
| 10 | 49. Etogrid _today L | Energy to grid today low | — | — | — | — | — | — |
| 10 | 50. Etogrid _total H | Energy to grid total high | — | — | — | — | — | — |
| 10 | 51. Etogrid _ total L | Energy to grid total high | — | — | — | — | — | — |
| 10 | 52. Edischarge 1_toda y H | Discharge energy 1 today | — | — | — | — | — | — |
| 10 | 53. Edischarge 1_toda y L | Discharge energy 1 today | — | — | — | — | — | — |
| 10 | 54. Edischarge 1_total H | Total discharge energy 1 (high) | — | — | — | — | — | — |
| 10 | 55. Edischarge 1_total L | Total discharge energy 1 (low) | — | — | — | — | — | — |
| 10 | 56. Echarge 1_today H | Charge 1 energy today | — | — | — | — | — | — |
| 10 | 57. Echarge 1_today L | Charge 1 energy today | — | — | — | — | — | — |
| 10 | 58. Echarge 1_total H | Charge 1 energy total | — | — | — | — | — | — |
| 10 | 59. Echarge 1_total L | Charge 1 energy total | — | — | — | — | — | — |
| 10 | 60. ELocal Load_Today H | Local load energy today | — | — | — | — | — | — |
| 10 | 61. ELocal Load_Today L | Local load energy today | — | — | — | — | — | — |
| 10 | 62. ELocal Load_Total H | Local load energy total | — | — | — | — | — | — |
| 10 | 63. ELocal Load_Total L | Local load energy total | — | — | — | — | — | — |
| 10 | 64. dw Export Limit Ap parent Power | Export Limit Apparent Power H | — | — rent Power | — | — | — | — |
| 10 | 65. dw Export Limit Ap parent Power | Export Limit Apparent Power L | — | — rent Power | — | — | — | — |
| 10 | 66. / | / | — | — rved | — | — | — | — |
| 10 | 67. EPS Fac | UPSfrequency | — | — | — | — | — | — |
| 10 | 68. EPS Vac 1 | UPS phase R output voltage | — | — | — | — | — | — |
| 10 | 69. EPS Iac 1 | UPS phase R output current | — | — | — | — | — | — |
| 10 | 70. EPS Pac 1 H | UPS phase R output power (H) | — | — | — | — | — | — |
| 10 | 71. EPS Pac 1 L | UPS phase R output power (L) | — | — | — | — | — | — |
| 10 | 72. EPS Vac 2 | UPS phase S output voltage | — | — | — | — | — | — |
| 10 | 73. EPS Iac 2 | UPS phase S output current | — | — se | — | — | — | — |
| 10 | 74. EPS Pac 2 H | UPS phase S output power (H) | — | — | — | — | — | — |
| 10 | 75. EPS Pac 2 L | UPS phase S output power (L) | — | — | — | — | — | — |
| 10 | 76. EPS Vac 3 | UPS phase T output voltage | — | — | — | — | — | — |
| 10 | 77. EPS Iac 3 | UPS phase T output current | — | — se | — | — | — | — |
| 10 | 78. EPS Pac 3 H | UPS phase T output power (H) | — | — | — | — | — | — |
| 10 | 79. EPS Pac 3 L | UPS phase T output power (L) | — | — | — | — | — | — |
| 10 | 80. Loadpercent | Load percent of UPS ouput | — | — | — | — | — | — |
| 10 | 81. PF | Power factor | — | — ary Value+1 | — | — | — | — |
| 10 | 82. BMS_Status Old | Status Old from BMS | — | — | — | — | — | — |
| 10 | 83. BMS_Status | Status from BMS | — | — | — | — | — | — |
| 10 | 84. BMS_Error Old | Error info Old from BMS | — | — | — | — | — | — |
| 10 | 85. BMS_Error | Errorinfomation from BMS | — | — | — | — | — | — |
| 10 | 86. BMS_SOC BMS_Battery Vol | SOC from BMS Battery voltage from BMS | — | — H 6 K H 6 K | — | — | — | — |
| 10 | 87. t BMS_Battery Cur | Battery current from BMS | — | — | — | — | — | — |
| 10 | 88. r BMS_Battery Te | Battery temperature from BMS | — | — | — | — | — | — |
| 10 | 89. mp BMS_Max Curr | Max. charge/discharge current | — | — | — | — | — | — |
| 10 | 90. | from BMS (pylon) | — | — | — | — | — | — |
| 10 | 91. BMS_Gauge RM | Gauge RM from BMS | — | — | — | — | — | — |
| 10 | 92. BMS_Gauge FCC | Gauge FCC from BMS | — | — | — | — | — | — |
| 10 | 93. BMS_FW | — | — | — | — | — | — | — |
| 10 | 94. BMS_Delta Volt | Delta V from BMS | — | — | — | — | — | — |
| 10 | 95. BMS_Cycle Cnt | Cycle Count from BMS | — | — | — | — | — | — |
| 10 | 96. BMS_SOH BMS_Constant V | SOH from BMS CV voltage from BMS | — | — | — | — | — | — |
| 10 | 97. olt BMS_Warn Info O | Warning info old from BMS | — | — | — | — | — | — |
| 10 | 98. ld | — | — | — | — | — | — | — |
| 10 | 99. BMS_Warn Info BMS_Gauge ICCu | Warning info from BMS Gauge IC current from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | MCU Software version from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Gauge Version from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Gauge FR Version L 16 from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Gauge FR Version H 16 from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | BMSInformation from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Pack Information from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Using Cap from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Maximum single battery voltage | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Lowest single battery voltage | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery parallel number | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Number of batteries Max Volt Cell No | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Min Volt Cell No | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Max Tempr Cell_10 T | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Min Tempr Cell_10 T | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Max Volt Tempr Cell No | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Min Volt Tempr Cell No | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Faulty Battery Address | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Parallel maximum SOC | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Parallel minimum SOC Battery Protection 2 | — | — CAN ID: 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery Protection 3 | — | — Byte 4~5 CAN ID: 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery Warn 2 | — | — Byte 6 CAN ID: 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — Byte 7 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | AC Charge Energy today | — | — Energy today | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | AC Charge Energy today | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — Energy total | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | AC Charge Power | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | AC Charge Power | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | uw Grid Power_70_Adj EE_SP | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | tra inverte AC Power to grid gh | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | trainverte AC Power to grid Low | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr today (high) | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr today (low) | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr total(high) | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr total(low) | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | System electric energy today H | — | — SPA used System electric energy today H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | stem electric energy today L | — | — d electric today L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | System electric energy total H | — | — d electric total H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | System electric energy total L | — | — d electric total L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self electric energy today H | — | — electric today H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self electric energy today L | — | — electric today L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self electric energy total H | — | — electric total H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self electric energy total L | — | — electric total L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | System power H | — | — power H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | System power L | — | — power L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self power H | — | — wer H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | self power L | — | — wer L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | PV electric energy today H | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | PV electric energy today L | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Discharge power pack number | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Cumulative discharge power high 16-bit byte | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Cumulative discharge power low 16-bit byte | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | charge power pack serial number | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Cumulative charge power high R 16-bit byte | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Cumulative charge power low R 16-bit byte | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | First Batt Fault Sn | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Second Batt Fault Sn | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Third Batt Fault Sn | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Fourth Batt Fault Sn | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 1 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 2 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 3 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 4 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 5 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 6 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 7 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Battery history fault code 8 | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Number of battery codes PACK number + BIC forward and reverse codes | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | Input 3 voltage | Intelligent reading is used to identify software compatibility features | — | — rgy; rgy | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 1 | Input 1 voltage | Maximum cell voltage | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Minimum cell voltage | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Number of Battery modules | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Total number of cells | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Max Volt Cell No | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Min Volt Cell No | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Max Tempr Cell_10 T | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Min Tempr Cell_10 T | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Max Tempr Cell No | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Min Tempr Cell No | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Fault Pack ID | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Parallel maximum SOC | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Parallel minimum SOC | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Bat Protect 1 Add | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Bat Protect 2 Add | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | Bat Warn 1 Add | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Highest Soft Version | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Hardware Version | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Request Type | — | — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 12 | Input 3 Amperage | Success sign of key detection before aging | — | — 1:Finished test 0: test not completed | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | Input 3 Amperage | / | — | — reversed | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 20 | Grid voltage | Inverter run state | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Output power (high) | — | — 1 W SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Output power (low) | — | — 1 W SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Grid frequency | — | — 01 Hz SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Three/single phase grid voltage | — | — 1 V SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Three/single phase grid output | — | — 1 A SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Three/single phase grid output VA (high) | — | — 1 VA SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Three/single phase grid output VA(low) | — | — 1 VA SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Today generate energy (high) | — | — 1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Today generate energy (low) | — | — 1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Total generate energy (high) | — | — WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Total generate energy (low) | — | — WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Work time total (high) | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Work time total (low) | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Inverter temperature | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | The inside IPM in inverter Temp | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Boost temperature | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | — | — | — reserved | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | Bat Volt_DSP | — | — Bat Volt(DSP) | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | P Bus inside Voltage | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | Grid voltage | N Bus inside Voltage | — | — SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | AC frequency | / | — | — Remote setup enable | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | / | — | — Remotely set power | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extra inverte AC Power to grid | — | — SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extrainverte AC Power to grid L | — | — SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extra inverter Power TOUser_Extr today (high) | — | — Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extra inverter Power TOUser_Extr today (low) | — | — Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extra inverter Power TOUser_Extratotal(high) | — | — Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Extra inverter Power TOUser_Extr total(low) | — | — Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | System electric energy today H | — | — Wh SPA used System electric energy today H | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | stem electric energy today L | — | — Wh SPA used System electric energy today L | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | System electric energy total H | — | — Wh SPA used System c total | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | System electric energy total L | — | — d c total | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | ACCharge energy today | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | ACCharge energy today | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | ACCharge energy total | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | ACCharge energy total | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Grid power to local load | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Grid power to local load | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | 0:Load First 1:Battery First 2:Grid First | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | 0:Lead-acid 1:Lithium battery | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | Aging mode | — | — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | AC frequency | — | — | — d | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 3 | Input 1 Wattage | 2: Reserved 3:Sys Fault module 4: Flash module 5:PVBATOnline module: 6:Bat Online module 7:PVOffline Mode 8:Bat Offline Mode The lower 8 bits indicate the m status (web page display) 0: Standby Status; 1: Normal Status; 3: Fault Status 4:Flash Status; | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV total power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 1 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 1 input current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 1 power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 2 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 2 input current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 2 power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 3 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 3 input current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 3 power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 4 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 4 input current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 4 power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | System output power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | reactive power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Output power | — | — ut | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Grid frequency | — | — r | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three/single phase grid voltage | — | — uency e/single | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — e grid age | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three/single phase grid output | — | — e/single rid | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three/single phase grid output VA | — | — ingle rid | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — watt hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid output current | — | — ltage hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid output power | — | — hase tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid output current | — | — ltage hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid output power | — | — hase tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total forward power | — | — orward | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total reverse power | — | — everse | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total load power | — | — load | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Work time total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today generate energy | — | — e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total generate energy | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 1 energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 1 energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 2 energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 2 energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 3 energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 3 energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today energy to user | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy to user | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today energy to grid | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy to grid | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today energy of user load | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy of user load | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 4 energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV 4 energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Derating Mode | — | — h | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — k T l A i | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | PV ISO value | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | R DCI Curr | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | S DCI Curr | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | T DCI Curr | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | GFCI Curr | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | total bus voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter temperature | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | The inside IPM in inverter temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Boost temperature | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Reserved | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Commmunication broad temperatur | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | P Bus inside Voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | N Bus inside Voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter output PF now | — | — 000 | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Real Output power Percent | — | — 0 | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Output Maxpower Limited | — | — ut ower | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter standby flag | — | — ted:turn off r;:PV Low;:AC | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — /Freq of scope; ~bit 7: rved | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter fault maincode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter Warning maincode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter fault subcode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Inverter Warning subcode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Present FFTValue [CHANNEL_A] | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | AFCI Status | — | — waiting e lf-check Detection | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | AFCI Strength[CHANNEL_A] | — | — arcing e ult state update e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | AFCI Self Check[CHANNEL_A] | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | inv start delay time | — | — lay | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BDC connect state | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Current status of Dry Contact | — | — of | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | self-use power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | System energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today discharge energy | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total discharge energy | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Charge energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Charge energy total | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today energy of AC charge | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy of AC charge | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy of system outpu | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Today energy of Self output | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total energy of Self output | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Word Mode | — | — ad First | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — ery Firs id First | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS frequency | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase R output voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase R output current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase R output power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase S output voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase S output current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase S output power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase T output voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase T output current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS phase T output power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | UPS output power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Load percent of UPS ouput | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Power factor | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | DC voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Whether to parse BDC data separ | — | — on't need | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BDCDerating Mode: 0: Normal, unrestricted 1:Standby or fault | — | — ed | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | 2:Maximum battery current limit (discharge) 3:Battery discharge Enable (Dis 4:High bus discharge derating (discharge) 5:High temperature discharge derating (discharge) 6:System warning No discharge (discharge) 7-15 Reserved (Discharge) 16:Maximum charging current of battery (charging) 17:High Temperature (LLC and Buckboost) (Charging) 18:Final soft charge 19:SOC setting limits (charging 20:Battery low temperature (cha 21:High bus voltage (charging) 22:Battery SOC (charging) 23: Need to charge (charge) 24: System warning not charging (charging) 25-29:Reserve (charge) System work State and mode The upper 8 bits indicate the mode; 0:No charge and discharge; 1:charge; 2:Discharge; | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | The lower 8 bits represent the 0: Standby Status; 1: Normal Status; 2: Fault Status 3:Flash Status; | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Storge device fault code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Storge device warning code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Battery voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Battery current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | State of charge Capacity | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Total BUS voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | On the BUS voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BUCK-BOOST Current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | LLC Current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Temperture A | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Temperture B | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Discharge power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Charge power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Discharge total energy of storg | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Charge total energy of storge d | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Reserved BDC mark (charge and dischar fault alarm code) Bit 0: Charge En; BDC allows char Bit 1: Discharge En; BDC allows discharge | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bit 2~7: Resvd; reserved Bit 8~11: Warn Sub Code; BDC sub-warning code Bit 12~15: Fault Sub Code; BDC sub-error code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Lower BUS voltage Bms Max Volt Cell No | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Min Volt Cell No | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Max Cell Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Max Cell Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Max SOC | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Min SOC Parallel Battery Num | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Derate Reason | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Gauge FCC(Ah) | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Bms Gauge RM(Ah) | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Protect 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMSWarn 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Fault 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Fault 2 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Battery ISO detection status | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | battery work request | — | — n | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | battery working status | — | — mancy ge harge | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — dby start t te | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Protect 2 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Warn 2 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS SOC BMS Battery Volt | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Battery Curr | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | battery cell maximum temperatur | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Maximum charging current Maximum discharge current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMSCycle Cnt | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS SOH Battery charging voltage limit | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | Battery discharge voltage limit | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Warn 3 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | BMS Protect 3 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | Input 1 Wattage | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 32 | Input 8 Amperage | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | BMS Battery Single Volt Max | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | BMS Battery Single Volt Min | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery Load Volt | — | — 0,650.00] | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 1 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 2 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 3 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 4 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 5 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 6 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 7 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 8 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 9 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 10 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 10 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 12 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 13 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 14 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 15 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Debug data 16 | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 output power H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 output power L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 output power H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 output power L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 energy Today H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 energy Today L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 energy Today H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 energy Today L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 energy Total H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 1 energy Total L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 energy Total H | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | PV inverter 2 energy Total L | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | battery pack number | — | — C reports e updated ery 15 nutes | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[0] | — | — C reports e updated | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[2] | — | — ery 15 | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[4] | — | — nutes | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[6] | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[8] | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[10]SN[11] | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[12]SN[13] | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Battery pack serial number SN[14]SN[15] | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Reserve | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | Input 8 Amperage | Clear day data flag | — | — ta of the rrent day at the rver determines whether to clear. 0:not cleared. 1: Clear. | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 40 | Fault code | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 41 | Intelligent Power Management temperature | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 41 | Intelligent Power Management temperature | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 42 | Fault code | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 48 | Input 1 energy today | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 49 | 71 | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | — | — |
| 49 | 72- 10 | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | — | — |
| 50 | Input 1 total energy | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | tl3:input_1_energy_total, offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |

## Offgrid SPF Input Registers
Observed off-grid register map (from integration implementation).

**Applies to:** Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Status code | Inverter run state | — | — | — | — | offgrid:status_code | Status code |
| 1 | Input 1 voltage | Input power (high) | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 2 | Input 2 voltage | Input power (low) | — | — | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3 | Input 1 Wattage | PV 1 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 4 | Input 1 Amperage | PV 1 input current | — | — | — | — | — | — |
| 5 | Input 1 Wattage | PV 1 input power(high) | — | — | — | — | offgrid:input_2_power | Input 2 Wattage, PV2 charge power |
| 6 | Ppv 1 L | PV 1 input power(low) | — | — | — | — | — | — |
| 7 | Input 1 Amperage | PV 2 voltage | — | — | — | — | offgrid:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 8 | Input 2 Amperage | PV 2 input current | — | — | — | — | offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9 | Input 2 Wattage | PV 2 input power (high) | — | — | — | — | offgrid:output_active_power | Output active power |
| 10 | . Ppv 2 L | PV 2 input power (low) | — | — | — | — | — | — |
| 11 | Input 3 voltage | PV 3 voltage | — | — | — | — | — | — |
| 12 | Input 3 Amperage | PV 3 input current | — | — | — | — | — | — |
| 13 | AC frequency | PV 3 input power (high) | — | — | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 14 | Output 1 voltage | PV 3 input power (low) | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV 4 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV 4 input current | — | — | — | — | — | — |
| 17 | Battery voltage | PV 4 input power (high) | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 18 | Output 2 voltage | PV 4 input power (low) | — | — | — | — | offgrid:soc | SOC |
| 19 | Bus voltage | PV 5 voltage | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 20 | Grid voltage | PV 5 input current | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | AC frequency | PV 5 input power(high) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 22 | Output 1 voltage | PV 5 input power(low) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 23 | Input 6 voltage | PV 6 voltage | — | — | — | — | offgrid:output_frequency | Output frequency |
| 24 | Input 6 Amperage | PV 6 input current | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 25 | Input 6 Wattage | PV 6 input power (high) | — | — | — | — | offgrid:inverter_temperature | Temperature |
| 26 | DC-DC temperature | PV 6 input power (low) | — | — | — | — | offgrid:dc_dc_temperature | DC-DC temperature |
| 27 | Input 7 voltage | PV 7 voltage | — | — | — | — | offgrid:load_percent | Inverter load |
| 28 | Battery port voltage | PV 7 input current | — | — | — | — | offgrid:battery_port_voltage | Battery port voltage |
| 29 | Battery bus voltage | PV 7 input power (high) | — | — | — | — | offgrid:battery_bus_voltage | Battery bus voltage |
| 30 | Running hours | PV 7 input power (low) | — | — | — | — | offgrid:operation_hours | Running hours |
| 31 | Input 8 voltage | PV 8 voltage | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV 8 input current | — | — | — | — | — | — |
| 33 | Input 8 Wattage | PV 8 input power (high) | — | — | — | — | — | — |
| 34 | Output 1 Amperage | PV 8 input power (low) | — | — | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35 | Output power | Output power (high) | — | — | — | — | — | — |
| 36 | . Pac L | Output power (low) | — | — | — | — | — | — |
| 37 | AC frequency | Grid frequency | — | — | — | — | — | — |
| 38 | Output 1 voltage | Three/single phase grid voltage | — | — | — | — | — | — |
| 39 | Output 1 Amperage | Three/single phase grid output | — | — | — | — | — | — |
| 40 | Fault code | Three/single phase grid output VA (high) | — | — | — | — | — | — |
| 41 | Intelligent Power Management temperature | Three/single phase grid output VA(low) | — | — | — | — | — | — |
| 42 | Fault code | Three phase grid voltage | — | — | — | — | offgrid:fault_code | Fault code |
| 43 | N-bus voltage | Three phase grid output current | — | — | — | — | offgrid:warning_code | Warning code |
| 44 | Output 2 Wattage | Three phase grid output power ( | — | — | — | — | — | — |
| 45 | . Pac 2 L | Three phase grid output power ( | — | — | — | — | — | — |
| 46 | Output 3 voltage | Three phase grid voltage | — | — | — | — | — | — |
| 47 | Derating mode | Three phase grid output current | — | — | — | — | offgrid:constant_power | — |
| 48 | Input 1 energy today | Three phase grid output power ( | — | — | — | — | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 49 | . Pac 3 L | Three phase grid output power ( | — | — | — | — | — | — |
| 50 | Input 1 total energy | Three phase grid voltage | — | — ne voltage | — | — | offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51 | . Vac_ST | Three phase grid voltage | — | — ne voltage | — | — | — | — |
| 52 | Input 2 energy today | Three phase grid voltage | — | — ne voltage | — | — | offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53 | Energy produced today | Today generate energy (high) | — | — | — | — | — | — |
| 54 | Input 2 total energy | Today generate energy (low) | — | — | — | — | offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55 | Total energy produced | Total generate energy (high) | — | — | — | — | — | — |
| 56 | Battery Charged (Today) | Total generate energy (low) | — | — | — | — | offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 57 | Running hours | Work time total (high) | — | — | — | — | — | — |
| 58 | Battery Charged (Total) | Work time total (low) | — | — | — | — | offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 59 | Input 1 energy today | PV 1 Energy today(high) | — | — | — | — | — | — |
| 60 | Battery Discharged (Today) | PV 1 Energy today (low) | — | — | — | — | offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61 | Input 1 total energy | PV 1 Energy total(high) | — | — | — | — | — | — |
| 62 | Battery Discharged (Total) | PV 1 Energy total (low) | — | — | — | — | offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63 | Input 2 energy today | PV 2 Energy today(high) | — | — | — | — | — | — |
| 64 | AC Discharged Today | PV 2 Energy today (low) | — | — h | — | — | offgrid:ac_discharge_energy_today | AC Discharged Today |
| 65 | Input 2 total energy | PV 2 Energy total(high) | — | — h | — | — | — | — |
| 66 | Grid Discharged Lifetime | PV 2 Energy total (low) | — | — h | — | — | offgrid:ac_discharge_energy_total | Grid Discharged Lifetime |
| 67 | Input 3 energy today | PV 3 Energy today(high) | — | — h | — | — | — | — |
| 68 | AC charge battery current | PV 3 Energy today (low) | — | — h | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69 | Battery discharge power | PV 3 Energy total(high) | — | — h | — | — | offgrid:discharge_power | Battery discharge power, Discharge Power |
| 70 | . Epv 3_total L | PV 3 Energy total (low) | — | — h | — | — | — | — |
| 71 | Input 4 energy today | PV 4 Energy today(high) | — | — h | — | — | — | — |
| 72 | . Epv 4_today L | PV 4 Energy today (low) | — | — h | — | — | — | — |
| 73 | Battery discharge current | PV 4 Energy total(high) | — | — h | — | — | offgrid:battery_discharge_amperage | Battery discharge current |
| 74 | . Epv 4_total L | PV 4 Energy total (low) | — | — h | — | — | — | — |
| 75 | Input 5 energy today | PV 5 Energy today(high) | — | — h | — | — | — | — |
| 76 | . Epv 5_today L | PV 5 Energy today (low) | — | — h | — | — | — | — |
| 77 | Battery charging/ discharging(-ve) | PV 5 Energy total(high) | — | — h | — | — | offgrid:battery_power | Battery charging/ discharging(-ve) |
| 78 | . Epv 5_total L | PV 5 Energy total (low) | — | — h | — | — | — | — |
| 79 | Input 6 energy today | PV 6 Energy today(high) | — | — h | — | — | — | — |
| 80 | . Epv 6_today L | PV 6 Energy today (low) | — | — h | — | — | — | — |
| 81 | Input 6 total energy | PV 6 Energy total(high) | — | — h | — | — | — | — |
| 82 | . Epv 6_total L | PV 6 Energy total (low) | — | — h | — | — | — | — |
| 83 | Input 7 energy today | PV 7 Energy today(high) | — | — h | — | — | — | — |
| 84 | . Epv 7_today L | PV 7 Energy today (low) | — | — h | — | — | — | — |
| 85 | Input 7 total energy | PV 7 Energy total(high) | — | — h | — | — | — | — |
| 86 | . Epv 7_total L | PV 7 Energy total (low) | — | — h | — | — | — | — |
| 87 | Input 8 energy today | PV 8 Energy today(high) | — | — h | — | — | — | — |
| 88 | . Epv 8_today L | PV 8 Energy today (low) | — | — h | — | — | — | — |
| 89 | Input 8 total energy | PV 8 Energy total(high) | — | — h | — | — | — | — |
| 90 | . Epv 8_total L | PV 8 Energy total (low) | — | — h | — | — | — | — |
| 91 | Total energy input | PV Energy total(high) | — | — h | — | — | — | — |
| 92 | . Epv_total L | PV Energy total (low) | — | — h | — | — | — | — |
| 93 | Temperature | Inverter temperature | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | The inside IPM in inverter Temp | — | — | — | — | — | — |
| 95 | Boost temperature | Boost temperature | — | — | — | — | — | — |
| 96 | . Temp 4 | — | — | — reserved | — | — | — | — |
| 97 | . uw Bat Volt_DSP | Bat Volt_DSP | — | — Bat Volt(DSP) | — | — | — | — |
| 98 | P-bus voltage | P Bus inside Voltage | — | — | — | — | — | — |
| 99 | N-bus voltage | N Bus inside Voltage | — | — | — | — | — | — |
| 10 | 0. IPF | Inverter output PF now | — | — | — | — | — | — |
| 10 | 1. Real OPPercent | Real Output power Percent | — | — | — | — | — | — |
| 10 | 2. OPFullwatt H | Output Maxpower Limited high | — | — | — | — | — | — |
| 10 | 3. OPFullwatt L | Output Maxpower Limited low | — | — | — | — | — | — |
| 10 | 4. Derating Mode | Derating Mode 0 1 2 3 4 5 6 7 8 9 B | — | — | — | — | — | — |
| 10 | 5. Fault Maincode | Inverter fault maincode | — | — | — | — | — | — |
| 10 | 6. | — | — | — | — | — | — | — |
| 10 | 7. Fault Subcode | Inverter fault subcode | — | — | — | — | — | — |
| 10 | 8. Remote Ctrl En | / 0 1 | — | — orage Pow (SPA) | — | — | — | — |
| 10 | 9. Remote Ctrl Pow er | / 2 | — | — orage Pow (SPA) | — | — | — | — |
| 11 | Input 3 voltage | Warning bit H | — | — | — | — | — | — |
| 11 | Input 3 voltage | Inverter warn subcode | — | — | — | — | — | — |
| 11 | Input 3 voltage | Inverter warn maincode ACCharge energy today | — | — orage wer | — | — | — | — |
| 11 | Input 3 voltage | real Power Percent 0 ACCharge energy today | — | — X orage wer | — | — | — | — |
| 11 | Input 3 voltage | nv start delay time ACCharge energy total | — | — X orage wer | — | — | — | — |
| 11 | Input 3 voltage | b INVAll Fault Code ACCharge energy total | — | — X orage wer | — | — | — | — |
| 11 | Input 3 voltage | Grid power to local load | — | — orage wer | — | — | — | — |
| 11 | Input 3 voltage | Grid power to local load | — | — orage wer | — | — | — | — |
| 11 | Input 3 voltage | 0:Load First 1:Battery First 2:Grid First | — | — orage Power | — | — | — | — |
| 11 | Input 3 voltage | 0:Lead-acid 1:Lithium battery | — | — Storage Power | — | — | — | — |
| 12 | Input 3 Amperage | Aging mode Auto-cal command | — | — Storage Power | — | — | — | — |
| 12 | Input 3 Amperage | — | — | — reserved | — | — | — | — |
| 12 | Input 3 Amperage | PID PV 1 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | — | — |
| 12 | Input 3 Amperage | PID PV 1 PE Curr | — | — m A | — | — | — | — |
| 12 | Input 3 Amperage | PID PV 2 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | — | — |
| 12 | Input 3 Amperage | PID PV 2 PE Curr | — | — m A | — | — | — | — |
| 12 | Input 3 Amperage | PID PV 3 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | — | — |
| 13 | AC frequency | PID PV 3 PE Curr | — | — m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 4 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 4 PE Curr | — | — m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 5 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 5 PE Curr | — | — m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 6 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 6 PE Curr | — | — m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 7 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 7 PE Curr | — | — m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | AC frequency | PID PV 8 PE Volt/ Flyspan volta (MAX HV) | — | — V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 14 | Output 1 voltage | PID PV 8 PE Curr | — | — m A | — | — | — | — |
| 14 | Output 1 voltage | Bit 0~7:PID Working Status 1:Wait Status 2:Normal Status 3:Fault Status Bit 8~15:Reversed | — | — | — | — | — | — |
| 14 | Output 1 voltage | PV String 1 voltage | — | — V | — | — | — | — |
| 14 | Output 1 voltage | PV String 1 current | — | — A | — | — | — | — |
| 14 | Output 1 voltage | PV String 2 voltage | — | — V | — | — | — | — |
| 14 | Output 1 voltage | PV String 2 current | — | — | — | — | — | — |
| 14 | Output 1 voltage | PV String 3 voltage | — | — | — | — | — | — |
| 14 | Output 1 voltage | PV String 3 current | — | — | — | — | — | — |
| 14 | Output 1 voltage | PV String 4 voltage | — | — | — | — | — | — |
| 14 | Output 1 voltage | PV String 4 current | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 5 voltage | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 5 current | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 6 voltage | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 6 current | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 7 voltage | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 7 current | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 8 voltage | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 8 current | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 9 voltage | — | — | — | — | — | — |
| 15 | Input 4 voltage | PV String 9 current | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 10 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 10 current | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 11 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 11 current | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 12 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 12 current | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 13 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 13 current | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 14 voltage | — | — | — | — | — | — |
| 16 | Input 4 Amperage | PV String 14 current | — | — | — | — | — | — |
| 17 | Battery voltage | PV String 15 voltage | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | PV String 15 current | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | PV String 16 voltage | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | PV String 16 current | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | Bit 0~15: String 1~16 unmatch | — | — suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | Bit 0~15: String 1~16 current u | — | — suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | Bit 0~15: String 1~16 disconnec | — | — suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | Bit 0:Output over voltage Bit 1: ISO fault Bit 2: BUS voltage abnormal Bit 3~15:reserved | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | String Prompt Bit 0:String Unmatch Bit 1:Str Disconnect Bit 2:Str Current Unblance Bit 3~15:reserved | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | Battery voltage | PV Warning Value | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 18 | Output 2 voltage | DSP 075 Warning Value | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | ult DSP 075 Fault Value | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 1 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 2 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 3 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 4 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 5 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 6 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 7 | — | — | — | — | offgrid:soc | SOC |
| 18 | Output 2 voltage | g DSP 067 Debug Data 8 | — | — | — | — | offgrid:soc | SOC |
| 19 | Bus voltage | g DSP 075 Debug Data 1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 2 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 3 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 4 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 5 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 6 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 7 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | g DSP 075 Debug Data 8 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | USBAging Test Ok Flag 0-1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | Bus voltage | Flash Erase Aging Ok Flag 0-1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 20 | Grid voltage | PVISOValue | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | R DCI Curr | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | S DCI Curr | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | T DCI Curr | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | PIDBus Volt | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | GFCI Curr | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | SVG/APF Status+SVGAPFEqual Rat | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | R phase load side current for | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | S phase load side current for | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | T phase load side current for | — | — | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | AC frequency | R phase load side output reac power for SVG(High) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | R phase load side output reac power for SVG(low) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | S phase load side output reac power for SVG(High) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | S phase load side output reac power for SVG(low) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | T phase load side output reac power for SVG(High) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | T phase load side output reac power for SVG(low) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | R phase load side harmonic | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | S phase load side harmonic | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | T phase load side harmonic | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | R phase compensate reactive p for SVG(High) | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 22 | Output 1 voltage | R phase compensate reactive p for SVG(low) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate reactive p for SVG(High) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate reactive p for SVG(low) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate reactive p for SVG(High) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate reactive p for SVG(low) | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | R phase compensate harmonic f SVG | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | S phase compensate harmonic f SVG | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | T phase compensate harmonic f SVG | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | RS 232 Aging Test Ok Flag | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | Output 1 voltage | Bit 0: Fan 1 fault bit Bit 1: Fan 2 fault bit Bit 2: Fan 3 fault bit Bit 3: Fan 4 fault bit Bit 4-7: Reserved | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 23 | Input 6 voltage | Output apparent power H | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Output apparent power L | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Real Output Reactive Power H | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Real Output Reactive Power L | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Nominal Output Reactive Power | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Nominal Output Reactive Power | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Reactive power generation | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Reactive power generation | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | 0:Waiting 1:Self-check state 2:Detect pull arc state 3:Fault 4:Update | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | Input 6 voltage | Present FFTValue [CHANNEL_A] | — | — | — | — | offgrid:output_frequency | Output frequency |
| 24 | Input 6 Amperage | Present FFTValue [CHANNEL_B] | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 1 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 2 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | ug DSP 067 Debug Data 3 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 4 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 5 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 6 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 7 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | g DSP 067 Debug Data 8 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | Input 6 Amperage | — | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 87 | Input 8 energy today | PV 9 voltage | — | — | — | — | — | — |
| 87 | Input 8 energy today | PV 9 Input current | — | — | — | — | — | — |
| 87 | Input 8 energy today | PV 9 input power (High) | — | — | — | — | — | — |
| 87 | Input 8 energy today | PV 9 input power (Low) | — | — | — | — | — | — |
| 87 | Input 8 energy today | PV 10 voltage | — | — | — | — | — | — |
| 88 | 0 PV 10 Curr | PV 10 Input current | — | — | — | — | — | — |
| 88 | 1 Ppv 10 H | PV 10 input power (High) | — | — | — | — | — | — |
| 88 | 2 Ppv 10 L | PV 10 input power (Low) | — | — | — | — | — | — |
| 88 | 3 Vpv 11 | PV 11 voltage | — | — | — | — | — | — |
| 88 | 4 PV 11 Curr | PV 11 Input current | — | — | — | — | — | — |
| 88 | 5 Ppv 11 H | PV 11 input power (High) | — | — | — | — | — | — |
| 88 | 6 Ppv 11 L | PV 11 input power (Low) | — | — | — | — | — | — |
| 88 | 7 Vpv 12 | PV 12 voltage | — | — | — | — | — | — |
| 88 | 8 PV 12 Curr | PV 12 Input current | — | — | — | — | — | — |
| 88 | 9 Ppv 12 H | PV 12 input power (High) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 12 input power (Low) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 13 voltage | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 13 Input current | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 13 input power (High) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 13 input power (Low) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 14 voltage | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 14 Input current | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 14 input power (High) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 14 input power (Low) | — | — | — | — | — | — |
| 89 | Input 8 total energy | PV 15 voltage | — | — | — | — | — | — |
| 90 | 0 PV 15 Curr | PV 15 Input current | — | — | — | — | — | — |
| 90 | 1 Ppv 15 H | PV 15 input power (High) | — | — | — | — | — | — |
| 90 | 2 Ppv 15 L | PV 15 input power (Low) | — | — | — | — | — | — |
| 90 | 3 Vpv 16 | PV 16 voltage | — | — | — | — | — | — |
| 90 | 4 PV 16 Curr | PV 16 Input current | — | — | — | — | — | — |
| 90 | 5 Ppv 16 H | PV 16 input power (High) | — | — | — | — | — | — |
| 90 | 6 Ppv 16 L | PV 16 input power (Low) | — | — | — | — | — | — |
| 90 | 7 Epv 9_today H | PV 9 energy today (High) | — | — | — | — | — | — |
| 90 | 8 Epv 9_today L | PV 9 energy today (Low) | — | — | — | — | — | — |
| 90 | 9 Epv 9_total H | PV 9 energy total (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 9 energy total (Low) | — | — | — | — | — | — |
| 91 | Total energy input | PV 10 energy today (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 10 energy today (Low) | — | — | — | — | — | — |
| 91 | Total energy input | PV 10 energy total (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 10 energy total (Low) | — | — | — | — | — | — |
| 91 | Total energy input | PV 11 energy today (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 11 energy today (Low) | — | — | — | — | — | — |
| 91 | Total energy input | PV 11 energy total (High) | — | — | — | — | — | — |
| 91 | Total energy input | PV 11 energy total (Low) | — | — | — | — | — | — |
| 91 | Total energy input | PV 12 energy today (High) | — | — | — | — | — | — |
| 92 | 0 Epv 12_today L | PV 12 energy today (Low) | — | — | — | — | — | — |
| 92 | 1 Epv 12_total H | PV 12 energy total (High) | — | — | — | — | — | — |
| 92 | 2 Epv 12_total L | PV 12 energy total (Low) | — | — | — | — | — | — |
| 92 | 3 Epv 13_today H | PV 13 energy today (High) | — | — | — | — | — | — |
| 92 | 4 Epv 13_today L | PV 13 energy today (Low) | — | — | — | — | — | — |
| 92 | 5 Epv 13_total H | PV 13 energy total (High) | — | — | — | — | — | — |
| 92 | 6 Epv 13_total L | PV 13 energy total (Low) | — | — | — | — | — | — |
| 92 | 7 Epv 14_today H | PV 14 energy today (High) | — | — | — | — | — | — |
| 92 | 8 Epv 14_today L | PV 14 energy today (Low) | — | — | — | — | — | — |
| 92 | 9 Epv 14_total H | PV 14 energy total (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 14 energy total (Low) | — | — | — | — | — | — |
| 93 | Temperature | PV 15 energy today (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 15 energy today (Low) | — | — | — | — | — | — |
| 93 | Temperature | PV 15 energy total (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 15 energy total (Low) | — | — | — | — | — | — |
| 93 | Temperature | PV 16 energy today (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 16 energy today (Low) | — | — | — | — | — | — |
| 93 | Temperature | PV 16 energy total (High) | — | — | — | — | — | — |
| 93 | Temperature | PV 16 energy total (Low) | — | — | — | — | — | — |
| 93 | Temperature | PID PV 9 PE Volt/ Flyspan volta (MAX HV) | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | PID PV 9 PE Current | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | + PID PV 10 PE/ Flyspan voltage ( HV) | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 0+ PID PV 10 PE Current | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 1+ PID PV 11 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 1+ PID PV 11 PE Current | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 2+ PID PV 12 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 2+ PID PV 12 PE Current | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 3+ PID PV 13 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 3+ PID PV 13 PE Current | — | — | — | — | — | — |
| 94 | Intelligent Power Management temperature | 4+ PID PV 14 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 95 | Boost temperature | 4+ PID PV 14 PE Current | — | — | — | — | — | — |
| 95 | Boost temperature | 5+ PID PV 15 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 95 | Boost temperature | 5+ PID PV 15 PE Current | — | — | — | — | — | — |
| 95 | Boost temperature | 6+ PID PV 16 PE Volt/ Flyspan volt (MAX HV) | — | — | — | — | — | — |
| 95 | Boost temperature | 6+ PID PV 16 PE Current | — | — | — | — | — | — |
| 95 | Boost temperature | PV String 17 voltage | — | — | — | — | — | — |
| 95 | Boost temperature | PV String 17 Current | — | — | — | — | — | — |
| 95 | Boost temperature | PV String 18 voltage | — | — | — | — | — | — |
| 95 | Boost temperature | PV String 18 Current | — | — | — | — | — | — |
| 95 | Boost temperature | PV String 19 voltage | — | — | — | — | — | — |
| 96 | 0 Curr _String 19 | PV String 19 Current | — | — | — | — | — | — |
| 96 | 1 V _String 20 | PV String 20 voltage | — | — | — | — | — | — |
| 96 | 2 Curr _String 20 | PV String 20 Current | — | — | — | — | — | — |
| 96 | 3 V _String 21 | PV String 21 voltage | — | — | — | — | — | — |
| 96 | 4 Curr _String 21 | PV String 21 Current | — | — | — | — | — | — |
| 96 | 5 V _String 22 | PV String 22 voltage | — | — | — | — | — | — |
| 96 | 6 Curr _String 22 | PV String 22 Current | — | — | — | — | — | — |
| 96 | 7 V _String 23 | PV String 23 voltage | — | — | — | — | — | — |
| 96 | 8 Curr _String 23 | PV String 23 Current | — | — | — | — | — | — |
| 96 | 9 V _String 24 | PV String 24 voltage | — | — | — | — | — | — |
| 97 | 0 Curr _String 24 | PV String 24 Current | — | — 0.1 A | — | — | — | — |
| 97 | 1 V _String 25 | PV String 25 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 2 Curr _String 25 | PV String 25 Current | — | — 0.1 A | — | — | — | — |
| 97 | 3 V _String 26 | PV String 26 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 4 Curr _String 26 | PV String 26 Current | — | — 0.1 A | — | — | — | — |
| 97 | 5 V _String 27 | PV String 27 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 6 Curr _String 27 | PV String 27 Current | — | — 0.1 A | — | — | — | — |
| 97 | 7 V _String 28 | PV String 28 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 8 Curr _String 28 | PV String 28 Current | — | — 0.1 A | — | — | — | — |
| 97 | 9 V _String 29 | PV String 29 voltage | — | — 0.1 V | — | — | — | — |
| 98 | P-bus voltage | PV String 29 Current | — | — 0.1 A | — | — | — | — |
| 98 | P-bus voltage | PV String 30 voltage | — | — 0.1 V | — | — | — | — |
| 98 | P-bus voltage | PV String 30 Current | — | — 0.1 A | — | — | — | — |
| 98 | P-bus voltage | PV String 31 voltage | — | — 0.1 V | — | — | — | — |
| 98 | P-bus voltage | PV String 31 Current | — | — 0.1 A | — | — | — | — |
| 98 | P-bus voltage | PV String 32 voltage | — | — 0.1 V | — | — | — | — |
| 98 | P-bus voltage | PV String 32 Current | — | — 0.1 A | — | — | — | — |
| 98 | P-bus voltage | Bit 0~15: String 17~32 unmatch | — | — | — | — | — | — |
| 98 | P-bus voltage | Bit 0~15:String 17~32 unblance | — | — | — | — | — | — |
| 98 | P-bus voltage | Bit 0~15: String 17~32 disconn | — | — | — | — | — | — |
| 99 | N-bus voltage | PV Warning Value (PV 9-PV 16) Contains PV 9~16 abnormal, 和 Boost 9~16 Drive anomalies | — | — | — | — | — | — |
| 99 | N-bus voltage | string 1~string 16 abnormal | — | — | — | — | — | — |
| 99 | N-bus voltage | string 17~string 32 abnormal | — | — | — | — | — | — |
| 99 | N-bus voltage | M 3 to DSP system command | — | — system command | — | — | — | — |
| 10 | 00. uw Sys Work Mode | System work mode | — | — Theworkingmode displayed by the monitoring to the customer is: 0 x 00: waiting module 0 x 01: Self-test mode, 0 x 03:fault module 0 x 04:flash odule x 05|0 x 06|0 x 07|0 08:normal odule | — | — | — | — |
| 10 | 01. Systemfault word 0 | System fault word 0 | — | — lease refer to hefault escription of ybrid | — | — | — | — |
| 10 | 02. Systemfault word 1 | System fault word 1 | — | — | — | — | — | — |
| 10 | 03. Systemfault word 2 | System fault word 2 | — | — | — | — | — | — |
| 10 | 04. Systemfault word 3 | System fault word 3 | — | — | — | — | — | — |
| 10 | 05. Systemfault word 4 | System fault word 4 | — | — | — | — | — | — |
| 10 | 06. Systemfault word 5 | System fault word 5 | — | — | — | — | — | — |
| 10 | 07. Systemfault word 6 | System fault word 6 | — | — | — | — | — | — |
| 10 | 08. Systemfault word 7 | System fault word 7 | — | — | — | — | — | — |
| 10 | 09. Pdischarge 1 H | Discharge power(high) | — | — | — | — | — | — |
| 10 | 10. Pdischarge 1 L | Discharge power (low) | — | — | — | — | — | — |
| 10 | 11. Pcharge 1 H | Charge power(high) | — | — | — | — | — | — |
| 10 | 12. Pcharge 1 L | Charge power (low) | — | — | — | — | — | — |
| 10 | 13. Vbat | Battery voltage | — | — | — | — | — | — |
| 10 | 14. SOC | State of charge Capacity | — | — ith/leadacid | — | — | — | — |
| 10 | 15. Pactouser R | H AC power to user H | — | — | — | — | — | — |
| 10 | 16. Pactouser R | L AC power to user L | — | — | — | — | — | — |
| 10 | 17. Pactouser S | H Pactouser S H | — | — | — | — | — | — |
| 10 | 18. Pactouser S | L Pactouser S L | — | — | — | — | — | — |
| 10 | 19. Pactouser T | H Pactouser T H | — | — | — | — | — | — |
| 10 | 20. Pactouser T | L Pactouser T H | — | — | — | — | — | — |
| 10 | 21. Pactouser Total H | AC power to user total H | — | — | — | — | — | — |
| 10 | 22. Pactouser Total L | AC power to user total L | — | — | — | — | — | — |
| 10 | 23. Pac to grid R H | AC power to grid H | — | — c output | — | — | — | — |
| 10 | 24. Pac to grid R L | AC power to grid L | — | — | — | — | — | — |
| 10 | 25. Pactogrid S H | — | — | — | — | — | — | — |
| 10 | 26. Pactogrid S L | — | — | — | — | — | — | — |
| 10 | 27. Pactogrid T H | — | — | — | — | — | — | — |
| 10 | 28. Pactogrid T L | — | — | — | — | — | — | — |
| 10 | 29. Pactogrid total H | AC power to grid total H | — | — | — | — | — | — |
| 10 | 30. Pactogrid total L | AC power to grid total L | — | — | — | — | — | — |
| 10 | 31. PLocal Load R | H INV power to local load H | — | — | — | — | — | — |
| 10 | 32. PLocal Load R | L INV power to local load L | — | — | — | — | — | — |
| 10 | 33. PLocal Load S | H | — | — | — | — | — | — |
| 10 | 34. PLocal Load S | L | — | — | — | — | — | — |
| 10 | 35. PLocal Load T H | — | — | — | — | — | — | — |
| 10 | 36. PLocal Load T L | — | — | — | — | — | — | — |
| 10 | 37. PLocal Load total | H INV power to local load tot | — | — | — | — | — | — |
| 10 | 38. PLocal Load total | L INV power to local load tot L | — | — | — | — | — | — |
| 10 | 39. IPM 2 Temperature | REC Temperature | — | — | — | — | — | — |
| 10 | 40. Battery 2 Temperature | Battery Temperature | — | — ithium p | — | — | — | — |
| 10 | 41. SP DSP Status | SP state | — | — | — | — | — | — |
| 10 | 42. SP Bus Volt | SP BUS 2 Volt | — | — | — | — | — | — |
| 10 | 43 | — | — | — | — | — | — | — |
| 10 | 44. Etouser_today H | Energy to user today high | — | — | — | — | — | — |
| 10 | 45. Etouser_today L | Energy to user today low | — | — | — | — | — | — |
| 10 | 46. Etouser_total H | Energy to user total high | — | — | — | — | — | — |
| 10 | 47. Etouser_ total L | Energy to user total high | — | — | — | — | — | — |
| 10 | 48. Etogrid_today H | Energy to grid today high | — | — | — | — | — | — |
| 10 | 49. Etogrid _today L | Energy to grid today low | — | — | — | — | — | — |
| 10 | 50. Etogrid _total H | Energy to grid total high | — | — | — | — | — | — |
| 10 | 51. Etogrid _ total L | Energy to grid total high | — | — | — | — | — | — |
| 10 | 52. Edischarge 1_toda y H | Discharge energy 1 today | — | — | — | — | — | — |
| 10 | 53. Edischarge 1_toda y L | Discharge energy 1 today | — | — | — | — | — | — |
| 10 | 54. Edischarge 1_total H | Total discharge energy 1 (high) | — | — | — | — | — | — |
| 10 | 55. Edischarge 1_total L | Total discharge energy 1 (low) | — | — | — | — | — | — |
| 10 | 56. Echarge 1_today H | Charge 1 energy today | — | — | — | — | — | — |
| 10 | 57. Echarge 1_today L | Charge 1 energy today | — | — | — | — | — | — |
| 10 | 58. Echarge 1_total H | Charge 1 energy total | — | — | — | — | — | — |
| 10 | 59. Echarge 1_total L | Charge 1 energy total | — | — | — | — | — | — |
| 10 | 60. ELocal Load_Today H | Local load energy today | — | — | — | — | — | — |
| 10 | 61. ELocal Load_Today L | Local load energy today | — | — | — | — | — | — |
| 10 | 62. ELocal Load_Total H | Local load energy total | — | — | — | — | — | — |
| 10 | 63. ELocal Load_Total L | Local load energy total | — | — | — | — | — | — |
| 10 | 64. dw Export Limit Ap parent Power | Export Limit Apparent Power H | — | — rent Power | — | — | — | — |
| 10 | 65. dw Export Limit Ap parent Power | Export Limit Apparent Power L | — | — rent Power | — | — | — | — |
| 10 | 66. / | / | — | — rved | — | — | — | — |
| 10 | 67. EPS Fac | UPSfrequency | — | — | — | — | — | — |
| 10 | 68. EPS Vac 1 | UPS phase R output voltage | — | — | — | — | — | — |
| 10 | 69. EPS Iac 1 | UPS phase R output current | — | — | — | — | — | — |
| 10 | 70. EPS Pac 1 H | UPS phase R output power (H) | — | — | — | — | — | — |
| 10 | 71. EPS Pac 1 L | UPS phase R output power (L) | — | — | — | — | — | — |
| 10 | 72. EPS Vac 2 | UPS phase S output voltage | — | — | — | — | — | — |
| 10 | 73. EPS Iac 2 | UPS phase S output current | — | — se | — | — | — | — |
| 10 | 74. EPS Pac 2 H | UPS phase S output power (H) | — | — | — | — | — | — |
| 10 | 75. EPS Pac 2 L | UPS phase S output power (L) | — | — | — | — | — | — |
| 10 | 76. EPS Vac 3 | UPS phase T output voltage | — | — | — | — | — | — |
| 10 | 77. EPS Iac 3 | UPS phase T output current | — | — se | — | — | — | — |
| 10 | 78. EPS Pac 3 H | UPS phase T output power (H) | — | — | — | — | — | — |
| 10 | 79. EPS Pac 3 L | UPS phase T output power (L) | — | — | — | — | — | — |
| 10 | 80. Loadpercent | Load percent of UPS ouput | — | — | — | — | — | — |
| 10 | 81. PF | Power factor | — | — ary Value+1 | — | — | — | — |
| 10 | 82. BMS_Status Old | Status Old from BMS | — | — | — | — | — | — |
| 10 | 83. BMS_Status | Status from BMS | — | — | — | — | — | — |
| 10 | 84. BMS_Error Old | Error info Old from BMS | — | — | — | — | — | — |
| 10 | 85. BMS_Error | Errorinfomation from BMS | — | — | — | — | — | — |
| 10 | 86. BMS_SOC BMS_Battery Vol | SOC from BMS Battery voltage from BMS | — | — H 6 K H 6 K | — | — | — | — |
| 10 | 87. t BMS_Battery Cur | Battery current from BMS | — | — | — | — | — | — |
| 10 | 88. r BMS_Battery Te | Battery temperature from BMS | — | — | — | — | — | — |
| 10 | 89. mp BMS_Max Curr | Max. charge/discharge current | — | — | — | — | — | — |
| 10 | 90. | from BMS (pylon) | — | — | — | — | — | — |
| 10 | 91. BMS_Gauge RM | Gauge RM from BMS | — | — | — | — | — | — |
| 10 | 92. BMS_Gauge FCC | Gauge FCC from BMS | — | — | — | — | — | — |
| 10 | 93. BMS_FW | — | — | — | — | — | — | — |
| 10 | 94. BMS_Delta Volt | Delta V from BMS | — | — | — | — | — | — |
| 10 | 95. BMS_Cycle Cnt | Cycle Count from BMS | — | — | — | — | — | — |
| 10 | 96. BMS_SOH BMS_Constant V | SOH from BMS CV voltage from BMS | — | — | — | — | — | — |
| 10 | 97. olt BMS_Warn Info O | Warning info old from BMS | — | — | — | — | — | — |
| 10 | 98. ld | — | — | — | — | — | — | — |
| 10 | 99. BMS_Warn Info BMS_Gauge ICCu | Warning info from BMS Gauge IC current from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | MCU Software version from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Gauge Version from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Gauge FR Version L 16 from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Gauge FR Version H 16 from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | — | — | — | — | — | — | — |
| 11 | Input 3 voltage | BMSInformation from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Pack Information from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Using Cap from BMS | — | — | — | — | — | — |
| 11 | Input 3 voltage | Maximum single battery voltage | — | — | — | — | — | — |
| 11 | Input 3 voltage | Lowest single battery voltage | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery parallel number | — | — | — | — | — | — |
| 11 | Input 3 voltage | Number of batteries Max Volt Cell No | — | — | — | — | — | — |
| 11 | Input 3 voltage | Min Volt Cell No | — | — | — | — | — | — |
| 11 | Input 3 voltage | Max Tempr Cell_10 T | — | — | — | — | — | — |
| 11 | Input 3 voltage | Min Tempr Cell_10 T | — | — | — | — | — | — |
| 11 | Input 3 voltage | Max Volt Tempr Cell No | — | — | — | — | — | — |
| 11 | Input 3 voltage | — | — | — | — | — | — | — |
| 11 | Input 3 voltage | Min Volt Tempr Cell No | — | — | — | — | — | — |
| 11 | Input 3 voltage | Faulty Battery Address | — | — | — | — | — | — |
| 11 | Input 3 voltage | Parallel maximum SOC | — | — | — | — | — | — |
| 11 | Input 3 voltage | Parallel minimum SOC Battery Protection 2 | — | — CAN ID: 0 x 323 | — | — | — | — |
| 11 | Input 3 voltage | Battery Protection 3 | — | — Byte 4~5 CAN ID: 0 x 323 | — | — | — | — |
| 11 | Input 3 voltage | Battery Warn 2 | — | — Byte 6 CAN ID: 0 x 323 | — | — | — | — |
| 11 | Input 3 voltage | — | — | — Byte 7 | — | — | — | — |
| 11 | Input 3 voltage | AC Charge Energy today | — | — Energy today | — | — | — | — |
| 11 | Input 3 voltage | AC Charge Energy today | — | — | — | — | — | — |
| 11 | Input 3 voltage | — | — | — Energy total | — | — | — | — |
| 11 | Input 3 voltage | — | — | — | — | — | — | — |
| 11 | Input 3 voltage | AC Charge Power | — | — | — | — | — | — |
| 11 | Input 3 voltage | AC Charge Power | — | — | — | — | — | — |
| 11 | Input 3 voltage | uw Grid Power_70_Adj EE_SP | — | — | — | — | — | — |
| 11 | Input 3 voltage | tra inverte AC Power to grid gh | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | trainverte AC Power to grid Low | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr today (high) | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr today (low) | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr total(high) | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | Extra inverter Power TOUser_Extr total(low) | — | — SPA used | — | — | — | — |
| 11 | Input 3 voltage | System electric energy today H | — | — SPA used System electric energy today H | — | — | — | — |
| 11 | Input 3 voltage | stem electric energy today L | — | — d electric today L | — | — | — | — |
| 11 | Input 3 voltage | System electric energy total H | — | — d electric total H | — | — | — | — |
| 11 | Input 3 voltage | System electric energy total L | — | — d electric total L | — | — | — | — |
| 11 | Input 3 voltage | self electric energy today H | — | — electric today H | — | — | — | — |
| 11 | Input 3 voltage | self electric energy today L | — | — electric today L | — | — | — | — |
| 11 | Input 3 voltage | self electric energy total H | — | — electric total H | — | — | — | — |
| 11 | Input 3 voltage | self electric energy total L | — | — electric total L | — | — | — | — |
| 11 | Input 3 voltage | System power H | — | — power H | — | — | — | — |
| 11 | Input 3 voltage | System power L | — | — power L | — | — | — | — |
| 11 | Input 3 voltage | self power H | — | — wer H | — | — | — | — |
| 11 | Input 3 voltage | self power L | — | — wer L | — | — | — | — |
| 11 | Input 3 voltage | PV electric energy today H | — | — | — | — | — | — |
| 11 | Input 3 voltage | PV electric energy today L | — | — | — | — | — | — |
| 11 | Input 3 voltage | Discharge power pack number | — | — | — | — | — | — |
| 11 | Input 3 voltage | Cumulative discharge power high 16-bit byte | — | — | — | — | — | — |
| 11 | Input 3 voltage | Cumulative discharge power low 16-bit byte | — | — | — | — | — | — |
| 11 | Input 3 voltage | charge power pack serial number | — | — | — | — | — | — |
| 11 | Input 3 voltage | Cumulative charge power high R 16-bit byte | — | — | — | — | — | — |
| 11 | Input 3 voltage | Cumulative charge power low R 16-bit byte | — | — | — | — | — | — |
| 11 | Input 3 voltage | First Batt Fault Sn | — | — | — | — | — | — |
| 11 | Input 3 voltage | Second Batt Fault Sn | — | — | — | — | — | — |
| 11 | Input 3 voltage | Third Batt Fault Sn | — | — | — | — | — | — |
| 11 | Input 3 voltage | Fourth Batt Fault Sn | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 1 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 2 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 3 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 4 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 5 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 6 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 7 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Battery history fault code 8 | — | — | — | — | — | — |
| 11 | Input 3 voltage | Number of battery codes PACK number + BIC forward and reverse codes | — | — | — | — | — | — |
| 11 | Input 3 voltage | — | — | — | — | — | — | — |
| 11 | Input 3 voltage | Intelligent reading is used to identify software compatibility features | — | — rgy; rgy | — | — | — | — |
| 1 | Input 1 voltage | Maximum cell voltage | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Minimum cell voltage | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Number of Battery modules | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Total number of cells | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Max Volt Cell No | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Min Volt Cell No | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Max Tempr Cell_10 T | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Min Tempr Cell_10 T | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Max Tempr Cell No | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Min Tempr Cell No | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Fault Pack ID | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Parallel maximum SOC | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Parallel minimum SOC | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Bat Protect 1 Add | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Bat Protect 2 Add | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | Bat Warn 1 Add | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Highest Soft Version | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Hardware Version | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | Input 1 voltage | BMS_Request Type | — | — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 12 | Input 3 Amperage | Success sign of key detection before aging | — | — 1:Finished test 0: test not completed | — | — | — | — |
| 12 | Input 3 Amperage | / | — | — reversed | — | — | — | — |
| 20 | Grid voltage | Inverter run state | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Output power (high) | — | — 1 W SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Output power (low) | — | — 1 W SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Grid frequency | — | — 01 Hz SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Three/single phase grid voltage | — | — 1 V SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Three/single phase grid output | — | — 1 A SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Three/single phase grid output VA (high) | — | — 1 VA SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Three/single phase grid output VA(low) | — | — 1 VA SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Today generate energy (high) | — | — 1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Today generate energy (low) | — | — 1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Total generate energy (high) | — | — WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Total generate energy (low) | — | — WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Work time total (high) | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Work time total (low) | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Inverter temperature | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | The inside IPM in inverter Temp | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Boost temperature | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | — | — | — reserved | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | Bat Volt_DSP | — | — Bat Volt(DSP) | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | P Bus inside Voltage | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | Grid voltage | N Bus inside Voltage | — | — SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | AC frequency | / | — | — Remote setup enable | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | / | — | — Remotely set power | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extra inverte AC Power to grid | — | — SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extrainverte AC Power to grid L | — | — SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extra inverter Power TOUser_Extr today (high) | — | — Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extra inverter Power TOUser_Extr today (low) | — | — Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extra inverter Power TOUser_Extratotal(high) | — | — Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Extra inverter Power TOUser_Extr total(low) | — | — Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | System electric energy today H | — | — Wh SPA used System electric energy today H | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | stem electric energy today L | — | — Wh SPA used System electric energy today L | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | System electric energy total H | — | — Wh SPA used System c total | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | System electric energy total L | — | — d c total | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | ACCharge energy today | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | ACCharge energy today | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | ACCharge energy total | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | ACCharge energy total | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Grid power to local load | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Grid power to local load | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | 0:Load First 1:Battery First 2:Grid First | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | 0:Lead-acid 1:Lithium battery | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | Aging mode | — | — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | AC frequency | — | — | — d | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 3 | Input 1 Wattage | 2: Reserved 3:Sys Fault module 4: Flash module 5:PVBATOnline module: 6:Bat Online module 7:PVOffline Mode 8:Bat Offline Mode The lower 8 bits indicate the m status (web page display) 0: Standby Status; 1: Normal Status; 3: Fault Status 4:Flash Status; | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV total power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 1 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 1 input current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 1 power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 2 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 2 input current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 2 power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 3 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 3 input current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 3 power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 4 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 4 input current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 4 power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | System output power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | reactive power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Output power | — | — ut | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Grid frequency | — | — r | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three/single phase grid voltage | — | — uency e/single | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — e grid age | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three/single phase grid output | — | — e/single rid | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three/single phase grid output VA | — | — ingle rid | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — watt hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid output current | — | — ltage hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid output power | — | — hase tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid output current | — | — ltage hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid output power | — | — hase tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Three phase grid voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total forward power | — | — orward | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total reverse power | — | — everse | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total load power | — | — load | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Work time total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today generate energy | — | — e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total generate energy | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 1 energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 1 energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 2 energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 2 energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 3 energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 3 energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today energy to user | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy to user | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today energy to grid | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy to grid | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today energy of user load | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy of user load | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 4 energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV 4 energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Derating Mode | — | — h | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — k T l A i | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | PV ISO value | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | R DCI Curr | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | S DCI Curr | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | T DCI Curr | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | GFCI Curr | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | total bus voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter temperature | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | The inside IPM in inverter temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Boost temperature | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Reserved | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Commmunication broad temperatur | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | P Bus inside Voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | N Bus inside Voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter output PF now | — | — 000 | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Real Output power Percent | — | — 0 | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Output Maxpower Limited | — | — ut ower | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter standby flag | — | — ted:turn off r;:PV Low;:AC | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — /Freq of scope; ~bit 7: rved | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter fault maincode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter Warning maincode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter fault subcode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Inverter Warning subcode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Present FFTValue [CHANNEL_A] | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | AFCI Status | — | — waiting e lf-check Detection | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | AFCI Strength[CHANNEL_A] | — | — arcing e ult state update e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | AFCI Self Check[CHANNEL_A] | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | inv start delay time | — | — lay | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BDC connect state | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Current status of Dry Contact | — | — of | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | self-use power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | System energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today discharge energy | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total discharge energy | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Charge energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Charge energy total | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today energy of AC charge | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy of AC charge | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy of system outpu | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Today energy of Self output | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total energy of Self output | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Word Mode | — | — ad First | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — ery Firs id First | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS frequency | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase R output voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase R output current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase R output power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase S output voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase S output current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase S output power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase T output voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase T output current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS phase T output power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | UPS output power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Load percent of UPS ouput | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Power factor | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | DC voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Whether to parse BDC data separ | — | — on't need | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BDCDerating Mode: 0: Normal, unrestricted 1:Standby or fault | — | — ed | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | 2:Maximum battery current limit (discharge) 3:Battery discharge Enable (Dis 4:High bus discharge derating (discharge) 5:High temperature discharge derating (discharge) 6:System warning No discharge (discharge) 7-15 Reserved (Discharge) 16:Maximum charging current of battery (charging) 17:High Temperature (LLC and Buckboost) (Charging) 18:Final soft charge 19:SOC setting limits (charging 20:Battery low temperature (cha 21:High bus voltage (charging) 22:Battery SOC (charging) 23: Need to charge (charge) 24: System warning not charging (charging) 25-29:Reserve (charge) System work State and mode The upper 8 bits indicate the mode; 0:No charge and discharge; 1:charge; 2:Discharge; | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | The lower 8 bits represent the 0: Standby Status; 1: Normal Status; 2: Fault Status 3:Flash Status; | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Storge device fault code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Storge device warning code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Battery voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Battery current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | State of charge Capacity | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Total BUS voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | On the BUS voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BUCK-BOOST Current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | LLC Current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Temperture A | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Temperture B | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Discharge power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Charge power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Discharge total energy of storg | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Charge total energy of storge d | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Reserved BDC mark (charge and dischar fault alarm code) Bit 0: Charge En; BDC allows char Bit 1: Discharge En; BDC allows discharge | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bit 2~7: Resvd; reserved Bit 8~11: Warn Sub Code; BDC sub-warning code Bit 12~15: Fault Sub Code; BDC sub-error code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Lower BUS voltage Bms Max Volt Cell No | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Min Volt Cell No | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Max Cell Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Max Cell Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Battery Avg Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Max SOC | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Min SOC Parallel Battery Num | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Derate Reason | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Gauge FCC(Ah) | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Bms Gauge RM(Ah) | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Protect 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMSWarn 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Fault 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Fault 2 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Battery ISO detection status | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | battery work request | — | — n | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | battery working status | — | — mancy ge harge | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — dby start t te | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Protect 2 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Warn 2 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS SOC BMS Battery Volt | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Battery Curr | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | battery cell maximum temperatur | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Maximum charging current Maximum discharge current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMSCycle Cnt | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS SOH Battery charging voltage limit | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | Battery discharge voltage limit | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Warn 3 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | BMS Protect 3 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | Input 1 Wattage | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 32 | Input 8 Amperage | — | — | — | — | — | — | — |
| 32 | Input 8 Amperage | BMS Battery Single Volt Max | — | — | — | — | — | — |
| 32 | Input 8 Amperage | BMS Battery Single Volt Min | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Battery Load Volt | — | — 0,650.00] | — | — | — | — |
| 32 | Input 8 Amperage | — | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 1 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 2 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 3 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 4 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 5 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 6 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 7 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 8 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 9 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 10 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 10 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 12 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 13 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 14 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 15 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Debug data 16 | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 output power H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 output power L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 output power H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 output power L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 energy Today H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 energy Today L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 energy Today H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 energy Today L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 energy Total H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 1 energy Total L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 energy Total H | — | — | — | — | — | — |
| 32 | Input 8 Amperage | PV inverter 2 energy Total L | — | — | — | — | — | — |
| 32 | Input 8 Amperage | battery pack number | — | — C reports e updated ery 15 nutes | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[0] | — | — C reports e updated | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[2] | — | — ery 15 | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[4] | — | — nutes | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[6] | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[8] | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[10]SN[11] | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[12]SN[13] | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Battery pack serial number SN[14]SN[15] | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Reserve | — | — | — | — | — | — |
| 32 | Input 8 Amperage | — | — | — | — | — | — | — |
| 32 | Input 8 Amperage | Clear day data flag | — | — ta of the rrent day at the rver determines whether to clear. 0:not cleared. 1: Clear. | — | — | — | — |
| 40 | Fault code | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | — | — |
| 41 | Intelligent Power Management temperature | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | — | — |
| 41 | Intelligent Power Management temperature | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | — | — |
| 42 | Fault code | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | offgrid:fault_code | Fault code |
| 48 | Input 1 energy today | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 49 | 71 | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | — | — |
| 49 | 72- 10 | The first 8 registers are the 1 | — | — en 69 registers have the | — | — | — | — |
| 50 | Input 1 total energy | same data area as 3165-3233, th 108 registers (including 8 regi | — | — eserved, a total of r). | — | — | offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |

