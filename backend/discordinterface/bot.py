import asyncio
import os

import aiohttp
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

API_URL = os.getenv('API_URL', 'http://localhost:8000/echo')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('n!hello'):
        await message.channel.send("Hello! What's your name?")

        try:
            reply = await client.wait_for(
                'message',
                timeout=30,
                check=lambda m: m.author == message.author and m.channel == message.channel,
            )
        except asyncio.TimeoutError:
            await message.channel.send('Timed out waiting for your name. Please try again.')
            return

        user_name = reply.content.strip()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, json={'name': user_name}) as response:
                    if response.status == 200:
                        data = await response.json()
                        await message.channel.send(f"Hello, {data['name']}!")
                    else:
                        await message.channel.send(f"API call failed with status {response.status}")
        except Exception as exc:  # Log unexpected failures for debugging
            await message.channel.send('Failed to reach the API. Please try again later.')
            print(f'API error: {exc}')

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

client.run(discord_token)
