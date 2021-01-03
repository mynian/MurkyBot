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

client = discord.Client()

@client.event
async def on_ready():
        print(f'{client.user} has connected to Discord!')

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
print(initialstatus)

client.run(TOKEN)
