import asyncio

from discord import Client as DiscordClient
from discord import Intents
from discord.abc import GuildChannel

from discbase.model.KeyValue import KeyValue
from discbase.util.CustomLogger import CustomLogger


class Client:
    def __init__(self, *, discord_client_token: str, discord_channel_id: int):
        self.__logger = CustomLogger.get_logger()
        self.__discord_client_token = discord_client_token
        self.__discord_channel_id = discord_channel_id
        self.__discord_client = DiscordClient(intents=Intents.all())
        self.__discord_channel = None
        self.client_task = None
        self.__ready = False

    def __get_channel(self, channel_id: int) -> GuildChannel:
        return self.__discord_client.get_channel(channel_id)

    async def start(self):
        self.__logger.info("STARTING DISCORD CLIENT")

        @self.__discord_client.event
        async def on_ready():
            self.__logger.important(f"DISCBASE IS RUNNING WITH USER {self.__discord_client.user}")
            self.__discord_channel = self.__discord_client.get_channel(self.__discord_channel_id)
            if self.__discord_channel == None:
                print("NONE CHANNEL")
            self.__ready = True

        self.client_task = asyncio.create_task(
            self.__discord_client.start(self.__discord_client_token)
        )

        await asyncio.sleep(0)  # Allow the event loop to start the client
        await self.__discord_client.wait_until_ready()

    async def stop(self):
        self.__logger.info("STOPPING DISCORD CLIENT")
        if self.client_task:
            self.client_task.cancel()
            try:
                await self.client_task
            except asyncio.CancelledError:
                pass

    async def wait_for_ready(self):
        max_wait_time_seconds = 5
        for _ in range(max_wait_time_seconds):
            if self.__ready:
                return
            await asyncio.sleep(1)
        raise Exception(f"TIMED OUT WAITING TO CONNECT AFTER {max_wait_time_seconds} SECONDS")

    async def write_kv(self, kv: KeyValue) -> None:
        await self.wait_for_ready()
        return await self.__discord_channel.send(kv.to_dict())
