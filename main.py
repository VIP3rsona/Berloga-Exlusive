import os
import discord
import requests

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DISCORD_CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):

    if message.author.bot:
        return

    # 🔒 Фильтр по каналу
    if str(message.channel.id) != DISCORD_CHANNEL_ID:
        return

    attachments = message.attachments
    text = message.content

    if len(attachments) >= 2:
        media = []

        for i, att in enumerate(attachments):
            item = {
                "type": "photo",
                "media": att.url
            }

            if i == 0 and text:
                item["caption"] = text

            media.append(item)

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMediaGroup",
            json={
                "chat_id": CHAT_ID,
                "media": media
            }
        )

    elif len(attachments) == 1:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "photo": attachments[0].url,
                "caption": text
            }
        )

    elif text:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text
            }
        )

client.run(DISCORD_TOKEN)
