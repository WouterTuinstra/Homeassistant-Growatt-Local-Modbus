# Growatt Modbus Register Map (Protocol v1.24)

This file documents every holding (FC=03/06/16) and input (FC=04) register described in Growatt’s Modbus protocol v1.24 and cross-references them with the Home Assistant `growatt_local` integration. Source tables were extracted directly from the PDF specification.

**Legend**: Access = spec write flag (`R`, `W`, `R/W`). “Range/Unit” merges the spec range column with the unit, when available. “Attributes” lists the integration attribute(s) mapped to the register; “Sensors” lists Home Assistant sensor entities exposing the attribute. Rows without attributes are not currently surfaced by the integration (typically configuration or reserved registers).

*Descriptions and notes are copied verbatim from the PDF specification. Some spacing may appear collapsed due to automated extraction; consult the original document when exact phrasing is required.*

## Coverage Summary
| Section | Spec Registers | Covered | Missing |
| --- | --- | --- | --- |
| Common Holding Registers (0–124) | 125 | 8 | 117 |
| TL-X/TL-XH Holding Registers (3000–3124) | 107 | 0 | 107 |
| TL-XH US Holding Registers (3125–3249) | 63 | 0 | 63 |
| TL3/MAX/MID/MAC Holding Registers (125–249) | 97 | 0 | 97 |
| Storage Holding Registers (1000–1124) | 97 | 0 | 97 |
| Storage Holding Registers (1125–1249) | 14 | 0 | 14 |
| Common Input Registers (0–124) | 122 | 84 | 38 |
| TL-X/TL-XH Input Registers (3000–3124) | 125 | 55 | 70 |
| TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249) | 125 | 52 | 73 |
| TL-X/TL-XH Extended Input Registers (3250–3374) | 23 | 0 | 23 |
| Storage Input Registers (1000–1124) | 125 | 13 | 112 |
| Storage Input Registers (1125–1249) | 68 | 0 | 68 |
| Storage Input Registers (2000–2124) | 43 | 0 | 43 |
| Storage TL-XH Input Registers (3041–3231) | 191 | 62 | 129 |
| Offgrid SPF Input Registers | 877 | 41 | 836 |

## Common Holding Registers (0–124)
Applies to TL-X/TL-XH, TL3/MAX/MID/MAC, and MIX/SPA/SPH storage families.

**Applies to:** TL-X/TL-XH/TL-XH US, TL3-X/MAX/MID/MAC, Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | On Off | Remote On/Off. On(1);Of(f 0)Inverter On(3);Off(2)BDC | W | 0, 1, 2, 3 | 1 | Theinvertercanbeswitched onandoff,andthe BDCcanbe switchedonandoffforthe battreadyfunction. | tlx:inverter_enabled, tl3:inverter_enabled | — |
| 01 | Safty Func En | Bit 0:SPIenable Bit 1:Auto Test Start Bit 2:LVFRTenable Bit 3:Freq Derating Enable Bit 4:Softstartenable Bit 5:DRMSenable Bit 6:Power Volt Func Enable Bit 7:HVFRTenable Bit 8:ROCOFenable Bit 9:Recover Freq Derating Mode Enable | W | 0 : disable 1:enable | — | SPI: system protection interface Bit 0~3:for CEI 0-21 Bit 4~6:for SAA | — | — |
| 02 | PF CMD memory state | Set Holding register 3,4,5,99 CMD will be memory or not(1/0), if not, these settings are the initialvalue. | W | 0 or 1 | 0 | Means these settings will be acting or not when next poweron | — | — |
| 03 | Active P Rate | Inverter Max output activepowerpercent | W | 0-100 or 255 % | 255 | 255:powerisnotbelimited | — | — |
| 04 | Reactive P Rate | Inverter max output reactivepowerpercent | W | -100-100 or 255 % | 255 | 255:powerisnotbelimited | — | — |
| 05 | Powerfactor | Inverter output power factor’s 10000 times | W | 0-20000, 0-10000 is underexci ted,other is overexcit ed | 0 | — | — | — |
| 06 | Pmax H | Normal power(high) | — | 0.1 VA | — | — | — | — |
| 07 | Pmax L | Normal power(low) | — | 0.1 VA | — | — | — | — |
| 08 | Vnormal | Normalwork PV voltage | — | 0.1 V | — | — | — | — |
| 09 | Fwversion H | Firmwareversion (high) | — | ASCII | — | — | tlx:firmware, tl3:firmware, storage:firmware | — |
| 10 | Fw version M | Firmwareversion (middle) | — | — | — | — | — | — |
| 11 | Fwversion L | Firmwareversion(low) | — | — | — | — | — | — |
| 12 | Fw version 2 H | Control Firmware version(high) | — | ASCII | — | — | — | — |
| 13 | Fw version 2 M | Control Firmware version(middle) | — | — | — | — | — | — |
| 14 | Fw version 2 L | Control Firmware version(low) | — | — | — | — | — | — |
| 15 | LCD language | LCDlanguage | W | 0-5 | — | 0:Italian; 1:English; 2:German; 3:Spanish; 4:French; 5:Chinese; 6:Polish 7:Portugues 8:Hungary | — | — |
| 16 | Country Sele cted | Country Selectedor not | W | 0: need toselect; 1: have selected | — | — | — | — |
| 17 | Vpvstart | Inputstartvoltage | W | 0.1 V | — | — | — | — |
| 18 | Timestart | Starttime | W | 1 s | — | — | — | — |
| 19 | Restart Delay Time | Restart Delay Time afterfaultback; | W | 1 s | — | — | — | — |
| 20 | w Power Start Slope | Powerstartslope | W | 1-1000 0.1% | — | — | — | — |
| 21 | w Power Rest art Slope EE | Powerrestartslope | W | 1-1000 0.1% | — | — | — | — |
| 22 | w Select Baud rate | Select communicationbaudrat e 0:9600 bps 1:38400 bps | W | 0-1 | 0 | — | — | — |
| 23 | Serial NO | Serialnumber 1-2 | — | ASCII | — | — | tlx:serial number, tl3:serial number | — |
| 24 | Serial NO | Serialnumber 3-4 | — | — | — | — | — | — |
| 25 | Serial NO | Serialnumber 5-6 | — | — | — | — | — | — |
| 26 | Serial NO | Serialnumber 7-8 | — | — | — | — | — | — |
| 27 | Serial NO | Serialnumber 9-10 | — | — | — | — | — | — |
| 28 | Module H | Inverter Module(high) | — | &*5 | — | — | tlx:Inverter model, tl3:Inverter model, storage:Inverter model | — |
| 29 | Module L | Inverter Module(low) | — | &*5 | — | — | — | — |
| 30 | Com Address | Communicate address | W | 1-254 | 1 | — | — | — |
| 31 | Flash Start | Updatefirmware | W | 1 | — | — | — | — |
| 32 | Reset User Info | Reset User Information | W | 0 x 0001 | — | — | — | — |
| 33 | Reset to factory | Resettofactory | W | 0 x 0001 | — | — | — | — |
| 34 | Manufacture r Info 8 | Manufacturer information(high) | — | ASCII | — | — | — | — |
| 35 | Manufacture r Info 7 | Manufacturer information(middle) | — | — | — | — | — | — |
| 36 | Manufacture r Info 6 | Manufacturer information(low) | — | — | — | — | — | — |
| 37 | Manufacture r Info 5 | Manufacturer information(high) | — | — | — | — | — | — |
| 38 | Manufacture r Info 4 | Manufacturer information(middle) | — | — | — | — | — | — |
| 39 | Manufacture r Info 3 | Manufacturer information(low) | — | — | — | — | — | — |
| 40 | Manufacture r Info 2 | Manufacturer information(low) | — | — | — | — | — | — |
| 41 | Manufacture r Info 1 | Manufacturer information(high) | — | — | — | — | — | — |
| 42 | bfailsafe En; | G 100 failsafe | W | Enable:1 Disable:0 | — | English G 100 failsafeset | — | — |
| 43 | DTC | Device Type Code | — | &*6 | — | — | tlx:device type code, tl3:device type code, storage:device type code | — |
| 44 | TP | Inputtrackernumand outputphasenum | — | Eg:0 x 020 3 is two MPPT and 3 ph output | — | — | tlx:number of trackers and phases, tl3:number of trackers and phases, storage:number of trackers and phases | — |
| 45 | Sys Year | Systemtime-year | W | Year offsetis 0 | — | Localtime | — | — |
| 46 | Sys Month | Systemtime-Month | W | — | — | — | — | — |
| 47 | Sys Day | Systemtime-Day | W | — | — | — | — | — |
| 48 | Sys Hour | Systemtime-Hour | W | — | — | — | — | — |
| 49 | Sys Min | Systemtime-Min | W | — | — | — | — | — |
| 50 | Sys Sec | Systemtime-Second | W | — | — | — | — | — |
| 51 | Sys Weekly | System Weekly | W | 0-6 | — | — | — | — |
| 52 | Vaclow | Gridvoltagelowlimit protect | W | 0.1 V | — | — | — | — |
| 53 | Vachigh | Gridvoltagehighlimit protect | W | 0.1 V | — | — | — | — |
| 54 | Faclow | Gridfrequencylow limitprotect | W | 0.01 Hz | — | — | — | — |
| 55 | Fachigh | Gridhigh frequencylimitprotect | W | 0.01 Hz | — | — | — | — |
| 56 | Vaclow 2 | Gridvoltagelowlimit protect 2 | W | 0.1 V | — | — | — | — |
| 57 | Vachigh 2 | Gridvoltagehighlimit protect 2 | W | 0.1 V | — | — | — | — |
| 58 | Faclow 2 | Gridfrequencylow limitprotect 2 | W | 0.01 Hz | — | — | — | — |
| 59 | Fachigh 2 | Gridhighfrequency limitprotect 2 | W | 0.01 Hz | — | — | — | — |
| 60 | Vaclow 3 | Grid voltage low limit protect 3 | W | 0.1 V | — | — | — | — |
| 61 | Vachigh 3 | Grid voltage high limit protect 3 | W | 0.1 V | — | — | — | — |
| 62 | Faclow 3 | Grid frequency low limitprotect 3 | W | 0.01 Hz | — | — | — | — |
| 63 | Fachigh 3 | Grid frequency high limitprotect 3 | W | 0.01 Hz | — | — | — | — |
| 64 | Vaclow C | Gridlowvoltagelimit connectto Grid | W | 0.1 V | — | — | — | — |
| 65 | Vachigh C | Gridhighvoltagelimit connectto Grid | W | 0.1 V | — | — | — | — |
| 66 | Faclow C | Gridlowfrequency | W | 0.01 | — | — | — | — |
| 67 | Fachigh C | Gridhighfrequency limitconnectto Grid | W | 0.01 Hz | — | — | — | — |
| 68 | Vac low 1 time | Grid voltage low limit protecttime 1 | W | Cycle | — | — | — | — |
| 69 | Vac high 1 time | Grid voltage high limit protecttime 1 | W | Cycle | — | — | — | — |
| 70 | Vac low 2 time | Grid voltage low limit protecttime 2 | W | Cycle | — | — | — | — |
| 71 | Vac high 2 time | Grid voltage high limit protecttime 2 | W | Cycle | — | — | — | — |
| 72 | Fac low 1 time | Grid frequency low limitprotecttime 1 | W | Cycle | — | — | — | — |
| 73 | Fac high 1 time | Grid frequency high limitprotecttime 1 | W | Cycle | — | — | tl3:modbus version | — |
| 74 | Fac low 2 time | Grid frequency low limitprotecttime 2 | W | Cycle | — | — | — | — |
| 75 | Fac high 2 time | Grid frequency high limitprotecttime 2 | W | Cycle | — | — | — | — |
| 76 | Vac low 3 time | Grid voltage low limit protecttime 3 | W | Cycle | — | — | — | — |
| 77 | Vac high 3 time | Grid voltage high limit protecttime 3 | W | Cycle | — | — | — | — |
| 78 | Fac low 3 time | Grid frequency low limitprotecttime 3 | W | Cycle | — | — | — | — |
| 79 | Fac high 3 time | Grid frequency high limitprotecttime 3 | W | Cycle | — | — | — | — |
| 80 | U 10 min | Voltprotectionfor 10 min | W | 0.1 V | 1.1 Vn | — | — | — |
| 81 | PV Voltage High Fault | PVVoltage High Fault | W | 0.1 V | — | — | — | — |
| 82 | FWBuild No. 5 | Modelletterversion | — | ASCII | — | — | — | — |
| 83 | FWBuild No. 4 | Modelletterversion | — | ASCII | — | — | — | — |
| 84 | FWBuild No. 3 | DSP 1 FWBuild No. | — | ASCII | — | — | — | — |
| 85 | FWBuild No. 2 | DSP 2/M 0 FWBuild No. | — | ASCII | — | — | — | — |
| 86 | FWBuild No. 1 | CPLD/AFCIFWBuild No. | — | ASCII | — | — | — | — |
| 87 | FWBuild No. | M 3 FWBuild No. | — | ASCII | — | — | — | — |
| 88 | Modbus Vers ion | Modbus Version | — | Eg:207 is V 2.07 Int(16 bits) | — | — | tlx:modbus version, storage:modbus version | — |
| 89 | PFModel | Set PFfunction Model 0:PF=1 1:PFbyset 2:default PFline 3:User PFline 4:Under Excited(Inda) Reactive Power 5:Over Excited(Capa) Reactive Power 6:Q(v)model 7:Direct Controlmode | W | — | — | — | — | — |
| 90 | GPRSIPFlag | Bit 0-3:read:1;Set GPRS IPSuccessed Write:2;Read GPRSIP Successed Bit 4-7:GPRSstatus | W | Bit 0-3:ab out GPRS IPSET Bit 4-7:ab out GRPRS Status | — | — | — | — |
| 91 | Freq Derate S tart | Frequencyderating startpoint | W | 0.01 H Z | — | — | — | — |
| 92 | FLrate | Frequency–loadlimit rate | W | 0-100 10 tim es | — | — | — | — |
| 93 | V 1 S | CEI 021 V 1 SQ(v) | W | V 1 S<V 2 S 0.1 V | — | — | — | — |
| 94 | V 2 S | CEI 021 V 2 SQ(v) | W | 0.1 V | — | — | — | — |
| 95 | V 1 L | CEI 021 V 1 LQ(v) | W | V 1 L<V 1 S 0.1 V | — | — | — | — |
| 96 | V 2 L | CEI 021 V 2 LQ(v) | W | V 2 L<V 1 L 0.1 V | — | — | — | — |
| 97 | Qlockinpow er | Q(v)lockinactive powerof CEI 021 | W | 0-100 Percen t | — | — | — | — |
| 98 | Qlock Outpo wer | Q(v)lock Outactive powerof CEI 021 | W | 0-100 Percen t | — | — | — | — |
| 99 | LIGrid V | Lockingirdvoltof CEI 021 PFline | W | n Vn 0.1 V | — | — | — | — |
| 100 | LOGrid V | Lockoutgirdvoltof CEI 021 PFline | W | n Vn 0.1 V | — | — | — | — |
| 101 | PFAdj 1 | PFadjustvalue 1 | — | 4096 is 1 | — | — | — | — |
| 102 | PFAdj 2 | PFadjustvalue 2 | — | 4096 is 1 | — | — | — | — |
| 103 | PFAdj 3 | PFadjustvalue 3 | — | 4096 is 1 | — | — | — | — |
| 104 | PFAdj 4 | PFadjustvalue 4 | — | 4096 is 1 | — | — | — | — |
| 105 | PFAdj 5 | PFadjustvalue 5 | — | 4096 is 1 | — | — | — | — |
| 106 | PFAdj 6 | PFadjustvalue 6 | — | 4096 is 1 | — | — | — | — |
| 107 | QVRPDelay Ti me EE | QV Reactive Power delaytime | W | 0-30 1 S | 3 S | — | — | — |
| 108 | Over FDerat D elay Time EE | Overfrequency derati ngdelaytime | W | 0-20 50 ms | 0 | — | — | — |
| 109 | Qpercent Ma x | Qmaxfor Q(V)curve | W | 0-1000 0.1% | — | — | — | — |
| 110 | PFLine P 1_LP | PFlimitlinepoint 1 loadpercent | W | 0-255 percen t | — | 255 meansnothispoint | — | — |
| 111 | PFLine P 1_PF | PFlimitlinepoint 1 powerfactor | W | 0-20000 | — | — | — | — |
| 112 | PFLine P 2_LP | PFlimitlinepoint 2 loadpercent | W | 0-255 percen t | — | 255 meansnothispoint | — | — |
| 113 | PFLine P 2_PF | PFlimitlinepoint 2 powerfactor | W | 0-20000 | — | — | — | — |
| 114 | PFLine P 3_LP | PFlimitlinepoint 3 loadpercent | W | 0-255 percen t | — | 255 meansnothispoint | — | — |
| 115 | PFLine P 3_PF | PFlimitlinepoint 3 powerfactor | W | 0-20000 | — | — | — | — |
| 116 | PFLine P 4_LP | PFlimitlinepoint 4 loadpercent | W | 0-255 percen t | — | 255 meansnothispoint | — | — |
| 117 | PFLine P 4_PF | PFlimitlinepoint 4 powerfactor | W | 0-20000 | — | — | — | — |
| 118 | Module 4 | Inverter Module(4) | — | &*11 | — | Sxx Bxx | — | — |
| 119 | Module 3 | Inverter Module(3) | — | &*11 | — | Dxx Txx | — | — |
| 120 | Module 2 | Inverter Module(2) | — | &*11 | — | Pxx Uxx | — | — |
| 121 | Module 1 | Inverter Module(1) | — | &*11 | — | Mxxxx Power | — | — |
| 122 | Export Limit_ En/dis | Export Limit_En/dis | R/W | 1/0 | — | Export Limitenable, 0:Disableexport Limit; 1:Enable 485 export Limit; 2:Enable 232 export Limit; 3:Enable CTexport Limit; | — | — |
| 123 | Export Limit P ower Rate | Export Limit Power Rate | R/W | -1000~+1 000 0.1% | — | Export Limit Power Rate | — | — |
| 124 | Traker Model | Traker Model | W | 0,1,2 | — | 0:Independent 1:DCSource 2:Parallel | — | — |

## TL-X/TL-XH Holding Registers (3000–3124)
Additional holding registers for TL-X/TL-XH hybrids (MIN series).

