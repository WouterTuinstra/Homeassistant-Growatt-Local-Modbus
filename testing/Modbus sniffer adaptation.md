**You:**

I'm thinking about using modbus sniffer to log the communication between the Growatt server and my inverter using a ShineWifi-X dongle, which uses a CH340 usb to serial converter and an esp32 based WiFi module.  I was thinking about using modbus sniffer: https://github.com/snhobbs/ModbusSniffer/blob/main/modbus_sniffer/modbus_sniffer.py  -  However, it seems this supports only one port, while if I want to sniff both the rx and tx of the CH340, I'd need two TTL to USB converters on my computer.  Would it be hard to adapt the modbus sniffer code to support two ports, one for master (CH340 RX) and one for slave (CH340 RX)?

* * *

**ChatGPT:**

Short answer: nope, it’s not hard. You can adapt that sniffer to open **two** serial ports—one “seeing” the master → slave line and one “seeing” the slave → master line—and then merge both byte streams into a single timestamped log while reconstructing Modbus-RTU frames by inter-character gap.

Here’s what you need, both hardware and software.

* * *

Hardware tap (important)
------------------------

* **Where to tap:** you want the **RX pin of each side** (from the perspective of your tap):
    
    * Port A (MASTER line): connect the **RX** of your USB-TTL adapter to the **TX** pin of the CH340 (i.e., the line going from CH340 → ESP32/inverter).
        
    * Port B (SLAVE line): connect the **RX** of a second USB-TTL adapter to the **RX** pin of the CH340 line’s _counterpart_ (i.e., the line coming back ESP32 → CH340). In many boards that’s the ESP32 TX line back to the CH340 RX.
        
* **Never drive the bus:** connect **RX only** on your taps; **do not** connect the tap’s TX.
    
* **Common ground:** tie the GND of both USB-TTL adapters to the device ground.
    
* **Voltage level:** almost certainly **3.3 V UART** inside a ShineWifi-X. Use 3.3 V-safe USB-TTL adapters (not 5 V).
    
* **Loading:** UART inputs are high-impedance; a straight RX tap is fine.
    

If you’d rather sniff **RS-485** on the inverter side instead of the internal CH340↔ESP link, use a high-impedance RS-485 receiver (or two), not TTL.

* * *

Software approach
-----------------

Key bits:

* Open **two** `pyserial` ports with identical settings (baud, parity, stop bits).
    
* Run a tiny per-port reader (threads or `asyncio`) that:
    
    * buffers bytes,
        
    * uses a timer to detect an **end-of-frame** by a gap ≥ **3.5 character times**,
        
    * hands completed frames to a central queue with a **direction tag**.
        
* The main loop pops frames, computes **CRC**, and prints parsed frames with timestamps and direction.
    

Below is a compact, self-contained script you can drop in as `dual_modbus_sniffer.py`. It borrows the “gap-based framing” idea used in many RTU sniffers, but generalized to two ports.

```python
#!/usr/bin/env python3
import sys, time, threading, queue, argparse, binascii
import serial

# ---------- CRC16 (Modbus) ----------
def modbus_crc(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

def crc_ok(frame: bytes) -> bool:
    if len(frame) < 4:
        return False
    body, got = frame[:-2], int.from_bytes(frame[-2:], "little")
    return modbus_crc(body) == got

# ---------- Framer thread ----------
class PortFramer(threading.Thread):
    def __init__(self, ser: serial.Serial, direction: str, outq: queue.Queue,
                 char_time: float, gap_chars: float = 3.5):
        super().__init__(daemon=True)
        self.ser = ser
        self.direction = direction  # "M->S" or "S->M"
        self.outq = outq
        self.char_time = char_time
        self.gap = gap_chars * char_time
        self._buf = bytearray()
        self._last = time.perf_counter()
        self._stop = threading.Event()

    def stop(self): self._stop.set()

    def run(self):
        while not self._stop.is_set():
            n = self.ser.in_waiting
            now = time.perf_counter()
            if n:
                chunk = self.ser.read(n)
                self._buf.extend(chunk)
                self._last = now
            else:
                # no new data: check for frame gap
                if self._buf and (now - self._last) >= self.gap:
                    ts = time.time()
                    frame = bytes(self._buf)
                    self._buf.clear()
                    self.outq.put((ts, self.direction, frame))
                time.sleep(self.char_time * 0.5)  # light polling

# ---------- Helper: parse a minimal RTU PDU preview ----------
def preview_pdu(frame: bytes):
    # Return "addr func ... len" without deep decoding
    if len(frame) < 4:  # address + func + CRC
        return "short"
    addr = frame[0]
    func = frame[1]
    body = frame[2:-2]
    return f"addr={addr}, func=0x{func:02X}, data_len={len(body)}"

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(
        description="Dual-port Modbus RTU sniffer (master and slave RX taps)."
    )
    ap.add_argument("--master-port", required=True, help="Serial port for master->slave line (tap RX on master TX)")
    ap.add_argument("--slave-port",  required=True, help="Serial port for slave->master line (tap RX on slave TX)")
    ap.add_argument("--baud", type=int, default=9600)
    ap.add_argument("--bytes", default="8E1", help="Format like 8N1, 8E1, 8O1. Default 8E1.")
    ap.add_argument("--raw", action="store_true", help="Print only hex lines + direction")
    ap.add_argument("--ts", action="store_true", help="Show UNIX timestamp seconds")
    ap.add_argument("--human-ts", action="store_true", help="Show human-readable time")
    args = ap.parse_args()

    # Parse "8E1"
    databits = int(args.bytes[0])
    parity   = args.bytes[1].upper()
    stopbits = int(args.bytes[2])
    py_parity = {"N": serial.PARITY_NONE, "E": serial.PARITY_EVEN, "O": serial.PARITY_ODD}[parity]
    py_stop   = {1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}[stopbits]

    # Bits per character for gap timing (start + data + parity? + stop)
    bits_per_char = 1 + databits + stopbits + (0 if parity == "N" else 1)
    char_time = bits_per_char / args.baud

    master = serial.Serial(args.master_port, args.baud, bytesize=databits,
                           parity=py_parity, stopbits=py_stop, timeout=0)
    slave  = serial.Serial(args.slave_port,  args.baud, bytesize=databits,
                           parity=py_parity, stopbits=py_stop, timeout=0)

    outq = queue.Queue()
    tM = PortFramer(master, "M->S", outq, char_time)
    tS = PortFramer(slave,  "S->M", outq, char_time)
    tM.start(); tS.start()

    print(f"# Listening @ {args.baud} {args.bytes} | char_time≈{char_time*1e3:.3f} ms | gap≥{3.5*char_time*1e3:.3f} ms")
    print(f"# Master port: {args.master_port} | Slave port: {args.slave_port}")

    try:
        while True:
            ts, direction, frame = outq.get()
            hexline = frame.hex(" ")
            ok = crc_ok(frame)
            ts_parts = []
            if args.ts: ts_parts.append(f"{ts:.6f}")
            if args.human_ts:
                ts_parts.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)))
            ts_str = ("[" + " ".join(ts_parts) + "] ") if ts_parts else ""

            if args.raw:
                print(f"{ts_str}{direction}: {hexline}")
            else:
                pv = preview_pdu(frame)
                print(f"{ts_str}{direction}: {hexline}  | {pv} | CRC={'OK' if ok else 'BAD'}")
    except KeyboardInterrupt:
        pass
    finally:
        tM.stop(); tS.stop()
        tM.join(); tS.join()
        master.close(); slave.close()

if __name__ == "__main__":
    main()
```

