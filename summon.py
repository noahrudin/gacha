#Import creds and bot hookup
import discord
from discord.ext import commands
import asyncio
import random
import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import requests
from io import BytesIO
#=======
DISCORD_TOKEN = 'NzA1ODY1MjYyODI1NzM0MjI0.Xqx76w.VY9TjtuziQLgJhkXD4Du8qb1K3w'
DISCORD_GUILD = 705865053689086032
client = discord.Client()
gc = gspread.service_account('service_account.json')
pool = gc.open_by_url('https://docs.google.com/spreadsheets/d/1L0yZMFHj68ZjQS-Yxduh8P0f1HYBJNiv_D4KEZQaQ7k/edit?usp=sharing')
bfSheet = pool.get_worksheet(0)
bbSheet = pool.get_worksheet(1)
nbSheet = pool.get_worksheet(2)
NUM_BRONZES = 15
NUM_SILVERS = 48
NUM_NB_GOLDS = 72
NUM_BF_GOLDS = 127
#WIP
#IMG_LIST = []
MULTI_LIST = ['','','','','','','','','','']

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content==('.multi nb'):
        await message.channel.send('Normal Banner multi-summon for {0.name}:'.format(message.author))
        i = 1
        while i < 11:
            randSeed=random.randint(0,99)
            #15% gold, 62% silver, 23% bronze
            if randSeed < 15:
                id1 = 'A'
                name1 = 'B'
                desc1 = 'C'
                star1 = 'D'
                url1 = 'E'
                colorVar = 0x0ffd500
                #want to select a random gold from column list
                randCol = random.randint(1,NUM_NB_GOLDS)
            elif randSeed >=15 and randSeed < 77:
                id1 = 'G'
                name1 = 'H'
                desc1 = 'I'
                star1 = 'J'
                url1 = 'K'
                colorVar = 0xd4d4d4
                randCol = random.randint(1,NUM_SILVERS)
            elif randSeed >= 77:
                id1 = 'M'
                name1 = 'N'
                desc1 = 'O'
                star1 = 'P'
                url1 = 'Q'
                colorVar = 0xad7550
                randCol = random.randint(1,NUM_BRONZES)
            #TODO: Edit embed instead of create new
            stitchedID = str(id1) + str(randCol)
            stitchedName = name1 + str(randCol)
            stitchedDesc = desc1 + str(randCol)
            stitchedURL = url1 + str(randCol)
            stitchedStar =star1 + str(randCol)
            id = nbSheet.acell(stitchedID).value
            name = nbSheet.acell(stitchedName).value
            desc = nbSheet.acell(stitchedDesc).value
            star = nbSheet.acell(stitchedStar).value
            stitchedStarEmoji =  ':star: ' + star
            url = nbSheet.acell(stitchedURL).value
            embed = discord.Embed(title=name, description=desc,color=colorVar)
            embed.set_thumbnail(url=str(url))
            embed.add_field(name="ID", value = id, inline=True)
            #Image Stitching WIP
            #response = requests.get(url)
            #img = Image.open(BytesIO(response.content))
            #IMG_LIST.append(img)
            appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
            MULTI_LIST[i-1] = appendStr
            if i == 1:
                summonMessage = await message.channel.send("Summon " + str(i) + "/10")
                embedMessage = await message.channel.send(embed=embed)
            else:
                await summonMessage.edit(content = "Summon " + str(i) + "/10")
                await embedMessage.edit(embed=embed)
            i += 1
        await asyncio.sleep(1)
        await summonMessage.delete()
        await embedMessage.delete()
        appendedStr = ''
        for x in MULTI_LIST:
            appendedStr += x
            appendedStr += '\n'
        summaryEmbed = discord.Embed(title='Results: ', description = appendedStr, color=0xb52700) 
        await message.channel.send(embed=summaryEmbed)   
        #i = 0
        #while i < 10:
            #if i > 0:
                #stitchedImage = get_concat_h(IMG_LIST[i-1], IMG_LIST[i])
                #i += 1
        #stitchedImage.save('/concat.png')
        #embed = discord.Embed(title='Multi-summon results for {0.name}')
        #embed.set_image(stitchedImage)
        #await message.channel.send(embed=stitchedImage)
    if message.content==('.multi bf'):
        await message.channel.send('Blazing Festival multi-summon for {0.name}:'.format(message.author))
        i = 1
        while i < 11:
            randSeed=random.randint(0,99)
            #15% gold, 62% silver, 23% bronze
            if randSeed < 15:
                id1 = 'A'
                name1 = 'B'
                desc1 = 'C'
                star1 = 'D'
                url1 = 'E'
                colorVar = 0x0ffd500
                #want to select a random gold from column list
                randCol = random.randint(1,NUM_BF_GOLDS)
            elif randSeed >=15 and randSeed < 77:
                id1 = 'G'
                name1 = 'H'
                desc1 = 'I'
                star1 = 'J'
                url1 = 'K'
                colorVar = 0xd4d4d4
                randCol = random.randint(1,NUM_SILVERS)
            elif randSeed >= 77:
                id1 = 'M'
                name1 = 'N'
                desc1 = 'O'
                star1 = 'P'
                url1 = 'Q'
                colorVar = 0xad7550
                randCol = random.randint(1,NUM_BRONZES)
            #TODO: Edit embed instead of create new
            stitchedID = str(id1) + str(randCol)
            stitchedName = name1 + str(randCol)
            stitchedDesc = desc1 + str(randCol)
            stitchedURL = url1 + str(randCol)
            stitchedStar =star1 + str(randCol)
            id = bfSheet.acell(stitchedID).value
            name = bfSheet.acell(stitchedName).value
            desc = bfSheet.acell(stitchedDesc).value
            star = bfSheet.acell(stitchedStar).value
            stitchedStarEmoji =  ':star: ' + star
            url = bfSheet.acell(stitchedURL).value
            embed = discord.Embed(title=name, description=desc,color=colorVar)
            embed.set_thumbnail(url=str(url))
            embed.add_field(name="ID", value = id, inline=True)
            #Image Stitching WIP
            #response = requests.get(url)
            #img = Image.open(BytesIO(response.content))
            #IMG_LIST.append(img)
            appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
            MULTI_LIST[i-1] = appendStr
            if i == 1:
                summonMessage = await message.channel.send("Summon " + str(i) + "/10")
                embedMessage = await message.channel.send(embed=embed)
            else:
                await summonMessage.edit(content = "Summon " + str(i) + "/10")
                await embedMessage.edit(embed=embed)
            i += 1
        await asyncio.sleep(1)
        await summonMessage.delete()
        await embedMessage.delete()
        appendedStr = ''
        for x in MULTI_LIST:
            appendedStr += x
            appendedStr += '\n'
        summaryEmbed = discord.Embed(title='Results: ', description = appendedStr, color=0xb52700) 
        await message.channel.send(embed=summaryEmbed)
    else:
        await message.channel.send(content = "Invalid command! Try \n`.multi nb` for Normal Banner Summons,\n`.multi bf` for Blazing Festival Summons, and \n`.multi bb` for Blazing Bash Summons.")
#async def createImage():
    
async def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)