import discord
from discord.ext    import commands
import random
import asyncio
import pickle
import os

my_servers_list = []
bot_token = 'INSERTYOURTOKENHERE'

class my_servers():
    def __init__(self,server_id = 0,bodt_enabled = True,en_channel_ids = [],custom_emojis = []):
        self.__server_id = server_id
        self.__bodt_enabled = bodt_enabled
        self.__en_channel_ids = en_channel_ids
        self.__custom_emojis = custom_emojis
        
    def __str__(self):
        return str(self.__server_id)
    
    def getServerID(self):
        return self.__server_id
    
    def getBotEnabled(self):
        return self.__bodt_enabled
    
    def toggleBotEnabled(self):
        self.__bodt_enabled = not self.__bodt_enabled
        print('Toggling:{}'.format(self.__bodt_enabled))
        return
    
    def getChannel(self):
        return self.__en_channel_ids
    
    def addChannel(self,new_id):
        if new_id in self.__en_channel_ids:
            print('Server: %s. Already enabled in this channel.' % self.__server_id)
        else:
            self.__en_channel_ids.append(new_id)
            print('Adding Channel ID: %s' % new_id)
        return
    
    def delChannel(self,old_id):
        if old_id in self.__en_channel_ids:
            self.__en_channel_ids.remove(old_id)
            print('Removing Channel ID: %s' % old_id)
        else:
            print('Server: %s. Already not enabled in this channel.' % self.__server_id)
        return
    
    def getCustom_Emoji(self):
        return self.__custom_emojis
    
    def setCustom_Emoji(self,emoji_list):
        self.__custom_emojis = emoji_list
        
    def addCustom_Emoji(self,emoji):
        if emoji in self.__custom_emojis:
            print('Emoji ID already found.')
        else:
            self.__custom_emojis.append(emoji)
            print('Adding emoji ID: %s in server obj %s' % (emoji,self.__server_id))
        return
    
    def delCustom_Emoji(self,emoji):
        if emoji in self.__custom_emojis:
            self.__custom_emojis.remove(emoji)
            print('Removing emoji ID: %s in server obj %s' % (emoji,self.__server_id))
        else:
            print('Emoji ID not found.')
        return


def findServerIndex(msgServerID):
    count = 0
    for serverdd in my_servers_list:
        if str(msgServerID) == str(serverdd):
            print('findServerIndex: %s server found' % str(msgServerID))
            return count
        elif str(msgServerID) != str(serverdd): 
            count += 1
        if len(my_servers_list)-1 < count:
            print('Server not found!')
            return -1
    return -1
            
####### SAVING DATA ########

def saveServerList():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bot_data','myserverlist.pkl')
    pickle.dump(my_servers_list, open(data_path,"wb"))
    print('Saving my_servers_list!')
    return
    
def loadServerList():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bot_data','myserverlist.pkl')
    global my_servers_list
    
    if os.path.isfile(data_path):
        print('Backup found. Loading...')
        my_servers_list = pickle.load(open(data_path,"rb"))
        print('Current Servers:')
        for srdv in my_servers_list:
            print(srdv)
        return
    else:
        print('Backup not found. Creating new file...')
        pickle.dump(0, open(data_path,"wb"))
    
    
######################## INITIALIZE BOT #################################
bot = commands.Bot(command_prefix='?', description='test')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    try: 
        loadServerList()
        print('my_servers_list succesfully loaded')
    except Exception as e:
        print('ERROR PKL FILE ERROR', e)

######################### CUSTOM DISCORD COMMANDS #########################
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Roll: Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    
@bot.command()
async def Mroll(ctx, dice: str):
    """Rolls a dice M times in MdNdN format."""
    try:
        times, rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Multi Roll: Format has to be in NdNdN!')
        return
    
    for i in range(times):
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

############################## UPVOTE AND DOWNVOTE DISCORD COMMANDS #############################################
@bot.command()
async def setup_server(ctx):
    server_id = ctx.guild.id
    
    if findServerIndex(server_id) < 0: # If server not found in list, create it
        my_servers_list.append(my_servers(server_id))
        print('The current server list is:')
        for serverdd in my_servers_list:
            print(serverdd)
        await ctx.send('Setup finished. run set_emoji_server next.')
    else:
        print('That server is already in here!')
        for serverdd in my_servers_list:
            print(serverdd)
        await ctx.send('ERROR. Server already exists')

@bot.command()
async def set_emoji_server(ctx, *args):
    srvr_indx = findServerIndex(ctx.guild.id)
    print('\n',args)
    newlist = []
    await ctx.send('Adding Emojis:')
    
    for emoj in args:
        newlist.append(emoj)
        await ctx.send(emoj)
    
    my_servers_list[srvr_indx].setCustom_Emoji(newlist)
    saveServerList()
    
@bot.command()
async def toggle(ctx):
    srvr_indx = findServerIndex(ctx.guild.id)
    my_servers_list[srvr_indx].toggleBotEnabled()
    await ctx.send('Toggling:{}'.format(my_servers_list[srvr_indx].getBotEnabled()))
    saveServerList()

@bot.command()
async def listchannel(ctx):
    srvr_indx = findServerIndex(ctx.guild.id)
    for chann in my_servers_list[srvr_indx].getChannel():
        await ctx.send('%s' % chann) 
    saveServerList()

@bot.command()
async def addchannel(ctx):
    srvr_indx = findServerIndex(ctx.guild.id)
    channel_int = ctx.channel.id
    if channel_int in my_servers_list[srvr_indx].getChannel():
        await ctx.send('Already enabled in this channel.')
    else:
        my_servers_list[srvr_indx].addChannel(channel_int)
        print('Adding Channel ID: %s' % channel_int)
        await ctx.send('Enabled in this channel.')
        saveServerList()
    
@bot.command()
async def removechannel(ctx):
    srvr_indx = findServerIndex(ctx.guild.id)
    channel_int = ctx.channel.id
    
    if channel_int in my_servers_list[srvr_indx].getChannel():
        my_servers_list[srvr_indx].delChannel(channel_int)
        print('Removing Channel ID: %s' % channel_int)
        await ctx.send('Disabled in this channel.')
        saveServerList()
    else:
        print('Channel ID not found')
        await ctx.send('Already disabled in this channel.')

################ UPVOTE OR DOWNVOTE MESSAGES LOGIC #############################

@bot.event
async def on_message(message):
    try: 
        srvr_indx = findServerIndex(message.guild.id)
        
        if message.content.startswith('?'):
            pass
        elif message.author == bot.user or my_servers_list[srvr_indx].getBotEnabled() == False:
            return
        elif message.channel.id in my_servers_list[srvr_indx].getChannel():
            print('\nREACTING...')
            guild_emoji_names = [str(guild_emoji) for guild_emoji in message.guild.emojis]
            
            for emoj in my_servers_list[srvr_indx].getCustom_Emoji():
                #print(emoji, guild_emoji_names)
                #print(emoji in guild_emoji_names)
                if emoj in guild_emoji_names:
                    await message.add_reaction(emoj)
    except ValueError as errror:
        print('VALUE ERROR FOUND')
        print(errror)
        
    await bot.process_commands(message)
    

path = os.path.dirname(os.path.abspath(__file__))
print('Running on:', path)


bot.run(bot_token)
