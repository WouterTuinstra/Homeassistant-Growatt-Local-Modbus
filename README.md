[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Home Assistant Growatt Local Intergration
 Growatt Local is a custom component for Home Assistant that connects directly to your Growatt inverter using the Modbus protocol and supports Serial, TCP and UDP communication layers to connect to your inverter

 This repository is at this moment not part of HACS therefore requiring manual adding this custom repository to HACS.

 This intergration makes use of the *config_flow* and can be configured using the UI no confgration required using the `configration.yaml`

 The requirement to be able to uses this intergration are:
 * The communication layer and related parameters
 * Modbus address of the device (Default value: 1)
 * Used protocol version by your device

## Protocol version
Currently there are 2 protocol versions supported with this intergration:
* Protocol version 3.15 used by older models that would support up to two strings
* Protocol version 1.20 used by newer models and larger devices

Note currently only supporting inverters adding support for storage devices is can be realized.

Currently the communication layer (API) is included in this repository but following the guidelines of HASS there should be seperate repositories