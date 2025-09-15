# Growatt Local Modbus Integration - Developer & Test Guide

This document explains how to work on the Growatt Local Modbus integration and
its simulator. It covers the repository layout, the devcontainer workflow,
available tooling, how to run automated tests, and how the external RTU broker
fits into development and hardware validation.

The examples focus on the MIN 6000XH-TL inverter because it is currently the
most complete data set, but the same tooling applies to other models once their
register maps are supplied.

---

## 1. Repository layout

```
external/
  Homeassistant-Growatt-Local-Modbus/     Home Assistant integration + simulator
    custom_components/growatt_local/
    testing/
    tests/
  growatt-rtu-broker/                     External broker (submodule or clone)
```

Key helper scripts:

- `testing/modbus_simulator.py` - Modbus TCP/RTU simulator with dataset support.
- `testing/read_registers.py` - Direct serial probe script that loads the
  integration code without Home Assistant.
- `testing/compact_capture.py` - Converts broker JSONL captures into dataset
  JSON files suitable for the simulator.

---

## 2. Getting the code

Clone the Home Assistant fork (contains the integration, datasets, and
recommended devcontainer).

```
git clone -b growatt-local-test https://github.com/l4m4re/HA-core.git
cd HA-core
```

The broker resides in `external/growatt-rtu-broker` alongside this repository.
Two options are supported:

1. **Git submodule (preferred for automation):**
   ```
   git submodule update --init --recursive external/growatt-rtu-broker
   ```
2. **Manual clone:**
   ```
   cd external
   git clone https://github.com/l4m4re/growatt-rtu-broker
   ```

Both layouts give the simulator predictable access to the broker sources when
needed for dataset capture. Keep broker dependencies out of the Home Assistant
integration itself.

---

## 3. Devcontainer workflow

The repository ships with a devcontainer that installs all Python dependencies,
starts Home Assistant, and exposes the simulator tools.

1. Open the repository in VS Code.
2. Reopen in the devcontainer when prompted.
3. Inside the container shell:
   ```
   cd external/Homeassistant-Growatt-Local-Modbus/testing
   python modbus_simulator.py
   ```
   This launches a Modbus TCP simulator on port 5020 using the default dataset.
4. Start Home Assistant Core (if it is not already running):
   ```
   hass -c config
   ```
5. In the Home Assistant UI add the integration, choose **TCP**, and point it to
   `localhost:5020` with unit id 1.

The simulator supports both TCP and serial transports, optional mutators, and
multiple device profiles. See section 5 for details.

---

## 4. Running the test suite

The pytest collection focuses on simulator behaviour, dataset loaders, and
supporting utilities. From the repository root (host or container):

```
pytest external/Homeassistant-Growatt-Local-Modbus/tests
```

Relevant fixtures spin up the simulator automatically. Use
`pytest -k <pattern>` to scope tests while iterating.

---

## 5. Simulator reference

`testing/modbus_simulator.py` offers several options:

- `--dataset` to load a specific dataset JSON.
- `--device` to pick an alternate register map (for example `min`, `tl_xh`).
- `--force-deterministic` to seed predictable values for tests.
- `--mutator` to load mutation plug-ins that adjust register values over time.
- `--serial` / `--tcp` to choose the transport the simulator exposes.

The dataset format is a JSON object with `holding` and `input` dictionaries whose
keys are register numbers stored as strings. Missing entries default to zero.

Example CLI usage:

```
python testing/modbus_simulator.py --dataset testing/datasets/min_6000xh_tl.json
python testing/modbus_simulator.py --tcp 0.0.0.0:5020 --mutator testing.mutators.energy_tick
```

---

## 6. Dataset management

### 6.1 Default dataset

`testing/datasets/min_6000xh_tl.json` is the baseline dataset bundled with the
simulator. It represents a realistic snapshot of a MIN 6000XH-TL inverter. Older
snapshots (such as `scan3.txt`) are retained only for historical reference; new
work should rely on the capture workflow below.

### 6.2 Capturing from live hardware

The preferred pipeline for refreshing datasets is:

1. Run the broker in capture mode against live hardware (see section 7 for
   deployment options).
2. Point Home Assistant or a probe script at the broker so it exchanges Modbus
   traffic with the inverter.
3. Use `testing/compact_capture.py` to transform the JSONL capture into a
   dataset.
   ```
   python testing/compact_capture.py --in session.jsonl --device min_6000xh_tl --out testing/datasets/min_6000xh_tl.json --source-tag "capture $(date +%F)"
   ```
4. Commit the updated dataset and document the provenance in
   `testing/growatt_registers.md` if new registers are mapped.

`compact_capture.py` keeps the last value seen for each register per function
(read input and read holding). The optional `_source` tag records where the data
came from.

---

## 7. Broker integration

