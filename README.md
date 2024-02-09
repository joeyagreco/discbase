<div align="center">
    <img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/discbase_1.png" alt="discbase logo" width="300"/>
<h1>Discbase</h1>
<h3>Discord as a Database</h3>

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.10-teal.svg"></a>
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/discbase)
<br>
![E2E Tests](https://github.com/joeyagreco/discbase/actions/workflows/e2e-tests.yml/badge.svg)
![Unit Tests](https://github.com/joeyagreco/discbase/actions/workflows/unit-tests.yml/badge.svg)
![Build](https://github.com/joeyagreco/discbase/actions/workflows/build.yml/badge.svg)
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
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/create_an_application.png" width="400">

3. Navigate to `Settings/General Information` and save the `Application ID`
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/settings_general_information.png" width="400"
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/application_id.png" width="400">

4. Navigate to `Settings/Bot`
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/settings_bot.png" width="400">

5. Click `Reset Token`, and save the `Token`
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/reset_token.png" width="400">

6. Enable `Presence Intent`, `Server Members Intent`, and `Message Content Intent`
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/privileged_intents.png" width="400">

7. Paste the application ID you saved into the following URL and paste it into any browser: https://discord.com/api/oauth2/authorize?client_id=APPLICATION_ID_HERE&permissions=8&scope=bot

8. Select the server you would like to add this to and follow the prompts to authorize
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/add_bot_to_server.png" width="400">

### Pick a Channel to Use for Storage
1. Go to the server that you want to use. The bot you created should be there
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/offline_bot.png" width="400">

2. Find or create the channel you would like to use for storage, right click on the name and copy the channel ID
<img src="https://raw.githubusercontent.com/joeyagreco/discbase/main/img/quickstart/copy_channel_id.png" width="400">

### Run the Client

```python3
import asyncio

from discbase.database.Client import Client

if __name__ == "__main__":
    # put your token here as a string
    TOKEN = "TOKEN_123"
    # put your channel id here as an integer
    CHANNEL_ID = 123
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

### Alternatively, Run the Client as a Context Manager

This is much slower as each time the context manager is used, it has to start up the client and connect first.

The advantage is closing will always be taken care of automatically.

```python3
import asyncio

from discbase.database.Client import Client

if __name__ == "__main__":
    async def main():
        # this runs the client
        async with Client(discord_client_token="TOKEN_123", discord_channel_id=123) as client:
            await client.dump(value="foo")
        # the client is now closed automatically

    asyncio.run(main())
``` 

## Performance
**NOTE:** You will need to save environment variables for `BOT_TOKEN` and `CHANNEL_ID` before running this.
```bash
$ export BOT_TOKEN='token'            # your bot token here
$ export CHANNEL_ID=12345             # your discord channel id
$ make speedtest                      # run speedtest with default number of messages
$ make speedtest SPEEDTEST_COUNT=100  # run speedtest with 100 messages
```

## Development

_Run these commands from the root folder_
- Install Dependencies: `make deps`
- Format Code: `make fmt`
- Run Unit Tests: `make test-unit`

## Styling

Primary Color: `#8557BA`