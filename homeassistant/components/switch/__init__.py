"""Stub switch component APIs for documentation generation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SwitchEntityDescription:
    """Minimal data container mirroring Home Assistant's switch description."""

    key: str
    name: str | None = None
    icon: str | None = None
    entity_registry_enabled_default: bool = True
    entity_category: str | None = None
    device_class: str | None = None
    translation_key: str | None = None
    value_fn: Any | None = None
    has_entity_name: bool | None = None
