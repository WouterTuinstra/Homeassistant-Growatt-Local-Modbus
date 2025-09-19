# The Growatt SPH and SPA inverters' modbus register map
<img src='images/img01-inverter.jpg' width='640px'>

These inverters use a different modbus register map from the one found on growatt-esp8266 project.
Below are the registers currently being read by this project and the data they contain.

You can find more information on [Growatt RTU protocol II v1.20 PDF](docs/growatt-inverter-modbus-rtu-protocolii-v120-english.pdf)

## Input registers
```
0   Inverter status (0, 1, 3, 5 & 6)
    0 Standby
    1 Normal / Checking
    3 Error / Fault
    5 Normal, battery and solar online
    6 Normal, only battery online (no solar)

3   Vpv1   (PV1 DC voltage)
4   Ipv1   (PV1 DC current)
5   Ppv1 H
6   Ppv1 L (PV1 power in watts)

7   Vpv2   (PV2 DC voltage)
8   Ipv2   (PV2 DC voltage)
9   Ppv2 H
10  Ppv2 L (PV2 power in watts)

35  Pac H
36  Pac L  (Power output in Watts)
37  Fac    (AC Grid frequency)

38  Vac1   (AC Grid phase 1 voltage)
39  Iac1   (AC Grid phase 1 current)
40  Pac1 H  
41  Pac1 L (AC Grid phase 1 power output in VA)

--------------------------- 8< ------------------------------
If you have a 3 phase inverter you can enable these as well

42  Vac2   (AC Grid phase 2 voltage)
43  Iac2   (AC Grid phase 2 current)
44  Pac2 H  
45  Pac2 L (AC Grid phase 2 power output in VA)

46  Vac3   (AC Grid phase 3 voltage)
47  Iac3   (AC Grid phase 3 current)
48  Pac3 H  
49  Pac3 L (AC Grid phase 3 power output in VA)
--------------------------- 8< ------------------------------

53  Etotal H
54  Etotal L  (total energy produced by inverter [in watts ?])
55  Etoday H
56  Etoday L  (energy produced by inverter today [in watts ?])
57  Ttotal H
58  Ttotal L  (total time inverter running [unknown units])
```

### Temperature registers and other stats
```
93  Temp 1 inverter / ºC
94  Temp 2 inverter IPM / ºC 
95  Temp 3 inverter boost / ºC
96  Temp 4 (reserved and not read)

104 Derating mode

118 Priority 0:LoadF, 1:BatF, 2:GridF
```

### Battery related registers
```
119 Battery type 0:LeadAcid, 1:Lithium 
1009 PdischargeH
1010 PdischargeL
1011 PchargeH
1012 PchargeL
1013 Vbat
1014 SOC
```

### Not used but seem interesting to add in the future
```
BMS related (Pylontech)
1086 BMS_SOC
1087 BMS_BatteryVolt
1088 BMS_BatteryCurr
1089 BMS_BatteryTemp
1090 BMS_MaxCurr (pylon)
```

## Holding registers

Registers of interest start at adress 1070 and go up to 1108. Registers 1110 up to 1118 are only available on SPA inverters which I don't have and can't test right now.
These are R/W registers. When writing to them, the inverter usually takes a few seconds to adapt to the changes.

Here's the current set of holding registers used by this project:

### Grid first related
```
1070  Grid first discharge power rate
1071  Grid first Stop State of Charge
...
1080  Grid first Start Time 1
1081  Grid first Stop Time 1
1082  Grid first Time 1 enable switch
1083  Grid first Start Time 2
1084  Grid first Stop Time 2
1085  Grid first Time 2 enable switch
1086  Grid first Start Time 3
1087  Grid first Stop Time 3
1088  Grid first Time 3 enable switch
...
```

### Battery first related
```
1090  Battery first charge power rate
1091  Battery first Stop State of Charge
1092  Battery first AC charger enable switch
...
1100  Battery first Start Time 1
1101  Battery first Stop Time 1
1102  Battery first Time 1 enable switch
1103  Battery first Start Time 2
1104  Battery first Stop Time 2
1105  Battery first Time 2 enable switch
1106  Battery first Start Time 3
1107  Battery first Stop Time 3
1108  Battery first Time 3 enable switch
...
```

### Load first related (only on SPA inverters)
The SPH inverter assumes that when Battery First and Grid First are not enabled, the user want Load First. So this seems to be the default behaviour.
This means the holding registers below are never read/written on SPH inverters.
```
1110  Load first Start Time 1
1111  Load first Stop Time 1
1112  Load first Time 1 enable switch
1113  Load first Start Time 2
1114  Load first Stop Time 2
1115  Load first Time 2 enable switch
1116  Load first Start Time 3
1117  Load first Stop Time 3
1118  Load first Time 3 enable switch 
```

:warning: I noticed that if you set the inverter to Battery first and the Battery first Time 1 is "00:00 00:00", the inverter will refuse to change and keep working in Load First. The only way I found to make it accept the command and change to Battery first is to set Battery First Time 1 to something "not zero", like "00:00 23:59".

