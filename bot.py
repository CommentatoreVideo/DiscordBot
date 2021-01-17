import os

import discord
from dotenv import load_dotenv
import requests
import re

regexCorsi="!corso (\d+)"

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

client=discord.Client()

@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content=="!ping":
    await message.reply("Pong!")
  elif message.content=="!spoonriver":
    await message.reply("Schifo totale! :face_vomiting:")
  elif message.content=="!corsi":
    testo = ""
    r = requests.get("https://www.umanet.net/api/subjects/")
    elenco=r.json()
    for e in elenco:
      testo+=e['title']+"\n"
    await message.reply(testo)
  elif re.search(regexCorsi,message.content):
    id=re.match(regexCorsi,message.content).group(1)
    r = requests.get("https://www.umanet.net/api/courses/")
    elenco=r.json()
    ris="Corso "
    for corso in elenco:
      if(str(corso['id'])==str(id)):
        ris+=corso['title']+":\n"
        ris+="Paragrafi:\n"
        for modulo in corso['modules']:
          ris+="--"+modulo['title']+"\n"
          if(modulo['description']):
            ris+="----"+modulo['description']+"\n"
    if(ris=="Corso "):
      ris="Il corso non esiste"
    await message.reply(ris);

client.run(TOKEN)