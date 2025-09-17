
# Growatt Local Modbus Integration — Developer & Test Guide

This guide describes how to use, test, and extend the Growatt Local Modbus integration and simulator, with a focus on the MIN 6000XH-TL inverter. It covers devcontainer usage, simulator operation, pytest, broker synergy, and register mapping.

---

## Devcontainer Workflow (Recommended)

1. **Clone the devcontainer fork:**
  ```bash
  git clone -b growatt-local-test https://github.com/l4m4re/HA-core.git
  cd HA-core
  ```

2. **Open in VS Code (with devcontainer support):**
  - VS Code will prompt to reopen in the container.
  - All dependencies are pre-installed.

3. **Run the simulator:**
  ```bash
  cd external/Homeassistant-Growatt-Local-Modbus
  python -m growatt_broker.simulator.modbus_simulator
  ```
  - By default, this simulates a MIN 6000XH-TL inverter on TCP port 5020.

4. **Start Home Assistant Core:**
  ```bash
  hass -c config
  ```
  - Open Home Assistant in your browser (usually at `http://localhost:8123`).

5. **Add the Growatt device in Home Assistant:**
  - Use TCP transport.
  - Host: `localhost`
  - Port: `5020`
  - Slave address: `1`

## Register Map Completeness

- The register mapping for MIN 6000XH-TL is complete as far as currently determined. See [`growatt_registers.md`](growatt_registers.md) for details.

## Simulator Usage

- The simulator (`growatt_broker.simulator.modbus_simulator`) supports static and deterministic datasets, mutation plug-ins, and is used for both manual and automated tests.
- By default, it simulates a MIN 6000XH-TL with battery.
- Use the `--force-deterministic` flag for stable test values.
- See below for advanced usage, mutation plug-ins, and dataset provenance.

## Pytest Environment

- Run tests with:
  ```bash
  pytest external/Homeassistant-Growatt-Local-Modbus/tests
  ```
- Several tests are provided, including register value checks and unique ID validation.

## Broker Synergy

- The project is designed to work with a separate broker (not included directly), which can generate datasets for the simulator.
- The broker is **not** a runtime or test dependency.
- See below for details on dataset provenance and broker usage policy.

---

## 0) Prerequisites

* You’re running **Home Assistant OS** or **Supervised** on a Raspberry Pi.
* Your Growatt inverter is connected via **USB‑RS485** to the Pi.
* You can access the Pi via the **Advanced SSH & Web Terminal** add‑on.

---

## 1) Install & configure the Advanced SSH add‑on

1. In Home Assistant: **Settings → Add‑ons → Add‑on Store →** install **SSH & Web Terminal (Community)**.
2. Open the add‑on **Configuration** and set at least one of:

   * `password: <your-strong-password>` **or** add your public key in `authorized_keys`.
3. **Disable Protection mode** (toggle off) so the Docker CLI can talk to the host daemon.
4. Start the add‑on and open the Web Terminal. If you see the limited `ha >` prompt, type `login` to drop to the host shell.

> **Note**: The HA OS config directory on the host is `/mnt/data/supervisor/homeassistant`. Inside add‑ons it’s often bind‑mounted as `/config`. For Docker `-v` binds, **always use the host path** (`/mnt/data/supervisor/homeassistant/...`).

---

## 2) Put the repo in a persistent location

Clone your repo under the HA config directory so it survives reboots:

```bash
cd /mnt/data/supervisor/homeassistant
# Your repo should contain custom_components/growatt_local and read_registers.py
git clone -b fix/min-6000xh https://github.com/l4m4re/Homeassistant-Growatt-Local-Modbus growatt-local
```

The script path will then be `/mnt/data/supervisor/homeassistant/growatt-local/read_registers.py`.

---

## 3) Find your serial device

In the **host shell** (not inside a container):

```bash
ls -l /dev/serial/by-id/  # preferred stable path (if present)
ls -l /dev/ttyUSB*        # fallback path
```

If `/dev/serial/by-id` isn’t available inside a minimal container, use `/dev/ttyUSB0` (or your actual tty) in the `--device` mapping and in the `SERIAL_PORT` env var.

