import aiohttp
import discord

async def post_async(api, header = {}, json = {}):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.json()

async def post_effect(api, header = {}, json = {}):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.read()

def cembed(
    title="", description="", thumbnail="", picture="", url="", color=discord.Color.dark_theme(), footer=""):
    embed = discord.Embed()
    if color != discord.Color.dark_theme():
        embed = discord.Embed(color=discord.Color(value=color))
    if title != "":
        embed.title = title
    if description != "":
        embed.description = description
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    if picture != "":
        embed.set_image(url=picture)
    if url != "":
        embed.url = url
    if footer != "":
        embed.set_footer(text=footer)
    return embed