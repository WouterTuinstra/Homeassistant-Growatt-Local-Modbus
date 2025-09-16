"""Sample mutation plug‑in for the simulator.

Usage:
  python -m growatt_broker.simulator.modbus_simulator --mutator testing.mutators.sample_mutator:EnergyIncrement
or shorter if mutate function exported as mutate.

Effect:
  - Increment holding register 331 (example: total power) by 5 each tick.
  - Increment all holding registers >= 1050 (example: energy totals) by 1 every 6 ticks.
"""
from __future__ import annotations

class EnergyIncrement:
    def __init__(self, step: int = 5):
        self.step = step
    def mutate(self, registers, tick: int):
        holding = registers['holding']
        if 331 in holding:
            holding[331] = (holding[331] + self.step) & 0xFFFF
        if tick % 6 == 0:
            for addr in list(holding.keys()):
                if addr >= 1050:
                    holding[addr] = (holding[addr] + 1) & 0xFFFF

# Simple function style alternative

def mutate(registers, tick: int):  # increments a small demo register if present
    h = registers['holding']
    if 30 in h:
        h[30] = (h[30] + 1) & 0xFFFF
