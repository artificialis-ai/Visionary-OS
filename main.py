from inspect import GEN_CREATED
import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import random
from urllib import request, parse
import json
from utils import *
import asyncio
from io import BytesIO


global pass_respose, generated
past_respose = []
generated = []

c = discord.Color.blue()
bot = commands.Bot(command_prefix='$', case_insensitive=True)


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
    auth = os.getenv("transformers_auth")
    headeras = {"Authorization": f"Bearer {auth}"}
    if message.author == bot.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Hello!')

    if message.content.lower().startswith("vision "):
        input_text = message.content.lower().replace("alfred", "")
        payload = {
                "inputs": {
                    "past_user_inputs": past_respose,
                    "generated_responses": generated,
                    "text": input_text,
                },
                "parameters": {"repetition_penalty": 1.33},
            }

        output = await post_async(API_URL, header=headeras, json=payload)

        if len(past_respose) < 20:
            past_respose.append(input_text)
            generated.append(output["generated_text"])
        else:
            past_respose.pop(0)
            generated.pop(0)
            past_respose.append(input_text)
            generated.append(output["generated_text"])

            
            await message.reply(output["generated_text"])

@bot.listen('on_command_error')
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(str(error))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print("error not caught")
        print(error) 

# Example of a command
@bot.command(name='command_name', description="Description for help command")
async def command(ctx, other_arguments_here):
    pass # Do stuff here

@bot.command(name='uptime', description="Get the time the bot has been online")
async def command(ctx):
    await ctx.send(f'Uptime: {datetime.datetime.now() - start_time}')

@bot.command(name='8ball', description="Answers a yes/no question")
async def command(ctx, question):
    answers = ["Yes", "No", "I don't know", "Maybe", "Yep", "Nope", "Absolutley yes", "Absolutley no"]
    await ctx.send(random.choice(answers))

@bot.command(name='translate', description="Translate some text to another language")
async def command(ctx, language_from, language_to, *, text):
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
    
    await ctx.send(translated_text)


@bot.command(aliases=["pfp"])
async def get_pfp(ctx, member:discord.Member=None):
    
    if member is None:
        embed = discord.Embed(title="Profile Picture : {}".format(ctx.author.name), color=c)
        embed.set_image(url=ctx.author.avatar_url)
    
    else:
        embed = discord.Embed(title="Profile Picture : {}".format(member.name), color=c)
        embed.set_image(url=member.avatar_url)
    
    await ctx.send(embed=embed)

@bot.command(aliases=['ef','effect'])
async def effects(ctx, effect:str = None, member:discord.Member=None):

    if member == None:
        url = ctx.author.avatar_url_as(format='png')
    else:
        url = member.avatar_url_as(format='png')

    url = str(url)

    if effect == None:
        await ctx.send(
                    embed=cembed(
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
                    embed=cembed(
                        title="OOPS",
                        description="""hmm no such effect. The effects are given below. \n s!effects <effect> <member> if member is none the users pfp will be modified \n The list of effects is \n- cartoonify \n- watercolor \n- canny \n- pencil \n- econify \n- negative \n- pen \n- candy \n- composition \n- feathers \n- muse \n- mosaic \n- night \n- scream \n- wave \n- udnie """,
                        color=c,
                    )
                )
        return

    elif effect in styles:
        json = {"url":url, "effect":effect}

        byte = await post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/style", json=json)


    elif effect in effects:
        json = {"url":url, "effect":effect}

        byte = await post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/cv", json=json)

    
    await ctx.send(file=discord.File(BytesIO(byte), 'effect.png'))

@bot.command(aliases=['transform'])
async def blend(ctx, urlef:str = None, member:discord.Member=None, ratio=0.5):
    if member == None:
        url = ctx.author.avatar_url_as(format='png')
    else:
        url = member.avatar_url_as(format='png')

    url = str(url)

    if urlef == None:
        await ctx.send(
                    embed=cembed(
                        title="OOPS",
                        description="""Hmm You seem to be forgetting an argument \n 'effects <style url> <member[optional]> <ratio[optional]> if member is none the users pfp will be modified. The default ratio is 0.5""",
                        color=c,
                    )
                )
        return

    json = {"url":url, "url2":urlef, "ratio":ratio}

    byte = await post_effect("https://suicide-detector-api-1.yashvardhan13.repl.co/style_predict", json=json)
    await ctx.send(file=discord.File(BytesIO(byte), 'effect.png'))

@bot.command()
async def gen(ctx, *, text):
    print(ctx.guild.name)
    API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
    payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 100, "return_full_text": True},
        }

    output = await post_async(API_URL2, header2, payload2)
        
    o = output[0]["generated_text"]
    await ctx.send(o)

bot.run(os.environ['BOT_TOKEN'])
