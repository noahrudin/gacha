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
import xlrd
#=======
DISCORD_TOKEN = 'NzA1ODY1MjYyODI1NzM0MjI0.Xq0tzw.6kCJDq-SkOUt6dX5uFEIbYrIEzI'
DISCORD_GUILD = 705865053689086032
client = discord.Client()
#gc = gspread.service_account('service_account.json')
#pool = gc.open_by_url('https://docs.google.com/spreadsheets/d/1L0yZMFHj68ZjQS-Yxduh8P0f1HYBJNiv_D4KEZQaQ7k/edit?usp=sharing')
#bfSheet = pool.get_worksheet(0)
#bbSheet = pool.get_worksheet(1)
#nbSheet = pool.get_worksheet(2)
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

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content==('.test'):
        print(str(int(nbSheet.cell_value(0,0))))
        print(str(nbSheet.cell_value(0,1)))
        print(str(nbSheet.cell_value(0,2)))
        print(str(int(nbSheet.cell_value(0,3))))
        print(str(nbSheet.cell_value(0,4)))
    if message.content==('.multi nb'):
        await message.channel.send('Normal Banner multi-summon for {0.name}:'.format(message.author))
        i = 1
        while i < 11:
            randSeed=random.randint(0,99)
            #15% gold, 62% silver, 23% bronze
            if randSeed < 15:
                #id1 = 'A'
                #name1 = 'B'
                #desc1 = 'C'
                #star1 = 'D'
                #url1 = 'E'
                id1 = 0
                name1 = 1
                desc1 = 2
                star1 = 3
                url1 = 4
                colorVar = 0x0ffd500
                #want to select a random gold from column list
                #randCol = random.randint(1,NUM_NB_GOLDS)
                randCol = random.randint(0,NUM_NB_GOLDS-1)
            elif randSeed >=15 and randSeed < 77:
                #id1 = 'G'
                #name1 = 'H'
                #desc1 = 'I'
                #star1 = 'J'
                #url1 = 'K'
                id1 = 6
                name1 = 7
                desc1 = 8
                star1 = 9
                url1 = 10
                colorVar = 0xd4d4d4
                #randCol = random.randint(1,NUM_SILVERS)
                randCol = random.randint(0,NUM_SILVERS-1)
            elif randSeed >= 77:
                #id1 = 'M'
                #name1 = 'N'
                #desc1 = 'O'
                #star1 = 'P'
                #url1 = 'Q'
                id1 = 12
                name1 = 13
                desc1 = 14
                star1 = 15
                url1 = 16
                colorVar = 0xad7550
                #randCol = random.randint(1,NUM_BRONZES)
                randCol = random.randint(0,NUM_BRONZES-1)
            #TODO: Edit embed instead of create new
            #stitchedID = str(id1) + str(randCol)
            #stitchedName = name1 + str(randCol)
            #stitchedDesc = desc1 + str(randCol)
            #stitchedURL = url1 + str(randCol)
            #stitchedStar =star1 + str(randCol)
            #id = nbSheet.acell(stitchedID).value
            id = str(int(nbSheet.cell_value(randCol, id1)))
            #name = nbSheet.acell(stitchedName).value
            name = nbSheet.cell_value(randCol, name1)
            #desc = nbSheet.acell(stitchedDesc).value
            desc = nbSheet.cell_value(randCol, desc1)
            #star = nbSheet.acell(stitchedStar).value
            star = str(int(nbSheet.cell_value(randCol, star1)))
            stitchedStarEmoji =  ':star: ' + star
            #url = nbSheet.acell(stitchedURL).value
            url = nbSheet.cell_value(randCol, url1)
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
                await asyncio.sleep(2)
            else:
                await summonMessage.edit(content = "Summon " + str(i) + "/10")
                await embedMessage.edit(embed=embed)
                await asyncio.sleep(2)
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
            embed = discord.Embed(title=name, description=desc,color=colorVar)
            embed.set_thumbnail(url=str(url))
            embed.add_field(name="ID", value = id, inline=True)
            appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
            MULTI_LIST[i-1] = appendStr
            if i == 1:
                summonMessage = await message.channel.send("Summon " + str(i) + "/10")
                embedMessage = await message.channel.send(embed=embed)
                await asyncio.sleep(2)
            else:
                await summonMessage.edit(content = "Summon " + str(i) + "/10")
                await embedMessage.edit(embed=embed)
                await asyncio.sleep(2)
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
    if message.content==('.multi bb'):
        await message.channel.send('Blazing Bash multi-summon for {0.name}:'.format(message.author))
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
            id = str(int(bbSheet.cell_value(randCol, id1)))
            name = bbSheet.cell_value(randCol, name1)
            desc = bbSheet.cell_value(randCol, desc1)
            star = str(int(bbSheet.cell_value(randCol, star1)))
            stitchedStarEmoji =  ':star: ' + star
            url = bbSheet.cell_value(randCol, url1)
            embed = discord.Embed(title=name, description=desc,color=colorVar)
            embed.set_thumbnail(url=str(url))
            embed.add_field(name="ID", value = id, inline=True)
            appendStr = str(i) + ' - '  +' **' + name + '**- ' + desc + " (" + stitchedStarEmoji + ") "
            MULTI_LIST[i-1] = appendStr
            if i == 1:
                summonMessage = await message.channel.send("Summon " + str(i) + "/10")
                embedMessage = await message.channel.send(embed=embed)
                await asyncio.sleep(2)
            else:
                await summonMessage.edit(content = "Summon " + str(i) + "/10")
                await embedMessage.edit(embed=embed)
                await asyncio.sleep(2)
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