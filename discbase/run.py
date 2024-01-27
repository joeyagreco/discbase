import asyncio

from client.client import get_client
from dotenv import load_dotenv
from util.CustomLogger import CustomLogger
from util.EnvironmentReader import EnvironmentReader


def main():
    logger = CustomLogger.get_logger()
    load_dotenv()
    TOKEN = EnvironmentReader.get("BOT_TOKEN")
    # GUILD_ID = EnvironmentReader.get("GUILD_ID", as_type=int)
    # CHANNEL_ID = EnvironmentReader.get("CHANNEL_ID", as_type=int)

    client = get_client()

    @client.event
    async def on_ready():
        logger.important(f"DISCBASE IS RUNNING WITH USER {client.user}")

    client.run(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
