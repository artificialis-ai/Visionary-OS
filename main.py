import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import random
from urllib import request, parse
import json

# Import local library - see the utils folder
import utils as ut

# Initialize the bot
bot = commands.Bot(command_prefix='$', case_insensitive=True)

# Remove the default help command
bot.remove_command('help')

# Get the starting time to calculate uptime
start_time = datetime.datetime.now()

# Load the language file for translations
with open("./assets/languages.json", "r") as f:
    languages = json.loads(f.read())

# Task to keep heroku busy
@tasks.loop(minutes=25.0)
async def heroku_ping():
    print("Ping!")

# Event examples
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    
    game = discord.Game("Open Sourcerers")
    heroku_ping.start()
    await bot.change_presence(activity = game)

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return

    # Secret commands here! They will not show in the help command
    
    if message.content.startswith('$ping'):
        await message.channel.send('Pong and Hello!')
    
    if message.content.startswith('$i-read-source-code ' + str(message.author.id)):
        await message.channel.send(message.author.mention + " reads source code!")

@bot.listen('on_command_error')
async def on_command_error(ctx, error):    
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        err = str(error)
    if isinstance(error, commands.MissingPermissions):
        err = "You do not have the appropriate permissions to run this command."
    if isinstance(error, commands.BotMissingPermissions):
        err = "I don't have sufficient permissions!"
    else:
        print("error not caught")
        print(error) 
        return
        
        # Comment the code above and uncomment the code below to get more accurate error mesages
        # raise error
    
    embed = ut.embeds.ErrorEmbed(ctx, err)
    await ctx.send(embed=embed)

# Uptime - send the difference between the current time and the starting time
@bot.command(name='uptime', description="Get the time the bot has been online", usage="uptime")
async def uptime(ctx):
    t = datetime.datetime.now() - start_time
    embed = ut.embeds.SendEmbed(ctx, "Uptime", str(t))
    await ctx.send(embed=embed)

# 8ball - Pick a random answer from the list and send it
@bot.command(name='8ball', description="Answers a yes/no question", usage="8ball <question>")
async def ball(ctx, *, question):
    answers = ["Yes", "No", "I don't know", "Maybe", "Yep", "Nope", "Absolutley yes", "Absolutley no"]
    embed = ut.embeds.SendEmbed(ctx, question, random.choice(answers))
    await ctx.send(embed=embed)

# Translate - Convert the languages to codes and access the Google Translate API
@bot.command(name='translate', description="Translate some text to another language", usage="translate <language_from> <language_to> <text>")
async def translate(ctx, language_from, language_to, *, text):
    if language_from not in languages.keys():
        await ctx.send(f"Language {language_from} not found")
    elif language_to not in languages.keys():
        await ctx.send(f"Language {language_to} not found")
    
    language_from = languages[language_from]
    language_to = languages[language_to]

    try:
        resp = ut.api.APIRequest("https://translate.googleapis.com/translate_a/single", params={"client": "gtx", "sl": language_from, "tl": language_to, "dt": "t", "q": text})
    except:
        await ctx.send("An error occurred", "An error occurred. Please try again later.")
    
    translated_text = ""
    
    for sentence in resp[0]:
        translated_text += sentence[0]
    
    embed = ut.embeds.SendEmbed(ctx, "Translated text", translated_text)
    await ctx.send(embed=embed)

# Latex - Convert the LaTeX code to an image and send it using the codecogs API
@bot.command(name="latex", description="Render some LaTeX", usage="latex <latex_code>")
async def latex(ctx, *, latex):
    url = "https://latex.codecogs.com/gif.latex?\\bg_white&space;" + parse.quote(latex.replace("(", "\(").replace(")", "\)"))
    embed = ut.embeds.SendEmbed(ctx, "Rendered LaTeX", latex, image=url)
    await ctx.send(embed=embed)

@bot.command(name="help", description="Get help on commands", usage="help [command]")
async def help(ctx, command=None):
    if not command:
        embed = ut.embeds.HelpEmbed(ctx, bot.commands)
    else:
        for c in bot.commands:
            if c.name == command:
                command = c
        if type(command) == str:
            embed = ut.embeds.ErrorEmbed(ctx, "Command {} not found".format(command))
            ctx.send(embed=embed)
            return
                
        embed = ut.embeds.CommandHelpEmbed(ctx, command)
    
    await ctx.send(embed=embed)

# Start the bot
# IMPORTANT: Use your token here. 
bot.run(os.environ['BOT_TOKEN'])