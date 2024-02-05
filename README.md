<div align="center">
    <img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/discbase_1.png" alt="discbase logo" width="300"/>
<h1>Discbase</h1>
<h3>Discord as a Database</h3>

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.10-teal.svg"></a>
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/discbase)
<br>
![Unit Tests](https://github.com/joeyagreco/discbase/actions/workflows/unit-tests.yml/badge.svg)
![Formatting Check](https://github.com/joeyagreco/discbase/actions/workflows/formatting-check.yml/badge.svg)
</div>

## Disclaimer
Use this library responsibly and be sure to read [Discord's Terms of Service](https://discord.com/terms) before using.

## Quickstart

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install discbase
```

### Set up a Discord bot

1. Navigate to the [Discord Developer Applications page](https://discord.com/developers/applications)
2. Create a new application and name it
3. Navigate to `Settings/General Information` and save the `Application ID`
4. Navigate to `Settings/Bot`
    - Click `Reset Token`, and save the `Token`
    - Enable `Presence Intent`, `Server Members Intent`, and `Message Content Intent`
5. Paste the application ID you saved into the following URL and paste it into any browser
    - https://discord.com/api/oauth2/authorize?client_id=APPLICATION_ID_HERE&permissions=8&scope=bot
5. Select the server you would like to add this to and follow the prompts to authorize
6. Go to the server that you want to use. The bot you created should be there
7. Find or create the channel you would like to use for storage, right click on the name and copy the channel ID
8. Use the `Token` and `Channel ID` to start the client

```python3
import asyncio

from discbase.database.Client import Client

if __name__ == "__main__":
    TOKEN = {token here as str}
    CHANNEL_ID = {channel id here as int}
    client = Client(discord_client_token=TOKEN, discord_channel_id=CHANNEL_ID)
    
    async def main():
        # start the client
        await client.start()
        try:
            # store some text data and some media
            stored_record = await client.dump(value="some message", media_path="https://some_image.png")
            # retrieve the data
            retrieved_record = await client.retrieve(record_id=stored_record.record_id)
            my_message = stored_record.text_data
            my_media_url = stored_record.media_urls[0]
        except Exception as e:
            print(e)
        # stop the client
        await client.stop()
    
    # run code asynchronously
    asyncio.run(main())
```




## Development

_Run these commands from the root folder_
- Install Dependencies: `make deps`
- Format Code: `make fmt`
- Run Unit Tests: `make test`