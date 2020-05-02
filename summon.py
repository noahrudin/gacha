#Bot hookup
import discord
from discord.ext import commands
import asyncio
import random
from threading import Lock
#Only need if we move back to Google Sheets
import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials
#
from PIL import Image
import requests
from io import BytesIO
import xlrd
#=======
DISCORD_TOKEN = 'NzA1ODY1MjYyODI1NzM0MjI0.Xq3JkQ.wFsyhCOFu_pGBo90SEesr3j0bRg'
DISCORD_GUILD = 705865053689086032
client = discord.Client()
loc = ('SummonPool.xlsx')
wb = xlrd.open_workbook(loc)
bfSheet = wb.sheet_by_index(0)
bbSheet = wb.sheet_by_index(1)
nbSheet = wb.sheet_by_index(2)
NUM_BRONZES = 15
NUM_SILVERS = 48
NUM_NB_GOLDS = 72
NUM_BF_GOLDS = 127
NUM_BB_GOLDS = 120
#WIP
#IMG_LIST = []
MULTI_LIST = ['','','','','','','','','','']
PRINT_LIST = []
#lock = Lock()
LOCK = "unlocked"

async def toggleLock(lock):
    global LOCK
    if LOCK == "unlocked" and lock == "unlocked":
        LOCK = "locked"
    else: LOCK = "unlocked"

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    lock = LOCK
    if message.content==('.test'):
        print(str(int(nbSheet.cell_value(0,0))))
        print(str(nbSheet.cell_value(0,1)))
        print(str(nbSheet.cell_value(0,2)))
        print(str(int(nbSheet.cell_value(0,3))))
        print(str(nbSheet.cell_value(0,4)))

    if message.content==('.multi nb'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            await message.channel.send('Normal Banner multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await nbMulti(author, message)
        else:
            await message.channel.send('Please wait for the current multi-summon to complete!')
            return
    
    if message.content==('.multi bf'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            await message.channel.send('Blazing Festival multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await bfMulti(author, message)
        else:
            await message.channel.send('Please wait for the current multi-summon to complete!')
            return
    
    if message.content==('.multi bb'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            await message.channel.send('Blazing Bash multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await bbMulti(author, message)
        else:
            await message.channel.send('Please wait for the current multi-summon to complete!')
            return
        
    if message.content==('.help'):
        await message.channel.send(content = "Try \n`.multi nb` for Normal Banner Summons,\n`.multi bf` for Blazing Festival Summons, and \n`.multi bb` for Blazing Bash Summons. \nOnly one multi at a time!")

@client.event
async def nbMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,99)
        #15% gold, 62% silver, 23% bronze
        if randSeed < 15:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_NB_GOLDS-1)
        elif randSeed >=15 and randSeed < 77:
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= 77:
            id1 = 12
            name1 = 13
            desc1 = 14
            star1 = 15
            url1 = 16
            colorVar = 0xad7550
            randCol = random.randint(0,NUM_BRONZES-1)
        id = str(int(nbSheet.cell_value(randCol, id1)))
        name = nbSheet.cell_value(randCol, name1)
        desc = nbSheet.cell_value(randCol, desc1)
        star = str(int(nbSheet.cell_value(randCol, star1)))
        stitchedStarEmoji =  ':star: ' + star
        url = nbSheet.cell_value(randCol, url1)
        summonCount = "Summon " + str(i) + "/10"
        embed = discord.Embed(title=name, description=desc,color=colorVar)
        embed.set_thumbnail(url=str(url))
        embed.add_field(name="ID", value = id, inline=True)
        embed.add_field(name=summonCount, value = author, inline=True)
        appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
        MULTI_LIST[i-1] = appendStr
        if i == 1:
            embedMessage = await message.channel.send(embed=embed)
            await asyncio.sleep(1)
        else:
            await embedMessage.edit(embed=embed)
            await asyncio.sleep(1)
        i += 1
    await embedMessage.delete()
    appendedStr = ''
    for x in MULTI_LIST:
        appendedStr += x
        appendedStr += '\n'
    summaryEmbed = discord.Embed(title='Results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)
  
@client.event
async def bfMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,99)
        #15% gold, 62% silver, 23% bronze
        if randSeed < 15:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_BF_GOLDS-1)
        elif randSeed >=15 and randSeed < 77:
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= 77:
            id1 = 12
            name1 = 13
            desc1 = 14
            star1 = 15
            url1 = 16
            colorVar = 0xad7550
            randCol = random.randint(0,NUM_BRONZES-1)
        id = str(int(bfSheet.cell_value(randCol, id1)))
        name = bfSheet.cell_value(randCol, name1)
        desc = bfSheet.cell_value(randCol, desc1)
        star = str(int(bfSheet.cell_value(randCol, star1)))
        stitchedStarEmoji =  ':star: ' + star
        url = bfSheet.cell_value(randCol, url1)
        summonCount = "Summon " + str(i) + "/10"
        embed = discord.Embed(title=name, description=desc,color=colorVar)
        embed.set_thumbnail(url=str(url))
        embed.add_field(name="ID", value = id, inline=True)
        embed.add_field(name=summonCount, value = author, inline=True)
        appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
        MULTI_LIST[i-1] = appendStr
        if i == 1:
            embedMessage = await message.channel.send(embed=embed)
            await asyncio.sleep(1)
        else:
            await embedMessage.edit(embed=embed)
            await asyncio.sleep(1)
        i += 1
    await embedMessage.delete()
    appendedStr = ''
    for x in MULTI_LIST:
        appendedStr += x
        appendedStr += '\n'
    summaryEmbed = discord.Embed(title='Results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)
  
@client.event
async def bbMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,99)
        #15% gold, 62% silver, 23% bronze
        if randSeed < 15:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_BB_GOLDS-1)
        elif randSeed >=15 and randSeed < 77:
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= 77:
            id1 = 12
            name1 = 13
            desc1 = 14
            star1 = 15
            url1 = 16
            colorVar = 0xad7550
            randCol = random.randint(0,NUM_BRONZES-1)
        id = str(int(bbSheet.cell_value(randCol, id1)))
        name = bbSheet.cell_value(randCol, name1)
        desc = bbSheet.cell_value(randCol, desc1)
        star = str(int(bbSheet.cell_value(randCol, star1)))
        stitchedStarEmoji =  ':star: ' + star
        url = bbSheet.cell_value(randCol, url1)
        summonCount = "Summon " + str(i) + "/10"
        embed = discord.Embed(title=name, description=desc,color=colorVar)
        embed.set_thumbnail(url=str(url))
        embed.add_field(name="ID", value = id, inline=True)
        embed.add_field(name=summonCount, value = author, inline=True)
        appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
        MULTI_LIST[i-1] = appendStr
        if i == 1:
            embedMessage = await message.channel.send(embed=embed)
            await asyncio.sleep(1)
        else:
            await embedMessage.edit(embed=embed)
            await asyncio.sleep(1)
        i += 1
    await embedMessage.delete()
    appendedStr = ''
    for x in MULTI_LIST:
        appendedStr += x
        appendedStr += '\n'
    summaryEmbed = discord.Embed(title='Results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)
    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)