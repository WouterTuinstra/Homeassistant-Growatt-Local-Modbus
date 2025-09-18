# Growatt Modbus Register Map (Protocol v1.24)

This file is generated from `growatt_registers_spec.json` (parsed from the official Modbus RTU protocol) and cross-references the Home Assistant `growatt_local` integration.

**Legend**: Access = spec write flag (`R`, `W`, `R/W`). “Range/Unit” merges the spec range column with the unit, when available. “Attributes” lists the integration attribute(s) mapped to the register; “Sensors” lists Home Assistant sensor entities exposing the attribute. Rows without attributes are not currently surfaced by the integration (typically configuration or reserved registers).

*Descriptions and notes are copied verbatim from the PDF specification. Some spacing may appear collapsed due to automated extraction; consult the original document when exact phrasing is required.*

## Coverage Summary
| Section | Spec Registers | Covered | Missing |
| --- | --- | --- | --- |
| Common Holding Registers (0–124) | 125 | 8 | 117 |
| TL-X/TL-XH Holding Registers (3000–3124) | 109 | 0 | 109 |
| TL-XH US Holding Registers (3125–3249) | 64 | 0 | 64 |
| TL3/MAX/MID/MAC Holding Registers (125–249) | 108 | 0 | 108 |
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
| 00 | On Off | Remote On/Off . On(1);Off(0)Inverter On(3) ;Off(2)BDC | W | 0, 1, 2, 3 — | 1 | The inverter can be switched on and off, and the BDC can be switched on and off for the batt ready function. | tlx:inverter_enabled, tl3:inverter_enabled | — |
| 01 | Safty Func En Bit Bit Bit Bit Ena Bit Bit Bit Ena Bit Bit Bit Fre Ena | 0: SPI enable 1: Auto Test Start 2: LVFRT enable 3:Freq Derating ble 4: Softstart enable 5: DRMS enable 6:Power Volt Func ble 7: HVFRT enable 8:ROCOF enable 9: Recover q Derating Mode ble Bit 10:Split phase enable Bit 10~15:预留 | W | 0 : disable 1: enable — | — | SPI: system protection interface Bit 0~3:for CEI 0-21 Bit 4~6:for SAA | — | — |
| 02 | PF CMD Set memory regis state will not(1 setti initi | Holding ter 3,4,5,99 CMD be memory or /0), if not, these ngs are the al value. | W | 0 or 1 — | 0 | Means these settings will be acting or not when next power on | — | — |
| 03 | Active P I Rate a | nverter Max output ctive power percent | W | 0-100 or % 255 — | 255 | 255: power is not be limited | — | — |
| 04 | Reactive P Rate | Inverter max output reactive power percent | W | -100-100 % or 255 — | 255 | 255: power is not be limited | — | — |
| 05 | Power factor In fa | verter output power ctor’s 10000 times | W | 0-20000, 0-10000 is underexci ted, other is overexcit ed — | 0 | — | — | — |
| 06 | Pmax H | Normal power (high) | — | 0.1 VA — | — | — | — | — |
| 07 | Pmax L | Normal power (low) | — | 0.1 VA — | — | — | — | — |
| 08 | Vnormal | Normal work PV voltage | — | 0.1 V — | — | — | — | — |
| 09 | Fw version H Fi (h | rmware version igh) | — | ASCII — | — | — | tlx:firmware, tl3:firmware, storage:firmware | — |
| 10 | Fw version F M ( | irmware version middle) | — | — | — | — | — | — |
| 11 | Fw version L Fi | rmware version (low) | — | — | — | — | — | — |
| 12 | Fw version 2 Con H ver | trol Firmware sion (high) | — | ASCII — | — | — | — | — |
| 13 | Fw version 2 Con M ver | trol Firmware sion (middle) | — | — | — | — | — | — |
| 14 | Fw version 2 Con L ver | trol Firmware sion (low) | — | — | — | — | — | — |
| 15 | LCD language | LCD language | W | 0-5 — | — | 0: Italian; 1: English; 2: German; 3: Spanish; 4: French; 5: Chinese; 6:Polish 7:Portugues 8:Hungary | — | — |
| 16 | Country Sele Cou cted not | ntry Selected or | W | 0: need to select; 1: have selected — | — | — | — | — |
| 17 | Vpv start | Input start voltage | W | 0.1 V — | — | — | — | — |
| 18 | Time start | Start time | W | 1 s — | — | — | — | — |
| 19 | Restart Delay Re Time af | start Delay Time ter fault back; | W | 1 s — | — | — | — | — |
| 20 | w Power Start Pow Slope | er start slope W | 1- | 1000 0.1% — | — | — | — | — |
| 21 | w Power Rest Powe art Slope EE | r restart slope W | 1- | 1000 0.1% — | — | — | — | — |
| 22 | w Select Baud Sel rate com e 0: 1:3 | ect W municationbaudrat 9600 bps 8400 bps | 0- | 1 0 — | — | — | — | — |
| 23 | Serial NO | Serial number 1-2 | — | ASCII — | — | — | tlx:serial number, tl3:serial number | — |
| 24 | Serial NO | Serial number 3-4 | — | — | — | — | — | — |
| 25 | Serial NO | Serial number 5-6 | — | — | — | — | — | — |
| 26 | Serial NO | Serial number 7-8 | — | — | — | — | — | — |
| 27 | Serial NO | Serial number 9-10 | — | — | — | — | — | — |
| 28 | Module H | Inverter Module (high) | &* | 5 — | — | — | tlx:Inverter model, tl3:Inverter model, storage:Inverter model | — |
| 29 | Module L | Inverter Module (low) | &* | 5 — | — | — | — | — |
| 30 | Com Address | Communicate address W | 1- | 254 1 — | — | — | — | — |
| 31 | Flash Start | Update firmware W | 1 | — | — | — | — | — |
| 32 | Reset User Info | Reset User Information W | 0x | 0001 — | — | — | — | — |
| 33 | Reset to factory | Reset to factory W | 0x | 0001 — | — | — | — | — |
| 34 | Manufacture Man r Info 8 inf | ufacturer ormation (high) | — | ASCII — | — | — | — | — |
| 35 | Manufacture Man r Info 7 inf | ufacturer ormation (middle) | — | — | — | — | — | — |
| 36 | Manufacture Man r Info 6 inf | ufacturer ormation (low) | — | — | — | — | — | — |
| 37 | Manufacture Man r Info 5 inf | ufacturer ormation (high) | — | — | — | — | — | — |
| 38 | Manufacture Man r Info 4 inf | ufacturer ormation (middle) | — | — | — | — | — | — |
| 39 | Manufacture Man r Info 3 inf | ufacturer ormation (low) | — | — | — | — | — | — |
| 40 | Manufacture Man r Info 2 inf | ufacturer ormation (low) | — | — | — | — | — | — |
| 41 | Manufacture Man r Info 1 inf | ufacturer ormation (high) | — | — | — | — | — | — |
| 42 | bfailsafe En; G 1 | 00 fail safe W | En Di | able:1 sable:0 — | Engli | sh G 100 fail safe set | — | — |
| 43 | DTC | Device Type Code | &* | 6 — | — | — | tlx:device type code, tl3:device type code, storage:device type code | — |
| 44 | TP | Input tracker num and output phase num | — | Eg:0 x 020 3 is two MPPT and 3 ph output — | — | — | tlx:number of trackers and phases, tl3:number of trackers and phases, storage:number of trackers and phases | — |
| 45 | Sys Year | System time-year | W | Year offset is 0 — | Loc | al time | — | — |
| 46 | Sys Month | System time- Month | W | — | — | — | — | — |
| 47 | Sys Day | System time- Day | W | — | — | — | — | — |
| 48 | Sys Hour | System time- Hour | W | — | — | — | — | — |
| 49 | Sys Min | System time- Min | W | — | — | — | — | — |
| 50 | Sys Sec | System time- Second | W | — | — | — | — | — |
| 51 | Sys Weekly | System Weekly | W | 0-6 — | — | — | — | — |
| 52 | Vac low | Grid voltage low limit protect | W | 0.1 V — | — | — | — | — |
| 53 | Vac high | Grid voltage high limit protect | W | 0.1 V — | — | — | — | — |
| 54 | Fac low | Grid frequency low limit protect | W | 0.01 Hz — | — | — | — | — |
| 55 | Fac high | Grid high frequencylimit protect | W | 0.01 Hz — | — | — | — | — |
| 56 | Vac low 2 | Grid voltage low limit protect 2 | W | 0.1 V — | — | — | — | — |
| 57 | Vac high 2 | Grid voltage high limit protect 2 | W | 0.1 V — | — | — | — | — |
| 58 | Fac low 2 | Grid frequency low limit protect 2 | W | 0.01 Hz — | — | — | — | — |
| 59 | Fac high 2 | Grid high frequency limit protect 2 | W | 0.01 Hz — | — | — | — | — |
| 60 | Vac low 3 | Grid voltage low limit protect 3 | W | 0.1 V — | — | — | — | — |
| 61 | Vac high 3 | Grid voltage high limit protect 3 | W | 0.1 V — | — | — | — | — |
| 62 | Fac low 3 | Grid frequency low limit protect 3 | W | 0.01 Hz — | — | — | — | — |
| 63 | Fac high 3 | Grid frequency high limit protect 3 | W | 0.01 Hz — | — | — | — | — |
| 64 | Vac low C | Grid low voltage limit connect to Grid | W | 0.1 V — | — | — | — | — |
| 65 | Vac high C | Grid high voltage limit connect to Grid | W | 0.1 V — | — | — | — | — |
| 66 | Fac low C | Grid low frequency limit connect to Grid | W | 0.01 Hz — | — | — | — | — |
| 67 | Fac high C | Grid high frequency limit connect to Grid | W | 0.01 Hz — | — | — | — | — |
| 68 | Vac low 1 G time p | rid voltage low limit rotect time 1 | W | Cycle — | — | — | — | — |
| 69 | Vac high 1 G time p | rid voltage high limit rotect time 1 | W | Cycle — | — | — | — | — |
| 70 | Vac low 2 G time p | rid voltage low limit rotect time 2 | W | Cycle — | — | — | — | — |
| 71 | Vac high 2 G time p | rid voltage high limit rotect time 2 | W | Cycle — | — | — | — | — |
| 72 | Fac low 1 G time l | rid frequency low imit protect time 1 | W | Cycle — | — | — | — | — |
| 73 | Fac high 1 G time l | rid frequency high imit protect time 1 | W | Cycle — | — | — | tl3:modbus version | — |
| 74 | Fac low 2 G time l | rid frequency low imit protect time 2 | W | Cycle — | — | — | — | — |
| 75 | Fac high 2 G time l | rid frequency high imit protect time 2 | W | Cycle — | — | — | — | — |
| 76 | Vac low 3 G time p | rid voltage low limit rotect time 3 | W | Cycle — | — | — | — | — |
| 77 | Vac high 3 G time p | rid voltage high limit rotect time 3 | W | Cycle — | — | — | — | — |
| 78 | Fac low 3 G time l | rid frequency low imit protect time 3 | W | Cycle — | — | — | — | — |
| 79 | Fac high 3 G time l | rid frequency high imit protect time 3 | W | Cycle — | — | — | — | — |
| 80 | U 10 min | Volt protection for 10 min | W | 0.1 V 1.1 Vn — | — | — | — | — |
| 81 | PV Voltage PV V High Fault | oltage High Fault | W | 0.1 V — | — | — | — | — |
| 82 | FW Build No. Mo 5 nu | del letter version mber (TJ) | — | ASCII — | — | — | — | — |
| 83 | FW Build No. Mo 4 nu | del letter version mber (AA) | — | ASCII — | — | — | — | — |
| 84 | FW Build No. DS 3 | P 1 FW Build No. | — | ASCII — | — | — | — | — |
| 85 | FW Build No. DS 2 | P 2/M 0 FW Build No. | — | ASCII — | — | — | — | — |
| 86 | FW Build No. CP 1 No | LD/AFCI FW Build . | — | ASCII — | — | — | — | — |
| 87 | FW Build No. M 3 0 | FW Build No. | — | ASCII — | — | — | — | — |
| 88 | Modbus Vers Modb ion | us Version | E V | g:207 is Int(16 2.07 bits) — | — | — | tlx:modbus version, storage:modbus version | — |
| 89 | PFModel | Set PF function Model 0: PF=1 1: PF by set 2: default PF line 3: User PF line 4: Under Excited (Inda) Reactive Power 5: Over Excited(Capa) Reactive Power 6:Q(v)model 7:Direct Control mode 8. Static capacitive QV mode 9. Static inductive QV mode | W | — | — | — | — | — |
| 90 | GPRS IP Flag Bi IP Wr Su Bi | t 0-3:read:1;Set GPRS Successed ite:2;Read GPRS IP ccessed t 4-7:GPRS status | W   B o I B o G S | it 0-3:ab ut GPRS P SET it 4-7:ab ut RPRS tatus — | — | — | — | — |
| 91 | Freq Derate S Fre tart sta | quency derating rt point | W | 0.01 H Z — | — | — | — | — |
| 92 | FLrate | Frequency – load limit rate | W   0 | -100 10 tim es — | — | — | — | — |
| 93 | V 1 S | CEI 021 V 1 S Q(v) | W   V | 1 S<V 2 S 0.1 V — | — | — | — | — |
| 94 | V 2 S | CEI 021 V 2 S Q(v) | W | 0.1 V — | — | — | — | — |
| 95 | V 1 L | CEI 021 V 1 L Q(v) | W   V | 1 L<V 1 S 0.1 V — | — | — | — | — |
| 96 | V 2 L | CEI 021 V 2 L Q(v) | W   V | 2 L<V 1 L 0.1 V — | — | — | — | — |
| 97 | Qlockinpow Q(v) er powe | lock in active r of CEI 021 | W   0 | -100 Percen t — | — | — | — | — |
| 98 | Qlock Outpo Q(v) wer powe | lock Out active r of CEI 021 | W   0 | -100 Percen t — | — | — | — | — |
| 99 | LIGrid V | Lock in gird volt of CEI 021 PF line | W   n | Vn 0.1 V — | — | — | — | — |
| 100 | LOGrid V | Lock out gird volt of CEI 021 PF line | W   n | Vn 0.1 V — | — | — | — | — |
| 101 | PFAdj 1 | PF adjust value 1 | — | 4096 is 1 — | — | — | — | — |
| 102 | PFAdj 2 | PF adjust value 2 | — | 4096 is 1 — | — | — | — | — |
| 103 | PFAdj 3 | PF adjust value 3 | — | 4096 is 1 — | — | — | — | — |
| 104 | PFAdj 4 | PF adjust value 4 | — | 4096 is 1 — | — | — | — | — |
| 105 | PFAdj 5 | PF adjust value 5 | — | 4096 is 1 — | — | — | — | — |
| 106 | PFAdj 6 | PF adjust value 6 | — | 4096 is 1 — | — | — | — | — |
| 107 | QVRPDelay Ti QV me EE del | Reactive Power aytime | W | 0-30 1 S — | 3 S | — | — | — |
| 108 | Over FDerat D Ove elay Time EE ngde | rfrequency derati laytime | W | 0-20 50 ms 0 — | — | — | — | — |
| 109 | Qpercent Ma Qmax x | for Q(V) curve | W | 0-1000 0.1% — | — | — | — | — |
| 110 | PFLine P 1_LP PF loa | limit line point 1 d percent | W | 0-255 percen t — | — | 255 means no this point | — | — |
| 111 | PFLine P 1_PF PF pow | limit line point 1 er factor | W | 0-20000 — | — | — | — | — |
| 112 | PFLine P 2_LP PF loa | limit line point 2 d percent | W | 0-255 percen t — | — | 255 means no this point | — | — |
| 113 | PFLine P 2_PF PF 2 po | limit line point wer factor | W | 0-20000 — | — | — | — | — |
| 114 | PFLine P 3_LP PF loa | limit line point 3 d percent | W | 0-255 percen t — | — | 255 means no this point | — | — |
| 115 | PFLine P 3_PF PF pow | limit line point 3 er factor | W | 0-20000 — | — | — | — | — |
| 116 | PFLine P 4_LP PF loa | limit line point 4 d percent | W | 0-255 percen t — | — | 255 means no this point | — | — |
| 117 | PFLine P 4_PF PF pow | limit line point 4 er factor | W | 0-20000 — | — | — | — | — |
| 118 | Module 4 | Inverter Module (4) | — | &*11 — | — | Sxx Bxx | — | — |
| 119 | Module 3 | Inverter Module (3) | — | &*11 — | — | Dxx Txx | — | — |
| 120 | Module 2 | Inverter Module (2) | — | &*11 — | — | Pxx Uxx | — | — |
| 121 | Module 1 | Inverter Module (1) | — | &*11 — | — | Mxxxx Power | — | — |
| 122 | Export Limit_ Ex En/dis | port Limit_En/dis | R/ | W 1/0 — | — | Export Limit enable, 0: Disable export Limit; 1: Enable 485 export Limit; 2: Enable 232 export Limit; 3: Enable CT export Limit; | — | — |
| 123 | Export Limit P Ex ower Rate | port Limit Power Rate | R/ | W -1000~+1 0.1% 000 — | — | Export Limit Power Rate | — | — |
| 124 | Traker Model Tra | ker Model | W | 0,1,2 — | — | 0:Independent 1:DC Source 2:Parallel | — | — |
| ……… 11 | 22~1124 Bat Serial NO. Produ | / ct serial number of / | / | / / / / ASCII — | — | reserve | — | — |

## TL-X/TL-XH Holding Registers (3000–3124)
Additional holding registers for TL-X/TL-XH hybrids (MIN series).

