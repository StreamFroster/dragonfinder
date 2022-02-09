import nextcord
import random
import uuid
import os

from nextcord.ext import commands

description = 'What truly counts as a dragon?'

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


# Download the image attachment from the user message, then send the image file back to the user.

@bot.command()
async def attachment(ctx):
    if ctx.message.attachments:
        await ctx.message.attachments[0].save('attachment.png')
        await ctx.send(file=nextcord.File('attachment.png'))
    else:
        await ctx.send('No attachments detected, please redo the command with an attachment in your message!')


bot.run('BOT_TOKEN')