### Usage

```bash
python3 dual_modbus_sniffer.py \
  --master-port /dev/ttyUSB0 \
  --slave-port  /dev/ttyUSB1 \
  --baud 9600 \
  --bytes 8E1 \
  --human-ts
```

* If your Growatt link is **8N1** (some are), change `--bytes 8N1`.
    
* For **3.5-char gap detection** to work at other baud rates, just set `--baud` correctly.
    
* Add `--raw` if you want pure direction + hex without commentary.
    

### Notes & gotchas

* **Frame reassembly vs bursts:** if you see split frames, increase the gap to, say, `gap_chars=4.0` inside `PortFramer` or reduce `time.sleep()` there.
    
* **Windows vs Linux:** This uses threads, so it’s cross-platform (no `select()` fd issues).
    
* **CRC errors:** When passively tapping UART you shouldn’t get CRC errors. If you do, check voltage level, ground, or that you tapped the correct line (TX vs RX).
    
* **ESP32 line speed:** ShineWifi-X firmware is often 9600 or 115200; confirm and match both ports.
    

* * *

If you want to keep using the original ModbusSniffer structure you linked, the minimal change is the same principle: instantiate **two** `serial.Serial` objects, spawn **two** readers that call the existing framing logic, and tag frames by source. But practically, the little script above is simpler to drop in for two-port sniffing.

Want me to tailor it to your exact ShineWifi-X board pinout or to log as pcap-ng for Wireshark?

* * *

**You:**

Another option could be to connect the dongle to my HA pi4, which is already connected to the inverter over 485. It could just forward the packages so both HA as well as ShineWifi could operate in parallel.

* * *

**ChatGPT:**

Yes—this can work, but there are two very different ways to do it, and only one is “clean”.

1) Quick-and-dirty: two masters on the same RS-485 bus
------------------------------------------------------

You can physically leave the ShineWiFi-X on the inverter’s RS-485 lines **and** keep HA polling. RS-485 is multi-drop, but **Modbus-RTU assumes a single master**. If both masters poll at the same time you’ll get collisions (garbled frames / CRC errors / timeouts). People sometimes “get away with it” by staggering poll intervals, but it’s not robust and hard to debug.

**Verdict:** possible, but I don’t recommend it.

* * *

2) Clean solution: make the Pi a broker (one master downstream, many clients upstream)
--------------------------------------------------------------------------------------

Put the HA Pi4 in the middle and make **the Pi the _only_ RTU master** that talks to the inverter. Then let _multiple_ upstream clients query _through_ the Pi in a controlled way.

### Hardware hookup

* **Downstream (to inverter):** Pi ↔ (USB-RS485 adapter) ↔ RS-485 A/B on inverter.
    
* **Upstream #1 (Shine dongle):** Plug the ShineWiFi-X into the Pi via USB. It will show up as `/dev/ttyUSBx` (CH340).
    
* **Upstream #2 (Home Assistant):** Point HA at a **Modbus-TCP** endpoint on the Pi (instead of RTU). HA’s Modbus integration works fine as a TCP _client_.
    

### What the broker does

* It listens to the **Shine serial port** and behaves like a transparent “inverter”: when Shine sends a Modbus-RTU request, the broker forwards it downstream to the real inverter, waits for the reply, and sends that back to Shine.
    
* It exposes a **Modbus-TCP server** for HA. HA sends standard Modbus-TCP requests; the broker converts them to RTU on the downstream line, returns the reply.
    
* The broker **serializes** all upstream requests so only **one** is on the wire at a time—no collisions, proper timing, correct inter-frame gaps.
    

### Why this is nicer

* The inverter sees exactly **one** master (the Pi), so there’s no bus contention.
    
* You can add more TCP clients later (Grafana poller, test scripts, etc.) without touching wiring.
    

* * *

Minimal setup that works today
------------------------------

### A. Let HA use Modbus-TCP instead of RTU

In `configuration.yaml`:

```yaml
modbus:
  - name: growatt_tcp
    type: tcp
    host: 127.0.0.1
    port: 5020
    # optional:
    retries: 3
    delay: 2
    timeout: 5
```

### B. Run a small broker on the Pi

Below is a lightweight Python broker that:

* Bridges **Shine serial** ⇄ **inverter RS-485** (RTU↔RTU, transparent).
    
* Serves **Modbus-TCP** on port 5020 for HA (TCP↔RTU).
    

It uses threads and a single queue to **serialize** access to the inverter. (It’s intentionally compact; you can harden it later—timeouts, logging, stats.)

> Save as `growatt_broker.py` and run with:
> 
> ```
> python3 growatt_broker.py \
>   --inverter /dev/ttyUSB485 --baud 9600 --bytes 8E1 \
>   --shine    /dev/ttyUSB_SHINE \
>   --tcp 0.0.0.0:5020
> ```

