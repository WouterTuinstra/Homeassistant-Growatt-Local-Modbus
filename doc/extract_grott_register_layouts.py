#!/usr/bin/env python3
"""Write grott_register_layouts.json from Grott's recorddict and MQTT settings."""

from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple
import re

DOC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOC_DIR.parent
EXTERNAL_ROOT = PROJECT_ROOT.parent
GROTT_ROOT = EXTERNAL_ROOT / "grott"
OUTPUT_PATH = DOC_DIR / "grott_register_layouts.json"

def _detect_grott_version() -> Optional[str]:
    candidate = GROTT_ROOT / "grott.py"
    if not candidate.exists():
        return None
    match = re.search(r'verrel\s*=\s*"([^"]+)"', candidate.read_text(encoding="utf-8"))
    if match:
        return match.group(1)
    return None


@contextmanager
def _temporary_working_directory(path: Path) -> Iterable[None]:
    original_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)


def _load_grott_conf() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    if not GROTT_ROOT.exists():
        raise FileNotFoundError(f"Expected Grott checkout at {GROTT_ROOT}")

    sys_path_was = list(sys.path)
    sys.path.insert(0, str(GROTT_ROOT))
    argv_was = list(sys.argv)

    verrel = _detect_grott_version() or "export"

    with _temporary_working_directory(GROTT_ROOT):
        try:
            from grottconf import Conf  # type: ignore
        except ImportError as exc:  # pragma: no cover - developer misconfiguration
            raise ImportError(
                "Unable to import grottconf from external/grott; ensure the submodule is present"
            ) from exc

        try:
            sys.argv = [argv_was[0]]
            conf = Conf(verrel)
        finally:
            sys.argv = argv_was

    # restore sys.path (Conf imports rely on grott root, keep module cached)
    sys.path = sys_path_was

    metadata = {
        "mqtt_topic": conf.mqtttopic,
        "mqtt_inverter_in_topic": bool(conf.mqttinverterintopic),
        "mqtt_meter_topic_enabled": bool(conf.mqttmtopic),
        "mqtt_meter_topic": conf.mqttmtopicname,
        "grott_version": getattr(conf, "verrel", None),
    }

    return conf.recorddict, metadata


def _normalise_layouts(recorddict: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    export_layouts: Dict[str, Any] = {}

    for layout_id in sorted(recorddict):
        layout_entries = recorddict[layout_id]
        meta_buckets: Dict[str, Any] = {}
        fields = []

        for key, data in sorted(layout_entries.items()):
            if not isinstance(data, dict):
                continue

            # treat keys without length as layout-level metadata
            length = data.get("length")
            if length is None:
                meta_buckets[key] = {k: v for k, v in data.items() if k != "length"}
                continue

            value = data.get("value")
            if value is None:
                meta_buckets[key] = data
                continue

            divide = data.get("divide")
            entry: Dict[str, Any] = {
                "field": key,
                "byte_offset": value,
                "length_bytes": length,
                "type": data.get("type", "num"),
            }
            if divide is not None:
                entry["divide"] = divide
            if "incl" in data:
                entry["include_by_default"] = data["incl"] != "no"
            if "pos" in data:
                entry["log_position"] = data["pos"]
            if "unit" in data:
                entry["unit"] = data["unit"]

            register = data.get("register")
            if register is not None:
                registers_consumed = max(1, (int(length) + 1) // 2)
                entry["register_start"] = register
                entry["register_end"] = register + registers_consumed - 1
                entry["register_count"] = registers_consumed

            # copy any additional attributes that may be useful for downstream tools
            extra = {
                k: v
                for k, v in data.items()
                if k
                not in {
                    "value",
                    "length",
                    "type",
                    "divide",
                    "incl",
                    "pos",
                    "unit",
                    "register",
                }
            }
            if extra:
                entry["extra"] = extra

            fields.append(entry)

        export_layouts[layout_id] = {
            "metadata": meta_buckets or None,
            "fields": fields,
        }

    return export_layouts


def main() -> None:
    recorddict, mqtt_meta = _load_grott_conf()
    layouts = _normalise_layouts(recorddict)

    mqtt_topic = mqtt_meta["mqtt_topic"]
    if mqtt_meta["mqtt_inverter_in_topic"] and mqtt_topic:
        mqtt_topic_template = f"{mqtt_topic}/{{device_id}}"
    else:
        mqtt_topic_template = mqtt_topic or None

    export = {
        "source": "grott",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "grott_version": mqtt_meta.get("grott_version"),
        "mqtt_topic_template": mqtt_topic_template,
        "mqtt_meter_topic": mqtt_meta["mqtt_meter_topic"] if mqtt_meta["mqtt_meter_topic_enabled"] else None,
        "layouts": layouts,
    }

    OUTPUT_PATH.write_text(json.dumps(export, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
