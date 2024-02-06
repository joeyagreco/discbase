import asyncio
import unittest

from test_e2e.util import get_client


class TestMain(unittest.TestCase):
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