```python
#!/usr/bin/env python3
import argparse, socket, threading, queue, time
import serial

# ---- Modbus RTU CRC16 ----
def modbus_crc(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if (crc & 1) else (crc >> 1)
    return crc & 0xFFFF

def add_crc(body: bytes) -> bytes:
    c = modbus_crc(body)
    return body + c.to_bytes(2, 'little')

def crc_ok(frame: bytes) -> bool:
    if len(frame) < 4: return False
    return modbus_crc(frame[:-2]) == int.from_bytes(frame[-2:], 'little')

# ---- Framing by inter-character gap (RTU) ----
class RTUFramer:
    def __init__(self, ser: serial.Serial, char_time: float, gap_chars=3.5):
        self.ser = ser
        self.char_time = char_time
        self.gap = gap_chars * char_time
        self.buf = bytearray()
        self.last = time.perf_counter()

    def read_frame(self, timeout=3.0):
        start = time.perf_counter()
        while True:
            n = self.ser.in_waiting
            now = time.perf_counter()
            if n:
                self.buf.extend(self.ser.read(n))
                self.last = now
            else:
                if self.buf and (now - self.last) >= self.gap:
                    frame = bytes(self.buf)
                    self.buf.clear()
                    return frame
                if (now - start) > timeout:
                    # timeout: return whatever we have (might be empty)
                    if self.buf:
                        frame = bytes(self.buf); self.buf.clear()
                        return frame
                    return b""
                time.sleep(self.char_time * 0.5)

# ---- Downstream: the single RTU master port to inverter ----
class Downstream:
    def __init__(self, dev, baud, fmt):
        databits = int(fmt[0]); parity = fmt[1].upper(); stop = int(fmt[2])
        py_par = {'N':serial.PARITY_NONE,'E':serial.PARITY_EVEN,'O':serial.PARITY_ODD}[parity]
        py_stp = {1:serial.STOPBITS_ONE,2:serial.STOPBITS_TWO}[stop]
        self.ser = serial.Serial(dev, baud, bytesize=databits, parity=py_par, stopbits=py_stp, timeout=0)
        bits_per_char = 1 + databits + stop + (0 if parity=='N' else 1)
        self.char_time = bits_per_char / baud
        self.lock = threading.Lock()
        self.framer = RTUFramer(self.ser, self.char_time)

    def transact(self, req: bytes, rtimeout=1.2):
        with self.lock:
            # Flush input to avoid mixing with previous noise
            _ = self.ser.read(self.ser.in_waiting or 0)
            # Write request
            self.ser.write(req)
            self.ser.flush()
            # Read reply frame
            reply = self.framer.read_frame(timeout=rtimeout)
            return reply

# ---- Upstream endpoint: Shine serial (acts like inverter) ----
class ShineEndpoint(threading.Thread):
    def __init__(self, dev, baud, fmt, downstream: Downstream):
        super().__init__(daemon=True)
        databits = int(fmt[0]); parity = fmt[1].upper(); stop = int(fmt[2])
        py_par = {'N':serial.PARITY_NONE,'E':serial.PARITY_EVEN,'O':serial.PARITY_ODD}[parity]
        py_stp = {1:serial.STOPBITS_ONE,2:serial.STOPBITS_TWO}[stop]
        self.ser = serial.Serial(dev, baud, bytesize=databits, parity=py_par, stopbits=py_stp, timeout=0)
        bits_per_char = 1 + databits + stop + (0 if parity=='N' else 1)
        self.framer = RTUFramer(self.ser, bits_per_char / baud)
        self.ds = downstream

    def run(self):
        while True:
            req = self.framer.read_frame(timeout=10.0)
            if not req:
                continue
            # If Shine sent PDU without CRC, ignore; normally it sends full RTU
            if len(req) >= 4 and crc_ok(req):
                resp = self.ds.transact(req)
                if resp:
                    self.ser.write(resp)
                    self.ser.flush()

# ---- Upstream endpoint: Modbus-TCP server for HA ----
# Minimal, single-PDU per connection handler (enough for HA polling).
class TCPServer(threading.Thread):
    def __init__(self, bind_host, bind_port, downstream: Downstream, unit_id_passthrough=True):
        super().__init__(daemon=True)
        self.addr = (bind_host, bind_port)
        self.ds = downstream
        self.unit_id_passthrough = unit_id_passthrough
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(8)

    def run(self):
        while True:
            conn, _ = self.sock.accept()
            threading.Thread(target=self.handle, args=(conn,), daemon=True).start()

    def handle(self, conn: socket.socket):
        try:
            conn.settimeout(3.0)
            while True:
                # MBAP (7 bytes) + PDU
                hdr = self._recv_exact(conn, 7)
                if not hdr: break
                tid = hdr[0:2]; pid = hdr[2:4]; length = int.from_bytes(hdr[4:6],'big'); uid = hdr[6]
                pdu = self._recv_exact(conn, length-1)
                if not pdu: break
                # Convert TCP PDU to RTU ADU: [uid][pdu][crc]
                rtu_req = add_crc(bytes([uid]) + pdu)
                rtu_resp = self.ds.transact(rtu_req)
                if not rtu_resp or len(rtu_resp) < 4 or not crc_ok(rtu_resp):
                    break
                # Convert RTU response back to TCP: MBAP with same TID/PID
                uid2 = rtu_resp[0]
                pdu2 = rtu_resp[1:-2]
                rsp_len = len(pdu2)+1
                mbap = tid + pid + rsp_len.to_bytes(2,'big') + bytes([uid2])
                conn.sendall(mbap + pdu2)
        except Exception:
            pass
        finally:
            try: conn.close()
            except: pass

    @staticmethod
    def _recv_exact(conn: socket.socket, n: int) -> bytes:
        buf = b""
        while len(buf) < n:
            chunk = conn.recv(n - len(buf))
            if not chunk: return b""
            buf += chunk
        return buf

# ---- main ----
def main():
    ap = argparse.ArgumentParser(description="Growatt broker: Shine serial + Modbus-TCP -> single RTU master")
    ap.add_argument("--inverter", required=True, help="Downstream RS-485 serial device")
    ap.add_argument("--shine",    required=True, help="Upstream ShineWiFi-X serial device")
    ap.add_argument("--baud", type=int, default=9600)
    ap.add_argument("--bytes", default="8E1")
    ap.add_argument("--tcp", default="0.0.0.0:5020", help="Bind host:port for Modbus-TCP server")
    args = ap.parse_args()

    host, port = args.tcp.split(":"); port = int(port)

    ds = Downstream(args.inverter, args.baud, args.bytes)
    ShineEndpoint(args.shine, args.baud, args.bytes, ds).start()
    TCPServer(host, port, ds).start()

    print(f"Broker up. Downstream={args.inverter}@{args.baud}/{args.bytes}  Shine={args.shine}  TCP={host}:{port}")
    threading.Event().wait()  # keep main alive

if __name__ == "__main__":
    main()
```