The external broker mediates between the RS-485 inverter bus, the ShineWiFi
serial dongle, and TCP clients such as Home Assistant or analysis tools.

### 7.1 Deployment on Home Assistant OS

`external/growatt-rtu-broker/docker-compose.yml` runs the broker beside Home
Assistant on a supervised Raspberry Pi:

1. Copy the `growatt-rtu-broker` directory to
   `/mnt/data/supervisor/homeassistant/growatt-rtu-broker` using the Advanced SSH
   add-on.
2. In that directory configure environment variables in `.env` or the shell:
   - `INV_DEV` -> inverter serial path (for example `/dev/serial/by-path/...`).
   - `SHINE_DEV` -> Shine dongle path; use the same value as `INV_DEV` to disable
     Shine pass-through.
   - Optional overrides: `TCP_BIND`, `MIN_PERIOD`, `RTIMEOUT`, `LOG_PATH`.
3. Start the container:
   ```
   docker compose up -d
   ```

The container binds port 5020 on the host and logs JSONL traffic to
`/var/log/growatt_broker.jsonl`. Point local or remote Home Assistant instances
at `HOST_IP:5020` using TCP transport.

### 7.2 Remote devcontainer against live hardware

A devcontainer session can connect to a broker that runs on your Home Assistant
host. Configure the integration inside the container with:

- Transport: TCP
- Host: the LAN IP of the machine running the broker
- Port: 5020 (or the value you configured)
- Unit id: match the inverter address (usually 1)

This mirrors the Shine + Home Assistant sharing use case while keeping physical
serial access restricted to the broker host.

### 7.3 Dataset capture

To record live traffic for later replay, enable capture mode when launching the
broker (see broker documentation for current flags) or tail the JSONL wire log.
Then run `testing/compact_capture.py` as described in section 6.2.

### 7.4 Multi-inverter roadmap

Issue #53 highlights the need to expose multiple virtual serial endpoints so
separate Home Assistant integrations can share one RS-485 line without fighting
for `/dev/ttyUSB0`. Planned broker work will create pseudo terminal devices
(`/run/growatt-broker/inverter<N>`) that funnel requests through the existing
mutex-protected downstream. Until that lands, prefer the TCP transport for
multiple inverters (one broker instance, many HA entries with different unit
ids).

### 7.5 Use cases at a glance

| Scenario                                    | Recommended tool | Mode             |
|---------------------------------------------|------------------|------------------|
| Develop new sensor mapping                  | Simulator        | Dataset          |
| Reverse engineer unknown registers          | Broker           | Capture          |
| Run HA + Shine simultaneously               | Broker           | Live             |
| Devcontainer HA against remote live inverter| Broker           | Live (TCP)       |
| CI regression without hardware              | Simulator        | Dataset          |
| Generate realistic datasets for docs/tests  | Broker + script  | Capture -> Dataset |

---

## 8. Working with live hardware without the broker

`testing/read_registers.py` is a convenience script for quick serial reads when
you do not need Home Assistant running:

```
SERIAL_PORT=/dev/ttyUSB0 python testing/read_registers.py
```

The script auto-detects `/dev/serial/by-id/*` paths, loads the integration's
register definitions, and prints register values. It respects the integration's
scaling logic, making it a useful sanity check before building new entities.

When running on Home Assistant OS, use the Advanced SSH add-on to launch a
Python container that mounts the repository and passes through the serial
device. The legacy instructions from earlier versions (interactive container,
non-interactive one-liner) still apply if needed but are no longer the
recommended workflow now that the broker handles serial access.

**Devcontainer note:** The VS Code container does not expose host USB devices by
default. Either run this script directly on the host (or inside the broker
container) or reconfigure the devcontainer to map the serial device (for example
by adding `--device /dev/ttyUSB0:/dev/ttyUSB0` to the devcontainer settings).
Otherwise the script will fail with `ModbusPortException: USB port /dev/ttyUSB0
is not available`.

---

## 9. Troubleshooting

- **Port busy / cannot open serial** - Stop Home Assistant Core or the broker
  and confirm the device path is correct.
- **Inconsistent values during tests** - Run the simulator with
  `--force-deterministic` and avoid mutators when comparing snapshots.
- **TCP client connection errors** - Verify the broker is listening (e.g.
  `ss -tnlp | grep 5020`) and that firewalls allow access from your devcontainer
  or workstation.
- **Dataset missing registers** - Regenerate the dataset via capture so the last
  observed values are recorded, then update entity mappings accordingly.

---

## 10. Related documentation

- `testing/growatt_registers.md` - Register mapping status and provenance notes.
- `external/growatt-rtu-broker/README.md` - Broker features, deployment, and
  roadmap.
- `AGENTS.md` (both repositories) - Guidance for automated agents and
  contributors about division of responsibilities between the simulator and the
  broker.

Keep this guide up to date as workflows evolve, especially when new capture
features or datasets land.
