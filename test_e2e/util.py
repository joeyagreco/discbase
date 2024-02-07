import unittest

from dotenv import load_dotenv

from discbase.database.Client import Client
from discbase.util.EnvironmentReader import EnvironmentReader


def get_client() -> Client:
    load_dotenv()
    TOKEN = EnvironmentReader.get("E2E_BOT_TOKEN")
    CHANNEL_ID = EnvironmentReader.get("E2E_CHANNEL_ID", as_type=int)
    return Client(discord_client_token=TOKEN, discord_channel_id=CHANNEL_ID)


def client_shutdown_successfully(client: Client) -> bool:
    return not client.alive()


def run_async_test(test_instance: unittest.TestCase, coro):
    """
    Utility method to run an async coroutine with the event loop.
    """
    return test_instance.loop.run_until_complete(coro)
