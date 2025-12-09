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
        await userCreationFlow(message)

async def userCreationFlow(message):
    await message.channel.send("Hello! What's your name?")

    try:
       # Collect name
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_name = reply.content.strip()

        # Collect email
        await message.channel.send("What's your email ID?")
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_email = reply.content.strip()

        # Collect DOB
        await message.channel.send("What's your date of birth? (dd/mm/yyyy)")
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_dob = reply.content.strip()

    except asyncio.TimeoutError:
        await message.channel.send('Timed out waiting for input. Please try again.')
        return

    try:
        async with aiohttp.ClientSession() as session:
            payload = {'name': user_name, 'email_id': user_email, 'dob': user_dob}
            async with session.post(API_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    await message.channel.send(f"Thank you! Your information has been received. \nName: {data['name']}\nEmail ID: {data['email_id']}\nDOB: {data['dob']}")
                else:
                    await message.channel.send(f"API call failed with status {response.status}")
    except Exception as exc:  # Log unexpected failures for debugging
        await message.channel.send('Failed to reach the API. Please try again later.')
        print(f'API error: {exc}')

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

client.run(discord_token)
