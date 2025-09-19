#!/usr/bin/env python

import sys
import time
from datetime import datetime
import argparse

from VfModbus import (
    connect_modbus, read_registers, format_value, get_categories, DEFAULT_SLAVE, DEFAULT_BAUDRATE, DEFAULT_TIMEOUT
)

def main():
    parser = argparse.ArgumentParser(description='Read and display Modbus settings')
    parser.add_argument('-p', '--port', help='Serial port to use')
    parser.add_argument('-b', '--baudrate', type=int, default=DEFAULT_BAUDRATE, help=f'Baudrate (default: {DEFAULT_BAUDRATE})')
    parser.add_argument('-s', '--slave', type=int, default=DEFAULT_SLAVE, help=f'Slave address (default: {DEFAULT_SLAVE})')
    parser.add_argument('-t', '--timeout', type=float, default=DEFAULT_TIMEOUT, help=f'Timeout in seconds (default: {DEFAULT_TIMEOUT})')
    parser.add_argument('-r', '--repeat', action='store_true', help='Continuously read values')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='Delay between reads in seconds (used with --repeat)')
    args = parser.parse_args()

    try:
        client = connect_modbus(port=args.port, baudrate=args.baudrate, timeout=args.timeout)
    except Exception as e:
        print(str(e))
        return 1

    try:
        while True:
            print(f"Modbus Settings Reader - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Port: {args.port or 'auto'}, Baudrate: {args.baudrate}, Slave ID: {args.slave}")
            print("-" * 80)

            register_values = read_registers(client, args.slave)

            categories = get_categories()
            for category, registers in categories.items():
                if registers:
                    print(f"\n{category}:")
                    print("-" * 80)
                    print(f"{'Reg':>4} {'Name':<30} {'Value':<12} {'Units':<8} {'Description'}")
                    print("-" * 80)
                    for reg in sorted(registers, key=lambda x: x["address"]):
                        value = register_values.get(reg["address"])
                        formatted_value = format_value(reg, value, all_regs=register_values)
                        print(f"{reg['address']:4d} {reg['name']:<30} {formatted_value:<12} {reg['units']:<8} {reg['description']}")
            if not args.repeat:
                break
            time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        client.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
