# bot.py
import os
import requests
import discord
import json
import asyncio
import datetime

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from gpiozero import LED

ledg = LED(16)
ledr = LED(6)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENTID = os.getenv('CLIENT_ID')
CLIENTSECRET = os.getenv('CLIENT_SECRET')
REALMID = os.getenv('REALM_ID')
USERID = os.getenv('USER_ID')

bot = commands.Bot(command_prefix='+')
guild = 0
role = 0
channel = 0

@tasks.loop(seconds=60.0)
async def update_status():
        while True:
                global initialstatus
                global accesstoken
                global tokenresponse
                global channel
                global initialqueue
                channel = discord.utils.get(guild.channels, name="server-status")
                tokenresponse = create_access_token(CLIENTID, CLIENTSECRET)
                accesstoken = tokenresponse["access_token"]
                print(f'Access Token: {accesstoken}')
                updaterequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{REALMID}?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
                if updaterequest:
                        updaterequest = updaterequest.json()
                        updatestatus = updaterequest['status']['name']
                        queuestatus = updaterequest['has_queue']
                        if updatestatus != initialstatus:
                                if updatestatus == 'Up':
                                        ledg.on()
                                        ledr.off()
                                else:
                                        ledg.off()
                                        ledr.on()
                                await channel.send(f'{role.mention} Server status has changed to: {updatestatus}!')
                                initialstatus = updatestatus
                                ct = datetime.datetime.now()
                                print(f'Status Changed to {updatestatus} at {ct}.')
                                await asyncio.sleep(5)
                        else:
                                if updatestatus == 'Up':
                                        ledg.on()
                                        ledr.off()
                                else:
                                        ledg.off()
                                        ledr.on()
                                ct = datetime.datetime.now()
                                print(f'No Change from {initialstatus} at {ct}.')
                                await asyncio.sleep(5)
                        if queuestatus != initialqueue:
                                if queuestatus is False:
                                        await channel.send(f'{role.mention} The server no longer has a login queue!')
                                else:
                                        await channel.send(f'{role.mention} The server now has a login queue!')
                                initialqueue = queuestatus
                                ct = datetime.datetime.now()
                                print(f'The queue status has changed at {ct}.')
                        else:
                                ct = datetime.datetime.now()
                                print(f'No queue change at {ct}.')
                else:
                        ct = datetime.datetime.now()
                        print(f'No Response from api request at {ct}.')
                        ledg.on()
                        ledr.on()

@bot.event
async def on_ready():
        global guild
        global role
        global channel
        update_status.start()
        guild = bot.guilds[0]
        role = discord.utils.get(guild.roles, name="Member")
        channel = discord.utils.get(guild.channels, name="server-status")
        print(f'{bot.user.name} has connected to Discord!')

def create_access_token(client_id, client_secret, region = 'us'):
        data = { 'grant_type': 'client_credentials' }
        response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
        if response.json() is not None:
            return response.json()
        else:
            ct = datetime.datetime.now()
            print(f'No JSON in response for access token at {ct}.')
            ledg.on()
            ledr.on()

tokenresponse = create_access_token(CLIENTID, CLIENTSECRET)
accesstoken = tokenresponse["access_token"]
print(accesstoken)

initialrequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{REALMID}?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
initialrequest = initialrequest.json()
initialstatus = initialrequest['status']['name']
initialqueue = initialrequest['has_queue']
if initialstatus == 'Up':
        ledg.on()
        ledr.off()
else:
        ledg.off()
        ledr.on()
print(f'Initial status: {initialstatus}')
print(f'Initial queue: {initialqueue}')

@bot.command(name='status', help='Gets the current server status')
async def manual_status(ctx):
       manualrequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{REALMID}?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
       manualrequest = manualrequest.json()
       manualstatus = manualrequest['status']['name']
       await ctx.send(f'{ctx.author.mention} Current world server status is: {manualstatus}')

@bot.command(name='loveme', help='Loves you not')
async def loveme(ctx):
        await ctx.send(f'{ctx.author.mention} Sorry, I am incapable of love as I am not real.')

@bot.command(name='test', help='Check the bot')
async def test(ctx):
        await ctx.send(f'{ctx.author.mention} I am responding to commands.')

@bot.command(name='queue', help='Check for a login queue')
async def queue(ctx):
        queuecheck = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{REALMID}?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
        queuecheck = queuecheck.json()
        queuestatus = queuecheck['has_queue']
        if queuestatus is False:
                await ctx.send(f'{ctx.author.mention} The server currently does not have a login queue.')
        else:
                await ctx.send(f'{ctx.author.mention} Get ready to wait, the server currently has a login queue.')

@bot.command(name='murkybotselfdestruct', help='stop the bot if it is doing something stupid')
async def murkybotselfdestruct(ctx):
        await ctx.send(f'{ctx.author.mention} MurkyBot has been disabled.')
        await ctx.send(f'<@{USERID}>, MurkyBot has been disabled. Please look for errors and reboot.')
        raise SystemExit

bot.run(TOKEN)
