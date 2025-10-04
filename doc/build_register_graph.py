#!/usr/bin/env python3
"""Build a knowledge graph of Growatt registers and related artefacts."""

from __future__ import annotations

import argparse
import json
import pickle
import re
from collections import defaultdict
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "networkx is required. Install with `pip install networkx` inside the dev container."
    ) from exc

# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

CANONICAL_FIELDS = (
    "length_bytes",
    "signed",
    "textual",
    "divide",
    "scale",
    "multiplier",
    "unit",
    "text_category",
)


TEXT_SERIAL_KEYWORDS = (
    "serial",
    "serialnumber",
    "serialno",
    "pvserial",
    "datalogserial",
    "inverterserial",
)


def slugify(value: str, *, default: str = "section") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or default


def find_enclosing_range(
    graph: nx.MultiDiGraph,
    table: str,
    start: Optional[int],
    end: Optional[int],
) -> Optional[str]:
    if start is None or end is None:
        return None
    best_id: Optional[str] = None
    best_span: Optional[int] = None
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "register_range" or attrs.get("table") != table:
            continue
        range_start = attrs.get("start_register")
        range_end = attrs.get("end_register")
        if range_start is None or range_end is None:
            continue
        if range_start <= start and range_end >= end:
            span = range_end - range_start
            if best_span is None or span < best_span:
                best_id = node_id
                best_span = span
    return best_id


def classify_textual_payload(*hints: Optional[Any]) -> Optional[str]:
    """Infer a semantic category for textual payloads (serial, model, etc.)."""

    values: List[str] = []
    for hint in hints:
        if hint is None:
            continue
        if isinstance(hint, (list, tuple, set)):
            values.extend(str(item) for item in hint if item is not None)
        else:
            values.append(str(hint))

    if not values:
        return None

    combined = " ".join(values).strip().lower()
    if not combined:
        return None

    tokens = [token for token in re.split(r"[^a-z0-9]+", combined) if token]
    token_set = set(tokens)

    if any(keyword in combined for keyword in TEXT_SERIAL_KEYWORDS) or "sn" in token_set:
        return "serial_number"
    if "imei" in token_set:
        return "imei"
    if "esn" in token_set:
        return "esn"
    if "mac" in token_set or "macaddress" in combined:
        return "mac_address"
    if "firmware" in token_set or "fw" in token_set or "version" in token_set:
        return "firmware_version"
    if "timestamp" in token_set or "datetime" in token_set or (
        "date" in token_set and "time" in token_set
    ):
        return "timestamp_ascii"
    if "model" in token_set or "modelno" in token_set:
        return "device_model"
    if "type" in token_set and (
        "device" in token_set
        or "inverter" in token_set
        or "battery" in token_set
        or "bdc" in token_set
    ):
        return "device_model"

    return None


def register_range_node_id(table: str, start: int, end: int) -> str:
    return f"register_range:{table}:{start}-{end}"


def ensure_register_range(
    graph: nx.MultiDiGraph,
    table: str,
    start: int,
    end: int,
    *,
    note: Optional[str] = None,
    source: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    if end < start:
        start, end = end, start
    registry: Dict[Tuple[str, int, int], str] = graph.graph.setdefault(
        "register_ranges", {}
    )
    key = (table, start, end)
    node_id = registry.get(key)
    if node_id is None:
        node_id = register_range_node_id(table, start, end)
        ensure_node(
            graph,
            node_id,
            type="register_range",
            table=table,
            start_register=start,
            end_register=end,
            length=end - start + 1,
        )
        registry[key] = node_id
    else:
        ensure_node(
            graph,
            node_id,
            table=table,
            start_register=start,
            end_register=end,
            length=end - start + 1,
        )

    if note:
        notes = graph.nodes[node_id].setdefault("notes", set())
        notes.add(note)

    if source and metadata:
        meta = graph.nodes[node_id].setdefault("metadata", defaultdict(list))
        meta[source].append(metadata)

    return node_id


VENDOR_DEVICE_RANGE_SPECS = [
    {
        "id": "tlx_family",
        "name": "TL-X / TL-XH / TL-XH US (MIN)",
        "aliases": ["tlx", "tlxh", "min"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 3000, "end": 3124},
                {"start": 3125, "end": 3249, "note": "Applies to TL-XH US variants."},
            ],
            "input": [
                {"start": 3000, "end": 3124},
                {"start": 3125, "end": 3249},
                {"start": 3250, "end": 3374, "note": "Applies to TL-XH variants."},
            ],
        },
    },
    {
        "id": "tl3_x_family",
        "name": "TL3-X (MAX, MID, MAC)",
        "aliases": ["tl3"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 125, "end": 249},
            ],
            "input": [
                {"start": 0, "end": 124},
                {"start": 125, "end": 249},
            ],
        },
    },
    {
        "id": "max_family",
        "name": "MAX 1500V / MAX-X LV",
        "aliases": ["max"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 125, "end": 249},
            ],
            "input": [
                {"start": 0, "end": 124},
                {"start": 125, "end": 249},
                {"start": 875, "end": 999},
            ],
        },
    },
    {
        "id": "mod_tl3_xh",
        "name": "MOD TL3-XH",
        "aliases": ["mod"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 3000, "end": 3124},
            ],
            "input": [
                {"start": 3000, "end": 3124},
                {"start": 3125, "end": 3249},
            ],
        },
    },
    {
        "id": "storage_mix",
        "name": "Storage (MIX)",
        "aliases": ["storage", "mix"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 1000, "end": 1124},
            ],
            "input": [
                {"start": 0, "end": 124},
                {"start": 1000, "end": 1124},
            ],
        },
    },
    {
        "id": "storage_spa",
        "name": "Storage (SPA)",
        "aliases": ["spa"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 1000, "end": 1124},
            ],
            "input": [
                {"start": 1000, "end": 1124},
                {"start": 1125, "end": 1249},
                {"start": 2000, "end": 2124},
            ],
        },
    },
    {
        "id": "storage_sph",
        "name": "Storage (SPH)",
        "aliases": ["sph"],
        "ranges": {
            "holding": [
                {"start": 0, "end": 124},
                {"start": 1000, "end": 1124},
            ],
            "input": [
                {"start": 0, "end": 124},
                {"start": 1000, "end": 1124},
                {"start": 1125, "end": 1249},
            ],
        },
    },
]


REPEATED_SECTION_SPECS = [
    {
        "id": "bdc_slots",
        "table": "holding",
        "template_range": (3085, 3124),
        "instance_start": 5000,
        "slot_size": 40,
        "slot_count": 10,
        "label": "Battery DC converters",
        "slot_label": "BDC Slot {index}",
    },
]


def section_node_id(table: str, start: int, end: int, slug: str) -> str:
    return f"section:{table}:{start}-{end}:{slug}"


def ensure_section(
    graph: nx.MultiDiGraph,
    section_id: str,
    *,
    table: str,
    start: int,
    end: int,
    label: Optional[str] = None,
    index: Optional[int] = None,
    kind: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    ensure_node(
        graph,
        section_id,
        type="register_section",
        table=table,
        start_register=start,
        end_register=end,
        label=label,
        index=index,
        kind=kind,
    )
    if metadata:
        meta = graph.nodes[section_id].setdefault("metadata", defaultdict(list))
        for key, value in metadata.items():
            meta[key].append(value)
    return section_id


def add_section_range_link(
    graph: nx.MultiDiGraph,
    section_id: str,
    range_id: str,
) -> None:
    add_edge(graph, section_id, range_id, type="SECTION_IN_RANGE")
    add_edge(graph, range_id, section_id, type="RANGE_HAS_SECTION")


def add_section_child(
    graph: nx.MultiDiGraph,
    parent_section: str,
    child_section: str,
    *,
    index: Optional[int] = None,
) -> None:
    add_edge(graph, parent_section, child_section, type="SECTION_HAS_CHILD", index=index)
    add_edge(graph, child_section, parent_section, type="SECTION_CHILD_OF", index=index)


def _normalise_for_signature(value: Any) -> str:
    if value is None:
        return "?"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:g}"
    return str(value)