---

## 4) Run the script in a clean Docker container (interactive)

1. Stop HA Core (frees the serial port):

```bash
ha core stop
```

2. Launch an interactive Python 3.11 container with your code mounted and the serial device passed through:

```bash
REPO=/mnt/data/supervisor/homeassistant/growatt-local
SER=/dev/ttyUSB0   # or your /dev/serial/by-id/… path; inside the container it will also be /dev/ttyUSB0

docker run -it --rm \
  --device=$SER:/dev/ttyUSB0 \
  -v "$REPO":/app -w /app \
  python:3.11 bash
```

3. Inside the container, install deps and run:

```bash
pip install --upgrade pip
pip install "pymodbus[serial]>=3.8,<3.9"
export PYTHONPATH=/app
SERIAL_PORT=/dev/ttyUSB0 python /app/read_registers.py
```

4. When finished, `exit`, then:

```bash
ha core start
```

---

## 5) Non‑interactive one‑liner (copy/paste)

```bash
REPO=/mnt/data/supervisor/homeassistant/growatt-local
SER=/dev/ttyUSB0
ha core stop && \
  docker run --rm -it \
    --device=$SER:/dev/ttyUSB0 \
    -v "$REPO":/app -w /app \
    python:3.11 sh -lc 'pip install -q "pymodbus[serial]>=3.8,<3.9" && PYTHONPATH=/app SERIAL_PORT=/dev/ttyUSB0 python /app/read_registers.py' && \
  ha core start
```

* Change `SER` to match your device.
* If you prefer the by‑id path and it exists on the host, you can bind it directly:

  ```bash
  --device=/dev/serial/by-id/usb-…:/dev/ttyUSB0
  ```

---

## 6) About the script

The provided **`read_registers.py`**:

* Bootstraps imports for `custom_components/growatt_local/API` without loading Home Assistant.
* Auto‑detects `/dev/serial/by-id/*` on the host if available; otherwise uses `/dev/ttyUSB0`. You can override with `SERIAL_PORT=/your/device`.
* Connects using: 115200 8N1, Modbus address 1, device type `HYBRID_120_TL_XH`.
* Scans the TL‑XH register windows: `0–124`, `3000–3124`, `3125–3249`, `3250–3374` and prints a table with Address, Name, and Value.

> The mapping names come from the integration’s `input_register` descriptions. Unmapped addresses show as `?` with `-` value.

---

## 7) Troubleshooting

**Port busy / cannot open serial**

* Stop HA Core: `ha core stop`.
* Ensure no other add‑on (e.g., ser2net) is holding the port.
* Verify the device appears in the container: `ls -l /dev/ttyUSB0`.

**No `/dev/serial/by-id` in container**

* Use `/dev/ttyUSB0` in both `--device` and `SERIAL_PORT`.

**`ModuleNotFoundError: pymodbus…`**

* Re‑install: `pip install "pymodbus[serial]>=3.8,<3.9"` (inside the container you run in).

**Permission denied**

* Using Docker `--device` avoids udev group issues. If you still see perms errors, confirm the device mapping and that HA Core is stopped.

**Keep your host clean**

* This approach installs Python packages only **inside the ephemeral container**; your HA OS host remains untouched.

---

## 8) Optional: VS Code debugging against HA on the Pi

If you also want to debug your **custom component** while HA runs on the Pi:

1. Add to `/config/configuration.yaml` on the Pi:

```yaml
debugpy:
  start: true
  wait: false
logger:
  default: info
  logs:
    custom_components.growatt_local: debug
    pymodbus: debug  # optional but very useful
```

