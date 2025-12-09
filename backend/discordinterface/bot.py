import asyncio
from datetime import datetime
import os
import aiohttp
import discord
from dotenv import load_dotenv
from openai import OpenAI

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
                    await show_typing_and_send(message, .5, f"You're all set! Welcome aboard, {data['name']}!")
                else:
                    await message.channel.send(f"API call failed with status {response.status}")
    except Exception as exc:  # Log unexpected failures for debugging
        await message.channel.send('Failed to reach the API. Please try again later.')
        print(f'API error: {exc}')

    await show_typing_and_send(message, .5, "Shall we get you the perfect outfit?")
    if (message.content.lower() in ['yes', 'y', 'sure', 'yeah']):
        await show_typing_and_send(message, 1, "Awesome! Let's get started on finding your perfect style!")
        await openai_start_outfit_flow(message)

async def openai_start_outfit_flow(message):

    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    )

    conversation_history = [
    {"role": "user", "content": "you are a helpful assistant that helps people find clothing styles that suit them best. You will ask them one liner questions, and base the rest of your questions based on their response. Ask one question at a time. Limit yourself to 5 questions before suggesting clothing. provide your suggestions in a concise manner as a oneliner. Get the user's feedback and act on it before closing the conversation"}
    ]

    def build_input_from_history(history):
        conversation_text = ""
        for msg in history:
            conversation_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return conversation_text

    while True:
        # Call Groq API
        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=build_input_from_history(conversation_history)
        )
        # Update history
        assistant_reply = response.output_text
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        await show_typing_and_send(message, .5, f"{assistant_reply}")
        
        reply = await client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        user_input = reply.content.strip() 
        conversation_history.append({"role": "user", "content": user_input})


discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

client.run(discord_token)