def make_canonical_signature(attrs: Dict[str, Any], conflicts: Dict[str, set]) -> str:
    parts: list[str] = []
    for field in CANONICAL_FIELDS:
        if conflicts.get(field):
            parts.append(f"{field}:conflict")
            continue
        value = attrs.get(field)
        parts.append(f"{field}:{_normalise_for_signature(value)}")
    return "|".join(parts)


def merge_value(target: Dict[str, set], field: str, value: Any) -> None:
    if value is None:
        return
    bucket = target.setdefault(field, set())
    bucket.add(value)


def collect_enum_metadata(
    graph: nx.MultiDiGraph, dtype_id: str
) -> Tuple[Dict[Any, Dict[str, Any]], Dict[int, Dict[str, Any]]]:
    enum_by_value: Dict[Any, Dict[str, Any]] = {}
    bitflag_by_bit: Dict[int, Dict[str, Any]] = {}
    for _, target, edge_data in graph.out_edges(dtype_id, data=True):
        edge_type = edge_data.get("type")
        if edge_type == "DATATYPE_HAS_ENUM_VALUE":
            node = graph.nodes.get(target, {})
            value = node.get("value")
            if value is None:
                continue
            existing = enum_by_value.setdefault(value, {})
            if node.get("label"):
                existing.setdefault("label", node.get("label"))
            if node.get("description"):
                existing.setdefault("description", node.get("description"))
            sources = existing.setdefault("sources", set())
            src = graph.nodes[dtype_id].get("namespace")
            if src:
                sources.add(src)
        elif edge_type == "DATATYPE_HAS_BITFLAG":
            node = graph.nodes.get(target, {})
            bit = node.get("bit")
            if bit is None:
                continue
            existing = bitflag_by_bit.setdefault(bit, {})
            if node.get("label"):
                existing.setdefault("label", node.get("label"))
            if node.get("description"):
                existing.setdefault("description", node.get("description"))
            sources = existing.setdefault("sources", set())
            src = graph.nodes[dtype_id].get("namespace")
            if src:
                sources.add(src)
    return enum_by_value, bitflag_by_bit


def serialise_enum_payload(enum_by_value: Dict[Any, Dict[str, Any]]) -> list[Dict[str, Any]]:
    payload: list[Dict[str, Any]] = []
    for value in sorted(enum_by_value, key=lambda item: (str(type(item)), item)):
        meta = enum_by_value[value]
        entry = {"value": value}
        if meta.get("label"):
            entry["label"] = meta["label"]
        if meta.get("description"):
            entry["description"] = meta["description"]
        if meta.get("sources"):
            entry["sources"] = sorted(meta["sources"])
        payload.append(entry)
    return payload


def serialise_bitflag_payload(bitflag_by_bit: Dict[int, Dict[str, Any]]) -> list[Dict[str, Any]]:
    payload: list[Dict[str, Any]] = []
    for bit in sorted(bitflag_by_bit):
        meta = bitflag_by_bit[bit]
        entry = {"bit": bit}
        if meta.get("label"):
            entry["label"] = meta["label"]
        if meta.get("description"):
            entry["description"] = meta["description"]
        if meta.get("sources"):
            entry["sources"] = sorted(meta["sources"])
        payload.append(entry)
    return payload

DOC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOC_DIR.parent

VENDOR_TABLE_PATH = DOC_DIR / "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json"
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
HA_LOCAL_PATH = DOC_DIR / "HA_local_registers.json"
OPENINVERTER_PATH = DOC_DIR / "openinverter_gateway_registers.json"
INVERTER_TO_MQTT_PATH = DOC_DIR / "inverter_to_mqtt_registers.json"
GROTT_LAYOUTS_PATH = DOC_DIR / "grott_register_layouts.json"
VENDOR_MANUAL_PDF_PATH = DOC_DIR / "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf"

DEFAULT_OUTPUT = DOC_DIR / "register_graph.gpickle"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def sha256sum(path: Path) -> Optional[str]:
    try:
        import hashlib

        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except FileNotFoundError:
        return None


def load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_node(graph: nx.MultiDiGraph, node_id: str, **attrs: Any) -> None:
    if graph.has_node(node_id):
        graph.nodes[node_id].update({k: v for k, v in attrs.items() if v is not None})
    else:
        graph.add_node(node_id, **attrs)


def add_edge(graph: nx.MultiDiGraph, node_u: str, node_v: str, **attrs: Any) -> None:
    graph.add_edge(node_u, node_v, **attrs)


def register_node_id(table: Optional[str], register: int) -> str:
    table_part = table if table else "unknown"
    return f"register:{table_part}:{register}"


def block_node_id(table: str, start: int, end: int) -> str:
    if start == end:
        return f"block:{table}:{start}"
    return f"block:{table}:{start}-{end}"


def grott_field_node_id(layout: str, field: str) -> str:
    return f"grott_field:{layout}:{field}"


def data_type_node_id(namespace: str, signature: str) -> str:
    return f"datatype:{namespace}:{signature}"


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ensure_canonical_datatype(
    graph: nx.MultiDiGraph,
    namespace: str,
    *,
    length: Optional[int] = None,
    signed: Optional[bool] = None,
    textual: bool = False,
    text_category: Optional[str] = None,
    divide: Optional[Any] = None,
    scale: Optional[Any] = None,
    multiplier: Optional[Any] = None,
    unit: Optional[str] = None,
    raw: Optional[Dict[str, Any]] = None,
    annotations: Optional[Iterable[Dict[str, Any]]] = None,
) -> str:
    parts: list[str] = []
    if length is not None:
        parts.append(f"len{length}")
    if textual:
        parts.append("text")
        if text_category:
            parts.append(f"textcat:{text_category}")
    else:
        if signed is True:
            parts.append("signed")
        elif signed is False:
            parts.append("unsigned")
    if divide is not None:
        parts.append(f"div{divide}")
    if scale is not None:
        parts.append(f"scale{scale}")
    if multiplier is not None:
        parts.append(f"mult{multiplier}")
    if unit:
        parts.append(f"unit:{unit}")
    if not parts:
        parts.append("unknown")
    signature = "|".join(parts)
    node_id = data_type_node_id(namespace, signature)
    existing_annotations: List[Dict[str, Any]] = []
    if graph.has_node(node_id):
        existing = graph.nodes[node_id].get("annotations")
        if isinstance(existing, list):
            existing_annotations = list(existing)

    attrs = {
        "type": "data_type",
        "namespace": namespace,
        "length_bytes": length,
        "signed": signed,
        "textual": textual,
        "text_category": text_category if textual else None,
        "divide": divide,
        "scale": scale,
        "multiplier": multiplier,
        "unit": unit,
    }
    if raw is not None:
        attrs["raw"] = raw
    consolidated_annotations: List[Dict[str, Any]] = list(existing_annotations)
    if annotations:
        for note in annotations:
            if note and note not in consolidated_annotations:
                consolidated_annotations.append(note)
    if consolidated_annotations:
        attrs["annotations"] = consolidated_annotations
    ensure_node(graph, node_id, **attrs)
    return node_id