2. In VS Code on your laptop, create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to HA on Pi (debugpy)",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "<PI_IP>", "port": 5678 },
      "pathMappings": [
        { "localRoot": "${workspaceFolder}", "remoteRoot": "/config" }
      ]
    }
  ]
}
```

3. Put your integration on the Pi at `/config/custom_components/growatt_local`, restart HA, then **Attach**.

> Combine this with the Docker runner above for quick register peeks when HA isn’t running.

---

## 9) Safety notes

* Always **restart HA Core** after tests so automations resume.
* Double‑check the Modbus address, port, and wiring (A/B swapped is a common culprit).
* Keep Protection mode **off** only while you need Docker CLI access; turn it back on afterwards if desired.

---

## 10) Commands reference (copy‑ready)

```bash
# Paths
REPO=/mnt/data/supervisor/homeassistant/growatt-local
SER=/dev/ttyUSB0   # or /dev/serial/by-id/usb-…

# Stop Home Assistant Core (frees the serial port)
ha core stop

# Interactive container
docker run -it --rm --device=$SER:/dev/ttyUSB0 -v "$REPO":/app -w /app python:3.11 bash
# Inside container
pip install --upgrade pip
pip install "pymodbus[serial]>=3.8,<3.9"
export PYTHONPATH=/app
SERIAL_PORT=/dev/ttyUSB0 python /app/read_registers.py
# Exit container, then
ha core start

# Non-interactive one-liner
ha core stop && docker run --rm -it --device=$SER:/dev/ttyUSB0 -v "$REPO":/app -w /app python:3.11 \
  sh -lc 'pip install -q "pymodbus[serial]>=3.8,<3.9" && PYTHONPATH=/app SERIAL_PORT=/dev/ttyUSB0 python /app/read_registers.py' && ha core start
```

## Parsing register specification

`parse_registers.py` converts the in-repo documentation
`growatt_registers.md` into machine readable JSON files. Run from this
directory:

```bash
python parse_registers.py
```

The script writes four outputs:

* `holding_min.json`
* `holding_tl_xh.json`
* `input_min.json`
* `input_tl_xh.json`

After generating new definitions, copy them into `../external/growatt-rtu-broker/growatt_broker/simulator/` so the shared simulator picks up the updates.

Each entry records register number, function code, length, scale, unit,
and description for the corresponding device type.

---

## Dataset provenance (simulation)

The default simulator dataset `growatt_broker/simulator/datasets/min_6000xh_tl.json` was generated from
`scan3.txt` contained in this repository under `python-modbus-scanner/`.
That scan originated from (and the scanner utility lives at):

  https://github.com/l4m4re/python-modbus-scanner

`scan3.txt` only logs registers with non-zero values (plus some negatives), so
the dataset represents a realistic snapshot of a running **MIN 6000XH‑TL**.

If you regenerate it, you can run:

```bash
python testing/build_dataset_from_scan.py \
  --scan-file testing/python-modbus-scanner/scan3.txt \
  --out ../external/growatt-rtu-broker/growatt_broker/simulator/datasets/min_6000xh_tl.json
```

Then restart any running simulator instance.

**Note:** The full broker project is only used to generate static datasets for the simulator. All dry-run and container testing should use the Modbus simulator provided by the broker package (`python -m growatt_broker.simulator.modbus_simulator`). Do not use the broker directly for development or testing in this repository.

To annotate a dataset with a provenance tag without breaking the loader you
may add a top‑level `_source` field, e.g.:

```jsonc
{
  "_source": "Derived from scan3.txt (python-modbus-scanner commit <hash>)",
  "holding": { ... },
  "input": { ... }
}
```

The simulator ignores unknown top‑level keys.

---

## 11) Broker ↔ Simulator synergy proposal

A separate companion project (Modbus Workbench, formerly Growatt RTU Broker) can complement this repository without being merged into it. Keeping concerns separated reduces review friction while unlocking advanced workflows.

### Roles at a glance
- This repo (integration + simulator):
  - Defines register maps / ATTR_* constants.
  - Provides static & replayable datasets for dry runs (CI, dev container).
  - Offers tooling to parse protocol specs and build JSON datasets.
- Modbus Workbench project (separate repo):
  - Mediates a *live* RS‑485 inverter connection and (optionally) the ShineWiFi dongle simultaneously.
  - Exposes a Modbus TCP endpoint for Home Assistant (and other tools) while enforcing safe pacing.
  - (Capture mode) Records every successful response into an incremental dataset you can feed back into this simulator.

### Unified backend model (concept)
```
Backend (abstract)
  read_input(unit, addr, count) -> list[int]
  read_holding(unit, addr, count) -> list[int]
  write_single(...)
  write_multiple(...)

