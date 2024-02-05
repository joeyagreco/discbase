from __future__ import annotations

from enum import Enum


class URLType(Enum):
    LOCAL = "LOCAL"
    ONLINE = "ONLINE"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def items(cls) -> list[tuple[URLType, str]]:
        return [(member.value, name) for name, member in cls.__members__.items()]

    @classmethod
    def from_str(cls, s: str) -> URLType:
        s_upper = s.upper()
        for member in cls:
            if member.name == s_upper:
                return member
        raise ValueError(f"'{s}' is not a valid URLType.")