def ensure_canonical_from_datatype(
    graph: nx.MultiDiGraph,
    dtype_id: str,
    source: Optional[str] = None,
) -> str:
    dtype_attrs = graph.nodes.get(dtype_id, {})
    aggregated_attrs = {field: dtype_attrs.get(field) for field in CANONICAL_FIELDS}
    signature = make_canonical_signature(aggregated_attrs, {})
    canonical_id = data_type_node_id("canonical", signature)

    existing = graph.nodes.get(canonical_id, {}) if graph.has_node(canonical_id) else {}
    sources = set(existing.get("sources", []))
    source_datatypes = set(existing.get("source_datatypes", []))
    annotations: List[Dict[str, Any]] = []
    if existing.get("annotations"):
        annotations.extend(existing["annotations"])
    dtype_annotations = dtype_attrs.get("annotations")
    if isinstance(dtype_annotations, list):
        for note in dtype_annotations:
            if note and note not in annotations:
                annotations.append(note)
    if source:
        sources.add(source)
    source_datatypes.add(dtype_id)

    canon_attrs = {
        "type": "data_type",
        "namespace": "canonical",
        **aggregated_attrs,
    }
    if sources:
        canon_attrs["sources"] = sorted(sources)
    if source_datatypes:
        canon_attrs["source_datatypes"] = sorted(source_datatypes)
    if annotations:
        canon_attrs["annotations"] = annotations

    ensure_node(graph, canonical_id, **canon_attrs)

    existing_edges = graph.get_edge_data(canonical_id, dtype_id) or {}
    if all(data.get("type") != "CANONICAL_FROM_DATATYPE" for data in existing_edges.values()):
        add_edge(graph, canonical_id, dtype_id, type="CANONICAL_FROM_DATATYPE", source=source)

    return canonical_id


def parse_register_range(value: Optional[str]) -> Optional[Tuple[int, int]]:
    if not value:
        return None
    token = value.strip().strip(".")
    if not token:
        return None
    token = token.replace(" ", "")
    if any(symbol in token for symbol in ("+", "*", "(", ")")):
        # Algebraic expressions (e.g. the BDC array description) cannot be
        # resolved to concrete register numbers at this stage.
        return None
    if "~" in token or "-" in token:
        for sep in ("~", "-"):
            if sep in token:
                parts = token.split(sep)
                if len(parts) != 2:
                    continue
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                except ValueError:
                    continue
                if end < start:
                    start, end = end, start
                return start, end
    try:
        register = int(token)
        return register, register
    except ValueError:
        digits = ''.join(ch if ch.isdigit() else ' ' for ch in token).split()
        if not digits:
            return None
        try:
            start = int(digits[0])
        except ValueError:
            return None
        if len(digits) > 1:
            try:
                end = int(digits[1])
            except ValueError:
                end = start
        else:
            end = start
        if end < start:
            start, end = end, start
        return start, end


# ---------------------------------------------------------------------------
# Ingestion helpers
# ---------------------------------------------------------------------------

def add_source_document(graph: nx.MultiDiGraph, name: str, path: Path) -> str:
    node_id = f"source:{name}"
    ensure_node(
        graph,
        node_id,
        type="source_document",
        name=name,
        path=str(path.relative_to(PROJECT_ROOT)) if path.exists() else str(path),
        sha256=sha256sum(path),
    )
    return node_id