Implementations:
  LiveSerialBackend (broker)
  DatasetBackend (simulator)
  CaptureBackend (wraps LiveSerialBackend, stores dataset deltas)
```
Both simulator and broker CLIs choose the backend; higher‑level frontends (Modbus TCP server, Shine pass‑through) remain unchanged.

### Capture → dataset workflow
1. Run broker in capture mode while HA (or any Modbus client) polls.
2. Broker appends JSONL events (unit, func, addr, values, timestamp).
3. A helper script (shared or here) compacts events into `holding` / `input` dicts, preserving last‑seen value per register.
4. Write `../external/growatt-rtu-broker/growatt_broker/simulator/datasets/<device>.json` (optionally add `_source`).
5. Simulator consumes the new dataset for offline regression or CI.

### Why keep projects separate?
- Different release cadence (broker is operational infra; integration is HA‑facing).
- Easier upstream PR acceptance (no serial concurrency code inside the HA custom component repo).
- Enables non‑Home‑Assistant users (pure Modbus tooling) to reuse the broker.

### Example use cases
| Scenario | Tool | Mode |
|----------|------|------|
| Develop new sensor mapping | Simulator | dataset
| Reverse engineer unknown registers | Broker | capture
| Run HA + Shine simultaneously (shared RS‑485) | Broker | live
| CI regression without hardware | Simulator | dataset
| Generate realistic snapshot for docs | Broker -> script | capture→dataset

### Proposed roadmap
1. Broker repo: introduce `DatasetBackend` & `CaptureBackend` (no breaking changes).
2. Export a simple dataset capture CLI: `growatt-broker capture --out session.jsonl`.
3. Add compaction script here: `python testing/compact_capture.py --in session.jsonl --out ../external/growatt-rtu-broker/growatt_broker/simulator/datasets/min_6000xh_tl_new.json`.
4. Extend simulator to accept a mutation plug‑in (e.g., auto‑increment energy counters) for long‑running test realism.
5. Add README section (this one) linking broker usage; document optional Modbus TCP integration.
6. Provide a minimal Home Assistant add‑on definition for the broker (optional future).
7. Optional: shared tiny PyPI package (`growatt-rtu-core`) with CRC, framing, backend ABC to eliminate duplication.

### Minimal dataset capture JSONL shape (example)
```
{"ts":"2025-09-13T12:34:56.789","unit":1,"func":4,"addr":0,"count":124,"regs":[...]}
{"ts":"2025-09-13T12:34:57.820","unit":1,"func":3,"addr":331,"count":2,"regs":[5075,0]}
```

### Compaction heuristics
- Keep last value per (func, addr+index).
- Optionally discard pure zero blocks except when a non‑zero was previously observed (avoids sparse noise).
- Preserve negative values and large jumps (potential fault codes).

### Integration README note (future PR)
Add a short paragraph: “If you run the optional Modbus Workbench (formerly Growatt RTU Broker), configure this integration in TCP mode pointing at the broker host:port to enable simultaneous Shine + HA access.”

---

## 12) Using the external RTU Broker from a Dev Container or Test Run

You can point the dev container (or a local laptop) at a **live inverter** through the **external Modbus Workbench** (formerly Growatt RTU Broker) instead of the in‑repo simulator.

### 12.1 Start (or verify) the broker on your HA host
Assuming the broker runs on the Home Assistant machine and exposes Modbus TCP on port 5020:

```bash
# On the HA host (example)
# Broker already launched earlier, or:
# growatt-broker --inverter /dev/ttyUSB0 --shine /dev/ttyUSB1 --baud 9600 --bytes 8E1 --tcp 0.0.0.0:5020
ss -tnlp | grep 5020   # should show LISTEN
```

Make sure your development machine (laptop / dev container) can reach the HA host’s IP on that port.

### 12.2 Dev container: configure integration against broker
Inside the VS Code dev container (or any HA Core instance you run locally):
1. Start Home Assistant (dev container already does this via `hass --script`).
2. In the UI add the integration “Growatt Local Modbus”.
3. Choose **TCP** as connection type.
4. Set Host = `HA_HOST_IP` (the machine running the broker) and Port = `5020`.
5. Keep Modbus address = `1` (unless your inverter address differs).

No USB devices need to be mapped into the dev container; all serial handling is performed remotely by the broker.

### 12.3 Running pytest against the live broker
If you want selected tests to use the broker instead of the simulator:
1. Stop (or avoid) the simulator fixtures if they auto‑start.
2. Provide environment variables consumed by a custom fixture (recommended):

```bash
export GROWATT_LIVE_HOST=192.168.1.50
export GROWATT_LIVE_PORT=5020
export GROWATT_LIVE_UNIT=1
pytest -k live --maxfail=1
```

If such a fixture does not yet exist, a simple pattern you can add (example only):

```python
# tests/fixtures_live.py
import os, pytest
from pymodbus.client import AsyncModbusTcpClient

