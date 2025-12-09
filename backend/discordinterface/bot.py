"""
Built as a fuck-around-and-find-out project to learn about integrating GenAI with Chatbots.

TODO:
1. Profile validation logic
2. Profile creation logic
3. Message to Bot Owner/Log channel logic for user interactions
4. Integration with MongoDB for info storage
5. Integration with Google Sheets for data audit

"""


import asyncio
from datetime import datetime
import json
import os
import aiohttp
import discord
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

API_URL = os.getenv('API_URL', 'http://localhost:8000/')

@discord_client.event
async def on_ready():
    print(f'We have logged in as {discord_client.user}')

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.mentions:
        await user_creation_flow(message)
        #await openai_start_outfit_flow(message)

#HELPER FUNCTIONS

async def show_typing_and_send(message, message_content):
    async with message.channel.typing():
        await asyncio.sleep(.3)
    await message.channel.send(message_content)

async def get_user_reply(message):
    try:
        reply = await discord_client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        return reply.content

    except asyncio.TimeoutError:
        await message.channel.send("I didn’t get a response.")
        return False

#USER CREATION FLOW - to be re-done

async def user_creation_flow(message):
    user_name = ""
    user_email = ""
    user_countrycode = ""
    user_phonenumber = ""
    
    await show_typing_and_send(message, "Hello! Welcome to Napbot!")
    await show_typing_and_send(message, "We're excited to get to know you and create the most personalized clothing for you!")
    await show_typing_and_send(message, "To verify if we already know you, please provide us with your email ID")

    try:
       # Collect name
        user_email = await get_user_reply(message)
        await show_typing_and_send(message, "Please wait while we check...")
        await show_typing_and_send(message, "We do not have you in our records, let's get you set up!")

        # Collect email
        await show_typing_and_send(message, "What's your name?")
        user_name = await get_user_reply(message)

        # Collect Phone Number
        await show_typing_and_send(message, f"Great! Nice to meet you, {user_name}! What's your Country Code?")
        user_countrycode = await get_user_reply(message)

        await show_typing_and_send(message, "What's your Phone Number?")
        user_phonenumber = await get_user_reply(message)

    except asyncio.TimeoutError:
        pass

    try:
        async with aiohttp.ClientSession() as session:
            payload = {'name': user_name, 'email_id': user_email, 'country_code': user_countrycode, 'phone_number': user_phonenumber}
            async with session.post(API_URL + "createUser", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                    await show_typing_and_send(message, f"You're all set! Welcome aboard, {data['name']}!")
                    await show_typing_and_send(message, "Shall we get you the perfect outfit?")
                    user_input = await get_user_reply(message)
                    if user_input and user_input.lower() in ['yes', 'y', 'sure', 'yeah']:
                        await show_typing_and_send(message, "Awesome! Let's get started on finding your perfect style!")
                        await openai_start_outfit_flow(message)
                else:
                    await message.channel.send(f"API call failed with status {response.status}")
    except Exception as exc:
        await message.channel.send('Failed to reach the API. Please try again later.')
        print(f'API error: {exc}')


#OUTFIT FLOW WITH GROQ OPENAI API

async def openai_start_outfit_flow(message):

    try:

        genai_trigger = True

        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key is None:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        groq = OpenAI(
            api_key=groq_api_key, 
            base_url="https://api.groq.com/openai/v1",
        )

        conversation_history = [
        {"role": "user", "content": "you are a helpful assistant for a seamstress that helps people find clothing styles that suit them best. You will strictly ask about clothing only, not footwear or accessories. You will ask them one liner questions, and base the rest of your questions based on their response. Ask one question at a time. Limit yourself to 5-10 questions based on clues provided by the user before suggesting clothing. provide your suggestions in a concise manner as a oneliner. Get the user's feedback and act on it before closing the conversation. At the end, please also ask the user for required measurements if they have access to the measurements, let the user respond with things such as 'not sure' and 'i can do this when i meet you', if the user does not wish to share it right now, don't push them to share it. If they say no once, don't ask for it again. Return the response as a JSON object with two keys: 'message' which contains the message to the user, and 'end_conversation' which is true if the conversation is to be ended, false otherwise. Remember to end the conversation after providing suggestions and getting feedback. Provide the end trigger at the next message where the user provides their consent that they are ok with the suggestions privided by you, do not wait for the user to send another message before triggering end_conversation."},
        {"role": "user", "content": "I am ready to find my perfect outfit!"},
        ]

        def build_input_from_history(history):
            conversation_text = """Return your response **strictly as a JSON object** in this format:
            {
                "message": "<text of the assistant reply>",
                "end_conversation": true/false
            }

            Do not include any other text. Do not use tools. Do not include "name" or "arguments".
            """
            for msg in history:
                conversation_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
            return conversation_text

        while genai_trigger:
            # Call Groq API
            response = groq.responses.create(
                model="openai/gpt-oss-20b",
                input=build_input_from_history(conversation_history)
            )

            # Parse response, separate "messaage" from "end_conversation"
            raw_reply = response.output_text
            parsed = json.loads(raw_reply)


            # Update history
            assistant_reply = parsed.get('message')
            genai_trigger = not parsed.get('end_conversation')
            conversation_history.append({"role": "assistant", "content": assistant_reply})

            await show_typing_and_send(message, f"{assistant_reply}")
            
            user_input = await get_user_reply(message)
            if user_input is False:
                break
            conversation_history.append({"role": "user", "content": user_input})


        if not genai_trigger:
            #return JSON summary of the conversation
            conversation_history.append({"role": "user", "content": "Ignore the previously described JSON format. Please provide a summary of our conversation in the following JSON format: {\"outfit\": \"<summary of the outfit suggestions and measurements discussed>\", \"size\": \"<summary of the size and measurements discussed, return as an array of different measurements as keys, if the user is not sure of their measurements or wants the seamstress to measure then, mark accordingly>\"}"})
            response = groq.responses.create(
                model="openai/gpt-oss-20b",
                input=build_input_from_history(conversation_history)
            )
            raw_reply = response.output_text
            parsed = json.loads(raw_reply)

            print("FINAL SUMMARY:", parsed)

            await show_typing_and_send(message, "It was great having a chat with you! Feel free to reach out anytime for more fashion advice. Have a wonderful day!")
            return True
        
        raise Exception("Conversation did not end as expected.")
    except Exception as e:
        pass


#MAIN BOT RUNNER 

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

discord_client.run(discord_token)
