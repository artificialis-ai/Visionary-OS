import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$', case_insensitive=True)

# EVENT EXAMPLES
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    members = len(set(bot.get_all_members()))
    game = discord.Game("Open Sourcerers")
    await bot.change_presence(activity = game)

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Hello!')

# Example of a command
@bot.command(name='command_name', description="description for help command")
async def command(ctx, other_arguments_here):
    pass # Do stuff here

bot.run(os.environ['BOT_TOKEN'])