def ensure_register(
    graph: nx.MultiDiGraph,
    register: int,
    table: Optional[str],
    *,
    source: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> str:
    node_id = register_node_id(table, register)
    attrs: Dict[str, Any] = {
        "type": "register",
        "register": register,
    }
    if table:
        attrs["table"] = table
    ensure_node(graph, node_id, **attrs)
    if source:
        sources = graph.nodes[node_id].setdefault("sources", set())
        sources.add(source)
    if data:
        payloads = graph.nodes[node_id].setdefault("payloads", defaultdict(list))
        payloads[source or "unknown"].append(data)
    return node_id


def ensure_block(
    graph: nx.MultiDiGraph,
    table: str,
    start: int,
    end: int,
    *,
    source: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> str:
    range_id = ensure_register_range(
        graph,
        table,
        start,
        end,
        note=data.get("note") if data else None,
        source=source,
        metadata=data,
    )

    node_id = block_node_id(table, start, end)
    ensure_node(
        graph,
        node_id,
        type="register_block",
        table=table,
        start_register=start,
        end_register=end,
    )
    add_edge(graph, range_id, node_id, type="RANGE_INCLUDES_BLOCK")
    add_edge(graph, node_id, range_id, type="BLOCK_BELONGS_TO_RANGE")
    if source and data:
        blocks = graph.nodes[node_id].setdefault("metadata", defaultdict(list))
        blocks[source].append(data)
    return node_id


def ingest_vendor_tables(graph: nx.MultiDiGraph) -> None:
    data = load_json(VENDOR_TABLE_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "vendor_tables", VENDOR_TABLE_PATH)
    for table in ("holding", "input"):
        rows = data.get(table, [])
        for row in rows:
            reg_range = parse_register_range(str(row.get("register")))
            if not reg_range:
                continue
            start, end = reg_range
            block_id = ensure_block(graph, table, start, end, source="vendor", data=row)
            range_id = ensure_register_range(graph, table, start, end)
            add_edge(graph, block_id, source_id, type="SOURCED_FROM")
            for register in range(start, end + 1):
                reg_id = ensure_register(
                    graph,
                    register,
                    table,
                    source="vendor",
                    data=row,
                )
                add_edge(graph, block_id, reg_id, type="BLOCK_CONTAINS")
                add_edge(graph, reg_id, block_id, type="REGISTER_IN_BLOCK")
                add_edge(graph, range_id, reg_id, type="RANGE_CONTAINS_REGISTER")
                add_edge(graph, reg_id, range_id, type="REGISTER_IN_RANGE")
                add_edge(graph, reg_id, source_id, type="SOURCED_FROM")


def ingest_curated_spec(graph: nx.MultiDiGraph) -> None:
    data = load_json(SPEC_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "growatt_registers_spec", SPEC_PATH)
    for table in ("holding", "input"):
        entries = data.get(table, [])
        for entry in entries:
            if entry.get("type") != "entry":
                continue
            start = entry.get("register_start")
            end = entry.get("register_end") or start
            if start is None:
                continue
            if end is None:
                end = start
            if end < start:
                start, end = end, start
            block_id = ensure_block(graph, table, start, end, source="spec", data=entry)
            range_id = ensure_register_range(graph, table, start, end)
            add_edge(graph, block_id, source_id, type="SOURCED_FROM")
            for register in range(start, end + 1):
                reg_id = ensure_register(
                    graph,
                    register,
                    table,
                    source="spec",
                    data=entry,
                )
                add_edge(graph, reg_id, source_id, type="SOURCED_FROM")
                add_edge(graph, reg_id, block_id, type="REGISTER_IN_BLOCK")
                add_edge(graph, range_id, reg_id, type="RANGE_CONTAINS_REGISTER")
                add_edge(graph, reg_id, range_id, type="REGISTER_IN_RANGE")


def infer_table_from_register(register: int) -> Optional[str]:
    if register <= 124:
        return "holding"
    if register >= 3000:
        return "input"
    return None


def infer_table_from_group_name(group_name: Optional[str]) -> Optional[str]:
    if not group_name:
        return None
    if group_name.startswith("holding"):
        return "holding"
    if group_name.startswith("input"):
        return "input"
    return None


def ingest_grott_layouts(graph: nx.MultiDiGraph) -> None:
    data = load_json(GROTT_LAYOUTS_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "grott_register_layouts", GROTT_LAYOUTS_PATH)
    exported_at = data.get("exported_at")
    version = data.get("grott_version")
    layout_meta = data.get("layouts", {})

    for layout_id, layout in layout_meta.items():
        layout_node = f"grott_layout:{layout_id}"
        ensure_node(
            graph,
            layout_node,
            type="grott_layout",
            layout=layout_id,
            exported_at=exported_at,
            grott_version=version,
        )
        add_edge(graph, layout_node, source_id, type="SOURCED_FROM")
        for field in layout.get("fields", []):
            field_name = field.get("field") or field.get("name")
            if not field_name:
                continue
            field_node = grott_field_node_id(layout_id, field_name)
            ensure_node(
                graph,
                field_node,
                type="grott_field",
                layout=layout_id,
                field=field_name,
                byte_offset=field.get("byte_offset") or field.get("value"),
                length_bytes=field.get("length_bytes") or field.get("length"),
                divide=field.get("divide"),
                raw=field,
            )
            add_edge(graph, layout_node, field_node, type="LAYOUT_CONTAINS_FIELD")
            add_edge(graph, field_node, source_id, type="SOURCED_FROM")

            field_type = field.get("type") or ""
            length = field.get("length_bytes") or field.get("length")
            divide = field.get("divide")
            signed = None
            textual = False
            text_category: Optional[str] = None
            annotations: Optional[List[Dict[str, Any]]] = None
            if field_type == "numx":
                signed = True
            elif field_type == "num":
                signed = False
            elif field_type == "text":
                textual = True
                extra = field.get("extra")
                extra_hints: List[Any] = []
                if isinstance(extra, dict):
                    extra_hints.extend(extra.values())
                elif isinstance(extra, (list, tuple, set)):
                    extra_hints.extend(extra)
                elif extra is not None:
                    extra_hints.append(extra)
                text_category = classify_textual_payload(
                    field_name,
                    field.get("field"),
                    field.get("name"),
                    field.get("description"),
                    field.get("label"),
                    field.get("mqtt_topic"),
                    *extra_hints,
                )
                annotation: Dict[str, Any] = {
                    "source": "grott",
                    "layout": layout_id,
                    "field": field_name,
                    "expected_charset": "ASCII",
                }
                if length is not None:
                    try:
                        annotation["length_bytes"] = int(length)
                    except (TypeError, ValueError):
                        annotation["length_bytes"] = length
                if field.get("include_by_default") is not None:
                    annotation["include_by_default"] = field.get("include_by_default")
                if field.get("divide"):
                    annotation["divide"] = field.get("divide")
                if extra_hints:
                    annotation["notes"] = [str(hint) for hint in extra_hints if hint is not None]
                annotations = [annotation]

            dtype_id = ensure_canonical_datatype(
                graph,
                "grott",
                length=length,
                signed=signed,
                textual=textual,
                text_category=text_category,
                divide=divide,
                raw={"type": field_type},
                annotations=annotations,
            )
            ensure_canonical_from_datatype(graph, dtype_id, source="grott")
            add_edge(graph, field_node, dtype_id, type="FIELD_HAS_DATATYPE")

            reg_start = field.get("register_start")
            reg_end = field.get("register_end") or reg_start
            if reg_start is not None:
                if reg_end is None:
                    reg_end = reg_start
                if reg_end < reg_start:
                    reg_start, reg_end = reg_end, reg_start
                for register in range(reg_start, reg_end + 1):
                    table = infer_table_from_register(register)
                    reg_id = ensure_register(
                        graph,
                        register,
                        table,
                        source="grott",
                        data={"layout": layout_id, "field": field_name},
                    )
                    add_edge(graph, field_node, reg_id, type="FIELD_MAPS_REGISTER")

                    add_edge(
                        graph,
                        reg_id,
                        dtype_id,
                        type="REGISTER_HAS_DATATYPE",
                        source="grott",
                        layout=layout_id,
                        field=field_name,
                    )


def ingest_ha_registers(graph: nx.MultiDiGraph) -> None:
    data = load_json(HA_LOCAL_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "ha_local_registers", HA_LOCAL_PATH)
    devices = data.get("devices", {})
    for device, groups in devices.items():
        for group_name, entries in groups.items():
            if not isinstance(entries, list):
                continue
            if not group_name:
                continue
            table = "holding" if group_name.startswith("holding") else "input"
            for entry in entries:
                register = entry.get("register")
                if register is None:
                    continue
                reg_id = ensure_register(
                    graph,
                    register,
                    table,
                    source="home_assistant",
                    data={"device": device, **entry},
                )
                ha_entity = f"ha_entity:{device}:{entry.get('name')}"
                ensure_node(
                    graph,
                    ha_entity,
                    type="ha_entity",
                    device=device,
                    name=entry.get("name"),
                    group=group_name,
                )
                add_edge(graph, ha_entity, reg_id, type="ENTITY_MAPS_REGISTER")
                add_edge(graph, ha_entity, source_id, type="SOURCED_FROM")
                add_edge(graph, reg_id, source_id, type="SOURCED_FROM")

                length = entry.get("length")
                length = int(length) if isinstance(length, (int, float, str)) and str(length).isdigit() else None
                scale = safe_float(entry.get("scale"))
                value_type = entry.get("value_type") or ""
                vt_lower = value_type.lower()
                textual = vt_lower.startswith("str")
                signed: Optional[bool]
                if vt_lower.startswith("i"):
                    signed = True
                elif vt_lower.startswith("u"):
                    signed = False
                else:
                    signed = None
                text_category = None
                if textual:
                    text_category = classify_textual_payload(
                        entry.get("name"),
                        entry.get("attribute"),
                        entry.get("device"),
                        entry.get("device_class"),
                    )
                dtype_id = ensure_canonical_datatype(
                    graph,
                    "home_assistant",
                    length=length,
                    signed=signed,
                    textual=textual,
                    text_category=text_category,
                    scale=scale,
                    unit=entry.get("unit"),
                    raw={"value_type": value_type},
                )
                add_edge(
                    graph,
                    reg_id,
                    dtype_id,
                    type="REGISTER_HAS_DATATYPE",
                    source="home_assistant",
                    device=device,
                    group=group_name,
                )
                if entry.get("name"):
                    attrs = graph.nodes[reg_id].setdefault("attributes", set())
                    attrs.add(entry["name"])
                fams = graph.nodes[reg_id].setdefault("families", set())
                fams.add(device)

                device_node = f"device:home_assistant:{device}"
                ensure_node(
                    graph,
                    device_node,
                    type="device",
                    source="home_assistant",
                    name=device,
                )
                add_edge(graph, device_node, source_id, type="SOURCED_FROM")

                group_node = f"device_group:home_assistant:{group_name}"
                group_table = infer_table_from_group_name(group_name)
                ensure_node(
                    graph,
                    group_node,
                    type="device_group",
                    source="home_assistant",
                    name=group_name,
                    table=group_table,
                )
                add_edge(graph, group_node, source_id, type="SOURCED_FROM")

                group_devices = graph.nodes[group_node].setdefault("devices", set())
                group_devices.add(device)

                device_groups = graph.nodes[device_node].setdefault("groups", set())
                device_groups.add(group_name)

                add_edge(
                    graph,
                    device_node,
                    group_node,
                    type="DEVICE_USES_GROUP",
                    source="home_assistant",
                )
                add_edge(
                    graph,
                    group_node,
                    device_node,
                    type="GROUP_HAS_DEVICE",
                    source="home_assistant",
                )
                add_edge(
                    graph,
                    group_node,
                    reg_id,
                    type="GROUP_COVERS_REGISTER",
                    source="home_assistant",
                )
                add_edge(
                    graph,
                    reg_id,
                    device_node,
                    type="REGISTER_SUPPORTED_BY_DEVICE",
                    source="home_assistant",
                    group=group_name,
                )


def ingest_vendor_device_ranges(graph: nx.MultiDiGraph) -> None:
    if not VENDOR_DEVICE_RANGE_SPECS:
        return
    source_id = add_source_document(graph, "vendor_device_ranges", VENDOR_MANUAL_PDF_PATH)

    for spec in VENDOR_DEVICE_RANGE_SPECS:
        family_node = f"device_family:vendor:{spec['id']}"
        ensure_node(
            graph,
            family_node,
            type="device_family",
            source="vendor",
            name=spec.get("name"),
        )
        add_edge(graph, family_node, source_id, type="SOURCED_FROM")

        aliases = graph.nodes[family_node].setdefault("aliases", set())
        aliases.update(spec.get("aliases", []))

        family_ranges = graph.nodes[family_node].setdefault("ranges", {})

        for table, ranges in spec.get("ranges", {}).items():
            table_ranges = family_ranges.setdefault(table, [])
            for range_spec in ranges:
                start = range_spec["start"]
                end = range_spec["end"]
                note = range_spec.get("note")

                table_ranges.append({"start": start, "end": end, "note": note})

                range_id = ensure_register_range(
                    graph,
                    table,
                    start,
                    end,
                    note=note,
                    source="vendor_range",
                    metadata={
                        "family_id": spec["id"],
                        "family_name": spec.get("name"),
                        "note": note,
                    },
                )

                block_id = ensure_block(
                    graph,
                    table,
                    start,
                    end,
                    source="vendor_range",
                    data={
                        "family_id": spec["id"],
                        "family_name": spec.get("name"),
                        "note": note,
                    },
                )
                add_edge(
                    graph,
                    family_node,
                    block_id,
                    type="FAMILY_SUPPORTS_BLOCK",
                    table=table,
                    range_start=start,
                    range_end=end,
                    note=note,
                )
                add_edge(
                    graph,
                    family_node,
                    range_id,
                    type="FAMILY_SUPPORTS_RANGE",
                    table=table,
                    range_start=start,
                    range_end=end,
                    note=note,
                )
                add_edge(
                    graph,
                    range_id,
                    family_node,
                    type="RANGE_SUPPORTED_BY_FAMILY",
                    table=table,
                    range_start=start,
                    range_end=end,
                    note=note,
                )

                for register in range(start, end + 1):
                    reg_id = ensure_register(
                        graph,
                        register,
                        table,
                        source="vendor_range",
                    )
                    add_edge(
                        graph,
                        family_node,
                        reg_id,
                        type="FAMILY_SUPPORTS_REGISTER",
                        table=table,
                        range_start=start,
                        range_end=end,
                        note=note,
                    )

                    add_edge(graph, block_id, reg_id, type="BLOCK_CONTAINS")
                    add_edge(graph, reg_id, block_id, type="REGISTER_IN_BLOCK")
                    add_edge(graph, range_id, reg_id, type="RANGE_CONTAINS_REGISTER")
                    add_edge(graph, reg_id, range_id, type="REGISTER_IN_RANGE")

        for alias in spec.get("aliases", []):
            device_node = f"device:home_assistant:{alias}"
            if graph.has_node(device_node):
                graph.nodes[family_node].setdefault("devices", set()).add(alias)
                add_edge(
                    graph,
                    device_node,
                    family_node,
                    type="DEVICE_IN_VENDOR_FAMILY",
                    source="vendor_range",
                )
                add_edge(
                    graph,
                    family_node,
                    device_node,
                    type="VENDOR_FAMILY_HAS_DEVICE",
                    source="vendor_range",
                )
                graph.nodes[device_node].setdefault("vendor_families", set()).add(spec["id"])

def ingest_manual_datatypes(graph: nx.MultiDiGraph) -> None:
    try:
        import build_register_data_types as brdt
    except ImportError:
        return

    source_id = add_source_document(
        graph,
        "manual_register_types",
        DOC_DIR / "build_register_data_types.py",
    )

    mapping_raw = brdt.load_mapping()
    mapping = mapping_raw.get("devices", mapping_raw)
    types: Dict[str, Dict[str, Any]] = {}
    reg_map: Dict[Tuple[str, int], Dict[str, Any]] = {}

    for family, groups in mapping.items():
        for group_name, entries in groups.items():
            table = brdt.table_from_group(group_name)
            for entry in entries:
                length = entry.get("length", 1) or 1
                scale = entry.get("scale", 10)
                read_write = entry.get("read_write", False)
                value_type = entry.get("value_type", "int")
                register = entry["register"]
                register_end = register + length - 1
                tid = brdt.type_id(length, scale, read_write, value_type)

                brdt.ensure_type(types, tid, length, scale, read_write, value_type)

                info = reg_map.setdefault(
                    (table, register),
                    {
                        "table": table,
                        "register": register,
                        "register_end": register_end,
                        "type": tid,
                        "attributes": set(),
                        "families": set(),
                    },
                )

                if info["type"] != tid:
                    info.setdefault("type_conflicts", set()).add(tid)
                info["register_end"] = max(info["register_end"], register_end)
                if entry.get("name"):
                    info["attributes"].add(entry["name"])
                info["families"].add(family)

    register_types = []
    for (_, _), info in sorted(reg_map.items(), key=lambda item: (item[0][0], item[0][1])):
        entry = {
            "table": info["table"],
            "register": info["register"],
            "register_end": info["register_end"],
            "type": info["type"],
            "attributes": sorted(info["attributes"]),
            "families": sorted(info["families"]),
        }
        if conflicts := info.get("type_conflicts"):
            entry["type_conflicts"] = sorted(conflicts)
        register_types.append(entry)

    for name, definition in brdt.MANUAL_TYPES.items():
        types[name] = definition

    register_types = brdt.merge_manual_registers(register_types, brdt.MANUAL_REGISTER_TYPES)

    def canonical_from_definition(name: str, definition: Dict[str, Any]) -> str:
        kind = definition.get("kind")
        registers = definition.get("registers")
        length_bytes = registers * 2 if isinstance(registers, int) else None
        signed: Optional[bool] = None
        textual = False
        divide = None
        scale = definition.get("scale")
        multiplier = None
        unit = definition.get("unit")
        text_category: Optional[str] = None
        if kind == "scaled_signed":
            signed = True
        elif kind in ("scaled", "scaled_signed"):
            signed = False if signed is None else signed
        elif kind == "bitfield":
            signed = False
        elif kind == "enum":
            signed = False
        elif kind == "ascii":
            textual = True
            if definition.get("characters") is not None:
                length_bytes = definition.get("characters")
            text_category = classify_textual_payload(name, definition.get("label"))
        elif kind == "raw":
            signed = None

        dtype_id = ensure_canonical_datatype(
            graph,
            "manual",
            length=length_bytes,
            signed=signed,
            textual=textual,
            text_category=text_category,
            divide=divide,
            scale=scale,
            multiplier=multiplier,
            unit=unit,
            raw={"kind": kind, "name": name},
        )

        if kind == "enum":
            for value, meta in (definition.get("values") or {}).items():
                enum_id = f"enum_value:manual:{name}:{value}"
                ensure_node(
                    graph,
                    enum_id,
                    type="enum_value",
                    value=value,
                    label=meta.get("label"),
                    description=meta.get("description"),
                )
                add_edge(graph, dtype_id, enum_id, type="DATATYPE_HAS_ENUM_VALUE")

        if kind == "bitfield":
            for flag in definition.get("flags", []):
                bit = flag.get("bit")
                flag_id = f"bitflag:manual:{name}:{bit}"
                ensure_node(
                    graph,
                    flag_id,
                    type="bitflag",
                    bit=bit,
                    label=flag.get("name"),
                    description=flag.get("description"),
                )
                add_edge(graph, dtype_id, flag_id, type="DATATYPE_HAS_BITFLAG")

        return dtype_id

    dtype_cache: Dict[str, str] = {}

    for entry in register_types:
        table = entry["table"]
        start = entry["register"]
        end = entry["register_end"]
        type_name = entry["type"]
        dtype_def = types.get(type_name, {})
        dtype_id = dtype_cache.get(type_name)
        if dtype_id is None:
            dtype_id = canonical_from_definition(type_name, dtype_def)
            dtype_cache[type_name] = dtype_id

        block_id = ensure_block(graph, table, start, end, source="manual", data=entry)
        add_edge(graph, block_id, source_id, type="SOURCED_FROM")

        for register in range(start, end + 1):
            reg_id = ensure_register(
                graph,
                register,
                table,
                source="manual",
                data={"type": type_name},
            )
            add_edge(graph, reg_id, source_id, type="SOURCED_FROM")
            add_edge(graph, reg_id, dtype_id, type="REGISTER_HAS_DATATYPE", source="manual")
            if entry.get("attributes"):
                attrs = graph.nodes[reg_id].setdefault("attributes", set())
                attrs.update(entry["attributes"])
            if entry.get("families"):
                fams = graph.nodes[reg_id].setdefault("families", set())
                fams.update(entry["families"])
            if entry.get("description"):
                notes = graph.nodes[reg_id].setdefault("manual_descriptions", [])
                notes.append(entry["description"])

            kind = dtype_def.get("kind")
            if kind == "bitfield":
                for flag in dtype_def.get("flags", []):
                    bit = flag.get("bit")
                    flag_id = f"bitflag:manual:{type_name}:{bit}"
                    add_edge(graph, reg_id, flag_id, type="REGISTER_HAS_BITFLAG")



def ingest_openinverter(graph: nx.MultiDiGraph) -> None:
    data = load_json(OPENINVERTER_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "openinverter_gateway", OPENINVERTER_PATH)
    devices = data.get("devices", {})
    for device, info in devices.items():
        device_node = f"openinverter_device:{device}"
        ensure_node(
            graph,
            device_node,
            type="openinverter_device",
            name=device,
            file=info.get("file"),
        )
        add_edge(graph, device_node, source_id, type="SOURCED_FROM")
        # Current export does not include explicit register mappings; retain metadata only for now.
        mqtt_keys = info.get("mqtt_keys") or []
        if mqtt_keys:
            graph.nodes[device_node]["mqtt_keys"] = mqtt_keys


def ingest_inverter_to_mqtt(graph: nx.MultiDiGraph) -> None:
    data = load_json(INVERTER_TO_MQTT_PATH)
    if not data:
        return
    source_id = add_source_document(graph, "inverter_to_mqtt", INVERTER_TO_MQTT_PATH)
    code = data.get("code", {})
    for file_path, info in code.items():
        reads = info.get("reads", [])
        for idx, read in enumerate(reads):
            read_type = read.get("type") or "input"
            table = "input" if read_type == "input" else "holding"
            block_start = read.get("block_start_register") or read.get("start_register")
            block_length = read.get("block_length") or read.get("length")
            block_end = None
            if block_start is not None and block_length is not None:
                block_end = block_start + block_length - 1

            op_node = f"inverter_to_mqtt:read:{file_path}:{idx}"
            ensure_node(
                graph,
                op_node,
                type="inverter_to_mqtt_read",
                file=file_path,
                function=read.get("function"),
            )
            add_edge(graph, op_node, source_id, type="SOURCED_FROM")

            section_id: Optional[str] = None
            if block_start is not None and block_end is not None and block_end >= block_start:
                section_slug = slugify(f"{Path(file_path).stem}-{idx}")
                section_id = section_node_id(table, block_start, block_end, section_slug)
                ensure_section(
                    graph,
                    section_id,
                    table=table,
                    start=block_start,
                    end=block_end,
                    label=f"{Path(file_path).name}:{idx}",
                    kind="inverter_to_mqtt_block",
                    metadata={
                        "inverter_to_mqtt": {
                            "file": file_path,
                            "function": read.get("function"),
                            "block_start_register": block_start,
                            "block_length": block_length,
                        }
                    },
                )

                parent_range_id = find_enclosing_range(graph, table, block_start, block_end)
                if parent_range_id:
                    add_section_range_link(graph, section_id, parent_range_id)
                else:
                    range_id = ensure_register_range(graph, table, block_start, block_end)
                    add_section_range_link(graph, section_id, range_id)

                add_edge(graph, op_node, section_id, type="MQTT_OPERATION_COVERS_SECTION")
                add_edge(graph, section_id, op_node, type="SECTION_HAS_OPERATION")

            for entry in read.get("entries", []):
                registers = entry.get("registers") or []
                try:
                    register_numbers = [int(r) for r in registers]
                except (TypeError, ValueError):
                    continue
                if not register_numbers:
                    continue
                entry_length = len(register_numbers)
                dtype_id = ensure_canonical_datatype(
                    graph,
                    "inverter_to_mqtt",
                    length=entry_length,
                    signed=None,
                    textual=False,
                    raw={"variable": entry.get("variable")},
                )
                for register in register_numbers:
                    reg_id = ensure_register(
                        graph,
                        register,
                        table,
                        source="inverter_to_mqtt",
                        data={"file": file_path, **entry},
                    )
                    add_edge(
                        graph,
                        op_node,
                        reg_id,
                        type="MQTT_OPERATION_MAPS_REGISTER",
                        variable=entry.get("variable"),
                        expression=entry.get("expression"),
                        buffer_indexes=entry.get("buffer_indexes"),
                        section=section_id,
                        registers=register_numbers,
                        register_count=entry_length,
                    )
                    if section_id:
                        offset = None
                        if block_start is not None:
                            offset = register - block_start
                        add_edge(
                            graph,
                            section_id,
                            reg_id,
                            type="SECTION_CONTAINS_REGISTER",
                            offset=offset,
                        )
                        add_edge(
                            graph,
                            reg_id,
                            section_id,
                            type="REGISTER_PART_OF_SECTION",
                            offset=offset,
                        )
                    add_edge(graph, reg_id, dtype_id, type="REGISTER_HAS_DATATYPE", source="inverter_to_mqtt")
                    add_edge(graph, reg_id, source_id, type="SOURCED_FROM")

        writes = info.get("writes", [])
        for idx, write in enumerate(writes):
            address = write.get("address")
            if address is None:
                continue
            reg_id = ensure_register(
                graph,
                address,
                "holding",
                source="inverter_to_mqtt",
                data={"file": file_path, **write},
            )
            op_node = f"inverter_to_mqtt:write:{file_path}:{idx}"
            ensure_node(
                graph,
                op_node,
                type="inverter_to_mqtt_write",
                file=file_path,
                call=write.get("call"),
            )
            add_edge(graph, op_node, source_id, type="SOURCED_FROM")
            add_edge(graph, op_node, reg_id, type="MQTT_OPERATION_WRITES_REGISTER")
            add_edge(graph, reg_id, source_id, type="SOURCED_FROM")


def synthesise_canonical_datatypes(graph: nx.MultiDiGraph) -> None:
    for node_id, attrs in list(graph.nodes(data=True)):
        if attrs.get("type") != "register":
            continue

        dtype_edges = [
            (target, edge_data)
            for _, target, edge_data in graph.out_edges(node_id, data=True)
            if edge_data.get("type") == "REGISTER_HAS_DATATYPE"
        ]
        if not dtype_edges:
            continue

        value_sets: Dict[str, set] = {}
        conflicts: Dict[str, set] = {}
        aggregated_attrs: Dict[str, Any] = {}
        source_names: set[str] = set()
        source_datatypes: set[str] = set()
        enum_values: Dict[Any, Dict[str, Any]] = {}
        bitflags: Dict[int, Dict[str, Any]] = {}
        annotations: List[Dict[str, Any]] = []

        for dtype_id, edge_data in dtype_edges:
            dtype_attrs = graph.nodes.get(dtype_id, {})
            source = edge_data.get("source") or dtype_attrs.get("namespace")
            if source:
                source_names.add(str(source))
            source_datatypes.add(dtype_id)

            for field in CANONICAL_FIELDS:
                merge_value(value_sets, field, dtype_attrs.get(field))

            enum_meta, bitflag_meta = collect_enum_metadata(graph, dtype_id)
            for value, data in enum_meta.items():
                target_entry = enum_values.setdefault(value, {})
                if data.get("label"):
                    target_entry.setdefault("label", data["label"])
                if data.get("description"):
                    target_entry.setdefault("description", data["description"])
                if data.get("sources"):
                    sources = target_entry.setdefault("sources", set())
                    sources.update(data["sources"])
            for bit, data in bitflag_meta.items():
                target_entry = bitflags.setdefault(bit, {})
                if data.get("label"):
                    target_entry.setdefault("label", data["label"])
                if data.get("description"):
                    target_entry.setdefault("description", data["description"])
                if data.get("sources"):
                    sources = target_entry.setdefault("sources", set())
                    sources.update(data["sources"])

            dtype_annotations = dtype_attrs.get("annotations")
            if isinstance(dtype_annotations, list):
                for note in dtype_annotations:
                    if note and note not in annotations:
                        annotations.append(note)

        for field, values in value_sets.items():
            if not values:
                continue
            if len(values) == 1:
                aggregated_attrs[field] = next(iter(values))
            else:
                conflicts[field] = values
                aggregated_attrs[field] = None

        if aggregated_attrs.get("textual"):
            aggregated_attrs["signed"] = None
        else:
            aggregated_attrs["text_category"] = None

        signature = make_canonical_signature(aggregated_attrs, conflicts)
        canonical_id = data_type_node_id("canonical", signature)

        canon_attrs = {
            "type": "data_type",
            "namespace": "canonical",
            **{field: aggregated_attrs.get(field) for field in CANONICAL_FIELDS},
        }
        if conflicts:
            canon_attrs["conflicts"] = {
                field: sorted(str(v) for v in values)
                for field, values in conflicts.items()
            }
        if source_names:
            canon_attrs["sources"] = sorted(source_names)
        if enum_values:
            canon_attrs["enum_values"] = serialise_enum_payload(enum_values)
        if bitflags:
            canon_attrs["bitflags"] = serialise_bitflag_payload(bitflags)
        canon_attrs["source_datatypes"] = sorted(source_datatypes)
        if annotations:
            canon_attrs["annotations"] = annotations

        ensure_node(graph, canonical_id, **canon_attrs)

        add_edge(
            graph,
            node_id,
            canonical_id,
            type="REGISTER_HAS_CANONICAL_DATATYPE",
        )

        for dtype_id, edge_data in dtype_edges:
            existing_edges = graph.get_edge_data(canonical_id, dtype_id)
            if existing_edges is None or all(
                data.get("type") != "CANONICAL_FROM_DATATYPE" for data in existing_edges.values()
            ):
                add_edge(
                    graph,
                    canonical_id,
                    dtype_id,
                    type="CANONICAL_FROM_DATATYPE",
                    source=edge_data.get("source"),
                )


def link_mirrored_blocks(graph: nx.MultiDiGraph) -> None:
    blocks_by_table: Dict[str, list[tuple[str, Dict[str, Any]]]] = defaultdict(list)
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") == "register_block":
            table = attrs.get("table") or "unknown"
            blocks_by_table[table].append((node_id, attrs))

    input_blocks = blocks_by_table.get("input", [])
    index_by_range = {
        (attrs.get("start_register"), attrs.get("end_register")): node_id
        for node_id, attrs in input_blocks
    }

    for node_id, attrs in input_blocks:
        start = attrs.get("start_register")
        end = attrs.get("end_register")
        if start is None or end is None:
            continue
        if start >= 3000:
            offset_start = start - 3000
            offset_end = end - 3000
            base_node = index_by_range.get((offset_start, offset_end))
            if base_node:
                add_edge(
                    graph,
                    node_id,
                    base_node,
                    type="BLOCK_MIRRORS_BLOCK",
                    offset=-3000,
                )
                add_edge(
                    graph,
                    base_node,
                    node_id,
                    type="BLOCK_MIRRORS_BLOCK",
                    offset=3000,
                )


def link_block_device_groups(graph: nx.MultiDiGraph) -> None:
    for block_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "register_block":
            continue
        registers: set[str] = set()
        for _, reg_id, edge_data in graph.out_edges(block_id, data=True):
            if edge_data.get("type") not in {"BLOCK_CONTAINS", "REGISTER_IN_BLOCK"}:
                continue
            registers.add(reg_id)

        covered_groups: set[str] = set()
        covered_devices: set[str] = set()
        for reg_id in registers:
            for group_node, _, edge_data in graph.in_edges(reg_id, data=True):
                if edge_data.get("type") == "GROUP_COVERS_REGISTER":
                    covered_groups.add(group_node)
            for _, device_node, edge_data in graph.out_edges(reg_id, data=True):
                if edge_data.get("type") == "REGISTER_SUPPORTED_BY_DEVICE":
                    covered_devices.add(device_node)

        for group_node in covered_groups:
            add_edge(
                graph,
                block_id,
                group_node,
                type="BLOCK_COVERED_BY_GROUP",
            )
        for device_node in covered_devices:
            add_edge(
                graph,
                block_id,
                device_node,
                type="BLOCK_SUPPORTED_BY_DEVICE",
            )


def build_repeated_sections(graph: nx.MultiDiGraph) -> None:
    if not REPEATED_SECTION_SPECS:
        return

    for spec in REPEATED_SECTION_SPECS:
        table: str = spec["table"]
        template_start, template_end = spec["template_range"]
        slot_size: int = spec["slot_size"]
        slot_count: int = spec.get("slot_count", 0)
        instance_start: int = spec.get("instance_start", template_start)
        label: Optional[str] = spec.get("label")
        slot_label_template: str = spec.get("slot_label", "Slot {index}")

        if slot_count <= 0:
            continue

        template_range_id = ensure_register_range(
            graph,
            table,
            template_start,
            template_end,
        )

        parent_range_id: Optional[str] = None
        parent_candidates: list[tuple[str, Dict[str, Any]]] = [
            (range_node, range_attrs)
            for range_node, range_attrs in graph.nodes(data=True)
            if range_attrs.get("type") == "register_range"
            and range_attrs.get("table") == table
            and range_attrs.get("start_register") is not None
            and range_attrs.get("end_register") is not None
            and range_attrs["start_register"] <= template_start
            and range_attrs["end_register"] >= template_end
            and (range_attrs["end_register"] - range_attrs["start_register"]) >= (template_end - template_start)
            and range_node != template_range_id
        ]
        parent_candidates.sort(
            key=lambda item: (
                item[1]["end_register"] - item[1]["start_register"],
                item[1]["start_register"],
            )
        )
        if parent_candidates:
            parent_range_id, _ = parent_candidates[0]
            for family_id, _, edge_data in graph.in_edges(parent_range_id, data=True):
                if edge_data.get("type") != "FAMILY_SUPPORTS_RANGE":
                    continue
                add_edge(
                    graph,
                    family_id,
                    template_range_id,
                    type="FAMILY_SUPPORTS_RANGE",
                    note=edge_data.get("note"),
                )

        template_section_id = section_node_id(
            table,
            template_start,
            template_end,
            spec["id"],
        )
        ensure_section(
            graph,
            template_section_id,
            table=table,
            start=template_start,
            end=template_end,
            label=label,
            kind="template",
            metadata={"spec_id": spec["id"]},
        )
        graph.nodes[template_section_id]["slot_size"] = slot_size
        graph.nodes[template_section_id]["slot_count"] = slot_count
        add_section_range_link(graph, template_section_id, template_range_id)
        if parent_range_id:
            add_section_range_link(graph, template_section_id, parent_range_id)

        template_register_ids: list[str] = []
        for register in range(template_start, template_end + 1):
            reg_id = register_node_id(table, register)
            if graph.has_node(reg_id):
                template_register_ids.append(reg_id)

        for index in range(1, slot_count + 1):
            slot_start = instance_start + (index - 1) * slot_size
            slot_end = slot_start + (template_end - template_start)
            slot_label = slot_label_template.format(index=index)
            slot_section_slug = f"{spec['id']}_slot_{index}"
            slot_section_id = section_node_id(
                table,
                template_start,
                template_end,
                slot_section_slug,
            )
            ensure_section(
                graph,
                slot_section_id,
                table=table,
                start=template_start,
                end=template_end,
                label=slot_label,
                index=index,
                kind="instance",
            )
            node_attrs = graph.nodes[slot_section_id]
            node_attrs["instance_start_register"] = slot_start
            node_attrs["instance_end_register"] = slot_end
            node_attrs["register_offset"] = slot_start - template_start
            node_attrs["slot_size"] = slot_size

            add_section_child(graph, template_section_id, slot_section_id, index=index)
            add_section_range_link(graph, slot_section_id, template_range_id)

            actual_range_id = ensure_register_range(graph, table, slot_start, slot_end)
            add_section_range_link(graph, slot_section_id, actual_range_id)

            for family_id, _, edge_data in graph.in_edges(template_range_id, data=True):
                if edge_data.get("type") != "FAMILY_SUPPORTS_RANGE":
                    continue
                add_edge(
                    graph,
                    family_id,
                    actual_range_id,
                    type="FAMILY_SUPPORTS_RANGE",
                    note=edge_data.get("note"),
                )

            add_edge(
                graph,
                slot_section_id,
                template_section_id,
                type="SECTION_MIRRORS_SECTION",
                offset=slot_start - template_start,
                slot_index=index,
            )

            for reg_id in template_register_ids:
                template_register = graph.nodes[reg_id].get("register")
                if template_register is None:
                    continue
                offset = template_register - template_start
                instance_register_addr = slot_start + offset
                add_edge(
                    graph,
                    slot_section_id,
                    reg_id,
                    type="SECTION_MAPS_CANONICAL_REGISTER",
                    offset=offset,
                    instance_register=instance_register_addr,
                    slot_index=index,
                )

                canonical_roles = graph.nodes[reg_id].setdefault(
                    "canonical_roles", set()
                )
                canonical_roles.add(spec["id"])

                instance_reg_id = register_node_id(table, instance_register_addr)
                if graph.has_node(instance_reg_id):
                    add_edge(
                        graph,
                        slot_section_id,
                        instance_reg_id,
                        type="SECTION_CONTAINS_REGISTER",
                        offset=offset,
                        canonical_register=reg_id,
                        slot_index=index,
                    )
                    add_edge(
                        graph,
                        instance_reg_id,
                        slot_section_id,
                        type="REGISTER_PART_OF_SECTION",
                        offset=offset,
                        slot_index=index,
                    )
                    add_edge(
                        graph,
                        instance_reg_id,
                        reg_id,
                        type="REGISTER_MIRRORS_CANONICAL_REGISTER",
                        offset=offset,
                        slot_index=index,
                    )
                    add_edge(
                        graph,
                        reg_id,
                        instance_reg_id,
                        type="CANONICAL_REGISTER_HAS_INSTANCE",
                        offset=offset,
                        slot_index=index,
                    )

                    mirrored = graph.nodes[instance_reg_id].setdefault(
                        "mirrors_canonical", set()
                    )
                    mirrored.add(reg_id)

def build_graph() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    graph.graph["generated_at"] = datetime.now(timezone.utc).isoformat()
    graph.graph["generator"] = "build_register_graph.py"

    ingest_vendor_tables(graph)
    ingest_curated_spec(graph)
    ingest_grott_layouts(graph)
    ingest_ha_registers(graph)
    ingest_vendor_device_ranges(graph)
    ingest_openinverter(graph)
    ingest_inverter_to_mqtt(graph)
    ingest_manual_datatypes(graph)
    synthesise_canonical_datatypes(graph)
    link_mirrored_blocks(graph)
    link_block_device_groups(graph)
    build_repeated_sections(graph)
    # Additional sources (openinverter, inverter_to_mqtt) can be ingested in future iterations.

    for _, attrs in graph.nodes(data=True):
        if "sources" in attrs and isinstance(attrs["sources"], set):
            attrs["sources"] = sorted(attrs["sources"])
        if "payloads" in attrs and isinstance(attrs["payloads"], defaultdict):
            attrs["payloads"] = {k: list(v) for k, v in attrs["payloads"].items()}
        if "metadata" in attrs and isinstance(attrs["metadata"], defaultdict):
            attrs["metadata"] = {k: list(v) for k, v in attrs["metadata"].items()}
        if "attributes" in attrs and isinstance(attrs["attributes"], set):
            attrs["attributes"] = sorted(attrs["attributes"])
        if "families" in attrs and isinstance(attrs["families"], set):
            attrs["families"] = sorted(attrs["families"])
        if "devices" in attrs and isinstance(attrs["devices"], set):
            attrs["devices"] = sorted(attrs["devices"])
        if "groups" in attrs and isinstance(attrs["groups"], set):
            attrs["groups"] = sorted(attrs["groups"])
        if "aliases" in attrs and isinstance(attrs["aliases"], set):
            attrs["aliases"] = sorted(attrs["aliases"])
        if "vendor_families" in attrs and isinstance(attrs["vendor_families"], set):
            attrs["vendor_families"] = sorted(attrs["vendor_families"])
        if "vendor_family_ranges" in attrs and isinstance(attrs["vendor_family_ranges"], set):
            attrs["vendor_family_ranges"] = sorted(
                [
                    {
                        "family_id": family_id,
                        "table": table,
                        "start": start,
                        "end": end,
                        "note": note or None,
                    }
                    for (family_id, table, start, end, note) in attrs["vendor_family_ranges"]
                ],
                key=lambda item: (item["family_id"], item["table"], item["start"], item["end"]),
            )
        if "notes" in attrs and isinstance(attrs["notes"], set):
            attrs["notes"] = sorted(attrs["notes"])
        if "ranges" in attrs and isinstance(attrs["ranges"], dict):
            deduped: Dict[str, List[Dict[str, Any]]] = {}
            for table, items in attrs["ranges"].items():
                seen: set[tuple] = set()
                table_items: List[Dict[str, Any]] = []
                for entry in items:
                    start = entry.get("start")
                    end = entry.get("end")
                    note = entry.get("note")
                    key = (start, end, note)
                    if key in seen:
                        continue
                    seen.add(key)
                    table_items.append(
                        {
                            "start": start,
                            "end": end,
                            "note": note,
                        }
                    )
                table_items.sort(key=lambda item: (item["start"], item["end"]))
                deduped[table] = table_items
            attrs["ranges"] = deduped
        if "canonical_roles" in attrs and isinstance(attrs["canonical_roles"], set):
            attrs["canonical_roles"] = sorted(attrs["canonical_roles"])
        if "mirrors_canonical" in attrs and isinstance(attrs["mirrors_canonical"], set):
            attrs["mirrors_canonical"] = sorted(attrs["mirrors_canonical"])
    return graph


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Growatt register knowledge graph")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the NetworkX graph pickle (default: %(default)s)",
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Suppress the textual summary of nodes/edges",
    )
    return parser.parse_args()


def print_summary(graph: nx.MultiDiGraph) -> None:
    counts = defaultdict(int)
    for _, attrs in graph.nodes(data=True):
        node_type = attrs.get("type", "unknown")
        counts[node_type] += 1
    print("Graph summary:")
    print(f"  Nodes: {graph.number_of_nodes()}  Edges: {graph.number_of_edges()}")
    for node_type, count in sorted(counts.items()):
        print(f"  - {node_type}: {count}")


def main() -> None:
    args = parse_args()
    graph = build_graph()
    output_path = args.output if args.output.is_absolute() else (DOC_DIR / args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if not args.no_summary:
        print_summary(graph)
        rel_path = output_path.relative_to(PROJECT_ROOT)
        print(f"Graph written to {rel_path}")


if __name__ == "__main__":
    main()
