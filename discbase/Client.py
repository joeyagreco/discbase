from __future__ import annotations

import asyncio
import os
import tempfile
from functools import wraps
from typing import Optional

import discord
from discord import Client as DiscordClient
from discord import File, Intents
from discord.abc import GuildChannel

from discbase.enumeration.URLType import URLType
from discbase.model.StoredRecord import StoredRecord
from discbase.util.CustomLogger import CustomLogger
from discbase.util.error import log_and_raise
from discbase.util.general import get_file_extension, get_random_string, get_url_type
from discbase.util.image import save_image_from_url


class Client:
    def __init__(
        self,
        *,
        discord_client_token: str,
        discord_channel_id: int,
        connection_timeout_seconds: int = 5,
    ):
        self.__logger = CustomLogger.get_logger()
        self.__discord_client_token = discord_client_token
        self.__discord_channel_id = discord_channel_id
        self.__connection_timeout_seconds = connection_timeout_seconds
        self.__discord_client = DiscordClient(intents=Intents.all())
        self.__discord_channel: Optional[GuildChannel] = None
        self.__client_tasks = []
        self.__ready = False

    async def __aenter__(self) -> Client:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> Client:
        await self.stop()

    def discord_message_to_stored_record(func: callable) -> callable:
        """
        Wraps a function that returns a Discord Message.
        Turns the response from a Discord Message to a StoredRecord.
        """

        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> any:
            discord_message_response = await func(self, *args, **kwargs)
            return StoredRecord.from_discord_message(discord_message_response)

        return wrapper

    def alive(self) -> bool:
        """
        Checks if this client is alive and running.
        """
        return self.__ready

    async def start(self):
        """
        Starts the client.
        """
        self.__logger.info("STARTING DISCORD CLIENT")

        @self.__discord_client.event
        async def on_ready():
            self.__logger.important(f"DISCBASE IS RUNNING WITH USER {self.__discord_client.user}")
            self.__discord_channel = self.__discord_client.get_channel(self.__discord_channel_id)
            if self.__discord_channel == None:
                log_and_raise(
                    self.__logger, f"COULD NOT RETRIEVE CHANNEL WITH ID {self.__discord_channel_id}"
                )
            self.__ready = True

        client_run_task = asyncio.create_task(
            self.__discord_client.start(self.__discord_client_token)
        )
        self.__client_tasks.append(client_run_task)

        await asyncio.sleep(0)  # Allow the event loop to start the client

        wait_to_connect_task = asyncio.create_task(self.__discord_client.wait_until_ready())
        self.__client_tasks.append(wait_to_connect_task)
        # wait for a connection to discord with a timeout
        done, _ = await asyncio.wait(
            {wait_to_connect_task}, timeout=self.__connection_timeout_seconds
        )
        if done:
            return

        error = client_run_task.exception()

        if isinstance(error, discord.errors.LoginFailure):
            self.__logger.error("unable to login to discord")
        await self.stop()
        raise error

    async def stop(self):
        """
        Stops the client.
        THE CLIENT MUST BE STOPPED IF STARTED BEFORE TERMINATION.
        """
        self.__logger.info("JG STOP CLALED")
        self.__logger.info("STOPPING DISCORD CLIENT")
        for task in self.__client_tasks:
            task_name = getattr(task.get_coro(), "__name__", "Unknown Task")
            self.__logger.info(f"CANCELING TASK: {task_name}")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError as e:
                self.__logger.debug(e)
        await self.__discord_client.close()
        self.__ready = False
        self.__client_tasks = []

    @discord_message_to_stored_record
    # @wait_for_ready
    async def dump(
        self, *, value: Optional[str] = None, media_paths: Optional[list[str]] = None
    ) -> StoredRecord:
        """
        Dumps into the Discord database.
        Returns a StoredRecord that represents the data that will be returned on retrieval of this data.
        """
        # validate that we got something
        if all(value is None for value in (value, media_paths)):
            raise Exception("Did not receive anything to dump.")

        # default to empty string for value
        value: str = "" if value is None else value
        files: list[File] = []
        media_paths = media_paths or []

        with tempfile.TemporaryDirectory() as tmp_dir:
            if len(media_paths) is not None:
                for media_path in media_paths:
                    url_type = get_url_type(media_path)
                    if url_type == URLType.UNKNOWN:
                        raise Exception("URL Type unknown")
                    media_extension = get_file_extension(media_path)
                    filename = f"media_{get_random_string(10)}{media_extension}"
                    if url_type == URLType.ONLINE:
                        # download locally (temporarily) before sending
                        tmp_media_path = os.path.join(tmp_dir, f"tmp{media_extension}")
                        save_image_from_url(url=media_path, save_path=tmp_media_path)
                        files.append(File(tmp_media_path, filename=filename))
                    else:
                        files.append(File(media_path, filename=filename))

            return await self.__discord_channel.send(content=value, files=files)

    @discord_message_to_stored_record
    # @wait_for_ready
    async def retrieve(self, *, record_id: Optional[int] = None) -> StoredRecord:
        """
        Retrieves the data from the Discord database.
        """
        return await self.__discord_channel.fetch_message(record_id)
