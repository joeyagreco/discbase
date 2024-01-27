import asyncio

from dotenv import load_dotenv

from discbase.database.Client import Client
from discbase.model.KeyValue import KeyValue
from discbase.util.EnvironmentReader import EnvironmentReader

if __name__ == "__main__":
    load_dotenv()
    TOKEN = EnvironmentReader.get("BOT_TOKEN")
    CHANNEL_ID = EnvironmentReader.get("CHANNEL_ID", as_type=int)
    client = Client(discord_client_token=TOKEN, discord_channel_id=CHANNEL_ID)
    
    async def main():
        await client.start()
        try:
            await client.write_kv(KeyValue(key="foo", value="bar"))
        except Exception as e:
            print(e)
        await client.stop()
    
    asyncio.run(main())