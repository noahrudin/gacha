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
#test for github and heroku
DISCORD_TOKEN = 'NzA1ODY1MjYyODI1NzM0MjI0.Xsg'+'AqQ.cbP1IzjrjHID_gnT3_wxJgoi1Xs'
#DISCORD_TOKEN = process.env.BOT_TOKEN
DISCORD_GUILD = 705865053689086032
client = discord.Client()
loc = ('SummonPool.xlsx')
wb = xlrd.open_workbook(loc)
bfSheet = wb.sheet_by_index(0)
bbSheet = wb.sheet_by_index(1)
nbSheet = wb.sheet_by_index(2)
specialSheet = wb.sheet_by_index(3)

NUM_BRONZES = 15
NUM_SILVERS = 48
#shikamaru
NUM_NB_GOLDS = 73
#OT Naru
NUM_BF_GOLDS = 132
NUM_BFS = 57
#rinne v2
NUM_BB_GOLDS = 128
NUM_BBS = 54
#anni 7vs 7vn
NUM_SPECIAL_GOLDS = 74
NUM_SPECIAL = 2
#Used for changing rates
ODDS_BF_GOLD = 15 #default 15
ODDS_BF_SILVER = 62 #default 62
ODDS_BF_BRONZE = 23  #default 23

ODDS_BB_GOLD = 15 #default 15
ODDS_BB_SILVER = 62  #default 62
ODDS_BB_BRONZE = 23 #default 23
#4 featured rn
ODDS_BB_FEATURED = 2 #1% random

ODDS_SPECIAL_GOLD = 15 #default 15
ODDS_SPECIAL_SILVER = 62 #default 62
ODDS_SPECIAL_BRONZE = 23  #default 23
ODDS_SPECIAL_FEATURED = 1

ODDS_NB_GOLD = 15  #default 15
ODDS_NB_SILVER = 62  #default 62
ODDS_NB_BRONZE = 23  #default 23
#WIP
#IMG_LIST = []
MULTI_LIST = ['','','','','','','','','','']
PRINT_LIST = []
LOCK = "unlocked"

async def toggleLock(lock):
    global LOCK
    if LOCK == "unlocked" and lock == "unlocked":
        LOCK = "locked"
    else: LOCK = "unlocked"

