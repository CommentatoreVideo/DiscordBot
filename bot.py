import os

import discord
from dotenv import load_dotenv
import requests
import re
from random import randint as ri

# from keep_alive import keep_alive

def generaGriglia():
  return [[0,0,0],[0,0,0],[0,0,0]]
  
def vincita(griglia):
  if(griglia[0][0]==griglia[0][1] and griglia[0][1]==griglia[0][2] and griglia[0][0]!=0):
    return -1 if griglia[0][0]=="O" else -2
  if(griglia[1][0]==griglia[1][1] and griglia[1][1]==griglia[1][2] and griglia[1][0]!=0):
    return -1 if griglia[1][0]=="O" else -2
  if(griglia[1][0]==griglia[2][1] and griglia[2][1]==griglia[2][2] and griglia[2][0]!=0):
    return -1 if griglia[2][0]=="O" else -2
  if(griglia[0][0]==griglia[1][0] and griglia[1][0]==griglia[2][0] and griglia[0][0]!=0):
    return -1 if griglia[0][0]=="O" else -2
  if(griglia[0][1]==griglia[1][1] and griglia[1][1]==griglia[2][1] and griglia[0][1]!=0):
    return -1 if griglia[0][1]=="O" else -2
  if(griglia[0][2]==griglia[1][2] and griglia[1][2]==griglia[2][2] and griglia[0][2]!=0):
    return -1 if griglia[0][2]=="O" else -2
  if(griglia[0][0]==griglia[1][1] and griglia[1][1]==griglia[2][2] and griglia[0][0]!=0):
    return -1 if griglia[0][0]=="O" else -2
  if(griglia[0][2]==griglia[1][1] and griglia[1][1]==griglia[2][0] and griglia[0][2]!=0):
    return -1 if griglia[0][2]=="O" else -2
  libere=0
  indice=1
  indiceL=1
  for riga in griglia:
    for cella in riga:
      if(cella==0):
        libere+=1
        indiceL=indice
        if(libere>1):
          return 0
  return indiceL
    
    
regexCorsi="!corso (\d+)"
regexTris="!tris (\d)"
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")
  client.griglia=generaGriglia()
  
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
    await message.reply(ris)
  elif re.search(regexTris,message.content):
    stringa=""
    id=re.match(regexTris,message.content).group(1)
    indice=1
    for i in range(len(client.griglia)):
      for j in range(len(client.griglia[i])):
        if str(indice) == str(id):
          if client.griglia[i][j]!=0:
            await message.reply("Posto non disponibile")
            return
          else:
            client.griglia[i][j]="X"
        indice+=1
    fine=vincita(client.griglia)
    if fine>=0:
      ok=False
      while ok==False:
        ok=True
        id=ri(1,10) if fine==0 else fine
        indice=1
        for i in range(len(client.griglia)):
          for j in range(len(client.griglia[i])):
            if str(indice) == str(id):
              if client.griglia[i][j]!=0:
                ok=False
              else:
                client.griglia[i][j]="O"
            indice+=1
    indice=1
    for riga in client.griglia:
      stringa+="|"
      for cella in riga:
        stringa+=str(indice) if cella==0 else cella
        stringa+="|"
        indice+=1
      stringa+="\n-------\n"
    if fine==-1:
      stringa+="Vince il bot"
      client.griglia=generaGriglia()
    elif fine==-2:
      stringa+="Hai vinto"
      client.griglia=generaGriglia()
    await message.reply(stringa)
  elif message.content=="!tris":
    stringa="Ecco la griglia. \n"
    indice=1
    for riga in client.griglia:
      stringa+="|"
      for cella in riga:
        stringa+=str(indice) if cella==0 else cella
        stringa+="|"
        indice+=1
      stringa+="\n-------\n"
    stringa+="Scrivi !tris n, dove n è uno dei numeri rimasti per giocare. Tu sei la X"
    await message.reply(stringa)
  elif message.content=="!tris c":
    print(message.author.id)
    if message.author.id==251003431345455105:
      client.griglia=generaGriglia()
      await message.reply("Griglia resettata")
    else:
      await message.reply("Non hai diritto a resettare la griglia")

# @client.event
# async def on_member_join(member):
#   print("dentro",member)
#   ruolo = discord.utils.get(member.guild.roles, id = 800448300247416832)
#   await member.add_roles(ruolo)

# keep_alive()
client.run(TOKEN)