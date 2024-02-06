
from dotenv import load_dotenv

from discbase.database.Client import Client
from discbase.util.EnvironmentReader import EnvironmentReader


def get_client() -> Client:
    load_dotenv()
    TOKEN = EnvironmentReader.get("E2E_BOT_TOKEN")
    CHANNEL_ID = EnvironmentReader.get("E2E_CHANNEL_ID", as_type=int)
    return Client(discord_client_token=TOKEN, discord_channel_id=CHANNEL_ID)
