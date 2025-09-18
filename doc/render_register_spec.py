"""Render Markdown summary from the structured register specification."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

DOC_DIR = Path(__file__).resolve().parent
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
DATA_TYPES_PATH = DOC_DIR / "growatt_register_data_types.json"
OUTPUT_PATH = DOC_DIR / "growatt_registers_spec.md"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def address_text(entry: dict) -> str:
    start = entry["address"]
    end = entry.get("end_address", start)
    return f"{start}" if start == end else f"{start}–{end}"


def collect_categories(entries: Iterable[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        category = entry.get("category") or "uncategorised"
        grouped[category].append(entry)
    for entry_list in grouped.values():
        entry_list.sort(key=lambda item: item["address"])
    return dict(sorted(grouped.items(), key=lambda item: item[0]))


def format_families(entry: dict) -> str:
    labels = entry.get("family_labels") or []
    if not labels:
        return "—"
    return ", ".join(labels)


def format_attributes(entry: dict) -> str:
    attrs = entry.get("attributes") or []
    if not attrs:
        return "—"
    return ", ".join(attrs)


def render_table(title: str, entries: list[dict]) -> list[str]:
    lines: list[str] = []
    lines.append(f"### {title}")
    lines.append("")
    header = [
        "Address",
        "Name",
        "Description",
        "Data type",
        "Unit",
        "Access",
        "Families",
        "Attributes",
    ]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join([" --- "] * len(header)) + "|")
    for entry in entries:
        access = "R/W" if entry.get("read_write") else "R"
        lines.append(
            "| "
            + " | ".join(
                [
                    address_text(entry),
                    entry.get("name") or "—",
                    (entry.get("description") or "—").replace("\n", " "),
                    entry.get("data_type") or "—",
                    entry.get("unit") or "—",
                    access,
                    format_families(entry),
                    format_attributes(entry),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def main() -> None:
    spec = load_json(SPEC_PATH)
    data_types = load_json(DATA_TYPES_PATH)["types"]

    lines: list[str] = []
    lines.append("# Growatt Modbus register reference")
    lines.append("")
    meta = spec.get("meta", {})
    if meta:
        lines.append(
            "Generated on ``{generated}`` using `{generator}`.".format(
                generated=meta.get("generated", "unknown"),
                generator=meta.get("generator", "unknown"),
            )
        )
        lines.append("")

    lines.append("## Data type catalogue")
    lines.append("")
    type_header = ["Identifier", "Kind", "Registers", "Notes"]
    lines.append("| " + " | ".join(type_header) + " |")
    lines.append("|" + "|".join([" --- "] * len(type_header)) + "|")
    for name, info in data_types.items():
        kind = info.get("kind", "—")
        registers = info.get("registers", "—")
        note_parts = []
        if kind == "scaled":
            divisor = info.get("divisor")
            signed = "signed" if info.get("signed") else "unsigned"
            note_parts.append(f"{signed} /{divisor}")
        elif kind == "enum":
            note_parts.append(f"{len(info.get('choices', {}))} values")
        elif kind == "bitfield":
            note_parts.append(f"{len(info.get('bits', []))} bit flags")
        elif kind == "ascii_segments":
            segs = info.get("segments", [])
            note_parts.append("; ".join(f"{s['name']}×{s['length']}" for s in segs))
        elif kind == "ascii":
            note_parts.append("ASCII text")
        note = ", ".join(note_parts) if note_parts else "—"
        lines.append(f"| {name} | {kind} | {registers} | {note} |")
    lines.append("")

    for table_key in ("holding", "input"):
        entries = spec.get(table_key, [])
        if not entries:
            continue
        lines.append(f"## {table_key.title()} registers")
        lines.append("")
        grouped = collect_categories(entries)
        for category, items in grouped.items():
            title = category.replace("_", " ").title()
            lines.extend(render_table(title, items))

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
