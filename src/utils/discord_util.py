import discord
from discord.ext import commands
from src.utils.secret_storage import secrets
import requests


def send_text(text):
    out = {
        "username": "AI Mod",
        "content": text,
        'avatar_url': 'https://i.imgur.com/0wVctyU.png'
    }
    requests.post(secrets['discord']['webhook_url'], data=out)


if __name__ == '__main__':
    send_text('test')
