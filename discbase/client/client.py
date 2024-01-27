from discord import Client, Intents


def get_client() -> Client:
    intents = Intents.all()
    return Client(intents=intents)