**Applies to:** TL-X/TL-XH/TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | Export Limit Fa iled Power Rat e | Thepowerratewhen export Limitfailed | R/W | 0.1% | — | Thepowerrate whenexport Limit failed | — | — |
| 3001 | New Serial NO | Serialnumber 1-2 | R/W | ASCII | — | Thenewmodel usesthefollowing registerstorecord theserialnumber; The representationis thesameasthe original:one registerholdstwo charactersandthe newserialnumber is 30 characters. | — | — |
| 3002 | New Serial NO | Serialnumber 3-4 | R/W | ASCII | — | — | — | — |
| 3003 | New Serial NO | Serialnumber 5-6 | R/W | ASCII | — | — | — | — |
| 3004 | New Serial NO | Serialnumber 7-8 | R/W | ASCII | — | — | — | — |
| 3005 | New Serial NO | Serialnumber 9-10 | R/W | ASCII | — | — | — | — |
| 3006 | New Serial NO | Serialnumber 11-12 | R/W | ASCII | — | — | — | — |
| 3007 | New Serial NO | Serialnumber 13-14 | R/W | ASCII | — | — | — | — |
| 3008 | New Serial NO | Serialnumber 15-16 | R/W | ASCII | — | — | — | — |
| 3009 | New Serial NO | Serialnumber 17-18 | R/W | ASCII | — | — | — | — |
| 3010 | New Serial NO | Serialnumber 19-20 | R/W | ASCII | — | — | — | — |
| 3011 | New Serial NO | Serialnumber 21-22 | R/W | ASCII | — | — | — | — |
| 3012 | New Serial NO | Serialnumber 23-24 | R/W | ASCII | — | — | — | — |
| 3013 | New Serial NO | Serialnumber 25-26 | R/W | ASCII | — | — | — | — |
| 3014 | New Serial NO | Serialnumber 27-28 | R/W | ASCII | — | — | — | — |
| 3015 | New Serial NO | Serialnumber 29-30 | R/W | ASCII | — | — | — | — |
| 3016 | Dry Contact Fu nc En | Dry Contactfunctionenable | R/W | 0:Disable 1:Enable | — | Dry Contact functionenable | — | — |
| 3017 | Dry Contact On Rate | The power rate of drycontactturnon | R/W | 0~1000 0.1% | — | The power rate of drycontactturnon | — | — |
| 3018 | b Work Mode | Work Mode----0:default,1: System Retrofit 2: Multi-Parallel | R/W | 0, 1, 2 | — | MIN 2.5~6 KTL-XH/ XADouble CT special | — | — |
| 3019 | Dry Contact Of f Rate | Dry Contact Off Rate | Dry contact closure power | R/W 0~100 0 | 0.1% | Drycontact closurepowerpe rcentage | — | — |
| 3020 | Box Ctrl Inv Ord er | Box Ctrl Inv Order | Off-net box control instruct ion | R/W | — | — | — | — |
| 3021 | Exter Comm Of f Grid En | External communication setting manual off-network enable | R/W | — | — | 0 x 00: Disable; (default) 0 x 01:Enable; | — | — |
| 3022 | uw Bdc Stop W ork Of Bus Volt | Bdc Stop Work Of Bus Volt | R | — | — | — | — | — |
| 3023 | b Grid Type | Grid Type---0:Single Phase 1:Three Phase 2:Split Phase | R/W | 0, 1, 2 | — | MIN 2.5~6 KTL-XH/ XADouble CT special | — | — |
| 3024 | Floatcharge currentlimit | Whenchargecurrent batteryneedislowerthan | R/W | 0.1 A | 600 | CCcurrent | — | — |
| 3025 | Vbat Warning | "Battery-low"warning setupvoltage | R/W | 0.1 V | 4800 | Leadacidbattery LVvoltage | — | — |
| 3026 | Vbatlow Warn Clr | "Battery-low"warning clearvoltage | R/W | 0.1 V | — | Clearbatterylow voltageerror voltagepoint Load Percent(only lead-Acid): 45.5 V(Load< 20%); 48.0 V(20%<=Load <=50%); 49.0 V(Load> 50%); | — | — |
| 3027 | Vbatstopfordi scharge | Batterycutoffvoltage | R/W | 0.1 V | — | Shouldstop dischargewhen lowerthanthis voltage(only lead-Acid): 46.0 V(Load< 20%); 44.8 V(20%<=Load <=50%); 44.2 V(Load> 50%); | — | — |
| 3028 | Vbatstopfor charge | Batteryoverchargevoltage | R/W | 0.01 V | 5800 | Shouldstop chargewhen higherthanthis voltage | — | — |
| 3029 | Vbatstartfor discharge | Batterystartdischarge voltage | R/W | 0.01 V | 4800 | Shouldnot dischargewhen lowerthanthis voltage | — | — |
| 3030 | Vbatconstant charge | Batteryconstantcharge voltage | R/W | 0.01 V | 5800 | CVvoltage(acid) canchargewhen lowerthanthis voltage | — | — |
| 3031 | Battemp lowerlimitd | Batterytemperaturelower limitfordischarge | R/W | 0.1℃ | 1170 | 0-200:0-20℃ 1000-1400: -40-0℃ | — | — |
| 3032 | Battemp upperlimitd | Batterytemperatureupper limitfordischarge | R/W | 0.1℃ | 420 | — | — | — |
| 3033 | Battemp lowerlimitc | Batterytemperaturelower limitforcharge | R/W | 0.1℃ | 30 | Battery temperaturelower limit 0-200:0-20℃ 1000-1400: -40-0℃ | — | — |
| 3034 | Battemp upperlimitc | Batterytemperatureupper limitforcharge | R/W | 0.1℃ | 370 | Battery temperature upperlimit | — | — |
| 3035 | uw Under Fre D ischarge Dely T ime | Under Fre Delay Time | R/W | 50 ms | — | Under Fre Delay Time | — | — |
| 3036 | Grid First Disch arge Power Rat e | Discharge Power Rate when Grid First | — | — | 1-255 | — | — | — |
| 3037 | Grid First Stop S OC | Stop Dischargesocwhen Grid First | — | — | 1-100 | — | — | — |
| 3038 | Time 1(xh) | Period 1:[Start Time~End Time],[Charge/Discharge], [Disable/Enable] 3038 enable,chargeand discharge,starttime,end time 3039 | R/W | — | — | Bit 0~7:minutes; Bit 8~12:hour; Bit 13~14, 0:loadpriority; 1:batterypriority; 2:Gridpriority; Bit 15, 0:prohibited;1: enabled; | — | — |
| 3039 | — | — | R/W | — | — | Bit 0~7:minutes; Bit 8~12:hour; Bit 13~15:reserved | — | — |
| 3040 | Time 2(xh) | Timeperiod 2:[starttime~ endtime],[charge/ discharge],[disable/ enable] 3040 enable,chargeand discharge,starttime,3041 endtime | R/W | — | — | Bit 0~7:minutes; Bit 8~12:hour; Bit 13~14, 0:loadpriority; 1:batterypriority; 2:Gridpriority; Bit 15, 0:prohibited;1: | — | — |
| 3041 | — | — | R/W | — | — | Bit 0~7:minutes; Bit 8~12:hour; Bit 13~15:reserved | — | — |
| 3042 | Time 3(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3043 | — | — | R/W | — | — | With Time 1 | — | — |
| 3044 | Time 4(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3045 | — | — | R/W | — | — | With Time 1 | — | — |
| 3046 | 预留 | — | — | — | — | — | — | — |
| 3047 | Bat First Power Rate | Charge Power Ratewhen Bat First | — | — | 1-100 | — | — | — |
| 3048 | w Bat Firststop SOC | Stop Chargesocwhen Bat First | — | — | 1-100 | — | — | — |
| 3049 | Ac Charge Ena ble | Ac Charge Enable | — | — | — | Enable:1 Disable:0 | — | — |
| 3050 | Time 5(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3051 | — | — | R/W | — | — | With Time 1 | — | — |
| 3052 | Time 6(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3053 | — | — | R/W | — | — | With Time 1 | — | — |
| 3054 | Time 7(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3055 | — | — | R/W | — | — | With Time 1 | — | — |
| 3056 | Time 8(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3057 | — | — | R/W | — | — | With Time 1 | — | — |
| 3058 | Time 9(xh) | With Time 1 | R/W | — | — | With Time 1 | — | — |
| 3059 | — | — | R/W | — | — | With Time 1 | — | — |
| 3060~ 3069 | Reserved | — | — | — | — | — | — | — |
| 3070 | Battery Type | Batterytypechooseof buck-boostinput | R/W | — | — | Batterytype 0:Lithium 1:Lead-acid 2:other | — | — |
| 3071 | Bat Mdl Seria/ Paral Num | Bat Mdl Seria/Paral Num | R/W | — | — | Bat Mdl Seria/Paral Num; SPH 4-11 Kused Theupper 8 bits indicatethe numberofseries segments; Thelower 8 bits indicatethe numberofparallel sections; | — | — |
| 3072 | Reserved | — | — | — | — | — | — | — |
| 3073 | Reserved | — | — | — | — | — | — | — |
| 3074 | Reserved | — | — | — | — | — | — | — |
| 3075 | Reserved | — | — | — | — | — | — | — |
| 3076 | Reserved | — | — | — | — | — | — | — |
| 3077 | Reserved | — | — | — | — | — | — | — |
| 3078 | Reserved | — | — | — | — | — | — | — |
| 3079 | Ups Fun En | Upsfunctionenableor disable | R/W | — | 0 | 0:disable 1:enable | — | — |
| 3080 | UPSVolt Set | UPSoutputvoltage | R/W | — | 0 | 0:230 V 1:208 V 2:240 V | — | — |
| 3081 | UPSFreq Set | UPSoutputfrequency | R/W | — | 0 | 0:50 Hz 1:60 Hz | — | — |
| 3082 | b Load First Sto p Soc Set | Stop Soc When Load First | R/W | — | 13-100 | ratio | — | — |
| 3083 | Reserved | — | — | — | — | — | — | — |
| 3084 | Reserved | — | — | — | — | — | — | — |
| 3085 | Com Address | Communicationaddr | R/W | — | 1 | 1:Communication addr=1 1~254: Communication addr=1~254 | — | — |
| 3086 | Baud Rate | Communication Baud Rate | R/W | — | 0 | 0:9600 bps 1:38400 bps | — | — |
| 3087 | Serial NO.1 | Serial Number 1-2 | R/W | ASCII | — | Forbattery | — | — |
| 3088 | Serial NO.2 | Serial Number 3-4 | R/W | ASCII | — | — | — | — |
| 3089 | Serial NO.3 | Serial Number 5-6 | R/W | ASCII | — | — | — | — |
| 3090 | Serial NO.4 | Serial Number 7-8 | R/W | ASCII | — | — | — | — |
| 3091 | Serial No.5 | Serial Number 9-10 | R/W | ASCII | — | — | — | — |
| 3092 | Serial No.6 | Serial Number 11-12 | R/W | ASCII | — | — | — | — |
| 3093 | Serial No.7 | Serial Number 13-14 | R/W | ASCII | — | — | — | — |
| 3094 | Serial No.8 | Serial Number 15-16 | R/W | ASCII | — | — | — | — |
| 3095 | Bdc Reset Cmd | BDCResetcommand | R/W | — | — | 0:Invaliddata 1:Resetsetting parameters 2:Resetcorrection parameter 3:Clearhistorical power | — | — |
| 3096 | ARKM 3 Code | BDCMonitoringsoftware code | R | ASCII | — | ZEBA | — | — |
| 3097 | — | — | — | — | — | — | — | — |
| 3098 | DTC | DTC | R | — | — | — | — | — |
| 3099 | FWCode | DSPsoftwarecode | R | ASCII | — | — | — | — |
| 3100 | — | — | — | — | — | — | — | — |
| 3101 | Processor 1 FWVision | DSPSoftware Version | R | ASCII | — | — | — | — |
| 3102 | Bus Volt Ref | Minimum BUSvoltagefor charginganddischarging batteries | R | — | — | — | — | — |
| 3103 | ARKM 3 Ver | BDCmonitoringsoftware version | R | — | — | — | — | — |
| 3104 | BMS_MCUVer sion | BMS hardware version information | R | 1 | — | — | — | — |
| 3105 | BMS_FW | BMSsoftwareversion information | R | 1 | — | — | — | — |
| 3106 | BMS_Info | BMSManufacturer Name | R | 1 | — | — | — | — |
| 3107 | BMSComm Ty pe | BMSComm Type | R | 1 | — | BMSCommunicati oninterfacetype: 0:RS 485; 1:CAN; | — | — |
| 3108 | Module 4 | BDCmodel(4) | R/W | &*11 | — | Sxx Bxx | — | — |
| 3109 | Module 3 | BDCmodel(3) | R/W | &*11 | — | Dxx Txx | — | — |
| 3110 | Module 2 | BDCmodel(2) | R/W | &*11 | — | Pxx Uxx | — | — |
| 3111 | Module 1 | BDCmodel(1) | R/W | &*11 | — | Mxxxx | — | — |
| 3112 | Reserved | — | — | — | — | — | — | — |
| 3113 | un Protocol Ve r | BDCProtocol Ver | R | 1 | — | Bit 8-bit 15 The majorversion numberranges from 0-256.In principle,itcannot bechanged Bit 0-bit 7 Minor versionnumber [0-256].Ifthe protocolis changed,youneed toupdatethis version No. | — | — |
| 3114 | uw Certificatio n Ver | BDCCertification Ver | R | 1 | — | — | — | — |
| 3115 ~ 3124 | Reserved | — | — | — | — | — | — | — |

## TL-XH US Holding Registers (3125–3249)
US-specific time schedule and dry-contact configuration registers.

**Applies to:** TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3125 | Time Month 1 | Usewith Time 1-9(us) ,Addmonthtime | R/W | — | — | bit 0~3:month_L; bit 4~7:month_H bit 8, 0:disable 1:enable Bit 9~15:reserve | — | — |
| 3126 | Time Month 2 | Usewith Time 10-18(us) ,Addmonthtime | R/W | — | — | With Time Month 1 | — | — |
| 3127 | Time Month 3 | Usewith Time 19-27(us) ,Addmonthtime | R/W | — | — | With Time Month 1 | — | — |
| 3128 | Time Month 4 | Usewith Time 28-36(us) ,Addmonthtime | R/W | — | — | With Time Month 1 | — | — |
| 3129 | Time 1(us) | time 1:[starttime~endtime] | R/W | [Charge/ discharg e/counte r | — | bit 0~6:min; bit 7~11:hour; bit 12~14, 0:loadfirst; | — | — |
| 3130 | — | — | R/W | — | — | bit 0~6:min; bit 7~11:hour; bit 12-13, 0:Weekday 1:Weekend 2:Wee K bit 14~15:reserve | — | — |
| 3131-3 132 | Time 2(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3133-3 134 | Time 3(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3135-3 136 | Time 4(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3137-3 138 | Time 5(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3139-3 140 | Time 6(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3141-3 142 | Time 7(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3143-3 144 | Time 8(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3145-3 146 | Time 9(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3147-3 148 | Time 10(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3149-3 150 | Time 11(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3151-3 152 | Time 12(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3153-3 154 | Time 13(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3155-3 156 | Time 14(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3157-3 158 | Time 15(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3159-3 160 | Time 16(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3161-3 162 | Time 17(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3163-3 164 | Time 18(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3165-3 166 | Time 19(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3167-3 168 | Time 20(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3169-3 170 | Time 21(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3171-3 172 | Time 22(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3173-3 174 | Time 23(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3175-3 176 | Time 24(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3177-3 178 | Time 25(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3179-3 180 | Time 26(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3181-3 182 | Time 27(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3183-3 184 | Time 28(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3185-3 186 | Time 29(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3187-3 188 | Time 30(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3189-3 190 | Time 31(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3191-3 192 | Time 32(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3193-3 194 | Time 33(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3195-3 196 | Time 34(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3197-3 198 | Time 35(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3199-3 200 | Time 36(us) | Sameasabove | R/W | — | — | Sameas Time 1 (us) | — | — |
| 3201 | Special Day 1 | Special Day 1(month,Day) | R/W | — | — | bit 0~7:day; bit 8~14:month bit 15, 0:disable 1: enable | — | — |
| 3202 | Special Day 1_ Time 1 | Starttime | R/W | — | — | bit 0~6:min; bit 7~11:hour; bit 12~14, 0:loadfirst; 1:batfirst; 2:gridfirst; 3:anti-reflux bit 15, 0:disable; 1:enable; | — | — |
| 3203 | — | endtime | R/W | — | — | bit 0~6:min; bit 7~11:hour; bit 12~15:reserve | — | — |
| 3204-3 205 | Special Day 1_ Time 2 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3206-3 207 | Special Day 1_ Time 3 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3208-3 209 | Special Day 1_ Time 4 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3210-3 211 | Special Day 1_ Time 5 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3212-3 213 | Special Day 1_ Time 6 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3214-3 215 | Special Day 1_ Time 7 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3216-3 217 | Special Day 1_ Time 8 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3218-3 219 | Special Day 1_ Time 9 | Sameasabove | R/W | — | — | Sameas Special Day 1_Time 1 | — | — |
| 3220 | Special Day 2 | Special Day 2(month,Day) | R/W | — | — | bit 0~7:day; bit 8~14:month bit 15, 0:disable 1:enable | — | — |
| 3221 | Special Day 2_ Time 1 | Starttime | R/W | — | — | bit 0~6:min; bit 7~11:hour; bit 12~14, 0:loadfirst; 1:batfirst; 2:gridfirst; 3:anti-reflux bit 15, 0:disable; 1:enable; | — | — |
| 3222 | — | endtime | R/W | — | — | bit 0~6:min; bit 7~11:hour; bit 12~15:reserve | — | — |
| 3223-3 224 | Special Day 2_ Time 2 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3225-3 226 | Special Day 2_ Time 3 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3227-3 228 | Special Day 2_ Time 4 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3229-3 230 | Special Day 2_ Time 5 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3231-3 232 | Special Day 2_ Time 6 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3233-3 234 | Special Day 2_ Time 7 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3235-3 236 | Special Day 2_ Time 8 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |
| 3237-3 238 | Special Day 2_ Time 9 | Sameasabove | R/W | — | — | Sameas Special Day 2_Time 1 | — | — |

## TL3/MAX/MID/MAC Holding Registers (125–249)
Three-phase inverter specific holding registers.

**Applies to:** TL3-X/MAX/MID/MAC

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 125 | INVType-1 | Invertertype-1 | R | ASCII | — | Reserved | — | — |
| 126 | INVType-2 | Invertertype-2 | R | ASCII | — | — | — | — |
| 127 | INVType-3 | Invertertype-3 | R | ASCII | — | — | — | — |
| 128 | INVType-4 | Invertertype-4 | R | ASCII | — | — | — | — |
| 129 | INVType-5 | Invertertype-5 | R | ASCII | — | — | — | — |
| 130 | INVType-6 | Invertertype-6 | R | ASCII | — | — | — | — |
| 131 | INVType-7 | Invertertype-7 | R | ASCII | — | — | — | — |
| 132 | INVType-8 | Invertertype-8 | R | ASCII | — | — | — | — |
| 133 | BLVersion 1 | Bootloaderversion 1 | R | — | — | Reserved | — | — |
| 134 | BLVersion 2 | Bootloaderversion 2 | R | — | — | Reserved | — | — |
| 135 | BLVersion 3 | Bootloaderversion 3 | R | — | — | Reserved | — | — |
| 136 | BLVersion 4 | Bootloaderversion 4 | R | — | — | Reserved | — | — |
| 137 | Reactive P Value H | Reactive Power H | R/W | 0.1 var | — | — | — | — |
| 138 | Reactive P Value L | Reactive Power L | R/W | 0.1 var | — | — | — | — |
| 139 | Reactive Out put Priority E nable | Reactive Output Priority Enable | R/W | 0/1 | — | 0:disable 1:enable | — | — |
| 140 | Reactive P Value(Ratio) | Reactive Power Ratio | R/W | 0.1 | — | — | — | — |
| 141 | Svg Function Enable | Svgenableonnight | R/W | 0/1 | — | 0:disable 1:enable | — | — |
| 142 | uw Under FU pload Point | Under FUpload Point | R/W | 0.01 H Z | — | — | — | — |
| 143 | uw OFDerate Recover Poin t | OFDerate Recover Point | R/W | 0.01 H Z | — | — | — | — |
| 144 | uw OFDerate Recover Dela y Time | OFDerate Recover Delay Time | R/W | 0-30000 50 ms | — | — | — | — |
| 145 | Zero Current Enable | Zero Current Enable | R/W | 0-1 | — | — | — | — |
| 146 | uw Zero Curre nt Staticlow V olt | Zero Current Staticlow Volt | R/W | 46-230 V 0.1 V | 115 V | — | — | — |
| 147 | uw Zero Curre nt Static High Volt | Zero Current Static High Volt | R/W | 230-276 V 0.1 V | 276 V | — | — | — |
| 148 | uw HVolt Der | HVolt Derate High Point | R/W | 0-1000 V 0.1 V | — | — | — | — |
| 149 | uw HVolt Der ate Low Point | HVolt Derate Low Point | R/W | 0-1000 V 0.1 V | — | — | — | — |
| 150 | uw QVPower Stable Time | QVPower Stable Time | R/W | 0-60 S 0.1 S | — | — | — | — |
| 151 | uw Under FU pload Stop Po int | Under F Upload Stop Point | R/W | 0.01 H Z | — | — | — | — |
| 152 | f Under Freq P oint | Underfrequency load startpoint | R/W | 46.00-50. 00 0.01 Hz | 49.80 | CEI | — | — |
| 153 | f Under Freq E nd Point | Underfrequency down loadendpoint | R/W | 46.00-50. 00 0.01 Hz | 49.10 | CEI | — | — |
| 154 | f Over Freq Po int | Over frequency loading startpoint | R/W | 50.00-52. 00 0.01 Hz | 50.20 | CEI | — | — |
| 155 | f Over Freq En d Point | Over frequency loading endpoint | R/W | 50.00-52. 00 0.01 Hz | 51.50 | CEI | — | — |
| 156 | f Under Volt P oint | Undervoltage load sheddingstartpoint | R/W | 160-300 0.1 V | 220.0 | CEI | — | — |
| 157 | f Under Volt E nd Point | Undervoltage derating endpoint | R/W | 160-300 0.1 V | 207.0 | CEI | — | — |
| 158 | f Over Volt Poi nt | Overvoltage loading startpoint | R/W | 160-300 0.1 V | 230.0 | CEI | — | — |
| 159 | f Over Volt En d Point | Overvoltage loading endpoint | R/W | 160-300 0.1 V | 245.0 | CEI | — | — |
| 160 | uw Nominal Grid Volt | Nominal Grid Volt Select | R/W | 0~3 | — | UL | — | — |
| 161 | uw Grid Watt Delay | Grid Watt Delay Time | R/W | 0~3000 20 ms | — | UL | — | — |
| 162 | uw Reconnec t Start Slope | Reconnect Start Slope | R/W | 1~1000 0.1 | — | UL | — | — |
| 163 | uw LFRTEE | LFRT 1 Freq | R/W | 5500~650 0 0.01 Hz | — | UL | — | — |
| 164 | uw LFRTTime EE | LFRT 1 Time | R/W | 20 ms | — | UL | — | — |
| 165 | uw LFRT 2 EE | LFRT 2 Freq | R/W | 5500~650 0 0.01 Hz | — | UL | — | — |
| 166 | uw LFRTTime 2 EE | LFRT 2 Time | R/W | 20 ms | — | UL | — | — |
| 167 | uw HFRTEE | HFRT 1 Freq | R/W | 5500~650 0 0.01 Hz | — | UL | — | — |
| 168 | uw HFRTTim e EE | HFRT 1 Time | R/W | 20 ms | — | UL | — | — |
| 169 | uw HFRT 2 EE | HFRT 2 Freq | R/W | 5500~650 0 0.01 Hz | — | UL | — | — |
| 170 | uw HFRTTim e 2 EE | HFRT 2 Time | R/W | 20 ms | — | UL | — | — |
| 171 | uw HVRTEE | HVRT 1 Volt | R/W | 0.001 Un | — | UL | — | — |
| 172 | uw HVRTTim e EE | HVRT 1 Time | R/W | 20 ms | — | UL | — | — |
| 173 | uw HVRT 2 EE | HVRT 2 Volt | R/W | 0.001 Un | — | UL | — | — |
| 174 | uw HVRTTim e 2 EE | HVRT 2 Time | R/W | 0.001 Un | — | UL | — | — |
| 175 | uw Under FU pload Delay Ti me | Under F Upload Delay Time | R/W | 0-2 s 50 ms | 0 s | 50549 | — | — |
| 176 | uw Under FU pload Rate EE | Under FUpload Rate | R/W | — | — | 50549 | — | — |
| 177 | uw Grid Resta rt_H_Freq | Grid Restart High Freq | R/W | 0.01 Hz | — | 50549 | — | — |
| 178 | Over FDerat R esponse Tim e | Over FDerat Response Time | W/R | 0-500 | — | — | — | — |
| 179 | Under FUplo ad Response Time | Under FUpload Response Time | W/R | 0-500 | — | — | — | — |
| 180 | Meter Link | Whether to elect the meter | R/W | — | — | 0:Missed,1:Received | — | — |
| 181 | OPTNumber | Number of connection optimizers | R/W | 0-64 | — | Thetotalnumberofoptimizers connectedtotheinverter | — | — |
| 182 | OPT Config OK Flag | Optimizer configuration completionflag | R/W | — | — | 0 x 00:Notconfiguredsuccess 0 x 01:Configurationiscomplete | — | — |
| 183 | Pv Str Scan | String Num | R/W | 0, 8, 16, 32 | — | 0:Notsupport Other:Pv String Num | — | — |
| 184 | BDCLink Num | BDCparallel Num | R/W | — | — | Thenumberof BDCs | — | — |
| 185 | Pack Num | Numberofbattery | R | — | — | Totalnumberofbattery | — | — |
| 186 | Reserved | — | — | — | — | — | — | — |
| 187 | VPP function enable status | VPPfunctionenable | R | — | — | 0:Disable | — | — |
| 188 | data Log Connect Serverstatus | data Log Connect | — | — | — | 0:connectionsucceeded | — | — |
| 200 | Reserved | — | — | — | — | Reserved | — | — |
| 201 | PID Working Model | PIDOperatingmode | W | 0: automati c 1: continuo us 2:All night | — | — | — | — |
| 202 | PID On/Off Ctrl | PID Breakcontrol | W | 0:On 1:Off | — | — | — | — |
| 203 | PID Volt Option | PID Output voltage option | W | 300~1000 V | — | — | — | — |
| 209 | New Serial NO | Serialnumber 1-2 | — | ASCII | — | — | — | — |
| 210 | New Serial NO | Serialnumber 3-4 | — | ASCII | — | — | — | — |
| 211 | New Serial NO | Serialnumber 5-6 | — | ASCII | — | — | — | — |
| 212 | New Serial NO | Serialnumber 7-8 | — | ASCII | — | — | — | — |
| 213 | New Serial NO | Serialnumber 9-10 | — | ASCII | — | — | — | — |
| 214 | New Serial NO | Serialnumber 11-12 | — | ASCII | — | — | — | — |
| 215 | New Serial NO | Serialnumber 13-14 | — | ASCII | — | — | — | — |
| 216 | New Serial NO | Serialnumber 15-16 | — | ASCII | — | — | — | — |
| 217 | New Serial NO | Serialnumber 17-18 | — | ASCII | — | — | — | — |
| 218 | New Serial NO | Serialnumber 19-20 | — | ASCII | — | — | — | — |
| 219 | New Serial NO | Serialnumber 21-22 | — | ASCII | — | — | — | — |
| 220 | New Serial NO | Serialnumber 23-24 | — | ASCII | — | — | — | — |
| 221 | New Serial NO | Serialnumber 25-26 | — | ASCII | — | — | — | — |
| 222 | New Serial NO | Serialnumber 27-28 | — | ASCII | — | — | — | — |
| 223 | New Serial NO | Serialnumber 29-30 | — | ASCII | — | — | — | — |
| 229 | Energy Adjus t | Powergeneration incrementalcalibration coefficient | W/R | 0.1% | — | 1-1000,(Percentratio) | — | — |
| 230~249forgrowattdebugsetting | — | — | — | — | — | — | — | — |
| 230 | Island Disabl e | Island Disableornot. 1:disable 0:Enable | W | 0,1 | 0 | — | — | — |
| 231 | Fan Check | Start Fan Check | W | 1 | — | — | — | — |
| 232 | Enable NLine | Enable NLineofgrid | W | 1 | 0 | — | — | — |
| 233 | w Check Hard ware | w Check Hardware Bit 0:GFCIBreak; Bit 1:SPSDamage Bit 8:Eeprom Read Warni ng Bit 9:EEWrite Warning …… | — | — | — | — | — | — |
| 234 | w Check Hard ware 2 | — | — | — | — | — | — | — |
| 235 | ub NTo GNDD etect | Dis/enable N to GND detectfunction | W | 1:enable 0:disable | 1 | — | — | — |
| 236 | Non Std Vac E nable | Enable/Disable Nonstandard Gridvoltagerange | W | 0-2 | 0 | — | — | — |
| 237 | uw Enable Sp ec Set | Disablse/enable appointedspecsetting | W | 1:enable 0:disable Binary | 0 x 000 0 | — | — | — |
| 238 | Fast MPPT enable | About Fastmppt | — | 0,1,2 | 0 | Reserved | — | — |
| 239 | / | / | / | / | / | Reserved | — | — |
| 240 | Check Step | — | W | — | — | — | — | — |
| 241 | INV-Lng | Inverter Longitude | W | — | — | Longitude | — | — |
| 242 | INV-Lat | Inverter Latitude | W | — | — | Latitude | — | — |

## Storage Holding Registers (1000–1124)
Storage (MIX/SPA/SPH) battery configuration holding registers.

**Applies to:** Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000. | — | Float charge current limit i | Whenchargecurrent batteryneedislower thanthisvalue,enter ntofloatcharge | W | 0.1 A | — | — | — |
| 1001. | — | PF CMD memory state | Set the following 19-22 CMD will be memory ornot(1/0), if not, these settings aretheinitia value. | W l 0 or 1, | — | — | — | — |
| 1002. | — | Vbat Start F or Discharg e | LVVbat | R/W | 0.1 V | — | — | — |
| 1003. | — | Vbatlow Wa rn Clr l | LoadPercent(only ead-Acid): 45.5V <20% 48.0V 20%~50% 49.0V >50 | W | 0.1 V | — | — | — |
| 1004. | — | Vbatstopfo rdischarge | Should stop discharge when lower than this | W | 0.01 V | — | — | — |
| 1005. | Vbat stop forcharge | Shouldstopcharge whenhigherthanthis voltage | W | 0.01 V | 5800 | — | — | — |
| 1006. | Vbat start for discharge | Should not discharge when lower than this voltage | W | 0.01 V | 4800 | — | — | — |
| 1007. | Vbat constant charge | canchargewhenlower thanthisvoltage | W | 0.01 V | 5800 | CVvoltage(acid) | — | — |
| 1008. | EESys Info.S ys Set En | Bit 0:Resved; Bit 1:Resved; Bit 2:Resved; Bit 3:Resved; Bit 4:Resved; Bit 5:b Discharge En; Bit 6:Force Dischr En; Bit 7:Charge En; Bit 8:b Force Chr En; Bit 9:b Back Up En; Bit 10:b Inv Limit Load E; Bit 11:b Sp Limit Load En; Bit 12:b ACCharge En; Bit 13:b PVLoad Limit En; Bit 14,15:Un Used; | W | — | — | System Enable | — | — |
| 1009. | Battemp lower limit d | Batterytemperature lowerlimitfordischarge | W | 0-200:0-2 0℃ 1000-140 0:-40-0℃ 0.1℃ | 1170 | — | — | — |
| 1010. | Bat temp upper limit d | Batterytemperature upperlimitfordischarge | W | 200-1000 0.1℃ | 420 | — | — | — |
| 1011. | Bat temp lower limit c | Batterytemperature lowerlimitforcharge | W | 0-200:0-2 0℃ 1000-140 0:-40-0℃ 0.1℃ | 30 | Lowertemperaturelimit | — | — |
| 1012. | Bat temp upper limit c | Batterytemperature upperlimitforcharge | W | 200-1000 0.1℃ | 370 | Uppertemperaturelimit | — | — |
| 1013. | uw Under Fr e Discharge Dely Time | Under Fre Delay Time | s | 0-20 50 ms | — | Under Fre Delay Time | — | — |
| 1014. | Bat Mdl Seri al Num | Batteryserialnumber | W | 00:00 | — | SPH 4-11 Kused | — | — |
| 1015. | Bat Mdl Para ll Num | Batteryparallelsection | W | 00:00 | — | SPH 4-11 Kused | — | — |
| 1016. | DRMS_EN | / | / | / / | / | 0:disable 1:enable | — | — |
| 1017. | Bat First Start Time 4 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1018. | Bat First Stop Time 4 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1019. | Bat First on/off Switch 4 | Enable:1 Disable:0 | — | 0 or 1 | — | Batterypriorityenable 1 | — | — |
| 1020. | Bat First Start Time 5 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1021. | Bat First Stop Time 5 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1022. | Bat First on/off Switch 5 | Enable:1 Disable:0 | — | 0 or 1 | — | Batterypriorityenable 1 | — | — |
| 1023. | Bat First Start Time 6 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1024. | Bat First Stop Time 6 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1025. | Bat First on/off Switch 6 | Enable:1 Disable:0 | — | 0 or 1 | — | Batterypriorityenable 1 | — | — |
| 1026. | Grid First Start Time | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1027. | Grid First Stop Time 4 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1028. | Grid First Stop Switch 4 | Enable:1 Disable:0 | — | 0 or 1 | — | Gridpriorityenable | — | — |
| 1029. | Grid First Start Time 5 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1030. | Grid First Stop Time 5 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1031. | Grid First Stop Switch 5 | Enable:1 Disable:0 | — | 0 or 1 | — | Gridpriorityenable | — | — |
| 1032. | Grid First Start Time 6 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1033. | Grid First Stop Time 6 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1034. | Grid First Stop Switch 6 | Enable:1 Disable:0 | — | 0 or 1 | — | Gridpriorityenable | — | — |
| 1035. | Bat First Start Time 4 | Higheight:hours Loweight:minutes | — | 0-23 0-59 | — | — | — | — |
| 1036. | / | / | / | / / | / | Reserve | — | — |
| 1037. | b CTMode | Usethe CTModeto Choose RFCT\Cable CT\METER | W | 2:METER 1:c Wirele ss CT 0:c Wired C T | 0 | — | — | — |
| 1038. | CTAdjust | CTAdjustenable | W | 0:disable 1:enable | 0 | — | — | — |
| 1039. | / | / | / | / / | / | Reserve | — | — |
| 1040. | / | / | — | / | / | — | — | — |
| 1041. | / | / | — | / | / | — | — | — |
| 1042. | / | / | — | / | / | — | — | — |
| 1043. | / | / | — | / | / | — | — | — |
| 1044. | Priority | Force Chr En/Force Dischr En Load first/bat first /grid first | — | R | 0.Load(de fault)/1.B attery/2.G rid | — | — | — |
| 1045. | / | / | — | / | / | — | — | — |
| 1046. | / | / | — | / | / | — | — | — |
| 1047. | Aging Test St ep Cmd | Commandforagingtest | — | — | 0:default 1:charge 2: discharge | — | — | — |
| 1048. | Battery Typ e | Batterytypechooseof buck-boostinput | — | — | 0:Lithium 1:Lead-aci d 2:other | — | — | — |
| 1049. | / | / | — | / | / | — | — | — |
| 1050. | / | / | — | / | / | — | — | — |
| 1051. | / | / | — | / | / | — | — | — |
| 1052. | / | / | — | / | / | — | — | — |
| 1053. | / | / | — | / | / | — | — | — |
| 1054. | / | / | — | / | / | — | — | — |
| 1060. | Buck Ups Fun E n | — | Ups function enable or disable | — | — | 0:disable 1:enable | — | — |
| 1061. | Buck UPSVolt S et | UPSoutputvoltage | — | 0:230 1:208 2:240 | 230 V | — | — | — |
| 1062. | UPSFreq Set | UPSoutputfrequency | — | 0:50 Hz 1:60 Hz | 50 Hz | — | — | — |
| 1070. | Grid First Disch arge Power Rat e | Discharge Power Rate when Grid First | W | 0-100 1% | Discharge Power Rate when Grid First | — | — | — |
| 1071. | Grid First Stop S OC | Stop Discharge soc when Grid First | W | 0-100 1% | Stop Discharge socwhen Grid First | — | — | — |
| 1072… 1079 | / | / | / | / / | / | — | — | — |
| 1080. | Grid First Start Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1081. | Grid First Stop Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1082. | Grid First Stop Switch 1 | Enable:1 Disable:0 | — | 0 or 1 | Grid First enable | — | — | — |
| 1083. | Grid First Start Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1084. | Grid First Stop Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1085. | Grid First Stop Switch 2 | Force Discharge.b Switch&L CD_SET_FORCE_TRUE_2)= =LCD_SET_FORCE_TRUE_2 | — | 0 or 1 | Grid First enable | — | — | — |
| 1086. | Grid First Start Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1087. | Grid First Stop Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1088. | Grid First Stop Switch 3 | Enable:1 Disable:0 | — | 0 or 1 | Grid First enable | — | — | — |
| 1089. | / | / | / | / / | / | — | — | — |
| 1090. | Bat First Power Rate | Charge Power Rate when Bat First | W | 0-100 1% | Charge Power Rate when Bat First | — | — | — |
| 1091. | w Bat Firststop SOC | Stop Charge soc when Bat First | W | 0-100 1% | Stop Chargesoc when Bat First | — | — | — |
| 1092. | AC charge Switch | When Bat First Enable:1 Disable:0 | — | Enable:1 Disable:0 | ACCharge Enable | — | — | — |
| 1093… 1099 | — | — | — | — | — | — | — | — |
| 1100. | Bat First Start Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1101. | Bat First Stop Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1102. | Bat First on/off Switch 1 | Enable:1 Disable:0 | — | 0 or 1 | Bat First Enable 1 | — | — | — |
| 1103. | Bat First Start Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1104. | Bat First Stop Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1105. | Bat Firston/off Switch 2 | Enable:1 Disable:0 | — | 0 or 1 | Bat First Enable 2 | — | — | — |
| 1106. | Bat First Start Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1107. | Bat First Stop Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | — | — | — |
| 1108. | Bat Firston/off Switch 3 | Enable:1 Disable:0 | — | 0 or 1 | Bat First Enable 3 | — | — | — |
| 1109. | / | / | / | / / | / | reserve | — | — |
| 1110. | Load First Start Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1111. | Load First Stop Time 1 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1112. | Load First Switch 1 | Enable:1 Disable:0 | — | 0 or 1 | Load First Enable | SPA/reserve | — | — |
| 1113. | Load First Start Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1114. | Load First Stop Time 2 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1115. | Load First Switch 2 | Enable:1 Disable:0 | — | 0 or 1 | Load First Enable | SPA/reserve | — | — |
| 1116. | Load First Start Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1117. | Load First Stop Time 3 | Higheightbit:hour Loweightbit:minute | — | 0-23 0-59 | — | SPA/reserve | — | — |
| 1118. | Load First Switch 3 | Enable:1 Disable:0 | — | 0 or 1 | Load First Enable | SPA/reserve | — | — |
| 1119. | New EPower C alc Flag | / | / | / / | / | 0:Theoldformula 1 : The new formula | — | — |
| 1120. | Back Up En | Back Up Enable | — | — | — | MIXUS | — | — |
| 1121. | SGIPEn | SGIPEnable | — | — | — | MIXUS | — | — |

## Storage Holding Registers (1125–1249)
Additional SPA/SPH storage configuration registers.

**Applies to:** Storage SPA/SPH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1125 | Bat Serial NO. 8 | Product serial number of the first PACK of energy storagebatteries | / | / ASCII | — | — | — | — |
| 1126 | Bat Serial NO. 7 | — | / | / ASCII | — | — | — | — |
| 1127 | Bat Serial NO. 6 | — | / | / ASCII | — | — | — | — |
| 1128 | Bat Serial NO. 5 | — | / | / ASCII | — | — | — | — |
| 1129 | Bat Serial NO. 4 | — | / | / ASCII | — | — | — | — |
| 1130 | Bat Serial NO. 3 | — | / | / ASCII | — | — | — | — |
| 1131 | Bat Serial NO. 2 | — | / | / ASCII | — | — | — | — |
| 1132 | Bat Serial NO. 1 | — | / | / ASCII | — | — | — | — |
| 1132 ~1204 | Bat Serial NO. 8~ Bat Serial NO. 1 | The serial number of the second to tenth packs of the energy storage battery consists of nine packs, and | / | / ASCII | — | — | — | — |
| 1244 | Com version Name H | Name of the battery main controlfirmwareversion | — | ASCII | — | — | — | — |
| 1245 | Com version Name L | Name of the battery main controlfirmwareversion | — | ASCII | — | — | — | — |
| 1246 | Com version No | Versionofthebatterymain controlfirmware | — | digital | — | — | — | — |
| 1247 | Com version Name H | Name of battery monitoring firmware version | — | ASCII | — | — | — | — |
| 1248 | Com version Name L | Name of battery monitoring firmware version | — | ASCII | — | — | — | — |
| 1249 | Com version No | Battery monitoring firmwareversion | — | digital | — | — | — | — |

## Common Input Registers (0–124)
Applies to TL3/MAX and legacy inverters for basic PV/AC telemetry.

**Applies to:** TL-X/TL-XH (legacy mode), TL3-X/MAX/MID/MAC, Storage MIX/SPA/SPH, Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0. | — | Inverter Status | Inverterrunstate | 0:waiting, 1:normal, 3:fault | — | — | tlx:status_code, tl3:status_code, offgrid:status_code | Status code |
| 1. | — | Ppv H | Inputpower(high) | 0.1 W | — | — | tlx:input_power, tl3:input_power, offgrid:input_1_voltage | Input 1 voltage, Internal wattage, PV1 voltage |
| 2. | — | Ppv L | Inputpower(low) | 0.1 W | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3. | — | Vpv 1 | PV1voltage | 0.1 V | — | — | tlx:input_1_voltage, tl3:input_1_voltage, offgrid:input_1_power | Input 1 Wattage, Input 1 voltage, PV1 charge power, PV1 voltage |
| 4. | — | PV 1 Curr | PV1inputcurrent | 0.1 A | — | — | tlx:input_1_amperage, tl3:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 5. | — | Ppv 1 H | PV1inputpower(high) | 0.1 W | — | — | tlx:input_1_power, tl3:input_1_power, offgrid:input_2_power | Input 1 Wattage, Input 2 Wattage, PV1 charge power, PV2 charge power |
| 6. | — | Ppv 1 L | PV1inputpower(low) | 0.1 W | — | — | — | — |
| 7. | — | Vpv 2 | PV2voltage | 0.1 V | — | — | tlx:input_2_voltage, tl3:input_2_voltage, offgrid:input_1_amperage | Input 1 Amperage, Input 2 voltage, PV1 buck current, PV2 voltage |
| 8. | — | PV 2 Curr | PV2inputcurrent | 0.1 A | — | — | tlx:input_2_amperage, tl3:input_2_amperage, offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9. | — | Ppv 2 H | PV2inputpower(high) | 0.1 W | — | — | tlx:input_2_power, tl3:input_2_power, offgrid:output_active_power | Input 2 Wattage, Output active power, PV2 charge power |
| 10. | — | Ppv 2 L | PV2inputpower(low) | 0.1 W | — | — | — | — |
| 11. | — | Vpv 3 | PV3voltage | 0.1 V | — | — | tlx:input_3_voltage, tl3:output_power | Input 3 voltage, Output power |
| 12. | — | PV 3 Curr | PV3inputcurrent | 0.1 A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 13. | — | Ppv 3 H | PV3inputpower(high) | 0.1 W | — | — | tlx:input_3_power, tl3:grid_frequency, offgrid:charge_power | AC frequency, Battery charge power, Charge Power, Grid frequency, Input 3 Wattage |
| 14. | — | Ppv 3 L | PV3inputpower(low) | 0.1 W | — | — | tl3:output_1_voltage | Output 1 voltage, Output voltage |
| 15. | — | Vpv 4 | PV4voltage | 0.1 V | — | — | tlx:input_4_voltage, tl3:output_1_amperage | Input 4 voltage, Output 1 Amperage, Output amperage |
| 16. | — | PV 4 Curr | PV4inputcurrent | 0.1 A | — | — | tlx:input_4_amperage, tl3:output_1_power | Input 4 Amperage, Output 1 Wattage |
| 17. | — | Ppv 4 H | PV4inputpower(high) | 0.1 W | — | — | tlx:input_4_power, offgrid:battery_voltage | Battery voltage, Input 4 Wattage |
| 18. | — | Ppv 4 L | PV4inputpower(low) | 0.1 W | — | — | tl3:output_2_voltage, offgrid:soc | Output 2 voltage, SOC |
| 19. | — | Vpv 5 | PV5voltage | 0.1 V | — | — | tlx:input_5_voltage, tl3:output_2_amperage, offgrid:bus_voltage | Bus voltage, Input 5 voltage, Output 2 Amperage |
| 20. | — | PV 5 Curr | PV5inputcurrent | 0.1 A | — | — | tlx:input_5_amperage, tl3:output_2_power, offgrid:grid_voltage | Grid voltage, Input 5 Amperage, Output 2 Wattage |
| 21. | — | Ppv 5 H | PV5inputpower(high) | 0.1 W | — | — | tlx:input_5_power, offgrid:grid_frequency | AC frequency, Grid frequency, Input 5 Wattage |
| 22. | — | Ppv 5 L | PV5inputpower(low) | 0.1 W | — | — | tl3:output_3_voltage, offgrid:output_1_voltage | Output 1 voltage, Output 3 voltage, Output voltage |
| 23. | — | Vpv 6 | PV6voltage | 0.1 V | — | — | tlx:input_6_voltage, tl3:output_3_amperage, offgrid:output_frequency | Input 6 voltage, Output 3 Amperage, Output frequency |
| 24. | — | PV 6 Curr | PV6inputcurrent | 0.1 A | — | — | tlx:input_6_amperage, tl3:output_3_power, offgrid:output_dc_voltage | Input 6 Amperage, Output 3 Wattage, Output DC voltage |
| 25. | Ppv 6 H | PV 6 inputpower(high) | — | 0.1 W | — | — | tlx:input_6_power, offgrid:inverter_temperature | Input 6 Wattage, Temperature |
| 26. | Ppv 6 L | PV 6 inputpower(low) | — | 0.1 W | — | — | tl3:output_energy_today, offgrid:dc_dc_temperature | DC-DC temperature, Energy produced today |
| 27. | Vpv 7 | PV 7 voltage | — | 0.1 V | — | — | tlx:input_7_voltage, offgrid:load_percent | Input 7 voltage, Inverter load |
| 28. | PV 7 Curr | PV 7 inputcurrent | — | 0.1 A | — | — | tlx:input_7_amperage, tl3:output_energy_total, offgrid:battery_port_voltage | Battery port voltage, Input 7 Amperage, Total energy produced |
| 29. | Ppv 7 H | PV 7 inputpower(high) | — | 0.1 W | — | — | tlx:input_7_power, offgrid:battery_bus_voltage | Battery bus voltage, Input 7 Wattage |
| 30. | Ppv 7 L | PV 7 inputpower(low) | — | 0.1 W | — | — | tl3:operation_hours, offgrid:operation_hours | Running hours |
| 31. | Vpv 8 | PV 8 voltage | — | 0.1 V | — | — | tlx:input_8_voltage | Input 8 voltage |
| 32. | PV 8 Curr | PV 8 inputcurrent | — | 0.1 A | — | — | tlx:input_8_amperage, tl3:inverter_temperature | Input 8 Amperage, Temperature |
| 33. | Ppv 8 H | PV 8 inputpower(high) | — | 0.1 W | — | — | tlx:input_8_power | Input 8 Wattage |
| 34. | Ppv 8 L | PV 8 inputpower(low) | — | 0.1 W | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35. | Pac H | Outputpower(high) | — | 0.1 W | — | — | tlx:output_power | Output power |
| 36. | Pac L | Outputpower(low) | — | 0.1 W | — | — | — | — |
| 37. | Fac | Gridfrequency | — | 0.01 Hz | — | — | tlx:grid_frequency | AC frequency, Grid frequency |
| 38. | Vac 1 | Three/singlephasegridvoltage | — | 0.1 V | — | — | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 39. | Iac 1 | Three/singlephasegridoutputcurrent | — | 0.1 A | — | — | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 40. | Pac 1 H | Three/single phase grid output watt VA(high) | — | 0.1 VA | — | — | tlx:output_1_power, tl3:fault_code | Fault code, Output 1 Wattage |
| 41. | Pac 1 L | Three/single phase grid output watt VA(low) | — | 0.1 VA | — | — | tl3:ipm_temperature | Intelligent Power Management temperature |
| 42. | Vac 2 | Threephasegridvoltage | — | 0.1 V | — | — | tlx:output_2_voltage, tl3:p_bus_voltage, offgrid:fault_code | Fault code, Output 2 voltage, P-bus voltage |
| 43. | Iac 2 | Threephasegridoutputcurrent | — | 0.1 A | — | — | tlx:output_2_amperage, tl3:n_bus_voltage, offgrid:warning_code | N-bus voltage, Output 2 Amperage, Warning code |
| 44. | Pac 2 H | Threephasegridoutputpower(high) | — | 0.1 VA | — | — | tlx:output_2_power | Output 2 Wattage |
| 45. | Pac 2 L | Threephasegridoutputpower(low) | — | 0.1 VA | — | — | — | — |
| 46. | Vac 3 | Threephasegridvoltage | — | 0.1 V | — | — | tlx:output_3_voltage | Output 3 voltage |
| 47. | Iac 3 | Threephasegridoutputcurrent | — | 0.1 A | — | — | tlx:output_3_amperage, tl3:derating_mode, offgrid:constant_power | Derating mode, Output 3 Amperage |
| 48. | Pac 3 H | Threephasegridoutputpower(high) | — | 0.1 VA | — | — | tlx:output_3_power, tl3:input_1_energy_today, offgrid:input_1_energy_today | Input 1 energy today, Output 3 Wattage, PV1 energy produced today |
| 49. | Pac 3 L | Threephasegridoutputpower(low) | — | 0.1 VA | — | — | — | — |
| 50. | Vac_RS | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | tl3:input_1_energy_total, offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51. | Vac_ST | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | — | — |
| 52. | Vac_TR | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | tl3:input_2_energy_today, offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53. | Eactoday H | Todaygenerateenergy(high) | — | 0.1 k WH | — | — | tlx:output_energy_today | Energy produced today |
| 54. | Eactoday L | Todaygenerateenergy(low) | — | 0.1 k WH | — | — | tl3:input_2_energy_total, offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55. | Eactotal H | Totalgenerateenergy(high) | — | 0.1 k WH | — | — | tlx:output_energy_total | Total energy produced |
| 56. | Eactotal L | Totalgenerateenergy(low) | — | 0.1 k WH | — | — | tl3:input_energy_total, offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today, Total energy input |
| 57. | Timetotal H | Worktimetotal(high) | — | 0.5 s | — | — | tlx:operation_hours | Running hours |
| 58. | Timetotal L | Worktimetotal(low) | — | 0.5 s | — | — | tl3:output_reactive_power, offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime, Reactive wattage |
| 59. | Epv 1_today H | PV 1 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 60. | Epv 1_today L | PV 1 Energytoday(low) | — | 0.1 k Wh | — | — | tl3:output_reactive_energy_today, offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61. | Epv 1_total H | PV 1 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 62. | Epv 1_total L | PV 1 Energytotal(low) | — | 0.1 k Wh | — | — | tl3:output_reactive_energy_total, offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63. | Epv 2_today H | PV 2 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 64. | Epv 2_today L | PV 2 Energytoday(low) | — | 0.1 k Wh | — | — | tl3:warning_code, offgrid:ac_discharge_energy_today | AC Discharged Today, Warning code |
| 65. | Epv 2_total H | PV 2 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_2_energy_total, tl3:warning_value | Input 2 total energy, PV2 energy produced Lifetime |
| 66. | Epv 2_total L | PV 2 Energytotal(low) | — | 0.1 k Wh | — | — | tl3:real_output_power_percent, offgrid:ac_discharge_energy_total | Grid Discharged Lifetime, Real power output percentage |
| 67. | Epv 3_today H | PV 3 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_3_energy_today | Input 3 energy today |
| 68. | Epv 3_today L | PV 3 Energytoday(low) | — | 0.1 k Wh | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69. | Epv 3_total H | PV 3 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_3_energy_total, offgrid:discharge_power | Battery discharge power, Discharge Power, Input 3 total energy |
| 70. | Epv 3_total L | PV 3 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 71. | Epv 4_today H | PV 4 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_4_energy_today | Input 4 energy today |
| 72. | Epv 4_today L | PV 4 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 73. | Epv 4_total H | PV 4 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_4_energy_total, offgrid:battery_discharge_amperage | Battery discharge current, Input 4 total energy |
| 74. | Epv 4_total L | PV 4 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 75. | Epv 5_today H | PV 5 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_5_energy_today | Input 5 energy today |
| 76. | Epv 5_today L | PV 5 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 77. | Epv 5_total H | PV 5 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_5_energy_total, offgrid:battery_power | Battery charging/ discharging(-ve), Input 5 total energy |
| 78. | Epv 5_total L | PV 5 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 79. | Epv 6_today H | PV 6 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_6_energy_today | Input 6 energy today |
| 80. | Epv 6_today L | PV 6 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 81. | Epv 6_total H | PV 6 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_6_energy_total | Input 6 total energy |
| 82. | Epv 6_total L | PV 6 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 83. | Epv 7_today H | PV 7 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_7_energy_today | Input 7 energy today |
| 84. | Epv 7_today L | PV 7 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 85. | Epv 7_total H | PV 7 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_7_energy_total | Input 7 total energy |
| 86. | Epv 7_total L | PV 7 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 87. | Epv 8_today H | PV 8 Energytoday(high) | — | 0.1 k Wh | — | — | tlx:input_8_energy_today | Input 8 energy today |
| 88. | Epv 8_today L | PV 8 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 89. | Epv 8_total H | PV 8 Energytotal(high) | — | 0.1 k Wh | — | — | tlx:input_8_energy_total | Input 8 total energy |
| 90. | Epv 8_total L | PV 8 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 91. | Epv_total H | PVEnergytotal(high) | — | 0.1 k Wh | — | — | tlx:input_energy_total | Total energy input |
| 92. | Epv_total L | PVEnergytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 93. | Temp 1 | Invertertemperature | — | 0.1 C | — | — | tlx:inverter_temperature | Temperature |
| 94. | Temp 2 | Theinside IPMininverter Temperature | — | 0.1 C | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 95. | Temp 3 | Boosttemperature | — | 0.1 C | — | — | tlx:boost_temperature | Boost temperature |
| 96. | Temp 4 | — | — | reserved | — | — | — | — |
| 97. | uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 98. | PBus Voltage | PBusinside Voltage | — | 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 99. | NBus Voltage | NBusinside Voltage | — | 0.1 V | — | — | tlx:n_bus_voltage | N-bus voltage |
| 100. | IPF | Inverteroutput PFnow | 0-20000 | — | — | — | — | — |
| 101. | Real OPPercent | Real Outputpower Percent | — | 1% | — | — | tlx:real_output_power_percent | Real power output percentage |
| 102. | OPFullwatt H | Output Maxpower Limitedhigh | — | — | — | — | — | — |
| 103. | OPFullwatt L | Output Maxpower Limitedlow | — | 0.1 W | — | — | — | — |
| 104. | Derating Mode | Derating Mode | 0:noderate; 1:PV; 2:*; 3:Vac; 4:Fac; 5:Tboost; 6:Tinv; 7:Control; 8:*; 9:*OverBack ByTime; | — | — | — | tlx:derating_mode | Derating mode |
| 105. | Fault Maincode | Inverterfaultmaincode | — | — | — | — | tlx:fault_code | Fault code |
| 106. | — | — | — | — | — | — | — | — |
| 107. | Fault Subcode | Inverterfaultsubcode | — | — | — | — | — | — |
| 108. | Remote Ctrl En | / | 0.LoadFirst 1.BatFirst 2.Grid | / Storage Pow er(SPA) | — | — | — | — |
| 109. | Remote Ctrl Pow er | / | — | / Storage Pow er(SPA) | — | — | — | — |
| 110. | Warningbit H | Warningbit H | — | — | — | — | tlx:warning_code | Warning code |
| 111. | Warn Subcode | Inverterwarnsubcode | — | — | — | — | — | — |
| 112. | Warn Maincode | Inverterwarnmaincode | — | — | — | — | — | — |
| 113. | real Power Percent | real Power Percent | 0-100 | % MAX | — | — | — | — |
| 114. | inv start delay time | invstartdelaytime | — | MAX | — | — | — | — |
| 115. | b INVAll Fault Cod e | b INVAll Fault Code | — | MAX | — | — | — | — |
| 116. | AC charge Power_H | Gridpowertolocalload | — | 0.1 kwh Storage Power | — | — | — | — |
| 117. | AC charge Power_L | Gridpowertolocalload | — | 0.1 kwh Storage Power | — | — | — | — |
| 118. | Priority | 0:Load First | — | Storage | — | — | — | — |
| 119. | Battery Type | 0:Lead-acid 1:Lithiumbattery | — | — | Storage Power | — | — | — |
| 120. | Auto Proofread C MD | Aging mode Auto-calibration command | — | — | Storage Power | — | — | — |
| 124. | reserved | — | — | — | reserved | — | — | — |

## TL-X/TL-XH Input Registers (3000–3124)
Primary TL-X/TL-XH telemetry mirror (PV/AC metrics).

**Applies to:** TL-X/TL-XH/TL-XH US

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | Inverter Status | Inverterrunstate High 8 bitsmode(specificmode) 0:Waitingmodule 1:Self-testmode,optional 2:Reserved 3:Sys Fault module 4:Flashmodule 5:PVBATOnlinemodule: 6:Bat Onlinemodule | — | — | — | — | tlx:status_code | Status code |
| 3001 | Ppv H | PVtotalpower | — | 0.1 W | — | — | tlx:input_power | Internal wattage |
| 3002 | Ppv L | — | — | — | — | — | — | — |
| 3003 | Vpv 1 | PV 1 voltage | — | 0.1 V | — | — | tlx:input_1_voltage | Input 1 voltage, PV1 voltage |
| 3004 | Ipv 1 | PV 1 inputcurrent | — | 0.1 A | — | — | tlx:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 3005 | Ppv 1 H | PV 1 power | — | 0.1 W | — | — | tlx:input_1_power | Input 1 Wattage, PV1 charge power |
| 3006 | Ppv 1 L | — | — | — | — | — | — | — |
| 3007 | Vpv 2 | PV 2 voltage | — | 0.1 V | — | — | tlx:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3008 | Ipv 2 | PV 2 inputcurrent | — | 0.1 A | — | — | tlx:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 3009 | Ppv 2 H | PV 2 power | — | 0.1 W | — | — | tlx:input_2_power | Input 2 Wattage, PV2 charge power |
| 3010 | Ppv 2 L | — | — | — | — | — | — | — |
| 3011 | Vpv 3 | PV 3 voltage | — | 0.1 V | — | — | tlx:input_3_voltage | Input 3 voltage |
| 3012 | Ipv 3 | PV 3 inputcurrent | — | 0.1 A | — | — | tlx:input_3_amperage | Input 3 Amperage |
| 3013 | Ppv 3 H | PV 3 power | — | 0.1 W | — | — | tlx:input_3_power | Input 3 Wattage |
| 3014 | Ppv 3 L | — | — | — | — | — | — | — |
| 3015 | Vpv 4 | PV 4 voltage | — | — | — | — | tlx:input_4_voltage | Input 4 voltage |
| 3016 | Ipv 4 | PV 4 inputcurrent | — | — | — | — | tlx:input_4_amperage | Input 4 Amperage |
| 3017 | Ppv 4 H | PV 4 power | — | — | — | — | tlx:input_4_power | Input 4 Wattage |
| 3018 | Ppv 4 L | — | — | — | — | — | — | — |
| 3019 | Psys H | Systemoutputpower | — | 0.1 W | — | — | — | — |
| 3020 | Psys L | — | — | — | — | — | — | — |
| 3021 | Qac H | reactivepower | — | 0.1 Var | — | — | tlx:output_reactive_power | Reactive wattage |
| 3022 | Qac L | — | — | — | — | — | — | — |
| 3023 | Pac H | Outputpower | — | 0.1 W Output power | — | — | tlx:output_power | Output power |
| 3024 | Pac L | — | — | — | — | — | — | — |
| 3025 | Fac | Gridfrequency | — | 0.01 Hz Grid frequency | — | — | tlx:grid_frequency | AC frequency, Grid frequency |
| 3026 | Vac 1 | Three/singlephasegridvoltage | — | 0.1 V Three/single phase grid voltage | — | — | tlx:output_1_voltage | Output 1 voltage, Output voltage |
| 3027 | Iac 1 | Three/singlephasegridoutputcurrent | — | 0.1 A Three/single | — | — | tlx:output_1_amperage | Output 1 Amperage, Output amperage |
| 3028 | Pac 1 H | Three/singlephasegridoutputwatt VA | — | 0.1 VA Three/single phasegrid outputwatt VA | — | — | tlx:output_1_power | Output 1 Wattage |
| 3029 | Pac 1 L | — | — | — | — | — | — | — |
| 3030 | Vac 2 | Threephasegridvoltage | — | 0.1 V Threephase gridvoltage | — | — | tlx:output_2_voltage | Output 2 voltage |
| 3031 | Iac 2 | Threephasegridoutputcurrent | — | 0.1 A Threephase gridoutput current | — | — | tlx:output_2_amperage | Output 2 Amperage |
| 3032 | Pac 2 H | Threephasegridoutputpower | — | 0.1 VA Threephase gridoutput power | — | — | tlx:output_2_power | Output 2 Wattage |
| 3033 | Pac 2 L | — | — | — | — | — | — | — |
| 3034 | Vac 3 | Threephasegridvoltage | — | 0.1 V Threephase gridvoltage | — | — | tlx:output_3_voltage | Output 3 voltage |
| 3035 | Iac 3 | Threephasegridoutputcurrent | — | 0.1 A Threephase gridoutput current | — | — | tlx:output_3_amperage | Output 3 Amperage |
| 3036 | Pac 3 H | Threephasegridoutputpower | — | 0.1 VA Threephase gridoutput power | — | — | tlx:output_3_power | Output 3 Wattage |
| 3037 | Pac 3 L | — | — | — | — | — | — | — |
| 3038 | Vac_RS | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3039 | Vac_ST | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3040 | Vac_TR | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3041 | Ptousertotal H | Totalforwardpower | — | 0.1 W Total forward power | — | — | tlx:power_to_user | Power to user |
| 3042 | Ptousertotal L | — | — | — | — | — | — | — |
| 3043 | Ptogridtotal H | Totalreversepower | — | 0.1 W Totalreverse power | — | — | tlx:power_to_grid | Power to grid |
| 3044 | Ptogridtotal L | — | — | — | — | — | — | — |
| 3045 | Ptoloadtotal H | Totalloadpower | — | 0.1 W Total load power | — | — | tlx:power_user_load | Power user load |
| 3046 | Ptoloadtotal L | — | — | — | — | — | — | — |
| 3047 | Timetotal H | Worktimetotal | — | 0.5 s | — | — | tlx:operation_hours | Running hours |
| 3048 | Timetotal L | — | — | — | — | — | — | — |
| 3049 | Eactoday H | Todaygenerateenergy | — | 0.1 k Wh Today generate energy | — | — | tlx:output_energy_today | Energy produced today |
| 3050 | Eactoday L | — | — | — | — | — | — | — |
| 3051 | Eactotal H | Totalgenerateenergy | — | 0.1 k Wh Total generate | — | — | tlx:output_energy_total | Total energy produced |
| 3052 | Eactotal L | — | — | — | — | — | — | — |
| 3053 | Epv_total H | PVenergytotal | — | 0.1 k Wh PVenergy total | — | — | tlx:input_energy_total | Total energy input |
| 3054 | Epv_total L | — | — | — | — | — | — | — |
| 3055 | Epv 1_today H | PV 1 energytoday | — | 0.1 k Wh | — | — | tlx:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 3056 | Epv 1_today L | — | — | — | — | — | — | — |
| 3057 | Epv 1_total H | PV 1 energytotal | — | 0.1 k Wh | — | — | tlx:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 3058 | Epv 1_total L | — | — | — | — | — | — | — |
| 3059 | Epv 2_today H | PV 2 energytoday | — | 0.1 k Wh | — | — | tlx:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 3060 | Epv 2_today L | — | — | — | — | — | — | — |
| 3061 | Epv 2_total H | PV 2 energytotal | — | 0.1 k Wh | — | — | tlx:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 3062 | Epv 2_total L | — | — | — | — | — | — | — |
| 3063 | Epv 3_today H | PV 3 energytoday | — | 0.1 k Wh | — | — | tlx:input_3_energy_today | Input 3 energy today |
| 3064 | Epv 3_today L | — | — | — | — | — | — | — |
| 3065 | Epv 3_total H | PV 3 energytotal | — | 0.1 k Wh | — | — | tlx:input_3_energy_total | Input 3 total energy |
| 3066 | Epv 3_total L | — | — | — | — | — | — | — |
| 3067 | Etouser_today H | Todayenergytouser | — | 0.1 k Wh Todayenergy touser | — | — | tlx:energy_to_user_today | Energy To User (Today) |
| 3068 | Etouser_today L | — | — | — | — | — | — | — |
| 3069 | Etouser_total H | Totalenergytouser | — | 0.1 k Wh Totalenergy touser | — | — | tlx:energy_to_user_total | Energy To User (Total) |
| 3070 | Etouser_total L | — | — | — | — | — | — | — |
| 3071 | Etogrid_today H | Todayenergytogrid | — | 0.1 k Wh Todayenergy togrid | — | — | tlx:energy_to_grid_today | Energy To Grid (Today) |
| 3072 | Etogrid_today L | — | — | — | — | — | — | — |
| 3073 | Etogrid_total H | Totalenergytogrid | — | 0.1 k Wh Totalenergy togrid | — | — | tlx:energy_to_grid_total | Energy To Grid (Total) |
| 3074 | Etogrid_total L | — | — | — | — | — | — | — |
| 3075 | Eload_today H | Todayenergyofuserload | — | 0.1 k Wh Todayenergy ofuserload | — | — | — | — |
| 3076 | Eload_today L | — | — | — | — | — | — | — |
| 3077 | Eload_total H | Totalenergyofuserload | — | 0.1 k Wh Totalenergy ofuserload | — | — | — | — |
| 3078 | Eload_total L | — | — | — | — | — | — | — |
| 3079 | Epv 4_today H | PV 4 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3080 | Epv 4_today L | — | — | — | — | — | — | — |
| 3081 | Epv 4_total H | PV 4 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3082 | Epv 4_total L | — | — | — | — | — | — | — |
| 3083 | Epv_today H | PVenergytoday | — | 0.1 k Wh | — | — | — | — |
| 3084 | Epv_today L | — | — | — | — | — | — | — |
| 3085 | Reserved | — | — | — | — | — | — | — |
| 3086 | Derating Mode | Derating Mode | — | 0:c NOTDerate 1:c PVHigh Der ate 2: c Power Con stant Derate 3: c Grid VHigh Derate 4:c Freq High D erate 5:c Dc Soure M ode Derate 6:c Inv Tempr D erate 7:c Active Pow er Order 8:c Load Speed Process 9:c Over Back by Time 10:c Internal T empr Derate 11:c Out Temp r Derate 12:c Line Impe Calc Derate 13: c Parallel A nti Backflow D erate 14:c Local Anti Backflow Dera te 15:c Bdc Load P ri Derate 16:c Chk CTErr Derate | — | — | tlx:derating_mode | Derating mode |
| 3087 | ISO | PVISOvalue | — | 1 KΩ | — | — | — | — |
| 3088 | DCI_R | RDCICurr | — | 0.1 m A | — | — | — | — |
| 3089 | DCI_S | SDCICurr | — | 0.1 m A | — | — | — | — |
| 3090 | DCI_T | TDCICurr | — | 0.1 m A | — | — | — | — |
| 3091 | GFCI | GFCICurr | — | 1 m A | — | — | — | — |
| 3092 | Bus Voltage | totalbusvoltage | — | 0.1 V | — | — | — | — |
| 3093 | Temp 1 | Invertertemperature | — | 0.1℃ | — | — | tlx:inverter_temperature | Temperature |
| 3094 | Temp 2 | Theinside IPMininvertertemperature | — | 0.1℃ | — | — | tlx:ipm_temperature | Intelligent Power Management temperature |
| 3095 | Temp 3 | Boosttemperature | — | 0.1℃ | — | — | tlx:boost_temperature | Boost temperature |
| 3096 | Temp 4 | Reserved | — | 0.1℃ | — | — | — | — |
| 3097 | Temp 5 | Commmunicationbroadtemperature | — | 0.1℃ | — | — | tlx:comm_board_temperature | Comm board temperature |
| 3098 | PBus Voltage | PBusinside Voltage | — | 0.1 V | — | — | tlx:p_bus_voltage | P-bus voltage |
| 3099 | NBus Voltage | NBusinside Voltage | — | 0.1 V | — | — | tlx:n_bus_voltage | N-bus voltage |
| 3100 | IPF | Inverteroutput PFnow | — | 0-20000 | — | — | — | — |
| 3101 | Real OPPercent | Real Outputpower Percent | — | 1% 1~100 | — | — | tlx:real_output_power_percent | Real power output percentage |
| 3102 | OPFullwatt H | Output Maxpower Limited | — | 0.1 W Output Maxpower Limited | — | — | — | — |
| 3103 | OPFullwatt L | — | — | — | — | — | — | — |
| 3104 | Standby Flag | Inverterstandbyflag | — | bitfield bit 0:turn off Order; bit 1:PVLow; bit 2:AC Volt/Freq outofscope; bit 3~bit 7 : Reserved | — | — | — | — |
| 3105 | Fault Maincode | Inverterfaultmaincode | — | — | — | — | tlx:fault_code | Fault code |
| 3106 | Warn Maincode | Inverter Warningmaincode | — | — | — | — | — | — |
| 3107 | Fault Subcode | Inverterfaultsubcode | — | bitfield | — | — | — | — |
| 3108 | Warn Subcode | Inverter Warningsubcode | — | bitfield | — | — | — | — |
| 3109 | — | — | — | bitfield | — | — | — | — |
| 3110 | — | — | — | bitfield | — | — | tlx:warning_code | Warning code |
| 3111 | uw Present FFTVa lue[CHANNEL_A ] | Present FFTValue[CHANNEL_A] | — | bitfield | — | — | tlx:present_fft_a | Present FFT A |
| 3112 | b Afci Status | AFCIStatus | — | 0 : waiting state 1:self-check 2:Detection of arcing state 3:faultstate 4 : update state | — | — | — | — |
| 3113 | uw Strength[CHA NNEL_A] | AFCIStrength[CHANNEL_A] | — | — | — | — | — | — |
| 3114 | uw Self Check Val ue[CHANNEL_A] | AFCISelf Check[CHANNEL_A] | — | — | — | — | — | — |
| 3115 | inv start delay time | invstartdelaytime | — | 1 S invstartdelay time | — | — | tlx:inv_start_delay | Inverter start delay |
| 3116 | Reserved | — | — | — | — | — | — | — |
| 3117 | Reserved | — | — | — | — | — | — | — |
| 3118 | BDC_On Off State | BDCconnectstate | — | 0:No BDC Connect 1:BDC 1 Connect 2:BDC 2 Connect 3:BDC 1+BDC 2 Connect | — | — | — | — |
| 3119 | Dry Contact State | Currentstatusof Dry Contact | — | Current status of Dry Contact 0:turnoff; 1:turnon; | — | — | — | — |
| 3120 | Reserved | — | — | — | — | — | — | — |
| 3121 | Pself H | self-usepower | — | 0.1 W | — | — | — | — |
| 3122 | Pself L | — | — | — | — | — | — | — |
| 3123 | Esys_today H | Systemenergytoday | — | 0.1 kwh | — | — | — | — |
| 3124 | Esys_today L | — | — | — | — | — | — | — |

## TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249)
Battery energy, power flow, and BMS telemetry for TL-XH hybrids.

**Applies to:** TL-X/TL-XH hybrids, Storage TL-XH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3239-3 249 | Reserve | Reserve | R/W | — | — | — | — | — |
| 3125 | Edischr_today H | Todaydischargeenergy | — | 0.1 k Wh Today discharge energy | — | — | tlx:discharge_energy_today, storage:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 3126 | Edischr_today L | — | — | — | — | — | — | — |
| 3127 | Edischr_total H | Totaldischargeenergy | — | 0.1 k Wh Total discharge energy | — | — | tlx:discharge_energy_total, storage:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 3128 | Edischr_total L | — | — | — | — | — | — | — |
| 3129 | Echr_today H | Chargeenergytoday | — | 0.1 k Wh Charge energytoday | — | — | tlx:charge_energy_today, storage:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 3130 | Echr_today L | — | — | — | — | — | — | — |
| 3131 | Echr_total H | Chargeenergytotal | — | 0.1 k Wh Charge energytotal | — | — | tlx:charge_energy_total, storage:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 3132 | Echr_total L | — | — | — | — | — | — | — |
| 3133 | Eacchr_today H | Todayenergyof ACcharge | — | 0.1 k Wh Todayenergy of ACcharge | — | — | — | — |
| 3134 | Eacchr_today L | — | — | — | — | — | — | — |
| 3135 | Eacchr_total H | Totalenergyof ACcharge | — | 0.1 k Wh Totalenergy of ACcharge | — | — | — | — |
| 3136 | Eacchr_total L | — | — | — | — | — | — | — |
| 3137 | Esys_total H | — | — | — | — | — | — | — |
| 3138 | Esys_total L | Totalenergyofsystemoutput\ | — | 0.1 k Wh | — | — | — | — |
| 3139 | Eself_today H | Todayenergyof Selfoutput | — | 0.1 k Wh | — | — | — | — |
| 3140 | Eself_today L | — | — | — | — | — | — | — |
| 3141 | Eself_total H | Totalenergyof Selfoutput | — | 0.1 kwh | — | — | — | — |
| 3142 | Eself_total L | — | — | — | — | — | — | — |
| 3143 | Reserved | — | — | — | — | — | — | — |
| 3144 | Priority | Word Mode | — | 0 Load First 1 Battery Firs t 2 Grid First | — | — | — | — |
| 3145 | EPSFac | UPSfrequency | — | 0.01 Hz | — | — | — | — |
| 3146 | EPSVac 1 | UPSphase Routputvoltage | — | 0.1 V | — | — | — | — |
| 3147 | EPSIac 1 | UPSphase Routputcurrent | — | 0.1 A | — | — | — | — |
| 3148 | EPSPac 1 H | UPSphase Routputpower | — | 0.1 VA | — | — | — | — |
| 3149 | EPSPac 1 L | — | — | — | — | — | — | — |
| 3150 | EPSVac 2 | UPSphase Soutputvoltage | — | 0.1 V | — | — | — | — |
| 3151 | EPSIac 2 | UPSphase Soutputcurrent | — | 0.1 A | — | — | — | — |
| 3152 | EPSPac 2 H | UPSphase Soutputpower | — | 0.1 VA | — | — | — | — |
| 3153 | EPSPac 2 L | — | — | — | — | — | — | — |
| 3154 | EPSVac 3 | UPSphase Toutputvoltage | — | 0.1 V | — | — | — | — |
| 3155 | EPSIac 3 | UPSphase Toutputcurrent | — | 0.1 A | — | — | — | — |
| 3156 | EPSPac 3 H | UPSphase Toutputpower | — | 0.1 VA | — | — | — | — |
| 3157 | EPSPac 3 L | — | — | — | — | — | — | — |
| 3158 | EPSPac H | UPSoutputpower | — | 0.1 VA | — | — | — | — |
| 3159 | EPSPac L | — | — | — | — | — | — | — |
| 3160 | Loadpercent | Loadpercentof UPSouput | — | 0.10% | — | — | — | — |
| 3161 | PF | Powerfactor | — | 0.1 | — | — | — | — |
| 3162 | DCV | DCvoltage | — | 1 m V | — | — | — | — |
| 3163 | Reserved | — | — | — | — | — | — | — |
| 3164 | New Bdc Flag | Whethertoparse BDCdataseparately | — | 0:Don'tneed 1:need | — | — | tlx:bdc_new_flag, storage:bdc_new_flag | BDC present |
| 3165 | BDCDerating Mo de | BDCDerating Mode: 0:Normal,unrestricted 1:Standbyorfault 2:Maximumbatterycurrentlimit (discharge) 3:Batterydischarge Enable(Discharge) 4:Highbusdischargederating | — | — | — | — | — | — |
| 3166 | Sys State_Mode | Systemwork Stateandmode The upper 8 bitsindicatethemode; 0:Nochargeanddischarge; 1:charge; 2:Discharge; Thelower 8 bitsrepresentthestatus; 0:Standby Status; 1:Normal Status; 2:Fault Status 3:Flash Status; | — | BDC 1 | — | — | — | — |
| 3167 | Fault Code | Storgedevicefaultcode | — | — | — | — | — | — |
| 3168 | Warn Code | Storgedevicewarningcode | — | — | — | — | — | — |
| 3169 | Vbat | Batteryvoltage | — | 0.01 V | — | — | tlx:battery_voltage, storage:battery_voltage | Battery voltage |
| 3170 | Ibat | Batterycurrent | — | 0.1 A | — | — | tlx:battery_current, storage:battery_current | Battery current |
| 3171 | SOC | Stateofcharge Capacity | — | 1% | — | — | tlx:soc, storage:soc | SOC |
| 3172 | Vbus 1 | Total BUSvoltage | — | 0.1 V | — | — | tlx:vbus1_voltage, storage:vbus1_voltage | VBUS1 voltage |
| 3173 | Vbus 2 | Onthe BUSvoltage | — | 0.1 V | — | — | tlx:vbus2_voltage, storage:vbus2_voltage | VBUS2 voltage |
| 3174 | Ibb | BUCK-BOOSTCurrent | — | 0.1 A | — | — | tlx:buck_boost_current, storage:buck_boost_current | Buck/boost current |
| 3175 | Illc | LLCCurrent | — | 0.1 A | — | — | tlx:llc_current, storage:llc_current | LLC current |
| 3176 | Temp A | Temperture A | — | 0.1℃ | — | — | tlx:battery_temperature_a, storage:battery_temperature_a | Battery temperature A |
| 3177 | Temp B | Temperture B | — | 0.1℃ | — | — | tlx:battery_temperature_b, storage:battery_temperature_b | Battery temperature B |
| 3178 | Pdischr H | Dischargepower | — | 0.1 W | — | — | tlx:discharge_power, storage:discharge_power | Battery discharge power, Discharge Power |
| 3179 | Pdischr L | — | — | — | — | — | — | — |
| 3180 | Pchr H | Chargepower | — | 0.1 W | — | — | tlx:charge_power, storage:charge_power | Battery charge power, Charge Power |
| 3181 | Pchr L | — | — | — | — | — | — | — |
| 3182 | Edischr_total H | Dischargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3183 | Edischr_total L | — | — | — | — | — | — | — |
| 3184 | Echr_total H | Chargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3185 | Echr_total L | — | — | — | — | — | — | — |
| 3186 | Reserved | Reserved | — | — | — | — | — | — |
| 3187 | BDC 1_Flag | BDCmark(chargeanddischarge, faultalarmcode) Bit 0:Charge En;BDCallowscharging Bit 1:Discharge En;BDCallows discharge Bit 2~7:Resvd;reserved Bit 8~11:Warn Sub Code;BDC sub-warningcode Bit 12~15:Fault Sub Code;BDC sub-errorcode | — | — | — | — | — | — |
| 3188 | Vbus 2 | Lower BUSvoltage | — | 0.1 V | — | — | — | — |
| 3189 | Bms Max Volt Cell No | Bms Max Volt Cell No | — | — | — | — | tlx:bms_max_volt_cell_no, storage:bms_max_volt_cell_no | BMS max volt cell no |
| 3190 | Bms Min Volt Cell No | Bms Min Volt Cell No | — | — | — | — | tlx:bms_min_volt_cell_no, storage:bms_min_volt_cell_no | BMS min volt cell no |
| 3191 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | tlx:bms_avg_temp_a, storage:bms_avg_temp_a | BMS avg temp A |
| 3192 | Bms Max Cell Tem p | Bms Max Cell Temp | — | 0.1°C | — | — | tlx:bms_max_cell_temp_a, storage:bms_max_cell_temp_a | BMS max cell temp A |
| 3193 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | 0.1°C | — | — | tlx:bms_avg_temp_b, storage:bms_avg_temp_b | BMS avg temp B |
| 3194 | Bms Max Cell Tem p | Bms Max Cell Temp | — | — | — | — | tlx:bms_max_cell_temp_b, storage:bms_max_cell_temp_b | BMS max cell temp B |
| 3195 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | tlx:bms_avg_temp_c, storage:bms_avg_temp_c | BMS avg temp C |
| 3196 | Bms Max SOC | Bms Max SOC | — | 1% | — | — | tlx:bms_max_soc, storage:bms_max_soc | BMS max SOC |
| 3197 | Bms Min SOC | Bms Min SOC | — | 1% | — | — | tlx:bms_min_soc, storage:bms_min_soc | BMS min SOC |
| 3198 | Parallel Battery N um | Parallel Battery Num | — | — | — | — | tlx:parallel_battery_num, storage:parallel_battery_num | — |
| 3199 | Bms Derate Reas on | Bms Derate Reason | — | — | — | — | tlx:bms_derate_reason, storage:bms_derate_reason | BMS derate reason |
| 3200 | Bms Gauge FCC (Ah) | Bms Gauge FCC(Ah) | — | — | — | — | tlx:bms_gauge_fcc_ah, storage:bms_gauge_fcc_ah | BMS full charge capacity |
| 3201 | Bms Gauge RM (Ah) | Bms Gauge RM(Ah) | — | — | — | — | tlx:bms_gauge_rm_ah, storage:bms_gauge_rm_ah | BMS remaining capacity |
| 3202 | Bms Error | BMSProtect 1 | — | — | — | — | tlx:bms_protect1, storage:bms_protect1 | BMS protect 1 |
| 3203 | Bms Warn | BMSWarn 1 | — | — | — | — | tlx:bms_warn1, storage:bms_warn1 | BMS warn 1 |
| 3204 | Bms Fault | BMSFault 1 | — | — | — | — | tlx:bms_fault1, storage:bms_fault1 | BMS fault 1 |
| 3205 | Bms Fault 2 | BMSFault 2 | — | — | — | — | tlx:bms_fault2, storage:bms_fault2 | BMS fault 2 |
| 3206 | Reserved | — | — | — | — | — | — | — |
| 3207 | Reserved | — | — | — | — | — | — | — |
| 3208 | Reserved | — | — | — | — | — | — | — |
| 3209 | Reserved | — | — | — | — | — | — | — |
| 3210 | Bat Iso Status | Battery ISOdetectionstatus | — | 0:Not detected 1:Detection completed | — | — | tlx:bat_iso_status, storage:bat_iso_status | — |
| 3211 | Batt Need Charge Request Flag | batteryworkrequest | — | bit 0:1: Prohibit chargin g,0: Allow the chargin g bit 1:1: Enable strong charge, 0: disable strong charge bit 2:1: Enable strong charge 2 0: disable strong charge | — | — | tlx:batt_request_flags, storage:batt_request_flags | — |
| 3212 | BMS_Status | batteryworkingstatus | R | 0:dormancy 1:Charge 2:Discharge 3:free 4:standby 5:Softstart 6:fault 7:update | — | — | tlx:bms_status, storage:bms_status | BMS status |
| 3213 | Bms Error 2 | BMSProtect 2 | R | 1 | — | — | tlx:bms_protect2, storage:bms_protect2 | BMS protect 2 |
| 3214 | Bms Warn 2 | BMSWarn 2 | R | 1 | — | — | tlx:bms_warn2, storage:bms_warn2 | BMS warn 2 |
| 3215 | BMS_SOC | BMSSOC | R | 1% | — | — | tlx:bms_soc, storage:bms_soc | BMS SOC |
| 3216 | BMS_Battery Vol t | BMSBattery Volt | R | 0.01 V | — | — | tlx:bms_battery_voltage, storage:bms_battery_voltage | BMS battery voltage |
| 3217 | BMS_Battery Cur r | BMSBattery Curr | R | 0.01 A | — | — | tlx:bms_battery_current, storage:bms_battery_current | BMS battery current |
| 3218 | BMS_Battery Te mp | batterycellmaximumtemperature | R | 0.1℃ | — | — | tlx:bms_cell_max_temp, storage:bms_cell_max_temp | BMS cell max temperature |
| 3219 | BMS_Max Curr | Maximumchargingcurrent | R | 0.01 A | — | — | tlx:bms_max_charge_current, storage:bms_max_charge_current | BMS max charge current |
| 3220 | BMS_Max Dischr Curr | Maximumdischargecurrent | R | 0.01 A | — | — | tlx:bms_max_discharge_current, storage:bms_max_discharge_current | BMS max discharge current |
| 3221 | BMS_Cycle Cnt | BMSCycle Cnt | R | 1 | — | — | tlx:bms_cycle_count, storage:bms_cycle_count | BMS cycle count |
| 3222 | BMS_SOH | BMSSOH | R | 1 | — | — | tlx:bms_soh, storage:bms_soh | BMS SOH |
| 3223 | BMS_Charge Vol t Limit | Batterychargingvoltagelimitvalue | R | 0.01 V | — | — | tlx:bms_charge_volt_limit, storage:bms_charge_volt_limit | BMS charge voltage limit |
| 3224 | BMS_Discharge Volt Limit | Batterydischargevoltagelimitvalue | — | — | — | — | tlx:bms_discharge_volt_limit, storage:bms_discharge_volt_limit | BMS discharge voltage limit |
| 3225 | Bms Warn 3 | BMSWarn 3 | R | 1 | — | — | tlx:bms_warn3, storage:bms_warn3 | BMS warn 3 |
| 3226 | Bms Error 3 | BMSProtect 3 | R | 1 | — | — | tlx:bms_protect3, storage:bms_protect3 | BMS protect 3 |
| 3227 | Reserved | — | — | — | — | — | — | — |
| 3228 | Reserved | — | — | — | — | — | — | — |
| 3229 | Reserved | — | — | — | — | — | — | — |
| 3230 | BMSSingle Volt M ax | BMSBattery Single Volt Max | R | 0.001 V | — | — | tlx:bms_cell_volt_max, storage:bms_cell_volt_max | BMS cell voltage max |
| 3231 | BMSSingle Volt M in | BMSBattery Single Volt Min | R | 0.001 V | — | — | tlx:bms_cell_volt_min, storage:bms_cell_volt_min | BMS cell voltage min |
| 3232 | Bat Load Volt | Battery Load Volt | R | 0.01 V [0,650.00] | — | — | — | — |
| 3233 | — | — | — | — | — | — | — | — |
| 3234 | Debugdata 1 | Debugdata 1 | R | — | — | — | — | — |
| 3235 | Debugdata 2 | Debugdata 2 | R | — | — | — | — | — |
| 3236 | Debugdata 3 | Debugdata 3 | R | — | — | — | — | — |
| 3237 | Debugdata 4 | Debugdata 4 | R | — | — | — | — | — |
| 3238 | Debugdata 5 | Debugdata 5 | R | — | — | — | — | — |
| 3239 | Debugdata 6 | Debugdata 6 | R | — | — | — | — | — |
| 3240 | Debugdata 7 | Debugdata 7 | R | — | — | — | — | — |
| 3241 | Debugdata 8 | Debugdata 8 | R | — | — | — | — | — |
| 3242 | Debugdata 9 | Debugdata 9 | R | — | — | — | — | — |
| 3243 | Debugdata 10 | Debugdata 10 | R | — | — | — | — | — |
| 3244 | Debugdata 10 | Debugdata 10 | R | — | — | — | — | — |
| 3245 | Debugdata 12 | Debugdata 12 | R | — | — | — | — | — |
| 3246 | Debugdata 13 | Debugdata 13 | R | — | — | — | — | — |
| 3247 | Debugdata 14 | Debugdata 14 | R | — | — | — | — | — |
| 3248 | Debugdata 15 | Debugdata 15 | R | — | — | — | — | — |
| 3249 | Debugdata 16 | Debugdata 16 | R | — | — | — | — | — |

## TL-X/TL-XH Extended Input Registers (3250–3374)
Extended diagnostics and reserved registers for TL-XH hybrids.

**Applies to:** TL-X/TL-XH hybrids

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3250 | Pex 1 H | PVinverter 1 outputpower H | R | 0.1 W | — | — | — | — |
| 3251 | Pex 1 L | PVinverter 1 outputpower L | R | 0.1 W | — | — | — | — |
| 3252 | Pex 2 H | PVinverter 2 outputpower H | R | 0.1 W | — | — | — | — |
| 3253 | Pex 2 L | PVinverter 2 outputpower L | R | 0.1 W | — | — | — | — |
| 3254 | Eex 1 Today H | PVinverter 1 energy Today H | R | 0.1 k Wh | — | — | — | — |
| 3255 | Eex 1 Today L | PVinverter 1 energy Today L | R | 0.1 k Wh | — | — | — | — |
| 3256 | Eex 2 Today H | PVinverter 2 energy Today H | R | 0.1 k Wh | — | — | — | — |
| 3257 | Eex 2 Today L | PVinverter 2 energy Today L | R | 0.1 k Wh | — | — | — | — |
| 3258 | Eex 1 Total H | PVinverter 1 energy Total H | R | 0.1 k Wh | — | — | — | — |
| 3259 | Eex 1 Total L | PVinverter 1 energy Total L | R | 0.1 k Wh | — | — | — | — |
| 3260 | Eex 2 Total H | PVinverter 2 energy Total H | R | 0.1 k Wh | — | — | — | — |
| 3261 | Eex 2 Total L | PVinverter 2 energy Total L | R | 0.1 k Wh | — | — | — | — |
| 3262 | uw Bat No | batterypacknumber | R | BDC reports are updated every 15 minutes | — | — | — | — |
| 3263 | Bat Serial Num 1 | Batterypackserialnumber SN[0]SN[1] | R | BDC reports are updated every 15 minutes | — | — | — | — |
| 3264 | Bat Serial Num 2 | Batterypackserialnumber SN[2]SN[3] | R | — | — | — | — | — |
| 3265 | Bat Serial Num 3 | Batterypackserialnumber SN[4]SN[5] | R | — | — | — | — | — |
| 3266 | Bat Serial Num 4 | Batterypackserialnumber SN[6]SN[7] | R | — | — | — | — | — |
| 3267 | Bat Serial Num 5 | Batterypackserialnumber SN[8]SN[9] | R | — | — | — | — | — |
| 3268 | Bat Serial Num 6 | Batterypackserial number SN[10]SN[11] | R | — | — | — | — | — |
| 3269 | Bat Serial Num 7 | Batterypackserial number SN[12]SN[13] | R | — | — | — | — | — |
| 3270 | Bat Serial Num 8 | Batterypackserial number SN[14]SN[15] | R | — | — | — | — | — |
| 3271- 3279 | Reserve | Reserve | — | — | — | — | — | — |
| 3280 | b Clr Today Data Fl ag | Cleardaydataflag | R | Data of the current day that the server | — | — | — | — |

## Storage Input Registers (1000–1124)
Storage (MIX/SPA/SPH) core telemetry.

**Applies to:** Storage (MIX/SPA/SPH)

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000. | uw Sys Work Mode | — | Systemworkmode | 0 x 00:waiting module 0 x 01: Self-test mode, optional 0 x 02 : Reserved 0 x 03:Sys Fault module 0 x 04: Flash module | — | — | — | — |
| 1001. | Systemfaultword 0 | Systemfaultword 0 | — | Please refer to thefault description of Hybrid | — | — | — | — |
| 1002. | Systemfaultword 1 | Systemfaultword 1 | — | — | — | — | — | — |
| 1003. | Systemfaultword 2 | Systemfaultword 2 | — | — | — | — | — | — |
| 1004. | Systemfaultword 3 | Systemfaultword 3 | — | — | — | — | — | — |
| 1005. | Systemfaultword 4 | Systemfaultword 4 | — | — | — | — | — | — |
| 1006. | Systemfaultword 5 | Systemfaultword 5 | — | — | — | — | — | — |
| 1007. | Systemfaultword 6 | Systemfaultword 6 | — | — | — | — | — | — |
| 1008. | Systemfaultword 7 | Systemfaultword 7 | — | — | — | — | — | — |
| 1009. | Pdischarge 1 H | Dischargepower(high) | — | 0.1 W | — | — | storage:discharge_power | Battery discharge power, Discharge Power |
| 1010. | Pdischarge 1 L | Dischargepower(low) | — | 0.1 W | — | — | — | — |
| 1011. | Pcharge 1 H | Chargepower(high) | — | 0.1 W | — | — | storage:charge_power | Battery charge power, Charge Power |
| 1012. | Pcharge 1 L | Chargepower(low) | — | 0.1 W | — | — | — | — |
| 1013. | Vbat | Batteryvoltage | — | 0.1 V | — | — | — | — |
| 1014. | SOC | Stateofcharge Capacity | 0-100 | 1% lith/leadacid | — | — | storage:soc | SOC |
| 1015. | Pactouser R H | ACpowertouser H | — | 0.1 w | — | — | — | — |
| 1016. | Pactouser R L | ACpowertouser L | — | 0.1 w | — | — | — | — |
| 1017. | Pactouser S H | Pactouser S H | — | 0.1 w | — | — | — | — |
| 1018. | Pactouser S L | Pactouser S L | — | 0.1 w | — | — | — | — |
| 1019. | Pactouser T H | Pactouser T H | — | 0.1 w | — | — | — | — |
| 1020. | Pactouser T L | Pactouser T H | — | 0.1 w | — | — | — | — |
| 1021. | Pactouser Total H | ACpowertousertotal H | — | 0.1 w | — | — | storage:pac_to_user_total | AC to user total |
| 1022. | Pactouser Total L | ACpowertousertotal L | — | 0.1 w | — | — | — | — |
| 1023. | Pactogrid R H | ACpowertogrid H | — | 0.1 w Ac output | — | — | — | — |
| 1024. | Pactogrid R L | ACpowertogrid L | — | 0.1 w | — | — | — | — |
| 1025. | Pactogrid S H | — | — | 0.1 w | — | — | — | — |
| 1026. | Pactogrid S L | — | — | 0.1 w | — | — | — | — |
| 1027. | — | Pactogrid TH | — | — | — | 0.1 w | — | — |
| 1028. | — | Pactogrid TL | — | — | — | 0.1 w | — | — |
| 1029. | — | Pactogridtotal H | — | ACpowertogridtotal H | — | 0.1 w | storage:pac_to_grid_total | AC to grid total |
| 1030. | — | Pactogridtotal L | — | ACpowertogridtotal L | — | 0.1 w | — | — |
| 1031. | — | PLocal Load R H | — | INVpowertolocalload H | — | 0.1 w | — | — |
| 1032. | — | PLocal Load R L | — | INVpowertolocalload L | — | 0.1 w | — | — |
| 1033. | — | PLocal Load S H | — | — | — | 0.1 w | — | — |
| 1034. | — | PLocal Load S L | — | — | — | 0.1 w | — | — |
| 1035. | — | PLocal Load T H | — | — | — | 0.1 w | — | — |
| 1036. | — | PLocal Load T L | — | — | — | 0.1 w | — | — |
| 1037. | — | PLocal Loadtotal H | — | INVpowertolocalloadtotal H | — | 0.1 w | — | — |
| 1038. | — | PLocal Loadtotal L | — | INV power to local load total L | — | 0.1 w | — | — |
| 1039. | — | IP 2 MTemperature | — | RECTemperature | — | 0.1℃ | — | — |
| 1040. | — | B 2 attery Temperature | — | Battery Temperature | — | 0.1℃ | — | — |
| 1041. | — | SPDSPStatus | — | SPstate | — | — | — | — |
| 1042. | — | SPBus Volt | — | SPBUS 2 Volt | — | 0.1 V | — | — |
| 1043 | — | — | — | — | — | — | — | — |
| 1044. | Etouser_today H | — | Energytousertodayhigh | — | 0.1 k Wh | — | storage:energy_to_user_today | Energy To User (Today) |
| 1045. | Etouser_today L | — | Energytousertodaylow | — | 0.1 k Wh | — | — | — |
| 1046. | Etouser_total H | — | Energytousertotalhigh | — | 0.1 k Wh | — | storage:energy_to_user_total | Energy To User (Total) |
| 1047. | Etouser_total L | — | Energytousertotalhigh | — | 0.1 k Wh | — | — | — |
| 1048. | Etogrid_today H | — | Energytogridtodayhigh | — | 0.1 k Wh | — | storage:energy_to_grid_today | Energy To Grid (Today) |
| 1049. | Etogrid_today L | — | Energytogridtodaylow | — | 0.1 k Wh | — | — | — |
| 1050. | Etogrid_total H | — | Energytogridtotalhigh | — | 0.1 k Wh | — | storage:energy_to_grid_total | Energy To Grid (Total) |
| 1051. | Etogrid_total L | — | Energytogridtotalhigh | — | 0.1 k Wh | — | — | — |
| 1052. | Edischarge 1_toda y H | — | Dischargeenergy1today | — | 0.1 k Wh | — | storage:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 1053. | Edischarge 1_toda y L | — | Dischargeenergy1today | — | 0.1 k Wh | — | — | — |
| 1054. | Edischarge 1_total H | — | Totaldischargeenergy1(high) | — | 0.1 k Wh | — | storage:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 1055. | Edischarge 1_total L | — | Totaldischargeenergy1(low) | — | 0.1 k Wh | — | — | — |
| 1056. | Echarge 1_today H | — | Charge1energytoday | — | 0.1 k Wh | — | storage:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 1057. | Echarge 1_today L | — | Charge1energytoday | — | 0.1 k Wh | — | — | — |
| 1058. | Echarge 1_total H | — | Charge1energytotal | — | 0.1 k Wh | — | storage:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 1059. | Echarge 1_total L | — | Charge1energytotal | — | 0.1 k Wh | — | — | — |
| 1060 | — | — | . ELocalLoad_Today H | — | — | Localloadenergytoday | — | — |
| 1061 | — | — | . ELocalLoad_Today L | — | — | Localloadenergytoday | — | — |
| 1062 | — | — | . ELocalLoad_Total H | — | — | Localloadenergytotal | — | — |
| 1063 | — | — | . ELocalLoad_Total L | — | — | Localloadenergytotal | — | — |
| 1064 | — | — | . dwExportLimitAp parentPower | — | — | Export Limit Apparent Power H | — | — |
| 1065 | — | — | . dwExportLimitAp parentPower | — | — | Export Limit Apparent Power L | — | — |
| 1066 | — | — | . / | — | — | / | — | — |
| 1067 | — | — | . EPSFac | — | — | UPSfrequency | — | — |
| 1068 | — | — | . EPSVac1 | — | — | UPSphase Routputvoltage | — | — |
| 1069 | — | — | . EPSIac1 | — | — | UPSphase Routputcurrent | — | — |
| 1070 | — | — | . EPSPac1H | — | — | UPSphase Routputpower(H) | — | — |
| 1071 | — | — | . EPSPac1L | — | — | UPSphase Routputpower(L) | — | — |
| 1072 | — | — | . EPSVac2 | — | — | UPSphase Soutputvoltage | — | — |
| 1073 | — | — | . EPSIac2 | — | — | UPSphase Soutputcurrent | — | — |
| 1074 | — | — | . EPSPac2H | — | — | UPSphase Soutputpower(H) | — | — |
| 1075 | — | — | . EPSPac2L | — | — | UPSphase Soutputpower(L) | — | — |
| 1076 | — | — | . EPSVac3 | — | — | UPSphase Toutputvoltage | — | — |
| 1077 | — | — | . EPSIac3 | — | — | UPSphase Toutputcurrent | — | — |
| 1078 | — | — | . EPSPac3H | — | — | UPSphase Toutputpower(H) | — | — |
| 1079 | — | — | . EPSPac3L | — | — | UPSphase Toutputpower(L) | — | — |
| 1080 | — | — | . Loadpercent | — | — | Loadpercentof UPSouput | — | — |
| 1081 | — | — | . PF | — | — | Powerfactor | — | — |
| 1082. | — | — | — | BMS_Status Old | — | Status Oldfrom BMS | — | — |
| 1083. | — | — | — | BMS_Status | — | Statusfrom BMS | — | — |
| 1084. | — | — | — | BMS_Error Old | — | Errorinfo Oldfrom BMS | — | — |
| 1085. | — | — | — | BMS_Error | — | Errorinfomationfrom BMS | — | — |
| 1086. | — | — | — | BMS_SOC | — | SOCfrom BMS | — | — |
| 1087. | — | — | — | BMS_Battery Vol t | — | Batteryvoltagefrom BMS | — | — |
| 1088. | — | — | — | BMS_Battery Cur r | — | Batterycurrentfrom BMS | — | — |
| 1089. | — | — | — | BMS_Battery Te mp | — | Batterytemperaturefrom BMS | — | — |
| 1090. | BMS_Max Curr | Max. charge/discharge current from BMS(pylon) | — | — | — | — | — | — |
| 1091. | BMS_Gauge RM | Gauge RMfrom BMS | — | — | — | — | — | — |
| 1092. | BMS_Gauge FCC | Gauge FCCfrom BMS | — | — | — | — | — | — |
| 1093. | BMS_FW | — | — | — | — | — | — | — |
| 1094. | BMS_Delta Volt | Delta Vfrom BMS | — | — | — | — | — | — |
| 1095. | BMS_Cycle Cnt | Cycle Countfrom BMS | — | — | — | — | — | — |
| 1096. | BMS_SOH | SOHfrom BMS | — | — | — | — | — | — |
| 1097. | BMS_Constant V olt | CVvoltagefrom BMS | — | — | — | — | — | — |
| 1098. | BMS_Warn Info O ld | Warninginfooldfrom BMS | — | — | — | — | — | — |
| 1099. | BMS_Warn Info | Warninginfofrom BMS | — | — | — | — | — | — |
| 1100. | BMS_Gauge ICCu rr | Gauge ICcurrentfrom BMS | — | — | — | — | — | — |
| 1101. | BMS_MCUVersi on | MCUSoftwareversionfrom BMS | — | — | — | — | — | — |
| 1102. | BMS_Gauge Vers ion | Gauge Versionfrom BMS | — | — | — | — | — | — |
| 1103. | BMS_w Gauge FR Version_L | Gauge FRVersion L 16 from BMS | — | — | — | — | — | — |
| 1104. | BMS_w Gauge FR Version_H | Gauge FRVersion H 16 from BMS | — | — | — | — | — | — |
| 1105. | BMS_BMSInfo | BMSInformationfrom BMS | — | — | — | — | — | — |
| 1106. | BMS_Pack Info | Pack Informationfrom BMS | — | — | — | — | — | — |
| 1107. | BMS_Using Cap | Using Capfrom BMS | — | — | — | — | — | — |
| 1108. | uw Max Cell Volt | Maximumsinglebatteryvoltage | — | 0.001 V | — | — | — | — |
| 1109. | uw Min Cell Volt | Lowestsinglebatteryvoltage | — | 0.001 V | — | — | — | — |
| 1110. | b Module Num | Batteryparallelnumber | — | 1 | — | — | — | — |
| 1111. | — | Numberofbatteries | — | 1 | — | — | — | — |
| 1112. | uw Max Volt Cell N o | Max Volt Cell No | — | 1 | — | — | — | — |
| 1113. | uw Min Volt Cell N o | Min Volt Cell No | — | 1 | — | — | — | — |
| 1114. | uw Max Tempr Ce ll_10 T | Max Tempr Cell_10 T | — | 0.1℃ | — | — | — | — |
| 1115. | uw Min Tempr Cel l_10 T | Min Tempr Cell_10 T | — | 0.1℃ | — | — | — | — |
| 1116. | uw Max Tempr Ce ll No | Max Volt Tempr Cell No | — | 1 | — | — | — | — |
| 1117. | uw Min Tempr Cel | Min Volt Tempr Cell No | — | 1 | — | — | — | — |
| 1118. | Protectpack ID | Faulty Battery Address | — | 1 | — | — | — | — |
| 1119. | Max SOC | Parallelmaximum SOC | — | 1% | — | — | — | — |
| 1120. | Min SOC | Parallelminimum SOC | — | 1% | — | — | — | — |
| 1121. | BMS_Error 2 | Battery Protection 2 | — | - | CAN ID : 0 x 323 Byte 4~5 | — | — | — |
| 1122. | BMS_Error 3 | Battery Protection 3 | — | - | CAN ID : 0 x 323 Byte 6 | — | — | — |
| 1123. | BMS_Warn Info 2 | Battery Warn 2 | — | - | CAN ID : 0 x 323 Byte 7 | — | — | — |
| 1124 | ACCharge Energy Today H | ACCharge Energytoday | kwh | — | Energytoday | — | — | — |

## Storage Input Registers (1125–1249)
Additional SPA/SPH telemetry (e.g., DRMS, schedules).

**Applies to:** Storage SPA/SPH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1125. | ACCharge Energy Today L | ACCharge Energytoday | kwh | — | — | — | — | — |
| 1126. | A 1 CCharge Energy Total H | — | — | — | Energytotal | — | — | — |
| 1127. | ACCharge Energy Total L | — | — | — | — | — | — | — |
| 1128. | AC Charge Power H | ACCharge Power | W | — | — | — | — | — |
| 1129. | AC Charge Power L | ACCharge Power | w | — | — | — | — | — |
| 1130. | 70% INV Power adjust | uw Grid Power_70_Adj EE_SP | W | — | — | — | — | — |
| 1131. | Extra AC Power to grid_H | Extrainverte ACPowertogrid High | ForSPA connect inverter | — | SPAused | — | — | — |
| 1132. | Extra AC Power to grid_L | Extrainverte ACPowertogrid Low | — | — | SPAused | — | — | — |
| 1133. | Eextra_today H | Extrainverter Power TOUser_Extra today(high) | R | 0.1 k Wh | SPA used | — | — | — |
| 1134. | Eextra_today L | Extrainverter Power TOUser_Extra today(low) | R | 0.1 k Wh | SPA used | — | — | — |
| 1135. | Eextra_total H | Extrainverter Power TOUser_Extra total(high) | — | 0.1 k Wh | SPA used | — | — | — |
| 1136. | Eextra_total L | Extrainverter Power TOUser_Extra total(low) | — | 0.1 k Wh | SPA used | — | — | — |
| 1137. | Esystem_today H | Systemelectricenergytoday H | — | 0.1 k Wh | SPA used System electric energytoday H | — | — | — |
| 1138. | Esystem_ today L | Systemelectricenergytoday L | — | 0.1 k Wh SPA used System electric energytoday L | — | — | — | — |
| 1139. | Esystem_total H | Systemelectricenergytotal H | — | 0.1 k Wh SPA used System electric energytotal H | — | — | — | — |
| 1140. | Esystem_total L | Systemelectricenergytotal L | — | 0.1 k Wh SPA used System electric energytotal L | — | — | — | — |
| 1141. | Eself_today H | selfelectricenergytoday H | — | 0.1 k Wh self electric energytoday H | — | — | — | — |
| 1142. | Eself_today L | selfelectricenergytoday L | — | 0.1 k Wh self electric energytoday L | — | — | — | — |
| 1143. | Eself_total H | selfelectricenergytotal H | — | 0.1 k Wh self electric energytotal H | — | — | — | — |
| 1144. | Eself_total L | selfelectricenergytotal L | — | 0.1 k Wh self electric energytotal L | — | — | — | — |
| 1145. | PSystem H | Systempower H | — | 0.1 w Systempower H | — | — | — | — |
| 1146. | PSystem L | Systempower L | — | 0.1 w Systempower L | — | — | — | — |
| 1147. | PSelf H | selfpower H | — | 0.1 w selfpower H | — | — | — | — |
| 1148. | PSelf L | selfpower L | — | 0.1 w selfpower L | — | — | — | — |
| 1149. | EPVAll_Today H | PVelectricenergytoday H | — | — | — | — | — | — |
| 1150. | EPVAll_Today L | PVelectricenergytoday L | — | — | — | — | — | — |
| 1151. | Ac Discharge Pack Sn | Discharge power pack serial number | R | / | — | — | — | — |
| 1152. | Accdischarge power_H | Cumulative discharge power high 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1153. | Accdischarge power_L | Cumulative discharge power low 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1154. | Acc Charge Pack Sn | chargepowerpackserialnumber | R | / | — | — | — | — |
| 1155. | Acc Charge power_H | Cumulative charge power high 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1156. | Acc Charge power_L | Cumulative charge power low 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1157. | First Batt Fault Sn | First Batt Fault Sn | R | / | — | — | — | — |
| 1158. | Second Batt Fault Sn | Second Batt Fault Sn | R | / | — | — | — | — |
| 1159. | Third Batt Fault Sn | Third Batt Fault Sn | R | / | — | — | — | — |
| 1160. | Fourth Batt Fault Sn | Fourth Batt Fault Sn | R | / | — | — | — | — |
| 1161. | Batteryhistory faultcode 1 | Batteryhistoryfaultcode 1 | R | / | — | — | — | — |
| 1162. | Batteryhistory faultcode 2 | Batteryhistoryfaultcode 2 | R | / | — | — | — | — |
| 1163. | Batteryhistory faultcode 3 | Batteryhistoryfaultcode 3 | R | / | — | — | — | — |
| 1164. | Batteryhistory faultcode 4 | Batteryhistoryfaultcode 4 | R | / | — | — | — | — |
| 1165. | Batteryhistory faultcode 5 | Batteryhistoryfaultcode 5 | R | / | — | — | — | — |
| 1166. | Batteryhistory faultcode 6 | Batteryhistoryfaultcode 6 | R | / | — | — | — | — |
| 1167. | Batteryhistory faultcode 7 | Batteryhistoryfaultcode 7 | R | / | — | — | — | — |
| 1168. | Batteryhistory faultcode 8 | Batteryhistoryfaultcode 8 | R | / | — | — | — | — |
| 1169. | Number of battery codes | Number of battery codes PACK number + BIC forward and reversecodes | R | / | — | — | — | — |
| 1170. | — | — | — | — | — | — | — | — |
| 1199 | New EPower Calc Flag | Intelligent reading is used to identify software compatibility features | — | 0 : Old energy calculation; 1 : new energy calculation | — | — | — | — |
| 1200 | Max Cell Volt | Maximumcellvoltage | R | 0.001 V | — | — | — | — |
| 1201 | Min Cell Volt | Minimumcellvoltage | R | 0.001 V | — | — | — | — |
| 1202 | Module Num | Numberof Batterymodules | R | / | — | — | — | — |
| 1203 | Total Cell Num | Totalnumberofcells | R | / | — | — | — | — |
| 1204 | Max Volt Cell No | Max Volt Cell No | R | / | — | — | — | — |
| 1205 | Min Volt Cell No | Min Volt Cell No | R | / | — | — | — | — |
| 1206 | Max Tempr Cell_ 10 T | Max Tempr Cell_10 T | R | 0.1℃ | — | — | — | — |
| 1207 | Min Tempr Cell_1 0 T | Min Tempr Cell_10 T | R | 0.1℃ | — | — | — | — |
| 1208 | Max Tempr Cell N o | Max Tempr Cell No | R | / | — | — | — | — |
| 1209 | Min Tempr Cell N o | Min Tempr Cell No | R | / | — | — | — | — |
| 1210 | Protect Pack ID | Fault Pack ID | R | / | — | — | — | — |
| 1211 | Max SOC | Parallelmaximum SOC | R | 1% | — | — | — | — |
| 1212 | Min SOC | Parallelminimum SOC | R | 1% | — | — | — | — |
| 1213 | Bat Protect 1 Add | Bat Protect 1 Add | R | / | — | — | — | — |
| 1214 | Bat Protect 2 Add | Bat Protect 2 Add | R | / | — | — | — | — |
| 1215 | Bat Warn 1 Add | Bat Warn 1 Add | R | / | — | — | — | — |
| 1216 | BMS_Highest Sof t Version | BMS_Highest Soft Version | R | / | — | — | — | — |
| 1217 | BMS_Hardware Version | BMS_Hardware Version | R | / | — | — | — | — |
| 1218 | BMS_Request Ty pe | BMS_Request Type | R | / | — | — | — | — |
| 1248 | b Key Aging Test O k Flag | Success sign of key detection beforeaging | — | 1:Finishedtest 0 : test not completed | — | — | — | — |
| 1249. | / | / | / | / reversed | — | — | — | — |

## Storage Input Registers (2000–2124)
SPA-specific grid interaction telemetry.

**Applies to:** Storage SPA

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2000 | — | Inverter Status | — | — | — | Inverterrunstate | — | — |
| 2035 | — | Pac H | — | — | — | Outputpower(high) | — | — |
| 2036 | — | Pac L | — | — | — | Outputpower(low) | — | — |
| 2037 | — | Fac | — | — | — | Gridfrequency | — | — |
| 2038 | — | Vac 1 | — | — | — | Three/singlephasegridvoltage | — | — |
| 2039 | — | Iac 1 | — | — | — | Three/singlephasegridoutputcurrent | — | — |
| 2040 | — | Pac 1 H | — | — | — | Three/single phase grid output watt VA(high) | — | — |
| 2041 | — | Pac 1 L | — | — | — | Three/single phase grid output watt VA(low) | — | — |
| 2053 | — | Eactoday H | — | — | — | Todaygenerateenergy(high) | — | — |
| 2054 | — | Eactoday L | — | — | — | Todaygenerateenergy(low) | — | — |
| 2055 | Eactotal H | Totalgenerateenergy(high) | — | 0.1 k WH SPA | — | — | — | — |
| 2056 | Eactotal L | Totalgenerateenergy(low) | — | 0.1 k WH SPA | — | — | — | — |
| 2057 | Timetotal H | Worktimetotal(high) | — | 0.5 s SPA | — | — | — | — |
| 2058 | Timetotal L | Worktimetotal(low) | — | 0.5 s SPA | — | — | — | — |
| 2093 | Temp 1 | Invertertemperature | — | 0.1 C SPA | — | — | — | — |
| 2094 | Temp 2 | Theinside IPMininverter Temperature | — | 0.1 C SPA | — | — | — | — |
| 2095 | Temp 3 | Boosttemperature | — | 0.1 C SPA | — | — | — | — |
| 2096 | Temp 4 | — | — | reserved | — | — | — | — |
| 2097 | uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 2098 | PBus Voltage | PBusinside Voltage | — | 0.1 V SPA | — | — | — | — |
| 2099 | NBus Voltage | NBusinside Voltage | — | 0.1 V SPA | — | — | — | — |
| 2100 | Remote Ctrl En | / | 0.LoadFirst 1.BatFirst 2.Grid | / Remote setup enable | — | — | — | — |
| 2101 | Remote Ctrl Pow er | / | — | / Remotely setpower | — | — | — | — |
| 2102 | Extra AC Power to grid_H | Extrainverte ACPowertogrid High | ForSPA connect inverter | SPAused | — | — | — | — |
| 2103 | Extra AC Power to grid_L | Extrainverte ACPowertogrid Low | — | SPAused | — | — | — | — |
| 2104 | Eextra_today H | Extrainverter Power TOUser_Extra today(high) | R | 0.1 k Wh SPA used | — | — | — | — |
| 2105 | Eextra_today L | Extrainverter Power TOUser_Extra today(low) | R | 0.1 k Wh SPA used | — | — | — | — |
| 2106 | Eextra_total H | Extrainverter Power TOUser_Extratotal(high) | — | 0.1 k Wh SPA used | — | — | — | — |
| 2107 | Eextra_total L | Extrainverter Power TOUser_Extra total(low) | — | 0.1 k Wh SPA used | — | — | — | — |
| 2108 | Esystem_today H | Systemelectricenergytoday H | — | 0.1 k Wh SPA used System electric energy today H | — | — | — | — |
| 2109 | Esystem_ today L | Systemelectricenergytoday L | — | 0.1 k Wh SPA used System electric energy today L | — | — | — | — |
| 2110 | Esystem_total H | Systemelectricenergytotal H | — | 0.1 k Wh SPA used System | — | — | — | — |
| 2111 | Esystem_total L | Systemelectricenergytotal L | — | 0.1 k Wh | SPA used System electric energy total L | — | — | — |
| 2112 | EACharge_Today _H | ACChargeenergytoday | — | 0.1 kwh | Storage Power | — | — | — |
| 2113 | EACharge_Today _L | ACChargeenergytoday | — | 0.1 kwh | Storage Power | — | — | — |
| 2114 | EACharge_Total _H | ACChargeenergytotal | — | 0.1 kwh | Storage Power | — | — | — |
| 2115 | EACharge_Total _L | ACChargeenergytotal | — | 0.1 kwh | Storage Power | — | — | — |
| 2116 | AC charge Power_H | Gridpowertolocalload | — | 0.1 kwh | Storage Power | — | — | — |
| 2117 | AC charge Power_L | Gridpowertolocalload | — | 0.1 kwh | Storage Power | — | — | — |
| 2118 | Priority | 0:Load First 1:Battery First 2:Grid First | — | — | Storage Power | — | — | — |
| 2119 | Battery Type | 0:Lead-acid 1:Lithiumbattery | — | — | Storage Power | — | — | — |
| 2120 | Auto Proofread C MD | Agingmode | — | — | Storage Power | — | — | — |
| 2124. | reserved | — | — | — | reserved | — | — | — |

## Storage TL-XH Input Registers (3041–3231)
BDC telemetry (battery module data) for TL-XH hybrids.

**Applies to:** Storage TL-XH

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3041 | Ptousertotal H | Totalforwardpower | — | 0.1 W Total forward power | — | — | storage:power_to_user | Power to user |
| 3042 | Ptousertotal L | — | — | — | — | — | — | — |
| 3043 | Ptogridtotal H | Totalreversepower | — | 0.1 W Totalreverse power | — | — | storage:power_to_grid | Power to grid |
| 3044 | Ptogridtotal L | — | — | — | — | — | — | — |
| 3045 | Ptoloadtotal H | Totalloadpower | — | 0.1 W Total load power | — | — | storage:power_user_load | Power user load |
| 3046 | Ptoloadtotal L | — | — | — | — | — | — | — |
| 3047 | Timetotal H | Worktimetotal | — | 0.5 s | — | — | — | — |
| 3048 | Timetotal L | — | — | — | — | — | — | — |
| 3049 | Eactoday H | Todaygenerateenergy | — | 0.1 k Wh Today generate energy | — | — | — | — |
| 3050 | Eactoday L | — | — | — | — | — | — | — |
| 3051 | Eactotal H | Totalgenerateenergy | — | 0.1 k Wh Total generate | — | — | — | — |
| 3052 | Eactotal L | — | — | — | — | — | — | — |
| 3053 | Epv_total H | PVenergytotal | — | 0.1 k Wh PVenergy total | — | — | — | — |
| 3054 | Epv_total L | — | — | — | — | — | — | — |
| 3055 | Epv 1_today H | PV 1 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3056 | Epv 1_today L | — | — | — | — | — | — | — |
| 3057 | Epv 1_total H | PV 1 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3058 | Epv 1_total L | — | — | — | — | — | — | — |
| 3059 | Epv 2_today H | PV 2 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3060 | Epv 2_today L | — | — | — | — | — | — | — |
| 3061 | Epv 2_total H | PV 2 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3062 | Epv 2_total L | — | — | — | — | — | — | — |
| 3063 | Epv 3_today H | PV 3 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3064 | Epv 3_today L | — | — | — | — | — | — | — |
| 3065 | Epv 3_total H | PV 3 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3066 | Epv 3_total L | — | — | — | — | — | — | — |
| 3067 | Etouser_today H | Todayenergytouser | — | 0.1 k Wh Todayenergy touser | — | — | storage:energy_to_user_today | Energy To User (Today) |
| 3068 | Etouser_today L | — | — | — | — | — | — | — |
| 3069 | Etouser_total H | Totalenergytouser | — | 0.1 k Wh Totalenergy touser | — | — | storage:energy_to_user_total | Energy To User (Total) |
| 3070 | Etouser_total L | — | — | — | — | — | — | — |
| 3071 | Etogrid_today H | Todayenergytogrid | — | 0.1 k Wh Todayenergy togrid | — | — | storage:energy_to_grid_today | Energy To Grid (Today) |
| 3072 | Etogrid_today L | — | — | — | — | — | — | — |
| 3073 | Etogrid_total H | Totalenergytogrid | — | 0.1 k Wh Totalenergy togrid | — | — | storage:energy_to_grid_total | Energy To Grid (Total) |
| 3074 | Etogrid_total L | — | — | — | — | — | — | — |
| 3075 | Eload_today H | Todayenergyofuserload | — | 0.1 k Wh Todayenergy ofuserload | — | — | — | — |
| 3076 | Eload_today L | — | — | — | — | — | — | — |
| 3077 | Eload_total H | Totalenergyofuserload | — | 0.1 k Wh Totalenergy ofuserload | — | — | — | — |
| 3078 | Eload_total L | — | — | — | — | — | — | — |
| 3079 | Epv 4_today H | PV 4 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3080 | Epv 4_today L | — | — | — | — | — | — | — |
| 3081 | Epv 4_total H | PV 4 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3082 | Epv 4_total L | — | — | — | — | — | — | — |
| 3083 | Epv_today H | PVenergytoday | — | 0.1 k Wh | — | — | — | — |
| 3084 | Epv_today L | — | — | — | — | — | — | — |
| 3085 | Reserved | — | — | — | — | — | — | — |
| 3086 | Derating Mode | Derating Mode | — | 0:c NOTDerate 1:c PVHigh Der ate 2: c Power Con stant Derate 3: c Grid VHigh Derate 4:c Freq High D erate 5:c Dc Soure M ode Derate 6:c Inv Tempr D erate 7:c Active Pow er Order 8:c Load Speed Process 9:c Over Back by Time 10:c Internal T empr Derate 11:c Out Temp r Derate 12:c Line Impe Calc Derate 13: c Parallel A nti Backflow D erate 14:c Local Anti Backflow Dera te 15:c Bdc Load P ri Derate 16:c Chk CTErr Derate | — | — | — | — |
| 3087 | ISO | PVISOvalue | — | 1 KΩ | — | — | — | — |
| 3088 | DCI_R | RDCICurr | — | 0.1 m A | — | — | — | — |
| 3089 | DCI_S | SDCICurr | — | 0.1 m A | — | — | — | — |
| 3090 | DCI_T | TDCICurr | — | 0.1 m A | — | — | — | — |
| 3091 | GFCI | GFCICurr | — | 1 m A | — | — | — | — |
| 3092 | Bus Voltage | totalbusvoltage | — | 0.1 V | — | — | — | — |
| 3093 | Temp 1 | Invertertemperature | — | 0.1℃ | — | — | — | — |
| 3094 | Temp 2 | Theinside IPMininvertertemperature | — | 0.1℃ | — | — | — | — |
| 3095 | Temp 3 | Boosttemperature | — | 0.1℃ | — | — | — | — |
| 3096 | Temp 4 | Reserved | — | 0.1℃ | — | — | — | — |
| 3097 | Temp 5 | Commmunicationbroadtemperature | — | 0.1℃ | — | — | storage:comm_board_temperature | Comm board temperature |
| 3098 | PBus Voltage | PBusinside Voltage | — | 0.1 V | — | — | — | — |
| 3099 | NBus Voltage | NBusinside Voltage | — | 0.1 V | — | — | — | — |
| 3100 | IPF | Inverteroutput PFnow | — | 0-20000 | — | — | — | — |
| 3101 | Real OPPercent | Real Outputpower Percent | — | 1% 1~100 | — | — | — | — |
| 3102 | OPFullwatt H | Output Maxpower Limited | — | 0.1 W Output Maxpower Limited | — | — | — | — |
| 3103 | OPFullwatt L | — | — | — | — | — | — | — |
| 3104 | Standby Flag | Inverterstandbyflag | — | bitfield bit 0:turn off Order; bit 1:PVLow; bit 2:AC Volt/Freq outofscope; bit 3~bit 7 : Reserved | — | — | — | — |
| 3105 | Fault Maincode | Inverterfaultmaincode | — | — | — | — | — | — |
| 3106 | Warn Maincode | Inverter Warningmaincode | — | — | — | — | — | — |
| 3107 | Fault Subcode | Inverterfaultsubcode | — | bitfield | — | — | — | — |
| 3108 | Warn Subcode | Inverter Warningsubcode | — | bitfield | — | — | — | — |
| 3109 | — | — | — | bitfield | — | — | — | — |
| 3110 | — | — | — | bitfield | — | — | — | — |
| 3111 | uw Present FFTVa lue[CHANNEL_A ] | Present FFTValue[CHANNEL_A] | — | bitfield | — | — | storage:present_fft_a | Present FFT A |
| 3112 | b Afci Status | AFCIStatus | — | 0 : waiting state 1:self-check 2:Detection of arcing state 3:faultstate 4 : update state | — | — | — | — |
| 3113 | uw Strength[CHA NNEL_A] | AFCIStrength[CHANNEL_A] | — | — | — | — | — | — |
| 3114 | uw Self Check Val ue[CHANNEL_A] | AFCISelf Check[CHANNEL_A] | — | — | — | — | — | — |
| 3115 | inv start delay time | invstartdelaytime | — | 1 S invstartdelay time | — | — | storage:inv_start_delay | Inverter start delay |
| 3116 | Reserved | — | — | — | — | — | — | — |
| 3117 | Reserved | — | — | — | — | — | — | — |
| 3118 | BDC_On Off State | BDCconnectstate | — | 0:No BDC Connect 1:BDC 1 Connect 2:BDC 2 Connect 3:BDC 1+BDC 2 Connect | — | — | — | — |
| 3119 | Dry Contact State | Currentstatusof Dry Contact | — | Current status of Dry Contact 0:turnoff; 1:turnon; | — | — | — | — |
| 3120 | Reserved | — | — | — | — | — | — | — |
| 3121 | Pself H | self-usepower | — | 0.1 W | — | — | — | — |
| 3122 | Pself L | — | — | — | — | — | — | — |
| 3123 | Esys_today H | Systemenergytoday | — | 0.1 kwh | — | — | — | — |
| 3124 | Esys_today L | — | — | — | — | — | — | — |
| 3125 | Edischr_today H | Todaydischargeenergy | — | 0.1 k Wh Today discharge energy | — | — | storage:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 3126 | Edischr_today L | — | — | — | — | — | — | — |
| 3127 | Edischr_total H | Totaldischargeenergy | — | 0.1 k Wh Total discharge energy | — | — | storage:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 3128 | Edischr_total L | — | — | — | — | — | — | — |
| 3129 | Echr_today H | Chargeenergytoday | — | 0.1 k Wh Charge energytoday | — | — | storage:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 3130 | Echr_today L | — | — | — | — | — | — | — |
| 3131 | Echr_total H | Chargeenergytotal | — | 0.1 k Wh Charge energytotal | — | — | storage:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 3132 | Echr_total L | — | — | — | — | — | — | — |
| 3133 | Eacchr_today H | Todayenergyof ACcharge | — | 0.1 k Wh Todayenergy of ACcharge | — | — | — | — |
| 3134 | Eacchr_today L | — | — | — | — | — | — | — |
| 3135 | Eacchr_total H | Totalenergyof ACcharge | — | 0.1 k Wh Totalenergy of ACcharge | — | — | — | — |
| 3136 | Eacchr_total L | — | — | — | — | — | — | — |
| 3137 | Esys_total H | — | — | — | — | — | — | — |
| 3138 | Esys_total L | Totalenergyofsystemoutput\ | — | 0.1 k Wh | — | — | — | — |
| 3139 | Eself_today H | Todayenergyof Selfoutput | — | 0.1 k Wh | — | — | — | — |
| 3140 | Eself_today L | — | — | — | — | — | — | — |
| 3141 | Eself_total H | Totalenergyof Selfoutput | — | 0.1 kwh | — | — | — | — |
| 3142 | Eself_total L | — | — | — | — | — | — | — |
| 3143 | Reserved | — | — | — | — | — | — | — |
| 3144 | Priority | Word Mode | — | 0 Load First 1 Battery Firs t 2 Grid First | — | — | — | — |
| 3145 | EPSFac | UPSfrequency | — | 0.01 Hz | — | — | — | — |
| 3146 | EPSVac 1 | UPSphase Routputvoltage | — | 0.1 V | — | — | — | — |
| 3147 | EPSIac 1 | UPSphase Routputcurrent | — | 0.1 A | — | — | — | — |
| 3148 | EPSPac 1 H | UPSphase Routputpower | — | 0.1 VA | — | — | — | — |
| 3149 | EPSPac 1 L | — | — | — | — | — | — | — |
| 3150 | EPSVac 2 | UPSphase Soutputvoltage | — | 0.1 V | — | — | — | — |
| 3151 | EPSIac 2 | UPSphase Soutputcurrent | — | 0.1 A | — | — | — | — |
| 3152 | EPSPac 2 H | UPSphase Soutputpower | — | 0.1 VA | — | — | — | — |
| 3153 | EPSPac 2 L | — | — | — | — | — | — | — |
| 3154 | EPSVac 3 | UPSphase Toutputvoltage | — | 0.1 V | — | — | — | — |
| 3155 | EPSIac 3 | UPSphase Toutputcurrent | — | 0.1 A | — | — | — | — |
| 3156 | EPSPac 3 H | UPSphase Toutputpower | — | 0.1 VA | — | — | — | — |
| 3157 | EPSPac 3 L | — | — | — | — | — | — | — |
| 3158 | EPSPac H | UPSoutputpower | — | 0.1 VA | — | — | — | — |
| 3159 | EPSPac L | — | — | — | — | — | — | — |
| 3160 | Loadpercent | Loadpercentof UPSouput | — | 0.10% | — | — | — | — |
| 3161 | PF | Powerfactor | — | 0.1 | — | — | — | — |
| 3162 | DCV | DCvoltage | — | 1 m V | — | — | — | — |
| 3163 | Reserved | — | — | — | — | — | — | — |
| 3164 | New Bdc Flag | Whethertoparse BDCdataseparately | — | 0:Don'tneed 1:need | — | — | storage:bdc_new_flag | BDC present |
| 3165 | BDCDerating Mo de | BDCDerating Mode: 0:Normal,unrestricted 1:Standbyorfault 2:Maximumbatterycurrentlimit (discharge) 3:Batterydischarge Enable(Discharge) 4:Highbusdischargederating | — | — | — | — | — | — |
| 3166 | Sys State_Mode | Systemwork Stateandmode The upper 8 bitsindicatethemode; 0:Nochargeanddischarge; 1:charge; 2:Discharge; Thelower 8 bitsrepresentthestatus; 0:Standby Status; 1:Normal Status; 2:Fault Status 3:Flash Status; | — | BDC 1 | — | — | — | — |
| 3167 | Fault Code | Storgedevicefaultcode | — | — | — | — | — | — |
| 3168 | Warn Code | Storgedevicewarningcode | — | — | — | — | — | — |
| 3169 | Vbat | Batteryvoltage | — | 0.01 V | — | — | storage:battery_voltage | Battery voltage |
| 3170 | Ibat | Batterycurrent | — | 0.1 A | — | — | storage:battery_current | Battery current |
| 3171 | SOC | Stateofcharge Capacity | — | 1% | — | — | storage:soc | SOC |
| 3172 | Vbus 1 | Total BUSvoltage | — | 0.1 V | — | — | storage:vbus1_voltage | VBUS1 voltage |
| 3173 | Vbus 2 | Onthe BUSvoltage | — | 0.1 V | — | — | storage:vbus2_voltage | VBUS2 voltage |
| 3174 | Ibb | BUCK-BOOSTCurrent | — | 0.1 A | — | — | storage:buck_boost_current | Buck/boost current |
| 3175 | Illc | LLCCurrent | — | 0.1 A | — | — | storage:llc_current | LLC current |
| 3176 | Temp A | Temperture A | — | 0.1℃ | — | — | storage:battery_temperature_a | Battery temperature A |
| 3177 | Temp B | Temperture B | — | 0.1℃ | — | — | storage:battery_temperature_b | Battery temperature B |
| 3178 | Pdischr H | Dischargepower | — | 0.1 W | — | — | storage:discharge_power | Battery discharge power, Discharge Power |
| 3179 | Pdischr L | — | — | — | — | — | — | — |
| 3180 | Pchr H | Chargepower | — | 0.1 W | — | — | storage:charge_power | Battery charge power, Charge Power |
| 3181 | Pchr L | — | — | — | — | — | — | — |
| 3182 | Edischr_total H | Dischargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3183 | Edischr_total L | — | — | — | — | — | — | — |
| 3184 | Echr_total H | Chargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3185 | Echr_total L | — | — | — | — | — | — | — |
| 3186 | Reserved | Reserved | — | — | — | — | — | — |
| 3187 | BDC 1_Flag | BDCmark(chargeanddischarge, faultalarmcode) Bit 0:Charge En;BDCallowscharging Bit 1:Discharge En;BDCallows discharge Bit 2~7:Resvd;reserved Bit 8~11:Warn Sub Code;BDC sub-warningcode Bit 12~15:Fault Sub Code;BDC sub-errorcode | — | — | — | — | — | — |
| 3188 | Vbus 2 | Lower BUSvoltage | — | 0.1 V | — | — | — | — |
| 3189 | Bms Max Volt Cell No | Bms Max Volt Cell No | — | — | — | — | storage:bms_max_volt_cell_no | BMS max volt cell no |
| 3190 | Bms Min Volt Cell No | Bms Min Volt Cell No | — | — | — | — | storage:bms_min_volt_cell_no | BMS min volt cell no |
| 3191 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | storage:bms_avg_temp_a | BMS avg temp A |
| 3192 | Bms Max Cell Tem p | Bms Max Cell Temp | — | 0.1°C | — | — | storage:bms_max_cell_temp_a | BMS max cell temp A |
| 3193 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | 0.1°C | — | — | storage:bms_avg_temp_b | BMS avg temp B |
| 3194 | Bms Max Cell Tem p | Bms Max Cell Temp | — | — | — | — | storage:bms_max_cell_temp_b | BMS max cell temp B |
| 3195 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | storage:bms_avg_temp_c | BMS avg temp C |
| 3196 | Bms Max SOC | Bms Max SOC | — | 1% | — | — | storage:bms_max_soc | BMS max SOC |
| 3197 | Bms Min SOC | Bms Min SOC | — | 1% | — | — | storage:bms_min_soc | BMS min SOC |
| 3198 | Parallel Battery N um | Parallel Battery Num | — | — | — | — | storage:parallel_battery_num | — |
| 3199 | Bms Derate Reas on | Bms Derate Reason | — | — | — | — | storage:bms_derate_reason | BMS derate reason |
| 3200 | Bms Gauge FCC (Ah) | Bms Gauge FCC(Ah) | — | — | — | — | storage:bms_gauge_fcc_ah | BMS full charge capacity |
| 3201 | Bms Gauge RM (Ah) | Bms Gauge RM(Ah) | — | — | — | — | storage:bms_gauge_rm_ah | BMS remaining capacity |
| 3202 | Bms Error | BMSProtect 1 | — | — | — | — | storage:bms_protect1 | BMS protect 1 |
| 3203 | Bms Warn | BMSWarn 1 | — | — | — | — | storage:bms_warn1 | BMS warn 1 |
| 3204 | Bms Fault | BMSFault 1 | — | — | — | — | storage:bms_fault1 | BMS fault 1 |
| 3205 | Bms Fault 2 | BMSFault 2 | — | — | — | — | storage:bms_fault2 | BMS fault 2 |
| 3206 | Reserved | — | — | — | — | — | — | — |
| 3207 | Reserved | — | — | — | — | — | — | — |
| 3208 | Reserved | — | — | — | — | — | — | — |
| 3209 | Reserved | — | — | — | — | — | — | — |
| 3210 | Bat Iso Status | Battery ISOdetectionstatus | — | 0:Not detected 1:Detection completed | — | — | storage:bat_iso_status | — |
| 3211 | Batt Need Charge Request Flag | batteryworkrequest | — | bit 0:1: Prohibit chargin g,0: Allow the chargin g bit 1:1: Enable strong charge, 0: disable strong charge bit 2:1: Enable strong charge 2 0: disable strong charge | — | — | storage:batt_request_flags | — |
| 3212 | BMS_Status | batteryworkingstatus | R | 0:dormancy 1:Charge 2:Discharge 3:free 4:standby 5:Softstart 6:fault 7:update | — | — | storage:bms_status | BMS status |
| 3213 | Bms Error 2 | BMSProtect 2 | R | 1 | — | — | storage:bms_protect2 | BMS protect 2 |
| 3214 | Bms Warn 2 | BMSWarn 2 | R | 1 | — | — | storage:bms_warn2 | BMS warn 2 |
| 3215 | BMS_SOC | BMSSOC | R | 1% | — | — | storage:bms_soc | BMS SOC |
| 3216 | BMS_Battery Vol t | BMSBattery Volt | R | 0.01 V | — | — | storage:bms_battery_voltage | BMS battery voltage |
| 3217 | BMS_Battery Cur r | BMSBattery Curr | R | 0.01 A | — | — | storage:bms_battery_current | BMS battery current |
| 3218 | BMS_Battery Te mp | batterycellmaximumtemperature | R | 0.1℃ | — | — | storage:bms_cell_max_temp | BMS cell max temperature |
| 3219 | BMS_Max Curr | Maximumchargingcurrent | R | 0.01 A | — | — | storage:bms_max_charge_current | BMS max charge current |
| 3220 | BMS_Max Dischr Curr | Maximumdischargecurrent | R | 0.01 A | — | — | storage:bms_max_discharge_current | BMS max discharge current |
| 3221 | BMS_Cycle Cnt | BMSCycle Cnt | R | 1 | — | — | storage:bms_cycle_count | BMS cycle count |
| 3222 | BMS_SOH | BMSSOH | R | 1 | — | — | storage:bms_soh | BMS SOH |
| 3223 | BMS_Charge Vol t Limit | Batterychargingvoltagelimitvalue | R | 0.01 V | — | — | storage:bms_charge_volt_limit | BMS charge voltage limit |
| 3224 | BMS_Discharge Volt Limit | Batterydischargevoltagelimitvalue | — | — | — | — | storage:bms_discharge_volt_limit | BMS discharge voltage limit |
| 3225 | Bms Warn 3 | BMSWarn 3 | R | 1 | — | — | storage:bms_warn3 | BMS warn 3 |
| 3226 | Bms Error 3 | BMSProtect 3 | R | 1 | — | — | storage:bms_protect3 | BMS protect 3 |
| 3227 | Reserved | — | — | — | — | — | — | — |
| 3228 | Reserved | — | — | — | — | — | — | — |
| 3229 | Reserved | — | — | — | — | — | — | — |
| 3230 | BMSSingle Volt M ax | BMSBattery Single Volt Max | R | 0.001 V | — | — | storage:bms_cell_volt_max | BMS cell voltage max |
| 3231 | BMSSingle Volt M in | BMSBattery Single Volt Min | R | 0.001 V | — | — | storage:bms_cell_volt_min | BMS cell voltage min |

## Offgrid SPF Input Registers
Observed off-grid register map (from integration implementation).

**Applies to:** Offgrid SPF

| Register | Name | Description | Access | Range/Unit | Initial | Notes | Attributes | Sensors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3239-3 249 | Reserve | Reserve | R/W | — | — | — | — | — |
| 5000-5039 | — | 1 | — | Reference 3085 to 3124 foratotalof 40 registers Description | — | — | — | — |
| 5040-5079 | — | 2 | — | — | — | — | — | — |
| 5000+(N-1)*40--- 5039+(N-1)*40 | — | N | — | — | — | — | — | — |
| 0. | — | Inverter Status | Inverterrunstate | 0:waiting, 1:normal, 3:fault | — | — | offgrid:status_code | Status code |
| 1. | — | Ppv H | Inputpower(high) | 0.1 W | — | — | offgrid:input_1_voltage | Input 1 voltage, PV1 voltage |
| 2. | — | Ppv L | Inputpower(low) | 0.1 W | — | — | offgrid:input_2_voltage | Input 2 voltage, PV2 voltage |
| 3. | — | Vpv 1 | PV1voltage | 0.1 V | — | — | offgrid:input_1_power | Input 1 Wattage, PV1 charge power |
| 4. | — | PV 1 Curr | PV1inputcurrent | 0.1 A | — | — | — | — |
| 5. | — | Ppv 1 H | PV1inputpower(high) | 0.1 W | — | — | offgrid:input_2_power | Input 2 Wattage, PV2 charge power |
| 6. | — | Ppv 1 L | PV1inputpower(low) | 0.1 W | — | — | — | — |
| 7. | — | Vpv 2 | PV2voltage | 0.1 V | — | — | offgrid:input_1_amperage | Input 1 Amperage, PV1 buck current |
| 8. | — | PV 2 Curr | PV2inputcurrent | 0.1 A | — | — | offgrid:input_2_amperage | Input 2 Amperage, PV2 buck current |
| 9. | — | Ppv 2 H | PV2inputpower(high) | 0.1 W | — | — | offgrid:output_active_power | Output active power |
| 10. | — | Ppv 2 L | PV2inputpower(low) | 0.1 W | — | — | — | — |
| 11. | — | Vpv 3 | PV3voltage | 0.1 V | — | — | — | — |
| 12. | — | PV 3 Curr | PV3inputcurrent | 0.1 A | — | — | — | — |
| 13. | — | Ppv 3 H | PV3inputpower(high) | 0.1 W | — | — | offgrid:charge_power | Battery charge power, Charge Power |
| 14. | — | Ppv 3 L | PV3inputpower(low) | 0.1 W | — | — | — | — |
| 15. | — | Vpv 4 | PV4voltage | 0.1 V | — | — | — | — |
| 16. | — | PV 4 Curr | PV4inputcurrent | 0.1 A | — | — | — | — |
| 17. | — | Ppv 4 H | PV4inputpower(high) | 0.1 W | — | — | offgrid:battery_voltage | Battery voltage |
| 18. | — | Ppv 4 L | PV4inputpower(low) | 0.1 W | — | — | offgrid:soc | SOC |
| 19. | — | Vpv 5 | PV5voltage | 0.1 V | — | — | offgrid:bus_voltage | Bus voltage |
| 20. | — | PV 5 Curr | PV5inputcurrent | 0.1 A | — | — | offgrid:grid_voltage | Grid voltage |
| 21. | — | Ppv 5 H | PV5inputpower(high) | 0.1 W | — | — | offgrid:grid_frequency | AC frequency, Grid frequency |
| 22. | — | Ppv 5 L | PV5inputpower(low) | 0.1 W | — | — | offgrid:output_1_voltage | Output 1 voltage, Output voltage |
| 23. | — | Vpv 6 | PV6voltage | 0.1 V | — | — | offgrid:output_frequency | Output frequency |
| 24. | — | PV 6 Curr | PV6inputcurrent | 0.1 A | — | — | offgrid:output_dc_voltage | Output DC voltage |
| 25. | Ppv 6 H | PV 6 inputpower(high) | — | 0.1 W | — | — | offgrid:inverter_temperature | Temperature |
| 26. | Ppv 6 L | PV 6 inputpower(low) | — | 0.1 W | — | — | offgrid:dc_dc_temperature | DC-DC temperature |
| 27. | Vpv 7 | PV 7 voltage | — | 0.1 V | — | — | offgrid:load_percent | Inverter load |
| 28. | PV 7 Curr | PV 7 inputcurrent | — | 0.1 A | — | — | offgrid:battery_port_voltage | Battery port voltage |
| 29. | Ppv 7 H | PV 7 inputpower(high) | — | 0.1 W | — | — | offgrid:battery_bus_voltage | Battery bus voltage |
| 30. | Ppv 7 L | PV 7 inputpower(low) | — | 0.1 W | — | — | offgrid:operation_hours | Running hours |
| 31. | Vpv 8 | PV 8 voltage | — | 0.1 V | — | — | — | — |
| 32. | PV 8 Curr | PV 8 inputcurrent | — | 0.1 A | — | — | — | — |
| 33. | Ppv 8 H | PV 8 inputpower(high) | — | 0.1 W | — | — | — | — |
| 34. | Ppv 8 L | PV 8 inputpower(low) | — | 0.1 W | — | — | offgrid:output_1_amperage | Output 1 Amperage, Output amperage |
| 35. | Pac H | Outputpower(high) | — | 0.1 W | — | — | — | — |
| 36. | Pac L | Outputpower(low) | — | 0.1 W | — | — | — | — |
| 37. | Fac | Gridfrequency | — | 0.01 Hz | — | — | — | — |
| 38. | Vac 1 | Three/singlephasegridvoltage | — | 0.1 V | — | — | — | — |
| 39. | Iac 1 | Three/singlephasegridoutputcurrent | — | 0.1 A | — | — | — | — |
| 40. | Pac 1 H | Three/single phase grid output watt VA(high) | — | 0.1 VA | — | — | — | — |
| 41. | Pac 1 L | Three/single phase grid output watt VA(low) | — | 0.1 VA | — | — | — | — |
| 42. | Vac 2 | Threephasegridvoltage | — | 0.1 V | — | — | offgrid:fault_code | Fault code |
| 43. | Iac 2 | Threephasegridoutputcurrent | — | 0.1 A | — | — | offgrid:warning_code | Warning code |
| 44. | Pac 2 H | Threephasegridoutputpower(high) | — | 0.1 VA | — | — | — | — |
| 45. | Pac 2 L | Threephasegridoutputpower(low) | — | 0.1 VA | — | — | — | — |
| 46. | Vac 3 | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 47. | Iac 3 | Threephasegridoutputcurrent | — | 0.1 A | — | — | offgrid:constant_power | — |
| 48. | Pac 3 H | Threephasegridoutputpower(high) | — | 0.1 VA | — | — | offgrid:input_1_energy_today | Input 1 energy today, PV1 energy produced today |
| 49. | Pac 3 L | Threephasegridoutputpower(low) | — | 0.1 VA | — | — | — | — |
| 50. | Vac_RS | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | offgrid:input_1_energy_total | Input 1 total energy, PV1 energy produced Lifetime |
| 51. | Vac_ST | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | — | — |
| 52. | Vac_TR | Threephasegridvoltage | — | 0.1 V Linevoltage | — | — | offgrid:input_2_energy_today | Input 2 energy today, PV2 energy produced today |
| 53. | Eactoday H | Todaygenerateenergy(high) | — | 0.1 k WH | — | — | — | — |
| 54. | Eactoday L | Todaygenerateenergy(low) | — | 0.1 k WH | — | — | offgrid:input_2_energy_total | Input 2 total energy, PV2 energy produced Lifetime |
| 55. | Eactotal H | Totalgenerateenergy(high) | — | 0.1 k WH | — | — | — | — |
| 56. | Eactotal L | Totalgenerateenergy(low) | — | 0.1 k WH | — | — | offgrid:charge_energy_today | Battery Charged (Today), Battery Charged Today |
| 57. | Timetotal H | Worktimetotal(high) | — | 0.5 s | — | — | — | — |
| 58. | Timetotal L | Worktimetotal(low) | — | 0.5 s | — | — | offgrid:charge_energy_total | Battery Charged (Total), Grid Charged Lifetime |
| 59. | Epv 1_today H | PV 1 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 60. | Epv 1_today L | PV 1 Energytoday(low) | — | 0.1 k Wh | — | — | offgrid:discharge_energy_today | Battery Discharged (Today), Battery Discharged Today |
| 61. | Epv 1_total H | PV 1 Energytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 62. | Epv 1_total L | PV 1 Energytotal(low) | — | 0.1 k Wh | — | — | offgrid:discharge_energy_total | Battery Discharged (Total), Battery Discharged Lifetime |
| 63. | Epv 2_today H | PV 2 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 64. | Epv 2_today L | PV 2 Energytoday(low) | — | 0.1 k Wh | — | — | offgrid:ac_discharge_energy_today | AC Discharged Today |
| 65. | Epv 2_total H | PV 2 Energytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 66. | Epv 2_total L | PV 2 Energytotal(low) | — | 0.1 k Wh | — | — | offgrid:ac_discharge_energy_total | Grid Discharged Lifetime |
| 67. | Epv 3_today H | PV 3 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 68. | Epv 3_today L | PV 3 Energytoday(low) | — | 0.1 k Wh | — | — | offgrid:ac_charge_amperage | AC charge battery current |
| 69. | Epv 3_total H | PV 3 Energytotal(high) | — | 0.1 k Wh | — | — | offgrid:discharge_power | Battery discharge power, Discharge Power |
| 70. | Epv 3_total L | PV 3 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 71. | Epv 4_today H | PV 4 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 72. | Epv 4_today L | PV 4 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 73. | Epv 4_total H | PV 4 Energytotal(high) | — | 0.1 k Wh | — | — | offgrid:battery_discharge_amperage | Battery discharge current |
| 74. | Epv 4_total L | PV 4 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 75. | Epv 5_today H | PV 5 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 76. | Epv 5_today L | PV 5 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 77. | Epv 5_total H | PV 5 Energytotal(high) | — | 0.1 k Wh | — | — | offgrid:battery_power | Battery charging/ discharging(-ve) |
| 78. | Epv 5_total L | PV 5 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 79. | Epv 6_today H | PV 6 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 80. | Epv 6_today L | PV 6 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 81. | Epv 6_total H | PV 6 Energytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 82. | Epv 6_total L | PV 6 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 83. | Epv 7_today H | PV 7 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 84. | Epv 7_today L | PV 7 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 85. | Epv 7_total H | PV 7 Energytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 86. | Epv 7_total L | PV 7 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 87. | Epv 8_today H | PV 8 Energytoday(high) | — | 0.1 k Wh | — | — | — | — |
| 88. | Epv 8_today L | PV 8 Energytoday(low) | — | 0.1 k Wh | — | — | — | — |
| 89. | Epv 8_total H | PV 8 Energytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 90. | Epv 8_total L | PV 8 Energytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 91. | Epv_total H | PVEnergytotal(high) | — | 0.1 k Wh | — | — | — | — |
| 92. | Epv_total L | PVEnergytotal(low) | — | 0.1 k Wh | — | — | — | — |
| 93. | Temp 1 | Invertertemperature | — | 0.1 C | — | — | — | — |
| 94. | Temp 2 | Theinside IPMininverter Temperature | — | 0.1 C | — | — | — | — |
| 95. | Temp 3 | Boosttemperature | — | 0.1 C | — | — | — | — |
| 96. | Temp 4 | — | — | reserved | — | — | — | — |
| 97. | uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 98. | PBus Voltage | PBusinside Voltage | — | 0.1 V | — | — | — | — |
| 99. | NBus Voltage | NBusinside Voltage | — | 0.1 V | — | — | — | — |
| 100. | IPF | Inverteroutput PFnow | 0-20000 | — | — | — | — | — |
| 101. | Real OPPercent | Real Outputpower Percent | — | 1% | — | — | — | — |
| 102. | OPFullwatt H | Output Maxpower Limitedhigh | — | — | — | — | — | — |
| 103. | OPFullwatt L | Output Maxpower Limitedlow | — | 0.1 W | — | — | — | — |
| 104. | Derating Mode | Derating Mode | 0:noderate; 1:PV; 2:*; 3:Vac; 4:Fac; 5:Tboost; 6:Tinv; 7:Control; 8:*; 9:*OverBack ByTime; | — | — | — | — | — |
| 105. | Fault Maincode | Inverterfaultmaincode | — | — | — | — | — | — |
| 106. | — | — | — | — | — | — | — | — |
| 107. | Fault Subcode | Inverterfaultsubcode | — | — | — | — | — | — |
| 108. | Remote Ctrl En | / | 0.LoadFirst 1.BatFirst 2.Grid | / Storage Pow er(SPA) | — | — | — | — |
| 109. | Remote Ctrl Pow er | / | — | / Storage Pow er(SPA) | — | — | — | — |
| 110. | Warningbit H | Warningbit H | — | — | — | — | — | — |
| 111. | Warn Subcode | Inverterwarnsubcode | — | — | — | — | — | — |
| 112. | Warn Maincode | Inverterwarnmaincode | — | — | — | — | — | — |
| 113. | real Power Percent | real Power Percent | 0-100 | % MAX | — | — | — | — |
| 114. | inv start delay time | invstartdelaytime | — | MAX | — | — | — | — |
| 115. | b INVAll Fault Cod e | b INVAll Fault Code | — | MAX | — | — | — | — |
| 116. | AC charge Power_H | Gridpowertolocalload | — | 0.1 kwh Storage Power | — | — | — | — |
| 117. | AC charge Power_L | Gridpowertolocalload | — | 0.1 kwh Storage Power | — | — | — | — |
| 118. | Priority | 0:Load First | — | Storage | — | — | — | — |
| 119. | Battery Type | 0:Lead-acid 1:Lithiumbattery | — | — | Storage Power | — | — | — |
| 120. | Auto Proofread C MD | Aging mode Auto-calibration command | — | — | Storage Power | — | — | — |
| 124. | reserved | — | — | — | reserved | — | — | — |
| 125. | PIDPV 1+Voltage | — | PIDPV1PEVolt/Flyspanvoltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 126. | PIDPV 1+Current | — | PIDPV1PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 127. | PIDPV 2+Voltage | — | PID PV2PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 128. | PIDPV 2+Current | — | PIDPV2PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 129. | PIDPV 3+Voltage | — | PID PV3PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 130. | PIDPV 3+Current | — | PIDPV3PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 131. | PIDPV 4+Voltage | — | PID PV4PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 132. | PIDPV 4+Current | — | PIDPV4PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 133. | PIDPV 5+Voltage | — | PID PV5PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 134. | PIDPV 5+Current | — | PIDPV5PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 135. | PIDPV 6+Voltage | — | PID PV6PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 136. | PIDPV 6+Current | — | PIDPV6PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 137. | PIDPV 7+Voltage | — | PID PV7PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 138. | PIDPV 7+Current | — | PIDPV7PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 139. | PIDPV 8+Voltage | — | PID PV8PE Volt/ Flyspan voltage (MAXHV) | 0~1000 V 0.1 V | — | — | — | — |
| 140. | PIDPV 8+Current | — | PIDPV8PECurr | -10~10 m A 0.1 m A | — | — | — | — |
| 141. | PIDStatus | — | Bit0~7:PIDWorkingStatus 1:WaitStatus 2:NormalStatus 3:FaultStatus Bit8~15:Reversed | 0~3 | — | — | — | — |
| 142. | V_String 1 | — | PVString1voltage | 0.1 V | — | — | — | — |
| 143. | Curr_String 1 | — | PVString1current | -15~15 A 0.1 A | — | — | — | — |
| 144. | V_String 2 | — | PVString2voltage | 0.1 V | — | — | — | — |
| 145. | Curr_String 2 | PVString 2 current | -15~15A | 0.1 A | — | — | — | — |
| 146. | V_String 3 | PVString 3 voltage | — | 0.1 V | — | — | — | — |
| 147. | Curr_String 3 | PVString 3 current | -15~15A | 0.1 A | — | — | — | — |
| 148. | V_String 4 | PVString 4 voltage | — | 0.1 V | — | — | — | — |
| 149. | Curr_String 4 | PVString 4 current | -15~15A | 0.1 A | — | — | — | — |
| 150. | V_String 5 | PVString 5 voltage | — | 0.1 V | — | — | — | — |
| 151. | Curr_String 5 | PVString 5 current | -15~15A | 0.1 A | — | — | — | — |
| 152. | V_String 6 | PVString 6 voltage | — | 0.1 V | — | — | — | — |
| 153. | Curr_String 6 | PVString 6 current | -15~15A | 0.1 A | — | — | — | — |
| 154. | V_String 7 | PVString 7 voltage | — | 0.1 V | — | — | — | — |
| 155. | Curr_String 7 | PVString 7 current | -15~15A | 0.1 A | — | — | — | — |
| 156. | V_String 8 | PVString 8 voltage | — | 0.1 V | — | — | — | — |
| 157. | Curr_String 8 | PVString 8 current | -15A~15A | 0.1 A | — | — | — | — |
| 158. | V_String 9 | PVString 9 voltage | — | 0.1 V | — | — | — | — |
| 159. | Curr_String 9 | PVString 9 current | -15A~15A | 0.1 A | — | — | — | — |
| 160. | V_String 10 | PVString 10 voltage | — | 0.1 V | — | — | — | — |
| 161. | Curr_String 10 | PVString 10 current | -15~15A | 0.1 A | — | — | — | — |
| 162. | V_String 11 | PVString 11 voltage | — | 0.1 V | — | — | — | — |
| 163. | Curr_String 11 | PVString 11 current | -15~15A | 0.1 A | — | — | — | — |
| 164. | V_String 12 | PVString 12 voltage | — | 0.1 V | — | — | — | — |
| 165. | Curr_String 12 | PVString 12 current | -15~15A | 0.1 A | — | — | — | — |
| 166. | V_String 13 | PVString 13 voltage | — | 0.1 V | — | — | — | — |
| 167. | Curr_String 13 | PVString 13 current | -15A~15A | 0.1 A | — | — | — | — |
| 168. | V_String 14 | PVString 14 voltage | — | 0.1 V | — | — | — | — |
| 169. | Curr_String 14 | PVString 14 current | -15~15A | 0.1 A | — | — | — | — |
| 170. | V_String 15 | PVString 15 voltage | — | 0.1 V | — | — | — | — |
| 171. | Curr_String 15 | PVString 15 current | -15~15A | 0.1 A | — | — | — | — |
| 172. | V_String 16 | PVString 16 voltage | — | 0.1 V | — | — | — | — |
| 173. | Curr_String 16 | PVString 16 current | -15~15A | 0.1 A | — | — | — | — |
| 174. | Str Unmatch | Bit 0~15:String 1~16 unmatch | — | suggestive | — | — | — | — |
| 175. | Str Current Unblan ce | Bit 0~15:String 1~16 currentunblance | — | suggestive | — | — | — | — |
| 176. | Str Disconnect | Bit 0~15:String 1~16 disconnect | — | suggestive | — | — | — | — |
| 177. | PIDFault Code | Bit 0:Outputovervoltage Bit 1:ISOfault Bit 2:BUSvoltageabnormal Bit 3~15:reserved | — | — | — | — | — | — |
| 178. | String Prompt | String Prompt Bit 0:String Unmatch Bit 1:Str Disconnect Bit 2:Str Current Unblance | — | — | — | — | — | — |
| 179 | PVWarning Value | PVWarning Value | — | — | — | — | — | — |
| 180 | DSP 075 Warning Value | DSP 075 Warning Value | — | — | — | — | — | — |
| 181 | DSP 075 Fault Value | DSP 075 Fault Value | — | — | — | — | — | — |
| 182 | DSP 067 Debug Data 1 | DSP 067 Debug Data 1 | — | — | — | — | — | — |
| 183 | DSP 067 Debug Data 2 | DSP 067 Debug Data 2 | — | — | — | — | — | — |
| 184 | DSP 067 Debug Data 3 | DSP 067 Debug Data 3 | — | — | — | — | — | — |
| 185 | DSP 067 Debug Data 4 | DSP 067 Debug Data 4 | — | — | — | — | — | — |
| 186 | DSP 067 Debug Data 5 | DSP 067 Debug Data 5 | — | — | — | — | — | — |
| 187 | DSP 067 Debug Data 6 | DSP 067 Debug Data 6 | — | — | — | — | — | — |
| 188 | DSP 067 Debug Data 7 | DSP 067 Debug Data 7 | — | — | — | — | — | — |
| 189 | DSP 067 Debug Data 8 | DSP 067 Debug Data 8 | — | — | — | — | — | — |
| 190 | DSP 075 Debug Data 1 | DSP 075 Debug Data 1 | — | — | — | — | — | — |
| 191 | DSP 075 Debug Data 2 | DSP 075 Debug Data 2 | — | — | — | — | — | — |
| 192 | DSP 075 Debug Data 3 | DSP 075 Debug Data 3 | — | — | — | — | — | — |
| 193 | DSP 075 Debug Data 4 | DSP 075 Debug Data 4 | — | — | — | — | — | — |
| 194 | DSP 075 Debug Data 55 | DSP 075 Debug Data 5 | — | — | — | — | — | — |
| 195 | DSP 075 Debug Data 6 | DSP 075 Debug Data 6 | — | — | — | — | — | — |
| 196 | DSP 075 Debug Data 7 | DSP 075 Debug Data 7 | — | — | — | — | — | — |
| 197 | DSP 075 Debug Data 8 | DSP 075 Debug Data 8 | — | — | — | — | — | — |
| 198 | b USBAging Test Ok Flag | USBAging Test Ok Flag | 0-1 | — | — | — | — | — |
| 199 | b Flash Erase Aging Ok Flag | Flash Erase Aging Ok Flag | 0-1 | — | — | — | — | — |
| 200 | PVISO | PVISOValue | — | KΩ | — | — | — | — |
| 201 | R_DCI | RDCICurr | — | 0.1 m A | — | — | — | — |
| 202 | S_DCI | SDCICurr | — | 0.1 m A | — | — | — | — |
| 203 | T_DCI | TDCICurr | — | 0.1 m A | — | — | — | — |
| 204 | PID_Bus | PIDBus Volt | — | 0.1 V | — | — | — | — |
| 205 | GFCI | GFCICurr | — | m A | — | — | — | — |
| 206 | SVG/APF Status+SVGAPFEq ual Ratio | SVG/APFStatus+SVGAPFEqual Ratio | High8bit： SVGAPFEqua lRatio Low8bit： SVG/APF Status 0:None 1:SVGRun 2:APFRun 3:SVG/APF Run | — | — | — | — | — |
| 207 | CT_I_R | Rphaseloadsidecurrentfor SVG | — | 0.1 A | — | — | — | — |
| 208 | CT_I_S | Sphaseloadsidecurrentfor SVG | — | 0.1 A | — | — | — | — |
| 209 | CT_I_T | Tphaseloadsidecurrentfor SVG | — | 0.1 A | — | — | — | — |
| 210 | CT_Q_RH | R phase load side output reactive powerfor SVG(High) | — | 0.1 Var | — | — | — | — |
| 211 | CT_Q_RL | R phase load side output reactive powerfor SVG(low) | — | 0.1 Var | — | — | — | — |
| 212 | CT_Q_SH | S phase load side output reactive powerfor SVG(High) | — | 0.1 Var | — | — | — | — |
| 213 | CT_Q_SL | S phase load side output reactive powerfor SVG(low) | — | 0.1 Var | — | — | — | — |
| 214 | CT_Q_TH | T phase load side output reactive powerfor SVG(High) | — | 0.1 Var | — | — | — | — |
| 215 | CT_Q_TL | T phase load side output reactive powerfor SVG(low) | — | 0.1 Var | — | — | — | — |
| 216 | CTHAR_I_R | Rphaseloadsideharmonic | — | 0.1 A | — | — | — | — |
| 217 | CTHAR_I_S | Sphaseloadsideharmonic | — | 0.1 A | — | — | — | — |
| 218 | CTHAR_I_T | Tphaseloadsideharmonic | — | 0.1 A | — | — | — | — |
| 219 | COMP_Q_RH | R phase compensate reactive power for SVG(High) | — | 0.1 Var | — | — | — | — |
| 220 | COMP_Q_RL | R phase compensate reactive power for SVG(low) | — | 0.1 Var | — | — | — | — |
| 221 | COMP_Q_SH | S phase compensate reactive power for SVG(High) | — | 0.1 Var | — | — | — | — |
| 222 | COMP_Q_SL | S phase compensate reactive power | — | 0.1 Var | — | — | — | — |
| 223 | COMP_Q_TH | T phase compensate reactive power for SVG(High) | — | 0.1 Var | — | — | — | — |
| 224 | COMP_Q_TL | T phase compensate reactive power for SVG(low) | — | 0.1 Var | — | — | — | — |
| 225 | COMPHAR_I_R | R phase compensate harmonic for SVG | — | 0.1 A | — | — | — | — |
| 226 | COMPHAR_I_S | S phase compensate harmonic for SVG | — | 0.1 A | — | — | — | — |
| 227 | COMPHAR_I_T | T phase compensate harmonic for SVG | — | 0.1 A | — | — | — | — |
| 228 | b RS 232 Aging Test Ok Flag | RS 232 Aging Test Ok Flag | 0-1 | — | — | — | — | — |
| 229 | b Fan Fault Bit | Bit 0:Fan 1 faultbit Bit 1:Fan 2 faultbit Bit 2:Fan 3 faultbit Bit 3:Fan 4 faultbit Bit 4-7:Reserved | — | — | — | — | — | — |
| 230 | Sac H | Outputapparentpower H | — | 0.1 W | — | — | — | — |
| 231 | Sac L | Outputapparentpower L | — | 0.1 W | — | — | — | — |
| 232 | Re Act Power H | Real Output Reactive Power H | Int32 | 0.1 W | — | — | — | — |
| 233 | Re Act Power L | Real Output Reactive Power L | — | — | — | — | — | — |
| 234 | Re Act Power Max H | Nominal Output Reactive Power H | — | 0.1 var | — | — | — | — |
| 235 | Re Act Power Max L | Nominal Output Reactive Power L | — | — | — | — | — | — |
| 236 | Re Act Power_Total H | Reactivepowergeneration | — | 0.1 kwh | — | — | — | — |
| 237 | Re Act Power_Total L | Reactivepowergeneration | — | — | — | — | — | — |
| 238 | b Afci Status | 0:Waiting 1:Self-checkstate 2:Detectpullarcstate 3:Fault 4:Update | — | — | — | — | — | — |
| 239 | uw Present FFTValu e[CHANNEL_A] | Present FFTValue[CHANNEL_A] | — | — | — | — | — | — |
| 240 | uw Present FFTValu e[CHANNEL_B] | Present FFTValue[CHANNEL_B] | — | — | — | — | — | — |
| 241 | DSP 067 Debug Data 1 | DSP 067 Debug Data 1 | — | — | — | — | — | — |
| 242 | DSP 067 Debug Data 2 | DSP 067 Debug Data 2 | — | — | — | — | — | — |
| 243 | DSP 067 Debug | DSP 067 Debug Data 3 | — | — | — | — | — | — |
| 244 | DSP 067 Debug Data 4 | DSP 067 Debug Data 4 | — | — | — | — | — | — |
| 245 | DSP 067 Debug Data 5 | DSP 067 Debug Data 5 | — | — | — | — | — | — |
| 246 | DSP 067 Debug Data 6 | DSP 067 Debug Data 6 | — | — | — | — | — | — |
| 247 | DSP 067 Debug Data 7 | DSP 067 Debug Data 7 | — | — | — | — | — | — |
| 248 | DSP 067 Debug Data 8 | DSP 067 Debug Data 8 | — | — | — | — | — | — |
| 249 | — | — | — | reserved | — | — | — | — |
| 875 | Vpv 9 | PV 9 voltage | — | 0.1 V | — | — | — | — |
| 876 | PV 9 Curr | PV 9 Inputcurrent | — | 0.1 A | — | — | — | — |
| 877 | Ppv 9 H | PV 9 inputpower(High) | — | 0.1 W | — | — | — | — |
| 878 | Ppv 9 L | PV 9 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 879 | Vpv 10 | PV 10 voltage | — | 0.1 V | — | — | — | — |
| 880 | PV 10 Curr | PV 10 Inputcurrent | — | 0.1 A | — | — | — | — |
| 881 | Ppv 10 H | PV 10 inputpower(High) | — | 0.1 W | — | — | — | — |
| 882 | Ppv 10 L | PV 10 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 883 | Vpv 11 | PV 11 voltage | — | 0.1 V | — | — | — | — |
| 884 | PV 11 Curr | PV 11 Inputcurrent | — | 0.1 A | — | — | — | — |
| 885 | Ppv 11 H | PV 11 inputpower(High) | — | 0.1 W | — | — | — | — |
| 886 | Ppv 11 L | PV 11 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 887 | Vpv 12 | PV 12 voltage | — | 0.1 V | — | — | — | — |
| 888 | PV 12 Curr | PV 12 Inputcurrent | — | 0.1 A | — | — | — | — |
| 889 | Ppv 12 H | PV 12 inputpower(High) | — | 0.1 W | — | — | — | — |
| 890 | Ppv 12 L | PV 12 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 891 | Vpv 13 | PV 13 voltage | — | 0.1 V | — | — | — | — |
| 892 | PV 13 Curr | PV 13 Inputcurrent | — | 0.1 A | — | — | — | — |
| 893 | Ppv 13 H | PV 13 inputpower(High) | — | 0.1 W | — | — | — | — |
| 894 | Ppv 13 L | PV 13 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 895 | Vpv 14 | PV 14 voltage | — | 0.1 V | — | — | — | — |
| 896 | PV 14 Curr | PV 14 Inputcurrent | — | 0.1 A | — | — | — | — |
| 897 | Ppv 14 H | PV 14 inputpower(High) | — | 0.1 W | — | — | — | — |
| 898 | Ppv 14 L | PV 14 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 899 | Vpv 15 | PV 15 voltage | — | 0.1 V | — | — | — | — |
| 900 | PV 15 Curr | PV 15 Inputcurrent | — | 0.1 A | — | — | — | — |
| 901 | Ppv 15 H | PV 15 inputpower(High) | — | 0.1 W | — | — | — | — |
| 902 | Ppv 15 L | PV 15 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 903 | Vpv 16 | PV 16 voltage | — | 0.1 V | — | — | — | — |
| 904 | PV 16 Curr | PV 16 Inputcurrent | — | 0.1 A | — | — | — | — |
| 905 | Ppv 16 H | PV 16 inputpower(High) | — | 0.1 W | — | — | — | — |
| 906 | Ppv 16 L | PV 16 inputpower(Low) | — | 0.1 W | — | — | — | — |
| 907 | Epv 9_today H | PV 9 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 908 | Epv 9_today L | PV 9 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 909 | Epv 9_total H | PV 9 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 910 | Epv 9_total L | PV 9 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 911 | Epv 10_today H | PV 10 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 912 | Epv 10_today L | PV 10 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 913 | Epv 10_total H | PV 10 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 914 | Epv 10_total L | PV 10 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 915 | Epv 11_today H | PV 11 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 916 | Epv 11_today L | PV 11 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 917 | Epv 11_total H | PV 11 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 918 | Epv 11_total L | PV 11 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 919 | Epv 12_today H | PV 12 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 920 | Epv 12_today L | PV 12 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 921 | Epv 12_total H | PV 12 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 922 | Epv 12_total L | PV 12 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 923 | Epv 13_today H | PV 13 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 924 | Epv 13_today L | PV 13 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 925 | Epv 13_total H | PV 13 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 926 | Epv 13_total L | PV 13 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 927 | Epv 14_today H | PV 14 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 928 | Epv 14_today L | PV 14 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 929 | Epv 14_total H | PV 14 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 930 | Epv 14_total L | PV 14 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 931 | Epv 15_today H | PV 15 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 932 | Epv 15_today L | PV 15 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 933 | Epv 15_total H | PV 15 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 934 | Epv 15_total L | PV 15 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 935 | Epv 16_today H | PV 16 energytoday(High) | — | 0.1 k Wh | — | — | — | — |
| 936 | Epv 16_today L | PV 16 energytoday(Low) | — | 0.1 k Wh | — | — | — | — |
| 937 | Epv 16_total H | PV 16 energytotal(High) | — | 0.1 k Wh | — | — | — | — |
| 938 | Epv 16_total L | PV 16 energytotal(Low) | — | 0.1 k Wh | — | — | — | — |
| 939 | PIDPV 9+Voltage | PID PV 9 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 940 | PIDPV 9+Current | PIDPV 9 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 941 | PID PV 10+ Voltage | PID PV 10 PE/ Flyspan voltage (MAX HV) | 0~1000V | 0.1 V | — | — | — | — |
| 942 | PID PV 10+ Current | PIDPV 10 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 943 | PID PV 11+ Voltage | PID PV 11 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 944 | PID PV 11+ Current | PIDPV 11 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 945 | PID PV 12+ Voltage | PID PV 12 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 946 | PID PV 12+ Current | PIDPV 12 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 947 | PID PV 13+ Voltage | PID PV 13 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 948 | PID PV 13+ Current | PIDPV 13 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 949 | PID PV 14+ Voltage | PID PV 14 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 950 | PID PV 14+ Current | PIDPV 14 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 951 | PID PV 15+ Voltage | PID PV 15 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 952 | PID PV 15+ Current | PIDPV 15 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 953 | PID PV 16+ Voltage | PID PV 16 PE Volt/ Flyspan voltage (MAXHV) | 0~1000V | 0.1 V | — | — | — | — |
| 954 | PID PV 16+ Current | PIDPV 16 PECurrent | -10~10mA | 0.1 m A | — | — | — | — |
| 955 | V_String 17 | PVString 17 voltage | — | 0.1 V | — | — | — | — |
| 956 | Curr_String 17 | PVString 17 Current | -15~15A | 0.1 A | — | — | — | — |
| 957 | V_String 18 | PVString 18 voltage | — | 0.1 V | — | — | — | — |
| 958 | Curr_String 18 | PVString 18 Current | -15~15A | 0.1 A | — | — | — | — |
| 959 | V_String 19 | PVString 19 voltage | — | 0.1 V | — | — | — | — |
| 960 | Curr_String 19 | PVString 19 Current | -15~15A | 0.1 A | — | — | — | — |
| 961 | V_String 20 | PVString 20 voltage | — | 0.1 V | — | — | — | — |
| 962 | Curr_String 20 | PVString 20 Current | -15~15A | 0.1 A | — | — | — | — |
| 963 | V_String 21 | PVString 21 voltage | — | 0.1 V | — | — | — | — |
| 964 | Curr_String 21 | PVString 21 Current | -15~15A | 0.1 A | — | — | — | — |
| 965 | V_String 22 | PVString 22 voltage | — | 0.1 V | — | — | — | — |
| 966 | Curr_String 22 | PVString 22 Current | -15~15A | 0.1 A | — | — | — | — |
| 967 | V_String 23 | PVString 23 voltage | — | 0.1 V | — | — | — | — |
| 968 | Curr_String 23 | PVString 23 Current | -15~15A | 0.1 A | — | — | — | — |
| 969 | V_String 24 | PVString 24 voltage | — | 0.1 V | — | — | — | — |
| 970 | Curr_String 24 | PVString 24 Current | — | -15 A~15 A | — | 0.1 A | — | — |
| 971 | V_String 25 | PVString 25 voltage | — | — | — | 0.1 V | — | — |
| 972 | Curr_String 25 | PVString 25 Current | — | -15 A~15 A | — | 0.1 A | — | — |
| 973 | V_String 26 | PVString 26 voltage | — | — | — | 0.1 V | — | — |
| 974 | Curr_String 26 | PVString 26 Current | — | -15~15 A | — | 0.1 A | — | — |
| 975 | V_String 27 | PVString 27 voltage | — | — | — | 0.1 V | — | — |
| 976 | Curr_String 27 | PVString 27 Current | — | -15~15 A | — | 0.1 A | — | — |
| 977 | V_String 28 | PVString 28 voltage | — | — | — | 0.1 V | — | — |
| 978 | Curr_String 28 | PVString 28 Current | — | -15~15 A | — | 0.1 A | — | — |
| 979 | V_String 29 | PVString 29 voltage | — | — | — | 0.1 V | — | — |
| 980 | Curr_String 29 | PVString 29 Current | — | -15 A~15 A | — | 0.1 A | — | — |
| 981 | V_String 30 | PVString 30 voltage | — | — | — | 0.1 V | — | — |
| 982 | Curr_String 30 | PVString 30 Current | — | -15~15 A | — | 0.1 A | — | — |
| 983 | V_String 31 | PVString 31 voltage | — | — | — | 0.1 V | — | — |
| 984 | Curr_String 31 | PVString 31 Current | — | -15~15 A | — | 0.1 A | — | — |
| 985 | V_String 32 | PVString 32 voltage | — | — | — | 0.1 V | — | — |
| 986 | Curr_String 32 | PVString 32 Current | — | -15~15 A | — | 0.1 A | — | — |
| 987 | Str Unmatch 2 | Bit 0~15:String 17~32 unmatch | — | — | — | — | — | — |
| 988 | Str Current Unblan ce 2 | Bit 0~15:String 17~32 current unblance | — | — | — | — | — | — |
| 989 | Str Disconnect 2 | Bit 0~15:String 17~32 disconnect | — | — | — | — | — | — |
| 990 | PVWarning Value | PVWarning Value(PV 9-PV 16) Contains PV 9~16 abnormal , 和 Boost 9~16 Driveanomalies | — | — | — | — | — | — |
| 991 | Str Waringvalue 1 | string 1~string 16 abnormal | — | — | — | — | — | — |
| 992 | Str Waringvalue 2 | string 17~string 32 abnormal | — | — | — | — | — | — |
| 999 | System Cmd | M 3 to DSPsystemcommand | — | — | — | — | — | — |
| 1000. | uw Sys Work Mode | — | Systemworkmode | 0 x 00:waiting module 0 x 01: Self-test mode, optional 0 x 02 : Reserved 0 x 03:Sys Fault module 0 x 04: Flash module | — | — | — | — |
| 1001. | Systemfaultword 0 | Systemfaultword 0 | — | Please refer to thefault description of Hybrid | — | — | — | — |
| 1002. | Systemfaultword 1 | Systemfaultword 1 | — | — | — | — | — | — |
| 1003. | Systemfaultword 2 | Systemfaultword 2 | — | — | — | — | — | — |
| 1004. | Systemfaultword 3 | Systemfaultword 3 | — | — | — | — | — | — |
| 1005. | Systemfaultword 4 | Systemfaultword 4 | — | — | — | — | — | — |
| 1006. | Systemfaultword 5 | Systemfaultword 5 | — | — | — | — | — | — |
| 1007. | Systemfaultword 6 | Systemfaultword 6 | — | — | — | — | — | — |
| 1008. | Systemfaultword 7 | Systemfaultword 7 | — | — | — | — | — | — |
| 1009. | Pdischarge 1 H | Dischargepower(high) | — | 0.1 W | — | — | — | — |
| 1010. | Pdischarge 1 L | Dischargepower(low) | — | 0.1 W | — | — | — | — |
| 1011. | Pcharge 1 H | Chargepower(high) | — | 0.1 W | — | — | — | — |
| 1012. | Pcharge 1 L | Chargepower(low) | — | 0.1 W | — | — | — | — |
| 1013. | Vbat | Batteryvoltage | — | 0.1 V | — | — | — | — |
| 1014. | SOC | Stateofcharge Capacity | 0-100 | 1% lith/leadacid | — | — | — | — |
| 1015. | Pactouser R H | ACpowertouser H | — | 0.1 w | — | — | — | — |
| 1016. | Pactouser R L | ACpowertouser L | — | 0.1 w | — | — | — | — |
| 1017. | Pactouser S H | Pactouser S H | — | 0.1 w | — | — | — | — |
| 1018. | Pactouser S L | Pactouser S L | — | 0.1 w | — | — | — | — |
| 1019. | Pactouser T H | Pactouser T H | — | 0.1 w | — | — | — | — |
| 1020. | Pactouser T L | Pactouser T H | — | 0.1 w | — | — | — | — |
| 1021. | Pactouser Total H | ACpowertousertotal H | — | 0.1 w | — | — | — | — |
| 1022. | Pactouser Total L | ACpowertousertotal L | — | 0.1 w | — | — | — | — |
| 1023. | Pactogrid R H | ACpowertogrid H | — | 0.1 w Ac output | — | — | — | — |
| 1024. | Pactogrid R L | ACpowertogrid L | — | 0.1 w | — | — | — | — |
| 1025. | Pactogrid S H | — | — | 0.1 w | — | — | — | — |
| 1026. | Pactogrid S L | — | — | 0.1 w | — | — | — | — |
| 1027. | — | Pactogrid TH | — | — | — | 0.1 w | — | — |
| 1028. | — | Pactogrid TL | — | — | — | 0.1 w | — | — |
| 1029. | — | Pactogridtotal H | — | ACpowertogridtotal H | — | 0.1 w | — | — |
| 1030. | — | Pactogridtotal L | — | ACpowertogridtotal L | — | 0.1 w | — | — |
| 1031. | — | PLocal Load R H | — | INVpowertolocalload H | — | 0.1 w | — | — |
| 1032. | — | PLocal Load R L | — | INVpowertolocalload L | — | 0.1 w | — | — |
| 1033. | — | PLocal Load S H | — | — | — | 0.1 w | — | — |
| 1034. | — | PLocal Load S L | — | — | — | 0.1 w | — | — |
| 1035. | — | PLocal Load T H | — | — | — | 0.1 w | — | — |
| 1036. | — | PLocal Load T L | — | — | — | 0.1 w | — | — |
| 1037. | — | PLocal Loadtotal H | — | INVpowertolocalloadtotal H | — | 0.1 w | — | — |
| 1038. | — | PLocal Loadtotal L | — | INV power to local load total L | — | 0.1 w | — | — |
| 1039. | — | IP 2 MTemperature | — | RECTemperature | — | 0.1℃ | — | — |
| 1040. | — | B 2 attery Temperature | — | Battery Temperature | — | 0.1℃ | — | — |
| 1041. | — | SPDSPStatus | — | SPstate | — | — | — | — |
| 1042. | — | SPBus Volt | — | SPBUS 2 Volt | — | 0.1 V | — | — |
| 1043 | — | — | — | — | — | — | — | — |
| 1044. | Etouser_today H | — | Energytousertodayhigh | — | 0.1 k Wh | — | — | — |
| 1045. | Etouser_today L | — | Energytousertodaylow | — | 0.1 k Wh | — | — | — |
| 1046. | Etouser_total H | — | Energytousertotalhigh | — | 0.1 k Wh | — | — | — |
| 1047. | Etouser_total L | — | Energytousertotalhigh | — | 0.1 k Wh | — | — | — |
| 1048. | Etogrid_today H | — | Energytogridtodayhigh | — | 0.1 k Wh | — | — | — |
| 1049. | Etogrid_today L | — | Energytogridtodaylow | — | 0.1 k Wh | — | — | — |
| 1050. | Etogrid_total H | — | Energytogridtotalhigh | — | 0.1 k Wh | — | — | — |
| 1051. | Etogrid_total L | — | Energytogridtotalhigh | — | 0.1 k Wh | — | — | — |
| 1052. | Edischarge 1_toda y H | — | Dischargeenergy1today | — | 0.1 k Wh | — | — | — |
| 1053. | Edischarge 1_toda y L | — | Dischargeenergy1today | — | 0.1 k Wh | — | — | — |
| 1054. | Edischarge 1_total H | — | Totaldischargeenergy1(high) | — | 0.1 k Wh | — | — | — |
| 1055. | Edischarge 1_total L | — | Totaldischargeenergy1(low) | — | 0.1 k Wh | — | — | — |
| 1056. | Echarge 1_today H | — | Charge1energytoday | — | 0.1 k Wh | — | — | — |
| 1057. | Echarge 1_today L | — | Charge1energytoday | — | 0.1 k Wh | — | — | — |
| 1058. | Echarge 1_total H | — | Charge1energytotal | — | 0.1 k Wh | — | — | — |
| 1059. | Echarge 1_total L | — | Charge1energytotal | — | 0.1 k Wh | — | — | — |
| 1060 | — | — | . ELocalLoad_Today H | — | — | Localloadenergytoday | — | — |
| 1061 | — | — | . ELocalLoad_Today L | — | — | Localloadenergytoday | — | — |
| 1062 | — | — | . ELocalLoad_Total H | — | — | Localloadenergytotal | — | — |
| 1063 | — | — | . ELocalLoad_Total L | — | — | Localloadenergytotal | — | — |
| 1064 | — | — | . dwExportLimitAp parentPower | — | — | Export Limit Apparent Power H | — | — |
| 1065 | — | — | . dwExportLimitAp parentPower | — | — | Export Limit Apparent Power L | — | — |
| 1066 | — | — | . / | — | — | / | — | — |
| 1067 | — | — | . EPSFac | — | — | UPSfrequency | — | — |
| 1068 | — | — | . EPSVac1 | — | — | UPSphase Routputvoltage | — | — |
| 1069 | — | — | . EPSIac1 | — | — | UPSphase Routputcurrent | — | — |
| 1070 | — | — | . EPSPac1H | — | — | UPSphase Routputpower(H) | — | — |
| 1071 | — | — | . EPSPac1L | — | — | UPSphase Routputpower(L) | — | — |
| 1072 | — | — | . EPSVac2 | — | — | UPSphase Soutputvoltage | — | — |
| 1073 | — | — | . EPSIac2 | — | — | UPSphase Soutputcurrent | — | — |
| 1074 | — | — | . EPSPac2H | — | — | UPSphase Soutputpower(H) | — | — |
| 1075 | — | — | . EPSPac2L | — | — | UPSphase Soutputpower(L) | — | — |
| 1076 | — | — | . EPSVac3 | — | — | UPSphase Toutputvoltage | — | — |
| 1077 | — | — | . EPSIac3 | — | — | UPSphase Toutputcurrent | — | — |
| 1078 | — | — | . EPSPac3H | — | — | UPSphase Toutputpower(H) | — | — |
| 1079 | — | — | . EPSPac3L | — | — | UPSphase Toutputpower(L) | — | — |
| 1080 | — | — | . Loadpercent | — | — | Loadpercentof UPSouput | — | — |
| 1081 | — | — | . PF | — | — | Powerfactor | — | — |
| 1082. | — | — | — | BMS_Status Old | — | Status Oldfrom BMS | — | — |
| 1083. | — | — | — | BMS_Status | — | Statusfrom BMS | — | — |
| 1084. | — | — | — | BMS_Error Old | — | Errorinfo Oldfrom BMS | — | — |
| 1085. | — | — | — | BMS_Error | — | Errorinfomationfrom BMS | — | — |
| 1086. | — | — | — | BMS_SOC | — | SOCfrom BMS | — | — |
| 1087. | — | — | — | BMS_Battery Vol t | — | Batteryvoltagefrom BMS | — | — |
| 1088. | — | — | — | BMS_Battery Cur r | — | Batterycurrentfrom BMS | — | — |
| 1089. | — | — | — | BMS_Battery Te mp | — | Batterytemperaturefrom BMS | — | — |
| 1090. | BMS_Max Curr | Max. charge/discharge current from BMS(pylon) | — | — | — | — | — | — |
| 1091. | BMS_Gauge RM | Gauge RMfrom BMS | — | — | — | — | — | — |
| 1092. | BMS_Gauge FCC | Gauge FCCfrom BMS | — | — | — | — | — | — |
| 1093. | BMS_FW | — | — | — | — | — | — | — |
| 1094. | BMS_Delta Volt | Delta Vfrom BMS | — | — | — | — | — | — |
| 1095. | BMS_Cycle Cnt | Cycle Countfrom BMS | — | — | — | — | — | — |
| 1096. | BMS_SOH | SOHfrom BMS | — | — | — | — | — | — |
| 1097. | BMS_Constant V olt | CVvoltagefrom BMS | — | — | — | — | — | — |
| 1098. | BMS_Warn Info O ld | Warninginfooldfrom BMS | — | — | — | — | — | — |
| 1099. | BMS_Warn Info | Warninginfofrom BMS | — | — | — | — | — | — |
| 1100. | BMS_Gauge ICCu rr | Gauge ICcurrentfrom BMS | — | — | — | — | — | — |
| 1101. | BMS_MCUVersi on | MCUSoftwareversionfrom BMS | — | — | — | — | — | — |
| 1102. | BMS_Gauge Vers ion | Gauge Versionfrom BMS | — | — | — | — | — | — |
| 1103. | BMS_w Gauge FR Version_L | Gauge FRVersion L 16 from BMS | — | — | — | — | — | — |
| 1104. | BMS_w Gauge FR Version_H | Gauge FRVersion H 16 from BMS | — | — | — | — | — | — |
| 1105. | BMS_BMSInfo | BMSInformationfrom BMS | — | — | — | — | — | — |
| 1106. | BMS_Pack Info | Pack Informationfrom BMS | — | — | — | — | — | — |
| 1107. | BMS_Using Cap | Using Capfrom BMS | — | — | — | — | — | — |
| 1108. | uw Max Cell Volt | Maximumsinglebatteryvoltage | — | 0.001 V | — | — | — | — |
| 1109. | uw Min Cell Volt | Lowestsinglebatteryvoltage | — | 0.001 V | — | — | — | — |
| 1110. | b Module Num | Batteryparallelnumber | — | 1 | — | — | — | — |
| 1111. | — | Numberofbatteries | — | 1 | — | — | — | — |
| 1112. | uw Max Volt Cell N o | Max Volt Cell No | — | 1 | — | — | — | — |
| 1113. | uw Min Volt Cell N o | Min Volt Cell No | — | 1 | — | — | — | — |
| 1114. | uw Max Tempr Ce ll_10 T | Max Tempr Cell_10 T | — | 0.1℃ | — | — | — | — |
| 1115. | uw Min Tempr Cel l_10 T | Min Tempr Cell_10 T | — | 0.1℃ | — | — | — | — |
| 1116. | uw Max Tempr Ce ll No | Max Volt Tempr Cell No | — | 1 | — | — | — | — |
| 1117. | uw Min Tempr Cel | Min Volt Tempr Cell No | — | 1 | — | — | — | — |
| 1118. | Protectpack ID | Faulty Battery Address | — | 1 | — | — | — | — |
| 1119. | Max SOC | Parallelmaximum SOC | — | 1% | — | — | — | — |
| 1120. | Min SOC | Parallelminimum SOC | — | 1% | — | — | — | — |
| 1121. | BMS_Error 2 | Battery Protection 2 | — | - | CAN ID : 0 x 323 Byte 4~5 | — | — | — |
| 1122. | BMS_Error 3 | Battery Protection 3 | — | - | CAN ID : 0 x 323 Byte 6 | — | — | — |
| 1123. | BMS_Warn Info 2 | Battery Warn 2 | — | - | CAN ID : 0 x 323 Byte 7 | — | — | — |
| 1124 | ACCharge Energy Today H | ACCharge Energytoday | kwh | — | Energytoday | — | — | — |
| 1125. | ACCharge Energy Today L | ACCharge Energytoday | kwh | — | — | — | — | — |
| 1126. | A 1 CCharge Energy Total H | — | — | — | Energytotal | — | — | — |
| 1127. | ACCharge Energy Total L | — | — | — | — | — | — | — |
| 1128. | AC Charge Power H | ACCharge Power | W | — | — | — | — | — |
| 1129. | AC Charge Power L | ACCharge Power | w | — | — | — | — | — |
| 1130. | 70% INV Power adjust | uw Grid Power_70_Adj EE_SP | W | — | — | — | — | — |
| 1131. | Extra AC Power to grid_H | Extrainverte ACPowertogrid High | ForSPA connect inverter | — | SPAused | — | — | — |
| 1132. | Extra AC Power to grid_L | Extrainverte ACPowertogrid Low | — | — | SPAused | — | — | — |
| 1133. | Eextra_today H | Extrainverter Power TOUser_Extra today(high) | R | 0.1 k Wh | SPA used | — | — | — |
| 1134. | Eextra_today L | Extrainverter Power TOUser_Extra today(low) | R | 0.1 k Wh | SPA used | — | — | — |
| 1135. | Eextra_total H | Extrainverter Power TOUser_Extra total(high) | — | 0.1 k Wh | SPA used | — | — | — |
| 1136. | Eextra_total L | Extrainverter Power TOUser_Extra total(low) | — | 0.1 k Wh | SPA used | — | — | — |
| 1137. | Esystem_today H | Systemelectricenergytoday H | — | 0.1 k Wh | SPA used System electric energytoday H | — | — | — |
| 1138. | Esystem_ today L | Systemelectricenergytoday L | — | 0.1 k Wh SPA used System electric energytoday L | — | — | — | — |
| 1139. | Esystem_total H | Systemelectricenergytotal H | — | 0.1 k Wh SPA used System electric energytotal H | — | — | — | — |
| 1140. | Esystem_total L | Systemelectricenergytotal L | — | 0.1 k Wh SPA used System electric energytotal L | — | — | — | — |
| 1141. | Eself_today H | selfelectricenergytoday H | — | 0.1 k Wh self electric energytoday H | — | — | — | — |
| 1142. | Eself_today L | selfelectricenergytoday L | — | 0.1 k Wh self electric energytoday L | — | — | — | — |
| 1143. | Eself_total H | selfelectricenergytotal H | — | 0.1 k Wh self electric energytotal H | — | — | — | — |
| 1144. | Eself_total L | selfelectricenergytotal L | — | 0.1 k Wh self electric energytotal L | — | — | — | — |
| 1145. | PSystem H | Systempower H | — | 0.1 w Systempower H | — | — | — | — |
| 1146. | PSystem L | Systempower L | — | 0.1 w Systempower L | — | — | — | — |
| 1147. | PSelf H | selfpower H | — | 0.1 w selfpower H | — | — | — | — |
| 1148. | PSelf L | selfpower L | — | 0.1 w selfpower L | — | — | — | — |
| 1149. | EPVAll_Today H | PVelectricenergytoday H | — | — | — | — | — | — |
| 1150. | EPVAll_Today L | PVelectricenergytoday L | — | — | — | — | — | — |
| 1151. | Ac Discharge Pack Sn | Discharge power pack serial number | R | / | — | — | — | — |
| 1152. | Accdischarge power_H | Cumulative discharge power high 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1153. | Accdischarge power_L | Cumulative discharge power low 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1154. | Acc Charge Pack Sn | chargepowerpackserialnumber | R | / | — | — | — | — |
| 1155. | Acc Charge power_H | Cumulative charge power high 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1156. | Acc Charge power_L | Cumulative charge power low 16-bitbyte | R | 0.1 k WH | — | — | — | — |
| 1157. | First Batt Fault Sn | First Batt Fault Sn | R | / | — | — | — | — |
| 1158. | Second Batt Fault Sn | Second Batt Fault Sn | R | / | — | — | — | — |
| 1159. | Third Batt Fault Sn | Third Batt Fault Sn | R | / | — | — | — | — |
| 1160. | Fourth Batt Fault Sn | Fourth Batt Fault Sn | R | / | — | — | — | — |
| 1161. | Batteryhistory faultcode 1 | Batteryhistoryfaultcode 1 | R | / | — | — | — | — |
| 1162. | Batteryhistory faultcode 2 | Batteryhistoryfaultcode 2 | R | / | — | — | — | — |
| 1163. | Batteryhistory faultcode 3 | Batteryhistoryfaultcode 3 | R | / | — | — | — | — |
| 1164. | Batteryhistory faultcode 4 | Batteryhistoryfaultcode 4 | R | / | — | — | — | — |
| 1165. | Batteryhistory faultcode 5 | Batteryhistoryfaultcode 5 | R | / | — | — | — | — |
| 1166. | Batteryhistory faultcode 6 | Batteryhistoryfaultcode 6 | R | / | — | — | — | — |
| 1167. | Batteryhistory faultcode 7 | Batteryhistoryfaultcode 7 | R | / | — | — | — | — |
| 1168. | Batteryhistory faultcode 8 | Batteryhistoryfaultcode 8 | R | / | — | — | — | — |
| 1169. | Number of battery codes | Number of battery codes PACK number + BIC forward and reversecodes | R | / | — | — | — | — |
| 1170. | — | — | — | — | — | — | — | — |
| 1199 | New EPower Calc Flag | Intelligent reading is used to identify software compatibility features | — | 0 : Old energy calculation; 1 : new energy calculation | — | — | — | — |
| 1200 | Max Cell Volt | Maximumcellvoltage | R | 0.001 V | — | — | — | — |
| 1201 | Min Cell Volt | Minimumcellvoltage | R | 0.001 V | — | — | — | — |
| 1202 | Module Num | Numberof Batterymodules | R | / | — | — | — | — |
| 1203 | Total Cell Num | Totalnumberofcells | R | / | — | — | — | — |
| 1204 | Max Volt Cell No | Max Volt Cell No | R | / | — | — | — | — |
| 1205 | Min Volt Cell No | Min Volt Cell No | R | / | — | — | — | — |
| 1206 | Max Tempr Cell_ 10 T | Max Tempr Cell_10 T | R | 0.1℃ | — | — | — | — |
| 1207 | Min Tempr Cell_1 0 T | Min Tempr Cell_10 T | R | 0.1℃ | — | — | — | — |
| 1208 | Max Tempr Cell N o | Max Tempr Cell No | R | / | — | — | — | — |
| 1209 | Min Tempr Cell N o | Min Tempr Cell No | R | / | — | — | — | — |
| 1210 | Protect Pack ID | Fault Pack ID | R | / | — | — | — | — |
| 1211 | Max SOC | Parallelmaximum SOC | R | 1% | — | — | — | — |
| 1212 | Min SOC | Parallelminimum SOC | R | 1% | — | — | — | — |
| 1213 | Bat Protect 1 Add | Bat Protect 1 Add | R | / | — | — | — | — |
| 1214 | Bat Protect 2 Add | Bat Protect 2 Add | R | / | — | — | — | — |
| 1215 | Bat Warn 1 Add | Bat Warn 1 Add | R | / | — | — | — | — |
| 1216 | BMS_Highest Sof t Version | BMS_Highest Soft Version | R | / | — | — | — | — |
| 1217 | BMS_Hardware Version | BMS_Hardware Version | R | / | — | — | — | — |
| 1218 | BMS_Request Ty pe | BMS_Request Type | R | / | — | — | — | — |
| 1248 | b Key Aging Test O k Flag | Success sign of key detection beforeaging | — | 1:Finishedtest 0 : test not completed | — | — | — | — |
| 1249. | / | / | / | / reversed | — | — | — | — |
| 2000 | — | Inverter Status | — | — | — | Inverterrunstate | — | — |
| 2035 | — | Pac H | — | — | — | Outputpower(high) | — | — |
| 2036 | — | Pac L | — | — | — | Outputpower(low) | — | — |
| 2037 | — | Fac | — | — | — | Gridfrequency | — | — |
| 2038 | — | Vac 1 | — | — | — | Three/singlephasegridvoltage | — | — |
| 2039 | — | Iac 1 | — | — | — | Three/singlephasegridoutputcurrent | — | — |
| 2040 | — | Pac 1 H | — | — | — | Three/single phase grid output watt VA(high) | — | — |
| 2041 | — | Pac 1 L | — | — | — | Three/single phase grid output watt VA(low) | — | — |
| 2053 | — | Eactoday H | — | — | — | Todaygenerateenergy(high) | — | — |
| 2054 | — | Eactoday L | — | — | — | Todaygenerateenergy(low) | — | — |
| 2055 | Eactotal H | Totalgenerateenergy(high) | — | 0.1 k WH SPA | — | — | — | — |
| 2056 | Eactotal L | Totalgenerateenergy(low) | — | 0.1 k WH SPA | — | — | — | — |
| 2057 | Timetotal H | Worktimetotal(high) | — | 0.5 s SPA | — | — | — | — |
| 2058 | Timetotal L | Worktimetotal(low) | — | 0.5 s SPA | — | — | — | — |
| 2093 | Temp 1 | Invertertemperature | — | 0.1 C SPA | — | — | — | — |
| 2094 | Temp 2 | Theinside IPMininverter Temperature | — | 0.1 C SPA | — | — | — | — |
| 2095 | Temp 3 | Boosttemperature | — | 0.1 C SPA | — | — | — | — |
| 2096 | Temp 4 | — | — | reserved | — | — | — | — |
| 2097 | uw Bat Volt_DSP | Bat Volt_DSP | — | 0.1 V Bat Volt(DSP) | — | — | — | — |
| 2098 | PBus Voltage | PBusinside Voltage | — | 0.1 V SPA | — | — | — | — |
| 2099 | NBus Voltage | NBusinside Voltage | — | 0.1 V SPA | — | — | — | — |
| 2100 | Remote Ctrl En | / | 0.LoadFirst 1.BatFirst 2.Grid | / Remote setup enable | — | — | — | — |
| 2101 | Remote Ctrl Pow er | / | — | / Remotely setpower | — | — | — | — |
| 2102 | Extra AC Power to grid_H | Extrainverte ACPowertogrid High | ForSPA connect inverter | SPAused | — | — | — | — |
| 2103 | Extra AC Power to grid_L | Extrainverte ACPowertogrid Low | — | SPAused | — | — | — | — |
| 2104 | Eextra_today H | Extrainverter Power TOUser_Extra today(high) | R | 0.1 k Wh SPA used | — | — | — | — |
| 2105 | Eextra_today L | Extrainverter Power TOUser_Extra today(low) | R | 0.1 k Wh SPA used | — | — | — | — |
| 2106 | Eextra_total H | Extrainverter Power TOUser_Extratotal(high) | — | 0.1 k Wh SPA used | — | — | — | — |
| 2107 | Eextra_total L | Extrainverter Power TOUser_Extra total(low) | — | 0.1 k Wh SPA used | — | — | — | — |
| 2108 | Esystem_today H | Systemelectricenergytoday H | — | 0.1 k Wh SPA used System electric energy today H | — | — | — | — |
| 2109 | Esystem_ today L | Systemelectricenergytoday L | — | 0.1 k Wh SPA used System electric energy today L | — | — | — | — |
| 2110 | Esystem_total H | Systemelectricenergytotal H | — | 0.1 k Wh SPA used System | — | — | — | — |
| 2111 | Esystem_total L | Systemelectricenergytotal L | — | 0.1 k Wh | SPA used System electric energy total L | — | — | — |
| 2112 | EACharge_Today _H | ACChargeenergytoday | — | 0.1 kwh | Storage Power | — | — | — |
| 2113 | EACharge_Today _L | ACChargeenergytoday | — | 0.1 kwh | Storage Power | — | — | — |
| 2114 | EACharge_Total _H | ACChargeenergytotal | — | 0.1 kwh | Storage Power | — | — | — |
| 2115 | EACharge_Total _L | ACChargeenergytotal | — | 0.1 kwh | Storage Power | — | — | — |
| 2116 | AC charge Power_H | Gridpowertolocalload | — | 0.1 kwh | Storage Power | — | — | — |
| 2117 | AC charge Power_L | Gridpowertolocalload | — | 0.1 kwh | Storage Power | — | — | — |
| 2118 | Priority | 0:Load First 1:Battery First 2:Grid First | — | — | Storage Power | — | — | — |
| 2119 | Battery Type | 0:Lead-acid 1:Lithiumbattery | — | — | Storage Power | — | — | — |
| 2120 | Auto Proofread C MD | Agingmode | — | — | Storage Power | — | — | — |
| 2124. | reserved | — | — | — | reserved | — | — | — |
| 3000 | Inverter Status | Inverterrunstate High 8 bitsmode(specificmode) 0:Waitingmodule 1:Self-testmode,optional 2:Reserved 3:Sys Fault module 4:Flashmodule 5:PVBATOnlinemodule: 6:Bat Onlinemodule | — | — | — | — | — | — |
| 3001 | Ppv H | PVtotalpower | — | 0.1 W | — | — | — | — |
| 3002 | Ppv L | — | — | — | — | — | — | — |
| 3003 | Vpv 1 | PV 1 voltage | — | 0.1 V | — | — | — | — |
| 3004 | Ipv 1 | PV 1 inputcurrent | — | 0.1 A | — | — | — | — |
| 3005 | Ppv 1 H | PV 1 power | — | 0.1 W | — | — | — | — |
| 3006 | Ppv 1 L | — | — | — | — | — | — | — |
| 3007 | Vpv 2 | PV 2 voltage | — | 0.1 V | — | — | — | — |
| 3008 | Ipv 2 | PV 2 inputcurrent | — | 0.1 A | — | — | — | — |
| 3009 | Ppv 2 H | PV 2 power | — | 0.1 W | — | — | — | — |
| 3010 | Ppv 2 L | — | — | — | — | — | — | — |
| 3011 | Vpv 3 | PV 3 voltage | — | 0.1 V | — | — | — | — |
| 3012 | Ipv 3 | PV 3 inputcurrent | — | 0.1 A | — | — | — | — |
| 3013 | Ppv 3 H | PV 3 power | — | 0.1 W | — | — | — | — |
| 3014 | Ppv 3 L | — | — | — | — | — | — | — |
| 3015 | Vpv 4 | PV 4 voltage | — | — | — | — | — | — |
| 3016 | Ipv 4 | PV 4 inputcurrent | — | — | — | — | — | — |
| 3017 | Ppv 4 H | PV 4 power | — | — | — | — | — | — |
| 3018 | Ppv 4 L | — | — | — | — | — | — | — |
| 3019 | Psys H | Systemoutputpower | — | 0.1 W | — | — | — | — |
| 3020 | Psys L | — | — | — | — | — | — | — |
| 3021 | Qac H | reactivepower | — | 0.1 Var | — | — | — | — |
| 3022 | Qac L | — | — | — | — | — | — | — |
| 3023 | Pac H | Outputpower | — | 0.1 W Output power | — | — | — | — |
| 3024 | Pac L | — | — | — | — | — | — | — |
| 3025 | Fac | Gridfrequency | — | 0.01 Hz Grid frequency | — | — | — | — |
| 3026 | Vac 1 | Three/singlephasegridvoltage | — | 0.1 V Three/single phase grid voltage | — | — | — | — |
| 3027 | Iac 1 | Three/singlephasegridoutputcurrent | — | 0.1 A Three/single | — | — | — | — |
| 3028 | Pac 1 H | Three/singlephasegridoutputwatt VA | — | 0.1 VA Three/single phasegrid outputwatt VA | — | — | — | — |
| 3029 | Pac 1 L | — | — | — | — | — | — | — |
| 3030 | Vac 2 | Threephasegridvoltage | — | 0.1 V Threephase gridvoltage | — | — | — | — |
| 3031 | Iac 2 | Threephasegridoutputcurrent | — | 0.1 A Threephase gridoutput current | — | — | — | — |
| 3032 | Pac 2 H | Threephasegridoutputpower | — | 0.1 VA Threephase gridoutput power | — | — | — | — |
| 3033 | Pac 2 L | — | — | — | — | — | — | — |
| 3034 | Vac 3 | Threephasegridvoltage | — | 0.1 V Threephase gridvoltage | — | — | — | — |
| 3035 | Iac 3 | Threephasegridoutputcurrent | — | 0.1 A Threephase gridoutput current | — | — | — | — |
| 3036 | Pac 3 H | Threephasegridoutputpower | — | 0.1 VA Threephase gridoutput power | — | — | — | — |
| 3037 | Pac 3 L | — | — | — | — | — | — | — |
| 3038 | Vac_RS | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3039 | Vac_ST | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3040 | Vac_TR | Threephasegridvoltage | — | 0.1 V | — | — | — | — |
| 3041 | Ptousertotal H | Totalforwardpower | — | 0.1 W Total forward power | — | — | — | — |
| 3042 | Ptousertotal L | — | — | — | — | — | — | — |
| 3043 | Ptogridtotal H | Totalreversepower | — | 0.1 W Totalreverse power | — | — | — | — |
| 3044 | Ptogridtotal L | — | — | — | — | — | — | — |
| 3045 | Ptoloadtotal H | Totalloadpower | — | 0.1 W Total load power | — | — | — | — |
| 3046 | Ptoloadtotal L | — | — | — | — | — | — | — |
| 3047 | Timetotal H | Worktimetotal | — | 0.5 s | — | — | — | — |
| 3048 | Timetotal L | — | — | — | — | — | — | — |
| 3049 | Eactoday H | Todaygenerateenergy | — | 0.1 k Wh Today generate energy | — | — | — | — |
| 3050 | Eactoday L | — | — | — | — | — | — | — |
| 3051 | Eactotal H | Totalgenerateenergy | — | 0.1 k Wh Total generate | — | — | — | — |
| 3052 | Eactotal L | — | — | — | — | — | — | — |
| 3053 | Epv_total H | PVenergytotal | — | 0.1 k Wh PVenergy total | — | — | — | — |
| 3054 | Epv_total L | — | — | — | — | — | — | — |
| 3055 | Epv 1_today H | PV 1 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3056 | Epv 1_today L | — | — | — | — | — | — | — |
| 3057 | Epv 1_total H | PV 1 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3058 | Epv 1_total L | — | — | — | — | — | — | — |
| 3059 | Epv 2_today H | PV 2 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3060 | Epv 2_today L | — | — | — | — | — | — | — |
| 3061 | Epv 2_total H | PV 2 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3062 | Epv 2_total L | — | — | — | — | — | — | — |
| 3063 | Epv 3_today H | PV 3 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3064 | Epv 3_today L | — | — | — | — | — | — | — |
| 3065 | Epv 3_total H | PV 3 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3066 | Epv 3_total L | — | — | — | — | — | — | — |
| 3067 | Etouser_today H | Todayenergytouser | — | 0.1 k Wh Todayenergy touser | — | — | — | — |
| 3068 | Etouser_today L | — | — | — | — | — | — | — |
| 3069 | Etouser_total H | Totalenergytouser | — | 0.1 k Wh Totalenergy touser | — | — | — | — |
| 3070 | Etouser_total L | — | — | — | — | — | — | — |
| 3071 | Etogrid_today H | Todayenergytogrid | — | 0.1 k Wh Todayenergy togrid | — | — | — | — |
| 3072 | Etogrid_today L | — | — | — | — | — | — | — |
| 3073 | Etogrid_total H | Totalenergytogrid | — | 0.1 k Wh Totalenergy togrid | — | — | — | — |
| 3074 | Etogrid_total L | — | — | — | — | — | — | — |
| 3075 | Eload_today H | Todayenergyofuserload | — | 0.1 k Wh Todayenergy ofuserload | — | — | — | — |
| 3076 | Eload_today L | — | — | — | — | — | — | — |
| 3077 | Eload_total H | Totalenergyofuserload | — | 0.1 k Wh Totalenergy ofuserload | — | — | — | — |
| 3078 | Eload_total L | — | — | — | — | — | — | — |
| 3079 | Epv 4_today H | PV 4 energytoday | — | 0.1 k Wh | — | — | — | — |
| 3080 | Epv 4_today L | — | — | — | — | — | — | — |
| 3081 | Epv 4_total H | PV 4 energytotal | — | 0.1 k Wh | — | — | — | — |
| 3082 | Epv 4_total L | — | — | — | — | — | — | — |
| 3083 | Epv_today H | PVenergytoday | — | 0.1 k Wh | — | — | — | — |
| 3084 | Epv_today L | — | — | — | — | — | — | — |
| 3085 | Reserved | — | — | — | — | — | — | — |
| 3086 | Derating Mode | Derating Mode | — | 0:c NOTDerate 1:c PVHigh Der ate 2: c Power Con stant Derate 3: c Grid VHigh Derate 4:c Freq High D erate 5:c Dc Soure M ode Derate 6:c Inv Tempr D erate 7:c Active Pow er Order 8:c Load Speed Process 9:c Over Back by Time 10:c Internal T empr Derate 11:c Out Temp r Derate 12:c Line Impe Calc Derate 13: c Parallel A nti Backflow D erate 14:c Local Anti Backflow Dera te 15:c Bdc Load P ri Derate 16:c Chk CTErr Derate | — | — | — | — |
| 3087 | ISO | PVISOvalue | — | 1 KΩ | — | — | — | — |
| 3088 | DCI_R | RDCICurr | — | 0.1 m A | — | — | — | — |
| 3089 | DCI_S | SDCICurr | — | 0.1 m A | — | — | — | — |
| 3090 | DCI_T | TDCICurr | — | 0.1 m A | — | — | — | — |
| 3091 | GFCI | GFCICurr | — | 1 m A | — | — | — | — |
| 3092 | Bus Voltage | totalbusvoltage | — | 0.1 V | — | — | — | — |
| 3093 | Temp 1 | Invertertemperature | — | 0.1℃ | — | — | — | — |
| 3094 | Temp 2 | Theinside IPMininvertertemperature | — | 0.1℃ | — | — | — | — |
| 3095 | Temp 3 | Boosttemperature | — | 0.1℃ | — | — | — | — |
| 3096 | Temp 4 | Reserved | — | 0.1℃ | — | — | — | — |
| 3097 | Temp 5 | Commmunicationbroadtemperature | — | 0.1℃ | — | — | — | — |
| 3098 | PBus Voltage | PBusinside Voltage | — | 0.1 V | — | — | — | — |
| 3099 | NBus Voltage | NBusinside Voltage | — | 0.1 V | — | — | — | — |
| 3100 | IPF | Inverteroutput PFnow | — | 0-20000 | — | — | — | — |
| 3101 | Real OPPercent | Real Outputpower Percent | — | 1% 1~100 | — | — | — | — |
| 3102 | OPFullwatt H | Output Maxpower Limited | — | 0.1 W Output Maxpower Limited | — | — | — | — |
| 3103 | OPFullwatt L | — | — | — | — | — | — | — |
| 3104 | Standby Flag | Inverterstandbyflag | — | bitfield bit 0:turn off Order; bit 1:PVLow; bit 2:AC Volt/Freq outofscope; bit 3~bit 7 : Reserved | — | — | — | — |
| 3105 | Fault Maincode | Inverterfaultmaincode | — | — | — | — | — | — |
| 3106 | Warn Maincode | Inverter Warningmaincode | — | — | — | — | — | — |
| 3107 | Fault Subcode | Inverterfaultsubcode | — | bitfield | — | — | — | — |
| 3108 | Warn Subcode | Inverter Warningsubcode | — | bitfield | — | — | — | — |
| 3109 | — | — | — | bitfield | — | — | — | — |
| 3110 | — | — | — | bitfield | — | — | — | — |
| 3111 | uw Present FFTVa lue[CHANNEL_A ] | Present FFTValue[CHANNEL_A] | — | bitfield | — | — | — | — |
| 3112 | b Afci Status | AFCIStatus | — | 0 : waiting state 1:self-check 2:Detection of arcing state 3:faultstate 4 : update state | — | — | — | — |
| 3113 | uw Strength[CHA NNEL_A] | AFCIStrength[CHANNEL_A] | — | — | — | — | — | — |
| 3114 | uw Self Check Val ue[CHANNEL_A] | AFCISelf Check[CHANNEL_A] | — | — | — | — | — | — |
| 3115 | inv start delay time | invstartdelaytime | — | 1 S invstartdelay time | — | — | — | — |
| 3116 | Reserved | — | — | — | — | — | — | — |
| 3117 | Reserved | — | — | — | — | — | — | — |
| 3118 | BDC_On Off State | BDCconnectstate | — | 0:No BDC Connect 1:BDC 1 Connect 2:BDC 2 Connect 3:BDC 1+BDC 2 Connect | — | — | — | — |
| 3119 | Dry Contact State | Currentstatusof Dry Contact | — | Current status of Dry Contact 0:turnoff; 1:turnon; | — | — | — | — |
| 3120 | Reserved | — | — | — | — | — | — | — |
| 3121 | Pself H | self-usepower | — | 0.1 W | — | — | — | — |
| 3122 | Pself L | — | — | — | — | — | — | — |
| 3123 | Esys_today H | Systemenergytoday | — | 0.1 kwh | — | — | — | — |
| 3124 | Esys_today L | — | — | — | — | — | — | — |
| 3125 | Edischr_today H | Todaydischargeenergy | — | 0.1 k Wh Today discharge energy | — | — | — | — |
| 3126 | Edischr_today L | — | — | — | — | — | — | — |
| 3127 | Edischr_total H | Totaldischargeenergy | — | 0.1 k Wh Total discharge energy | — | — | — | — |
| 3128 | Edischr_total L | — | — | — | — | — | — | — |
| 3129 | Echr_today H | Chargeenergytoday | — | 0.1 k Wh Charge energytoday | — | — | — | — |
| 3130 | Echr_today L | — | — | — | — | — | — | — |
| 3131 | Echr_total H | Chargeenergytotal | — | 0.1 k Wh Charge energytotal | — | — | — | — |
| 3132 | Echr_total L | — | — | — | — | — | — | — |
| 3133 | Eacchr_today H | Todayenergyof ACcharge | — | 0.1 k Wh Todayenergy of ACcharge | — | — | — | — |
| 3134 | Eacchr_today L | — | — | — | — | — | — | — |
| 3135 | Eacchr_total H | Totalenergyof ACcharge | — | 0.1 k Wh Totalenergy of ACcharge | — | — | — | — |
| 3136 | Eacchr_total L | — | — | — | — | — | — | — |
| 3137 | Esys_total H | — | — | — | — | — | — | — |
| 3138 | Esys_total L | Totalenergyofsystemoutput\ | — | 0.1 k Wh | — | — | — | — |
| 3139 | Eself_today H | Todayenergyof Selfoutput | — | 0.1 k Wh | — | — | — | — |
| 3140 | Eself_today L | — | — | — | — | — | — | — |
| 3141 | Eself_total H | Totalenergyof Selfoutput | — | 0.1 kwh | — | — | — | — |
| 3142 | Eself_total L | — | — | — | — | — | — | — |
| 3143 | Reserved | — | — | — | — | — | — | — |
| 3144 | Priority | Word Mode | — | 0 Load First 1 Battery Firs t 2 Grid First | — | — | — | — |
| 3145 | EPSFac | UPSfrequency | — | 0.01 Hz | — | — | — | — |
| 3146 | EPSVac 1 | UPSphase Routputvoltage | — | 0.1 V | — | — | — | — |
| 3147 | EPSIac 1 | UPSphase Routputcurrent | — | 0.1 A | — | — | — | — |
| 3148 | EPSPac 1 H | UPSphase Routputpower | — | 0.1 VA | — | — | — | — |
| 3149 | EPSPac 1 L | — | — | — | — | — | — | — |
| 3150 | EPSVac 2 | UPSphase Soutputvoltage | — | 0.1 V | — | — | — | — |
| 3151 | EPSIac 2 | UPSphase Soutputcurrent | — | 0.1 A | — | — | — | — |
| 3152 | EPSPac 2 H | UPSphase Soutputpower | — | 0.1 VA | — | — | — | — |
| 3153 | EPSPac 2 L | — | — | — | — | — | — | — |
| 3154 | EPSVac 3 | UPSphase Toutputvoltage | — | 0.1 V | — | — | — | — |
| 3155 | EPSIac 3 | UPSphase Toutputcurrent | — | 0.1 A | — | — | — | — |
| 3156 | EPSPac 3 H | UPSphase Toutputpower | — | 0.1 VA | — | — | — | — |
| 3157 | EPSPac 3 L | — | — | — | — | — | — | — |
| 3158 | EPSPac H | UPSoutputpower | — | 0.1 VA | — | — | — | — |
| 3159 | EPSPac L | — | — | — | — | — | — | — |
| 3160 | Loadpercent | Loadpercentof UPSouput | — | 0.10% | — | — | — | — |
| 3161 | PF | Powerfactor | — | 0.1 | — | — | — | — |
| 3162 | DCV | DCvoltage | — | 1 m V | — | — | — | — |
| 3163 | Reserved | — | — | — | — | — | — | — |
| 3164 | New Bdc Flag | Whethertoparse BDCdataseparately | — | 0:Don'tneed 1:need | — | — | — | — |
| 3165 | BDCDerating Mo de | BDCDerating Mode: 0:Normal,unrestricted 1:Standbyorfault 2:Maximumbatterycurrentlimit (discharge) 3:Batterydischarge Enable(Discharge) 4:Highbusdischargederating | — | — | — | — | — | — |
| 3166 | Sys State_Mode | Systemwork Stateandmode The upper 8 bitsindicatethemode; 0:Nochargeanddischarge; 1:charge; 2:Discharge; Thelower 8 bitsrepresentthestatus; 0:Standby Status; 1:Normal Status; 2:Fault Status 3:Flash Status; | — | BDC 1 | — | — | — | — |
| 3167 | Fault Code | Storgedevicefaultcode | — | — | — | — | — | — |
| 3168 | Warn Code | Storgedevicewarningcode | — | — | — | — | — | — |
| 3169 | Vbat | Batteryvoltage | — | 0.01 V | — | — | — | — |
| 3170 | Ibat | Batterycurrent | — | 0.1 A | — | — | — | — |
| 3171 | SOC | Stateofcharge Capacity | — | 1% | — | — | — | — |
| 3172 | Vbus 1 | Total BUSvoltage | — | 0.1 V | — | — | — | — |
| 3173 | Vbus 2 | Onthe BUSvoltage | — | 0.1 V | — | — | — | — |
| 3174 | Ibb | BUCK-BOOSTCurrent | — | 0.1 A | — | — | — | — |
| 3175 | Illc | LLCCurrent | — | 0.1 A | — | — | — | — |
| 3176 | Temp A | Temperture A | — | 0.1℃ | — | — | — | — |
| 3177 | Temp B | Temperture B | — | 0.1℃ | — | — | — | — |
| 3178 | Pdischr H | Dischargepower | — | 0.1 W | — | — | — | — |
| 3179 | Pdischr L | — | — | — | — | — | — | — |
| 3180 | Pchr H | Chargepower | — | 0.1 W | — | — | — | — |
| 3181 | Pchr L | — | — | — | — | — | — | — |
| 3182 | Edischr_total H | Dischargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3183 | Edischr_total L | — | — | — | — | — | — | — |
| 3184 | Echr_total H | Chargetotalenergyofstorgedevice | — | 0.1 k Wh | — | — | — | — |
| 3185 | Echr_total L | — | — | — | — | — | — | — |
| 3186 | Reserved | Reserved | — | — | — | — | — | — |
| 3187 | BDC 1_Flag | BDCmark(chargeanddischarge, faultalarmcode) Bit 0:Charge En;BDCallowscharging Bit 1:Discharge En;BDCallows discharge Bit 2~7:Resvd;reserved Bit 8~11:Warn Sub Code;BDC sub-warningcode Bit 12~15:Fault Sub Code;BDC sub-errorcode | — | — | — | — | — | — |
| 3188 | Vbus 2 | Lower BUSvoltage | — | 0.1 V | — | — | — | — |
| 3189 | Bms Max Volt Cell No | Bms Max Volt Cell No | — | — | — | — | — | — |
| 3190 | Bms Min Volt Cell No | Bms Min Volt Cell No | — | — | — | — | — | — |
| 3191 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | — | — |
| 3192 | Bms Max Cell Tem p | Bms Max Cell Temp | — | 0.1°C | — | — | — | — |
| 3193 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | 0.1°C | — | — | — | — |
| 3194 | Bms Max Cell Tem p | Bms Max Cell Temp | — | — | — | — | — | — |
| 3195 | Bms Battery Avg T emp | Bms Battery Avg Temp | — | — | — | — | — | — |
| 3196 | Bms Max SOC | Bms Max SOC | — | 1% | — | — | — | — |
| 3197 | Bms Min SOC | Bms Min SOC | — | 1% | — | — | — | — |
| 3198 | Parallel Battery N um | Parallel Battery Num | — | — | — | — | — | — |
| 3199 | Bms Derate Reas on | Bms Derate Reason | — | — | — | — | — | — |
| 3200 | Bms Gauge FCC (Ah) | Bms Gauge FCC(Ah) | — | — | — | — | — | — |
| 3201 | Bms Gauge RM (Ah) | Bms Gauge RM(Ah) | — | — | — | — | — | — |
| 3202 | Bms Error | BMSProtect 1 | — | — | — | — | — | — |
| 3203 | Bms Warn | BMSWarn 1 | — | — | — | — | — | — |
| 3204 | Bms Fault | BMSFault 1 | — | — | — | — | — | — |
| 3205 | Bms Fault 2 | BMSFault 2 | — | — | — | — | — | — |
| 3206 | Reserved | — | — | — | — | — | — | — |
| 3207 | Reserved | — | — | — | — | — | — | — |
| 3208 | Reserved | — | — | — | — | — | — | — |
| 3209 | Reserved | — | — | — | — | — | — | — |
| 3210 | Bat Iso Status | Battery ISOdetectionstatus | — | 0:Not detected 1:Detection completed | — | — | — | — |
| 3211 | Batt Need Charge Request Flag | batteryworkrequest | — | bit 0:1: Prohibit chargin g,0: Allow the chargin g bit 1:1: Enable strong charge, 0: disable strong charge bit 2:1: Enable strong charge 2 0: disable strong charge | — | — | — | — |
| 3212 | BMS_Status | batteryworkingstatus | R | 0:dormancy 1:Charge 2:Discharge 3:free 4:standby 5:Softstart 6:fault 7:update | — | — | — | — |
| 3213 | Bms Error 2 | BMSProtect 2 | R | 1 | — | — | — | — |
| 3214 | Bms Warn 2 | BMSWarn 2 | R | 1 | — | — | — | — |
| 3215 | BMS_SOC | BMSSOC | R | 1% | — | — | — | — |
| 3216 | BMS_Battery Vol t | BMSBattery Volt | R | 0.01 V | — | — | — | — |
| 3217 | BMS_Battery Cur r | BMSBattery Curr | R | 0.01 A | — | — | — | — |
| 3218 | BMS_Battery Te mp | batterycellmaximumtemperature | R | 0.1℃ | — | — | — | — |
| 3219 | BMS_Max Curr | Maximumchargingcurrent | R | 0.01 A | — | — | — | — |
| 3220 | BMS_Max Dischr Curr | Maximumdischargecurrent | R | 0.01 A | — | — | — | — |
| 3221 | BMS_Cycle Cnt | BMSCycle Cnt | R | 1 | — | — | — | — |
| 3222 | BMS_SOH | BMSSOH | R | 1 | — | — | — | — |
| 3223 | BMS_Charge Vol t Limit | Batterychargingvoltagelimitvalue | R | 0.01 V | — | — | — | — |
| 3224 | BMS_Discharge Volt Limit | Batterydischargevoltagelimitvalue | — | — | — | — | — | — |
| 3225 | Bms Warn 3 | BMSWarn 3 | R | 1 | — | — | — | — |
| 3226 | Bms Error 3 | BMSProtect 3 | R | 1 | — | — | — | — |
| 3227 | Reserved | — | — | — | — | — | — | — |
| 3228 | Reserved | — | — | — | — | — | — | — |
| 3229 | Reserved | — | — | — | — | — | — | — |
| 3230 | BMSSingle Volt M ax | BMSBattery Single Volt Max | R | 0.001 V | — | — | — | — |
| 3231 | BMSSingle Volt M in | BMSBattery Single Volt Min | R | 0.001 V | — | — | — | — |
| 3232 | Bat Load Volt | Battery Load Volt | R | 0.01 V [0,650.00] | — | — | — | — |
| 3233 | — | — | — | — | — | — | — | — |
| 3234 | Debugdata 1 | Debugdata 1 | R | — | — | — | — | — |
| 3235 | Debugdata 2 | Debugdata 2 | R | — | — | — | — | — |
| 3236 | Debugdata 3 | Debugdata 3 | R | — | — | — | — | — |
| 3237 | Debugdata 4 | Debugdata 4 | R | — | — | — | — | — |
| 3238 | Debugdata 5 | Debugdata 5 | R | — | — | — | — | — |
| 3239 | Debugdata 6 | Debugdata 6 | R | — | — | — | — | — |
| 3240 | Debugdata 7 | Debugdata 7 | R | — | — | — | — | — |
| 3241 | Debugdata 8 | Debugdata 8 | R | — | — | — | — | — |
| 3242 | Debugdata 9 | Debugdata 9 | R | — | — | — | — | — |
| 3243 | Debugdata 10 | Debugdata 10 | R | — | — | — | — | — |
| 3244 | Debugdata 10 | Debugdata 10 | R | — | — | — | — | — |
| 3245 | Debugdata 12 | Debugdata 12 | R | — | — | — | — | — |
| 3246 | Debugdata 13 | Debugdata 13 | R | — | — | — | — | — |
| 3247 | Debugdata 14 | Debugdata 14 | R | — | — | — | — | — |
| 3248 | Debugdata 15 | Debugdata 15 | R | — | — | — | — | — |
| 3249 | Debugdata 16 | Debugdata 16 | R | — | — | — | — | — |
| 3250 | Pex 1 H | PVinverter 1 outputpower H | R | 0.1 W | — | — | — | — |
| 3251 | Pex 1 L | PVinverter 1 outputpower L | R | 0.1 W | — | — | — | — |
| 3252 | Pex 2 H | PVinverter 2 outputpower H | R | 0.1 W | — | — | — | — |
| 3253 | Pex 2 L | PVinverter 2 outputpower L | R | 0.1 W | — | — | — | — |
| 3254 | Eex 1 Today H | PVinverter 1 energy Today H | R | 0.1 k Wh | — | — | — | — |
| 3255 | Eex 1 Today L | PVinverter 1 energy Today L | R | 0.1 k Wh | — | — | — | — |
| 3256 | Eex 2 Today H | PVinverter 2 energy Today H | R | 0.1 k Wh | — | — | — | — |
| 3257 | Eex 2 Today L | PVinverter 2 energy Today L | R | 0.1 k Wh | — | — | — | — |
| 3258 | Eex 1 Total H | PVinverter 1 energy Total H | R | 0.1 k Wh | — | — | — | — |
| 3259 | Eex 1 Total L | PVinverter 1 energy Total L | R | 0.1 k Wh | — | — | — | — |
| 3260 | Eex 2 Total H | PVinverter 2 energy Total H | R | 0.1 k Wh | — | — | — | — |
| 3261 | Eex 2 Total L | PVinverter 2 energy Total L | R | 0.1 k Wh | — | — | — | — |
| 3262 | uw Bat No | batterypacknumber | R | BDC reports are updated every 15 minutes | — | — | — | — |
| 3263 | Bat Serial Num 1 | Batterypackserialnumber SN[0]SN[1] | R | BDC reports are updated every 15 minutes | — | — | — | — |
| 3264 | Bat Serial Num 2 | Batterypackserialnumber SN[2]SN[3] | R | — | — | — | — | — |
| 3265 | Bat Serial Num 3 | Batterypackserialnumber SN[4]SN[5] | R | — | — | — | — | — |
| 3266 | Bat Serial Num 4 | Batterypackserialnumber SN[6]SN[7] | R | — | — | — | — | — |
| 3267 | Bat Serial Num 5 | Batterypackserialnumber SN[8]SN[9] | R | — | — | — | — | — |
| 3268 | Bat Serial Num 6 | Batterypackserial number SN[10]SN[11] | R | — | — | — | — | — |
| 3269 | Bat Serial Num 7 | Batterypackserial number SN[12]SN[13] | R | — | — | — | — | — |
| 3270 | Bat Serial Num 8 | Batterypackserial number SN[14]SN[15] | R | — | — | — | — | — |
| 3271- 3279 | Reserve | Reserve | — | — | — | — | — | — |
| 3280 | b Clr Today Data Fl ag | Cleardaydataflag | R | Data of the current day that the server | — | — | — | — |
