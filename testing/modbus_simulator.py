"""
Configurable Modbus TCP simulator for Growatt devices.

Features:
 - Support multiple device types via JSON register definition files
 - Optional dataset JSON with realistic register values (e.g. based on real MIN 6000XH-TL scans)
 - Re-usable async context manager for tests, plus CLI for manual use

JSON definition format (existing):
 [ {"number": 1, "name": "...", "length": 1}, ... ]

Dataset JSON format:
 {
   "holding": {"1": 401, "2": 0, ...},
   "input": {"3001": 123, ...}
 }
Missing registers are initialised to 0.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import logging
import importlib, inspect
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Tuple, Iterable, Callable, Any

from pymodbus.datastore import (
    ModbusServerContext,
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
)
from pymodbus.server import ModbusTcpServer

BASE_PATH = Path(__file__).parent
DATASETS_PATH = BASE_PATH / "datasets"

_LOGGER = logging.getLogger(__name__)

DEVICE_TYPES: dict[str, Tuple[str, str]] = {
    # key -> (holding_definition_file, input_definition_file)
    "min": ("holding_min.json", "input_min.json"),
    # TL-XH variants (MIN 6000XH-TL hybrid) use tl_xh mapping
    "tl_xh": ("holding_tl_xh.json", "input_tl_xh.json"),
    "min_6000xh_tl": ("holding_tl_xh.json", "input_tl_xh.json"),
}

DEFAULT_DATASETS: dict[str, str] = {
    # Provide realistic baseline for MIN 6000XH-TL based on scans
    "min_6000xh_tl": "min_6000xh_tl.json",
}


def _load_register_definitions(filename: str) -> Dict[int, int]:
    """Return a dict of every register address defined (value unused=0)."""
    with open(BASE_PATH / filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    registers: dict[int, int] = {}
    for item in data:
        number = int(item["number"])
        length = int(item.get("length", 1))
        for offset in range(length):
            registers[number + offset] = 0
    return registers


def _load_dataset(
    dataset_file: Path | None, force_deterministic: bool = False
) -> tuple[dict[int, int], dict[int, int]]:
    """Load dataset file returning holding and input value dicts.

    When no dataset is supplied, provide deterministic non-zero values for input
    registers 1 and 2 so tests composing a 32-bit value have a stable baseline.
    If force_deterministic is True, set first 32 input registers to 1..32 for test stability.
    """
    if not dataset_file or not dataset_file.exists():
        input_regs = {1: 1, 2: 2}
        if force_deterministic:
            input_regs = {i: i for i in range(1, 33)}
        return {}, input_regs

    with open(dataset_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    def to_uint16(val: int) -> int:
        """Coerce any value into an unsigned 16-bit representation."""
        return int(val) & 0xFFFF

    holding = {int(k): to_uint16(v) for k, v in raw.get("holding", {}).items()}
    input_ = {int(k): to_uint16(v) for k, v in raw.get("input", {}).items()}
    if force_deterministic:
        # Force deterministic values for the first 32 input registers
        for i in range(1, 33):
            input_[i] = i
    return holding, input_


def _max_or_default(keys: Iterable[int]) -> int:
    try:
        return max(keys)
    except ValueError:
        return 0


def _build_value_arrays(
    holding_def: dict[int, int],
    input_def: dict[int, int],
    holding_values: dict[int, int],
    input_values: dict[int, int],
    *,
    strict_defs: bool = False,
):
    """Create dense arrays for ModbusSequentialDataBlock.

    If strict_defs is False (default), include dataset registers even if not in definition files.
    This allows using rich real-world scans without enumerating every register in mapping JSON.
    """
    MAX_REGISTERS = 4000
    hr_array = [0] * MAX_REGISTERS
    ir_array = [0] * MAX_REGISTERS

    # Overwrite with values from definition and dataset
    hr_keys = set(holding_def.keys()) | set(holding_values.keys())
    ir_keys = set(input_def.keys()) | set(input_values.keys())
    for reg in hr_keys:
        if 0 <= reg < MAX_REGISTERS:
            hr_array[reg] = holding_values.get(reg, 0)
    for reg in ir_keys:
        if 0 <= reg < MAX_REGISTERS:
            ir_array[reg] = input_values.get(reg, 0)
    return hr_array, ir_array


# Mutation plug‑in API ---------------------------------------------------------
# A mutator is either:
#   - a callable mutate(registers: dict[str, dict[int,int]], tick: int) -> None
#   - an object with method mutate(registers, tick)
# It can adjust in‑memory holding/input register values each simulator tick.


class _MutatorWrapper:
    def __init__(self, target: Any):
        if callable(target) and not hasattr(target, "mutate"):
            self._fn = target
        else:
            self._fn = getattr(target, "mutate")
        if not callable(self._fn):
            raise TypeError("Mutator has no callable mutate()")

    def mutate(self, registers: dict[str, dict[int, int]], tick: int):
        self._fn(registers, tick)


def _load_mutators(specs: list[str]) -> list[_MutatorWrapper]:
    muts: list[_MutatorWrapper] = []
    for spec in specs:
        try:
            mod_name, _, attr = spec.partition(":")
            mod = importlib.import_module(mod_name)
            obj = getattr(mod, attr) if attr else getattr(mod, "mutate", mod)
            # If attribute name given and is a class, instantiate; else use directly
            if inspect.isclass(obj):
                obj = obj()
            muts.append(_MutatorWrapper(obj))
        except Exception as e:  # pragma: no cover
            print(f"[SIM] Failed to load mutator '{spec}': {e}")
    return muts


@asynccontextmanager
async def start_simulator(
    *args,
    port: int = 5020,
    host: str = "127.0.0.1",
    device: str = "min_6000xh_tl",
    dataset: str | None = None,
    force_deterministic: bool = False,
    strict_defs: bool = False,
    mutators: list[str] | None = None,
    debug_wire: bool = False,
):
    """Start a Modbus TCP simulator serving predefined registers.

    Backwards compatibility:
        Previously accepted a single positional argument (port). Support that pattern while
        encouraging keyword usage going forward.
    """
    if args:
        if len(args) == 1 and isinstance(args[0], int):
            port = args[0]
        else:  # pragma: no cover - defensive
            raise TypeError("start_simulator accepts at most one positional int (port)")
    # Parameters doc kept above in updated docstring.

    if device not in DEVICE_TYPES:
        raise ValueError(
            f"Unknown device type '{device}'. Valid: {', '.join(DEVICE_TYPES)}"
        )

    holding_file, input_file = DEVICE_TYPES[device]
    holding_def = _load_register_definitions(holding_file)
    input_def = _load_register_definitions(input_file)

    dataset_path: Path | None = None
    if dataset:
        dp = Path(dataset)
        dataset_path = dp if dp.is_absolute() else (DATASETS_PATH / dataset)
    elif device in DEFAULT_DATASETS:
        dataset_path = DATASETS_PATH / DEFAULT_DATASETS[device]

    holding_values, input_values = _load_dataset(
        dataset_path, force_deterministic=force_deterministic
    )
    hr_values, ir_values = _build_value_arrays(
        holding_def, input_def, holding_values, input_values, strict_defs=strict_defs
    )

    class LoggingDataBlock(ModbusSequentialDataBlock):
        def __init__(self, start, values, *, kind: str):
            super().__init__(start, values)
            self._kind = kind

        def getValues(self, address, count=1):  # type: ignore[override]
            result = super().getValues(address, count)
            if debug_wire:
                _LOGGER.debug(
                    "%s read %d:%d -> %s",
                    self._kind,
                    address,
                    address + count - 1,
                    result,
                )
            return result

        def setValues(self, address, values):  # type: ignore[override]
            if debug_wire:
                _LOGGER.debug(
                    "%s write %d:%d <- %s",
                    self._kind,
                    address,
                    address + len(values) - 1,
                    values,
                )
            return super().setValues(address, values)

    # Pymodbus offsets holding-register addresses by +1 for TCP servers.
    # Starting the holding block at ``1`` aligns client address ``0`` with
    # index ``0`` of ``hr_values``. Input registers do not require this
    # offset and therefore retain a base address of ``0``.
    hr_block = LoggingDataBlock(1, hr_values, kind="holding")
    ir_block = LoggingDataBlock(0, ir_values, kind="input")
    store = {1: ModbusDeviceContext(hr=hr_block, ir=ir_block)}
    # Pass mapping as first positional arg; current pymodbus expects this without 'slaves=' kw
    context = ModbusServerContext(store, single=False)

    server = ModbusTcpServer(context, address=(host, port))
    task = asyncio.create_task(server.serve_forever())
    _LOGGER.info(
        "Simulator started on %s:%d (device=%s, dataset=%s defs(h/i)=%d/%d total(h/i)=%d/%d populated(h/i)=%d/%d strict=%s)",
        host,
        port,
        device,
        dataset_path.name if dataset_path else "<none>",
        len(holding_def),
        len(input_def),
        len(hr_values),
        len(ir_values),
        sum(1 for v in hr_values if v != 0),
        sum(1 for v in ir_values if v != 0),
        strict_defs,
    )
    _mutators = _load_mutators(mutators or [])
    _tick = 0
    _stop = asyncio.Event()

    async def _mutation_loop():
        nonlocal _tick
        if not _mutators:
            await _stop.wait()
            return
        while not _stop.is_set():
            _tick += 1
            regs = {"holding": holding_values, "input": input_values}
            for m in _mutators:
                try:
                    m.mutate(regs, _tick)
                except Exception as e:  # pragma: no cover
                    print(f"[SIM] mutator error: {e}")
            # Apply any changes from mutators back to value arrays
            for reg, val in holding_values.items():
                hr_block.setValues(reg, [val])
            for reg, val in input_values.items():
                ir_block.setValues(reg, [val])
            try:
                await asyncio.wait_for(_stop.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                pass

    mutation_task = asyncio.create_task(_mutation_loop())

    try:
        # Brief pause to ensure server socket is bound before yielding to caller
        await asyncio.sleep(0.05)
        yield (host, port)
    finally:
        _stop.set()
        mutation_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await mutation_task
        await server.shutdown()
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
        _LOGGER.info("Simulator stopped")


def _parse_args():
    parser = argparse.ArgumentParser(description="Growatt Modbus TCP simulator")
    parser.add_argument("--port", type=int, default=5020, help="TCP port to listen on")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host/IP to bind (use 0.0.0.0 for all interfaces)",
    )
    parser.add_argument(
        "--device",
        default="min_6000xh_tl",
        choices=sorted(DEVICE_TYPES.keys()),
        help="Device type mapping to use",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Dataset JSON (filename in datasets/ or absolute path). Overrides default dataset.",
    )
    parser.add_argument(
        "--strict-defs",
        action="store_true",
        help="Only include registers present in definition JSON files (ignore extra dataset registers).",
    )
    parser.add_argument(
        "--force-deterministic",
        action="store_true",
        help="Force first 32 input registers to values 1..32 for test stability.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=0,
        help="Optional duration in seconds before auto-shutdown (0 = run forever)",
    )
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    parser.add_argument(
        "--mutator",
        action="append",
        help="Mutation plug‑in spec module[:attr] (repeatable)",
    )
    parser.add_argument(
        "--debug-modbus",
        action="store_true",
        help="Enable debug logging for all Modbus requests and replies",
    )
    parser.add_argument(
        "--debug-wire",
        action="store_true",
        help="Log register reads/writes at the simulator layer",
    )
    return parser.parse_args()


async def _run_cli():
    args = _parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))
    if args.debug_modbus:
        logging.getLogger("pymodbus").setLevel(logging.DEBUG)
    async with start_simulator(
        host=args.host,
        port=args.port,
        device=args.device,
        dataset=args.dataset,
        strict_defs=args.strict_defs,
        mutators=args.mutator,
        debug_wire=args.debug_wire,
        force_deterministic=args.force_deterministic,
    ):
        if args.duration > 0:
            await asyncio.sleep(args.duration)
        else:
            # Sleep indefinitely
            while True:
                await asyncio.sleep(3600)


if __name__ == "__main__":  # pragma: no cover
    try:
        asyncio.run(_run_cli())
    except KeyboardInterrupt:
        pass