@client.event
async def on_message(message):
    #if message.channel.name  == 'summon-simulator' or message.channel.name  == 'private-test':
        ## or message.channel.name  == 'private-test' or message.channel.name  == 'commands'
        # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    lock = LOCK

    if message.content==('=multi nb'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            introMessage = await message.channel.send('Normal Banner multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await nbMulti(author, message)
            await introMessage.delete()
        else:
            waitMessage = await message.channel.send('Please wait for the current multi-summon to complete!')
            await waitMessage.delete(delay = 3)
            return
    
    if message.content==('=multi bf'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            introMessage = await message.channel.send('Blazing Festival multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await bfMulti(author, message)
            await introMessage.delete()
        else:
            waitMessage = await message.channel.send('Please wait for the current multi-summon to complete!')
            await waitMessage.delete(delay = 3)
            return
    
    if message.content==('=multi bb'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            introMessage = await message.channel.send('Blazing Bash multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await bbMulti(author, message)
            await introMessage.delete()
        else:
            waitMessage = await message.channel.send('Please wait for the current multi-summon to complete!')
            await waitMessage.delete(delay = 3)
            return

    if message.content==('=multi special'):
        if LOCK == "unlocked":
            lock = "unlocked"
            await toggleLock(lock)
            lock = "locked"
            introMessage = await message.channel.send('Special 7* multi-summon for {0.name}:'.format(message.author))
            author = str(message.author)
            await specialMulti(author, message)
            await introMessage.delete()
        else:
            waitMessage = await message.channel.send('Please wait for the current multi-summon to complete!')
            await waitMessage.delete(delay = 3)
            return
        
    if message.content==('=help'):
        await message.channel.send(content = "Try \n`=multi nb` for Normal Banner Summons,\n`=multi bf` for Blazing Festival Summons,\n`=multi bb` for Blazing Bash Summons, and\n`=multi special` for 7-star summon.\nOnly one multi at a time!")
    
    if '=' in message.content:
        if message.content!=('=help') and message.content!=('=multi bb') and message.content!=('=multi bf') and message.content!=('=multi nb') and message.content!=('=multi special'):
            await message.channel.send(content = "Incorrect command! Type `=help` for commands.")


@client.event
async def nbMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,(ODDS_NB_GOLD + ODDS_NB_SILVER + ODDS_NB_BRONZE)-1)
        #15% gold, 62% silver, 23% bronze
        if randSeed < ODDS_NB_GOLD:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_NB_GOLDS-1)
        elif randSeed >=ODDS_NB_GOLD and randSeed < (ODDS_NB_SILVER + ODDS_NB_GOLD):
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed  >= (ODDS_NB_SILVER + ODDS_NB_GOLD):
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
    summaryEmbed = discord.Embed(title='Normal Banner results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)

@client.event
async def bfMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,(ODDS_BF_GOLD + ODDS_BF_SILVER + ODDS_BF_BRONZE)-1)
        #15% gold, 62% silver, 23% bronze
        if randSeed < ODDS_BF_GOLD:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_BF_GOLDS-1)
            #select a random bf from the list
            #randCol = random.randint(NUM_BF_GOLDS-NUM_BFS,NUM_BF_GOLDS-1)
        elif randSeed >=ODDS_BF_GOLD and randSeed < (ODDS_BF_SILVER + ODDS_BF_GOLD):
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= (ODDS_BF_SILVER + ODDS_BF_GOLD):
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
    summaryEmbed = discord.Embed(title='Blazing Festival results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)

@client.event
async def bbMulti(author, message):
    i = 1
    while i < 11:
        randSeed=random.randint(0,(ODDS_BB_GOLD + ODDS_BB_SILVER + ODDS_BB_BRONZE)-1)
        #randSeed=random.randint(0,(ODDS_BB_GOLD + ODDS_BB_SILVER + ODDS_BB_BRONZE + ODDS_BB_FEATURED)-1)
        #15% gold, 62% silver, 23% bronze
        #if randSeed <= ODDS_BB_FEATURED:
            #id1 = 0
            #name1 = 1
            #desc1 = 2
            #star1 = 3
            #url1 = 4
            #colorVar = 0x0ffd500
            #randCol = random.randint(73,120)
        #if randSeed < ODDS_BB_GOLD and randSeed > ODDS_BB_FEATURED:
        if randSeed < ODDS_BB_GOLD:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_BB_GOLDS-1)
            #guaranteed BB unit on gold
            #randCol = random.randint(NUM_BB_GOLDS-NUM_BBS,NUM_BB_GOLDS-1)
        elif randSeed >=ODDS_BB_GOLD and randSeed < (ODDS_BB_SILVER + ODDS_BB_GOLD):
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= (ODDS_BB_SILVER + ODDS_BB_GOLD):
            id1 = 12
            name1 = 13
            desc1 = 14
            star1 = 15
            url1 = 16
            colorVar = 0xad7550
            randCol = random.randint(0,NUM_BRONZES-1)
        id = str(int(bbSheet.cell_value(randCol, id1)))
        name = bbSheet.cell_value(randCol, name1)
        #print(name + id)
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
    summaryEmbed = discord.Embed(title='Blazing Bash featured results for ' + author + ": ", description = appendedStr, color=0xb52700) 
    await message.channel.send(embed=summaryEmbed)
    lock = "unlocked"
    await toggleLock(lock)
    
@client.event
async def specialMulti(author, message):
    i = 1
    while i < 11:
        #randSeed=random.randint(0,(ODDS_BB_GOLD + ODDS_BB_SILVER + ODDS_BB_BRONZE)-1)
        randSeed=random.randint(0,(ODDS_SPECIAL_GOLD + ODDS_SPECIAL_SILVER + ODDS_SPECIAL_BRONZE + ODDS_SPECIAL_FEATURED)-1)
        #15% gold, 62% silver, 23% bronze
        if randSeed <= ODDS_SPECIAL_FEATURED:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x4ad8ff
            randCol = random.randint(73,74) #7vn/7vs featured
        if randSeed < ODDS_SPECIAL_GOLD and randSeed > ODDS_SPECIAL_FEATURED:
            id1 = 0
            name1 = 1
            desc1 = 2
            star1 = 3
            url1 = 4
            colorVar = 0x0ffd500
            #want to select a random gold from column list
            randCol = random.randint(0,NUM_SPECIAL_GOLDS-1)
            #guaranteed BB unit on gold
            #randCol = random.randint(NUM_BB_GOLDS-NUM_BBS,NUM_BB_GOLDS-1)
        elif randSeed >=ODDS_SPECIAL_GOLD and randSeed < (ODDS_SPECIAL_SILVER + ODDS_SPECIAL_GOLD):
            id1 = 6
            name1 = 7
            desc1 = 8
            star1 = 9
            url1 = 10
            colorVar = 0xd4d4d4
            randCol = random.randint(0,NUM_SILVERS-1)
        elif randSeed >= (ODDS_SPECIAL_SILVER + ODDS_SPECIAL_GOLD):
            id1 = 12
            name1 = 13
            desc1 = 14
            star1 = 15
            url1 = 16
            colorVar = 0xad7550
            randCol = random.randint(0,NUM_BRONZES-1)
        id = str(int(specialSheet.cell_value(randCol, id1)))
        name = specialSheet.cell_value(randCol, name1)
        desc = specialSheet.cell_value(randCol, desc1)
        star = str(int(specialSheet.cell_value(randCol, star1)))
        stitchedStarEmoji =  ':star: ' + star
        url = specialSheet.cell_value(randCol, url1)
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
    summaryEmbed = discord.Embed(title='Special banner featured results for ' + author + ": ", description = appendedStr, color=0xb52700) 
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