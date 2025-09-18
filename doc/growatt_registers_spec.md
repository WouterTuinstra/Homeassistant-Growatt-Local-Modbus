# Growatt Modbus register reference

Generated on ``2025-09-18T19:47:56+00:00`` using `generate_register_spec.py`.

## Data type catalogue

| Identifier | Kind | Registers | Notes |
| --- | --- | --- | --- |
| ascii_8 | ascii | 8 | ASCII text |
| baud_rate_select | enum | 1 | 3 values |
| binary_flag | enum | 1 | 2 values |
| device_type_code | callable | 1 | — |
| firmware_blocks | ascii_segments | 6 | inverter×3; control×3 |
| lcd_language | enum | 1 | 9 values |
| model_code | callable_per_family | 2 | — |
| mppt_phase_tuple | callable | 1 | — |
| s32_div10 | scaled | 2 | signed /10 |
| s32_div7200 | scaled | 2 | signed /7200 |
| safety_function_flags | bitfield | 1 | 11 bit flags |
| serial_ascii_5 | ascii | 5 | ASCII text |
| u16 | integer | 1 | — |
| u16_div10 | scaled | 1 | unsigned /10 |
| u16_div100 | scaled | 1 | unsigned /100 |
| u16_div1000 | scaled | 1 | unsigned /1000 |

## Holding registers

### Communication

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 22 | Modbus baud rate | Selects the RTU baud rate used by the RS485 interface. | baud_rate_select | — | R/W | — | — |
| 30 | Slave address | Modbus device address (1–247). | u16 | — | R/W | — | — |

### Control

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Remote enable | Primary run/stop flag. Set to 1 to allow AC output; 0 places the inverter in standby. | binary_flag | — | R/W | Storage MIX/SPA/SPH, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | inverter_enabled |

### Grid Protection

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Grid safety function enables | Bitfield enabling optional grid-code features such as ride-through curves, DRMS, and safety relays. Bits set to 1 activate the corresponding function. | safety_function_flags | — | R/W | — | — |

### Identity

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9–14 | Firmware revisions | Registers 9–14 store two ASCII revision blocks: 9–11 report the inverter firmware, while 12–14 hold the control/communication board firmware. | firmware_blocks | — | R | Storage MIX/SPA/SPH, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | firmware |
| 23–27 | Serial number | 10-character factory serial number (two ASCII characters per register). | serial_ascii_5 | — | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | serial number |
| 28–29 | Model code | Encodes inverter hardware options; decoding varies per product family. | model_code | — | R | Storage MIX/SPA/SPH, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | Inverter model |
| 34–41 | Manufacturer string | Eight registers containing an ASCII manufacturer descriptor. | ascii_8 | — | R | — | — |
| 43 | Device type | Growatt device type identifier mapped to human-friendly product names. | device_type_code | — | R | Storage MIX/SPA/SPH, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | device type code |
| 44 | Trackers / phases | High byte = MPPT tracker count, low byte = AC phase count. | mppt_phase_tuple | — | R | Storage MIX/SPA/SPH, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | number of trackers and phases |
| 73 | Modbus Version | Reported Modbus protocol revision (raw value divided by 100). | u16_div100 | — | R | TL3/MAX/MID/MAC three-phase | modbus version |
| 88 | Modbus Version | Reported Modbus protocol revision (raw value divided by 100). | u16_div100 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | modbus version |
| 3001–3015 | Serial number | 10-character factory serial number (two ASCII characters per register). | serial_ascii_5 | — | R | Storage MIX/SPA/SPH | serial number |

### Maintenance

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | Firmware update trigger | Writing the documented magic value starts the bootloader firmware update routine. | u16 | — | R/W | — | — |
| 32 | Reset user configuration | Clears user-tuned parameters (grid codes, limits) back to defaults when written with the documented key. | u16 | — | R/W | — | — |
| 33 | Factory reset | Restores factory configuration and clears history counters when executed with the vendor key. | u16 | — | R/W | — | — |

### Uncategorised

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3049 | AC Charge | Value backing integration attribute `ac_charge_enabled`. | u16 | — | R/W | Storage MIX/SPA/SPH | ac_charge_enabled |

## Input registers

