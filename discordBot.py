import discord #from discord.py
import requests
import magic #from python-magic, specifically python-magic-bin
import io
import sys
import os
#import pickle
import tokenStore

globalVars = {}
globalVars['currentDir'] = ''

#TODO, the bot cant write data to itself in heroku.
# instead ima have to save the config info in a discord channel of sorts.
# actually I wonder if I can write this info into the notes field. on the bot itself
# note's field can hold up to 256 chars.
def writeChanges(obj,dir):
    #f = open(dir,'wb')
    #pickle.dump(obj,f)
    #print(obj)
    #f.close()
    #pickle.dumps(obj).hex()
    
    print(tokenStore.setVal(dir,obj))
    
    
def loadFromFile(dir):
    #f = open(dir,'rb')
    #temp = pickle.load(f)
    #f.close()
    #print(temp)
    #pickle.loads(bytes.fromhex(aHex))
    temp = tokenStore.getVal(dir)
    if(temp is None):
        return {}
    print(temp)
    return temp
    

def processFileFromURL(url,fileName):
    ext = '.bin'
    response = requests.get(url)
    if(response.status_code == 200):
        #actually check if the file is something we recongize.
        test = magic.from_buffer(response.content).split(',')[0]
        if(test == 'JPEG image data'):
            ext = '.jpg'
        elif(test == 'GIF image data'):
            ext = '.gif'
        elif(test == 'PNG image data'):
            ext = '.png'
        elif(test == 'WebM'):
            ext = '.webm'
        elif(test == 'ASCII text'): # this means it just paintext, so we could just msg the whole thing loal.
            ext = '.txt'
        
        # need a case for jfif files. turns out they can work as jpg files?
        
        return discord.File(io.BytesIO(response.content),filename=fileName+ext)
    else:
        return discord.File(io.BytesIO(b''),filename=fileName+ext)
        
def extEquals(x,y):
    return x.lower().split('.')[-1] == y.lower().split('.')[-1]

disClient = discord.Client()
botSettings = {}

try:
    botSettings = loadFromFile('dat')
except:
    pass

@disClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(disClient))
    b = await disClient.application_info()
    print(b.owner)
    a = await disClient.fetch_user(b.owner.id)
    #await a.send("bot active.")

@disClient.event
async def on_message(message):
    print('===MSGBODY===')
    print(message.content)
    print('====FROM=====')
    print(message.author) #very obvious msg spy thingy. you may wana remove this.
    print(message.author.id)
    print('=============')
    if message.author == disClient.user:
        return
    
    isDM = False
    try:
        botSettings[message.guild.id] #message.guild.id is None when its a DM or other.
    except KeyError:
        botSettings[message.guild.id] = {}
        botSettings[message.guild.id]['targetChannel'] = None
        botSettings[message.guild.id]['commandExt'] = '$$$'
        botSettings[message.guild.id]['whitelistedRoles'] = set() #SAVE
        writeChanges(botSettings,'dat')
    except AttributeError:
        isDM = True
    
    scanCommand = False
    try:
        if(not message.author.guild_permissions.administrator): #mystery error, but sometimes the author is a none type. no idea wtf it is.
            compare = set()
            for i in message.author.roles: compare.add(i.id)
            scanCommand = len(botSettings[message.guild.id]['whitelistedRoles'].intersection(compare))>0
        else:
            scanCommand = True
    except AttributeError:
        pass
    
    isChannel = False
    try:
        isChannel = message.channel.id == botSettings[message.guild.id]['targetChannel']
    except AttributeError:
        pass
    
    if(isDM or isChannel): #target channel
        gatheredFiles = []
        for i in message.attachments:
            print(i.url)
            # download file and analyze.
            iFile = processFileFromURL(i.url,str(len(gatheredFiles)))
            if not extEquals(i.url,iFile.filename):
                gatheredFiles.append(iFile)
        if(len(gatheredFiles)>0):
            await message.channel.send('processed files.',files=gatheredFiles)
    
    print("===debug===")
    print(message.channel.id)
    print('===debug===')
    
    if(isChannel):
        if message.content.startswith(botSettings[message.guild.id]['commandExt']+'targetChannelHere') and scanCommand:
            botSettings[message.guild.id]['targetChannel'] = message.channel.id #SAVE
            writeChanges(botSettings,'dat')
            await message.channel.send('channel set to '+ str(message.channel.id))
        
        elif message.content.startswith(botSettings[message.guild.id]['commandExt']+'targetChannel') and scanCommand:
            targ = message.content.split(' ')[1]
            didFail = False
            try:
                botSettings[message.guild.id]['targetChannel'] = int(targ) #SAVE
                writeChanges(botSettings,'dat')
            except:
                didFail = True
            if(didFail):
                await message.channel.send('not a valid integer')
            else:
                await message.channel.send('channel set to '+targ)
                
        elif message.content.startswith(botSettings[message.guild.id]['commandExt']+'setCommandPrefix') and scanCommand:
            targ = message.content.split(' ')[1]
            didFail = False
            try:
                botSettings[message.guild.id]['commandExt'] = targ #SAVE
                writeChanges(botSettings,'dat')
            except:
                didFail = True
            if(didFail):
                await message.channel.send('cant set that ext')
            else:
                await message.channel.send('cmdExt set to '+targ)
        
        elif message.content.startswith(botSettings[message.guild.id]['commandExt']+'setWhitelistedRoles') and scanCommand:
            targ = message.content.split(' ')[1:]
            updatedRoles = set()
            didFail = False
            try:
                for i in targ:
                    updatedRoles.add(int(i))
            except:
                didFail = True
            if(didFail):
                await message.channel.send('not a valid set of role IDs')
            else:
                botSettings[message.guild.id]['whitelistedRoles'] = updatedRoles #SAVE
                writeChanges(botSettings,'dat')
                await message.channel.send('updated roles')

logToken = None
try:
    logToken = sys.argv[1]
except IndexError:
    try:
        logToken = os.environ['BOT_TOKEN']
    except KeyError:
        pass

disClient.run(logToken, bot=True)
# btw, this is NOT the client secret, ya dumb dumb. goto the bot page not the OAuth page.