**Applies to:** TL-X/TL-XH/TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | Export Limit Fa T iled Power Rat ex e | he power rate when port Limit failed | — | R/W 0.1% — | — | The power rate when export Limit failed | — | — |
| 3001 | New Serial NO | Serial number 1-2 | — | R/W ASCII — | — | The new model uses the following | — | — |
| 3002 | New Serial NO | Serial number 3-4 | — | R/W ASCII — | — | registers to record the serial number; The | — | — |
| 3003 | New Serial NO | Serial number 5-6 | — | R/W ASCII — | — | representation is the same as the | — | — |
| 3004 | New Serial NO | Serial number 7-8 | — | R/W ASCII — | — | original: one register holds two | — | — |
| 3005 | New Serial NO | Serial number 9-10 | — | R/W ASCII — | — | characters and the new serial number | — | — |
| 3006 | New Serial NO | Serial number 11-12 | — | R/W ASCII — | — | is 30 characters. | — | — |
| 3007 | New Serial NO | Serial number 13-14 | — | R/W ASCII — | — | — | — | — |
| 3008 | New Serial NO | Serial number 15-16 | — | R/W ASCII — | — | — | — | — |
| 3009 | New Serial NO | Serial number 17-18 | — | R/W A — | SCII | — | — | — |
| 3010 | New Serial NO | Serial number 19-20 | — | R/W A — | SCII | — | — | — |
| 3011 | New Serial NO | Serial number 21-22 | — | R/W A — | SCII | — | — | — |
| 3012 | New Serial NO | Serial number 23-24 | — | R/W A — | SCII | — | — | — |
| 3013 | New Serial NO | Serial number 25-26 | — | R/W A — | SCII | — | — | — |
| 3014 | New Serial NO | Serial number 27-28 | — | R/W A — | SCII | — | — | — |
| 3015 | New Serial NO | Serial number 29-30 | — | R/W A — | SCII | — | — | — |
| 3016 | Dry Contact Fu Dr nc En | R y Contact function enable | /W 0: 1: | Disable Enable — | — | Dry Contact function enable | — | — |
| 3017 | Dry Contact On Th Rate dr | e power rate ycontact turn on | of R | /W 0~1000 0 — | .1% | The power rate of drycontact turn on | — | — |
| 3018 | b Work Mode | Work Mode----0:default,1: System Retrofit 2: Multi-Parallel | — | R/W 0, 1, 2 — | — | MIN 2.5~6 KTL-XH/ XA Double CT special | — | — |
| 3019 | Dry Contact Of f Rate | Dry Contact Off Rate | — | Dry R/W 0 contact closure power — | ~100 0 | 0.1% Dry contact closure power pe rcentage | — | — |
| 3020 | Box Ctrl Inv Ord B er | ox Ctrl Inv Order | — | R/W Off-net box control instruct ion — | — | — | — | — |
| 3021 | Exter Comm Of Ext f Grid En set ena | ernal communication R/W ting manual off-network ble | — | — | — | 0 x 00: Disable; (default) 0 x 01: Enable; | — | — |
| 3022 | uw Bdc Stop W Bdc S ork Of Bus Volt | top Work Of Bus Volt | — | R — | — | — | — | — |
| 3023 | b Grid Type | Grid Type---0:Single Phase 1:Three Phase 2:Split Phase | — | R/W 0, 1, 2 — | — | MIN 2.5~6 KTL-XH/ XA Double CT special | — | — |
| 3024 | Float charge current limit | When charge current battery need is lower th this value, enter into f charge | an loat | R/W 0 — | .1 A 60 | 0 CC current | — | — |
| 3025 | Vbat Warning "Ba set | ttery-low" warning up voltage | — | R/W 0.1 V 4800 — | Le LV | ad acid battery voltage | — | — |
| 3026 | Vbatlow Warn "Ba Clr cle | ttery-low" warning ar voltage | — | R/W 0.1 V — | Cl vo vo Lo le 45 20 48 <= 49 50 | ear battery low ltage error ltage point ad Percent(only ad-Acid): .5 V(Load < %); .0 V(20%<=Load 50%); .0 V(Load > %); | — | — |
| 3027 | Vbatstopfordi B scharge | attery cut off voltage | — | R/W 0.1 V — | Sh di lo vo le 46 20 44 <= 44 50 | ould stop scharge when wer than this ltage(only ad-Acid): .0 V(Load < %); .8 V(20%<=Load 50%); .2 V(Load > %); | — | — |
| 3028 | Vbat stop for B charge | attery over charge voltage | R/W | 0.01 V 5800 — | Sh ch hi vo | ould stop arge when gher than this ltage | — | — |
| 3029 | Vbat start for discharge | Battery start discharge voltage | — | R/W 0.01 V 4800 — | Sh di lo vo | ould not scharge when wer than this ltage | — | — |
| 3030 | Vbat constant B charge v | attery constant charge oltage | — | R/W 0.01 V 5800 — | CV ca lo vo | voltage(acid) n charge when wer than this ltage | — | — |
| 3031 | Battemp B lower limit d l | attery temperature lower imit for discharge | — | R/W 0.1℃ 1170 — | 0-2 100 -40 | 00:0-20℃ 0-1400: -0℃ | — | — |
| 3032 | Bat temp B upper limit d l | attery temperature upper imit for discharge | — | R/W 0.1℃ 420 — | — | — | — | — |
| 3033 | Bat temp lower limit c | Battery temperature lowe limit for charge | r | R/W 0.1℃ 30 — | Bat tem lim 0-2 100 -40 | tery perature lower it 00:0-20℃ 0-1400: -0℃ | — | — |
| 3034 | Bat temp B upper limit c l | attery temperature upper imit for charge | — | R/W 0.1℃ 370 — | Bat tem upp | tery perature er limit | — | — |
| 3035 | uw Under Fre D Und ischarge Dely T ime | er Fre Delay Time | — | R/W 50 ms — | Und Tim | er Fre Delay e | — | — |
| 3036 | Grid First Disch arge Power Rat wh e | Discharge Power Rate en Grid First | — | 1-255 — | — | — | — | — |
| 3037 | Grid First Stop S OC | Stop Discharge soc when Grid First | — | 1-100 — | — | — | — | — |
| 3038 | Time 1(xh) | Period 1: [Start Time ~ Time], [Charge/Discharge [Disable/Enable] 3038 enable, charge and discharge, start time, time 3039 | End ], end | R/W — | Bit Bit Bit 0: 1: 2: Bit 0: ena | 0~7: minutes; 8~12: hour; 13~14, load priority; battery priority; Grid priority; 15, prohibited; 1: bled; | — | — |
| 3039 | — | — | — | R/W — | Bit Bit Bit | 0~7: minutes; 8~12: hour; 13~15: reserved | — | — |
| 3040 | Time 2(xh) | Time period 2: [start ti end time], [charge / discharge], [disable enable] 3040 enable, charge and discharge, start time, 3 end time | me ~ / 041 | R/W enab — | Bit Bit Bit 0: 1: 2: Bit 0: led; | 0~7: minutes; 8~12: hour; 13~14, load priority; battery priority; Grid priority; 15, prohibited; 1: | — | — |
| 3041 | — | — | R/W | Bit 0 Bit 8 Bit 1 — | ~7: mi ~12: h 3~15: | nutes; our; reserved | — | — |
| 3042 | Time 3(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3043 | — | — | R/W | With — | Time 1 | — | — | — |
| 3044 | Time 4(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3045 | — | — | R/W | With — | Time 1 | — | — | — |
| 3046 | 预留 | — | — | — | — | — | — | — |
| 3047 | Bat First Power C Rate B | harge Power Rate when at First | — | 1-100 — | — | — | — | — |
| 3048 | w Bat First stop SOC | Stop Charge soc when Bat First | — | 1-100 — | — | — | — | — |
| 3049 | Ac Charge Ena Ac C ble | harge Enable | — | Enab Disa — | le :1 ble:0 | — | — | — |
| 3050 | Time 5(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3051 | — | — | R/W | With — | Time 1 | — | — | — |
| 3052 | Time 6(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3053 | — | — | R/W | With — | Time 1 | — | — | — |
| 3054 | Time 7(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3055 | — | — | R/W | With — | Time 1 | — | — | — |
| 3056 | Time 8(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3057 | — | — | R/W | With — | Time 1 | — | — | — |
| 3058 | Time 9(xh) | With Time 1 | R/W | With — | Time 1 | — | — | — |
| 3059 | — | — | R/W | With — | Time 1 | — | — | — |
| 3060~ | Reserved | — | — | — | — | — | — | — |
| 3069 | — | — | — | — | — | — | — | — |
| 3070 | Battery Type | Battery type choose of buck-boost input | R/W | — | B 0 1 2 | attery type :Lithium :Lead-acid :other | — | — |
| 3071 | Bat Mdl Seria/ Ba Paral Num | t Mdl Seria/Paral Num | R/W | — | B N S T i n s T i n s | at Mdl Seria/Paral um; PH 4-11 K used he upper 8 bits ndicate the umber of series egments; he lower 8 bits ndicate the umber of parallel ections; | — | — |
| 3072 | Reserved | — | — | — | — | — | — | — |
| 3073 | Reserved | — | — | — | — | — | — | — |
| 3074 | Reserved | — | — | — | — | — | — | — |
| 3075 | Reserved | — | — | — | — | — | — | — |
| 3076 | Reserved | — | — | — | — | — | — | — |
| 3077 | Reserved | — | — | — | — | — | — | — |
| 3078 | Reserved | — | — | — | — | — | — | — |
| 3079 | Ups Fun En | Ups function enable or disable | R/W | 0 — | 0 1 | :disable :enable | — | — |
| 3080 | UPSVolt Set | UPS output voltage | R/W | 0 — | 0 1 2 | :230 V :208 V :240 V | — | — |
| 3081 | UPSFreq Set | UPS output frequency | R/W | 0 — | 0 1 | :50 Hz :60 Hz | — | — |
| 3082 | b Load First Sto S p Soc Set | top Soc When Load First | R/W | 13-100 — | r | atio | — | — |
| 3083 | Reserved | — | — | — | — | — | — | — |
| 3084 | Reserved | — | — | — | — | — | — | — |
| 3085 | Com Address Com | munication addr | R/W | 1 — | 1 a 1 C a | : Communication ddr=1 ~ 254 : ommunication ddr=1~254 | — | — |
| 3086 | Baud Rate | Communication Baud Rate | R/W | 0 — | 0 1 | : 9600 bps : 38400 bps | — | — |
| 3087 | Serial NO. 1 | Serial Number 1-2 | R/W | ASCII — | F | or battery | — | — |
| 3088 | Serial NO. 2 | Serial Number 3-4 | — | R/W ASCII — | — | — | — | — |
| 3089 | Serial NO. 3 | Serial Number 5-6 | — | R/W ASCII — | — | — | — | — |
| 3090 | Serial NO. 4 | Serial Number 7-8 | — | R/W ASCII — | — | — | — | — |
| 3091 | Serial No. 5 | Serial Number 9-10 | — | R/W ASCII — | — | — | — | — |
| 3092 | Serial No.6 | Serial Number 11-12 | — | R/W ASCII — | — | — | — | — |
| 3093 | Serial No. 7 | Serial Number 13-14 | — | R/W ASCII — | — | — | — | — |
| 3094 | Serial No. 8 | Serial Number 15-16 | — | R/W ASCII — | — | — | — | — |
| 3095 | Bdc Reset Cmd BDC | Reset command | — | R/W — | — | 0:Invalid data 1:Reset setting parameters 2:Reset correction parameter 3:Clear historical power | — | — |
| 3096 | ARKM 3 Code BDCM | onitoring software | — | R ASCII — | — | ZEBA | — | — |
| 3097 | code | — | — | — | — | — | — | — |
| 3098 | DTC | DTC | — | R — | — | — | — | — |
| 3099 | FW Code | DSP software code | — | R ASCII — | — | — | — | — |
| 3100 | — | — | — | — | — | — | — | — |
| 3101 | Processor 1 FW Vision | DSP Software Version | — | R ASCII — | — | — | — | — |
| 3102 | Bus Volt Ref | Minimum BUS voltage for charging and discharging batteries | — | R — | — | — | — | — |
| 3103 | ARKM 3 Ver BMS_MCUVer BMS | BDC monitoring software version hardware ver | sion | R R 1 — | — | — | — | — |
| 3104 | sion info BMS_FW | rmation BMS software version | R | 1 — | — | — | — | — |
| 3105 | BMS_Info | information BMS Manufacturer Name | R | 1 — | — | — | — | — |
| 3106 | BMSComm Ty BMSCo pe | mm Type | R | 1 — | — | BMSCommunicati on interface type: | — | — |
| 3107 | — | — | — | — | — | 0: RS 485; 1: CAN; | — | — |
| 3108 | Module 4 | BDCmodel (4) | — | R/W &*11 — | — | Sxx Bxx | — | — |
| 3109 | Module 3 | BDCmodel (3) | — | R/W &*11 — | — | Dxx Txx | — | — |
| 3110 | Module 2 | BDCmodel (2) | — | R/W &*11 — | — | Pxx Uxx | — | — |
| 3111 | Module 1 | BDCmodel (1) | — | R/W &*11 — | — | Mxxxx | — | — |
| 3112 | Reserved | — | — | — | — | — | — | — |
| 3113 | un Protocol Ve BD r | CProtocol Ver | — | R 1 — | — | Bit 8-bit 15 The major version number ranges from 0-256. In principle, it cannot be changed Bit 0-bit 7 Minor version number [0-256]. If the protocol is changed, you need to update this version No. | — | — |
| 3114 | uw Certificatio n Ver | BDC Certification Ver | — | R 1 — | — | — | — | — |
| 3115 | Reserved | — | — | — | — | — | — | — |
| 3124 | — | — | — | — | — | — | — | — |

## TL-XH US Holding Registers (3125–3249)
US-specific time schedule and dry-contact configuration registers.

**Applies to:** TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3125 | Time Month 1 Use ,Ad | with Time 1-9(us) d month time | R | /W — | — | bit 0~3:month_L; bit 4~7: month_H bit 8, 0:disable 1:enable Bit 9~15:reserve | — | — |
| 3126 | Time Month 2 Use ,Ad | with Time 10-18(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3127 | Time Month 3 Use ,Ad | with Time 19-27(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3128 | Time Month 4 Use ,Ad | with Time 28-36(us) R/W d month time | — | — | — | With Time Month 1 | — | — |
| 3129 | Time 1(us) | time 1:[starttime~endtime | ] cu [d e | R/W [Charge/ discharg e/counte r rrent], 1 isable/ 2 nable] 3 b 0 1 — | :batfi :gridf : anti it 15, :disab :enabl | bit 0~6:min; bit 7~11:hour; bit 12~14, 0:loadfirst; rst; irst; -reflux le; e; | — | — |
| 3130 | — | R/W | — | b b b 0 1 2 b — | it 0~6: it 7~11 it 12-1 :Weekd :Weeke :Wee K it 14~1 | min; :hour; 3, ay nd 5:reserve | — | — |
| 3131-3 | Time 2(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3133-3 | Time 3(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3135-3 | Time 4(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3137-3 | Time 5(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3139-3 | Time 6(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3141-3 | Time 7(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3143-3 | Time 8(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3145-3 | Time 9(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3147-3 | Time 10(us)Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3149-3 | Time 11(us)Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3151-3 | Time 12(us)Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3153-3 | Time 13(us)Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3155-3 | Time 14(us)Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3157-3 | Time 15(us) Same as | above R/W | — | S — | ame as | Time 1 | — | — |
| 3159-3 | Time 16(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3161-3 | Time 17(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3163-3 | Time 18(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3165-3 | Time 19(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3167-3 | Time 20(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3169-3 | Time 21(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3171-3 | Time 22(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3173-3 | Time 23(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3175-3 | Time 24(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3177-3 | Time 25(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3179-3 | Time 26(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3181-3 | Time 27(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3183-3 | Time 28(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3185-3 | Time 29(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3187-3 | Time 30(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3189-3 | Time 31(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3191-3 | Time 32(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3193-3 | Time 33(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3195-3 | Time 34(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3197-3 | Time 35(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3199-3 | Time 36(us)Same as | above R/W | — | Same a — | s Time | 1 | — | — |
| 3201 | Special Day 1 | Special Day 1(month,Day)R/ | W | bit 0~7 bit 8~1 bit 15, 0:disa enable — | :day; 4:mont ble 1: | h | — | — |
| 3202 | Special Day 1_ Time 1 | Start time R/W | — | bit 0~6 bit 7~1 bit 12~ 0:load 1:batf 2:grid 3: ant bit 15, 0: dis 1: ena — | :min; 1:hour 14, first; irst; first; i-refl able; ble; | ; ux | — | — |
| 3203 | — | endtime R/W | — | bit 0~6 bit 7~1 bit 12~ — | :min; 1:hour 15:res | ; erve | — | — |
| 3204-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3206-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3208-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3210-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3212-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3214-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3216-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3218-3 | Special Day 1_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3220 | Special Day 2 | Special Day 2(month,Day)R/ | W | bit 0~7 bit 8~1 bit 15, 0:disa 1:enab — | :day; 4:mont ble le | h | — | — |
| 3221 | Special Day 2_ Time 1 | Start time R/W | — | bit 0~6 bit 7~1 bit 12~ 0: loa 1: bat 2: gri 3: ant bit 15, 0: dis 1: ena — | : min; 1: hou 14, dfirst first; dfirst i-refl able; ble; | r; ; ; ux | — | — |
| 3222 | — | endtime R/W | — | bit 0~6 bit 7~1 bit 12~ — | : min; 1: hou 15:res | r; erve | — | — |
| 3223-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3225-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3227-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3229-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3231-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3233-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3235-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3237-3 | Special Day 2_ Same | as above R/W | — | Same a — | s | — | — | — |
| 3239-3 | Reserve | Reserve | — | R/W — | — | — | — | — |

## TL3/MAX/MID/MAC Holding Registers (125–249)
Three-phase inverter specific holding registers.

**Applies to:** TL3-X/MAX/MID/MAC

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 125 | INV Type-1 | Inverter type-1 R | — | ASCII — | Rese | rved | — | — |
| 126 | INV Type-2 | Inverter type-2 R | — | ASCII — | — | — | — | — |
| 127 | INV Type-3 | Inverter type-3 R | — | ASCII — | — | — | — | — |
| 128 | INV Type-4 | Inverter type-4 R | — | ASCII — | — | — | — | — |
| 129 | INV Type-5 | Inverter type-5 R | — | ASCII — | — | — | — | — |
| 130 | INV Type-6 | Inverter type-6 R | — | ASCII — | — | — | — | — |
| 131 | INV Type-7 | Inverter type-7 R | — | ASCII — | — | — | — | — |
| 132 | INV Type-8 | Inverter type-8 R | — | ASCII — | — | — | — | — |
| 133 | BLVersion 1 | Boot loader version 1 R | — | — | Rese | rved | — | — |
| 134 | BLVersion 2 | Boot loader version 2 R | — | — | Rese | rved | — | — |
| 135 | BLVersion 3 | Boot loader version 3 R | — | — | Rese | rved | — | — |
| 136 | BLVersion 4 | Boot loader version 4 R | — | — | Rese | rved | — | — |
| 137 | Reactive P Value H | Reactive Power H R/W | — | 0.1 var — | — | — | — | — |
| 138 | Reactive P Value L | Reactive Power L R/W | — | 0.1 var — | — | — | — | — |
| 139 | Reactive Out Rea put Priority E En nable | ctive Output Priority R/W able | — | 0/1 — | 0:di 1:en | sable able | — | — |
| 140 | Reactive P Reac Value(Ratio) | tive Power Ratio R/W | — | 0.1 — | — | — | — | — |
| 141 | Svg Function Svg Enable | enable on night R/W | — | 0/1 — | 0:di 1:en | sable able | — | — |
| 142 | uw Under FU Under pload Point | F Upload Point R/W | — | 0.01 H Z — | — | — | — | — |
| 143 | uw OFDerate OFDe Recover Poin t | rate Recover Point R/W | — | 0.01 H Z — | — | — | — | — |
| 144 | uw OFDerate OFDe Recover Dela Rec y Time | rate R/W over Delay Time | 0-30 | 000 50 ms — | — | — | — | — |
| 145 | Zero Current Zer Enable | o Current Enable R/W | 0- | 1 — | — | — | — | — |
| 146 | uw Zero Curre Zer nt Staticlow V St olt | o Current R/W aticlow Volt | 46 | -230 V 0.1 V 115 V — | — | — | — | — |
| 147 | uw Zero Curre Zer nt Static High St Volt | o Current R/W atic High Volt | 23 | 0-276 V 0.1 V 276 V — | — | — | — | — |
| 148 | uw HVolt Der HVol ate High Point | t Derate High Point R/W | 0- | 1000 V 0.1 V — | — | — | — | — |
| 149 | uw HVolt Der HVol ate Low Point | t Derate Low Point R/W | — | 0-1000 V 0.1 V — | — | — | — | — |
| 150 | uw QVPower QVPow Stable Time | er Stable Time R/ | W | 0-60 S 0.1 S — | — | — | — | — |
| 151 | uw Under FU Under pload Stop Po Sto int | F Upload R p Point | /W | 0.01 H Z — | — | — | — | — |
| 152 | f Under Freq P Und oint sta | erfrequency load R rt point | /W 46 00 | .00-50. 0.01 Hz 49.80 — | CEI | — | — | — |
| 153 | f Under Freq E Und nd Point loa | erfrequency down R/W 46.00 d end point 00 | -50. | 0.01 Hz 49.10 CEI — | — | — | — | — |
| 154 | f Over Freq Po Ove int sta | r frequency loading R/W 50 rt point 00 | .00-5 | 2. 0.01 Hz 50.20 CEI — | — | — | — | — |
| 155 | f Over Freq En Ove d Point end | r frequency loading R/W 50 point 00 | .00-5 | 2. 0.01 Hz 51.50 CEI — | — | — | — | — |
| 156 | f Under Volt P Und oint she | ervoltage load R/W 1 dding start point | 60-30 | 0 0.1 V 220 — | .0 CEI | — | — | — |
| 157 | f Under Volt E Und nd Point end | ervoltage derating R/W 160 point | -300 | 0.1 V 207 — | .0 CEI | — | — | — |
| 158 | f Over Volt Poi Ov nt st | ervoltage loading art point | R/W 1 | 60-300 0.1 V 230 — | .0 CEI | — | — | — |
| 159 | f Over Volt En Ove d Point end | rvoltage loading point | R/W 1 | 60-300 0.1 V 245 — | .0 CEI | — | — | — |
| 160 | uw Nominal Nomin Grid Volt | R/W al Grid Volt Select | — | 0~3 — | UL | — | — | — |
| 161 | uw Grid Watt Grid Delay | R/ Watt Delay Time | W | 0~3000 20 ms — | UL | — | — | — |
| 162 | uw Reconnec Rec t Start Slope | R/ onnect Start Slope | W | 1~1000 0.1 — | UL | — | — | — |
| 163 | uw LFRTEE | R/ LFRT 1 Freq | W | 5500~650 0.01 Hz 0 — | UL | — | — | — |
| 164 | uw LFRTTime LFRT EE | R/ 1 Time | W | 20 ms — | UL | — | — | — |
| 165 | uw LFRT 2 EE LFRT 2 | R/ Freq | W | 5500~650 0.01 Hz 0 — | UL | — | — | — |
| 166 | uw LFRTTime LFRT 2 EE | R/ 2 Time | W | 20 ms — | UL | — | — | — |
| 167 | uw HFRTEE | R/ HFRT 1 Freq | W | 5500~650 0.01 Hz 0 — | UL | — | — | — |
| 168 | uw HFRTTim HFRT 1 e EE | R/ Time | W | 20 ms — | UL | — | — | — |
| 169 | uw HFRT 2 EE HFRT 2 | R/W Freq | 55 0 | 00~650 0.01 Hz — | UL | — | — | — |
| 170 | uw HFRTTim HFRT 2 e 2 EE | R/W Time | — | 20 ms — | UL | — | — | — |
| 171 | uw HVRTEE | R/W HVRT 1 Volt | — | 0.001 Un — | UL | — | — | — |
| 172 | uw HVRTTim HVRT 1 e EE | R/W Time | — | 20 ms — | UL | — | — | — |
| 173 | uw HVRT 2 EE HVRT 2 | R/W Volt | — | 0.001 Un — | UL | — | — | — |
| 174 | uw HVRTTim HVRT 2 e 2 EE | R/W Time | — | 0.001 Un — | UL | — | — | — |
| 175 | uw Under FU Un pload Delay Ti Up me | R/W der F load Delay Time | 0-2s | 50 ms 0 s — | 50549 | — | — | — |
| 176 | uw Under FU Und pload Rate EE | R/W er F Upload Rate | — | — | 50549 | — | — | — |
| 177 | uw Grid Resta Gri rt_H_Freq | d Restart High Freq R/W | — | 0.01 Hz — | 50549 | — | — | — |
| 178 | Over FDerat R Ove esponse Tim Resp e | r FDerat W/R onse Time | 0-50 | 0 — | — | — | — | — |
| 179 | Under FUplo Unde ad Response Resp Time | r FUpload W/R onse Time | 0-50 | 0 — | — | — | — | — |
| 180 | Meter Link | Whether to elect the R/W meter | — | — | 0: Mis | sed, 1: Received | — | — |
| 181 | OPT Number Numb opti | er of connection R/W mizers | 0- | 64 — | The to connec | tal number of optimizers ted to the inverter | — | — |
| 182 | OPT Config OK Flag | Optimizer R/W configuration completion flag | — | — | 0 x 00:N 0 x 01:C | ot configured success onfiguration is complete | — | — |
| 183 | Pv Str Scan | String Num R/W | 0、 32 | 8, 16, — | 0:Not Other: | support Pv String Num | — | — |
| 184 | BDCLink Num BDC | parallel Num R/W | — | — | The nu connec machin Defaul | mber of BDCs ted to the current e t is 0 | — | — |
| 185 | Pack Num | Number of battery modules | R | — | Tot mod wit | al number of battery ules currently associated h all BDCs | — | — |
| 186 | Reserved | — | — | — | — | — | — | — |
| 187 | VPP function VP enable st status | P function enable atus | R | — | 0:D 1:E | isable nable | — | — |
| 188 | data Log d Connect S Server status | ata Log Connect erver status | — | — | 0:c 1:C | onnection succeeded onnection failed | — | — |
| 200 | Reserved | — | — | — | Res | erved | — | — |
| 201 | PID Working PID Model | Operating mode | — | W 0: automati c 1: continuo us 2: All night — | — | — | — | — |
| 202 | PID On/Off Ctrl | PID Break control | — | W 0:On 1:Off — | — | — | — | — |
| 203 | PID Volt PID Option opt | Output voltage ion | — | W 300~1000 V — | — | — | — | — |
| 209 | New Serial NO | Serial number 1-2 | — | ASCII — | — | — | — | — |
| 210 | New Serial NO | Serial number 3-4 | — | ASCII — | — | — | — | — |
| 211 | New Serial NO | Serial number 5-6 | — | ASCII — | — | — | — | — |
| 212 | New Serial NO | Serial number 7-8 | — | ASCII — | — | — | — | — |
| 213 | New Serial NO | Serial number 9-10 | — | ASCII — | — | — | — | — |
| 214 | New Serial NO | Serial number 11-12 | — | ASCII — | — | — | — | — |
| 215 | New Serial NO | Serial number 13-14 | — | ASCII — | — | — | — | — |
| 216 | New Serial NO | Serial number 15-16 | — | ASCII — | — | — | — | — |
| 217 | New Serial NO | Serial number 17-18 | — | ASCII — | — | — | — | — |
| 218 | New Serial NO | Serial number 19-20 | — | ASCII — | — | — | — | — |
| 219 | New Serial NO | Serial number 21-22 | — | ASCII — | — | — | — | — |
| 220 | New Serial NO | Serial number 23-24 | — | ASCII — | — | — | — | — |
| 221 | New Serial NO | Serial number 25-26 | — | ASCII — | — | — | — | — |
| 222 | New Serial NO | Serial number 27-28 | — | ASCII — | — | — | — | — |
| 223 | New Serial NO | Serial number 29-30 | — | ASCII — | — | — | — | — |
| 229 | Energy Adjus Pow t inc coe | er generation W/R remental calibration fficient | — | 0.1% — | 1-1000 | ,(Percent ratio) | — | — |
| 230~24 | 9 for growatt debug | setting | — | — | — | — | — | — |
| 230 | Island Disabl Is e 1: | land Disable or not. W disable 0:Enable | 0,1 | 0 — | — | — | — | — |
| 231 | Fan Check | Start Fan Check W | 1 | — | — | — | — | — |
| 232 | Enable NLine Ena | ble N Line of grid W | 1 | 0 — | — | — | — | — |
| 233 | w Check Hard w Che ware Bit 0 Bit 1 Bit 8 ng Bit 9 | ck Hardware : GFCIBreak; :SPSDamage :Eeprom Read Warni :EEWrite Warning …… | — | — | — | — | — | — |
| 234 | w Check Hard ware 2 | — | — | — | reserv | ed | — | — |
| 235 | ub NTo GNDD Dis/e etect detec | nable N to GND W t function | 1:e 0:d | nable 1 isable — | — | — | — | — |
| 236 | Non Std Vac E Enab nable Nons Grid | le/Disable W tandard voltage range | 0-2 | 0 — | 0:Disa 1:Enab 2:Enab | ble; le Voltgrade 1 le Voltgrade 2 | — | — |
| 237 | uw Enable Sp Disa ec Set appo | blse/enable W inted spec setting | 1:e 0:d | nable Binary 0 x 000 Bi isable 0 — | t 0: H | ungary | — | — |
| 238 | Fast MPPT About enable | Fast mppt | — | 0,1,2 0 — | Rese | rved | — | — |
| 239 | / | / | / | / / — | Rese | rved | — | — |
| 240 | Check Step | — | W | — | — | — | — | — |
| 241 | INV-Lng | Inverter Longitude | W | — | Long | itude | — | — |
| 242 | INV-Lat | Inverter Latitude | W | — | Lati | tude | — | — |
| 132 | — | — | — | ( — | us) | — | — | — |
| 134 | — | — | — | ( — | us) | — | — | — |
| 136 | — | — | — | ( — | us) | — | — | — |
| 138 | — | — | — | ( — | us) | — | — | — |
| 140 | — | — | — | ( — | us) | — | — | — |
| 142 | — | — | — | ( — | us) | — | — | — |
| 144 | — | — | — | ( — | us) | — | — | — |
| 146 | — | — | — | ( — | us) | — | — | — |
| 148 | — | — | — | ( — | us) | — | — | — |
| 150 | — | — | — | ( — | us) | — | — | — |
| 152 | — | — | — | ( — | us) | — | — | — |
| 154 | — | — | — | ( — | us) | — | — | — |
| 156 | — | — | — | ( — | us) | — | — | — |
| 158 | — | — | — | ( — | us) | — | — | — |
| 160 | — | — | — | (us) — | — | — | — | — |
| 162 | — | — | — | (us) — | — | — | — | — |
| 164 | — | — | — | (us) — | — | — | — | — |
| 166 | — | — | — | (us) — | — | — | — | — |
| 168 | — | — | — | (us) — | — | — | — | — |
| 170 | — | — | — | (us) — | — | — | — | — |
| 172 | — | — | — | (us) — | — | — | — | — |
| 174 | — | — | — | (us) — | — | — | — | — |
| 176 | — | — | — | (us) — | — | — | — | — |
| 178 | — | — | — | (us) — | — | — | — | — |
| 180 | — | — | — | (us) — | — | — | — | — |
| 182 | — | — | — | (us) — | — | — | — | — |
| 184 | — | — | — | (us) — | — | — | — | — |
| 186 | — | — | — | (us) — | — | — | — | — |
| 188 | — | — | — | (us) — | — | — | — | — |
| 190 | — | — | — | (us) — | — | — | — | — |
| 192 | — | — | — | (us) — | — | — | — | — |
| 194 | — | — | — | (us) — | — | — | — | — |
| 196 | — | — | — | (us) — | — | — | — | — |
| 198 | — | — | — | (us) — | — | — | — | — |
| 200 | — | — | — | (us) — | — | — | — | — |
| 205 | Time 2 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 207 | Time 3 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 209 | Time 4 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 211 | Time 5 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 213 | Time 6 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 215 | Time 7 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 217 | Time 8 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 219 | Time 9 | — | — | Specia 1 — | l Day 1_ | Time | — | — |
| 224 | Time 2 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 226 | Time 3 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 228 | Time 4 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 230 | Time 5 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 232 | Time 6 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 234 | Time 7 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 236 | Time 8 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 238 | Time 9 | — | — | Specia 1 — | l Day 2_ | Time | — | — |
| 249 | — | — | — | — | — | — | — | — |

## Storage Holding Registers (1000–1124)
Storage (MIX/SPA/SPH) battery configuration holding registers.

**Applies to:** Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000. | Float W charge b current t limit i | hen charge current W attery need is lower han this value, enter nto float charge | — | 0.1 A 600 — | CC cur | rent | — | — |
| 1001. | PF CMD Set t memory CMD w state ornot setti value | he following 19-22 W ill be memory (1/0), if not, these ngs are the initial . | 0 | or 1, 0 — | Means acting power | these settings will be or not when next on(02 repeat) | — | — |
| 1002. | Vbat Start F LV V or Discharg e | bat R/ | W | 0.1 V — | Lead-a | cid battery LV voltage | — | — |
| 1003. | Vbatlow Wa Load P rn Clr lead- 45.5 V <20% 48.0 V 20%~5 49.0 V >50 | ercent(only W Acid): 0% | — | 0.1 V — | Clear voltag | battery low voltage error e point | — | — |
| 1004. | Vbatstopfo Shou rdischarge when v 4 < 4 2 4 > | ld stop discharge W lower than this oltage(only lead-Acid): 6.0 V 20% 4.8 V 0%~50% 4.2 V 50% | — | 0.01 V — | — | — | — | — |
| 1005. | Vbat stop Shoul for charge when volt | d stop charge higher than this age | W | 0.01 V 5800 — | — | — | — | — |
| 1006. | Vbat start Shou for when discharge volta | ld not discharge W lower than this ge | — | 0.01 V 4800 — | — | — | — | — |
| 1007. | Vbat c constant t charge | an charge when lower W han this voltage | — | 0.01 V 5800 — | CV vol | tage(acid) | — | — |
| 1008. | EESys Info.S Bit ys Set En Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit Bit | 0:Resved; W 1:Resved; 2:Resved; 3:Resved; 4:Resved; 5:b Discharge En; 6:Force Dischr En; 7:Charge En; 8:b Force Chr En; 9:b Back Up En; 10:b Inv Limit Load E; 11:b Sp Limit Load En; 12:b ACCharge En; 13:b PVLoad Limit En; 14,15:Un Used; | — | — | Syst | em Enable | — | — |
| 1009. | Battemp Bat lower limit low d | tery temperature W er limit for discharge | 0 0 1 0 | -200:0-2 0.1℃ 1170 ℃ 000-140 :-40-0℃ — | — | — | — | — |
| 1010. | Bat temp Batter upper limit upp d | y temperature W er limit for discharge | 2 | 00-1000 0.1℃ 420 — | — | — | — | — |
| 1011. | Bat temp Batter lower limit low c | y temperature er limit for charge | W   0 0 1 0 | -200:0-2 0.1℃ 30 ℃ 000-140 :-40-0℃ — | Lowe | r temperature limit | — | — |
| 1012. | Bat temp Batter upper limit upp c | y temperature W er limit for charge | 2 | 00-1000 0.1℃ 370 Up — | per te | mperature limit | — | — |
| 1013. | uw Under Fr Under e Discharge Dely Time | Fre Delay Time | s   0 | -20 50 ms Un — | der Fr | e Delay Time | — | — |
| 1014. | Bat Mdl Seri Batt al Num | ery serial number W | 0 | 0:00 SP — | H 4-11 K | used | — | — |
| 1015. | Bat Mdl Para Batt ll Num | ery parallel section W | 0 | 0:00 SP — | H 4-11 K | used | — | — |
| 1016. | DRMS_EN / | / | / | / / 0: — | disabl | e 1:enable | — | — |
| 1017. | Bat First Hi Start Time Low 4 | gh eight:hours eight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1018. | Bat First Hig Stop Time Low e 4 | h eight:hours ight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1019. | Bat First E on/off D Switch 4 | nable:1 isable:0 | 0 | or 1 Ba — | ttery | priority enable 1 | — | — |
| 1020. | Bat First Hi Start Time Low 5 | gh eight:hours eight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1021. | Bat First High Stop Time Low e 5 | eight:hours ight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1022. | Bat First E on/off D Switch 5 | nable:1 isable:0 | 0 | or 1 Ba — | ttery | priority enable 1 | — | — |
| 1023. | Bat First High Start Time Low 6 | eight:hours eight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1024. | Bat First High Stop Time Low e 6 | eight:hours ight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1025. | Bat First E on/off D Switch 6 | nable:1 isable:0 | 0 | or 1 Ba — | ttery | priority enable 1 | — | — |
| 1026. | Grid First High Start Time Low 4 | eight:hours eight: minutes | 0 0 | -23 -59 — | — | — | — | — |
| 1027. | Grid First High Stop Time Low e 4 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1028. | Grid First Enab Stop Disa Switch 4 | le:1 ble:0 | 0 or | 1 Grid — | priori | ty enable | — | — |
| 1029. | Grid First High Start Time Low 5 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1030. | Grid First High Stop Time Low e 5 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1031. | Grid First Enab Stop Disa Switch 5 | le:1 ble:0 | 0 or | 1 Grid — | priori | ty enable | — | — |
| 1032. | Grid First High Start Time Low 6 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1033. | Grid First High Stop Time Low e 6 | eight:hours ight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1034. | Grid First Enab Stop Disa Switch 6 | le:1 ble:0 | 0 or | 1 Grid — | priori | ty enable | — | — |
| 1035. | Bat First High Start Time Low 4 | eight:hours eight: minutes | 0-23 0-59 | — | — | — | — | — |
| 1036. | / / | / | / | / / Reser — | ve | — | — | — |
| 1037. | U b CTMode C C | se the CTMode to W hoose RFCT \ Cable T\METER | 2:ME 1:cW ssCT 0:cW T | TER 0 irele ired C — | — | — | — | — |
| 1038. | CTAdjust C | TAdjust enable W | 0:di 1:en | sable 0 able — | — | — | — | — |
| 1039. | / / | / | / | / / Reser — | ve | — | — | — |
| 1040. | / / | / | / | / / R — | eserve | — | — | — |
| 1041. | / / | / | / | / / R — | eserve | — | — | — |
| 1042. | / / | / | / | / R — | eserve | — | — | — |
| 1043. | / / | / | / | / / R — | eserve | — | — | — |
| 1044. | Priority F E L f | orce Chr En/Force Dischr R n oad first/bat first /grid irst | 0.L fau att rid | oad(de b lt)/1.B n ery/2.G — | Force C /dis | hr En/disb Force Dischr E | — | — |
| 1045. | / / | / | / | / / R — | eserve | — | — | — |
| 1046. | / / | / | / | / / R — | eserve | — | — | — |
| 1047. | Aging Test St Com ep Cmd | mand for aging test | 0: 1: 2: dis | default C charge charge — | md for | aging test | — | — |
| 1048. | Battery Typ Batt e buck | ery type choose of -boost input | 0:L 1:L d 2:o | ithium 0 B ead-aci ther — | attery | type | — | — |
| 1049. | / / | / | / | / R — | eserve | — | — | — |
| 1050. | / / | / | / | / / R — | eserve | — | — | — |
| 1051. | / / | / | / | / R — | eserve | — | — | — |
| 1052. | / / | / | / | / R — | eserve | — | — | — |
| 1053. | / / | / | / | / R — | eserve | — | — | — |
| 1054. | / / | / | / | / / R — | eserve | — | — | — |
| 1060. | Buck Ups Fun E Ups n dis | function enable or able | — | 0:disable 1:enable — | — | — | — | — |
| 1061. | Buck UPSVolt S UP et | S output voltage | — | 0:230 230 V 1:208 2:240 — | — | — | — | — |
| 1062. | UPSFreq Set | UPS output frequency | — | 0:50 Hz 50 Hz 1:60 Hz — | — | — | — | — |
| 1070. | Grid First Disch arge Power Rat wh e | Discharge Power R en Grid First | ate W | 0-100 1% Dis Powe when — | charge r Rate Grid First | — | — | — |
| 1071. | Grid First Stop S OC | Stop Discharge soc when W Grid First | — | 0-100 1% S Disc soc Grid — | top harge when First | — | — | — |
| 1072… | / | / | / | / / / — | — | reverse | — | — |
| 1079 | — | — | — | — | — | — | — | — |
| 1080. | Grid First Start Time 1 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1081. | Grid First Stop Time 1 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1082. | Grid First Stop Switch 1 | Enable :1 Disable:0 | — | 0 or 1 Grid enab — | First le | — | — | — |
| 1083. | Grid First Start Time 2 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1084. | Grid First Stop Time 2 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1085. | Grid First Stop Switch 2 | Force Discharge.b Switch&L CD_SET_FORCE_TRUE_2)= =LCD_SET_FORCE_TRUE_2 | — | 0 or 1 Grid enab — | First le | Force Discharge; LCD_SET_FORCE_T RUE_2 | — | — |
| 1086. | Grid First Start Time 3 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1087. | Grid First Stop Time 3 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | — | — | — |
| 1088. | Grid First Stop Switch 3 | Enable :1 Disable:0 | — | 0 or 1 Grid enab — | First le | — | — | — |
| 1089. | / | / | / | / / / — | — | reserve | — | — |
| 1090. | Bat First Power C Rate B | harge Power Rate when W at First | 0- | 100 1% Char Power when Fir — | ge Rate Bat st | — | — | — |
| 1091. | w Bat First stop SOC | Stop Charge soc when Bat W First | 0- | 100 1% Sto Charge when Fir — | p soc Bat st | — | — | — |
| 1092. | AC charge W Switch E D | hen Bat First nable:1 isable:0 | En Di | able:1 AC Cha sable:0 Enabl — | rge e | — | — | — |
| 1093… | — | — | — | — | — | — | — | — |
| 1099 | — | — | — | — | — | — | — | — |
| 1100. | Bat First Start Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1101. | Bat First Stop Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1102. | Bat First on/off Switch 1 | Enable :1 Disable:0 | 0 | or 1 Bat Enable — | First 1 | — | — | — |
| 1103. | Bat First Start Time 2 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1104. | Bat First Stop Time 2 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1105. | Bat Firston/off Switch 2 | Enable :1 Disable:0 | 0 | or 1 Bat Enable — | First 2 | — | — | — |
| 1106. | Bat First Start Time 3 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1107. | Bat First Stop Time 3 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | — | — | — |
| 1108. | Bat Firston/off Switch 3 | Enable :1 Disable:0 | 0 | or 1 Bat Enable — | First 3 | — | — | — |
| 1109. | / | / / | / | / / — | — | reserve | — | — |
| 1110. | Load First Start Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | SPA/ reserve | — | — |
| 1111. | Load First Stop Time 1 | High eight bit:hour Low eight bit:minute | 0- 0- | 23 59 — | — | SPA/ reserve | — | — |
| 1112. | Load First Switch 1 | Enable :1 Disable:0 | 0 | or 1 Load F Enab — | irst S le | PA/ reserve | — | — |
| 1113. | Load First Start Time 2 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | SPA/ reserve | — | — |
| 1114. | Load First Stop Time 2 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | SPA/ reserve | — | — |
| 1115. | Load First Switch 2 | Enable :1 Disable:0 | — | 0 or 1 Loa Ena — | d Firs ble | t SPA/ reserve | — | — |
| 1116. | Load First Start Time 3 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | SPA/ reserve | — | — |
| 1117. | Load First Stop Time 3 | High eight bit:hour Low eight bit:minute | — | 0-23 0-59 — | — | SPA/ reserve | — | — |
| 1118. | Load First Switch 3 | Enable :1 Disable:0 | — | 0 or 1 Loa Ena — | d Firs ble | t SPA/ reserve | — | — |
| 1119. | New EPower C / alc Flag | — | / | / / / — | — | 0:The old formula 1 : The new formula | — | — |
| 1120. | Back Up En | Back Up Enable | — | — | — | MIX US | — | — |
| 1121. | SGIPEn | SGIP Enable | — | — | — | MIX US | — | — |

## Storage Holding Registers (1125–1249)
Additional SPA/SPH storage configuration registers.

**Applies to:** Storage SPA/SPH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1125 | 8 the f Bat Serial NO. stora | irst PACK of energy ge batteries / | — | / ASCII — | — | — | — | — |
| 1126 | 7 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1127 | 6 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1128 | 5 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1129 | 4 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1130 | 3 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1131 | 2 Bat Serial NO. | — | / | / ASCII — | — | — | — | — |
| 1132 | 1 Bat Serial NO. 8~ | The serial number of the second to tenth packs of | / | / ASCII — | — | — | — | — |
| 1132 | Bat Serial NO. | the energy storage batte | ry | — | — | — | — | — |
| ~1204 | 1 | consists of nine packs, the format of the serial number of each PACK is 1125 to 1132 | and | — | — | — | — | — |
| 1244 | Com version Nam Name H con | e of the battery main trol firmware version | — | ASCII — | — | — | — | — |
| 1245 | Com version Nam Name L con | e of the battery main trol firmware version | — | ASCII — | — | — | — | — |
| 1246 | Com versio No | n Version of the battery m control firmware | ain | digital — | — | — | — | — |
| 1247 | Com version Nam Name H mon ver | e of b itoring firm sion | atter ware | y ASCII — | — | — | — | — |
| 1248 | Com version Nam Name L mon ver | e of b itoring firm sion | atter ware | y ASCII — | — | — | — | — |
| 1249 | Com versio No | n Battery monitori firmware version | ng | digital — | — | — | — | — |

## Common Input Registers (0–124)
Applies to TL3/MAX and legacy inverters for basic PV/AC telemetry.

**Applies to:** TL-X/TL-XH (legacy mode), TL3-X/MAX/MID/MAC, Storage MIX/SPA/SPH, Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0. | Inverter Status | Inverter run state | — | 0:waiting, 1:normal, 3:fault — | — | — | tlx:status_code, tl3:status_code, offgrid:status_code | Status code |
| 1. | Ppv H | Input power (high) | — | 0.1 W — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 2. | Ppv L | Input power (low) | — | 0.1 W — | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3. | Vpv 1 | PV 1 voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 4. | PV 1 Curr | PV 1 input current | — | 0.1 A — | — | — | tlx:input_1_amperage, tl3:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 5. | Ppv 1 H | PV 1 input power(high) | — | 0.1 W — | — | — | tlx:input_1_power, tl3:input_1_power, offgrid:input_2_power | Input 1 Wattage, Input 2 Wattage, PV1 charge power, PV2 charge power |
| 6. | Ppv 1 L | PV 1 input power(low) | — | 0.1 W — | — | — | — | — |
| 7. | Vpv 2 | PV 2 voltage | — | 0.1 V — | — | — | tlx:input_2_voltage, tl3:input_2_voltage, offgrid:input_1_amperage | Input 1 Amperage, Input 2 voltage, PV1 buck current, PV2 voltage |
| 8. | PV 2 Curr | PV 2 input current | — | 0.1 A — | — | — | tlx:input_2_amperage, tl3:input_2_amperage, offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9. | Ppv 2 H | PV 2 input power (high) | — | 0.1 W — | — | — | tlx:input_2_power, tl3:input_2_power, offgrid:output_active_power | Input 2 Wattage, Output active power, PV2 charge power |
| 10 | . Ppv 2 L | PV 2 input power (low) | — | 0.1 W — | — | — | — | — |
| 11 | . Vpv 3 | PV 3 voltage | — | 0.1 V — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12 | . PV 3 Curr | PV 3 input current | — | 0.1 A — | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 13 | . Ppv 3 H | PV 3 input power (high) | — | 0.1 W — | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 14 | . Ppv 3 L | PV 3 input power (low) | — | 0.1 W — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 15 | . Vpv 4 | PV 4 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16 | . PV 4 Curr | PV 4 input current | — | 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17 | . Ppv 4 H | PV 4 input power (high) | — | 0.1 W — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 18 | . Ppv 4 L | PV 4 input power (low) | — | 0.1 W — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 19 | . Vpv 5 | PV 5 voltage | — | 0.1 V — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20 | . PV 5 Curr | PV 5 input current | — | 0.1 A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | . Ppv 5 H | PV 5 input power(high) | — | 0.1 W — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 22 | . Ppv 5 L | PV 5 input power(low) | — | 0.1 W — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 23 | . Vpv 6 | PV 6 voltage | — | 0.1 V — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24 | . PV 6 Curr | PV 6 input current | — | 0.1 A — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 25 | . Ppv 6 H | PV 6 input power (high) | — | 0.1 W — | — | — | tlx:input_6_power, offgrid:inverter_temperature | Input 6 Wattage, Temperature |
| 26 | . Ppv 6 L | PV 6 input power (low) | — | 0.1 W — | — | — | tl3:output_energy_today, offgrid:dc_dc_temperature | DC-DC temperature, Energy produced today |
| 27 | . Vpv 7 | PV 7 voltage | — | 0.1 V — | — | — | tlx:input_7_voltage, offgrid:load_percent | Input 7 voltage, Inverter load |
| 28 | . PV 7 Curr | PV 7 input current | — | 0.1 A — | — | — | tlx:input_7_amperage, tl3:output_energy_total, offgrid:battery_port_voltage | Battery port voltage, Input 7 Amperage, Total energy produced |
| 29 | . Ppv 7 H | PV 7 input power (high) | — | 0.1 W — | — | — | tlx:input_7_power, offgrid:battery_bus_voltage | Battery bus voltage, Input 7 Wattage |
| 30 | . Ppv 7 L | PV 7 input power (low) | — | 0.1 W — | — | — | tl3:operation_hours, offgrid:operation_hours | Running hours |
| 31 | . Vpv 8 | PV 8 voltage | — | 0.1 V — | — | — | tlx:input_8_voltage | Input 8 voltage |
| 32 | . PV 8 Curr | PV 8 input current | — | 0.1 A — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 33 | . Ppv 8 H | PV 8 input power (high) | — | 0.1 W — | — | — | tlx:input_8_power | Input 8 Wattage |
| 34 | . Ppv 8 L | PV 8 input power (low) | — | 0.1 W — | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35 | . Pac H | Output power (high) | — | 0.1 W — | — | — | tlx:output_power | Output power |
| 36 | . Pac L | Output power (low) | — | 0.1 W — | — | — | — | — |
| 37 | . Fac | Grid frequency | — | 0.01 Hz — | — | — | tlx:grid_frequency | AC frequency, Grid frequency |
| 38 | . Vac 1 | Three/single phase grid voltage | — | 0.1 V — | — | — | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 39 | . Iac 1 | Three/single phase grid output | — | current 0.1 A — | — | — | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 40 | . Pac 1 H | Three/single phase grid output VA (high) | — | watt 0.1 VA — | — | — | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 41 | . Pac 1 L | Three/single phase grid output VA(low) | — | watt 0.1 VA — | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 42 | . Vac 2 | Three phase grid voltage | — | 0.1 V — | — | — | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 43 | . Iac 2 | Three phase grid output current | — | 0.1 A — | — | — | tlx:output_2_amperage, tl3:n_bus_voltage, offgrid:warning_code | N-bus voltage, Output 2 Amperage, Warning code |
| 44 | . Pac 2 H | Three phase grid output power ( | — | high) 0.1 VA — | — | — | tlx:output_2_power | Output 2 Wattage |
| 45 | . Pac 2 L | Three phase grid output power ( | — | low) 0.1 VA — | — | — | — | — |
| 46 | . Vac 3 | Three phase grid voltage | — | 0.1 V — | — | — | tlx:output_3_voltage | Output 3 voltage |
| 47 | . Iac 3 | Three phase grid output current | — | 0.1 A — | — | — | tlx:output_3_amperage, tl3:derating_mode, offgrid:constant_power | Derating mode, Output 3 Amperage |
| 48 | . Pac 3 H | Three phase grid output power ( | — | high) 0.1 VA — | — | — | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 49 | . Pac 3 L | Three phase grid output power ( | — | low) 0.1 VA — | — | — | — | — |
| 50 | . Vac_RS | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | tl3:input_1_energy_total, offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51 | . Vac_ST | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | — | — |
| 52 | . Vac_TR | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | tl3:input_2_energy_today, offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53 | . Eactoday H | Today generate energy (high) | — | 0.1 k WH — | — | — | tlx:output_energy_today | Energy produced today |
| 54 | . Eac today L | Today generate energy (low) | — | 0.1 k WH — | — | — | tl3:input_2_energy_total, offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55 | . Eac total H | Total generate energy (high) | — | 0.1 k WH — | — | — | tlx:output_energy_total | Total energy produced |
| 56 | . Eac total L | Total generate energy (low) | — | 0.1 k WH — | — | — | tl3:input_energy_total, offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today, Total energy input |
| 57 | . Time total H | Work time total (high) | — | 0.5 s — | — | — | tlx:operation_hours | Running hours |
| 58 | . Time total L | Work time total (low) | — | 0.5 s — | — | — | tl3:output_reactive_power, offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime, Reactive wattage |
| 59 | . Epv 1_today H | PV 1 Energy today(high) | — | 0.1 k Wh — | — | — | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 60 | . Epv 1_today L | PV 1 Energy today (low) | — | 0.1 k Wh — | — | — | tl3:output_reactive_energy_today, offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61 | . Epv 1_total H | PV 1 Energy total(high) | — | 0.1 k Wh — | — | — | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 62 | . Epv 1_total L | PV 1 Energy total (low) | — | 0.1 k Wh — | — | — | tl3:output_reactive_energy_total, offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63 | . Epv 2_today H | PV 2 Energy today(high) | — | 0.1 k Wh — | — | — | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 64 | . Epv 2_today L | PV 2 Energy today (low) | — | 0.1 k W h | — | — | tl3:warning_code, offgrid:ac_discharge_energy_today | AC Discharged Today, Warning code |
| 65 | . Epv 2_total H | PV 2 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_2_energy_total, tl3:warning_value | Input 2 total energy, PV2 energy produced Lifetime |
| 66 | . Epv 2_total L | PV 2 Energy total (low) | — | 0.1 k W h | — | — | tl3:real_output_power_percent, offgrid:ac_discharge_energy_total | Grid Discharged Lifetime, Real power output percentage |
| 67 | . Epv 3_today H | PV 3 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_3_energy_today | Input 3 energy today |
| 68 | . Epv 3_today L | PV 3 Energy today (low) | — | 0.1 k W h | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69 | . Epv 3_total H | PV 3 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_3_energy_total, offgrid:discharge_power | Battery discharge power, Discharge Power, Input 3 total energy |
| 70 | . Epv 3_total L | PV 3 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 71 | . Epv 4_today H | PV 4 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_4_energy_today | Input 4 energy today |
| 72 | . Epv 4_today L | PV 4 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 73 | . Epv 4_total H | PV 4 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_4_energy_total, offgrid:battery_discharge_amperage | Battery discharge current, Input 4 total energy |
| 74 | . Epv 4_total L | PV 4 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 75 | . Epv 5_today H | PV 5 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_5_energy_today | Input 5 energy today |
| 76 | . Epv 5_today L | PV 5 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 77 | . Epv 5_total H | PV 5 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_5_energy_total, offgrid:battery_power | Battery charging/ discharging(-ve), Input 5 total energy |
| 78 | . Epv 5_total L | PV 5 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 79 | . Epv 6_today H | PV 6 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_6_energy_today | Input 6 energy today |
| 80 | . Epv 6_today L | PV 6 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 81 | . Epv 6_total H | PV 6 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_6_energy_total | Input 6 total energy |
| 82 | . Epv 6_total L | PV 6 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 83 | . Epv 7_today H | PV 7 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_7_energy_today | Input 7 energy today |
| 84 | . Epv 7_today L | PV 7 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 85 | . Epv 7_total H | PV 7 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_7_energy_total | Input 7 total energy |
| 86 | . Epv 7_total L | PV 7 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 87 | . Epv 8_today H | PV 8 Energy today(high) | — | 0.1 k W h | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 88 | . Epv 8_today L | PV 8 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 89 | . Epv 8_total H | PV 8 Energy total(high) | — | 0.1 k W h | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 90 | . Epv 8_total L | PV 8 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 91 | . Epv_total H | PV Energy total(high) | — | 0.1 k W h | — | — | tlx:input_energy_total | Total energy input |
| 92 | . Epv_total L | PV Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 93 | . Temp 1 | Inverter temperature | — | 0.1 C — | — | — | tlx:inverter_temperature | Temperature |
| 94 | . Temp 2 | The inside IPM in inverter Temp | — | erature 0.1 C — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95 | . Temp 3 | Boost temperature | — | 0.1 C — | — | — | tlx:boost_temperature | Boost temperature |
| 96 | . Temp 4 | — | — | — reserved | — | — | — | — |
| 97 | . uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 98 | . P Bus Voltage | P Bus inside Voltage | — | 0.1 V — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 99 | . N Bus Voltage | N Bus inside Voltage | — | 0.1 V — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 10 | 0. IPF | Inverter output PF now | — | 0-20000 — | — | — | — | — |
| 10 | 1. Real OPPercent | Real Output power Percent | — | 1% — | — | — | — | — |
| 10 | 2. OPFullwatt H | Output Maxpower Limited high | — | — | — | — | — | — |
| 10 | 3. OPFullwatt L | Output Maxpower Limited low | — | 0.1 W — | — | — | — | — |
| 10 | 4. Derating Mode | Derating Mode 0 1 2 3 4 5 6 7 8 9 B | — | :no derate; :PV; :*; :Vac; :Fac; :Tboost; :Tinv; :Control; :*; :*Over Back y Time; — | — | — | — | — |
| 10 | 5. Fault Maincode | Inverter fault maincode | — | — | — | — | — | — |
| 10 | 6. | — | — | — | — | — | — | — |
| 10 | 7. Fault Subcode | Inverter fault subcode | — | — | — | — | — | — |
| 10 | 8. Remote Ctrl En | / 0 1 | — | / St .Load First er .Bat First orage Pow (SPA) | — | — | — | — |
| 10 | 9. Remote Ctrl Pow er | / 2 | — | / St .Grid er orage Pow (SPA) | — | — | — | — |
| 11 | 0. Warning bit H | Warning bit H | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 1. Warn Subcode | Inverter warn subcode | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 2. Warn Maincode EACharge_Today _H | Inverter warn maincode ACCharge energy today | — | 0.1 kwh St Po orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 3. real Power Percent EACharge_Today _L | real Power Percent 0 ACCharge energy today | — | -100 % MA 0.1 kwh St Po X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 4. inv start delay i time EACharge_Total _H | nv start delay time ACCharge energy total | — | MA 0.1 kwh St Po X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 5. b INVAll Fault Cod e EACharge_Total _L | b INVAll Fault Code ACCharge energy total | — | MA 0.1 kwh St Po X orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 6. AC charge Power_H | Grid power to local load | — | 0.1 kwh St Po orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 7. AC charge Power_L | Grid power to local load | — | 0.1 kwh St Po orage wer | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 8. Priority | 0:Load First 1:Battery First 2:Grid First | — | St orage Power | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 9. Battery Type | 0:Lead-acid 1:Lithium battery | — | — Storage Power | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12 | 0. Auto Proofread C MD | Aging mode Auto-cal command | — | ibration Storage Power | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 4. reserved | — | — | — reserved | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 5. PID PV 1+ Voltage | PID PV 1 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 6. PID PV 1+ Current | PID PV 1 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 7. PID PV 2+ Voltage | PID PV 2 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 8. PID PV 2+ Current | PID PV 2 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 9. PID PV 3+ Voltage | PID PV 3 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 13 | 0. PID PV 3+ Current | PID PV 3 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 1. PID PV 4+ Voltage | PID PV 4 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 2. PID PV 4+ Current | PID PV 4 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 3. PID PV 5+ Voltage | PID PV 5 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 4. PID PV 5+ Current | PID PV 5 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 5. PID PV 6+ Voltage | PID PV 6 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 6. PID PV 6+ Current | PID PV 6 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 7. PID PV 7+ Voltage | PID PV 7 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 8. PID PV 7+ Current | PID PV 7 PE Curr | — | -10~10 m A 0.1 m A | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 13 | 9. PID PV 8+ Voltage | PID PV 8 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 14 | 0. PID PV 8+ Current | PID PV 8 PE Curr | — | -10~10 m A 0.1 m A | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 1. PID Status | Bit 0~7:PID Working Status 1:Wait Status 2:Normal Status 3:Fault Status Bit 8~15:Reversed | — | 0~3 — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 2. V _String 1 | PV String 1 voltage | — | 0.1 V | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 3. Curr _String 1 | PV String 1 current | — | -15~15 A 0.1 A | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 4. V _String 2 | PV String 2 voltage | — | 0.1 V | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 5. Curr _String 2 | PV String 2 current | — | -15~15 A 0.1 A — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 6. V _String 3 | PV String 3 voltage | — | 0.1 V — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 7. Curr _String 3 | PV String 3 current | — | -15~15 A 0.1 A — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 8. V _String 4 | PV String 4 voltage | — | 0.1 V — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 14 | 9. Curr _String 4 | PV String 4 current | — | -15~15 A 0.1 A — | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 15 | 0. V _String 5 | PV String 5 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 1. Curr _String 5 | PV String 5 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 2. V _String 6 | PV String 6 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 3. Curr _String 6 | PV String 6 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 4. V _String 7 | PV String 7 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 5. Curr _String 7 | PV String 7 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 6. V _String 8 | PV String 8 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 7. Curr _String 8 | PV String 8 current | — | -15 A~15 A 0.1 A — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 8. V _String 9 | PV String 9 voltage | — | 0.1 V — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 15 | 9. Curr _String 9 | PV String 9 current | — | -15 A~15 A 0.1 A — | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16 | 0. V _String 10 | PV String 10 voltage | — | 0.1 V — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 1. Curr _String 10 | PV String 10 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 2. V _String 11 | PV String 11 voltage | — | 0.1 V — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 3. Curr _String 11 | PV String 11 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 4. V _String 12 | PV String 12 voltage | — | 0.1 V — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 5. Curr _String 12 | PV String 12 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 6. V _String 13 | PV String 13 voltage | — | 0.1 V — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 7. Curr _String 13 | PV String 13 current | — | -15 A~15 A 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 8. V _String 14 | PV String 14 voltage | — | 0.1 V — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 16 | 9. Curr _String 14 | PV String 14 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17 | 0. V _String 15 | PV String 15 voltage | — | 0.1 V — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 1. Curr _String 15 | PV String 15 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 2. V _String 16 | PV String 16 voltage | — | 0.1 V — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 3. Curr _String 16 | PV String 16 current | — | -15~15 A 0.1 A — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 4. Str Unmatch | Bit 0~15: String 1~16 unmatch | — | — suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 5. Str Current Unblan ce | Bit 0~15: String 1~16 current u | — | nblance suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 6. Str Disconnect | Bit 0~15: String 1~16 disconnec | — | t suggestive | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 7. PIDFault Code | Bit 0:Output over voltage Bit 1: ISO fault Bit 2: BUS voltage abnormal Bit 3~15:reserved | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 8. String Prompt | String Prompt Bit 0:String Unmatch Bit 1:Str Disconnect Bit 2:Str Current Unblance Bit 3~15:reserved | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 17 | 9 PV Warning Value | PV Warning Value | — | — | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 18 | 0 DSP 075 Warning Value | DSP 075 Warning Value | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 1 DSP 075 Fa Value | ult DSP 075 Fault Value | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 2 DSP 067 Debu Data 1 | g DSP 067 Debug Data 1 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 3 DSP 067 Debu Data 2 | g DSP 067 Debug Data 2 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 4 DSP 067 Debu Data 3 | g DSP 067 Debug Data 3 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 5 DSP 067 Debu Data 4 | g DSP 067 Debug Data 4 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 6 DSP 067 Debu Data 5 | g DSP 067 Debug Data 5 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 7 DSP 067 Debu Data 6 | g DSP 067 Debug Data 6 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 8 DSP 067 Debu Data 7 | g DSP 067 Debug Data 7 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 18 | 9 DSP 067 Debu Data 8 | g DSP 067 Debug Data 8 | — | — | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 19 | 0 DSP 075 Debu Data 1 | g DSP 075 Debug Data 1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 1 DSP 075 Debu Data 2 | g DSP 075 Debug Data 2 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 2 DSP 075 Debu Data 3 | g DSP 075 Debug Data 3 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 3 DSP 075 Debu Data 4 | g DSP 075 Debug Data 4 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 4 DSP 075 Debu Data 55 | g DSP 075 Debug Data 5 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 5 DSP 075 Debu Data 6 | g DSP 075 Debug Data 6 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 6 DSP 075 Debu Data 7 | g DSP 075 Debug Data 7 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 7 DSP 075 Debu Data 8 | g DSP 075 Debug Data 8 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 8 b USBAging Test Ok Flag | USBAging Test Ok Flag 0-1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 19 | 9 b Flash Erase Aging Ok Flag | Flash Erase Aging Ok Flag 0-1 | — | — | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20 | 0 PVISO | PVISOValue | — | KΩ — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 1 R_DCI | R DCI Curr | — | 0.1 m A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 2 S_DCI | S DCI Curr | — | 0.1 m A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 3 T_DCI | T DCI Curr | — | 0.1 m A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 4 PID_Bus | PIDBus Volt | — | 0.1 V — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 5 GFCI | GFCI Curr | — | m A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 6 SVG/APF Status+SVGAPFEq ual Ratio | SVG/APF Status+SVGAPFEqual Rat | — | io High 8 bit: SVGAPFEqua l Ratio Low 8 bit: SVG/APF Status 0:None 1:SVG Run 2:APF Run 3:SVG/APF Run — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 7 CT_I _R | R phase load side current for | — | SVG 0.1 A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 8 CT_I _S | S phase load side current for | — | SVG 0.1 A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 9 CT_I _T | T phase load side current for | — | SVG 0.1 A — | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | 0 CT_Q _R H | R phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 1 CT_Q _R L | R phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 2 CT_Q _S H | S phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 3 CT_Q _S L | S phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 4 CT_Q _T H | T phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 5 CT_Q _T L | T phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 6 CT HAR_I_R | R phase load side harmonic | — | 0.1 A — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 7 CT HAR_I_S | S phase load side harmonic | — | 0.1 A — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 8 CT HAR_I_T | T phase load side harmonic | — | 0.1 A — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 9 COMP_Q _R H | R phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 22 | 0 COMP_Q _R L | R phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 1 COMP_Q _S H | S phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 2 COMP_Q _S L | S phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 3 COMP_Q _T H | T phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 4 COMP_Q _T L | T phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 5 COMP HAR_I_R | R phase compensate harmonic f SVG | — | or 0.1 A — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 6 COMP HAR_I_S | S phase compensate harmonic f SVG | — | or 0.1 A — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 7 COMP HAR_I_T | T phase compensate harmonic f SVG | — | or 0.1 A — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 8 b RS 232 Aging Test Ok Flag | RS 232 Aging Test Ok Flag | — | 0-1 — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 22 | 9 b Fan Fault Bit | Bit 0: Fan 1 fault bit Bit 1: Fan 2 fault bit Bit 2: Fan 3 fault bit Bit 3: Fan 4 fault bit Bit 4-7: Reserved | — | — | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 23 | 0 Sac H | Output apparent power H | — | 0.1 W — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 1 Sac L | Output apparent power L | — | 0.1 W — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 2 Re Act Power H | Real Output Reactive Power H | — | Int 32 0.1 W — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 3 Re Act Power L | Real Output Reactive Power L | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 4 Re Act Power Max H | Nominal Output Reactive Power | — | H 0.1 var — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 5 Re Act Power Max L | Nominal Output Reactive Power | — | L — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 6 Re Act Power_Total H | Reactive power generation | — | 0.1 kwh — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 7 Re Act Power_Total L | Reactive power generation | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 8 b Afci Status | 0:Waiting 1:Self-check state 2:Detect pull arc state 3:Fault 4:Update | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 23 | 9 uw Present FFTValu e [CHANNEL_A] | Present FFTValue [CHANNEL_A] | — | — | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24 | 0 uw Present FFTValu e [CHANNEL_B] | Present FFTValue [CHANNEL_B] | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 1 DSP 067 Deb Data 1 | ug DSP 067 Debug Data 1 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 2 DSP 067 Deb Data 2 | ug DSP 067 Debug Data 2 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 3 DSP 067 Deb Data 3 | ug DSP 067 Debug Data 3 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 4 DSP 067 Debu Data 4 | g DSP 067 Debug Data 4 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 5 DSP 067 Debu Data 5 | g DSP 067 Debug Data 5 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 6 DSP 067 Debu Data 6 | g DSP 067 Debug Data 6 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 7 DSP 067 Debu Data 7 | g DSP 067 Debug Data 7 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 8 DSP 067 Debu Data 8 | g DSP 067 Debug Data 8 | — | — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 24 | 9 | — | — | reserved — | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 87 | 5 Vpv 9 | PV 9 voltage | — | 0.1 V — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | 6 PV 9 Curr | PV 9 Input current | — | 0.1 A — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | 7 Ppv 9 H | PV 9 input power (High) | — | 0.1 W — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | 8 Ppv 9 L | PV 9 input power (Low) | — | 0.1 W — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 87 | 9 Vpv 10 | PV 10 voltage | — | 0.1 V — | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 88 | 0 PV 10 Curr | PV 10 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 1 Ppv 10 H | PV 10 input power (High) | — | 0.1 W — | — | — | — | — |
| 88 | 2 Ppv 10 L | PV 10 input power (Low) | — | 0.1 W — | — | — | — | — |
| 88 | 3 Vpv 11 | PV 11 voltage | — | 0.1 V — | — | — | — | — |
| 88 | 4 PV 11 Curr | PV 11 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 5 Ppv 11 H | PV 11 input power (High) | — | 0.1 W — | — | — | — | — |
| 88 | 6 Ppv 11 L | PV 11 input power (Low) | — | 0.1 W — | — | — | — | — |
| 88 | 7 Vpv 12 | PV 12 voltage | — | 0.1 V — | — | — | — | — |
| 88 | 8 PV 12 Curr | PV 12 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 9 Ppv 12 H | PV 12 input power (High) | — | 0.1 W — | — | — | — | — |
| 89 | 0 Ppv 12 L | PV 12 input power (Low) | — | 0.1 W — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 1 Vpv 13 | PV 13 voltage | — | 0.1 V — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 2 PV 13 Curr | PV 13 Input current | — | 0.1 A — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 3 Ppv 13 H | PV 13 input power (High) | — | 0.1 W — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 4 Ppv 13 L | PV 13 input power (Low) | — | 0.1 W — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 5 Vpv 14 | PV 14 voltage | — | 0.1 V — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 6 PV 14 Curr | PV 14 Input current | — | 0.1 A — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 7 Ppv 14 H | PV 14 input power (High) | — | 0.1 W — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 8 Ppv 14 L | PV 14 input power (Low) | — | 0.1 W — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 89 | 9 Vpv 15 | PV 15 voltage | — | 0.1 V — | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 90 | 0 PV 15 Curr | PV 15 Input current | — | 0.1 A — | — | — | — | — |
| 90 | 1 Ppv 15 H | PV 15 input power (High) | — | 0.1 W — | — | — | — | — |
| 90 | 2 Ppv 15 L | PV 15 input power (Low) | — | 0.1 W — | — | — | — | — |
| 90 | 3 Vpv 16 | PV 16 voltage | — | 0.1 V — | — | — | — | — |
| 90 | 4 PV 16 Curr | PV 16 Input current | — | 0.1 A — | — | — | — | — |
| 90 | 5 Ppv 16 H | PV 16 input power (High) | — | 0.1 W — | — | — | — | — |
| 90 | 6 Ppv 16 L | PV 16 input power (Low) | — | 0.1 W — | — | — | — | — |
| 90 | 7 Epv 9_today H | PV 9 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 90 | 8 Epv 9_today L | PV 9 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 90 | 9 Epv 9_total H | PV 9 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 0 Epv 9_total L | PV 9 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 1 Epv 10_today H | PV 10 energy today (High) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 2 Epv 10_today L | PV 10 energy today (Low) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 3 Epv 10_total H | PV 10 energy total (High) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 4 Epv 10_total L | PV 10 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 5 Epv 11_today H | PV 11 energy today (High) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 6 Epv 11_today L | PV 11 energy today (Low) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 7 Epv 11_total H | PV 11 energy total (High) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 8 Epv 11_total L | PV 11 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 91 | 9 Epv 12_today H | PV 12 energy today (High) | — | 0.1 k Wh — | — | — | tlx:input_energy_total | Total energy input |
| 92 | 0 Epv 12_today L | PV 12 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 1 Epv 12_total H | PV 12 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 2 Epv 12_total L | PV 12 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 3 Epv 13_today H | PV 13 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 4 Epv 13_today L | PV 13 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 5 Epv 13_total H | PV 13 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 6 Epv 13_total L | PV 13 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 7 Epv 14_today H | PV 14 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 8 Epv 14_today L | PV 14 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 9 Epv 14_total H | PV 14 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 0 Epv 14_total L | PV 14 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 1 Epv 15_today H | PV 15 energy today (High) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 2 Epv 15_today L | PV 15 energy today (Low) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 3 Epv 15_total H | PV 15 energy total (High) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 4 Epv 15_total L | PV 15 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 5 Epv 16_today H | PV 16 energy today (High) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 6 Epv 16_today L | PV 16 energy today (Low) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 7 Epv 16_total H | PV 16 energy total (High) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 8 Epv 16_total L | PV 16 energy total (Low) | — | 0.1 k Wh — | — | — | tlx:inverter_temperature | Temperature |
| 93 | 9 PID PV 9+ Voltage | PID PV 9 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V — | — | — | tlx:inverter_temperature | Temperature |
| 94 | 0 PID PV 9+ Current | PID PV 9 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 1 PID PV 10 Voltage | + PID PV 10 PE/ Flyspan voltage ( HV) | — | MAX 0~1000 V 0.1 V — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 2 PID PV 1 Current | 0+ PID PV 10 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 3 PID PV 1 Voltage | 1+ PID PV 11 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 4 PID PV 1 Current | 1+ PID PV 11 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 5 PID PV 1 Voltage | 2+ PID PV 12 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 6 PID PV 1 Current | 2+ PID PV 12 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 7 PID PV 1 Voltage | 3+ PID PV 13 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 8 PID PV 1 Current | 3+ PID PV 13 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 94 | 9 PID PV 1 Voltage | 4+ PID PV 14 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95 | 0 PID PV 1 Current | 4+ PID PV 14 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 1 PID PV 1 Voltage | 5+ PID PV 15 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 2 PID PV 1 Current | 5+ PID PV 15 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 3 PID PV 1 Voltage | 6+ PID PV 16 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 4 PID PV 1 Current | 6+ PID PV 16 PE Current | — | -10~10 m A 0.1 m A — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 5 V _String 17 | PV String 17 voltage | — | 0.1 V — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 6 Curr _String 17 | PV String 17 Current | — | -15~15 A 0.1 A — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 7 V _String 18 | PV String 18 voltage | — | 0.1 V — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 8 Curr _String 18 | PV String 18 Current | — | -15~15 A 0.1 A — | — | — | tlx:boost_temperature | Boost temperature |
| 95 | 9 V _String 19 | PV String 19 voltage | — | 0.1 V — | — | — | tlx:boost_temperature | Boost temperature |
| 96 | 0 Curr _String 19 | PV String 19 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 1 V _String 20 | PV String 20 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 2 Curr _String 20 | PV String 20 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 3 V _String 21 | PV String 21 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 4 Curr _String 21 | PV String 21 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 5 V _String 22 | PV String 22 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 6 Curr _String 22 | PV String 22 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 7 V _String 23 | PV String 23 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 8 Curr _String 23 | PV String 23 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 9 V _String 24 | PV String 24 voltage | — | 0.1 V — | — | — | — | — |
| 97 | 0 Curr _String 24 | PV String 24 Current | — | -15 A~15 A 0.1 A | — | — | — | — |
| 97 | 1 V _String 25 | PV String 25 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 2 Curr _String 25 | PV String 25 Current | — | -15 A~15 A 0.1 A | — | — | — | — |
| 97 | 3 V _String 26 | PV String 26 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 4 Curr _String 26 | PV String 26 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 5 V _String 27 | PV String 27 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 6 Curr _String 27 | PV String 27 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 7 V _String 28 | PV String 28 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 8 Curr _String 28 | PV String 28 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 9 V _String 29 | PV String 29 voltage | — | — 0.1 V | — | — | — | — |
| 98 | 0 Curr _String 29 | PV String 29 Current | — | -15 A~15 A 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 1 V _String 30 | PV String 30 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 2 Curr _String 30 | PV String 30 Current | — | -15~15 A 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 3 V _String 31 | PV String 31 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 4 Curr _String 31 | PV String 31 Current | — | -15~15 A 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 5 V _String 32 | PV String 32 voltage | — | — 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 6 Curr _String 32 | PV String 32 Current | — | -15~15 A 0.1 A | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 7 Str Unmatch 2 | Bit 0~15: String 17~32 unmatch | — | — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 8 Str Current Unblan ce 2 | Bit 0~15:String 17~32 unblance | — | current — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 98 | 9 Str Disconnect 2 | Bit 0~15: String 17~32 disconn | — | ect — | — | — | tlx:p_bus_voltage | P-bus voltage |
| 99 | 0 PV Warning Value | PV Warning Value (PV 9-PV 16) Contains PV 9~16 abnormal , 和 Boost 9~16 Drive anomalies | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | 1 Str Waringvalue 1 | string 1~string 16 abnormal | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | 2 Str Waringvalue 2 | string 17~string 32 abnormal | — | — | — | — | tlx:n_bus_voltage | N-bus voltage |
| 99 | 9 System Cmd | M 3 to DSP system command | — | — system command | — | — | tlx:n_bus_voltage | N-bus voltage |
| 10 | 00. uw Sys Work Mode | System work mode | — | 0 x 00:waiting module 0 x 01: Self-test mode, optional 0 x 02 : Reserved 0 x 03:Sys Fault module 0 x 04: Flash module 0 x 05 : m PVBATOnline 0 module, x 0 x 06 : m Bat Online module, 0 x 07 : PVOffline Mod e module, 0 x 08 : Bat Offline Mo de module, Theworkingmode displayed by the monitoring to the customer is: 0 x 00: waiting module 0 x 01: Self-test mode, 0 x 03:fault module 0 x 04:flash odule x 05|0 x 06|0 x 07|0 08:normal odule | — | — | — | — |
| 10 | 01. Systemfault word 0 | System fault word 0 | — | P t d H lease refer to hefault escription of ybrid | — | — | — | — |
| 10 | 02. Systemfault word 1 | System fault word 1 | — | — | — | — | — | — |
| 10 | 03. Systemfault word 2 | System fault word 2 | — | — | — | — | — | — |
| 10 | 04. Systemfault word 3 | System fault word 3 | — | — | — | — | — | — |
| 10 | 05. Systemfault word 4 | System fault word 4 | — | — | — | — | — | — |
| 10 | 06. Systemfault word 5 | System fault word 5 | — | — | — | — | — | — |
| 10 | 07. Systemfault word 6 | System fault word 6 | — | — | — | — | — | — |
| 10 | 08. Systemfault word 7 | System fault word 7 | — | — | — | — | — | — |
| 10 | 09. Pdischarge 1 H | Discharge power(high) | — | 0.1 W — | — | — | — | — |
| 10 | 10. Pdischarge 1 L | Discharge power (low) | — | 0.1 W — | — | — | — | — |
| 10 | 11. Pcharge 1 H | Charge power(high) | — | 0.1 W — | — | — | — | — |
| 10 | 12. Pcharge 1 L | Charge power (low) | — | 0.1 W — | — | — | — | — |
| 10 | 13. Vbat | Battery voltage | — | 0.1 V — | — | — | — | — |
| 10 | 14. SOC | State of charge Capacity | — | 0-100 1% l ith/leadacid | — | — | — | — |
| 10 | 15. Pactouser R | H AC power to user H | — | 0.1 w — | — | — | — | — |
| 10 | 16. Pactouser R | L AC power to user L | — | 0.1 w — | — | — | — | — |
| 10 | 17. Pactouser S | H Pactouser S H | — | 0.1 w — | — | — | — | — |
| 10 | 18. Pactouser S | L Pactouser S L | — | 0.1 w — | — | — | — | — |
| 10 | 19. Pactouser T | H Pactouser T H | — | 0.1 w — | — | — | — | — |
| 10 | 20. Pactouser T | L Pactouser T H | — | 0.1 w — | — | — | — | — |
| 10 | 21. Pactouser Total H | AC power to user total H | — | 0.1 w — | — | — | — | — |
| 10 | 22. Pactouser Total L | AC power to user total L | — | 0.1 w — | — | — | — | — |
| 10 | 23. Pac to grid R H | AC power to grid H | — | 0.1 w A c output | — | — | — | — |
| 10 | 24. Pac to grid R L | AC power to grid L | — | 0.1 w — | — | — | — | — |
| 10 | 25. Pactogrid S H | — | — | 0.1 w — | — | — | — | — |
| 10 | 26. Pactogrid S L | — | — | 0.1 w — | — | — | — | — |
| 10 | 27. Pactogrid T H | — | — | 0.1 w — | — | — | — | — |
| 10 | 28. Pactogrid T L | — | — | 0.1 w — | — | — | — | — |
| 10 | 29. Pactogrid total H | AC power to grid total H | — | 0.1 w — | — | — | — | — |
| 10 | 30. Pactogrid total L | AC power to grid total L | — | 0.1 w — | — | — | — | — |
| 10 | 31. PLocal Load R | H INV power to local load H | — | 0.1 w — | — | — | — | — |
| 10 | 32. PLocal Load R | L INV power to local load L | — | 0.1 w — | — | — | — | — |
| 10 | 33. PLocal Load S | H | — | 0.1 w — | — | — | — | — |
| 10 | 34. PLocal Load S | L | — | 0.1 w — | — | — | — | — |
| 10 | 35. PLocal Load T H | — | — | 0.1 w — | — | — | — | — |
| 10 | 36. PLocal Load T L | — | — | 0.1 w — | — | — | — | — |
| 10 | 37. PLocal Load total | H INV power to local load tot | — | al H 0.1 w — | — | — | — | — |
| 10 | 38. PLocal Load total | L INV power to local load tot L | — | al 0.1 w — | — | — | — | — |
| 10 | 39. IPM 2 Temperature | REC Temperature | — | 0.1℃ No use — | — | — | — | — |
| 10 | 40. Battery 2 Temperature | Battery Temperature | — | 0.1℃ Lead acid/l battery tem ithium p | — | — | — | — |
| 10 | 41. SP DSP Status | SP state | — | CHG/Dis CHG — | — | — | — | — |
| 10 | 42. SP Bus Volt | SP BUS 2 Volt | — | 0.1 V — | — | — | — | — |
| 10 | 43 | — | — | — | — | — | — | — |
| 10 | 44. Etouser_today H | Energy to user today high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 45. Etouser_today L | Energy to user today low | — | 0.1 k Wh — | — | — | — | — |
| 10 | 46. Etouser_total H | Energy to user total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 47. Etouser_ total L | Energy to user total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 48. Etogrid_today H | Energy to grid today high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 49. Etogrid _today L | Energy to grid today low | — | 0.1 k Wh — | — | — | — | — |
| 10 | 50. Etogrid _total H | Energy to grid total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 51. Etogrid _ total L | Energy to grid total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 52. Edischarge 1_toda y H | Discharge energy 1 today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 53. Edischarge 1_toda y L | Discharge energy 1 today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 54. Edischarge 1_total H | Total discharge energy 1 (high) | — | 0.1 k Wh — | — | — | — | — |
| 10 | 55. Edischarge 1_total L | Total discharge energy 1 (low) | — | 0.1 k Wh — | — | — | — | — |
| 10 | 56. Echarge 1_today H | Charge 1 energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 57. Echarge 1_today L | Charge 1 energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 58. Echarge 1_total H | Charge 1 energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 59. Echarge 1_total L | Charge 1 energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 60. ELocal Load_Today H | Local load energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 61. ELocal Load_Today L | Local load energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 62. ELocal Load_Total H | Local load energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 63. ELocal Load_Total L | Local load energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 64. dw Export Limit Ap parent Power | Export Limit Apparent Power H | — | 0.1 k Wh Appa rent Power | — | — | — | — |
| 10 | 65. dw Export Limit Ap parent Power | Export Limit Apparent Power L | — | 0.1 k Wh Appa rent Power | — | — | — | — |
| 10 | 66. / | / | — | / / rese rved | — | — | — | — |
| 10 | 67. EPS Fac | UPSfrequency | — | 5000/6000 0.01 Hz — | — | — | — | — |
| 10 | 68. EPS Vac 1 | UPS phase R output voltage | — | 2300 0.1 V — | — | — | — | — |
| 10 | 69. EPS Iac 1 | UPS phase R output current | — | 0.1 A — | — | — | — | — |
| 10 | 70. EPS Pac 1 H | UPS phase R output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 71. EPS Pac 1 L | UPS phase R output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 72. EPS Vac 2 | UPS phase S output voltage | — | 0.1 V — | — | — | — | — |
| 10 | 73. EPS Iac 2 | UPS phase S output current | — | 0.1 A No u se | — | — | — | — |
| 10 | 74. EPS Pac 2 H | UPS phase S output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 75. EPS Pac 2 L | UPS phase S output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 76. EPS Vac 3 | UPS phase T output voltage | — | 0.1 V — | — | — | — | — |
| 10 | 77. EPS Iac 3 | UPS phase T output current | — | 0.1 A No u se | — | — | — | — |
| 10 | 78. EPS Pac 3 H | UPS phase T output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 79. EPS Pac 3 L | UPS phase T output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 80. Loadpercent | Load percent of UPS ouput | — | 0-100 1% — | — | — | — | — |
| 10 | 81. PF | Power factor | — | 0-2 0.1 Prim ary Value+1 | — | — | — | — |
| 10 | 82. BMS_Status Old | Status Old from BMS | — | Detail information, refer — | — | — | — | — |
| 10 | 83. BMS_Status | Status from BMS | — | to W/R — | — | — | — | — |
| 10 | 84. BMS_Error Old | Error info Old from BMS | — | document:Growattxx Sxx — | — | — | — | — |
| 10 | 85. BMS_Error | Errorinfomation from BMS | — | P ESS Protocol; — | — | — | — | — |
| 10 | 86. BMS_SOC BMS_Battery Vol | SOC from BMS Battery voltage from BMS | — | R SP R SP H 6 K H 6 K | — | — | — | — |
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
| 11 | 00. rr BMS_MCUVersi | MCU Software version from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 01. on BMS_Gauge Vers | Gauge Version from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 02. ion BMS_w Gauge FR | Gauge FR Version L 16 from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 03. Version_ L BMS_w Gauge FR | Gauge FR Version H 16 from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 04. Version_H | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 05. BMS_BMSInfo | BMSInformation from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 06. BMS_Pack Info | Pack Information from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 07. BMS_Using Cap | Using Cap from BMS | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 08. uw Max Cell Volt | Maximum single battery voltage | — | 0.001 V — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 09. uw Min Cell Volt | Lowest single battery voltage | — | 0.001 V — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 10. b Module Num | Battery parallel number | — | 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 11. uw Max Volt Cell N | Number of batteries Max Volt Cell No | — | 1 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 12. o uw Min Volt Cell N | Min Volt Cell No | — | 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 13. o uw Max Tempr Ce | Max Tempr Cell_10 T | — | 0.1℃ — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 14. ll_10 T uw Min Tempr Cel | Min Tempr Cell_10 T | — | 0.1℃ — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 15. l_10 T uw Max Tempr Ce | Max Volt Tempr Cell No | — | 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 16. ll No | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 17. uw Min Tempr Cel l No | Min Volt Tempr Cell No | — | 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 18. Protect pack ID | Faulty Battery Address | — | 1 — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 19. Max SOC | Parallel maximum SOC | — | 1% — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 20. Min SOC BMS_Error 2 | Parallel minimum SOC Battery Protection 2 | — | 1% - CAN ID : 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 21. BMS_Error 3 | Battery Protection 3 | — | - Byte 4~5 CAN ID : 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 22. BMS_Warn Info 2 | Battery Warn 2 | — | - Byte 6 CAN ID : 0 x 323 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 23. | — | — | — Byte 7 | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 24 AC Charge Energy Today H | AC Charge Energy today | — | kwh Energy today | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 25. ACCharge Energy Today L | AC Charge Energy today | — | kwh — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 26. 1 Charge AC Energy Total H | — | — | — Energy total | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 27. ACCharge Energy Total L | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 28. AC Charge Power H | AC Charge Power | — | W — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 29. AC Charge Power L | AC Charge Power | — | w — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 30. 70% INV Power adjust | uw Grid Power_70_Adj EE_SP | — | W — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 31. Extra AC Power Ex to grid_H Hi | tra inverte AC Power to grid gh | — | For SPA connect inverter SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 32. Extra AC Power Ex to grid_L | trainverte AC Power to grid Low | — | — SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 33. Eextra_today H | Extra inverter Power TOUser_Extr today (high) | — | a R 0.1 k Wh SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 34. Eextra_today L | Extra inverter Power TOUser_Extr today (low) | — | a R 0.1 k Wh SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 35. Eextra_total H | Extra inverter Power TOUser_Extr total(high) | — | a 0.1 k Wh SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 36. Eextra_total L | Extra inverter Power TOUser_Extr total(low) | — | a 0.1 k Wh SPA used | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 37. Esystem_today H | System electric energy today H | — | 0.1 k Wh SPA used System electric energy today H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 38. Esystem_ today Sy L | stem electric energy today L | — | 0.1 k Wh SPA use System energy d electric today L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 39. Esystem_total H | System electric energy total H | — | 0.1 k Wh SPA use System energy d electric total H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 40. Esystem_ total L | System electric energy total L | — | 0.1 k Wh SPA use System energy d electric total L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 41. Eself_today H | self electric energy today H | — | 0.1 k Wh self energy electric today H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 42. Eself_ today L | self electric energy today L | — | 0.1 k Wh self energy electric today L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 43. Eself_total H | self electric energy total H | — | 0.1 k Wh self energy electric total H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 44. Eself_ total L | self electric energy total L | — | 0.1 k Wh self energy electric total L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 45. PSystem H | System power H | — | 0.1 w System power H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 46. PSystem L | System power L | — | 0.1 w System power L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 47. PSelf H | self power H | — | 0.1 w self po wer H | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 48. PSelf L | self power L | — | 0.1 w self po wer L | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 49. EPVAll_Today H | PV electric energy today H | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 50. EPVAll_Today L | PV electric energy today L | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 51. Ac Discharge Pack Sn | Discharge power pack number | — | serial R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 52. Accdischarge power_H | Cumulative discharge power high 16-bit byte | — | R 0.1 k WH — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 53. Accdischarge power_L | Cumulative discharge power low 16-bit byte | — | R 0.1 k WH — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 54. Acc Charge Pack Sn | charge power pack serial number | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 55. Acc Charge power_H | Cumulative charge power high R 16-bit byte | — | 0.1 k WH — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 56. Acc Charge power_L | Cumulative charge power low R 16-bit byte | — | 0.1 k WH — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 57. First Batt Fault Sn | First Batt Fault Sn | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 58. Second Batt Fault Sn | Second Batt Fault Sn | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 59. Third Batt Fault Sn | Third Batt Fault Sn | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 60. Fourth Batt Fault Sn | Fourth Batt Fault Sn | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 61. Battery history fault code 1 | Battery history fault code 1 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 62. Battery history fault code 2 | Battery history fault code 2 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 63. Battery history fault code 3 | Battery history fault code 3 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 64. Battery history fault code 4 | Battery history fault code 4 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 65. Battery history fault code 5 | Battery history fault code 5 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 66. Battery history fault code 6 | Battery history fault code 6 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 67. Battery history fault code 7 | Battery history fault code 7 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 68. Battery history fault code 8 | Battery history fault code 8 | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 69. Number of battery codes | Number of battery codes PACK number + BIC forward and reverse codes | — | R / — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 70. | — | — | — | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 11 | 99 New EPower Calc Flag | Intelligent reading is used to identify software compatibility features | — | 0 : Old ene calculation 1 : new ene calculation rgy ; rgy | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 1 | 200 Max Cell Volt | Maximum cell voltage | — | R 0.001 V — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 201 Min Cell Volt | Minimum cell voltage | — | R 0.001 V — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 202 Module Num | Number of Battery modules | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 203 Total Cell Num | Total number of cells | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 204 Max Volt Cell No | Max Volt Cell No | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 205 Min Volt Cell No | Min Volt Cell No | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 206 Max Tempr Cell_ 10 T | Max Tempr Cell_10 T | — | R 0.1℃ — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 207 Min Tempr Cell_1 0 T | Min Tempr Cell_10 T | — | R 0.1℃ — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 208 Max Tempr Cell N o | Max Tempr Cell No | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 209 Min Tempr Cell N o | Min Tempr Cell No | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 210 Protect Pack ID | Fault Pack ID | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 211 Max SOC | Parallel maximum SOC | — | R 1% — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 212 Min SOC | Parallel minimum SOC | — | R 1% — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 213 Bat Protect 1 Add | Bat Protect 1 Add | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 214 Bat Protect 2 Add | Bat Protect 2 Add | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 215 Bat Warn 1 Add | Bat Warn 1 Add | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 216 BMS_Highest Sof t Version | BMS_Highest Soft Version | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 217 BMS_Hardware Version | BMS_Hardware Version | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 1 | 218 BMS_Request Ty pe | BMS_Request Type | — | R / — | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 12 | 48 b Key Aging Test O k Flag | Success sign of key detection before aging | — | — 1:Finished test 0 : test not completed | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 12 | 49. / | / | — | / / reversed | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 20 | 00 Inverter Status | Inverter run state | — | 0:waiting, 1:normal, 3:fault SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 35 Pac H | Output power (high) | — | 0. 1 W SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 36 Pac L | Output power (low) | — | 0. 1 W SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 37 Fac | Grid frequency | — | 0. 01 Hz SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 38 Vac 1 | Three/single phase grid voltage | — | 0. 1 V SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 39 Iac 1 | Three/single phase grid output | — | current 0. 1 A SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 40 Pac 1 H | Three/single phase grid output VA (high) | — | watt 0. 1 VA SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 41 Pac 1 L | Three/single phase grid output VA(low) | — | watt 0. 1 VA SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 53 Eac today H | Today generate energy (high) | — | 0. 1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 54 Eac today L | Today generate energy (low) | — | 0. 1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 55 Eac total H | Total generate energy (high) | — | 0.1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 56 Eac total L | Total generate energy (low) | — | 0.1 k WH SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 57 Time total H | Work time total (high) | — | 0.5 s SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 58 Time total L | Work time total (low) | — | 0.5 s SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 93 Temp 1 | Inverter temperature | — | 0.1 C SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 94 Temp 2 | The inside IPM in inverter Temp | — | erature 0.1 C SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 95 Temp 3 | Boost temperature | — | 0.1 C SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 96 Temp 4 | — | — | — reserved | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 97 uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 98 P Bus Voltage | P Bus inside Voltage | — | 0.1 V SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 20 | 99 N Bus Voltage | N Bus inside Voltage | — | 0.1 V SPA | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21 | 00 Remote Ctrl En | / | — | / 0.Load First 1.Bat First Remote setup enable | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 01 Remote Ctrl Pow er | / | — | 2.Grid / Remotely set power | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 02 Extra AC Power to grid_H | Extra inverte AC Power to grid | — | High For SPA connect inverter SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 03 Extra AC Power to grid_L | Extrainverte AC Power to grid L | — | ow SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 04 Eextra_today H | Extra inverter Power TOUser_Extr today (high) | — | a R 0.1 k Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 05 Eextra_today L | Extra inverter Power TOUser_Extr today (low) | — | a R 0.1 k Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 06 Eextra_total H | Extra inverter Power TOUser_Extratotal(high) | — | 0.1 k Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 07 Eextra_total L | Extra inverter Power TOUser_Extr total(low) | — | a 0.1 k Wh SPA used | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 08 Esystem_today H | System electric energy today H | — | 0.1 k Wh SPA used System electric energy today H | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 09 Esystem_ today Sy L | stem electric energy today L | — | 0.1 k Wh SPA used System electric energy today L | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 10 Esystem_total H | System electric energy total H | — | 0.1 k electri energy H Wh SPA used System c total | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 11 Esystem_ total L | System electric energy total L | — | 0.1 k Wh SPA use System electri energy L d c total | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 12 EACharge_Today _H | ACCharge energy today | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 13 EACharge_Today _L | ACCharge energy today | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 14 EACharge_Total _H | ACCharge energy total | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 15 EACharge_Total _L | ACCharge energy total | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 16 AC charge Power_H | Grid power to local load | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 17 AC charge Power_L | Grid power to local load | — | 0.1 kwh Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 18 Priority | 0:Load First 1:Battery First 2:Grid First | — | Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 19 Battery Type | 0:Lead-acid 1:Lithium battery | — | Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 20 Auto Proofread C MD | Aging mode | — | Storage Power — | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 21 | 24. reserved | — | — | reserve d | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 3 | 000 | 2: Reserved 3:Sys Fault module 4: Flash module 5:PVBATOnline module: 6:Bat Online module 7:PVOffline Mode 8:Bat Offline Mode The lower 8 bits indicate the m status (web page display) 0: Standby Status; 1: Normal Status; 3: Fault Status 4:Flash Status; | — | achine — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 001 Ppv H | PV total power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 002 Ppv L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 003 Vpv 1 | PV 1 voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 004 Ipv 1 | PV 1 input current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 005 Ppv 1 H | PV 1 power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 006 Ppv 1 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 007 Vpv 2 | PV 2 voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 008 Ipv 2 | PV 2 input current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 009 Ppv 2 H | PV 2 power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 010 Ppv 2 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 011 Vpv 3 | PV 3 voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 012 Ipv 3 | PV 3 input current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 013 Ppv 3 H | PV 3 power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 014 Ppv 3 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 015 Vpv 4 | PV 4 voltage | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 016 Ipv 4 | PV 4 input current | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 017 Ppv 4 H | PV 4 power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 018 Ppv 4 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 019 Psys H | System output power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 020 Psys L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 021 Qac H Qac L | reactive power | — | 0.1 Var — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 022 | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 023 Pac H | Output power | — | 0.1 W Outp ut | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 024 Pac L Fac | Grid frequency | — | powe 0.01 Hz Grid r | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 025 Vac 1 | Three/single phase grid voltage | — | freq 0.1 V Thre uency e/single | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 026 | — | — | phas volt e grid age | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 027 Iac 1 | Three/single phase grid output | — | current 0.1 A Thre phase g output current e/single rid | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 028 Pac 1 H Pac 1 L | Three/single phase grid output VA | — | watt 0.1 VA Three/s phase g ingle rid | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 029 Vac 2 | Three phase grid voltage | — | output VA 0.1 V Three p watt hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 030 Iac 2 | Three phase grid output current | — | grid vo 0.1 A Three p ltage hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 031 | — | — | grid ou current tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 032 Pac 2 H Pac 2 L | Three phase grid output power | — | 0.1 VA Three p grid ou hase tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 033 Vac 3 | Three phase grid voltage | — | power 0.1 V Three p hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 034 Iac 3 | Three phase grid output current | — | grid vo 0.1 A Three p ltage hase | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 035 | — | — | grid ou current tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 036 Pac 3 H Pac 3 L | Three phase grid output power | — | 0.1 VA Three p grid ou hase tput | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 037 | — | — | power — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 038 Vac_RS | Three phase grid voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 039 Vac_ST | Three phase grid voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 040 Vac_TR | Three phase grid voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 041 Ptouser total H | Total forward power | — | 0.1 W Total f power orward | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 042 Ptouser total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 043 Ptogrid total H | Total reverse power | — | 0.1 W Total r power everse | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 044 Ptogrid total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 045 Ptoload total H | Total load power | — | 0.1 W Total power load | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 046 Ptoload total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 047 Time total H | Work time total | — | 0.5 s — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 048 Time total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 049 Eac today H Eac today L | Today generate energy | — | 0.1 k Wh Today generat e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 050 | — | — | energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 051 Eac total H | Total generate energy | — | 0.1 k Wh Total — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 052 Eac total L | — | — | generat energy e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 053 Epv_total H | PV energy total | — | 0.1 k Wh PV energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 054 Epv_total L | — | — | total — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 055 Epv 1_today H | PV 1 energy today | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 056 Epv 1_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 057 Epv 1_total H | PV 1 energy total | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 058 Epv 1_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 059 Epv 2_today H | PV 2 energy today | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 060 Epv 2_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 061 Epv 2_total H | PV 2 energy total | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 062 Epv 2_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 063 Epv 3_today H | PV 3 energy today | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 064 Epv 3_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 065 Epv 3_total H | PV 3 energy total | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 066 Epv 3_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 067 Etouser_today H | Today energy to user | — | 0.1 k Wh Today energy to user — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 068 Etouser_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 069 Etouser_total H | Total energy to user | — | 0.1 k Wh Total energy to user — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 070 Etouser_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 071 Etogrid_today H | Today energy to grid | — | 0.1 k Wh Today energy to grid — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 072 Etogrid_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 073 Etogrid_total H | Total energy to grid | — | 0.1 k Wh Total energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 074 Etogrid_total L | — | — | to grid — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 075 Eload_today H | Today energy of user load | — | 0.1 k Wh Today energy of user load — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 076 Eload_today L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 077 Eload_total H | Total energy of user load | — | 0.1 k Wh Total energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 078 Eload_total L | — | — | of user load — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 079 Epv 4_today H Epv 4_today L | PV 4 energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 080 | — | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 081 Epv 4_total H Epv 4_total L | PV 4 energy total | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 082 | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 083 Epv_today H | PV energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 084 Epv_today L | — | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 085 Reserved Derating Mode | Derating Mode | — | 0:c NOTDerate 1:c PVHigh Der ate 2: c Power Con stant Derate 3: c Grid VHig Derate 4:c Freq High D erate 5:c Dc Soure M ode Derate 6:c Inv Tempr D erate 7:c Active Pow er Order 8:c Load Speed Process h | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 086 | — | — | 9:c Over Bac by Time 10:c Internal empr Derate 11:c Out Temp r Derate 12:c Line Impe Calc Derate 13: c Paralle nti Backflow D erate 14:c Local Ant Backflow Dera te 15:c Bdc Load P ri Derate 16:c Chk CTErr Derate k T l A i | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 087 ISO | PV ISO value | — | 1 KΩ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 088 DCI_R | R DCI Curr | — | 0.1 m A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 089 DCI_S | S DCI Curr | — | 0.1 m A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 090 DCI_T | T DCI Curr | — | 0.1 m A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 091 GFCI | GFCI Curr | — | 1 m A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 092 Bus Voltage | total bus voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 093 Temp 1 | Inverter temperature | — | 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 094 Temp 2 | The inside IPM in inverter temp | — | erature 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 095 Temp 3 | Boost temperature | — | 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 096 Temp 4 | Reserved | — | 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 097 Temp 5 | Commmunication broad temperatur | — | e 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 098 P Bus Voltage | P Bus inside Voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 099 N Bus Voltage | N Bus inside Voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 100 IPF | Inverter output PF now | — | 0-20 000 | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 101 Real OPPercent | Real Output power Percent | — | 1% 1~10 0 | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 102 OPFullwatt H OPFullwatt L | Output Maxpower Limited | — | 0.1 W Outp Maxp ut ower | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 103 Standby Flag | Inverter standby flag | — | Limi bitfield bit 0 Orde bit 1 bit 2 ted :turn off r; :PV Low; :AC | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 104 | — | — | Volt out bit 3 Rese /Freq of scope; ~bit 7 : rved | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 105 Fault Maincode | Inverter fault maincode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 106 Warn Maincode | Inverter Warning maincode | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 107 Fault Subcode | Inverter fault subcode | — | bitfield — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 108 Warn Subcode | Inverter Warning subcode | — | bitfield — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 109 | — | — | bitfield — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 110 uw Present FFTVa | Present FFTValue [CHANNEL_A] | — | bitfield bitfield — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 111 lue [CHANNEL_A ] b Afci Status | AFCI Status | — | 0 : stat 1:se 2 : waiting e lf-check Detection | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 112 uw Strength[CHA | AFCI Strength[CHANNEL_A] | — | of stat 3:fa 4 : stat arcing e ult state update e | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 113 NNEL_A] uw Self Check Val | AFCI Self Check[CHANNEL_A] | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 114 ue[CHANNEL_A] inv start delay | inv start delay time | — | 1 S inv start de lay | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 115 time | — | — | time — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 116 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 117 Reserved BDC_On Off State | BDC connect state | — | 0:No BDC Connect 1:BDC 1 Connect — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 118 Dry Contact State | Current status of Dry Contact | — | 2:BDC 2 Connect 3:BDC 1+BDC 2 Connect Current status of | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 119 | — | — | Dry Contact 0: turn off; 1: turn on; — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 120 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 121 Pself H Pself L | self-use power | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 122 | — | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 123 Esys_today H Esys_today L | System energy today | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 124 | — | — | 0.1 kwh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 125 Edischr_today H Edischr_today L | Today discharge energy | — | 0.1 k Wh Today discharge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 126 | — | — | energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 127 Edischr_total H Edischr_total L | Total discharge energy | — | 0.1 k Wh Total discharge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 128 | — | — | energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 129 Echr_today H | Charge energy today | — | 0.1 k Wh Charge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 130 Echr_today L | — | — | energy today — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 131 Echr_total H | Charge energy total | — | 0.1 k Wh Charge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 132 Echr_total L | — | — | energy total — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 133 Eacchr_today H | Today energy of AC charge | — | 0.1 k Wh Today energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 134 Eacchr_today L | — | — | of AC charge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 135 Eacchr_total H | Total energy of AC charge | — | 0.1 k Wh Total energy — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 136 Eacchr_total L | — | — | of AC charge — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 137 Esys_total H Esys_total L | Total energy of system outpu | — | t \ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 138 | — | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 139 Eself_today H Eself_today L | Today energy of Self output | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 140 | — | — | 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 141 Eself_total H Eself_ total L | Total energy of Self output | — | 0.1 kwh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 142 | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 143 Reserved Priority | Word Mode | — | 0 Lo 1 ad First | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 144 | — | — | Batt t 2 Gr ery Firs id First | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 145 EPS Fac | UPS frequency | — | 0.01 Hz — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 146 EPS Vac 1 | UPS phase R output voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 147 EPS Iac 1 | UPS phase R output current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 148 EPS Pac 1 H | UPS phase R output power | — | 0.1 VA — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 149 EPS Pac 1 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 150 EPS Vac 2 | UPS phase S output voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 151 EPS Iac 2 | UPS phase S output current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 152 EPS Pac 2 H | UPS phase S output power | — | 0.1 VA — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 153 EPS Pac 2 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 154 EPS Vac 3 | UPS phase T output voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 155 EPS Iac 3 | UPS phase T output current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 156 EPS Pac 3 H | UPS phase T output power | — | 0.1 VA — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 157 EPS Pac 3 L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 158 EPS Pac H | UPS output power | — | 0.1 VA — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 159 EPS Pac L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 160 Loadpercent | Load percent of UPS ouput | — | 0.10% — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 161 PF | Power factor | — | 0.1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 162 DCV | DC voltage | — | 1 m V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 163 Reserved New Bdc Flag | Whether to parse BDC data separ | — | ately 0: D on't need | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 164 BDCDerating Mo de | BDCDerating Mode: 0: Normal, unrestricted 1:Standby or fault | — | 1:ne ed | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 165 Sys State_Mode | 2:Maximum battery current limit (discharge) 3:Battery discharge Enable (Dis 4:High bus discharge derating (discharge) 5:High temperature discharge derating (discharge) 6:System warning No discharge (discharge) 7-15 Reserved (Discharge) 16:Maximum charging current of battery (charging) 17:High Temperature (LLC and Buckboost) (Charging) 18:Final soft charge 19:SOC setting limits (charging 20:Battery low temperature (cha 21:High bus voltage (charging) 22:Battery SOC (charging) 23: Need to charge (charge) 24: System warning not charging (charging) 25-29:Reserve (charge) System work State and mode The upper 8 bits indicate the mode; 0:No charge and discharge; 1:charge; 2:Discharge; | — | charge) ) rging) BDC 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 166 | The lower 8 bits represent the 0: Standby Status; 1: Normal Status; 2: Fault Status 3:Flash Status; | — | status; — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 167 Fault Code | Storge device fault code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 168 Warn Code | Storge device warning code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 169 Vbat | Battery voltage | — | 0.01 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 170 Ibat | Battery current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 171 SOC | State of charge Capacity | — | 1% — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 172 Vbus 1 | Total BUS voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 173 Vbus 2 | On the BUS voltage | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 174 Ibb | BUCK-BOOST Current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 175 Illc | LLC Current | — | 0.1 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 176 Temp A | Temperture A | — | 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 177 Temp B | Temperture B | — | 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 178 Pdischr H | Discharge power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 179 Pdischr L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 180 Pchr H | Charge power | — | 0.1 W — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 181 Pchr L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 182 Edischr_total H | Discharge total energy of storg | — | e device 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 183 Edischr_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 184 Echr_total H | Charge total energy of storge d | — | evice 0.1 k Wh — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 185 Echr_total L | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 186 Reserved BDC 1_Flag | Reserved BDC mark (charge and dischar fault alarm code) Bit 0: Charge En; BDC allows char Bit 1: Discharge En; BDC allows discharge | — | ge, ging — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 187 | Bit 2~7: Resvd; reserved Bit 8~11: Warn Sub Code; BDC sub-warning code Bit 12~15: Fault Sub Code; BDC sub-error code | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 188 Vbus 2 Bms Max Volt Cell | Lower BUS voltage Bms Max Volt Cell No | — | 0.1 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 189 No Bms Min Volt Cell | Bms Min Volt Cell No | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 190 No Bms Battery Avg T | Bms Battery Avg Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 191 emp Bms Max Cell Tem | Bms Max Cell Temp | — | 0.1°C — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 192 p Bms Battery Avg T | Bms Battery Avg Temp | — | 0.1°C — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 193 emp Bms Max Cell Tem | Bms Max Cell Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 194 p Bms Battery Avg T | Bms Battery Avg Temp | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 195 emp | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 196 Bms Max SOC | Bms Max SOC | — | 1% — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 197 Bms Min SOC Parallel Battery N | Bms Min SOC Parallel Battery Num | — | 1% — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 198 um Bms Derate Reas | Bms Derate Reason | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 199 on Bms Gauge FCC | Bms Gauge FCC(Ah) | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 200 (Ah) Bms Gauge RM | Bms Gauge RM(Ah) | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 201 (Ah) | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 202 Bms Error | BMS Protect 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 203 Bms Warn | BMSWarn 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 204 Bms Fault | BMS Fault 1 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 205 Bms Fault 2 | BMS Fault 2 | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 206 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 207 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 208 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 209 Reserved Bat Iso Status | Battery ISO detection status | — | 0:Not detected — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 210 Batt Need Charge Request Flag | battery work request | — | 1 : Detectio completed bit 0:1: Prohibit chargin g,0: Allow the chargin g bit 1:1: Enable strong charge, n | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 211 BMS_Status | battery working status | — | 0: disable strong charge bit 2:1: Enable strong charge 2 0: disable strong charge 2 bit 8:1: Dischar ge is prohibit ed, 0: allow discharg e bit 9:1: Turn on power reductio n 0: turn off power reductio n; R 0: dor 1:Char 2:Disc 3:free mancy ge harge | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 212 | — | — | 4:stan 5:Soft 6:faul 7:upda dby start t te | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 213 Bms Error 2 | BMS Protect 2 | — | R 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 214 Bms Warn 2 | BMS Warn 2 | — | R 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 215 BMS_SOC BMS_Battery Vol | BMS SOC BMS Battery Volt | — | R 1% R 0.01 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 216 t BMS_Battery Cur | BMS Battery Curr | — | R 0.01 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 217 r BMS_Battery Te | battery cell maximum temperatur | — | e R 0.1℃ — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 218 mp | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 219 BMS_Max Curr BMS_Max Dischr | Maximum charging current Maximum discharge current | — | R 0.01 A R 0.01 A — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 220 Curr | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 221 BMS_Cycle Cnt | BMSCycle Cnt | — | R 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 222 BMS_SOH BMS_Charge Vol | BMS SOH Battery charging voltage limit | — | R 1 value R 0.01 V — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 223 t Limit BMS_Discharge | Battery discharge voltage limit | — | value — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 224 Volt Limit | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 225 Bms Warn 3 | BMS Warn 3 | — | R 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 226 Bms Error 3 | BMS Protect 3 | — | R 1 — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 227 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 3 | 228 Reserved | — | — | — | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 32 | 29 Reserved | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 30 BMSSingle Volt M ax | BMS Battery Single Volt Max | — | R 0.001 V — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 31 BMSSingle Volt M in | BMS Battery Single Volt Min | — | R 0.001 V — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 32 Bat Load Volt | Battery Load Volt | — | R 0.01 V [ 0,650.00] | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 33 | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 34 Debug data 1 | Debug data 1 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 35 Debug data 2 | Debug data 2 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 36 Debug data 3 | Debug data 3 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 37 Debug data 4 | Debug data 4 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 38 Debug data 5 | Debug data 5 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 39 Debug data 6 | Debug data 6 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 40 Debug data 7 | Debug data 7 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 41 Debug data 8 | Debug data 8 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 42 Debug data 9 | Debug data 9 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 43 Debug data 10 | Debug data 10 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 44 Debug data 10 | Debug data 10 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 45 Debug data 12 | Debug data 12 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 46 Debug data 13 | Debug data 13 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 47 Debug data 14 | Debug data 14 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 48 Debug data 15 | Debug data 15 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 49 Debug data 16 | Debug data 16 | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 50 Pex 1 H | PV inverter 1 output power H | — | R 0.1 W — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 51 Pex 1 L | PV inverter 1 output power L | — | R 0.1 W — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 52 Pex 2 H | PV inverter 2 output power H | — | R 0.1 W — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 53 Pex 2 L | PV inverter 2 output power L | — | R 0.1 W — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 54 Eex 1 Today H | PV inverter 1 energy Today H | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 55 Eex 1 Today L | PV inverter 1 energy Today L | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 56 Eex 2 Today H | PV inverter 2 energy Today H | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 57 Eex 2 Today L | PV inverter 2 energy Today L | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 58 Eex 1 Total H | PV inverter 1 energy Total H | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 59 Eex 1 Total L | PV inverter 1 energy Total L | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 60 Eex 2 Total H | PV inverter 2 energy Total H | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 61 Eex 2 Total L | PV inverter 2 energy Total L | — | R 0.1 k Wh — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 62 uw Bat No | battery pack number | — | R BD ar ev mi C reports e updated ery 15 nutes | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 63 Bat Serial Num 1 | Battery pack serial number SN[0] | — | SN[1] R BD ar C reports e updated | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 64 Bat Serial Num 2 | Battery pack serial number SN[2] | — | SN[3] R ev ery 15 | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 65 Bat Serial Num 3 | Battery pack serial number SN[4] | — | SN[5] R mi nutes | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 66 Bat Serial Num 4 | Battery pack serial number SN[6] | — | SN[7] R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 67 Bat Serial Num 5 | Battery pack serial number SN[8] | — | SN[9] R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 68 Bat Serial Num 6 | Battery pack serial number SN[10]SN[11] | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 69 Bat Serial Num 7 | Battery pack serial number SN[12]SN[13] | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 70 Bat Serial Num 8 | Battery pack serial number SN[14]SN[15] | — | R — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 71- Reserve | Reserve | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 79 | — | — | — | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 32 | 80 b Clr Today Data Fl ag | Clear day data flag | — | R Da cu th se ta of the rrent day at the rver determines whether to clear. 0:not cleared. 1: Clear. | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 40 | 00- 1 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 41 | 07 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 41 | 08- 2 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 42 | 15 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 48 | 64- 9 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 49 | 71 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | — | — |
| 49 | 72- 10 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | — | — |
| 50 | 79 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | tl3:input_1_energy_total, offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |

## Offgrid SPF Input Registers
Observed off-grid register map (from integration implementation).

**Applies to:** Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0. | Inverter Status | Inverter run state | — | 0:waiting, 1:normal, 3:fault — | — | — | offgrid:status_code | Status code |
| 1. | Ppv H | Input power (high) | — | 0.1 W — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 2. | Ppv L | Input power (low) | — | 0.1 W — | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3. | Vpv 1 | PV 1 voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 4. | PV 1 Curr | PV 1 input current | — | 0.1 A — | — | — | — | — |
| 5. | Ppv 1 H | PV 1 input power(high) | — | 0.1 W — | — | — | offgrid:input_2_power | Input 2 Wattage, PV2 charge power |
| 6. | Ppv 1 L | PV 1 input power(low) | — | 0.1 W — | — | — | — | — |
| 7. | Vpv 2 | PV 2 voltage | — | 0.1 V — | — | — | offgrid:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 8. | PV 2 Curr | PV 2 input current | — | 0.1 A — | — | — | offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9. | Ppv 2 H | PV 2 input power (high) | — | 0.1 W — | — | — | offgrid:output_active_power | Output active power |
| 10 | . Ppv 2 L | PV 2 input power (low) | — | 0.1 W — | — | — | — | — |
| 11 | . Vpv 3 | PV 3 voltage | — | 0.1 V — | — | — | — | — |
| 12 | . PV 3 Curr | PV 3 input current | — | 0.1 A — | — | — | — | — |
| 13 | . Ppv 3 H | PV 3 input power (high) | — | 0.1 W — | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 14 | . Ppv 3 L | PV 3 input power (low) | — | 0.1 W — | — | — | — | — |
| 15 | . Vpv 4 | PV 4 voltage | — | 0.1 V — | — | — | — | — |
| 16 | . PV 4 Curr | PV 4 input current | — | 0.1 A — | — | — | — | — |
| 17 | . Ppv 4 H | PV 4 input power (high) | — | 0.1 W — | — | — | offgrid:battery_voltage | Battery voltage |
| 18 | . Ppv 4 L | PV 4 input power (low) | — | 0.1 W — | — | — | offgrid:soc | SOC |
| 19 | . Vpv 5 | PV 5 voltage | — | 0.1 V — | — | — | offgrid:bus_voltage | Bus voltage |
| 20 | . PV 5 Curr | PV 5 input current | — | 0.1 A — | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | . Ppv 5 H | PV 5 input power(high) | — | 0.1 W — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 22 | . Ppv 5 L | PV 5 input power(low) | — | 0.1 W — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 23 | . Vpv 6 | PV 6 voltage | — | 0.1 V — | — | — | offgrid:output_frequency | Output frequency |
| 24 | . PV 6 Curr | PV 6 input current | — | 0.1 A — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 25 | . Ppv 6 H | PV 6 input power (high) | — | 0.1 W — | — | — | offgrid:inverter_temperature | Temperature |
| 26 | . Ppv 6 L | PV 6 input power (low) | — | 0.1 W — | — | — | offgrid:dc_dc_temperature | DC-DC temperature |
| 27 | . Vpv 7 | PV 7 voltage | — | 0.1 V — | — | — | offgrid:load_percent | Inverter load |
| 28 | . PV 7 Curr | PV 7 input current | — | 0.1 A — | — | — | offgrid:battery_port_voltage | Battery port voltage |
| 29 | . Ppv 7 H | PV 7 input power (high) | — | 0.1 W — | — | — | offgrid:battery_bus_voltage | Battery bus voltage |
| 30 | . Ppv 7 L | PV 7 input power (low) | — | 0.1 W — | — | — | offgrid:operation_hours | Running hours |
| 31 | . Vpv 8 | PV 8 voltage | — | 0.1 V — | — | — | — | — |
| 32 | . PV 8 Curr | PV 8 input current | — | 0.1 A — | — | — | — | — |
| 33 | . Ppv 8 H | PV 8 input power (high) | — | 0.1 W — | — | — | — | — |
| 34 | . Ppv 8 L | PV 8 input power (low) | — | 0.1 W — | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35 | . Pac H | Output power (high) | — | 0.1 W — | — | — | — | — |
| 36 | . Pac L | Output power (low) | — | 0.1 W — | — | — | — | — |
| 37 | . Fac | Grid frequency | — | 0.01 Hz — | — | — | — | — |
| 38 | . Vac 1 | Three/single phase grid voltage | — | 0.1 V — | — | — | — | — |
| 39 | . Iac 1 | Three/single phase grid output | — | current 0.1 A — | — | — | — | — |
| 40 | . Pac 1 H | Three/single phase grid output VA (high) | — | watt 0.1 VA — | — | — | — | — |
| 41 | . Pac 1 L | Three/single phase grid output VA(low) | — | watt 0.1 VA — | — | — | — | — |
| 42 | . Vac 2 | Three phase grid voltage | — | 0.1 V — | — | — | offgrid:fault_code | Fault code |
| 43 | . Iac 2 | Three phase grid output current | — | 0.1 A — | — | — | offgrid:warning_code | Warning code |
| 44 | . Pac 2 H | Three phase grid output power ( | — | high) 0.1 VA — | — | — | — | — |
| 45 | . Pac 2 L | Three phase grid output power ( | — | low) 0.1 VA — | — | — | — | — |
| 46 | . Vac 3 | Three phase grid voltage | — | 0.1 V — | — | — | — | — |
| 47 | . Iac 3 | Three phase grid output current | — | 0.1 A — | — | — | offgrid:constant_power | — |
| 48 | . Pac 3 H | Three phase grid output power ( | — | high) 0.1 VA — | — | — | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 49 | . Pac 3 L | Three phase grid output power ( | — | low) 0.1 VA — | — | — | — | — |
| 50 | . Vac_RS | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51 | . Vac_ST | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | — | — |
| 52 | . Vac_TR | Three phase grid voltage | — | 0.1 V Li ne voltage | — | — | offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53 | . Eactoday H | Today generate energy (high) | — | 0.1 k WH — | — | — | — | — |
| 54 | . Eac today L | Today generate energy (low) | — | 0.1 k WH — | — | — | offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55 | . Eac total H | Total generate energy (high) | — | 0.1 k WH — | — | — | — | — |
| 56 | . Eac total L | Total generate energy (low) | — | 0.1 k WH — | — | — | offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 57 | . Time total H | Work time total (high) | — | 0.5 s — | — | — | — | — |
| 58 | . Time total L | Work time total (low) | — | 0.5 s — | — | — | offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 59 | . Epv 1_today H | PV 1 Energy today(high) | — | 0.1 k Wh — | — | — | — | — |
| 60 | . Epv 1_today L | PV 1 Energy today (low) | — | 0.1 k Wh — | — | — | offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61 | . Epv 1_total H | PV 1 Energy total(high) | — | 0.1 k Wh — | — | — | — | — |
| 62 | . Epv 1_total L | PV 1 Energy total (low) | — | 0.1 k Wh — | — | — | offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63 | . Epv 2_today H | PV 2 Energy today(high) | — | 0.1 k Wh — | — | — | — | — |
| 64 | . Epv 2_today L | PV 2 Energy today (low) | — | 0.1 k W h | — | — | offgrid:ac_discharge_energy_today | AC Discharged Today |
| 65 | . Epv 2_total H | PV 2 Energy total(high) | — | 0.1 k W h | — | — | — | — |
| 66 | . Epv 2_total L | PV 2 Energy total (low) | — | 0.1 k W h | — | — | offgrid:ac_discharge_energy_total | Grid Discharged Lifetime |
| 67 | . Epv 3_today H | PV 3 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 68 | . Epv 3_today L | PV 3 Energy today (low) | — | 0.1 k W h | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69 | . Epv 3_total H | PV 3 Energy total(high) | — | 0.1 k W h | — | — | offgrid:discharge_power | Battery discharge power, Discharge Power |
| 70 | . Epv 3_total L | PV 3 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 71 | . Epv 4_today H | PV 4 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 72 | . Epv 4_today L | PV 4 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 73 | . Epv 4_total H | PV 4 Energy total(high) | — | 0.1 k W h | — | — | offgrid:battery_discharge_amperage | Battery discharge current |
| 74 | . Epv 4_total L | PV 4 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 75 | . Epv 5_today H | PV 5 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 76 | . Epv 5_today L | PV 5 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 77 | . Epv 5_total H | PV 5 Energy total(high) | — | 0.1 k W h | — | — | offgrid:battery_power | Battery charging/ discharging(-ve) |
| 78 | . Epv 5_total L | PV 5 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 79 | . Epv 6_today H | PV 6 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 80 | . Epv 6_today L | PV 6 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 81 | . Epv 6_total H | PV 6 Energy total(high) | — | 0.1 k W h | — | — | — | — |
| 82 | . Epv 6_total L | PV 6 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 83 | . Epv 7_today H | PV 7 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 84 | . Epv 7_today L | PV 7 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 85 | . Epv 7_total H | PV 7 Energy total(high) | — | 0.1 k W h | — | — | — | — |
| 86 | . Epv 7_total L | PV 7 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 87 | . Epv 8_today H | PV 8 Energy today(high) | — | 0.1 k W h | — | — | — | — |
| 88 | . Epv 8_today L | PV 8 Energy today (low) | — | 0.1 k W h | — | — | — | — |
| 89 | . Epv 8_total H | PV 8 Energy total(high) | — | 0.1 k W h | — | — | — | — |
| 90 | . Epv 8_total L | PV 8 Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 91 | . Epv_total H | PV Energy total(high) | — | 0.1 k W h | — | — | — | — |
| 92 | . Epv_total L | PV Energy total (low) | — | 0.1 k W h | — | — | — | — |
| 93 | . Temp 1 | Inverter temperature | — | 0.1 C — | — | — | — | — |
| 94 | . Temp 2 | The inside IPM in inverter Temp | — | erature 0.1 C — | — | — | — | — |
| 95 | . Temp 3 | Boost temperature | — | 0.1 C — | — | — | — | — |
| 96 | . Temp 4 | — | — | — reserved | — | — | — | — |
| 97 | . uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 98 | . P Bus Voltage | P Bus inside Voltage | — | 0.1 V — | — | — | — | — |
| 99 | . N Bus Voltage | N Bus inside Voltage | — | 0.1 V — | — | — | — | — |
| 10 | 0. IPF | Inverter output PF now | — | 0-20000 — | — | — | — | — |
| 10 | 1. Real OPPercent | Real Output power Percent | — | 1% — | — | — | — | — |
| 10 | 2. OPFullwatt H | Output Maxpower Limited high | — | — | — | — | — | — |
| 10 | 3. OPFullwatt L | Output Maxpower Limited low | — | 0.1 W — | — | — | — | — |
| 10 | 4. Derating Mode | Derating Mode 0 1 2 3 4 5 6 7 8 9 B | — | :no derate; :PV; :*; :Vac; :Fac; :Tboost; :Tinv; :Control; :*; :*Over Back y Time; — | — | — | — | — |
| 10 | 5. Fault Maincode | Inverter fault maincode | — | — | — | — | — | — |
| 10 | 6. | — | — | — | — | — | — | — |
| 10 | 7. Fault Subcode | Inverter fault subcode | — | — | — | — | — | — |
| 10 | 8. Remote Ctrl En | / 0 1 | — | / St .Load First er .Bat First orage Pow (SPA) | — | — | — | — |
| 10 | 9. Remote Ctrl Pow er | / 2 | — | / St .Grid er orage Pow (SPA) | — | — | — | — |
| 11 | 0. Warning bit H | Warning bit H | — | — | — | — | — | — |
| 11 | 1. Warn Subcode | Inverter warn subcode | — | — | — | — | — | — |
| 11 | 2. Warn Maincode EACharge_Today _H | Inverter warn maincode ACCharge energy today | — | 0.1 kwh St Po orage wer | — | — | — | — |
| 11 | 3. real Power Percent EACharge_Today _L | real Power Percent 0 ACCharge energy today | — | -100 % MA 0.1 kwh St Po X orage wer | — | — | — | — |
| 11 | 4. inv start delay i time EACharge_Total _H | nv start delay time ACCharge energy total | — | MA 0.1 kwh St Po X orage wer | — | — | — | — |
| 11 | 5. b INVAll Fault Cod e EACharge_Total _L | b INVAll Fault Code ACCharge energy total | — | MA 0.1 kwh St Po X orage wer | — | — | — | — |
| 11 | 6. AC charge Power_H | Grid power to local load | — | 0.1 kwh St Po orage wer | — | — | — | — |
| 11 | 7. AC charge Power_L | Grid power to local load | — | 0.1 kwh St Po orage wer | — | — | — | — |
| 11 | 8. Priority | 0:Load First 1:Battery First 2:Grid First | — | St orage Power | — | — | — | — |
| 11 | 9. Battery Type | 0:Lead-acid 1:Lithium battery | — | — Storage Power | — | — | — | — |
| 12 | 0. Auto Proofread C MD | Aging mode Auto-cal command | — | ibration Storage Power | — | — | — | — |
| 12 | 4. reserved | — | — | — reserved | — | — | — | — |
| 12 | 5. PID PV 1+ Voltage | PID PV 1 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | — | — |
| 12 | 6. PID PV 1+ Current | PID PV 1 PE Curr | — | -10~10 m A 0.1 m A | — | — | — | — |
| 12 | 7. PID PV 2+ Voltage | PID PV 2 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | — | — |
| 12 | 8. PID PV 2+ Current | PID PV 2 PE Curr | — | -10~10 m A 0.1 m A | — | — | — | — |
| 12 | 9. PID PV 3+ Voltage | PID PV 3 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | — | — |
| 13 | 0. PID PV 3+ Current | PID PV 3 PE Curr | — | -10~10 m A 0.1 m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 1. PID PV 4+ Voltage | PID PV 4 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 2. PID PV 4+ Current | PID PV 4 PE Curr | — | -10~10 m A 0.1 m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 3. PID PV 5+ Voltage | PID PV 5 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 4. PID PV 5+ Current | PID PV 5 PE Curr | — | -10~10 m A 0.1 m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 5. PID PV 6+ Voltage | PID PV 6 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 6. PID PV 6+ Current | PID PV 6 PE Curr | — | -10~10 m A 0.1 m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 7. PID PV 7+ Voltage | PID PV 7 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 8. PID PV 7+ Current | PID PV 7 PE Curr | — | -10~10 m A 0.1 m A | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 13 | 9. PID PV 8+ Voltage | PID PV 8 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 14 | 0. PID PV 8+ Current | PID PV 8 PE Curr | — | -10~10 m A 0.1 m A | — | — | — | — |
| 14 | 1. PID Status | Bit 0~7:PID Working Status 1:Wait Status 2:Normal Status 3:Fault Status Bit 8~15:Reversed | — | 0~3 — | — | — | — | — |
| 14 | 2. V _String 1 | PV String 1 voltage | — | 0.1 V | — | — | — | — |
| 14 | 3. Curr _String 1 | PV String 1 current | — | -15~15 A 0.1 A | — | — | — | — |
| 14 | 4. V _String 2 | PV String 2 voltage | — | 0.1 V | — | — | — | — |
| 14 | 5. Curr _String 2 | PV String 2 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 14 | 6. V _String 3 | PV String 3 voltage | — | 0.1 V — | — | — | — | — |
| 14 | 7. Curr _String 3 | PV String 3 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 14 | 8. V _String 4 | PV String 4 voltage | — | 0.1 V — | — | — | — | — |
| 14 | 9. Curr _String 4 | PV String 4 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 15 | 0. V _String 5 | PV String 5 voltage | — | 0.1 V — | — | — | — | — |
| 15 | 1. Curr _String 5 | PV String 5 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 15 | 2. V _String 6 | PV String 6 voltage | — | 0.1 V — | — | — | — | — |
| 15 | 3. Curr _String 6 | PV String 6 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 15 | 4. V _String 7 | PV String 7 voltage | — | 0.1 V — | — | — | — | — |
| 15 | 5. Curr _String 7 | PV String 7 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 15 | 6. V _String 8 | PV String 8 voltage | — | 0.1 V — | — | — | — | — |
| 15 | 7. Curr _String 8 | PV String 8 current | — | -15 A~15 A 0.1 A — | — | — | — | — |
| 15 | 8. V _String 9 | PV String 9 voltage | — | 0.1 V — | — | — | — | — |
| 15 | 9. Curr _String 9 | PV String 9 current | — | -15 A~15 A 0.1 A — | — | — | — | — |
| 16 | 0. V _String 10 | PV String 10 voltage | — | 0.1 V — | — | — | — | — |
| 16 | 1. Curr _String 10 | PV String 10 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 16 | 2. V _String 11 | PV String 11 voltage | — | 0.1 V — | — | — | — | — |
| 16 | 3. Curr _String 11 | PV String 11 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 16 | 4. V _String 12 | PV String 12 voltage | — | 0.1 V — | — | — | — | — |
| 16 | 5. Curr _String 12 | PV String 12 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 16 | 6. V _String 13 | PV String 13 voltage | — | 0.1 V — | — | — | — | — |
| 16 | 7. Curr _String 13 | PV String 13 current | — | -15 A~15 A 0.1 A — | — | — | — | — |
| 16 | 8. V _String 14 | PV String 14 voltage | — | 0.1 V — | — | — | — | — |
| 16 | 9. Curr _String 14 | PV String 14 current | — | -15~15 A 0.1 A — | — | — | — | — |
| 17 | 0. V _String 15 | PV String 15 voltage | — | 0.1 V — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 1. Curr _String 15 | PV String 15 current | — | -15~15 A 0.1 A — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 2. V _String 16 | PV String 16 voltage | — | 0.1 V — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 3. Curr _String 16 | PV String 16 current | — | -15~15 A 0.1 A — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 4. Str Unmatch | Bit 0~15: String 1~16 unmatch | — | — suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 5. Str Current Unblan ce | Bit 0~15: String 1~16 current u | — | nblance suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 6. Str Disconnect | Bit 0~15: String 1~16 disconnec | — | t suggestive | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 7. PIDFault Code | Bit 0:Output over voltage Bit 1: ISO fault Bit 2: BUS voltage abnormal Bit 3~15:reserved | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 8. String Prompt | String Prompt Bit 0:String Unmatch Bit 1:Str Disconnect Bit 2:Str Current Unblance Bit 3~15:reserved | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 17 | 9 PV Warning Value | PV Warning Value | — | — | — | — | offgrid:battery_voltage | Battery voltage |
| 18 | 0 DSP 075 Warning Value | DSP 075 Warning Value | — | — | — | — | offgrid:soc | SOC |
| 18 | 1 DSP 075 Fa Value | ult DSP 075 Fault Value | — | — | — | — | offgrid:soc | SOC |
| 18 | 2 DSP 067 Debu Data 1 | g DSP 067 Debug Data 1 | — | — | — | — | offgrid:soc | SOC |
| 18 | 3 DSP 067 Debu Data 2 | g DSP 067 Debug Data 2 | — | — | — | — | offgrid:soc | SOC |
| 18 | 4 DSP 067 Debu Data 3 | g DSP 067 Debug Data 3 | — | — | — | — | offgrid:soc | SOC |
| 18 | 5 DSP 067 Debu Data 4 | g DSP 067 Debug Data 4 | — | — | — | — | offgrid:soc | SOC |
| 18 | 6 DSP 067 Debu Data 5 | g DSP 067 Debug Data 5 | — | — | — | — | offgrid:soc | SOC |
| 18 | 7 DSP 067 Debu Data 6 | g DSP 067 Debug Data 6 | — | — | — | — | offgrid:soc | SOC |
| 18 | 8 DSP 067 Debu Data 7 | g DSP 067 Debug Data 7 | — | — | — | — | offgrid:soc | SOC |
| 18 | 9 DSP 067 Debu Data 8 | g DSP 067 Debug Data 8 | — | — | — | — | offgrid:soc | SOC |
| 19 | 0 DSP 075 Debu Data 1 | g DSP 075 Debug Data 1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 1 DSP 075 Debu Data 2 | g DSP 075 Debug Data 2 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 2 DSP 075 Debu Data 3 | g DSP 075 Debug Data 3 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 3 DSP 075 Debu Data 4 | g DSP 075 Debug Data 4 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 4 DSP 075 Debu Data 55 | g DSP 075 Debug Data 5 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 5 DSP 075 Debu Data 6 | g DSP 075 Debug Data 6 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 6 DSP 075 Debu Data 7 | g DSP 075 Debug Data 7 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 7 DSP 075 Debu Data 8 | g DSP 075 Debug Data 8 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 8 b USBAging Test Ok Flag | USBAging Test Ok Flag 0-1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 19 | 9 b Flash Erase Aging Ok Flag | Flash Erase Aging Ok Flag 0-1 | — | — | — | — | offgrid:bus_voltage | Bus voltage |
| 20 | 0 PVISO | PVISOValue | — | KΩ — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 1 R_DCI | R DCI Curr | — | 0.1 m A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 2 S_DCI | S DCI Curr | — | 0.1 m A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 3 T_DCI | T DCI Curr | — | 0.1 m A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 4 PID_Bus | PIDBus Volt | — | 0.1 V — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 5 GFCI | GFCI Curr | — | m A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 6 SVG/APF Status+SVGAPFEq ual Ratio | SVG/APF Status+SVGAPFEqual Rat | — | io High 8 bit: SVGAPFEqua l Ratio Low 8 bit: SVG/APF Status 0:None 1:SVG Run 2:APF Run 3:SVG/APF Run — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 7 CT_I _R | R phase load side current for | — | SVG 0.1 A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 8 CT_I _S | S phase load side current for | — | SVG 0.1 A — | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 9 CT_I _T | T phase load side current for | — | SVG 0.1 A — | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | 0 CT_Q _R H | R phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 1 CT_Q _R L | R phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 2 CT_Q _S H | S phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 3 CT_Q _S L | S phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 4 CT_Q _T H | T phase load side output reac power for SVG(High) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 5 CT_Q _T L | T phase load side output reac power for SVG(low) | — | tive 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 6 CT HAR_I_R | R phase load side harmonic | — | 0.1 A — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 7 CT HAR_I_S | S phase load side harmonic | — | 0.1 A — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 8 CT HAR_I_T | T phase load side harmonic | — | 0.1 A — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 9 COMP_Q _R H | R phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 22 | 0 COMP_Q _R L | R phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 1 COMP_Q _S H | S phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 2 COMP_Q _S L | S phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 3 COMP_Q _T H | T phase compensate reactive p for SVG(High) | — | ower 0.1 Var — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 4 COMP_Q _T L | T phase compensate reactive p for SVG(low) | — | ower 0.1 Var — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 5 COMP HAR_I_R | R phase compensate harmonic f SVG | — | or 0.1 A — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 6 COMP HAR_I_S | S phase compensate harmonic f SVG | — | or 0.1 A — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 7 COMP HAR_I_T | T phase compensate harmonic f SVG | — | or 0.1 A — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 8 b RS 232 Aging Test Ok Flag | RS 232 Aging Test Ok Flag | — | 0-1 — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 22 | 9 b Fan Fault Bit | Bit 0: Fan 1 fault bit Bit 1: Fan 2 fault bit Bit 2: Fan 3 fault bit Bit 3: Fan 4 fault bit Bit 4-7: Reserved | — | — | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 23 | 0 Sac H | Output apparent power H | — | 0.1 W — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 1 Sac L | Output apparent power L | — | 0.1 W — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 2 Re Act Power H | Real Output Reactive Power H | — | Int 32 0.1 W — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 3 Re Act Power L | Real Output Reactive Power L | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 4 Re Act Power Max H | Nominal Output Reactive Power | — | H 0.1 var — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 5 Re Act Power Max L | Nominal Output Reactive Power | — | L — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 6 Re Act Power_Total H | Reactive power generation | — | 0.1 kwh — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 7 Re Act Power_Total L | Reactive power generation | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 8 b Afci Status | 0:Waiting 1:Self-check state 2:Detect pull arc state 3:Fault 4:Update | — | — | — | — | offgrid:output_frequency | Output frequency |
| 23 | 9 uw Present FFTValu e [CHANNEL_A] | Present FFTValue [CHANNEL_A] | — | — | — | — | offgrid:output_frequency | Output frequency |
| 24 | 0 uw Present FFTValu e [CHANNEL_B] | Present FFTValue [CHANNEL_B] | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 1 DSP 067 Deb Data 1 | ug DSP 067 Debug Data 1 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 2 DSP 067 Deb Data 2 | ug DSP 067 Debug Data 2 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 3 DSP 067 Deb Data 3 | ug DSP 067 Debug Data 3 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 4 DSP 067 Debu Data 4 | g DSP 067 Debug Data 4 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 5 DSP 067 Debu Data 5 | g DSP 067 Debug Data 5 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 6 DSP 067 Debu Data 6 | g DSP 067 Debug Data 6 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 7 DSP 067 Debu Data 7 | g DSP 067 Debug Data 7 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 8 DSP 067 Debu Data 8 | g DSP 067 Debug Data 8 | — | — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 24 | 9 | — | — | reserved — | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 87 | 5 Vpv 9 | PV 9 voltage | — | 0.1 V — | — | — | — | — |
| 87 | 6 PV 9 Curr | PV 9 Input current | — | 0.1 A — | — | — | — | — |
| 87 | 7 Ppv 9 H | PV 9 input power (High) | — | 0.1 W — | — | — | — | — |
| 87 | 8 Ppv 9 L | PV 9 input power (Low) | — | 0.1 W — | — | — | — | — |
| 87 | 9 Vpv 10 | PV 10 voltage | — | 0.1 V — | — | — | — | — |
| 88 | 0 PV 10 Curr | PV 10 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 1 Ppv 10 H | PV 10 input power (High) | — | 0.1 W — | — | — | — | — |
| 88 | 2 Ppv 10 L | PV 10 input power (Low) | — | 0.1 W — | — | — | — | — |
| 88 | 3 Vpv 11 | PV 11 voltage | — | 0.1 V — | — | — | — | — |
| 88 | 4 PV 11 Curr | PV 11 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 5 Ppv 11 H | PV 11 input power (High) | — | 0.1 W — | — | — | — | — |
| 88 | 6 Ppv 11 L | PV 11 input power (Low) | — | 0.1 W — | — | — | — | — |
| 88 | 7 Vpv 12 | PV 12 voltage | — | 0.1 V — | — | — | — | — |
| 88 | 8 PV 12 Curr | PV 12 Input current | — | 0.1 A — | — | — | — | — |
| 88 | 9 Ppv 12 H | PV 12 input power (High) | — | 0.1 W — | — | — | — | — |
| 89 | 0 Ppv 12 L | PV 12 input power (Low) | — | 0.1 W — | — | — | — | — |
| 89 | 1 Vpv 13 | PV 13 voltage | — | 0.1 V — | — | — | — | — |
| 89 | 2 PV 13 Curr | PV 13 Input current | — | 0.1 A — | — | — | — | — |
| 89 | 3 Ppv 13 H | PV 13 input power (High) | — | 0.1 W — | — | — | — | — |
| 89 | 4 Ppv 13 L | PV 13 input power (Low) | — | 0.1 W — | — | — | — | — |
| 89 | 5 Vpv 14 | PV 14 voltage | — | 0.1 V — | — | — | — | — |
| 89 | 6 PV 14 Curr | PV 14 Input current | — | 0.1 A — | — | — | — | — |
| 89 | 7 Ppv 14 H | PV 14 input power (High) | — | 0.1 W — | — | — | — | — |
| 89 | 8 Ppv 14 L | PV 14 input power (Low) | — | 0.1 W — | — | — | — | — |
| 89 | 9 Vpv 15 | PV 15 voltage | — | 0.1 V — | — | — | — | — |
| 90 | 0 PV 15 Curr | PV 15 Input current | — | 0.1 A — | — | — | — | — |
| 90 | 1 Ppv 15 H | PV 15 input power (High) | — | 0.1 W — | — | — | — | — |
| 90 | 2 Ppv 15 L | PV 15 input power (Low) | — | 0.1 W — | — | — | — | — |
| 90 | 3 Vpv 16 | PV 16 voltage | — | 0.1 V — | — | — | — | — |
| 90 | 4 PV 16 Curr | PV 16 Input current | — | 0.1 A — | — | — | — | — |
| 90 | 5 Ppv 16 H | PV 16 input power (High) | — | 0.1 W — | — | — | — | — |
| 90 | 6 Ppv 16 L | PV 16 input power (Low) | — | 0.1 W — | — | — | — | — |
| 90 | 7 Epv 9_today H | PV 9 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 90 | 8 Epv 9_today L | PV 9 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 90 | 9 Epv 9_total H | PV 9 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 0 Epv 9_total L | PV 9 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 1 Epv 10_today H | PV 10 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 2 Epv 10_today L | PV 10 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 3 Epv 10_total H | PV 10 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 4 Epv 10_total L | PV 10 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 5 Epv 11_today H | PV 11 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 6 Epv 11_today L | PV 11 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 7 Epv 11_total H | PV 11 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 8 Epv 11_total L | PV 11 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 91 | 9 Epv 12_today H | PV 12 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 0 Epv 12_today L | PV 12 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 1 Epv 12_total H | PV 12 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 2 Epv 12_total L | PV 12 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 3 Epv 13_today H | PV 13 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 4 Epv 13_today L | PV 13 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 5 Epv 13_total H | PV 13 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 6 Epv 13_total L | PV 13 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 7 Epv 14_today H | PV 14 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 8 Epv 14_today L | PV 14 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 92 | 9 Epv 14_total H | PV 14 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 0 Epv 14_total L | PV 14 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 1 Epv 15_today H | PV 15 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 2 Epv 15_today L | PV 15 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 3 Epv 15_total H | PV 15 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 4 Epv 15_total L | PV 15 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 5 Epv 16_today H | PV 16 energy today (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 6 Epv 16_today L | PV 16 energy today (Low) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 7 Epv 16_total H | PV 16 energy total (High) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 8 Epv 16_total L | PV 16 energy total (Low) | — | 0.1 k Wh — | — | — | — | — |
| 93 | 9 PID PV 9+ Voltage | PID PV 9 PE Volt/ Flyspan volta (MAX HV) | — | ge 0~1000 V 0.1 V — | — | — | — | — |
| 94 | 0 PID PV 9+ Current | PID PV 9 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 94 | 1 PID PV 10 Voltage | + PID PV 10 PE/ Flyspan voltage ( HV) | — | MAX 0~1000 V 0.1 V — | — | — | — | — |
| 94 | 2 PID PV 1 Current | 0+ PID PV 10 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 94 | 3 PID PV 1 Voltage | 1+ PID PV 11 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 94 | 4 PID PV 1 Current | 1+ PID PV 11 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 94 | 5 PID PV 1 Voltage | 2+ PID PV 12 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 94 | 6 PID PV 1 Current | 2+ PID PV 12 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 94 | 7 PID PV 1 Voltage | 3+ PID PV 13 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 94 | 8 PID PV 1 Current | 3+ PID PV 13 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 94 | 9 PID PV 1 Voltage | 4+ PID PV 14 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 95 | 0 PID PV 1 Current | 4+ PID PV 14 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 95 | 1 PID PV 1 Voltage | 5+ PID PV 15 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 95 | 2 PID PV 1 Current | 5+ PID PV 15 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 95 | 3 PID PV 1 Voltage | 6+ PID PV 16 PE Volt/ Flyspan volt (MAX HV) | — | age 0~1000 V 0.1 V — | — | — | — | — |
| 95 | 4 PID PV 1 Current | 6+ PID PV 16 PE Current | — | -10~10 m A 0.1 m A — | — | — | — | — |
| 95 | 5 V _String 17 | PV String 17 voltage | — | 0.1 V — | — | — | — | — |
| 95 | 6 Curr _String 17 | PV String 17 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 95 | 7 V _String 18 | PV String 18 voltage | — | 0.1 V — | — | — | — | — |
| 95 | 8 Curr _String 18 | PV String 18 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 95 | 9 V _String 19 | PV String 19 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 0 Curr _String 19 | PV String 19 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 1 V _String 20 | PV String 20 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 2 Curr _String 20 | PV String 20 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 3 V _String 21 | PV String 21 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 4 Curr _String 21 | PV String 21 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 5 V _String 22 | PV String 22 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 6 Curr _String 22 | PV String 22 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 7 V _String 23 | PV String 23 voltage | — | 0.1 V — | — | — | — | — |
| 96 | 8 Curr _String 23 | PV String 23 Current | — | -15~15 A 0.1 A — | — | — | — | — |
| 96 | 9 V _String 24 | PV String 24 voltage | — | 0.1 V — | — | — | — | — |
| 97 | 0 Curr _String 24 | PV String 24 Current | — | -15 A~15 A 0.1 A | — | — | — | — |
| 97 | 1 V _String 25 | PV String 25 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 2 Curr _String 25 | PV String 25 Current | — | -15 A~15 A 0.1 A | — | — | — | — |
| 97 | 3 V _String 26 | PV String 26 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 4 Curr _String 26 | PV String 26 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 5 V _String 27 | PV String 27 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 6 Curr _String 27 | PV String 27 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 7 V _String 28 | PV String 28 voltage | — | — 0.1 V | — | — | — | — |
| 97 | 8 Curr _String 28 | PV String 28 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 97 | 9 V _String 29 | PV String 29 voltage | — | — 0.1 V | — | — | — | — |
| 98 | 0 Curr _String 29 | PV String 29 Current | — | -15 A~15 A 0.1 A | — | — | — | — |
| 98 | 1 V _String 30 | PV String 30 voltage | — | — 0.1 V | — | — | — | — |
| 98 | 2 Curr _String 30 | PV String 30 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 98 | 3 V _String 31 | PV String 31 voltage | — | — 0.1 V | — | — | — | — |
| 98 | 4 Curr _String 31 | PV String 31 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 98 | 5 V _String 32 | PV String 32 voltage | — | — 0.1 V | — | — | — | — |
| 98 | 6 Curr _String 32 | PV String 32 Current | — | -15~15 A 0.1 A | — | — | — | — |
| 98 | 7 Str Unmatch 2 | Bit 0~15: String 17~32 unmatch | — | — | — | — | — | — |
| 98 | 8 Str Current Unblan ce 2 | Bit 0~15:String 17~32 unblance | — | current — | — | — | — | — |
| 98 | 9 Str Disconnect 2 | Bit 0~15: String 17~32 disconn | — | ect — | — | — | — | — |
| 99 | 0 PV Warning Value | PV Warning Value (PV 9-PV 16) Contains PV 9~16 abnormal , 和 Boost 9~16 Drive anomalies | — | — | — | — | — | — |
| 99 | 1 Str Waringvalue 1 | string 1~string 16 abnormal | — | — | — | — | — | — |
| 99 | 2 Str Waringvalue 2 | string 17~string 32 abnormal | — | — | — | — | — | — |
| 99 | 9 System Cmd | M 3 to DSP system command | — | — system command | — | — | — | — |
| 10 | 00. uw Sys Work Mode | System work mode | — | 0 x 00:waiting module 0 x 01: Self-test mode, optional 0 x 02 : Reserved 0 x 03:Sys Fault module 0 x 04: Flash module 0 x 05 : m PVBATOnline 0 module, x 0 x 06 : m Bat Online module, 0 x 07 : PVOffline Mod e module, 0 x 08 : Bat Offline Mo de module, Theworkingmode displayed by the monitoring to the customer is: 0 x 00: waiting module 0 x 01: Self-test mode, 0 x 03:fault module 0 x 04:flash odule x 05|0 x 06|0 x 07|0 08:normal odule | — | — | — | — |
| 10 | 01. Systemfault word 0 | System fault word 0 | — | P t d H lease refer to hefault escription of ybrid | — | — | — | — |
| 10 | 02. Systemfault word 1 | System fault word 1 | — | — | — | — | — | — |
| 10 | 03. Systemfault word 2 | System fault word 2 | — | — | — | — | — | — |
| 10 | 04. Systemfault word 3 | System fault word 3 | — | — | — | — | — | — |
| 10 | 05. Systemfault word 4 | System fault word 4 | — | — | — | — | — | — |
| 10 | 06. Systemfault word 5 | System fault word 5 | — | — | — | — | — | — |
| 10 | 07. Systemfault word 6 | System fault word 6 | — | — | — | — | — | — |
| 10 | 08. Systemfault word 7 | System fault word 7 | — | — | — | — | — | — |
| 10 | 09. Pdischarge 1 H | Discharge power(high) | — | 0.1 W — | — | — | — | — |
| 10 | 10. Pdischarge 1 L | Discharge power (low) | — | 0.1 W — | — | — | — | — |
| 10 | 11. Pcharge 1 H | Charge power(high) | — | 0.1 W — | — | — | — | — |
| 10 | 12. Pcharge 1 L | Charge power (low) | — | 0.1 W — | — | — | — | — |
| 10 | 13. Vbat | Battery voltage | — | 0.1 V — | — | — | — | — |
| 10 | 14. SOC | State of charge Capacity | — | 0-100 1% l ith/leadacid | — | — | — | — |
| 10 | 15. Pactouser R | H AC power to user H | — | 0.1 w — | — | — | — | — |
| 10 | 16. Pactouser R | L AC power to user L | — | 0.1 w — | — | — | — | — |
| 10 | 17. Pactouser S | H Pactouser S H | — | 0.1 w — | — | — | — | — |
| 10 | 18. Pactouser S | L Pactouser S L | — | 0.1 w — | — | — | — | — |
| 10 | 19. Pactouser T | H Pactouser T H | — | 0.1 w — | — | — | — | — |
| 10 | 20. Pactouser T | L Pactouser T H | — | 0.1 w — | — | — | — | — |
| 10 | 21. Pactouser Total H | AC power to user total H | — | 0.1 w — | — | — | — | — |
| 10 | 22. Pactouser Total L | AC power to user total L | — | 0.1 w — | — | — | — | — |
| 10 | 23. Pac to grid R H | AC power to grid H | — | 0.1 w A c output | — | — | — | — |
| 10 | 24. Pac to grid R L | AC power to grid L | — | 0.1 w — | — | — | — | — |
| 10 | 25. Pactogrid S H | — | — | 0.1 w — | — | — | — | — |
| 10 | 26. Pactogrid S L | — | — | 0.1 w — | — | — | — | — |
| 10 | 27. Pactogrid T H | — | — | 0.1 w — | — | — | — | — |
| 10 | 28. Pactogrid T L | — | — | 0.1 w — | — | — | — | — |
| 10 | 29. Pactogrid total H | AC power to grid total H | — | 0.1 w — | — | — | — | — |
| 10 | 30. Pactogrid total L | AC power to grid total L | — | 0.1 w — | — | — | — | — |
| 10 | 31. PLocal Load R | H INV power to local load H | — | 0.1 w — | — | — | — | — |
| 10 | 32. PLocal Load R | L INV power to local load L | — | 0.1 w — | — | — | — | — |
| 10 | 33. PLocal Load S | H | — | 0.1 w — | — | — | — | — |
| 10 | 34. PLocal Load S | L | — | 0.1 w — | — | — | — | — |
| 10 | 35. PLocal Load T H | — | — | 0.1 w — | — | — | — | — |
| 10 | 36. PLocal Load T L | — | — | 0.1 w — | — | — | — | — |
| 10 | 37. PLocal Load total | H INV power to local load tot | — | al H 0.1 w — | — | — | — | — |
| 10 | 38. PLocal Load total | L INV power to local load tot L | — | al 0.1 w — | — | — | — | — |
| 10 | 39. IPM 2 Temperature | REC Temperature | — | 0.1℃ No use — | — | — | — | — |
| 10 | 40. Battery 2 Temperature | Battery Temperature | — | 0.1℃ Lead acid/l battery tem ithium p | — | — | — | — |
| 10 | 41. SP DSP Status | SP state | — | CHG/Dis CHG — | — | — | — | — |
| 10 | 42. SP Bus Volt | SP BUS 2 Volt | — | 0.1 V — | — | — | — | — |
| 10 | 43 | — | — | — | — | — | — | — |
| 10 | 44. Etouser_today H | Energy to user today high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 45. Etouser_today L | Energy to user today low | — | 0.1 k Wh — | — | — | — | — |
| 10 | 46. Etouser_total H | Energy to user total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 47. Etouser_ total L | Energy to user total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 48. Etogrid_today H | Energy to grid today high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 49. Etogrid _today L | Energy to grid today low | — | 0.1 k Wh — | — | — | — | — |
| 10 | 50. Etogrid _total H | Energy to grid total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 51. Etogrid _ total L | Energy to grid total high | — | 0.1 k Wh — | — | — | — | — |
| 10 | 52. Edischarge 1_toda y H | Discharge energy 1 today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 53. Edischarge 1_toda y L | Discharge energy 1 today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 54. Edischarge 1_total H | Total discharge energy 1 (high) | — | 0.1 k Wh — | — | — | — | — |
| 10 | 55. Edischarge 1_total L | Total discharge energy 1 (low) | — | 0.1 k Wh — | — | — | — | — |
| 10 | 56. Echarge 1_today H | Charge 1 energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 57. Echarge 1_today L | Charge 1 energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 58. Echarge 1_total H | Charge 1 energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 59. Echarge 1_total L | Charge 1 energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 60. ELocal Load_Today H | Local load energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 61. ELocal Load_Today L | Local load energy today | — | 0.1 k Wh — | — | — | — | — |
| 10 | 62. ELocal Load_Total H | Local load energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 63. ELocal Load_Total L | Local load energy total | — | 0.1 k Wh — | — | — | — | — |
| 10 | 64. dw Export Limit Ap parent Power | Export Limit Apparent Power H | — | 0.1 k Wh Appa rent Power | — | — | — | — |
| 10 | 65. dw Export Limit Ap parent Power | Export Limit Apparent Power L | — | 0.1 k Wh Appa rent Power | — | — | — | — |
| 10 | 66. / | / | — | / / rese rved | — | — | — | — |
| 10 | 67. EPS Fac | UPSfrequency | — | 5000/6000 0.01 Hz — | — | — | — | — |
| 10 | 68. EPS Vac 1 | UPS phase R output voltage | — | 2300 0.1 V — | — | — | — | — |
| 10 | 69. EPS Iac 1 | UPS phase R output current | — | 0.1 A — | — | — | — | — |
| 10 | 70. EPS Pac 1 H | UPS phase R output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 71. EPS Pac 1 L | UPS phase R output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 72. EPS Vac 2 | UPS phase S output voltage | — | 0.1 V — | — | — | — | — |
| 10 | 73. EPS Iac 2 | UPS phase S output current | — | 0.1 A No u se | — | — | — | — |
| 10 | 74. EPS Pac 2 H | UPS phase S output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 75. EPS Pac 2 L | UPS phase S output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 76. EPS Vac 3 | UPS phase T output voltage | — | 0.1 V — | — | — | — | — |
| 10 | 77. EPS Iac 3 | UPS phase T output current | — | 0.1 A No u se | — | — | — | — |
| 10 | 78. EPS Pac 3 H | UPS phase T output power (H) | — | 0.1 VA — | — | — | — | — |
| 10 | 79. EPS Pac 3 L | UPS phase T output power (L) | — | 0.1 VA — | — | — | — | — |
| 10 | 80. Loadpercent | Load percent of UPS ouput | — | 0-100 1% — | — | — | — | — |
| 10 | 81. PF | Power factor | — | 0-2 0.1 Prim ary Value+1 | — | — | — | — |
| 10 | 82. BMS_Status Old | Status Old from BMS | — | Detail information, refer — | — | — | — | — |
| 10 | 83. BMS_Status | Status from BMS | — | to W/R — | — | — | — | — |
| 10 | 84. BMS_Error Old | Error info Old from BMS | — | document:Growattxx Sxx — | — | — | — | — |
| 10 | 85. BMS_Error | Errorinfomation from BMS | — | P ESS Protocol; — | — | — | — | — |
| 10 | 86. BMS_SOC BMS_Battery Vol | SOC from BMS Battery voltage from BMS | — | R SP R SP H 6 K H 6 K | — | — | — | — |
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
| 11 | 00. rr BMS_MCUVersi | MCU Software version from BMS | — | — | — | — | — | — |
| 11 | 01. on BMS_Gauge Vers | Gauge Version from BMS | — | — | — | — | — | — |
| 11 | 02. ion BMS_w Gauge FR | Gauge FR Version L 16 from BMS | — | — | — | — | — | — |
| 11 | 03. Version_ L BMS_w Gauge FR | Gauge FR Version H 16 from BMS | — | — | — | — | — | — |
| 11 | 04. Version_H | — | — | — | — | — | — | — |
| 11 | 05. BMS_BMSInfo | BMSInformation from BMS | — | — | — | — | — | — |
| 11 | 06. BMS_Pack Info | Pack Information from BMS | — | — | — | — | — | — |
| 11 | 07. BMS_Using Cap | Using Cap from BMS | — | — | — | — | — | — |
| 11 | 08. uw Max Cell Volt | Maximum single battery voltage | — | 0.001 V — | — | — | — | — |
| 11 | 09. uw Min Cell Volt | Lowest single battery voltage | — | 0.001 V — | — | — | — | — |
| 11 | 10. b Module Num | Battery parallel number | — | 1 — | — | — | — | — |
| 11 | 11. uw Max Volt Cell N | Number of batteries Max Volt Cell No | — | 1 1 — | — | — | — | — |
| 11 | 12. o uw Min Volt Cell N | Min Volt Cell No | — | 1 — | — | — | — | — |
| 11 | 13. o uw Max Tempr Ce | Max Tempr Cell_10 T | — | 0.1℃ — | — | — | — | — |
| 11 | 14. ll_10 T uw Min Tempr Cel | Min Tempr Cell_10 T | — | 0.1℃ — | — | — | — | — |
| 11 | 15. l_10 T uw Max Tempr Ce | Max Volt Tempr Cell No | — | 1 — | — | — | — | — |
| 11 | 16. ll No | — | — | — | — | — | — | — |
| 11 | 17. uw Min Tempr Cel l No | Min Volt Tempr Cell No | — | 1 — | — | — | — | — |
| 11 | 18. Protect pack ID | Faulty Battery Address | — | 1 — | — | — | — | — |
| 11 | 19. Max SOC | Parallel maximum SOC | — | 1% — | — | — | — | — |
| 11 | 20. Min SOC BMS_Error 2 | Parallel minimum SOC Battery Protection 2 | — | 1% - CAN ID : 0 x 323 | — | — | — | — |
| 11 | 21. BMS_Error 3 | Battery Protection 3 | — | - Byte 4~5 CAN ID : 0 x 323 | — | — | — | — |
| 11 | 22. BMS_Warn Info 2 | Battery Warn 2 | — | - Byte 6 CAN ID : 0 x 323 | — | — | — | — |
| 11 | 23. | — | — | — Byte 7 | — | — | — | — |
| 11 | 24 AC Charge Energy Today H | AC Charge Energy today | — | kwh Energy today | — | — | — | — |
| 11 | 25. ACCharge Energy Today L | AC Charge Energy today | — | kwh — | — | — | — | — |
| 11 | 26. 1 Charge AC Energy Total H | — | — | — Energy total | — | — | — | — |
| 11 | 27. ACCharge Energy Total L | — | — | — | — | — | — | — |
| 11 | 28. AC Charge Power H | AC Charge Power | — | W — | — | — | — | — |
| 11 | 29. AC Charge Power L | AC Charge Power | — | w — | — | — | — | — |
| 11 | 30. 70% INV Power adjust | uw Grid Power_70_Adj EE_SP | — | W — | — | — | — | — |
| 11 | 31. Extra AC Power Ex to grid_H Hi | tra inverte AC Power to grid gh | — | For SPA connect inverter SPA used | — | — | — | — |
| 11 | 32. Extra AC Power Ex to grid_L | trainverte AC Power to grid Low | — | — SPA used | — | — | — | — |
| 11 | 33. Eextra_today H | Extra inverter Power TOUser_Extr today (high) | — | a R 0.1 k Wh SPA used | — | — | — | — |
| 11 | 34. Eextra_today L | Extra inverter Power TOUser_Extr today (low) | — | a R 0.1 k Wh SPA used | — | — | — | — |
| 11 | 35. Eextra_total H | Extra inverter Power TOUser_Extr total(high) | — | a 0.1 k Wh SPA used | — | — | — | — |
| 11 | 36. Eextra_total L | Extra inverter Power TOUser_Extr total(low) | — | a 0.1 k Wh SPA used | — | — | — | — |
| 11 | 37. Esystem_today H | System electric energy today H | — | 0.1 k Wh SPA used System electric energy today H | — | — | — | — |
| 11 | 38. Esystem_ today Sy L | stem electric energy today L | — | 0.1 k Wh SPA use System energy d electric today L | — | — | — | — |
| 11 | 39. Esystem_total H | System electric energy total H | — | 0.1 k Wh SPA use System energy d electric total H | — | — | — | — |
| 11 | 40. Esystem_ total L | System electric energy total L | — | 0.1 k Wh SPA use System energy d electric total L | — | — | — | — |
| 11 | 41. Eself_today H | self electric energy today H | — | 0.1 k Wh self energy electric today H | — | — | — | — |
| 11 | 42. Eself_ today L | self electric energy today L | — | 0.1 k Wh self energy electric today L | — | — | — | — |
| 11 | 43. Eself_total H | self electric energy total H | — | 0.1 k Wh self energy electric total H | — | — | — | — |
| 11 | 44. Eself_ total L | self electric energy total L | — | 0.1 k Wh self energy electric total L | — | — | — | — |
| 11 | 45. PSystem H | System power H | — | 0.1 w System power H | — | — | — | — |
| 11 | 46. PSystem L | System power L | — | 0.1 w System power L | — | — | — | — |
| 11 | 47. PSelf H | self power H | — | 0.1 w self po wer H | — | — | — | — |
| 11 | 48. PSelf L | self power L | — | 0.1 w self po wer L | — | — | — | — |
| 11 | 49. EPVAll_Today H | PV electric energy today H | — | — | — | — | — | — |
| 11 | 50. EPVAll_Today L | PV electric energy today L | — | — | — | — | — | — |
| 11 | 51. Ac Discharge Pack Sn | Discharge power pack number | — | serial R / — | — | — | — | — |
| 11 | 52. Accdischarge power_H | Cumulative discharge power high 16-bit byte | — | R 0.1 k WH — | — | — | — | — |
| 11 | 53. Accdischarge power_L | Cumulative discharge power low 16-bit byte | — | R 0.1 k WH — | — | — | — | — |
| 11 | 54. Acc Charge Pack Sn | charge power pack serial number | — | R / — | — | — | — | — |
| 11 | 55. Acc Charge power_H | Cumulative charge power high R 16-bit byte | — | 0.1 k WH — | — | — | — | — |
| 11 | 56. Acc Charge power_L | Cumulative charge power low R 16-bit byte | — | 0.1 k WH — | — | — | — | — |
| 11 | 57. First Batt Fault Sn | First Batt Fault Sn | — | R / — | — | — | — | — |
| 11 | 58. Second Batt Fault Sn | Second Batt Fault Sn | — | R / — | — | — | — | — |
| 11 | 59. Third Batt Fault Sn | Third Batt Fault Sn | — | R / — | — | — | — | — |
| 11 | 60. Fourth Batt Fault Sn | Fourth Batt Fault Sn | — | R / — | — | — | — | — |
| 11 | 61. Battery history fault code 1 | Battery history fault code 1 | — | R / — | — | — | — | — |
| 11 | 62. Battery history fault code 2 | Battery history fault code 2 | — | R / — | — | — | — | — |
| 11 | 63. Battery history fault code 3 | Battery history fault code 3 | — | R / — | — | — | — | — |
| 11 | 64. Battery history fault code 4 | Battery history fault code 4 | — | R / — | — | — | — | — |
| 11 | 65. Battery history fault code 5 | Battery history fault code 5 | — | R / — | — | — | — | — |
| 11 | 66. Battery history fault code 6 | Battery history fault code 6 | — | R / — | — | — | — | — |
| 11 | 67. Battery history fault code 7 | Battery history fault code 7 | — | R / — | — | — | — | — |
| 11 | 68. Battery history fault code 8 | Battery history fault code 8 | — | R / — | — | — | — | — |
| 11 | 69. Number of battery codes | Number of battery codes PACK number + BIC forward and reverse codes | — | R / — | — | — | — | — |
| 11 | 70. | — | — | — | — | — | — | — |
| 11 | 99 New EPower Calc Flag | Intelligent reading is used to identify software compatibility features | — | 0 : Old ene calculation 1 : new ene calculation rgy ; rgy | — | — | — | — |
| 1 | 200 Max Cell Volt | Maximum cell voltage | — | R 0.001 V — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 201 Min Cell Volt | Minimum cell voltage | — | R 0.001 V — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 202 Module Num | Number of Battery modules | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 203 Total Cell Num | Total number of cells | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 204 Max Volt Cell No | Max Volt Cell No | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 205 Min Volt Cell No | Min Volt Cell No | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 206 Max Tempr Cell_ 10 T | Max Tempr Cell_10 T | — | R 0.1℃ — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 207 Min Tempr Cell_1 0 T | Min Tempr Cell_10 T | — | R 0.1℃ — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 208 Max Tempr Cell N o | Max Tempr Cell No | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 209 Min Tempr Cell N o | Min Tempr Cell No | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 210 Protect Pack ID | Fault Pack ID | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 211 Max SOC | Parallel maximum SOC | — | R 1% — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 212 Min SOC | Parallel minimum SOC | — | R 1% — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 213 Bat Protect 1 Add | Bat Protect 1 Add | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 214 Bat Protect 2 Add | Bat Protect 2 Add | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 215 Bat Warn 1 Add | Bat Warn 1 Add | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 216 BMS_Highest Sof t Version | BMS_Highest Soft Version | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 217 BMS_Hardware Version | BMS_Hardware Version | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 1 | 218 BMS_Request Ty pe | BMS_Request Type | — | R / — | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 12 | 48 b Key Aging Test O k Flag | Success sign of key detection before aging | — | — 1:Finished test 0 : test not completed | — | — | — | — |
| 12 | 49. / | / | — | / / reversed | — | — | — | — |
| 20 | 00 Inverter Status | Inverter run state | — | 0:waiting, 1:normal, 3:fault SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 35 Pac H | Output power (high) | — | 0. 1 W SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 36 Pac L | Output power (low) | — | 0. 1 W SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 37 Fac | Grid frequency | — | 0. 01 Hz SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 38 Vac 1 | Three/single phase grid voltage | — | 0. 1 V SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 39 Iac 1 | Three/single phase grid output | — | current 0. 1 A SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 40 Pac 1 H | Three/single phase grid output VA (high) | — | watt 0. 1 VA SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 41 Pac 1 L | Three/single phase grid output VA(low) | — | watt 0. 1 VA SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 53 Eac today H | Today generate energy (high) | — | 0. 1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 54 Eac today L | Today generate energy (low) | — | 0. 1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 55 Eac total H | Total generate energy (high) | — | 0.1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 56 Eac total L | Total generate energy (low) | — | 0.1 k WH SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 57 Time total H | Work time total (high) | — | 0.5 s SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 58 Time total L | Work time total (low) | — | 0.5 s SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 93 Temp 1 | Inverter temperature | — | 0.1 C SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 94 Temp 2 | The inside IPM in inverter Temp | — | erature 0.1 C SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 95 Temp 3 | Boost temperature | — | 0.1 C SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 96 Temp 4 | — | — | — reserved | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 97 uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 98 P Bus Voltage | P Bus inside Voltage | — | 0.1 V SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 20 | 99 N Bus Voltage | N Bus inside Voltage | — | 0.1 V SPA | — | — | offgrid:grid_voltage | Grid voltage |
| 21 | 00 Remote Ctrl En | / | — | / 0.Load First 1.Bat First Remote setup enable | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 01 Remote Ctrl Pow er | / | — | 2.Grid / Remotely set power | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 02 Extra AC Power to grid_H | Extra inverte AC Power to grid | — | High For SPA connect inverter SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 03 Extra AC Power to grid_L | Extrainverte AC Power to grid L | — | ow SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 04 Eextra_today H | Extra inverter Power TOUser_Extr today (high) | — | a R 0.1 k Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 05 Eextra_today L | Extra inverter Power TOUser_Extr today (low) | — | a R 0.1 k Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 06 Eextra_total H | Extra inverter Power TOUser_Extratotal(high) | — | 0.1 k Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 07 Eextra_total L | Extra inverter Power TOUser_Extr total(low) | — | a 0.1 k Wh SPA used | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 08 Esystem_today H | System electric energy today H | — | 0.1 k Wh SPA used System electric energy today H | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 09 Esystem_ today Sy L | stem electric energy today L | — | 0.1 k Wh SPA used System electric energy today L | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 10 Esystem_total H | System electric energy total H | — | 0.1 k electri energy H Wh SPA used System c total | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 11 Esystem_ total L | System electric energy total L | — | 0.1 k Wh SPA use System electri energy L d c total | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 12 EACharge_Today _H | ACCharge energy today | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 13 EACharge_Today _L | ACCharge energy today | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 14 EACharge_Total _H | ACCharge energy total | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 15 EACharge_Total _L | ACCharge energy total | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 16 AC charge Power_H | Grid power to local load | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 17 AC charge Power_L | Grid power to local load | — | 0.1 kwh Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 18 Priority | 0:Load First 1:Battery First 2:Grid First | — | Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 19 Battery Type | 0:Lead-acid 1:Lithium battery | — | Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 20 Auto Proofread C MD | Aging mode | — | Storage Power — | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 21 | 24. reserved | — | — | reserve d | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 3 | 000 | 2: Reserved 3:Sys Fault module 4: Flash module 5:PVBATOnline module: 6:Bat Online module 7:PVOffline Mode 8:Bat Offline Mode The lower 8 bits indicate the m status (web page display) 0: Standby Status; 1: Normal Status; 3: Fault Status 4:Flash Status; | — | achine — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 001 Ppv H | PV total power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 002 Ppv L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 003 Vpv 1 | PV 1 voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 004 Ipv 1 | PV 1 input current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 005 Ppv 1 H | PV 1 power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 006 Ppv 1 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 007 Vpv 2 | PV 2 voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 008 Ipv 2 | PV 2 input current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 009 Ppv 2 H | PV 2 power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 010 Ppv 2 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 011 Vpv 3 | PV 3 voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 012 Ipv 3 | PV 3 input current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 013 Ppv 3 H | PV 3 power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 014 Ppv 3 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 015 Vpv 4 | PV 4 voltage | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 016 Ipv 4 | PV 4 input current | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 017 Ppv 4 H | PV 4 power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 018 Ppv 4 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 019 Psys H | System output power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 020 Psys L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 021 Qac H Qac L | reactive power | — | 0.1 Var — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 022 | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 023 Pac H | Output power | — | 0.1 W Outp ut | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 024 Pac L Fac | Grid frequency | — | powe 0.01 Hz Grid r | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 025 Vac 1 | Three/single phase grid voltage | — | freq 0.1 V Thre uency e/single | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 026 | — | — | phas volt e grid age | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 027 Iac 1 | Three/single phase grid output | — | current 0.1 A Thre phase g output current e/single rid | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 028 Pac 1 H Pac 1 L | Three/single phase grid output VA | — | watt 0.1 VA Three/s phase g ingle rid | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 029 Vac 2 | Three phase grid voltage | — | output VA 0.1 V Three p watt hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 030 Iac 2 | Three phase grid output current | — | grid vo 0.1 A Three p ltage hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 031 | — | — | grid ou current tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 032 Pac 2 H Pac 2 L | Three phase grid output power | — | 0.1 VA Three p grid ou hase tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 033 Vac 3 | Three phase grid voltage | — | power 0.1 V Three p hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 034 Iac 3 | Three phase grid output current | — | grid vo 0.1 A Three p ltage hase | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 035 | — | — | grid ou current tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 036 Pac 3 H Pac 3 L | Three phase grid output power | — | 0.1 VA Three p grid ou hase tput | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 037 | — | — | power — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 038 Vac_RS | Three phase grid voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 039 Vac_ST | Three phase grid voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 040 Vac_TR | Three phase grid voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 041 Ptouser total H | Total forward power | — | 0.1 W Total f power orward | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 042 Ptouser total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 043 Ptogrid total H | Total reverse power | — | 0.1 W Total r power everse | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 044 Ptogrid total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 045 Ptoload total H | Total load power | — | 0.1 W Total power load | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 046 Ptoload total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 047 Time total H | Work time total | — | 0.5 s — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 048 Time total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 049 Eac today H Eac today L | Today generate energy | — | 0.1 k Wh Today generat e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 050 | — | — | energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 051 Eac total H | Total generate energy | — | 0.1 k Wh Total — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 052 Eac total L | — | — | generat energy e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 053 Epv_total H | PV energy total | — | 0.1 k Wh PV energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 054 Epv_total L | — | — | total — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 055 Epv 1_today H | PV 1 energy today | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 056 Epv 1_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 057 Epv 1_total H | PV 1 energy total | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 058 Epv 1_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 059 Epv 2_today H | PV 2 energy today | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 060 Epv 2_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 061 Epv 2_total H | PV 2 energy total | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 062 Epv 2_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 063 Epv 3_today H | PV 3 energy today | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 064 Epv 3_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 065 Epv 3_total H | PV 3 energy total | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 066 Epv 3_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 067 Etouser_today H | Today energy to user | — | 0.1 k Wh Today energy to user — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 068 Etouser_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 069 Etouser_total H | Total energy to user | — | 0.1 k Wh Total energy to user — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 070 Etouser_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 071 Etogrid_today H | Today energy to grid | — | 0.1 k Wh Today energy to grid — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 072 Etogrid_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 073 Etogrid_total H | Total energy to grid | — | 0.1 k Wh Total energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 074 Etogrid_total L | — | — | to grid — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 075 Eload_today H | Today energy of user load | — | 0.1 k Wh Today energy of user load — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 076 Eload_today L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 077 Eload_total H | Total energy of user load | — | 0.1 k Wh Total energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 078 Eload_total L | — | — | of user load — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 079 Epv 4_today H Epv 4_today L | PV 4 energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 080 | — | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 081 Epv 4_total H Epv 4_total L | PV 4 energy total | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 082 | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 083 Epv_today H | PV energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 084 Epv_today L | — | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 085 Reserved Derating Mode | Derating Mode | — | 0:c NOTDerate 1:c PVHigh Der ate 2: c Power Con stant Derate 3: c Grid VHig Derate 4:c Freq High D erate 5:c Dc Soure M ode Derate 6:c Inv Tempr D erate 7:c Active Pow er Order 8:c Load Speed Process h | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 086 | — | — | 9:c Over Bac by Time 10:c Internal empr Derate 11:c Out Temp r Derate 12:c Line Impe Calc Derate 13: c Paralle nti Backflow D erate 14:c Local Ant Backflow Dera te 15:c Bdc Load P ri Derate 16:c Chk CTErr Derate k T l A i | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 087 ISO | PV ISO value | — | 1 KΩ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 088 DCI_R | R DCI Curr | — | 0.1 m A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 089 DCI_S | S DCI Curr | — | 0.1 m A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 090 DCI_T | T DCI Curr | — | 0.1 m A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 091 GFCI | GFCI Curr | — | 1 m A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 092 Bus Voltage | total bus voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 093 Temp 1 | Inverter temperature | — | 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 094 Temp 2 | The inside IPM in inverter temp | — | erature 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 095 Temp 3 | Boost temperature | — | 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 096 Temp 4 | Reserved | — | 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 097 Temp 5 | Commmunication broad temperatur | — | e 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 098 P Bus Voltage | P Bus inside Voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 099 N Bus Voltage | N Bus inside Voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 100 IPF | Inverter output PF now | — | 0-20 000 | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 101 Real OPPercent | Real Output power Percent | — | 1% 1~10 0 | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 102 OPFullwatt H OPFullwatt L | Output Maxpower Limited | — | 0.1 W Outp Maxp ut ower | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 103 Standby Flag | Inverter standby flag | — | Limi bitfield bit 0 Orde bit 1 bit 2 ted :turn off r; :PV Low; :AC | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 104 | — | — | Volt out bit 3 Rese /Freq of scope; ~bit 7 : rved | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 105 Fault Maincode | Inverter fault maincode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 106 Warn Maincode | Inverter Warning maincode | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 107 Fault Subcode | Inverter fault subcode | — | bitfield — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 108 Warn Subcode | Inverter Warning subcode | — | bitfield — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 109 | — | — | bitfield — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 110 uw Present FFTVa | Present FFTValue [CHANNEL_A] | — | bitfield bitfield — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 111 lue [CHANNEL_A ] b Afci Status | AFCI Status | — | 0 : stat 1:se 2 : waiting e lf-check Detection | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 112 uw Strength[CHA | AFCI Strength[CHANNEL_A] | — | of stat 3:fa 4 : stat arcing e ult state update e | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 113 NNEL_A] uw Self Check Val | AFCI Self Check[CHANNEL_A] | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 114 ue[CHANNEL_A] inv start delay | inv start delay time | — | 1 S inv start de lay | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 115 time | — | — | time — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 116 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 117 Reserved BDC_On Off State | BDC connect state | — | 0:No BDC Connect 1:BDC 1 Connect — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 118 Dry Contact State | Current status of Dry Contact | — | 2:BDC 2 Connect 3:BDC 1+BDC 2 Connect Current status of | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 119 | — | — | Dry Contact 0: turn off; 1: turn on; — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 120 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 121 Pself H Pself L | self-use power | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 122 | — | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 123 Esys_today H Esys_today L | System energy today | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 124 | — | — | 0.1 kwh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 125 Edischr_today H Edischr_today L | Today discharge energy | — | 0.1 k Wh Today discharge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 126 | — | — | energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 127 Edischr_total H Edischr_total L | Total discharge energy | — | 0.1 k Wh Total discharge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 128 | — | — | energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 129 Echr_today H | Charge energy today | — | 0.1 k Wh Charge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 130 Echr_today L | — | — | energy today — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 131 Echr_total H | Charge energy total | — | 0.1 k Wh Charge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 132 Echr_total L | — | — | energy total — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 133 Eacchr_today H | Today energy of AC charge | — | 0.1 k Wh Today energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 134 Eacchr_today L | — | — | of AC charge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 135 Eacchr_total H | Total energy of AC charge | — | 0.1 k Wh Total energy — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 136 Eacchr_total L | — | — | of AC charge — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 137 Esys_total H Esys_total L | Total energy of system outpu | — | t \ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 138 | — | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 139 Eself_today H Eself_today L | Today energy of Self output | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 140 | — | — | 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 141 Eself_total H Eself_ total L | Total energy of Self output | — | 0.1 kwh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 142 | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 143 Reserved Priority | Word Mode | — | 0 Lo 1 ad First | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 144 | — | — | Batt t 2 Gr ery Firs id First | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 145 EPS Fac | UPS frequency | — | 0.01 Hz — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 146 EPS Vac 1 | UPS phase R output voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 147 EPS Iac 1 | UPS phase R output current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 148 EPS Pac 1 H | UPS phase R output power | — | 0.1 VA — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 149 EPS Pac 1 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 150 EPS Vac 2 | UPS phase S output voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 151 EPS Iac 2 | UPS phase S output current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 152 EPS Pac 2 H | UPS phase S output power | — | 0.1 VA — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 153 EPS Pac 2 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 154 EPS Vac 3 | UPS phase T output voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 155 EPS Iac 3 | UPS phase T output current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 156 EPS Pac 3 H | UPS phase T output power | — | 0.1 VA — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 157 EPS Pac 3 L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 158 EPS Pac H | UPS output power | — | 0.1 VA — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 159 EPS Pac L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 160 Loadpercent | Load percent of UPS ouput | — | 0.10% — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 161 PF | Power factor | — | 0.1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 162 DCV | DC voltage | — | 1 m V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 163 Reserved New Bdc Flag | Whether to parse BDC data separ | — | ately 0: D on't need | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 164 BDCDerating Mo de | BDCDerating Mode: 0: Normal, unrestricted 1:Standby or fault | — | 1:ne ed | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 165 Sys State_Mode | 2:Maximum battery current limit (discharge) 3:Battery discharge Enable (Dis 4:High bus discharge derating (discharge) 5:High temperature discharge derating (discharge) 6:System warning No discharge (discharge) 7-15 Reserved (Discharge) 16:Maximum charging current of battery (charging) 17:High Temperature (LLC and Buckboost) (Charging) 18:Final soft charge 19:SOC setting limits (charging 20:Battery low temperature (cha 21:High bus voltage (charging) 22:Battery SOC (charging) 23: Need to charge (charge) 24: System warning not charging (charging) 25-29:Reserve (charge) System work State and mode The upper 8 bits indicate the mode; 0:No charge and discharge; 1:charge; 2:Discharge; | — | charge) ) rging) BDC 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 166 | The lower 8 bits represent the 0: Standby Status; 1: Normal Status; 2: Fault Status 3:Flash Status; | — | status; — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 167 Fault Code | Storge device fault code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 168 Warn Code | Storge device warning code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 169 Vbat | Battery voltage | — | 0.01 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 170 Ibat | Battery current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 171 SOC | State of charge Capacity | — | 1% — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 172 Vbus 1 | Total BUS voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 173 Vbus 2 | On the BUS voltage | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 174 Ibb | BUCK-BOOST Current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 175 Illc | LLC Current | — | 0.1 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 176 Temp A | Temperture A | — | 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 177 Temp B | Temperture B | — | 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 178 Pdischr H | Discharge power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 179 Pdischr L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 180 Pchr H | Charge power | — | 0.1 W — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 181 Pchr L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 182 Edischr_total H | Discharge total energy of storg | — | e device 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 183 Edischr_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 184 Echr_total H | Charge total energy of storge d | — | evice 0.1 k Wh — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 185 Echr_total L | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 186 Reserved BDC 1_Flag | Reserved BDC mark (charge and dischar fault alarm code) Bit 0: Charge En; BDC allows char Bit 1: Discharge En; BDC allows discharge | — | ge, ging — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 187 | Bit 2~7: Resvd; reserved Bit 8~11: Warn Sub Code; BDC sub-warning code Bit 12~15: Fault Sub Code; BDC sub-error code | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 188 Vbus 2 Bms Max Volt Cell | Lower BUS voltage Bms Max Volt Cell No | — | 0.1 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 189 No Bms Min Volt Cell | Bms Min Volt Cell No | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 190 No Bms Battery Avg T | Bms Battery Avg Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 191 emp Bms Max Cell Tem | Bms Max Cell Temp | — | 0.1°C — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 192 p Bms Battery Avg T | Bms Battery Avg Temp | — | 0.1°C — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 193 emp Bms Max Cell Tem | Bms Max Cell Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 194 p Bms Battery Avg T | Bms Battery Avg Temp | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 195 emp | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 196 Bms Max SOC | Bms Max SOC | — | 1% — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 197 Bms Min SOC Parallel Battery N | Bms Min SOC Parallel Battery Num | — | 1% — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 198 um Bms Derate Reas | Bms Derate Reason | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 199 on Bms Gauge FCC | Bms Gauge FCC(Ah) | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 200 (Ah) Bms Gauge RM | Bms Gauge RM(Ah) | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 201 (Ah) | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 202 Bms Error | BMS Protect 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 203 Bms Warn | BMSWarn 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 204 Bms Fault | BMS Fault 1 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 205 Bms Fault 2 | BMS Fault 2 | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 206 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 207 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 208 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 209 Reserved Bat Iso Status | Battery ISO detection status | — | 0:Not detected — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 210 Batt Need Charge Request Flag | battery work request | — | 1 : Detectio completed bit 0:1: Prohibit chargin g,0: Allow the chargin g bit 1:1: Enable strong charge, n | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 211 BMS_Status | battery working status | — | 0: disable strong charge bit 2:1: Enable strong charge 2 0: disable strong charge 2 bit 8:1: Dischar ge is prohibit ed, 0: allow discharg e bit 9:1: Turn on power reductio n 0: turn off power reductio n; R 0: dor 1:Char 2:Disc 3:free mancy ge harge | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 212 | — | — | 4:stan 5:Soft 6:faul 7:upda dby start t te | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 213 Bms Error 2 | BMS Protect 2 | — | R 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 214 Bms Warn 2 | BMS Warn 2 | — | R 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 215 BMS_SOC BMS_Battery Vol | BMS SOC BMS Battery Volt | — | R 1% R 0.01 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 216 t BMS_Battery Cur | BMS Battery Curr | — | R 0.01 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 217 r BMS_Battery Te | battery cell maximum temperatur | — | e R 0.1℃ — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 218 mp | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 219 BMS_Max Curr BMS_Max Dischr | Maximum charging current Maximum discharge current | — | R 0.01 A R 0.01 A — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 220 Curr | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 221 BMS_Cycle Cnt | BMSCycle Cnt | — | R 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 222 BMS_SOH BMS_Charge Vol | BMS SOH Battery charging voltage limit | — | R 1 value R 0.01 V — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 223 t Limit BMS_Discharge | Battery discharge voltage limit | — | value — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 224 Volt Limit | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 225 Bms Warn 3 | BMS Warn 3 | — | R 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 226 Bms Error 3 | BMS Protect 3 | — | R 1 — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 227 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 3 | 228 Reserved | — | — | — | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 32 | 29 Reserved | — | — | — | — | — | — | — |
| 32 | 30 BMSSingle Volt M ax | BMS Battery Single Volt Max | — | R 0.001 V — | — | — | — | — |
| 32 | 31 BMSSingle Volt M in | BMS Battery Single Volt Min | — | R 0.001 V — | — | — | — | — |
| 32 | 32 Bat Load Volt | Battery Load Volt | — | R 0.01 V [ 0,650.00] | — | — | — | — |
| 32 | 33 | — | — | — | — | — | — | — |
| 32 | 34 Debug data 1 | Debug data 1 | — | R — | — | — | — | — |
| 32 | 35 Debug data 2 | Debug data 2 | — | R — | — | — | — | — |
| 32 | 36 Debug data 3 | Debug data 3 | — | R — | — | — | — | — |
| 32 | 37 Debug data 4 | Debug data 4 | — | R — | — | — | — | — |
| 32 | 38 Debug data 5 | Debug data 5 | — | R — | — | — | — | — |
| 32 | 39 Debug data 6 | Debug data 6 | — | R — | — | — | — | — |
| 32 | 40 Debug data 7 | Debug data 7 | — | R — | — | — | — | — |
| 32 | 41 Debug data 8 | Debug data 8 | — | R — | — | — | — | — |
| 32 | 42 Debug data 9 | Debug data 9 | — | R — | — | — | — | — |
| 32 | 43 Debug data 10 | Debug data 10 | — | R — | — | — | — | — |
| 32 | 44 Debug data 10 | Debug data 10 | — | R — | — | — | — | — |
| 32 | 45 Debug data 12 | Debug data 12 | — | R — | — | — | — | — |
| 32 | 46 Debug data 13 | Debug data 13 | — | R — | — | — | — | — |
| 32 | 47 Debug data 14 | Debug data 14 | — | R — | — | — | — | — |
| 32 | 48 Debug data 15 | Debug data 15 | — | R — | — | — | — | — |
| 32 | 49 Debug data 16 | Debug data 16 | — | R — | — | — | — | — |
| 32 | 50 Pex 1 H | PV inverter 1 output power H | — | R 0.1 W — | — | — | — | — |
| 32 | 51 Pex 1 L | PV inverter 1 output power L | — | R 0.1 W — | — | — | — | — |
| 32 | 52 Pex 2 H | PV inverter 2 output power H | — | R 0.1 W — | — | — | — | — |
| 32 | 53 Pex 2 L | PV inverter 2 output power L | — | R 0.1 W — | — | — | — | — |
| 32 | 54 Eex 1 Today H | PV inverter 1 energy Today H | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 55 Eex 1 Today L | PV inverter 1 energy Today L | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 56 Eex 2 Today H | PV inverter 2 energy Today H | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 57 Eex 2 Today L | PV inverter 2 energy Today L | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 58 Eex 1 Total H | PV inverter 1 energy Total H | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 59 Eex 1 Total L | PV inverter 1 energy Total L | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 60 Eex 2 Total H | PV inverter 2 energy Total H | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 61 Eex 2 Total L | PV inverter 2 energy Total L | — | R 0.1 k Wh — | — | — | — | — |
| 32 | 62 uw Bat No | battery pack number | — | R BD ar ev mi C reports e updated ery 15 nutes | — | — | — | — |
| 32 | 63 Bat Serial Num 1 | Battery pack serial number SN[0] | — | SN[1] R BD ar C reports e updated | — | — | — | — |
| 32 | 64 Bat Serial Num 2 | Battery pack serial number SN[2] | — | SN[3] R ev ery 15 | — | — | — | — |
| 32 | 65 Bat Serial Num 3 | Battery pack serial number SN[4] | — | SN[5] R mi nutes | — | — | — | — |
| 32 | 66 Bat Serial Num 4 | Battery pack serial number SN[6] | — | SN[7] R — | — | — | — | — |
| 32 | 67 Bat Serial Num 5 | Battery pack serial number SN[8] | — | SN[9] R — | — | — | — | — |
| 32 | 68 Bat Serial Num 6 | Battery pack serial number SN[10]SN[11] | — | R — | — | — | — | — |
| 32 | 69 Bat Serial Num 7 | Battery pack serial number SN[12]SN[13] | — | R — | — | — | — | — |
| 32 | 70 Bat Serial Num 8 | Battery pack serial number SN[14]SN[15] | — | R — | — | — | — | — |
| 32 | 71- Reserve | Reserve | — | — | — | — | — | — |
| 32 | 79 | — | — | — | — | — | — | — |
| 32 | 80 b Clr Today Data Fl ag | Clear day data flag | — | R Da cu th se ta of the rrent day at the rver determines whether to clear. 0:not cleared. 1: Clear. | — | — | — | — |
| 40 | 00- 1 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | — | — |
| 41 | 07 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | — | — |
| 41 | 08- 2 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | — | — |
| 42 | 15 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | offgrid:fault_code | Fault code |
| 48 | 64- 9 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 49 | 71 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | — | — |
| 49 | 72- 10 | The first 8 registers are the 1 | — | 6-bit serial number of BDC, th en 69 registers have the | — | — | — | — |
| 50 | 79 | same data area as 3165-3233, th 108 registers (including 8 regi | — | e remaining 31 registers are r sters occupied by serial numbe eserved, a total of r). | — | — | offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |

