from __future__ import annotations

from dataclasses import dataclass

from discord import Message


@dataclass(kw_only=True, eq=False)
class StoredRecord:
    record_id: int
    discord_message: Message

    @staticmethod
    def from_discord_message(discord_message: Message) -> StoredRecord:
        return StoredRecord(record_id=discord_message.id, discord_message=discord_message)
