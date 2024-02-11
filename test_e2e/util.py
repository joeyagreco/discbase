import unittest

from discbase.Client import Client
from discbase.util.EnvironmentReader import EnvironmentReader

TEST_BOT_TOKEN = EnvironmentReader.get("E2E_BOT_TOKEN")
TEST_CHANNEL_ID = EnvironmentReader.get("E2E_CHANNEL_ID", as_type=int)


def get_client() -> Client:
    return Client(discord_client_token=TEST_BOT_TOKEN, discord_channel_id=TEST_CHANNEL_ID)


def client_shutdown_successfully(client: Client) -> bool:
    return not client.alive()


def run_async_test(test_instance: unittest.TestCase, coro):
    """
    Utility method to run an async coroutine with the event loop.
    """
    return test_instance.loop.run_until_complete(coro)
