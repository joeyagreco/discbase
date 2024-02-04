import asyncio
from functools import wraps
from typing import Optional
from discbase.model.StoredRecord import StoredRecord

from discord import Client as DiscordClient
from discord import Intents
from discord.abc import GuildChannel

from discbase.util.CustomLogger import CustomLogger
from discbase.util.error import log_and_raise


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
        self.stop()

    def wait_for_ready(func: callable) -> callable:
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
    
    def response_as_stored_record(func: callable) -> callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> any:
            discord_message_response = await func(self, *args, **kwargs)
            return StoredRecord.from_discord_message(discord_message_response)
        return wrapper

    async def start(self):
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
        self.__logger.info("STOPPING DISCORD CLIENT")
        for task in self.__client_tasks:
            task_name = getattr(task.get_coro(), "__name__", "Unknown Task")
            self.__logger.info(f"CANCELING TASK: {task_name}")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    @response_as_stored_record
    @wait_for_ready
    async def dump(self, value: any) -> StoredRecord:
        return await self.__discord_channel.send(value)
