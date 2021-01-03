# bot.py
import os
import requests
import discord
import json

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENTID = os.getenv('CLIENT_ID')
CLIENTSECRET = os.getenv('CLIENT_SECRET')

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')
        channel = bot.get_channel(795162312112865280)
        await channel.send('MurkyBot has connected')

def create_access_token(client_id, client_secret, region = 'us'):
        data = { 'grant_type': 'client_credentials' }
        response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
        return response.json()

tokenresponse = create_access_token(CLIENTID, CLIENTSECRET)
accesstoken = tokenresponse["access_token"]
print(accesstoken)

initialrequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/154?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
initialrequest = initialrequest.json()
initialstatus = initialrequest['status']['type']

async def update_status():
        global initialstatus
        await  bot.wait_until_ready()
        channel = bot.get_channel(795162312112865280)
        updaterequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/154?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
        updaterequest = updaterequest.json()
        updatestatus = updaterequest['status']['type']
        if updatestatus != initialstatus:
                await channel.send(f'World server status has changed to: {updatestatus}!')
                initialstatus = updatestatus
                print('Status Change')
        else:
                print('No Change')

while True:
        update_status()
        time.sleep(5)

@bot.command(name='status', help='Gets the current server status')
async def manual_status(ctx):
        manualrequest = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/154?namespace=dynamic-us&locale=en_US&access_token={accesstoken}')
        manualrequest = manualrequest.json()
        manualstatus = manualrequest['status']['type']
        channel = bot.get_channel(795162312112865280)
        await ctx.send(f'Current world server status is: {manualstatus}')

bot.run(TOKEN)