@pytest.fixture(scope="session")
async def live_modbus():
    host = os.environ.get("GROWATT_LIVE_HOST")
    port = int(os.environ.get("GROWATT_LIVE_PORT", 5020))
    client = AsyncModbusTcpClient(host, port=port)
    await client.connect()
    yield client
    client.close()
```

Then a test can directly query registers to sanity‑check connectivity:

```python
async def test_live_read_basic(live_modbus):
    rr = await live_modbus.read_input_registers(0, count=10, device_id=1)
    assert hasattr(rr, "registers")
```

### 12.4 Switching between simulator and broker
| Mode | Action |
|------|--------|
| Simulator (offline) | Run existing `start_simulator` fixture / script |
| Live broker | Skip simulator fixture; set integration to TCP host:5020 |
| Capture future dataset | Run broker in capture mode (planned) then compact JSONL → dataset |

### 12.5 Recommended workflow during mapping changes
1. Run broker live; browse new / unknown registers with a raw Modbus probe (or enhancement to `probe_simulator.py` adding TCP mode).
2. Add new `GrowattDeviceRegisters` to the appropriate device type file.
3. Add sensor entity descriptions.
4. Restart HA in the dev container (or use Reload) pointing at the broker—new sensors appear if keys resolve.
5. (Optional) Capture a snapshot to evolve the simulator dataset for regression tests.

### 12.6 Notes / Caveats
- Latency: Live broker round‑trip will be slightly higher than local simulator; keep test timeouts modestly larger.
- Exclusivity: Broker must be the **only** RTU master; do not connect the inverter directly to another serial client simultaneously.
- Consistency: The broker may pace (throttle) requests; tests expecting instantaneous multi‑burst reads should be tolerant of minor delays.

### 12.7 Future enhancements (roadmap tie‑in)
- Add `--capture` mode to broker and `compact_capture.py` here (see Section 11 roadmap step 2–3).
- Provide a `--tcp-host/--tcp-port` option for `probe_simulator.py` so the same probe script works against simulator **and** broker without code changes.
- Add a pytest marker (e.g. `@pytest.mark.live_broker`) to selectively include live tests in CI (skipped by default unless env vars set).

---

## 13) Adding the external RTU Broker as a Git Submodule (for agents / automation)

To let automated agents (or CI) seamlessly use the **external Modbus Workbench** (formerly Growatt RTU Broker) alongside this repository—without merging code—add it as a **git submodule**. This preserves clear boundaries but gives local tooling a predictable path.

### 13.1 Add submodule
Choose a target path (example: `external/growatt-rtu-broker`):

```bash
git submodule add https://github.com/your-org-or-user/growatt-rtu-broker external/growatt-rtu-broker
git commit -m "chore: add growatt-rtu-broker submodule"
```

# Already present in this branch via .gitmodules
# To initialize after cloning:
git submodule update --init --recursive external/growatt-rtu-broker
```

