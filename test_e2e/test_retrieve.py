import asyncio
import os
import unittest

from test_e2e.util import get_client


class TestRetrieve(unittest.TestCase):
    RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = get_client()
        # Create a new event loop and set it as the current event loop
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.loop.run_until_complete(cls.client.start())

    @classmethod
    def tearDownClass(cls) -> None:
        # Use the same loop to run cleanup
        cls.loop.run_until_complete(cls.client.stop())
        cls.loop.close()
        asyncio.set_event_loop(None)  # Optional: remove the loop from current context

    def test_retrieve_text(self):
        # This method ensures the test runs in an async context
        def run_async_test(async_func):
            return self.loop.run_until_complete(async_func)

        async def main():
            stored_record = await self.client.retrieve(record_id=1204650562943979580)
            self.assertEqual("retrieve me", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual([], stored_record.media_urls)
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(main())

    def test_retrieve_image(self):
        # This method ensures the test runs in an async context
        def run_async_test(async_func):
            return self.loop.run_until_complete(async_func)

        async def main():
            stored_record = await self.client.retrieve(record_id=1204651320561238086)
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(main())

    def test_retrieve_text_and_image(self):
        # This method ensures the test runs in an async context
        def run_async_test(async_func):
            return self.loop.run_until_complete(async_func)

        async def main():
            stored_record = await self.client.retrieve(record_id=1204652081420443668)
            self.assertEqual("image text", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(main())
