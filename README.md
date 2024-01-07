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
* Protocol version 3.15 used by older models that would support up to two strings
* Protocol version 1.20 used by newer models and larger devices including Storage and Hybrid inverters
* Protocol for Offgrid inverters

Currently the communication layer (API) is included in this repository but following the guidelines of HASS there should be seperate repositories


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