### Uncategorised

| Address | Name | Description | Data type | Unit | Access | Families | Attributes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Status code | Value backing integration attribute `status_code`. | u16 | — | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | status_code |
| 1–2 | Input 1 Voltage, Input Power | Provides multiple integration attributes: `input_1_voltage`, `input_power` | s32_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_voltage, input_power |
| 2 | PV2 voltage | Value backing integration attribute `input_2_voltage`. | u16_div10 | V | R | Off-grid SPF | input_2_voltage |
| 3–4 | Input 1 Power, Input 1 Voltage | Provides multiple integration attributes: `input_1_power`, `input_1_voltage` | s32_div10 | W | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_power, input_1_voltage |
| 4 | PV1 buck current | Value backing integration attribute `input_1_amperage`. | u16_div10 | A | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_amperage |
| 5–6 | Input 1 Power, Input 2 Power | Provides multiple integration attributes: `input_1_power`, `input_2_power` | s32_div10 | W | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_power, input_2_power |
| 7 | Input 1 Amperage, Input 2 Voltage | Provides multiple integration attributes: `input_1_amperage`, `input_2_voltage` | u16_div10 | A | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_amperage, input_2_voltage |
| 8 | PV2 buck current | Value backing integration attribute `input_2_amperage`. | u16_div10 | A | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_2_amperage |
| 9–10 | Input 2 Power, Output Active Power | Provides multiple integration attributes: `input_2_power`, `output_active_power` | s32_div10 | W | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_2_power, output_active_power |
| 11–12 | Input 3 Voltage, Output Power | Provides multiple integration attributes: `input_3_voltage`, `output_power` | s32_div10 | V | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_3_voltage, output_power |
| 12 | Input 3 Amperage | Value backing integration attribute `input_3_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | input_3_amperage |
| 13–14 | Charge Power, Grid Frequency, Input 3 Power | Provides multiple integration attributes: `charge_power`, `grid_frequency`, `input_3_power` | s32_div10 | W | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | charge_power, grid_frequency, input_3_power |
| 14 | Output voltage | Value backing integration attribute `output_1_voltage`. | u16_div10 | V | R | TL3/MAX/MID/MAC three-phase | output_1_voltage |
| 15 | Input 4 Voltage, Output 1 Amperage | Provides multiple integration attributes: `input_4_voltage`, `output_1_amperage` | u16_div10 | V | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_4_voltage, output_1_amperage |
| 16–17 | Input 4 Amperage, Output 1 Power | Provides multiple integration attributes: `input_4_amperage`, `output_1_power` | s32_div10 | A | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_4_amperage, output_1_power |
| 17–18 | Battery Voltage, Input 4 Power | Provides multiple integration attributes: `battery_voltage`, `input_4_power` | s32_div10 | V | R | Off-grid SPF, TL-X/TL-XH single-phase | battery_voltage, input_4_power |
| 18 | Output 2 Voltage, Soc | Provides multiple integration attributes: `output_2_voltage`, `soc` | — | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | output_2_voltage, soc |
| 19 | Bus Voltage, Input 5 Voltage, Output 2 Amperage | Provides multiple integration attributes: `bus_voltage`, `input_5_voltage`, `output_2_amperage` | u16_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | bus_voltage, input_5_voltage, output_2_amperage |
| 20–21 | Grid Voltage, Input 5 Amperage, Output 2 Power | Provides multiple integration attributes: `grid_voltage`, `input_5_amperage`, `output_2_power` | s32_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | grid_voltage, input_5_amperage, output_2_power |
| 21–22 | Grid Frequency, Input 5 Power | Provides multiple integration attributes: `grid_frequency`, `input_5_power` | s32_div10 | Hz | R | Off-grid SPF, TL-X/TL-XH single-phase | grid_frequency, input_5_power |
| 22 | Output 1 Voltage, Output 3 Voltage | Provides multiple integration attributes: `output_1_voltage`, `output_3_voltage` | u16_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | output_1_voltage, output_3_voltage |
| 23 | Input 6 Voltage, Output 3 Amperage, Output Frequency | Provides multiple integration attributes: `input_6_voltage`, `output_3_amperage`, `output_frequency` | u16_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_6_voltage, output_3_amperage, output_frequency |
| 24–25 | Input 6 Amperage, Output 3 Power, Output Dc Voltage | Provides multiple integration attributes: `input_6_amperage`, `output_3_power`, `output_dc_voltage` | s32_div10 | A | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_6_amperage, output_3_power, output_dc_voltage |
| 25–26 | Input 6 Power, Inverter Temperature | Provides multiple integration attributes: `input_6_power`, `inverter_temperature` | s32_div10 | W | R | Off-grid SPF, TL-X/TL-XH single-phase | input_6_power, inverter_temperature |
| 26–27 | Dc Dc Temperature, Output Energy Today | Provides multiple integration attributes: `dc_dc_temperature`, `output_energy_today` | s32_div10 | °C | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | dc_dc_temperature, output_energy_today |
| 27 | Input 7 Voltage, Load Percent | Provides multiple integration attributes: `input_7_voltage`, `load_percent` | u16_div10 | V | R | Off-grid SPF, TL-X/TL-XH single-phase | input_7_voltage, load_percent |
| 28–29 | Battery Port Voltage, Input 7 Amperage, Output Energy Total | Provides multiple integration attributes: `battery_port_voltage`, `input_7_amperage`, `output_energy_total` | s32_div10 | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | battery_port_voltage, input_7_amperage, output_energy_total |
| 29–30 | Battery Bus Voltage, Input 7 Power | Provides multiple integration attributes: `battery_bus_voltage`, `input_7_power` | s32_div10 | V | R | Off-grid SPF, TL-X/TL-XH single-phase | battery_bus_voltage, input_7_power |
| 30–31 | Running hours | Value backing integration attribute `operation_hours`. | s32_div7200 | h | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | operation_hours |
| 31 | Input 8 voltage | Value backing integration attribute `input_8_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | input_8_voltage |
| 32 | Input 8 Amperage, Inverter Temperature | Provides multiple integration attributes: `input_8_amperage`, `inverter_temperature` | u16_div10 | A | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_8_amperage, inverter_temperature |
| 33–34 | Input 8 Wattage | Value backing integration attribute `input_8_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_8_power |
| 34 | Output amperage | Value backing integration attribute `output_1_amperage`. | u16_div10 | A | R | Off-grid SPF | output_1_amperage |
| 35–36 | Output power | Value backing integration attribute `output_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_power |
| 37 | Grid frequency | Value backing integration attribute `grid_frequency`. | u16_div100 | Hz | R | TL-X/TL-XH single-phase | grid_frequency |
| 38 | Output voltage | Value backing integration attribute `output_1_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | output_1_voltage |
| 39 | Output amperage | Value backing integration attribute `output_1_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | output_1_amperage |
| 40–41 | Fault Code, Output 1 Power | Provides multiple integration attributes: `fault_code`, `output_1_power` | — | — | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | fault_code, output_1_power |
| 41 | Intelligent Power Management temperature | Value backing integration attribute `ipm_temperature`. | u16_div10 | °C | R | TL3/MAX/MID/MAC three-phase | ipm_temperature |
| 42 | Fault Code, Output 2 Voltage, P Bus Voltage | Provides multiple integration attributes: `fault_code`, `output_2_voltage`, `p_bus_voltage` | — | — | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | fault_code, output_2_voltage, p_bus_voltage |
| 43 | N Bus Voltage, Output 2 Amperage, Warning Code | Provides multiple integration attributes: `n_bus_voltage`, `output_2_amperage`, `warning_code` | — | V | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | n_bus_voltage, output_2_amperage, warning_code |
| 44–45 | Output 2 Wattage | Value backing integration attribute `output_2_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_2_power |
| 46 | Output 3 voltage | Value backing integration attribute `output_3_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | output_3_voltage |
| 47 | Constant Power, Derating Mode, Output 3 Amperage | Provides multiple integration attributes: `constant_power`, `derating_mode`, `output_3_amperage` | — | — | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | constant_power, derating_mode, output_3_amperage |
| 48–49 | Input 1 Energy Today, Output 3 Power | Provides multiple integration attributes: `input_1_energy_today`, `output_3_power` | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_1_energy_today, output_3_power |
| 50–51 | PV1 energy produced Lifetime | Value backing integration attribute `input_1_energy_total`. | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | input_1_energy_total |
| 52–53 | PV2 energy produced today | Value backing integration attribute `input_2_energy_today`. | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | input_2_energy_today |
| 53–54 | Energy produced today | Value backing integration attribute `output_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | output_energy_today |
| 54–55 | PV2 energy produced Lifetime | Value backing integration attribute `input_2_energy_total`. | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | input_2_energy_total |
| 55–56 | Total energy produced | Value backing integration attribute `output_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | output_energy_total |
| 56–57 | Charge Energy Today, Input Energy Total | Provides multiple integration attributes: `charge_energy_today`, `input_energy_total` | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | charge_energy_today, input_energy_total |
| 57–58 | Running hours | Value backing integration attribute `operation_hours`. | s32_div7200 | h | R | TL-X/TL-XH single-phase | operation_hours |
| 58–59 | Charge Energy Total, Output Reactive Power | Provides multiple integration attributes: `charge_energy_total`, `output_reactive_power` | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | charge_energy_total, output_reactive_power |
| 59–60 | PV1 energy produced today | Value backing integration attribute `input_1_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_1_energy_today |
| 60–61 | Discharge Energy Today, Output Reactive Energy Today | Provides multiple integration attributes: `discharge_energy_today`, `output_reactive_energy_today` | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | discharge_energy_today, output_reactive_energy_today |
| 61–62 | PV1 energy produced Lifetime | Value backing integration attribute `input_1_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_1_energy_total |
| 62–63 | Discharge Energy Total, Output Reactive Energy Total | Provides multiple integration attributes: `discharge_energy_total`, `output_reactive_energy_total` | s32_div10 | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | discharge_energy_total, output_reactive_energy_total |
| 63–64 | PV2 energy produced today | Value backing integration attribute `input_2_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_2_energy_today |
| 64–65 | Ac Discharge Energy Today, Warning Code | Provides multiple integration attributes: `ac_discharge_energy_today`, `warning_code` | — | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | ac_discharge_energy_today, warning_code |
| 65–66 | Input 2 Energy Total, Warning Value | Provides multiple integration attributes: `input_2_energy_total`, `warning_value` | — | kWh | R | TL3/MAX/MID/MAC three-phase, TL-X/TL-XH single-phase | input_2_energy_total, warning_value |
| 66–67 | Ac Discharge Energy Total, Real Output Power Percent | Provides multiple integration attributes: `ac_discharge_energy_total`, `real_output_power_percent` | — | kWh | R | Off-grid SPF, TL3/MAX/MID/MAC three-phase | ac_discharge_energy_total, real_output_power_percent |
| 67–68 | Input 3 energy today | Value backing integration attribute `input_3_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_3_energy_today |
| 68 | AC charge battery current | Value backing integration attribute `ac_charge_amperage`. | u16_div10 | A | R | Off-grid SPF | ac_charge_amperage |
| 69–70 | Discharge Power, Input 3 Energy Total | Provides multiple integration attributes: `discharge_power`, `input_3_energy_total` | s32_div10 | W | R | Off-grid SPF, TL-X/TL-XH single-phase | discharge_power, input_3_energy_total |
| 71–72 | Input 4 energy today | Value backing integration attribute `input_4_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_4_energy_today |
| 73–74 | Battery Discharge Amperage, Input 4 Energy Total | Provides multiple integration attributes: `battery_discharge_amperage`, `input_4_energy_total` | s32_div10 | A | R | Off-grid SPF, TL-X/TL-XH single-phase | battery_discharge_amperage, input_4_energy_total |
| 75–76 | Input 5 energy today | Value backing integration attribute `input_5_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_5_energy_today |
| 77–78 | Battery Power, Input 5 Energy Total | Provides multiple integration attributes: `battery_power`, `input_5_energy_total` | s32_div10 | W | R | Off-grid SPF, TL-X/TL-XH single-phase | battery_power, input_5_energy_total |
| 79–80 | Input 6 energy today | Value backing integration attribute `input_6_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_6_energy_today |
| 81–82 | Input 6 total energy | Value backing integration attribute `input_6_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_6_energy_total |
| 83–84 | Input 7 energy today | Value backing integration attribute `input_7_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_7_energy_today |
| 85–86 | Input 7 total energy | Value backing integration attribute `input_7_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_7_energy_total |
| 87–88 | Input 8 energy today | Value backing integration attribute `input_8_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_8_energy_today |
| 89–90 | Input 8 total energy | Value backing integration attribute `input_8_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_8_energy_total |
| 91–92 | Total energy input | Value backing integration attribute `input_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_energy_total |
| 93 | Temperature | Value backing integration attribute `inverter_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | inverter_temperature |
| 94 | Intelligent Power Management temperature | Value backing integration attribute `ipm_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | ipm_temperature |
| 95 | Boost temperature | Value backing integration attribute `boost_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | boost_temperature |
| 98 | P-bus voltage | Value backing integration attribute `p_bus_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | p_bus_voltage |
| 99 | N-bus voltage | Value backing integration attribute `n_bus_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | n_bus_voltage |
| 101 | Real power output percentage | Value backing integration attribute `real_output_power_percent`. | u16 | % | R | TL-X/TL-XH single-phase | real_output_power_percent |
| 104 | Derating mode | Value backing integration attribute `derating_mode`. | u16 | — | R | TL-X/TL-XH single-phase | derating_mode |
| 105 | Fault code | Value backing integration attribute `fault_code`. | u16 | — | R | TL-X/TL-XH single-phase | fault_code |
| 110–111 | Warning code | Value backing integration attribute `warning_code`. | u16 | — | R | TL-X/TL-XH single-phase | warning_code |
| 234–235 | Reactive wattage | Value backing integration attribute `output_reactive_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_reactive_power |
| 236–237 | Output Reactive Energy Total | Value backing integration attribute `output_reactive_energy_total`. | s32_div10 | — | R | TL-X/TL-XH single-phase | output_reactive_energy_total |
| 1009–1010 | Battery discharge power | Value backing integration attribute `discharge_power`. | s32_div10 | W | R | Storage MIX/SPA/SPH | discharge_power |
| 1011–1012 | Battery charge power | Value backing integration attribute `charge_power`. | s32_div10 | W | R | Storage MIX/SPA/SPH | charge_power |
| 1014 | SOC | Value backing integration attribute `soc`. | u16 | % | R | Storage MIX/SPA/SPH | soc |
| 1021–1022 | AC to user total | Value backing integration attribute `pac_to_user_total`. | s32_div10 | W | R | Storage MIX/SPA/SPH | pac_to_user_total |
| 1029–1030 | AC to grid total | Value backing integration attribute `pac_to_grid_total`. | s32_div10 | W | R | Storage MIX/SPA/SPH | pac_to_grid_total |
| 1044–1045 | Energy To User (Today) | Value backing integration attribute `energy_to_user_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | energy_to_user_today |
| 1046–1047 | Energy To User (Total) | Value backing integration attribute `energy_to_user_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | energy_to_user_total |
| 1048–1049 | Energy To Grid (Today) | Value backing integration attribute `energy_to_grid_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | energy_to_grid_today |
| 1050–1051 | Energy To Grid (Total) | Value backing integration attribute `energy_to_grid_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | energy_to_grid_total |
| 1052–1053 | Battery Discharged Today | Value backing integration attribute `discharge_energy_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | discharge_energy_today |
| 1054–1055 | Battery Discharged Lifetime | Value backing integration attribute `discharge_energy_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | discharge_energy_total |
| 1056–1057 | Battery Charged Today | Value backing integration attribute `charge_energy_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | charge_energy_today |
| 1058–1059 | Grid Charged Lifetime | Value backing integration attribute `charge_energy_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH | charge_energy_total |
| 3000 | Status code | Value backing integration attribute `status_code`. | u16 | — | R | TL-X/TL-XH single-phase | status_code |
| 3001–3002 | Internal wattage | Value backing integration attribute `input_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_power |
| 3003 | PV1 voltage | Value backing integration attribute `input_1_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | input_1_voltage |
| 3004 | PV1 buck current | Value backing integration attribute `input_1_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | input_1_amperage |
| 3005–3006 | PV1 charge power | Value backing integration attribute `input_1_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_1_power |
| 3007 | PV2 voltage | Value backing integration attribute `input_2_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | input_2_voltage |
| 3008 | PV2 buck current | Value backing integration attribute `input_2_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | input_2_amperage |
| 3009–3010 | PV2 charge power | Value backing integration attribute `input_2_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_2_power |
| 3011 | Input 3 voltage | Value backing integration attribute `input_3_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | input_3_voltage |
| 3012 | Input 3 Amperage | Value backing integration attribute `input_3_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | input_3_amperage |
| 3013–3014 | Input 3 Wattage | Value backing integration attribute `input_3_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_3_power |
| 3015 | Input 4 voltage | Value backing integration attribute `input_4_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | input_4_voltage |
| 3016 | Input 4 Amperage | Value backing integration attribute `input_4_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | input_4_amperage |
| 3017–3018 | Input 4 Wattage | Value backing integration attribute `input_4_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | input_4_power |
| 3021–3022 | Reactive wattage | Value backing integration attribute `output_reactive_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_reactive_power |
| 3023–3024 | Output power | Value backing integration attribute `output_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_power |
| 3025 | Grid frequency | Value backing integration attribute `grid_frequency`. | u16_div100 | Hz | R | TL-X/TL-XH single-phase | grid_frequency |
| 3026 | Output voltage | Value backing integration attribute `output_1_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | output_1_voltage |
| 3027 | Output amperage | Value backing integration attribute `output_1_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | output_1_amperage |
| 3028–3029 | Output 1 Wattage | Value backing integration attribute `output_1_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_1_power |
| 3030 | Output 2 voltage | Value backing integration attribute `output_2_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | output_2_voltage |
| 3031 | Output 2 Amperage | Value backing integration attribute `output_2_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | output_2_amperage |
| 3032–3033 | Output 2 Wattage | Value backing integration attribute `output_2_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_2_power |
| 3034 | Output 3 voltage | Value backing integration attribute `output_3_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | output_3_voltage |
| 3035 | Output 3 Amperage | Value backing integration attribute `output_3_amperage`. | u16_div10 | A | R | TL-X/TL-XH single-phase | output_3_amperage |
| 3036–3037 | Output 3 Wattage | Value backing integration attribute `output_3_power`. | s32_div10 | W | R | TL-X/TL-XH single-phase | output_3_power |
| 3041–3042 | Power to user | Value backing integration attribute `power_to_user`. | s32_div10 | W | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | power_to_user |
| 3043–3044 | Power to grid | Value backing integration attribute `power_to_grid`. | s32_div10 | W | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | power_to_grid |
| 3045–3046 | Power user load | Value backing integration attribute `power_user_load`. | s32_div10 | W | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | power_user_load |
| 3047–3048 | Running hours | Value backing integration attribute `operation_hours`. | s32_div7200 | h | R | TL-X/TL-XH single-phase | operation_hours |
| 3049–3050 | Energy produced today | Value backing integration attribute `output_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | output_energy_today |
| 3051–3052 | Total energy produced | Value backing integration attribute `output_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | output_energy_total |
| 3053–3054 | Total energy input | Value backing integration attribute `input_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_energy_total |
| 3055–3056 | PV1 energy produced today | Value backing integration attribute `input_1_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_1_energy_today |
| 3057–3058 | PV1 energy produced Lifetime | Value backing integration attribute `input_1_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_1_energy_total |
| 3059–3060 | PV2 energy produced today | Value backing integration attribute `input_2_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_2_energy_today |
| 3061–3062 | PV2 energy produced Lifetime | Value backing integration attribute `input_2_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_2_energy_total |
| 3063–3064 | Input 3 energy today | Value backing integration attribute `input_3_energy_today`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_3_energy_today |
| 3065–3066 | Input 3 total energy | Value backing integration attribute `input_3_energy_total`. | s32_div10 | kWh | R | TL-X/TL-XH single-phase | input_3_energy_total |
| 3067–3068 | Energy To User (Today) | Value backing integration attribute `energy_to_user_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | energy_to_user_today |
| 3069–3070 | Energy To User (Total) | Value backing integration attribute `energy_to_user_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | energy_to_user_total |
| 3071–3072 | Energy To Grid (Today) | Value backing integration attribute `energy_to_grid_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | energy_to_grid_today |
| 3073–3074 | Energy To Grid (Total) | Value backing integration attribute `energy_to_grid_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | energy_to_grid_total |
| 3086 | Derating mode | Value backing integration attribute `derating_mode`. | u16 | — | R | TL-X/TL-XH single-phase | derating_mode |
| 3093 | Temperature | Value backing integration attribute `inverter_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | inverter_temperature |
| 3094 | Intelligent Power Management temperature | Value backing integration attribute `ipm_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | ipm_temperature |
| 3095 | Boost temperature | Value backing integration attribute `boost_temperature`. | u16_div10 | °C | R | TL-X/TL-XH single-phase | boost_temperature |
| 3097 | Comm board temperature | Value backing integration attribute `comm_board_temperature`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | comm_board_temperature |
| 3098 | P-bus voltage | Value backing integration attribute `p_bus_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | p_bus_voltage |
| 3099 | N-bus voltage | Value backing integration attribute `n_bus_voltage`. | u16_div10 | V | R | TL-X/TL-XH single-phase | n_bus_voltage |
| 3101 | Real power output percentage | Value backing integration attribute `real_output_power_percent`. | u16 | % | R | TL-X/TL-XH single-phase | real_output_power_percent |
| 3105 | Fault code | Value backing integration attribute `fault_code`. | u16 | — | R | TL-X/TL-XH single-phase | fault_code |
| 3110–3111 | Warning code | Value backing integration attribute `warning_code`. | u16 | — | R | TL-X/TL-XH single-phase | warning_code |
| 3111 | Present FFT A | Value backing integration attribute `present_fft_a`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | present_fft_a |
| 3115 | Inverter start delay | Value backing integration attribute `inv_start_delay`. | u16 | s | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | inv_start_delay |
| 3125–3126 | Battery Discharged Today | Value backing integration attribute `discharge_energy_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | discharge_energy_today |
| 3127–3128 | Battery Discharged Lifetime | Value backing integration attribute `discharge_energy_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | discharge_energy_total |
| 3129–3130 | Battery Charged Today | Value backing integration attribute `charge_energy_today`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | charge_energy_today |
| 3131–3132 | Grid Charged Lifetime | Value backing integration attribute `charge_energy_total`. | s32_div10 | kWh | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | charge_energy_total |
| 3164 | BDC present | Value backing integration attribute `bdc_new_flag`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bdc_new_flag |
| 3169 | Battery voltage | Value backing integration attribute `battery_voltage`. | u16_div100 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | battery_voltage |
| 3170 | Battery current | Value backing integration attribute `battery_current`. | u16_div10 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | battery_current |
| 3171 | SOC | Value backing integration attribute `soc`. | u16 | % | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | soc |
| 3172 | VBUS1 voltage | Value backing integration attribute `vbus1_voltage`. | u16_div10 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | vbus1_voltage |
| 3173 | VBUS2 voltage | Value backing integration attribute `vbus2_voltage`. | u16_div10 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | vbus2_voltage |
| 3174 | Buck/boost current | Value backing integration attribute `buck_boost_current`. | u16_div10 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | buck_boost_current |
| 3175 | LLC current | Value backing integration attribute `llc_current`. | u16_div10 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | llc_current |
| 3176 | Battery temperature A | Value backing integration attribute `battery_temperature_a`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | battery_temperature_a |
| 3177 | Battery temperature B | Value backing integration attribute `battery_temperature_b`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | battery_temperature_b |
| 3178–3179 | Battery discharge power | Value backing integration attribute `discharge_power`. | s32_div10 | W | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | discharge_power |
| 3180–3181 | Battery charge power | Value backing integration attribute `charge_power`. | s32_div10 | W | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | charge_power |
| 3189 | BMS max volt cell no | Value backing integration attribute `bms_max_volt_cell_no`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_volt_cell_no |
| 3190 | BMS min volt cell no | Value backing integration attribute `bms_min_volt_cell_no`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_min_volt_cell_no |
| 3191 | BMS avg temp A | Value backing integration attribute `bms_avg_temp_a`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_avg_temp_a |
| 3192 | BMS max cell temp A | Value backing integration attribute `bms_max_cell_temp_a`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_cell_temp_a |
| 3193 | BMS avg temp B | Value backing integration attribute `bms_avg_temp_b`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_avg_temp_b |
| 3194 | BMS max cell temp B | Value backing integration attribute `bms_max_cell_temp_b`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_cell_temp_b |
| 3195 | BMS avg temp C | Value backing integration attribute `bms_avg_temp_c`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_avg_temp_c |
| 3196 | BMS max SOC | Value backing integration attribute `bms_max_soc`. | u16 | % | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_soc |
| 3197 | BMS min SOC | Value backing integration attribute `bms_min_soc`. | u16 | % | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_min_soc |
| 3198 | Parallel Battery Num | Value backing integration attribute `parallel_battery_num`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | parallel_battery_num |
| 3199 | BMS derate reason | Value backing integration attribute `bms_derate_reason`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_derate_reason |
| 3200 | BMS full charge capacity | Value backing integration attribute `bms_gauge_fcc_ah`. | u16 | Ah | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_gauge_fcc_ah |
| 3201 | BMS remaining capacity | Value backing integration attribute `bms_gauge_rm_ah`. | u16 | Ah | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_gauge_rm_ah |
| 3202 | BMS protect 1 | Value backing integration attribute `bms_protect1`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_protect1 |
| 3203 | BMS warn 1 | Value backing integration attribute `bms_warn1`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_warn1 |
| 3204 | BMS fault 1 | Value backing integration attribute `bms_fault1`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_fault1 |
| 3205 | BMS fault 2 | Value backing integration attribute `bms_fault2`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_fault2 |
| 3210 | Bat Iso Status | Value backing integration attribute `bat_iso_status`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bat_iso_status |
| 3211 | Batt Request Flags | Value backing integration attribute `batt_request_flags`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | batt_request_flags |
| 3212 | BMS status | Value backing integration attribute `bms_status`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_status |
| 3213 | BMS protect 2 | Value backing integration attribute `bms_protect2`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_protect2 |
| 3214 | BMS warn 2 | Value backing integration attribute `bms_warn2`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_warn2 |
| 3215 | BMS SOC | Value backing integration attribute `bms_soc`. | u16 | % | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_soc |
| 3216 | BMS battery voltage | Value backing integration attribute `bms_battery_voltage`. | u16_div100 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_battery_voltage |
| 3217 | BMS battery current | Value backing integration attribute `bms_battery_current`. | u16_div100 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_battery_current |
| 3218 | BMS cell max temperature | Value backing integration attribute `bms_cell_max_temp`. | u16_div10 | °C | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_cell_max_temp |
| 3219 | BMS max charge current | Value backing integration attribute `bms_max_charge_current`. | u16_div100 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_charge_current |
| 3220 | BMS max discharge current | Value backing integration attribute `bms_max_discharge_current`. | u16_div100 | A | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_max_discharge_current |
| 3221 | BMS cycle count | Value backing integration attribute `bms_cycle_count`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_cycle_count |
| 3222 | BMS SOH | Value backing integration attribute `bms_soh`. | u16 | % | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_soh |
| 3223 | BMS charge voltage limit | Value backing integration attribute `bms_charge_volt_limit`. | u16_div100 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_charge_volt_limit |
| 3224 | BMS discharge voltage limit | Value backing integration attribute `bms_discharge_volt_limit`. | u16_div100 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_discharge_volt_limit |
| 3225 | BMS warn 3 | Value backing integration attribute `bms_warn3`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_warn3 |
| 3226 | BMS protect 3 | Value backing integration attribute `bms_protect3`. | u16 | — | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_protect3 |
| 3230 | BMS cell voltage max | Value backing integration attribute `bms_cell_volt_max`. | u16_div1000 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_cell_volt_max |
| 3231 | BMS cell voltage min | Value backing integration attribute `bms_cell_volt_min`. | u16_div1000 | V | R | Storage MIX/SPA/SPH, TL-X/TL-XH single-phase | bms_cell_volt_min |

