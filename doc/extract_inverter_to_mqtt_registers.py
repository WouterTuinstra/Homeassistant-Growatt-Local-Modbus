#!/usr/bin/env python3
"""Extract register mappings from inverter-to-mqtt-esp8266 Growatt sources."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = REPO_ROOT / "external" / "inverter-to-mqtt-esp8266"
SRC_GROWATT_DIR = PROJECT_ROOT / "src" / "growatt"
MARKDOWN_PATH = PROJECT_ROOT / "REGISTERS.md"
TOPICS_PATH = PROJECT_ROOT / "TOPICS.md"
OUTPUT_PATH = Path(__file__).resolve().parent / "inverter_to_mqtt_registers.json"


def strip_comments(source: str) -> str:
    """Remove C/C++ style comments from source code."""
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    source = re.sub(r"//.*", "", source)
    return source


def find_matching_brace(text: str, start: int) -> int:
    depth = 0
    for idx in range(start, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return idx
    return -1


def find_function_name(text: str, pos: int) -> str | None:
    snippet = text[:pos]
    matches = list(
        re.finditer(r"([A-Za-z0-9_:~]+::[A-Za-z0-9_]+)\s*\([^;]*\)\s*{", snippet)
    )
    if matches:
        return matches[-1].group(1)
    return None


def parse_numeric(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    # floating point candidate (optional trailing f/F)
    float_candidate = value.rstrip("fF")
    if re.fullmatch(r"-?\d*\.\d+(?:e[-+]?\d+)?", float_candidate, re.I) or re.fullmatch(
        r"-?\d+\.\d*(?:e[-+]?\d+)?", float_candidate, re.I
    ):
        try:
            return float(float_candidate)
        except ValueError:
            pass
    if re.fullmatch(r"-?\d+(?:e[-+]?\d+)?", value, re.I):
        try:
            return int(value)
        except ValueError:
            pass
    try:
        return int(value, 0)
    except ValueError:
        return value


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


def clean_label(value: str) -> str:
    value = value.strip()
    if value.startswith("F(") and value.endswith(")"):
        inner = value[2:-1].strip()
        if inner.startswith('"') and inner.endswith('"'):
            value = inner
    if value.startswith('"') and value.endswith('"'):
        return value.strip('"')
    return value


def parse_struct_fields(field_string: str) -> dict[str, Any]:
    parts = split_args(field_string)
    entry: dict[str, Any] = {}
    if len(parts) >= 1:
        entry["address"] = parse_numeric(parts[0])
    if len(parts) >= 2:
        entry["default"] = parse_numeric(parts[1])
    if len(parts) >= 3:
        entry["size"] = parts[2].strip()
    if len(parts) >= 4:
        entry["label"] = clean_label(parts[3])
    if len(parts) >= 5:
        entry["multiplier"] = parse_numeric(parts[4])
    if len(parts) >= 6:
        entry["resolution"] = parse_numeric(parts[5])
    if len(parts) >= 7:
        entry["unit"] = clean_label(parts[6])
    if len(parts) >= 8:
        entry["frontend"] = parse_numeric(parts[7])
    if len(parts) >= 9:
        entry["plot"] = parse_numeric(parts[8])
    return entry


def parse_read_blocks(source: str, file_name: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"read(Input|Holding)Registers\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*;"
    )
    entries: list[dict[str, Any]] = []
    idx = 0
    while True:
        match = pattern.search(source, idx)
        if not match:
            break
        kind = match.group(1).lower()
        start_reg = int(match.group(2))
        length = int(match.group(3))
        idx = match.end()
        brace_pos = source.find("{", idx)
        if brace_pos == -1:
            continue
        block_end = find_matching_brace(source, brace_pos)
        if block_end == -1:
            continue
        block = source[brace_pos + 1 : block_end]
        func_name = find_function_name(source, match.start())
        assignment_pattern = re.compile(r"this->([A-Za-z0-9_]+)\s*=\s*([^;]+);")
        block_entries: list[dict[str, Any]] = []
        for assign in assignment_pattern.finditer(block):
            variable = assign.group(1)
            expression = assign.group(2).strip()
            buffer_indexes = [
                int(n) for n in re.findall(r"getResponseBuffer\((\d+)\)", expression)
            ]
            if not buffer_indexes:
                continue
            registers = [start_reg + n for n in buffer_indexes]
            block_entries.append(
                {
                    "variable": variable,
                    "expression": expression,
                    "buffer_indexes": buffer_indexes,
                    "registers": registers,
                }
            )
        entries.append(
            {
                "type": kind,
                "block_start_register": start_reg,
                "block_length": length,
                "function": func_name,
                "file": file_name,
                "entries": block_entries,
            }
        )
        idx = block_end + 1
    return entries


def parse_write_calls(source: str, file_name: str) -> list[dict[str, Any]]:
    writes: list[dict[str, Any]] = []
    for match in re.finditer(r"write(?:Multiple)?Registers\s*\((\d+)", source):
        writes.append(
            {
                "call": match.group(0).split("(")[0].strip(),
                "address": int(match.group(1)),
                "file": file_name,
            }
        )
    for match in re.finditer(r"WriteHoldingReg(?:Frag)?\s*\((\d+)", source):
        writes.append(
            {
                "call": match.group(0).split("(")[0].strip(),
                "address": int(match.group(1)),
                "file": file_name,
            }
        )
    return writes


def parse_get_address_functions(source: str, file_name: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for match in re.finditer(r"([A-Za-z0-9_:]+::getAddress)\s*\(\s*\)", source):
        brace_start = source.find("{", match.end())
        if brace_start == -1:
            continue
        brace_end = find_matching_brace(source, brace_start)
        if brace_end == -1:
            continue
        body = source[brace_start + 1 : brace_end]
        return_matches = re.findall(r"return\s+(0x[0-9a-fA-F]+|\d+)\s*;", body)
        returns = [int(value, 0) for value in return_matches]
        results.append(
            {
                "function": match.group(1),
                "file": file_name,
                "returns": returns,
            }
        )
    return results


def collect_data_set_calls(source: str, file_name: str) -> list[dict[str, Any]]:
    pattern = re.compile(r"data\.set\(\s*(?P<key>[^,]+?)\s*,\s*(?P<value>[^;]+?)\);")
    calls: list[dict[str, Any]] = []
    for match in pattern.finditer(source):
        key_expr = match.group("key").strip()
        value_expr = match.group("value").strip()
        calls.append(
            {
                "file": file_name,
                "key_expression": key_expr,
                "value_expression": value_expr,
            }
        )
    return calls


def parse_cpp_sources() -> dict[str, Any]:
    files_data: dict[str, Any] = {}
    for cpp_path in sorted(SRC_GROWATT_DIR.glob("*.cpp")):
        text = cpp_path.read_text(encoding="utf-8")
        clean = strip_comments(text)
        file_key = str(cpp_path.relative_to(PROJECT_ROOT))
        files_data[file_key] = {
            "reads": parse_read_blocks(clean, file_key),
            "writes": parse_write_calls(clean, file_key),
            "address_functions": parse_get_address_functions(clean, file_key),
            "data_set_calls": collect_data_set_calls(clean, file_key),
        }
    return files_data


def parse_markdown() -> dict[str, list[dict[str, Any]]]:
    if not MARKDOWN_PATH.exists():
        return {}
    sections: dict[str, list[dict[str, Any]]] = {}
    current_section: str | None = None
    in_code_block = False
    block_lines: list[str] = []
    for line in MARKDOWN_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code_block and current_section:
                entries: list[dict[str, Any]] = []
                for block_line in block_lines:
                    block_line = block_line.strip()
                    if not block_line or block_line.startswith("#"):
                        continue
                    match = re.match(r"(\d+)\s+(.+)", block_line)
                    if match:
                        entries.append(
                            {
                                "address": int(match.group(1)),
                                "text": match.group(2).strip(),
                            }
                        )
                sections.setdefault(current_section, []).extend(entries)
                block_lines = []
            in_code_block = not in_code_block
            continue
        if stripped.startswith("## "):
            current_section = stripped[3:].strip().lower().replace(" ", "_")
            continue
        if in_code_block:
            block_lines.append(line)
    return sections


def parse_topics() -> dict[str, list[dict[str, str]]]:
    if not TOPICS_PATH.exists():
        return {}

    sections: dict[str, list[dict[str, str]]] = {}
    current_section: str | None = None

    for line in TOPICS_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current_section = stripped[3:].strip().lower().replace(" ", "_")
            continue
        if not stripped.startswith("|"):
            continue
        # Skip header separator rows consisting of dashes
        if re.match(r"^\|\s*-+\s*\|", stripped):
            continue
        columns = [col.strip() for col in stripped.strip("|").split("|")]
        if len(columns) < 4:
            continue
        # Skip header row
        if columns[0].lower() in {"topic", "`topic"}:
            continue
        entry = {
            "topic": columns[0].strip("`"),
            "units": columns[1],
            "format": columns[2],
            "description": columns[3],
        }
        if current_section is None:
            current_section = "general"
        sections.setdefault(current_section, []).append(entry)
    return sections


def _extract_topic_key(expr: str) -> str | None:
    """Extract a literal MQTT topic key from an expression like F("Vpv1")."""
    s = expr.strip()
    # Remove F(...) wrappers commonly used for flash strings
    if s.startswith("F(") and s.endswith(")"):
        s = s[2:-1].strip()
    # Remove parentheses if they remain
    if s.startswith("(") and s.endswith(")") and len(s) > 1:
        s = s[1:-1].strip()
    # Strip quotes
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return s[1:-1]
    return None


def _compute_var_to_topic(files_data: dict[str, Any]) -> None:
    """Add mqtt_var_to_topic and mqtt_keys per file by correlating data.set calls with variables."""
    ident_re = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b")
    for info in files_data.values():
        # Collect variables defined by read blocks
        variables: set[str] = set()
        for read in info.get("reads", []):
            for ent in read.get("entries", []):
                var = ent.get("variable")
                if isinstance(var, str):
                    variables.add(var)
        var_to_topic: dict[str, str] = {}
        for call in info.get("data_set_calls", []):
            key_expr = call.get("key_expression")
            val_expr = call.get("value_expression")
            topic = _extract_topic_key(key_expr) if isinstance(key_expr, str) else None
            if not topic or not isinstance(val_expr, str):
                continue
            # Find identifiers and map those that match known variables
            ids = {m.group(1) for m in ident_re.finditer(val_expr)}
            for var in ids & variables:
                var_to_topic.setdefault(var, topic)
        if var_to_topic:
            info["mqtt_var_to_topic"] = var_to_topic
            info["mqtt_keys"] = sorted(set(var_to_topic.values()))


def build_snapshot() -> dict[str, Any]:
    """Return a JSON-serialisable snapshot of registers, topics, and code mapping."""
    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(PROJECT_ROOT.relative_to(REPO_ROOT)),
        "markdown_registers": parse_markdown(),
        "topics": parse_topics(),
        "code": parse_cpp_sources(),
    }
    # Enrich with variable-to-topic mapping per file
    _compute_var_to_topic(snapshot["code"])  # type: ignore[arg-type]
    return snapshot


def main() -> None:
    """Generate the inverter_to_mqtt_registers.json artifact."""
    snapshot = build_snapshot()
    OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(Path(__file__).resolve().parent)}")


if __name__ == "__main__":
    main()
