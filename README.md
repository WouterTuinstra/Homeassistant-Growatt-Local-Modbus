[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Home Assistant Growatt Local Intergration
 Growatt Local is a custom component for Home Assistant that connects directly to your Growatt inverter using the Modbus protocol and supports Serial, TCP and UDP communication layers to connect to your inverter

 This repository is at this moment not part of HACS therefore requiring manual adding this custom repository to HACS.

 This intergration makes use of the *config_flow* and can be configured using the UI no confgration required using the `configration.yaml`

 The only requirement is that you know which Modbus adress the device has the default value would be 1

Currently the communication layer (API) is included in this repository but following the guidelines of HASS they should be seperate