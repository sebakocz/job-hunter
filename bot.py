import os
import time

from dotenv import load_dotenv

import discord
from discord.ext import commands

import asyncpraw

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    target_channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL")))

    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_API_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent="Job Hunter (by u/_Sevas_)",
        username=os.getenv("REDDIT_USERNAME"),
    )

    subreddit = await reddit.subreddit(os.getenv("SUBREDDIT_LIST"))
    while True:
        try:
            async for submission in subreddit.stream.submissions(skip_existing=True, pause_after=0):
                if submission is None:
                    continue
                if "hiring" in submission.title.lower():
                    await target_channel.send(f"https://www.reddit.com{submission.permalink}")
        except Exception as e:
            await target_channel.send(e)
            time.sleep(60*5)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")

bot.run(os.getenv("DISCORD_TOKEN"))
