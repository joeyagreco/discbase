import asyncio
import os
import unittest

from test_e2e.util import client_shutdown_successfully, get_client


class TestRetrieve(unittest.TestCase):
    RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))

    def test_retrieve_text(self):
        client = get_client()

        async def main():
            await client.start()
            try:
                self.stored_record = await client.retrieve(record_id=1204650562943979580)
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("retrieve me", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual([], self.stored_record.media_urls)
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))

    def test_retrieve_image(self):
        client = get_client()

        async def main():
            await client.start()
            try:
                self.stored_record = await client.retrieve(record_id=1204651320561238086)
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

    def test_retrieve_text_and_image(self):
        client = get_client()

        async def main():
            await client.start()
            try:
                self.stored_record = await client.retrieve(record_id=1204652081420443668)
            except Exception as e:
                self.fail(e)
            await client.stop()

        asyncio.run(main())

        self.assertEqual("image text", self.stored_record.text_data)
        self.assertIsNotNone(self.stored_record.record_id)
        self.assertEqual(1, len(self.stored_record.media_urls))
        self.assertIsNotNone(self.stored_record.created_at_utc)
        self.assertIsNotNone(self.stored_record.discord_message)
        self.assertTrue(client_shutdown_successfully(client))
