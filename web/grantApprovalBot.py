import os
from collections import OrderedDict
import discord
from dotenv import load_dotenv
from discord.ext import commands
from airFile import *

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('This bot does not know what to do with this command!')
        
@bot.command(name='approver_add')
async def add_approver(ctx, channelID: str, userID: str):
    
    if ctx.message.channel.type == discord.ChannelType.private:
        # this is a dm
        if ctx.message.author.id == int(superAdminUserID):
            # this is a superadmin DM
            flag = False
            flag = addApprover(channelID, userID, flag)
            if(flag):
                await ctx.send('User has been added as an approver for the Channel')
            else:
                await ctx.send('The user could not be added, please check the Channel ID entered!')
            
    elif ctx.message.channel.type == discord.ChannelType.text:
        # this is a guild/channel message
        print('This is a Channel message, cannot respond to it!')
        
@bot.command(name='channel_add')
async def add_channel(ctx, channelID: str, name: str):
    if ctx.message.channel.type == discord.ChannelType.private:
        # this is a dm
        if ctx.message.author.id == int(superAdminUserID):
            addChannel(channelID, name)
            await ctx.send('Channel added to be monitored!')

@bot.event
async def on_reaction_add(reaction, user):
    reactorID = user.id
    channelID = reaction.message.channel.id
    print(f'channel id = {channelID}, user id = {reactorID}')
    if reaction.emoji == '✅':
        if str(reaction.message.author.id) == grantBotUserID:
            print('message is authored by the bot!')
            if isUserApproved(channelID, reactorID):
                print('user is approvable, grant to be approved!')
                acceptGrant(reaction.message)
                #await reaction.message.channel.send('Grant Approved!')
            else:
                print('User is not in the approving users list!')
            
    elif reaction.emoji == '❌':
        
        if str(reaction.message.author.id) == grantBotUserID:
            print('message is authored by the bot!')
            if isUserApproved(channelID, reactorID):
                print('User is Approvable, grant to be denied!')
                rejectGrant(reaction.message)
                #await reaction.message.channel.send('Grant Denied!')
            else:
                print('User is not in the approving users list!')
    else:
        print('Not a usable emoji! ')
        #await reaction.message.channel.send('not approved!')
        

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(f' message: {message.content} \n channel id: {message.channel.id} \n user ID: {message.author.id}')
    
    if message.channel.type == discord.ChannelType.private:
        # this is a DM
        if message.author.id == int(superAdminUserID):
            #this is a superadmin DM
            print('This is a superadmin DM')

#client.run(token)
bot.run(token)