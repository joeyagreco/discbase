from __future__ import annotations

import asyncio
import os
import tempfile
from functools import wraps
from typing import Optional

from discord import Client as DiscordClient
from discord import File, Intents, Message
from discord.abc import GuildChannel

from discbase.enumeration.URLType import URLType
from discbase.model.StoredRecord import StoredRecord
from discbase.util.CustomLogger import CustomLogger
from discbase.util.error import log_and_raise
from discbase.util.general import get_file_extension, get_random_string, get_url_type
from discbase.util.image import save_image_from_url


class Client:
    def __init__(self, *, discord_client_token: str, discord_channel_id: int):
        self.__logger = CustomLogger.get_logger()
        self.__discord_client_token = discord_client_token
        self.__discord_channel_id = discord_channel_id
        self.__discord_client = DiscordClient(intents=Intents.all())
        self.__discord_channel: Optional[GuildChannel] = None
        self.__client_tasks = []  # TODO: create a process to prune this as the tasks finish
        self.__ready = False  # NOTE: linter thinks this isn't used but it is

    def __del__(self):
        # NOTE: this is not guaranteed to be called on instance deletion,
        # but it is better than not having it in case consumers forget to stop the client.
        asyncio.run(self.stop())

    async def __aenter__(self) -> Client:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> Client:
        await self.stop()

    def __cleanup_after_stop(self) -> None:
        """
        Puts client into a good state after it has been stopped.
        """
        self.__ready = False
        self.__client_tasks = []

    async def __send_with_file(self, *, file_path: str, filename: str, content: str) -> Message:
        file = File(file_path, filename=filename)
        return await self.__discord_channel.send(content=content, file=file)

    def wait_for_ready(func: callable) -> callable:
        """
        Waits for the client to be ready before running the wrapped function.
        If the client is not ready before the timeout, will raise an exception.
        """

        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> any:
            max_wait_time_seconds = 5
            for _ in range(max_wait_time_seconds):
                if self.__ready:
                    return await func(self, *args, **kwargs)
                await asyncio.sleep(1)
            log_and_raise(
                self.__logger, "TIMED OUT WAITING TO CONNECT AFTER {max_wait_time_seconds} SECONDS"
            )

        return wrapper

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
        return self.__ready or len(self.__client_tasks) > 0

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

        self.__client_tasks.append(
            asyncio.create_task(self.__discord_client.start(self.__discord_client_token))
        )
        await asyncio.sleep(0)  # Allow the event loop to start the client
        await self.__discord_client.wait_until_ready()

    async def stop(self):
        """
        Stops the client.
        THE CLIENT MUST BE STOPPED IF STARTED BEFORE TERMINATION.
        """
        if not self.alive():
            return
        self.__logger.info("STOPPING DISCORD CLIENT")
        for task in self.__client_tasks:
            task_name = getattr(task.get_coro(), "__name__", "Unknown Task")
            self.__logger.info(f"CANCELING TASK: {task_name}")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError as e:
                self.__logger.debug(e)
        self.__cleanup_after_stop()

    @discord_message_to_stored_record
    @wait_for_ready
    async def dump(
        self, *, value: Optional[str] = None, media_path: Optional[str] = None
    ) -> StoredRecord:
        """
        Dumps into the Discord database.
        Returns a StoredRecord that represents the data that will be returned on retrieval of this data.
        """
        # validate that we got something
        if all(value is None for value in (value, media_path)):
            raise Exception("Did not receive anything to dump.")

        # default to empty string for value
        value = "" if value is None else value

        if media_path is not None:
            url_type = get_url_type(media_path)
            if url_type == URLType.UNKNOWN:
                raise Exception("URL Type unknown")
            media_extension = get_file_extension(media_path)
            filename = f"media_{get_random_string(10)}{media_extension}"
            if url_type == URLType.ONLINE:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_media_path = os.path.join(tmp_dir, f"tmp{media_extension}")
                    save_image_from_url(url=media_path, save_path=tmp_media_path)
                    return await self.__send_with_file(
                        file_path=tmp_media_path, filename=filename, content=value
                    )
            else:
                return await self.__send_with_file(
                    file_path=media_path, filename=filename, content=value
                )

        return await self.__discord_channel.send(content=value)

    @discord_message_to_stored_record
    @wait_for_ready
    async def retrieve(self, *, record_id: Optional[int] = None) -> StoredRecord:
        """
        Retrieves the data from the Discord database.
        """
        return await self.__discord_channel.fetch_message(record_id)
