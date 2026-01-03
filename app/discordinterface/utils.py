import asyncio

active_sessions = {}

async def show_typing_and_send(message, message_content):
    async with message.channel.typing():
        await asyncio.sleep(.3)
    await message.channel.send(message_content)

async def get_user_reply(message, discord_client):
    try:
        reply = await discord_client.wait_for(
            'message',
            timeout=30,
            check=lambda m: m.author == message.author and m.channel == message.channel,
        )
        return reply.content

    except asyncio.TimeoutError:
        await message.channel.send("I didn't get a response.")
        if message.author.id in active_sessions:
            del active_sessions[message.author.id]