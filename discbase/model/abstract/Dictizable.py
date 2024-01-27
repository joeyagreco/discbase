from __future__ import annotations

from .DictDeserializable import DictDeserializable
from .DictSerializable import DictSerializable


class Dictizable(DictSerializable, DictDeserializable):
    ...
