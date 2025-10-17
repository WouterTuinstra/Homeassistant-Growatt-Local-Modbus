[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Home Assistant Growatt Local Integration
 Growatt Local is a custom component for Home Assistant that connects directly to your Growatt inverter using the Modbus protocol and supports Serial, TCP and UDP communication layers to connect to your inverter

 This repository is at this moment not part of HACS therefore requiring manual adding this custom repository to HACS.

 This integration makes use of the *config_flow* and can be configured using the UI, so no configuration required using the `configuration.yaml`

 The requirement to be able to uses this integration are:
 * The communication layer and related parameters
 * Modbus address of the device (Default value: 1)
 * Used protocol version by your device

## Protocol version
Currently there are 3 protocol versions supported with this integration:
* RTU Protocol version 3.15 used by older models that would support up to two strings
* RTU Protocol 2 version 1.24 used by newer models and larger devices including Storage and Hybrid inverters
* RTU Protocol for SPH Hybrid/Offgrid inverters version 0.11

Currently the communication layer (API) is included in this repository but following the guidelines of HASS there should be seperate repositories

## Additional functionality of this intergration

Customizable control of the update rate of sensor values.
* A scan interval of all information.
* A seperate scan inverval of main power values

For inverters a optional switch can be set active if you want control when the inverter may produces power to the grid.

## Manual Installation by ssh

1. Open the `\share` directory.
2. If you do not have a `custom_components` directory there, you need to create it.

Optionally, you can choose another directory, but be aware that the ssh add-on is running in a docker container, so
[changes may be lost on reboot](https://community.home-assistant.io/t/user-file-changes-lost-on-reboot/545757/2).

#### Git clone method

This is a preferred method of manual installation, because it allows you to keep the `git` functionality,
allowing you to manually install updates just by running `git pull origin master` from the created directory.

Now you can clone the repository somewhere else and symlink it to Home Assistant like so:

1. Clone the repo.

```shell
git clone https://github.com/WouterTuinstra/Homeassistant-Growatt-Local-Modbus.git
```

2. Create the symlink to `growatt_local` in the configuration directory.
   If you have non standard directory for configuration, use it instead.

```shell
ln -s /share/custom_components/Homeassistant-Growatt-Local-Modbus/custom_components/growatt_local /config/custom_components/growatt_local
```

# Example: Testing the API and Requesting Register Values Without Home Assistant

You can test the API directly without Home Assistant by running a Python script. This is useful for development, debugging, or exploring register values.


## Example: Reading Register Values

1. Clone this repository if you have not already:

   ```shell
   git clone https://github.com/WouterTuinstra/Homeassistant-Growatt-Local-Modbus.git
   ```

2. Navigate to the `custom_components/growatt_local/API` directory.
3. Ensure you have Python 3.8+ installed.
4. Install the required dependency:

   ```shell
   pip install pymodbus
   ```

5. Run the following script (adjust the serial port and device type as needed):

```python
import asyncio
from growatt import GrowattSerial, GrowattDevice, DeviceTypes
from utils import RegisterKeys

# Set up the connection to your inverter
growatt = GrowattDevice(
    GrowattSerial("/dev/ttyUSB0"),  # Change to your serial port
    DeviceTypes.HYBRIDE_120,        # Change to your device type
    1                               # Modbus address (default: 1)
)

async def main():
    await growatt.connect()
    # Request input registers 0-29
    result = await growatt.update(RegisterKeys(input=set(range(0, 30))))
    print(result)

asyncio.run(main())
```

## Customizing Register Requests

- To request different registers, modify the `RegisterKeys` input set.
- You can also request holding registers by adding `holding={...}` to `RegisterKeys`.
- Example to request input registers 0-10 and holding registers 100-110:

```python
result = await growatt.update(RegisterKeys(
    input=set(range(0, 11)),
    holding=set(range(100, 111))
))
```

## Notes

- Make sure your user has permission to access the serial port.
- For TCP/UDP, use `GrowattTCP` or `GrowattUDP` instead of `GrowattSerial`.