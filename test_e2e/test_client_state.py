import asyncio
import unittest

from test_e2e.util import get_client


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
