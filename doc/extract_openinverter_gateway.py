#!/usr/bin/env python3
"""Extract register mappings from the OpenInverterGateway ShineWiFi-ModBus firmware."""

from __future__ import annotations

import ast
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = (
    REPO_ROOT / "external" / "OpenInverterGateway" / "SRC" / "ShineWiFi-ModBus"
)
OUTPUT_PATH = Path(__file__).resolve().parent / "openinverter_gateway_registers.json"
MQTT_DOC_PATH = REPO_ROOT / "external" / "OpenInverterGateway" / "Doc" / "MQTT.md"

ENUMS: dict[str, dict[str, int]] = {}
ENUM_VALUE_LOOKUP: dict[str, int] = {}


def strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    source = re.sub(r"//.*", "", source)
    return source


def eval_int_expression(expr: str, local_ctx: dict[str, int]) -> int:
    expr = expr.strip()
    expr = re.sub(r"([0-9])([uUlLfF]+)", r"\1", expr)
    allowed_names = {**ENUM_VALUE_LOOKUP, **local_ctx}

    class Visitor(ast.NodeVisitor):
        def visit_Constant(self, node: ast.Constant) -> int:
            if isinstance(node.value, (int, float)):
                return int(node.value)
            raise ValueError

        def visit_Name(self, node: ast.Name) -> int:
            if node.id not in allowed_names:
                raise ValueError
            return allowed_names[node.id]

        def visit_UnaryOp(self, node: ast.UnaryOp) -> int:
            value = self.visit(node.operand)
            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value
            if isinstance(node.op, ast.Invert):
                return ~value
            raise ValueError

        def visit_BinOp(self, node: ast.BinOp) -> int:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return int(left / right)
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.LShift):
                return left << right
            if isinstance(node.op, ast.RShift):
                return left >> right
            if isinstance(node.op, ast.BitAnd):
                return left & right
            if isinstance(node.op, ast.BitOr):
                return left | right
            if isinstance(node.op, ast.BitXor):
                return left ^ right
            raise ValueError

        def generic_visit(self, node: ast.AST) -> int:
            raise ValueError

    tree = ast.parse(expr, mode="eval")
    return Visitor().visit(tree.body)


def parse_enums() -> None:
    enum_pattern = re.compile(r"typedef\s+enum\s*\{(.*?)\}\s*(\w+)\s*;", re.S)
    for header in sorted(PROJECT_ROOT.glob("*.h")):
        text = strip_comments(header.read_text(encoding="utf-8"))
        for match in enum_pattern.finditer(text):
            body, name = match.groups()
            entries: dict[str, int] = {}
            current_value: int | None = None
            local_ctx: dict[str, int] = {}
            for raw_item in body.split(","):
                item = raw_item.strip()
                if not item:
                    continue
                if "=" in item:
                    enum_name, expr = item.split("=", 1)
                    enum_name = enum_name.strip()
                    current_value = eval_int_expression(expr, local_ctx)
                else:
                    enum_name = item
                    if current_value is None:
                        current_value = 0
                entries[enum_name] = current_value
                ENUM_VALUE_LOOKUP[enum_name] = current_value
                local_ctx[enum_name] = current_value
                current_value += 1
            ENUMS[name] = entries


def split_args(arg_string: str) -> list[str]:
    args: list[str] = []
    depth = 0
    current: list[str] = []
    for char in arg_string:
        if char in "({[":
            depth += 1
        elif char in ")}]":
            depth -= 1
        if char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    leftover = "".join(current).strip()
    if leftover:
        args.append(leftover)
    return args


def clean_string(value: str) -> str:
    value = value.strip()
    if value.startswith("F(") and value.endswith(")"):
        inner = value[2:-1].strip()
        if inner.startswith('"') and inner.endswith('"'):
            return inner.strip('"')
    if value.startswith('"') and value.endswith('"'):
        return value.strip('"')
    return value


def parse_numeric(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    float_candidate = value.rstrip("fF")
    if re.match(r"^-?\d*\.\d+(e[-+]?\d+)?$", float_candidate, re.I) or re.match(
        r"^-?\d+\.\d*(e[-+]?\d+)?$", float_candidate, re.I
    ):
        try:
            return float(float_candidate)
        except ValueError:
            pass
    if re.match(r"^-?\d+(e[-+]?\d+)?$", value, re.I):
        try:
            return int(value)
        except ValueError:
            pass
    try:
        return eval_int_expression(value, {})
    except Exception:
        return value


def parse_struct_fields(field_string: str) -> list[Any]:
    parts = split_args(field_string)
    parsed: list[Any] = []
    for index, part in enumerate(parts):
        if index == 3:
            parsed.append(clean_string(part))
        elif index in (0, 1, 4, 5):
            parsed.append(parse_numeric(part))
        else:
            part = part.strip()
            if part in {"true", "false"}:
                parsed.append(part == "true")
            else:
                parsed.append(clean_string(part))
    return parsed


def extract_preceding_comment(text: str, start: int) -> str | None:
    comment_lines: list[str] = []
    idx = start
    while idx > 0:
        line_start = text.rfind("\n", 0, idx - 1)
        if line_start == -1:
            candidate = text[:idx].strip()
            idx = 0
        else:
            candidate = text[line_start + 1 : idx].strip()
            idx = line_start
        if not candidate:
            continue
        if candidate.startswith("//"):
            comment_lines.insert(0, candidate[2:].strip())
            continue
        break
    return " ".join(comment_lines) if comment_lines else None


def collect_struct_assignments(
    source: str, raw_source: str, kind: str
) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"Protocol\.{}Registers\[(?P<index>[^\]]+)\]\s*=\s*sGrowattModbusReg_t\s*\{{(?P<fields>.*?)\}};".format(
            kind
        ),
        re.S,
    )
    assignments: list[dict[str, Any]] = []
    for match in pattern.finditer(source):
        index = match.group("index").strip()
        fields = parse_struct_fields(match.group("fields"))
        comment = extract_preceding_comment(raw_source, match.start())
        entry = {
            "enum": index,
            "enum_value": ENUM_VALUE_LOOKUP.get(index),
            "address": fields[0] if len(fields) > 0 else None,
            "default": fields[1] if len(fields) > 1 else None,
            "size": fields[2] if len(fields) > 2 else None,
            "label": fields[3] if len(fields) > 3 else None,
            "multiplier": fields[4] if len(fields) > 4 else None,
            "resolution": fields[5] if len(fields) > 5 else None,
            "unit": fields[6] if len(fields) > 6 else None,
            "frontend": fields[7] if len(fields) > 7 else None,
            "plot": fields[8] if len(fields) > 8 else None,
        }
        if comment:
            entry["comment"] = comment
        assignments.append(entry)
    return assignments


