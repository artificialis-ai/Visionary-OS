import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import random
from urllib import request, parse
import json
from sqlalchemy import alias

from tables import Description
from utils import *
import asyncio
from io import BytesIO
import utils as ut

global pass_respose, generated
past_respose = []
generated = []

c = discord.Color.blue()
bot = commands.Bot(command_prefix='$', case_insensitive=True)

bot.remove_command('help')

start_time = datetime.datetime.now()

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
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    auth = os.environ["transformers_auth"]
    headeras = {"Authorization": f"Bearer {auth}"}
    if message.author == bot.user:
        return

    # Secret commands here! They will not show in the help command
    
    if message.content.startswith('$ping'):
        await message.channel.send('Pong and Hello!')
    
    if message.content.startswith('$i-read-source-code ' + str(message.author.id)):
        await message.channel.send(message.author.mention + " reads source code!")

    if message.content.lower().startswith("vision ") or message.content.lower().startswith("visionary "):
        input_text = message.content.lower().replace("alfred", "")
        payload = {
                "inputs": {
                    "past_user_inputs": past_respose,
                    "generated_responses": generated,
                    "text": input_text,
                },
                "parameters": {"repetition_penalty": 1.33},
            }

        output = await ut.post_async(API_URL, header=headeras, json=payload)

        if len(past_respose) < 20:
            past_respose.append(input_text)
            generated.append(output["generated_text"])
        else:
            past_respose.pop(0)
            generated.pop(0)
            past_respose.append(input_text)
            generated.append(output["generated_text"])

            
            await message.reply(output["generated_text"])
@bot.command(name = 'chatbot', help = 'To use chatbot use ```vision/visionary <text>```')
async def chatbot(ctx):
    await ctx.send("To use chatbot use `vision/visionary <text>`")

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
        # print("error not caught")
        # print(error) 
        raise error
        # return
    
    embed = ut.embeds.ErrorEmbed(ctx, err)
    await ctx.send(embed=embed)

# Example of a command
@bot.command(name='command_name', description="Description for help command")
async def command(ctx, other_arguments_here):
    pass # Do stuff here

@bot.command(name='uptime', description="Get the time the bot has been online", usage="uptime")
async def uptime(ctx):
    t = datetime.datetime.now() - start_time
    embed = ut.embeds.SendEmbed(ctx, "Uptime", str(t))
    await ctx.send(embed=embed)

@bot.command(name='8ball', description="Answers a yes/no question", usage="8ball <question>")
async def ball(ctx, *, question):
    answers = ["Yes", "No", "I don't know", "Maybe", "Yep", "Nope", "Absolutley yes", "Absolutley no"]
    embed = ut.embeds.SendEmbed(ctx, question, random.choice(answers))
    await ctx.send(embed=embed)

@bot.command(name='translate', description="Translate some text to another language", usage="translate <language_from> <language_to> <text>")
async def translate(ctx, language_from, language_to, *, text):
    if language_from not in languages.keys():
        await ctx.send(f"Language {language_from} not found")
    elif language_to not in languages.keys():
        await ctx.send(f"Language {language_to} not found")
    
    language_from = languages[language_from]
    language_to = languages[language_to]

    try:
        resp = request.urlopen(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={language_from}&tl={language_to}&dt=t&q={parse.quote_plus(text)}").read().decode("utf8")
    except:
        await ctx.send("An error occurred", "An error occurred. Please try again later.")
    
    translated_text = ""
    
    for sentence in json.loads(resp)[0]:
        translated_text += sentence[0]
    
    embed = ut.embeds.SendEmbed(ctx, "Translated text", translated_text)
    await ctx.send(embed=embed)


@bot.command(name = "pfp", aliases=["profilepicture", "profilepic", "pp"], description="Get a user's profile picture", usage="pfp <user>")
async def get_pfp(ctx, member:discord.Member=None):
    
    if member is None:
        embed = discord.Embed(title="Profile Picture : {}".format(ctx.author.name), color=c)
        embed.set_image(url=ctx.author.avatar_url)
    
    else:
        embed = discord.Embed(title="Profile Picture : {}".format(member.name), color=c)
        embed.set_image(url=member.avatar_url)
    
    await ctx.send(embed=embed)

@bot.command(name = "effect", aliases=['ef','effect'] , description="Get a desired effect on a pfp effect \n The list of effects is ``` \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie```", usage="effect <effect_name> <user[Optional]> ")
async def effects(ctx, effect:str = None, member:discord.Member=None):

    if member == None:
        url = ctx.author.avatar_url_as(format='png')
    else:
        url = member.avatar_url_as(format='png')

    url = str(url)

    if effect == None:
        await ctx.send(
                    embed=ut.cembed(
                        title="OOPS",
                        description="""Hmm You seem to be forgetting an argument \n 'effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                        color=c,
                    )
                )
        return

    styles = ['candy', 'composition', 'feathers', 'muse', 'mosaic', 'night', 'scream', 'wave', 'udnie']

    effects = ['cartoonify', 'watercolor', 'canny', 'pencil', 'econify', 'negative', 'pen']

    if effect not in styles and effect not in effects and effect is not None:
        await ctx.send(
                    embed=ut.cembed(
                        title="OOPS",
                        description="""hmm no such effect. The effects are given below. \n s!effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                        color=c,
                    )
                )
        return

    elif effect in styles:
        json = {"url":url, "effect":effect}

        byte = await ut.post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/style", json=json)


    elif effect in effects:
        json = {"url":url, "effect":effect}

        byte = await ut.post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/cv", json=json)

    
    await ctx.send(file=discord.File(BytesIO(byte), 'effect.png'))

@bot.command(name = "blend", aliases=['transform'], description = "Blend a users image with an external images", usage="blend <desired image url> <user[optional](userid or ping the user)>")
async def blend(ctx, urlef:str = None, member:discord.Member=None, ratio=0.5):
    if member == None:
        url = ctx.author.avatar_url_as(format='png')
    else:
        url = member.avatar_url_as(format='png')

    url = str(url)

    if urlef == None:
        await ctx.send(
                    embed=ut.cembed(
                        title="OOPS",
                        description="""Hmm You seem to be forgetting an argument \n 'effects <style url> <member[optional]> <ratio[optional]> if member is none the users pfp will be modified. The default ratio is 0.5""",
                        color=c,
                    )
                )
        return

    json = {"url":url, "url2":urlef, "ratio":ratio}

    byte = await ut.post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/style_predict", json=json)
    await ctx.send(file=discord.File(BytesIO(byte), 'effect.png'))

@bot.command(name = "generate", alias=['gen'], description = "Generate text based on input prompt", usage="generate <text>")
async def gen(ctx, *, text):
    
    API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
    payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 200, "return_full_text": True},
        }

    output = await ut.post_async(API_URL2, header2, payload2)
        
    o = output[0]["generated_text"]
    await ctx.send(o)

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

bot.run(os.environ['BOT_TOKEN'])
