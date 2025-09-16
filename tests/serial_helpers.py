"""Helpers for setting up virtual serial links using socat."""

from __future__ import annotations

import asyncio
import contextlib
from contextlib import asynccontextmanager
import os
import pty
import shutil
from typing import AsyncIterator, Tuple

__all__ = ["virtual_serial_pair", "serial_environment_available"]


def serial_environment_available() -> bool:
    """Return True if socat and PTY creation are available."""
    if shutil.which("socat") is None:
        return False
    try:
        master, slave = pty.openpty()
    except OSError:
        return False
    os.close(master)
    os.close(slave)
    return True


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
    log_lines: list[str] = []

    try:
        while len(ports) < 2:
            try:
                line = await asyncio.wait_for(process.stderr.readline(), timeout=2.0)
            except asyncio.TimeoutError as exc:
                raise RuntimeError("Timed out waiting for socat PTY pair") from exc
            if not line:
                rc = process.returncode
                detail = "; ".join(log_lines)
                raise RuntimeError(
                    "Failed to start socat PTY pair"
                    + (f" (rc={rc}): {detail}" if rc is not None else "")
                )
            text = line.decode().strip()
            log_lines.append(text)
            if "PTY is" in text:
                ports.append(text.split()[-1])
            elif " E " in text or text.startswith("E "):
                raise RuntimeError(f"socat error: {text}")
        # socat prints a final status line before entering transfer loop; consume it
        await asyncio.sleep(0)
        yield ports[0], ports[1]
    finally:
        process.terminate()
        with contextlib.suppress(ProcessLookupError):
            await process.wait()
