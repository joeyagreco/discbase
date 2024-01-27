import asyncio

import discord
from dotenv import load_dotenv
from util.EnvironmentReader import EnvironmentReader


def main():
    load_dotenv()
    TOKEN = EnvironmentReader.get("BOT_TOKEN")
    GUILD_ID = EnvironmentReader.get("GUILD_ID", as_type=int)
    CHANNEL_ID = EnvironmentReader.get("CHANNEL_ID", as_type=int)

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    client.run(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
