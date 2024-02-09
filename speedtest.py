import asyncio
import sys
import time

from dotenv import load_dotenv

from discbase.database.Client import Client
from discbase.util.EnvironmentReader import EnvironmentReader

if __name__ == "__main__":
    load_dotenv()
    TOKEN: str = EnvironmentReader.get("BOT_TOKEN")
    CHANNEL_ID: int = EnvironmentReader.get("CHANNEL_ID", as_type=int)

    async def main(count: int) -> None:
        stored_messages: list = []

        async with Client(discord_client_token=TOKEN, discord_channel_id=CHANNEL_ID) as c:
            start_time: float = time.time()

            for i in range(count):
                stored_messages.append(await c.dump(value=f"message {i+1}"))

            end_time: float = time.time()
            total_time: float = end_time - start_time
            print(f"Dumped {count} messages in {total_time:.2f} seconds.")
            print(f"{count / total_time:.2f} messages per second.")

            start_time = time.time()

            for msg in stored_messages:
                await c.retrieve(record_id=msg.record_id)

            end_time = time.time()
            total_time = end_time - start_time
            print(f"Retrieved {count} messages in {total_time:.2f} seconds.")
            print(f"{count / total_time:.2f} messages per second.")

    # Check if at least one additional argument is provided
    if len(sys.argv) <= 1:
        print("No speedtest count provided")
        exit(1)
    count = int(sys.argv[1])

    asyncio.run(main(count))
