import discord
from discord.ext import commands, tasks
from discord import client, Intents 
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import json
import asyncio
import time
import datetime
from datetime import datetime
import random
import sys
import os
import traceback
import requests

"""
https://github.com/Crazycatz00/heroku-buildpack-libopus
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest Need these two package aswell.
"""

bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=Intents.all())

@bot.command()
async def whoareyou(ctx):
    await ctx.send('"WHAT YOU THINK?" I am Bot.')

@bot.command()
async def hi(ctx):
    await ctx.send('Hello! How can i help you')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping is {round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_permissions(administrator=True)
async def timer(ctx, secounds):
    try:
        secoundint = int(secounds)
        if secoundint <= 0:
            await ctx.send('ARE YOU TRY TO MAKE ME FOOL! Put the secound higher than Zero.')
            raise BaseException
   
        message = await ctx.send(f'Timer has been set for {secounds}')
    
    
        while True:
         secoundint -= 1
         if secoundint == 0:
             await message.edit(content='What you are looking for its Ended.')
             break
         await message.edit(content=f'Timer: {secoundint}')
         await asyncio.sleep(1)
        await ctx.send(f'{ctx.author.mention},"Where are you?" Your count down has been Ended.')
    
    except ValueError:
        await ctx.send('"Retard, Secounds are in number" Enter the number.')

@timer.error
async def timer_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('"Count Yourself!" You dont have permission.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('"ARE YOU RETARD", Put some secound to count down.')


@bot.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def av(ctx,user: discord.Member=None):
    if user is None:
        user = ctx.message.author
        return await ctx.send(user.avatar_url)
    await ctx.send(user.avatar_url)

@bot.event
async def on_member_join(member: discord.Member):
    url = requests.get(member.avatar_url)
    avatar = Image.open(BytesIO(url.content))
    avatar = avatar.resize((250, 250))
    bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mask)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('avatar.png')
    fundo = Image.open( 'imagens/welcome.png' )
    fonte = ImageFont.truetype('fonts/Digital.otf', 50)
    escrever = ImageDraw.Draw(fundo)
    escrever.text(xy=(300,90), text='Hey! {}'.format(member.name), fill="#ffffff", font=fonte)
    escrever.text(xy=(300,135), text='Welcome to SAMP Legal Mods.'.format(member.guild.name), fill="#ffffff", font=fonte)
    escrever.text(xy=(300,180), text='You are the {} member.\nMake sure you read the rules.'.format(member.guild.member_count), fill="#ffffff", font=fonte)
    fundo.paste(avatar, (25, 25), avatar)
    fundo.save('tmpBv.png', format='PNG')
    file = discord.File(open('tmpBv.png', 'rb'))
    channel_welcome = bot.get_channel(747426149268848690)
    await channel_welcome.send(f'Hey! {member.mention}, Welcome to {member.guild.name}.')
    await channel_welcome.send(file=file)
    role = member.guild.get_role(746380043344937081)
    await member.add_roles(role, reason=None)
    await member.send(f' Hey! {member.name} Welcome to SA-MP Legal Mods.\nThe one best modifications server for modding on discord.\nMake sure you read rules in #📌-𝘿𝙞𝙨𝙘𝙤𝙧𝙙-𝙍𝙪𝙡𝙚𝙨-📜.')


@bot.event
async def on_member_remove(member: discord.Member):
    await member.send(f'Hey! {member.mention} You left the SA-MP Legal Mods.\n Hope you have great time with us.')



extensions=[
            'cogs.moderation',
            'cogs.music',
            'cogs.samp',
]



if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Error loading {extension}', file=sys.stderr)
            traceback.print_exc()


# async def create_db_pool():
#     bot.db = await asyncpg.create_pool(database="chieftest", user="postgres", password="ArYa250611")
#     print("Connected to Datebase.")

# bot.loop.create_task(create_db_pool())


with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    activity = discord.Game(name="Listening Instruction from DeViL#3078", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")

bot.run(TOKEN)
