import asyncio
import os
import unittest

from test_e2e.util import get_client, run_async_test


class TestDump(unittest.TestCase):
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

    def test_dump_text(self):
        async def main():
            stored_record = await self.client.dump(value="foo")
            self.assertEqual("foo", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual([], stored_record.media_urls)
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_local(self):
        async def main():
            local_image_path = os.path.join(self.RESOURCES_PATH, "image.jpg")
            stored_record = await self.client.dump(media_paths=[local_image_path])
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_online(self):
        async def main():
            stored_record = await self.client.dump(
                media_paths=["https://en.wikipedia.org/wiki/Discord#/media/File:Discord_logo.svg"]
            )
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_text_and_image(self):
        local_image_path = os.path.join(self.RESOURCES_PATH, "image.jpg")

        async def main():
            stored_record = await self.client.dump(value="foo", media_paths=[local_image_path])
            self.assertEqual("foo", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())
