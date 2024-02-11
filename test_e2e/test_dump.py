import asyncio
import os
import unittest

from test_e2e.util import get_client, run_async_test


class TestDump(unittest.TestCase):
    RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))
    LOCAL_IMAGE_PATH = os.path.join(RESOURCES_PATH, "image.jpg")
    ONLINE_IMAGE_URL = "https://en.wikipedia.org/wiki/Discord#/media/File:Discord_logo.svg"

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

    def test_dump_image_local_single_image(self):
        async def main():
            stored_record = await self.client.dump(media_paths=[self.LOCAL_IMAGE_PATH])
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_local_multiple_images(self):
        async def main():
            stored_record = await self.client.dump(
                media_paths=[self.LOCAL_IMAGE_PATH, self.LOCAL_IMAGE_PATH, self.LOCAL_IMAGE_PATH]
            )
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(3, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_online_single_image(self):
        async def main():
            stored_record = await self.client.dump(media_paths=[self.ONLINE_IMAGE_URL])
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_online_multiple_images(self):
        async def main():
            stored_record = await self.client.dump(
                media_paths=[self.ONLINE_IMAGE_URL, self.ONLINE_IMAGE_URL, self.ONLINE_IMAGE_URL]
            )
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(3, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_local_and_online_image(self):
        async def main():
            stored_record = await self.client.dump(
                media_paths=[self.LOCAL_IMAGE_PATH, self.ONLINE_IMAGE_URL]
            )
            self.assertEqual("", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(2, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_text_and_image(self):
        async def main():
            stored_record = await self.client.dump(value="foo", media_paths=[self.LOCAL_IMAGE_PATH])
            self.assertEqual("foo", stored_record.text_data)
            self.assertIsNotNone(stored_record.record_id)
            self.assertEqual(1, len(stored_record.media_urls))
            self.assertIsNotNone(stored_record.created_at_utc)
            self.assertIsNotNone(stored_record.discord_message)

        run_async_test(self, main())

    def test_dump_image_invalid_url(self):
        async def main():
            with self.assertRaises(Exception) as context:
                await self.client.dump(media_paths=["im invalid"])
            self.assertTrue(self.client.alive())
            self.assertEqual("url is invalid: 'im invalid'", str(context.exception))

        run_async_test(self, main())

    def test_dump_image_invalid_online_url(self):
        async def main():
            with self.assertRaises(Exception) as context:
                await self.client.dump(media_paths=["https://im-invalid.com"])
            self.assertTrue(self.client.alive())
            self.assertTrue(
                str(context.exception).startswith("could not save url: 'https://im-invalid.com'")
            )

        run_async_test(self, main())