Later clones need:
```bash
git clone <this-repo>
cd <this-repo>
git submodule update --init --recursive
```

### 13.2 Recommended directory layout
```
Homeassistant-Growatt-Local-Modbus/
  custom_components/
  testing/
  external/
    growatt-rtu-broker/
```
An agent can detect presence of the broker by checking for `external/growatt-rtu-broker/pyproject.toml` (or `setup.cfg`).

**Automation / agent hint:** Because `.gitmodules` is committed, any CI or AI agent cloning this branch only needs to run `git submodule update --init --recursive` to fetch the private broker project (provided SSH key / token access is configured for `git@github.com:l4m4re/...`).

### 13.3 Dev container integration (optional)
Add to a future devcontainer postCreateCommand (example):
```bash
pip install -e external/growatt-rtu-broker
```
This makes the broker CLI (e.g. `growatt-broker`) available inside the container for live or capture modes.

### 13.4 Using broker from tests
Environment switch pattern (no code change needed in core tests):
```bash
export GROWATT_BROKER_PATH=external/growatt-rtu-broker
export GROWATT_LIVE_HOST=127.0.0.1
export GROWATT_LIVE_PORT=5020
pytest -k live_broker
```
A fixture can:
1. If `GROWATT_BROKER_PATH` is set and no TCP listener found, spawn the broker subprocess (`subprocess.Popen([...])`).
2. Wait for TCP port readiness.
3. Yield host/port to tests.
4. Terminate broker after session.

### 13.5 Capture + compact workflow via submodule
```bash
# Start broker in capture mode (planned feature)
growatt-broker --inverter /dev/ttyUSB0 --capture session.jsonl --tcp 0.0.0.0:5020 &
# Run HA or probe tooling for N minutes
python testing/compact_capture.py --in session.jsonl --out ../external/growatt-rtu-broker/growatt_broker/simulator/datasets/min_6000xh_tl_new.json --device min_6000xh_tl --source-tag "capture $(date +%F)"
```
Produces a dataset JSON you can rename / replace after validation.

**If --out omitted** the default path is:
```
../external/growatt-rtu-broker/growatt_broker/simulator/datasets/<device>.json
```

---

## 15) Simulator mutation plug‑ins (dynamic values)

The simulator can optionally apply *mutation plug‑ins* each tick to make register values change over time (useful for UI demos or stressing logic expecting deltas).

### 15.1 Plug‑in API
A plug‑in is referenced with `--mutator module[:attr]` and must provide either:
- A callable `mutate(registers: dict[str, dict[int,int]], tick: int) -> None`, OR
- A class named in the attr position exposing `.mutate(registers, tick)`.

`registers` contains two dicts: `{'holding': {...}, 'input': {...}}` (integer keys).
`tick` increments once per simulator loop (currently 1 second in the placeholder loop).

### 15.2 Sample plug‑in
See `testing/mutators/sample_mutator.py`:
- Class `EnergyIncrement` bumps holding register 331 by 5 each tick and energy total registers (>=1050) every 6 ticks.
- Function `mutate()` increments holding register 30.

### 15.3 Usage examples
Increment totals using the class:
```bash
python -m growatt_broker.simulator.modbus_simulator --mutator testing.mutators.sample_mutator:EnergyIncrement
```
Use the function form:
```bash
python -m growatt_broker.simulator.modbus_simulator --mutator testing.mutators.sample_mutator
```
Combine multiple mutators:
```bash
python -m growatt_broker.simulator.modbus_simulator \
  --mutator testing.mutators.sample_mutator:EnergyIncrement \
  --mutator testing.mutators.sample_mutator
```

### 15.4 Notes
- Mutators run sequentially each tick; later mutators see earlier changes.
- Values are masked to 16‑bit (0xFFFF) after each write.
- Avoid expensive I/O in mutate functions—keep them fast.
- Future enhancement: configurable tick interval & scheduling.

---

## 16) Acknowledgements

Thanks to the Home Assistant community and contributors for their support and for the amazing platform that makes these integrations possible.

---

*End of extended developer & integration notes.*
