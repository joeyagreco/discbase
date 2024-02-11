import asyncio
import os
import unittest

from test_e2e.util import get_client, run_async_test


class TestRetrieve(unittest.TestCase):
    RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = get_client()
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.loop.run_until_complete(cls.client.start())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.loop.run_until_complete(cls.client.stop())
        cls.loop.close()

    def test_retrieve_text(self):
        async def main():
            stored_record = await self.client.retrieve(record_id=1204650562943979580)
            self.assertEqual("retrieve me", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual([], stored_record.media_urls)
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_retrieve_image(self):
        async def main():
            stored_record = await self.client.retrieve(record_id=1204651320561238086)
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_retrieve_multiple_images(self):
        async def main():
            stored_record = await self.client.retrieve(record_id=1205749135924404224)
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(3, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_retrieve_text_and_image(self):
        async def main():
            stored_record = await self.client.retrieve(record_id=1204652081420443668)
            self.assertEqual("image text", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_retrieve_invalid_record_id(self):
        async def main():
            with self.assertRaises(Exception) as context:
                await self.client.retrieve(record_id=12345)
            self.assertTrue(self.client.alive())
            self.assertTrue(
                str(context.exception).startswith("unable to retrieve message with id: 12345")
            )

        run_async_test(self, main())