def collect_fragments(source: str, kind: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"Protocol\.{}ReadFragments\[(?P<index>[^\]]+)\]\s*=\s*sGrowattReadFragment_t\s*\{{(?P<fields>.*?)\}};".format(
            kind
        ),
        re.S,
    )
    fragments: list[dict[str, Any]] = []
    for match in pattern.finditer(source):
        index = match.group("index").strip()
        fields = split_args(match.group("fields"))
        start = parse_numeric(fields[0]) if fields else None
        size = parse_numeric(fields[1]) if len(fields) > 1 else None
        fragments.append(
            {
                "index": index,
                "start_address": start,
                "fragment_size": size,
            }
        )
    return fragments


def collect_counts(source: str) -> dict[str, Any]:
    counts: dict[str, Any] = {}
    for attr in (
        "InputRegisterCount",
        "HoldingRegisterCount",
        "InputFragmentCount",
        "HoldingFragmentCount",
    ):
        pattern = re.compile(rf"Protocol\.{attr}\s*=\s*([^;]+);")
        match = pattern.search(source)
        if match:
            counts[attr] = match.group(1).strip()
    return counts


def collect_setter_functions(source: str, file_name: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"std::tuple\s*<\s*bool\s*,\s*String\s*>\s*(\w+)\s*\((.*?)\)\s*\{",
        re.S,
    )
    setters: list[dict[str, Any]] = []
    for match in pattern.finditer(source):
        name = match.group(1)
        params = " ".join(match.group(2).split())
        setters.append(
            {
                "name": name,
                "parameters": params,
                "file": file_name,
            }
        )
    return setters


def build_devices() -> dict[str, Any]:
    devices: dict[str, Any] = {}
    for cpp_file in sorted(PROJECT_ROOT.glob("Growatt*.cpp")):
        raw_source = cpp_file.read_text(encoding="utf-8")
        source = strip_comments(raw_source)
        base = cpp_file.stem
        input_regs = collect_struct_assignments(source, raw_source, "Input")
        holding_regs = collect_struct_assignments(source, raw_source, "Holding")

        devices[base] = {
            "file": str(cpp_file.relative_to(PROJECT_ROOT)),
            "input_registers": input_regs,
            "holding_registers": holding_regs,
            "input_fragments": collect_fragments(source, "Input"),
            "holding_fragments": collect_fragments(source, "Holding"),
            "counts": collect_counts(source),
            "setters": collect_setter_functions(raw_source, cpp_file.name),
        }
    return devices


def parse_mqtt_doc() -> dict[str, Any]:
    if not MQTT_DOC_PATH.exists():
        return {}

    text = MQTT_DOC_PATH.read_text(encoding="utf-8")
    fields: dict[str, dict[str, Any]] = {}
    current_name: str | None = None
    """Parse MQTT documentation and return a mapping of topics to register metadata."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("name:"):
            current_name = stripped.split(":", 1)[1].strip().strip('"')
        match = re.search(r"value_json\.([A-Za-z0-9_]+)", line)
        if match:
            field = match.group(1)
            fields.setdefault(field, {"occurrences": []})
            if current_name:
                fields[field]["name"] = current_name
            fields[field]["occurrences"].append(line.strip())
        if not stripped or stripped.startswith(("- ", "service")):
            current_name = None

    commands: list[str] = []
    command_section = False
    for line in text.splitlines():
        if "The following MQTT commands" in line:
            command_section = True
            continue
        if command_section:
            if line.strip().startswith("```"):
                if commands:
                    break
                continue
            if line.strip() and not line.startswith("```"):
                commands.append(line.strip())

    return {
        "fields": fields,
        "commands": commands,
    }


def build_snapshot() -> dict[str, Any]:
    parse_enums()
    """Build a snapshot of all device register mappings and metadata."""
    return {
        "generated_at": datetime.now(datetime.UTC).isoformat(),
        "source": str(PROJECT_ROOT.relative_to(REPO_ROOT)),
        "devices": build_devices(),
        "metadata": {
            "enums": ENUMS,
            "mqtt_doc": parse_mqtt_doc(),
        },
    }


def main() -> None:
    """Main entry point for extraction script."""
    snapshot = build_snapshot()
    OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    # Use logging if needed, but avoid print statements in production


if __name__ == "__main__":
    main()
