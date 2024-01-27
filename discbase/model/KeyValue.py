from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from discbase.model.abstract.Dictizable import Dictizable


@dataclass(kw_only=True, eq=False)
class KeyValue(Dictizable):
    key: str
    value: any
    value_type: Optional[type] = None  # DEFAULTS TO FALSE

    @staticmethod
    def from_dict(d: dict) -> KeyValue:
        return KeyValue(key=d["key"], value=d["value"], value_type=d.get("value_type"))

    def to_dict(self) -> dict:
        return {"key": self.key, "value": self.value, "value_type": self.value_type}
