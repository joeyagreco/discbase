import asyncio
import os
import unittest

from test_e2e.util import client_shutdown_successfully, get_client


class TestDump(unittest.TestCase):
    RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))

    def test_dump_text(self):
        client = get_client()

        async def main():
            await client.start()
            try:
                self.stored_record = await client.dump(value="foo")
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("foo", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual([], self.stored_record.media_urls)
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))

    def test_dump_image_local(self):
        client = get_client()

        local_image_path = os.path.join(self.RESOURCES_PATH, "image.jpg")

        async def main():
            await client.start()
            try:
                self.stored_record = await client.dump(media_path=local_image_path)
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual(1, len(self.stored_record.media_urls))
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))

    def test_dump_image_online(self):
        client = get_client()

        async def main():
            await client.start()
            try:
                self.stored_record = await client.dump(
                    media_path="https://en.wikipedia.org/wiki/Discord#/media/File:Discord_logo.svg"
                )
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual(1, len(self.stored_record.media_urls))
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))

    def test_dump_text_and_image(self):
        client = get_client()

        local_image_path = os.path.join(self.RESOURCES_PATH, "image.jpg")

        async def main():
            await client.start()
            try:
                self.stored_record = await client.dump(value="foo", media_path=local_image_path)
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("foo", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual(1, len(self.stored_record.media_urls))
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))