import asyncio
import unittest

import discord

from discbase.Client import Client
from test_e2e.util import TEST_BOT_TOKEN, TEST_CHANNEL_ID, get_client


class TestClientState(unittest.TestCase):
    def test_alive(self):
        client = get_client()

        async def main():
            await client.start()
            self.assertTrue(client.alive())
            await client.stop()

        asyncio.run(main())
        self.assertFalse(client.alive())

    def test_client_as_context_manager(self):
        client = get_client()

        async def main():
            async with client as c:
                self.assertTrue(c.alive())

        asyncio.run(main())
        self.assertFalse(client.alive())

    def test_create_client_with_invalid_client_token(self):
        # TODO: this passes but logs "Unclosed connector". Not sure why.
        async def main():
            client = Client(
                discord_client_token="im bad",
                discord_channel_id=TEST_CHANNEL_ID,
                connection_timeout_seconds=5,
            )
            with self.assertRaises(discord.errors.LoginFailure):
                await client.start()
            self.assertFalse(client.alive())

        asyncio.run(main())

    def test_dump_with_invalid_channel_id(self):
        async def main():
            client = Client(
                discord_client_token=TEST_BOT_TOKEN,
                discord_channel_id=12345,
                connection_timeout_seconds=5,
            )

            with self.assertRaises(Exception) as context:
                await client.start()
            self.assertFalse(client.alive())
            self.assertEqual("COULD NOT RETRIEVE CHANNEL WITH ID 12345", str(context.exception))

        asyncio.run(main())
