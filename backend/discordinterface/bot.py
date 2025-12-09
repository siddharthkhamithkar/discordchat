import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('n!hello'):
        await message.channel.send('Hello!')

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

client.run(discord_token)
