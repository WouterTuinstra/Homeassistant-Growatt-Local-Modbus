"""Helpers for setting up virtual serial links using socat."""

from __future__ import annotations

import asyncio
import contextlib
from contextlib import asynccontextmanager
from typing import AsyncIterator, Tuple

__all__ = ["virtual_serial_pair"]


@asynccontextmanager
async def virtual_serial_pair() -> AsyncIterator[Tuple[str, str]]:
    """Create a connected PTY pair backed by a socat process."""
    try:
        process = await asyncio.create_subprocess_exec(
            "socat",
            "-d",
            "-d",
            "PTY,raw,echo=0",
            "PTY,raw,echo=0",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment issue
        raise RuntimeError("socat is required for serial tests") from exc

    ports: list[str] = []
    assert process.stderr is not None

    try:
        while len(ports) < 2:
            line = await process.stderr.readline()
            if not line:
                raise RuntimeError("Failed to start socat PTY pair")
            text = line.decode().strip()
            if "PTY is" in text:
                ports.append(text.split()[-1])
        # socat prints a final status line before entering transfer loop; consume it
        await asyncio.sleep(0)
        yield ports[0], ports[1]
    finally:
        process.terminate()
        with contextlib.suppress(ProcessLookupError):
            await process.wait()
