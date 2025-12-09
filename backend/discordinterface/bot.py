import asyncio
from datetime import datetime
import os

import aiohttp
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

API_URL = os.getenv('API_URL', 'http://localhost:8000/')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('n!hello'):
        await userCreationFlow(message)

async def show_typing_and_send(message, delay, message_content):
    async with message.channel.typing():
        await asyncio.sleep(delay)
    await message.channel.send(message_content)

async def userCreationFlow(message):
    await show_typing_and_send(message, 1, "Hello! Welcome to Napbot!")
    await show_typing_and_send(message, 1, "We're excited to get to know you and create the most personalized clothing for you!")
    await show_typing_and_send(message, 1, "To verify if we already know you, please provide us with your email ID")

    try:
       # Collect name
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_email = reply.content.strip()
        await show_typing_and_send(message, 1, "Please wait while we check...")
        await show_typing_and_send(message, 1, "We do not have you in our records, let's get you set up!")

        # Collect email
        await show_typing_and_send(message, 1, "What's your name?")
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_name = reply.content.strip()

        # Collect Phone Number
        await show_typing_and_send(message, 1, f"Great! Nice to meet you, {user_name}! What's your Country Code?")
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_countrycode = reply.content.strip()

        await show_typing_and_send(message, 1, "What's your Phone Number?")
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_phonenumber = reply.content.strip()

    except asyncio.TimeoutError:
        await message.channel.send('Timed out waiting for input. Please try again.')
        return

    try:
        async with aiohttp.ClientSession() as session:
            payload = {'name': user_name, 'email_id': user_email, 'country_code': user_countrycode, 'phone_number': user_phonenumber}
            async with session.post(API_URL + "createUser", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                    await message.channel.send(f"Status: {data['status']}\nName: {data['name']}\nEmail ID: {data['email_id']}")
                else:
                    await message.channel.send(f"API call failed with status {response.status}")
    except Exception as exc:  # Log unexpected failures for debugging
        await message.channel.send('Failed to reach the API. Please try again later.')
        print(f'API error: {exc}')

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

client.run(discord_token)
