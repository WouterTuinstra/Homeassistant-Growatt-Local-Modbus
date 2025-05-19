from homeassistant.components.number import NumberEntityDescription
from dataclasses import dataclass

@dataclass
class GrowattNumberEntityDescription(NumberEntityDescription):
    key: str
    name: str
    register: int
    scale: float
    writeable: bool
