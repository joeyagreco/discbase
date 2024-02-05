from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from discord import Message


@dataclass(kw_only=True, eq=False) 
class StoredRecord:
    record_id: int
    text_data: str
    media_urls: list[str]
    created_at_utc: datetime
    # https://discordpy.readthedocs.io/en/stable/api.html#discord.Message
    discord_message: Message

    @staticmethod
    def from_discord_message(discord_message: Message) -> StoredRecord:
        media_urls = []
        for attachment in discord_message.attachments:
            media_urls.append(attachment.url)
        return StoredRecord(
            record_id=discord_message.id,
            text_data=discord_message.content,
            media_urls=media_urls,
            created_at_utc=discord_message.created_at,
            discord_message=discord_message,
        )