**Notes**

* Set `--baud/--bytes` to match your inverter. Many Growatt use **9600 8E1**, but some are **8N1**.
    
* The Shine dongle usually speaks plain Modbus-RTU to the inverter, so the serial bridge above just forwards frames.
    
* If your HA and Shine hammer the bus, the broker still keeps them orderly—requests are serialized. If you want rate-limiting or caching, it’s easy to add around `Downstream.transact()`.
    

* * *

Which should you pick?
----------------------

* If you just want to “try it tonight,” you _can_ run two masters on RS-485 and see if collisions are rare.
    
* If you want something you can leave running, the **broker** pattern is the right way: Pi is the sole master; both HA and Shine are happy.
    

If you want, I can tweak the broker to also log every request/response pair to a CSV or pcap-ng so you get a clean Modbus trace while you’re at it.

* * *

**You:**

It seems the growatt integration I'm using does indeed support modbus over tcp: https://github.com/l4m4re/Homeassistant-Growatt-Local-Modbus/blob/fix/min-6000xh/custom_components/growatt_local/API/growatt.py 

* * *

**ChatGPT:**

Nice—yep, that custom component does support TCP, so your “Pi-in-the-middle” plan slots in cleanly. The upstream repo explicitly says it supports **Serial, TCP and UDP**, so pointing it at a local TCP endpoint is expected. [GitHub](https://github.com/WouterTuinstra/Homeassistant-Growatt-Local-Modbus?utm_source=chatgpt.com)

Here’s the tidy way to wire it:

Wiring (one master on RS-485)
=============================

* **Downstream (only master):** Pi4 ↔ USB-RS485 ↔ inverter A/B.
    
* **ShineWiFi-X:** plug into the Pi via USB (CH340 shows up as `/dev/ttyUSB*`).
    
* **Home Assistant:** talk **Modbus-TCP** to the Pi (not RTU).
    

Software layout
===============

Run a small broker on the Pi that:

* Accepts **Modbus-TCP** from HA (port e.g. 5020),
    
* Accepts **Modbus-RTU** from the Shine dongle on its serial port,
    
* **Serializes** both toward the single RS-485 line (no collisions), returning replies to the right client.
    

(That’s exactly what the dual-endpoint broker I gave you does. Keep `--baud/--bytes` correct for your inverter, often `9600 8E1`.)

Example:

```bash
python3 growatt_broker.py \
  --inverter /dev/ttyUSB485 --baud 9600 --bytes 8E1 \
  --shine    /dev/ttyUSB_SHINE \
  --tcp      0.0.0.0:5020
```

Home Assistant → point your Growatt Local config at that TCP endpoint (on the same Pi use 127.0.0.1:5020). For HA’s built-in modbus (if you use it for anything), the minimal is:

```yaml
modbus:
  - name: growatt_tcp
    type: tcp
    host: 127.0.0.1
    port: 5020
    timeout: 5
    retries: 3
    delay: 2
```

A quick note on **RTU-over-TCP** vs **Modbus-TCP**
--------------------------------------------------

* Some devices/adapters (EW11, `ser2net`, etc.) give you a **raw socket** that’s just RTU bytes in a TCP stream (often called _rtu-over-tcp_).
    
* **Modbus-TCP** is a different framing (MBAP header).  
    Your broker speaks **Modbus-TCP** to HA (clean & supported broadly) and **pure RTU** on the wire to the inverter/Shine. If you ever choose a raw-tunnel instead (EW11/ser2net), make sure the client is set to _rtu_over_tcp_, not _tcp_. The Growatt Local repo says it supports TCP and UDP, which typically means it can handle those tunnels too; otherwise stick with the broker. [GitHub](https://github.com/WouterTuinstra/Homeassistant-Growatt-Local-Modbus?utm_source=chatgpt.com)
    

Optional: add logging
---------------------

If you want a trace, it’s trivial to log every request/response pair inside `Downstream.transact()` (timestamp, direction, hex, CRC-ok) to CSV or JSON. Say the word and I’ll drop that in.

* * *

**You:**

I like the broker idea. This way, I can also debug the integration code on my pc and connect to the inverter, even while simultaneously the growatt integration and the shinewifi are running, assuming there's enough bandwidth.  The port on the inverter side runs on 11500, btw. That's the advantage of using the usb port over the native 485 port. I can't use the latter, btw, because that's connected to my battery system.

* * *

**ChatGPT:**

Love it — the broker pattern fits your setup perfectly.

A few practical notes and a drop-in plan you can use today:

What you’ll get
===============

* **One master on the wire** (the Pi), so no RS-485 collisions.
    
* **Many upstream clients**: HA (Modbus-TCP), ShineWiFi-X (serial RTU), and your dev PC (Modbus-TCP) all at once.
    
* **Serialized requests** so replies always match the right client.
    

Baud rate on the inverter side
==============================

You said “11500”. If that really is **11500**, Linux + CH340 will still do it. If you meant **115200** (common), use that.  
For **8E1 at 115200**, one character ≈ 11 bits → ~95.5 µs/char; Modbus RTU’s 3.5-char gap ≈ **0.33 ms**. Plenty of bandwidth for multiple clients if you don’t hammer the device with high-rate polls.

How to wire and point clients
=============================

1. **Downstream (inverter)**: Pi ↔ USB-RS485 ↔ inverter A/B (this is the _only_ master link).
    
2. **ShineWiFi-X**: plug into the same Pi via USB (CH340 shows as `/dev/ttyUSB…`).
    
3. **Home Assistant**: configure the Growatt Local integration to talk **TCP** to `127.0.0.1:5020`.
    
4. **Your PC**: point your Modbus tool to `pi-address:5020` (Modbus-TCP).
    

The broker I gave you already:

* exposes **Modbus-TCP** on a port (default 5020) for HA + your PC,
    
* pass-throughs the **Shine** serial,
    
* **serializes** everything to the one RS-485 port.
    

Run it like this (adjust baud/format to your link):

```bash
python3 growatt_broker.py \
  --inverter /dev/ttyUSB485 --baud 115200 --bytes 8E1 \
  --shine    /dev/ttyUSB_SHINE \
  --tcp      0.0.0.0:5020
```

HA config example (Growatt Local via TCP)
=========================================

In your integration config, point to the broker’s TCP endpoint (on the same Pi here):

```yaml
modbus:
  - name: growatt_tcp
    type: tcp
    host: 127.0.0.1
    port: 5020
    timeout: 5
    retries: 3
    delay: 2
```

(Or in your custom Growatt Local integration’s options, select TCP and set host/port accordingly.)

Tips to make it robust
======================

* **Stable device names**: add udev rules so your ports don’t shuffle:
    
    ```
    # /etc/udev/rules.d/99-serial-names.rules
    SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttyUSB_SHINE"
    SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", SYMLINK+="ttyUSB485"
    ```
    
    (Adjust vendor/product to match your adapters: `udevadm info -a -n /dev/ttyUSB0`.)
    
* **systemd service** (so it starts on boot):
    
    ```
    [Unit]
    Description=Growatt Modbus Broker
    After=network-online.target
    
    [Service]
    ExecStart=/usr/bin/python3 /opt/growatt/growatt_broker.py \
              --inverter /dev/ttyUSB485 --baud 115200 --bytes 8E1 \
              --shine /dev/ttyUSB_SHINE --tcp 0.0.0.0:5020
    Restart=on-failure
    User=homeassistant
    Group=homeassistant
    WorkingDirectory=/opt/growatt
    
    [Install]
    WantedBy=multi-user.target
    ```
    
* **Don’t over-poll**: if HA polls every 1 s and your PC tool also polls every 1 s, it’s fine—the broker queues them. If you add more clients, consider 2–5 s intervals per client to keep latency low.
    
* **Debugging**: for a quick check from your PC, use a Modbus-TCP client (`mbpoll`/`pymodbus`) against `pi:5020` while HA + Shine run; you should still get clean replies.
    

Optional quality-of-life add-ons
================================

If you want, I can drop in:

* **CSV/JSON logging** of every request/response pair (timestamp, client, function, address range, CRC-OK).
    
* **pcap-ng export** so you can load the session straight into Wireshark as “Modbus/TCP” and see the decoded registers.
    
* **Simple cache** (e.g., 500 ms) so simultaneous identical polls return instantly without re-hitting the inverter.
    

If you share the exact baud/parity pair the USB port expects (and whether it truly is 11500), I’ll pre-configure the broker snippet with logging + a tiny cache so you can just paste-run it.

* * *

**You:**

The growatt 1.24 spec (shared in another chat) a/o says we should wait at least 850 ms between requests: "Minimum CMD period (RS485 Time out): 850ms. 
Wait for minimum850ms to send a new CMD after last CMD. Suggestion is 1s; "   - While this is specified for native 485, with default 9600 bps, I guess this also goes for the usb modbus with the ch340 based shinewifi dongle.

* * *

**ChatGPT:**

Yep—treat that **≥850 ms** as a device “think time” budget and enforce it globally, no matter the baud. Even if the USB path runs at 115200, the inverter’s Modbus server still wants breathing room between commands. Make the **Pi broker** serialize **and** rate-limit so the _combined_ traffic from HA + Shine + your PC never exceeds ~1 req/s.

Here’s a drop-in tweak for the broker I gave you:

### What it does

* A single **global cooldown** after each **completed transaction** (request→response or timeout).
    
* Default **`min_cmd_period = 1.0` s** (per spec’s “suggestion is 1 s”).
    
* Fair to all upstreams because everything is serialized through `Downstream.transact()`.
    

### Patch (replace `Downstream` class)

```python
class Downstream:
    def __init__(self, dev, baud, fmt, min_cmd_period=1.0, rtimeout=1.2):
        databits = int(fmt[0]); parity = fmt[1].upper(); stop = int(fmt[2])
        py_par = {'N':serial.PARITY_NONE,'E':serial.PARITY_EVEN,'O':serial.PARITY_ODD}[parity]
        py_stp = {1:serial.STOPBITS_ONE,2:serial.STOPBITS_TWO}[stop]
        self.ser = serial.Serial(dev, baud, bytesize=databits, parity=py_par, stopbits=py_stp, timeout=0)
        bits_per_char = 1 + databits + stop + (0 if parity=='N' else 1)
        self.char_time = bits_per_char / baud
        self.lock = threading.Lock()
        self.framer = RTUFramer(self.ser, self.char_time)
        self.min_cmd_period = float(min_cmd_period)
        self.rtimeout = float(rtimeout)
        self._last_done = 0.0  # when the last transaction finished (resp fully read or timeout)

    def _enforce_spacing(self):
        # ensure at least min_cmd_period since last finished transaction
        now = time.perf_counter()
        wait = self.min_cmd_period - (now - self._last_done)
        if wait > 0:
            time.sleep(wait)

    def transact(self, req: bytes):
        with self.lock:
            # Respect minimum period before starting a new request
            self._enforce_spacing()

            # Flush any stale bytes
            _ = self.ser.read(self.ser.in_waiting or 0)

            # Send request
            self.ser.write(req)
            self.ser.flush()

            # Read reply (gap-framed)
            reply = self.framer.read_frame(timeout=self.rtimeout)

            # Mark transaction end time (response gap or timeout)
            self._last_done = time.perf_counter()
            return reply
```

### How to run it

```bash
python3 growatt_broker.py \
  --inverter /dev/ttyUSB485 --baud 115200 --bytes 8E1 \
  --shine    /dev/ttyUSB_SHINE \
  --tcp      0.0.0.0:5020
```

(Inside `main()`, pass `min_cmd_period=1.0` into `Downstream(...)` if you want a different value.)

### Set HA poll rates accordingly

* If the device can only handle **~1 cmd/s total**, split that across clients.
    
* Example: HA every **2 s**, Shine every **1 s**, and your PC ad-hoc — the broker queues them and keeps spacing.
    
* In HA, use a longer `scan_interval` (or the integration’s equivalent) to avoid building up a queue.
    

### Why “after transaction end”?

The safest interpretation is: wait the period after the **previous command cycle completes** (i.e., after you’ve received the response or timed out), not just after you transmitted. That way, device processing + line idle both fit inside the guard band.

If you want, I can add:

* **Per-client rate limits** (so one aggressive client can’t starve others),
    
* **CSV/JSON logging** of every request/response with timestamps and who asked,
    
* A tiny **cache** (e.g., 500 ms) for identical back-to-back reads.

* * *

**You:**

Does the growatt integration read multiple registers at a time in one request?  I suppose it would, but perhaps you can find out: https://github.com/l4m4re/Homeassistant-Growatt-Local-Modbus/blob/fix/min-6000xh/custom_components/growatt_local/API/growatt.py

* * *

**ChatGPT:**

Short answer: **yes**—that integration’s API is built to request **ranges** of registers and will read **multiple registers per request** when it can.

Evidence from the repo’s own docs/example: they show calling  
`update(RegisterKeys(input=set(range(0, 30))))`, i.e., asking for input registers **0–29** in one go. That only makes sense if the transport groups contiguous ranges and issues a bulk Modbus read (function 0x04 or 0x03 with a `count > 1`) rather than 30 separate single-register reads. They also note you can request both input and holding ranges in one update call, which implies internal batching by contiguous ranges per function code. [GitHub](https://github.com/WouterTuinstra/Homeassistant-Growatt-Local-Modbus)

So, with your broker in place:

* The integration will **batch contiguous blocks**; your broker will still **serialize** them and enforce your **≥850 ms** spacing between completed transactions.
    
* If you want to watch what it actually does on the wire, add a quick log at `Downstream.transact()` to print the function code + starting address + count for each forwarded request.

* * *

**You:**

Quite interesting detail is that I can actually try the broker idea tonight, since only software, while I would have to modify the shine dongle to work over 485, since the serial bus is internal in the dongle and TTL, not 232 nor 485. While I do have a spare shine dongle I could modify, it's a lot more work and I would also have to register the new dongle on the Growatt server. 

* * *

**ChatGPT:**

Exactly — that’s the beauty of the broker idea: **no hardware surgery required** 🙂.

If you proxy ShineWiFi through the Pi over USB, you keep all of Growatt’s cloud registration machinery intact (the dongle still thinks it’s plugged straight into the inverter). You also get:

* **HA + Shine + your dev PC all active in parallel**  
    (broker arbitrates the bus, keeps ≥850 ms gap).
    
* **Quick rollback** if something breaks: just stop the broker and plug Shine back in normally.
    
* **Debugging freedom**: you can attach Wireshark or your own code to the TCP side and watch both the official Shine traffic and HA’s polls at the same time.
    
* **Less risk**: opening the Shine case and hacking the internal TTL bus risks damaging the ESP32 or CH340, and as you noted you’d have to go through the hassle of re-registering the new dongle with Growatt’s servers.
    

So: tonight you can simply run the broker on the Pi, point HA at `127.0.0.1:5020`, leave the Shine dongle in USB, and you’ll be able to capture traffic, test integration code, and still keep the Growatt server happy.

Would you like me to adapt the broker code so it **also logs every Shine request/response pair** to a file (CSV/JSON) while forwarding? That way you could immediately see what the official dongle is asking, without touching hardware.

* * *

**You:**

Biggest advantage of the Pi in the middle is that I can now actually use the shine platform once again, since I had to remove to be able to use the HA integration, which is currently incomplete. So, whenever I wish to change some battery setting, I have to unplug the pi and plug in the shine dongle. This exercise often results in the inverter becoming unresponsive requiring a power cycle of both the inverter and the battery. Quite a hassle just to set some parameter.

* * *

**ChatGPT:**

That’s a perfect justification for the broker — you’ve basically described the classic “single-master bottleneck” problem:

* **Native setup**: only one master (either ShineWiFi _or_ HA) → you’re forced to hot-swap, and the inverter/ARK battery really doesn’t like that.
    
* **Broker setup**: Pi becomes the only real master → Shine thinks it still has its private serial, HA thinks it has its Modbus endpoint, and the inverter just sees orderly requests. No more plug/unplug dance.
    

That means:

✅ you can **leave the Shine dongle in permanently** (Growatt cloud works, firmware updates, parameter writes).  
✅ you can **run HA integration 24/7** to log, automate, and tune.  
✅ you can even **connect a dev tool from your PC** over TCP for debugging, without destabilizing the inverter.

And because you’ll enforce the ≥850 ms delay globally, you’re actually treating the inverter _better_ than the old setup, where two different masters might bombard it without coordination.

If you like, I can extend the broker to:

* **Log all Shine traffic** separately (so you can see exactly what it writes/reads when you change a battery setting in the official app).
    
* **Prioritize writes** (if Shine sends a config change, it gets dispatched immediately, HA polls are queued until the inverter settles).
    
* **Expose a “mirror” TCP stream** of Shine’s traffic so you can packet-sniff on your PC without interfering.
    

Would you like me to add one of those logging/mirroring options right away so you can observe Shine’s “hidden” Modbus register writes tonight?

* * *

**You:**

Yep, very interesting base for reverse engineering undocumented registers. In the register mapping thread we found no registers for the "winter" setting the web-gui supports. This allows setting a different minimum SOC for the battery between on-grid and off-grid mode in winter, for which you can set a period.  Rather strange to do it like this and not have a separate setting for off-grid mode anyway, but it is what it is.  Also rather annoying they limit both the on and off-grid minimal SOC to between 10 and 30%, while I probably want 10% in off-grid mode and more like 60 or 70% in on-grid mode, since at the moment I want to spare my battery as much as possible ("salderingsregeling" still applies now) unless there is a grid failure.

* * *

**ChatGPT:**

Totally agree—that broker becomes your **non-intrusive RE tap**. Let’s wire it so you can (a) keep Shine + HA online, and (b) **log every Shine write** to hunt the “winter” params (and any other hidden settings).

Here’s a practical plan + drop-in code upgrades.

What we’ll capture
==================

* **Writes** (function 0x06, 0x10): log unit id, start addr, value(s), CRC-OK, timestamps.
    
* **Reads** (0x03, 0x04): optional (can be noisy); still useful when you toggle a UI widget and see what Shine re-reads.
    
* **Per-client tagging**: “SHINE” vs “TCP:n.n.n.n:port” (HA or your PC).
    
* **Spec spacing**: still enforces ≥850 ms between transactions (global).
    

How to reverse-engineer “winter” settings
=========================================

1. Start the broker with logging (below).
    
2. In the **Shine app/web**, toggle **Winter mode** on/off, change the **period**, and adjust **on-grid/off-grid min SOC**.
    
3. Watch the log for **0x06 / 0x10** to **holding registers** near known SOC knobs (e.g., you already saw things like 3036/3037/3047/3048/3082 for other modes).
    
4. Change **one thing at a time**; take two samples (before/after). The diff will isolate the addresses.
    
5. If Growatt caps 10–30% in UI, try **edge values** (10 → 30) to see which registers move; that helps identify scaling (percent vs tenths).
    
6. Once identified, you can script HA to set your preferred **on-grid 60–70%** and **off-grid 10%** directly—whether or not the UI allows it (careful: device may clamp).
    

* * *

Broker upgrades (logging + mirror)
----------------------------------

Below are minimal patches you can apply to the broker I gave you earlier. Replace the `Downstream` class and add the small **Logger** + **Mirror** pieces. This keeps the file compact.

### 1) Add a tiny logger + helpers (top of file)

```python
import json, datetime, socket

def now_iso():
    return datetime.datetime.now().isoformat(timespec="milliseconds")

def parse_rtu(frame: bytes):
    if len(frame) < 4: return {}
    uid, func = frame[0], frame[1]
    body = frame[2:-2]
    info = {"uid": uid, "func": func, "len": len(body)}
    # quick parse for common funcs
    if func in (0x03, 0x04) and len(body) >= 4:
        # req: [addr_hi, addr_lo, count_hi, count_lo]
        info["addr"]  = (body[0] << 8) | body[1]
        info["count"] = (body[2] << 8) | body[3]
    elif func == 0x06 and len(body) >= 4:
        info["addr"] = (body[0] << 8) | body[1]
        info["value"]= (body[2] << 8) | body[3]
    elif func == 0x10 and len(body) >= 5:
        # req: start addr (2) + qty (2) + bytecount (1) + data...
        info["addr"]  = (body[0] << 8) | body[1]
        info["count"] = (body[2] << 8) | body[3]
        info["bytes"] = body[4]
    return info

class MirrorTap:
    """Optional: push line-oriented JSON events to any TCP clients that connect."""
    def __init__(self, bind="0.0.0.0", port=15020):
        self.addr = (bind, port)
        self.clients = []
        self.lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr); self.sock.listen(4)
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while True:
            c, a = self.sock.accept()
            c.settimeout(5)
            with self.lock: self.clients.append(c)

    def publish(self, event: dict):
        line = (json.dumps(event, separators=(",",":")) + "\n").encode()
        drop = []
        with self.lock:
            for c in self.clients:
                try: c.sendall(line)
                except: drop.append(c)
            for c in drop:
                try: c.close()
                except: pass
                self.clients.remove(c)

class WireLogger:
    def __init__(self, path="/var/log/growatt_broker.jsonl", mirror: MirrorTap|None=None):
        self.path = path
        self.mirror = mirror
        self._lock = threading.Lock()
    def log(self, **event):
        event["ts"] = now_iso()
        line = json.dumps(event, ensure_ascii=False)
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line+"\n")
        if self.mirror:
            self.mirror.publish(event)
```

### 2) Replace `Downstream` with a spaced, logging version

```python
class Downstream:
    def __init__(self, dev, baud, fmt, min_cmd_period=1.0, rtimeout=1.2, logger: WireLogger|None=None):
        databits = int(fmt[0]); parity = fmt[1].upper(); stop = int(fmt[2])
        py_par = {'N':serial.PARITY_NONE,'E':serial.PARITY_EVEN,'O':serial.PARITY_ODD}[parity]
        py_stp = {1:serial.STOPBITS_ONE,2:serial.STOPBITS_TWO}[stop]
        self.ser = serial.Serial(dev, baud, bytesize=databits, parity=py_par, stopbits=py_stp, timeout=0)
        bits_per_char = 1 + databits + stop + (0 if parity=='N' else 1)
        self.char_time = bits_per_char / baud
        self.lock = threading.Lock()
        self.framer = RTUFramer(self.ser, self.char_time)
        self.min_cmd_period = float(min_cmd_period)
        self.rtimeout = float(rtimeout)
        self._last_done = 0.0
        self.logger = logger

    def _enforce_spacing(self):
        now = time.perf_counter()
        wait = self.min_cmd_period - (now - self._last_done)
        if wait > 0: time.sleep(wait)

    def transact(self, req: bytes, client="UNKNOWN"):
        with self.lock:
            self._enforce_spacing()
            _ = self.ser.read(self.ser.in_waiting or 0)

            # Log request (pre-send)
            if self.logger:
                self.logger.log(role="REQ", from_client=client,
                                crc_ok=crc_ok(req), hex=req.hex(),
                                **parse_rtu(req))

            self.ser.write(req); self.ser.flush()
            reply = self.framer.read_frame(timeout=self.rtimeout)
            self._last_done = time.perf_counter()

            # Log response
            if self.logger:
                self.logger.log(role="RSP", to_client=client,
                                crc_ok=crc_ok(reply), hex=(reply.hex() if reply else ""),
                                **parse_rtu(reply or b""))

            return reply
```

### 3) Tag Shine and TCP clients with names

In `ShineEndpoint.run()` change:

```python
resp = self.ds.transact(req, client="SHINE")
```

In `TCPServer.handle()` change the transact call:

```python
peer = f"TCP:{conn.getpeername()[0]}:{conn.getpeername()[1]}"
rtu_resp = self.ds.transact(rtu_req, client=peer)
```

### 4) Wire it up in `main()`

Add:

```python
mirror = MirrorTap(bind="0.0.0.0", port=15020)   # optional live feed
logger = WireLogger(path="/var/log/growatt_broker.jsonl", mirror=mirror)
ds = Downstream(args.inverter, args.baud, args.bytes, min_cmd_period=1.0, rtimeout=1.5, logger=logger)
```

(…then pass `ds` to `ShineEndpoint` and `TCPServer` like before.)

* * *

Using it tonight
----------------

1. Run the broker (with your baud/format):
    

```bash
sudo python3 growatt_broker.py \
  --inverter /dev/ttyUSB485 --baud 115200 --bytes 8E1 \
  --shine    /dev/ttyUSB_SHINE \
  --tcp      0.0.0.0:5020
```

2. Point **HA** to `127.0.0.1:5020` (Modbus-TCP).
    
3. Leave **Shine** plugged into the Pi (serial path you gave as `--shine`).
    
4. Optionally, on your PC:
    

```bash
telnet pi 15020
```

You’ll see JSON lines like:

```json
{"ts":"2025-08-26T21:07:11.123","role":"REQ","from_client":"SHINE","uid":1,"func":16,"addr":3048,"count":2,"bytes":4,"len":7,"crc_ok":true,"hex":"01 10 0b e8 00 02 04 00 3c 00 0a xx xx"}
{"ts":"2025-08-26T21:07:11.457","role":"RSP","to_client":"SHINE","uid":1,"func":16,"addr":3048,"count":2,"len":4,"crc_ok":true,"hex":"01 10 0b e8 00 02 xx xx"}
```

(Example means **Write Multiple Registers** at address `0x0BE8 = 3048` writing 0x003C, 0x000A → could be “Stop Charge SOC when Bat First = 60” and “Off-grid min SOC = 10”, purely illustrative.)

5. After toggling **Winter mode** in the official UI, search your log (`/var/log/growatt_broker.jsonl`) for **`"func":16`** or **`"func":6`** around the time you clicked. The **`addr`**(+ maybe a paired addr) will be your candidate registers. Repeat a few variations to confirm.
    

* * *

Notes / safety
--------------

* Keep ≥850 ms spacing (already enforced).
    
* Writes can affect battery behavior—test at safe SOC and load.
    
* Some settings may require inverter/battery handshake; Shine may write **multiple registers** in a specific order—log captures that sequence.
    

If you want, I can also add a **CSV companion** (addr,value,count,client) or a **Wireshark-friendly pcapng Modbus/TCP mirror** so you can decode flows visually.

* * *

**You:**

More on winter mode here (with a/o a screenshot of the GUI):

https://github.com/PLCHome/growatt/issues/32

And:

https://en.growatt.com/media/news/battery-health-management-guide:-how-to-extend-battery-life-in-energy-storage-systems

"Growatt Winter Mode: Cold-Weather Battery Protection
Winter presents a unique challenge for energy storage systems. Solar production drops, temperatures plummet, and users may experience longer periods without full battery charging. Growatt’s Winter Mode is specifically designed to counter these seasonal stressors.

This mode uses temperature sensors and State of Charge (SOC) monitoring to:

    • Prompt users to activate Winter Mode when low temperatures are detected

    • Enable users to configure local winter settings and define higher discharge stop SOC levels

    • Prevent deep discharges during snow-covered or low-sunlight days

    • Resume normal charging once environmental conditions improve

By proactively managing SOC and discharge levels, Growatt Winter Mode significantly reduces battery stress and preserves long-term health."


It _may_ actually use documented regisers, but we may also find out they use undocumented registers for this mode. 

In any case, this would be the prime candidate for reverse-engineering what the shine wifi actually does.

* * *

**ChatGPT:**

Totally agreed—**Winter Mode** is the perfect “first target” for RE. Growatt’s own write-up confirms the feature exists and that it raises the **discharge stop SOC** based on temperature/seasonal conditions, configurable via Shine (web/app). That’s exactly the sort of thing that should show up as **one or more holding-register writes** when you toggle it. [en.growatt.com+1](https://en.growatt.com/media/news/battery-health-management-guide%3A-how-to-extend-battery-life-in-energy-storage-systems)

Here’s a tight, do-it-tonight plan using the broker you’re setting up:

What to capture
===============

* Focus on **writes**: Modbus **0x06** (Write Single Register) and **0x10** (Write Multiple Registers) from **client=SHINE**.
    
* Expect addresses around the **3xxx** holding space (e.g., you already found 3036/3037/3047/3048/3082 for other modes). Winter Mode might re-use or add nearby registers.
    

Quick experiment recipe
=======================

1. **Run the broker with logging + ≥1.0 s spacing** (you’ve got the class with `min_cmd_period=1.0`).
    
2. Point HA to the broker (TCP), keep it running if you want—no problem—but for a clean trace you can temporarily raise HA’s scan interval to reduce noise.
    
3. In **Shine web/app**, do these **one at a time** (wait ~2–3 s between actions):
    
    * Toggle **Winter Mode: OFF → ON** (Save).
        
    * Change **On-grid Min SOC**: e.g., 20% → 30% → 25% (Save each).
        
    * Change **Off-grid Min SOC**: e.g., 10% → 15% → 12%.
        
    * Adjust **Winter period** (start/end dates), Save.
        
    * Toggle **Winter Mode: ON → OFF**, Save.
        
4. Tail the broker log (`/var/log/growatt_broker.jsonl`) and note **0x06 / 0x10** lines from `from_client:"SHINE"`; those address/value pairs are your candidates.
    

Tiny log scrapers (pick one)
============================

**Bash/grep glance:**

```bash
grep '"from_client":"SHINE"' /var/log/growatt_broker.jsonl | \
grep '"role":"REQ"' | egrep '"func":6|"func":16' | cut -d'}' -f1
```

**Python mini-summary (group writes by second):**

```python
import json, time
from collections import defaultdict
events=defaultdict(list)
with open("/var/log/growatt_broker.jsonl","r",encoding="utf-8") as f:
    for line in f:
        e=json.loads(line)
        if e.get("role")=="REQ" and e.get("from_client")=="SHINE" and e.get("func") in (6,16):
            t=e["ts"]; sec=t.split(".")[0]
            events[sec].append(e)
for sec, evs in sorted(events.items()):
    print(sec)
    for e in evs:
        func=e["func"]; addr=e.get("addr"); cnt=e.get("count"); val=e.get("value")
        print(f"  func=0x{func:02X} addr={addr} count={cnt} value={val} len={e.get('len')}")
```

**What you’ll see:** when you hit Save, Shine typically sends a **burst** of 1–N writes in the same second; those are the registers for that setting. If values look like **10 → 30 → 25**, it’s % directly (0x000A→0x001E→0x0019). If increments look like **100 → 300 → 250**, it’s **tenths of a percent**.

Sanity checks
=============

* After you identify addresses, **read them back** (via your PC Modbus-TCP client through the broker) to confirm values match the UI.
    
* Try **edge values** the UI allows (e.g., 10% and 30%) to make scaling obvious.
    
* If Growatt clamps UI to 10–30% but you want **60–70% on-grid**, test carefully—some devices accept higher writes but clamp internally; others reject.
    

Nice-to-have (I can add if you want)
====================================

* **Per-client priorities**: give Shine writes a short priority window; HA polls queue behind.
    
* **CSV/pcap-ng** export for Wireshark (decoded as Modbus/TCP).
    
* A **500 ms read cache** so back-to-back identical polls don’t hit the inverter.
    

This should quickly surface the “winter” knobs—whether Growatt reused known SOC registers or hid new ones. Once mapped, you can script HA to enforce your preferred **on-grid 60–70%** vs **off-grid 10%**, while keeping the Shine platform usable. And because the **broker** is the sole master, everything stays stable and within Growatt’s recommended pacing. [en.growatt.com](https://en.growatt.com/media/news/battery-health-management-guide%3A-how-to-extend-battery-life-in-energy-storage-systems)