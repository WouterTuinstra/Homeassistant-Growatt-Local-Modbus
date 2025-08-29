# README — Run & Debug the Growatt Register Reader on Home Assistant OS (Raspberry Pi)


Note: Quick&Dirty AI generated draft. Stopping HA is not required, but it is
wise to disable the local growatt integration while running the script to avoid
conflicts on the serial port. Most important is how to get the docker python
container up&running.

---

This guide shows how to run the provided `read_registers.py` directly **on your
Home Assistant OS (Pi)** inside a **clean Docker container**, using the
**Advanced SSH & Web Terminal** add‑on. It’s designed for quick register
inspection and for debugging the Growatt Local Modbus integration without
modifying HA Core.

> TL;DR — One‑liner:
>
> ```bash
> REPO=/mnt/data/supervisor/homeassistant/growatt-local
> ha core stop && \
> docker run --rm -it \
>   --device=/dev/ttyUSB0:/dev/ttyUSB0 \
>   -v "$REPO":/app -w /app python:3.11 \
>   sh -lc 'pip install -q "pymodbus[serial]>=3.8,<3.9" && PYTHONPATH=/app SERIAL_PORT=/dev/ttyUSB0 python /app/read_registers.py' && \
> ha core start
> ```

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

Each entry records register number, function code, length, scale, unit,
and description for the corresponding device type.

---

*Happy hacking and safe debugging!*
