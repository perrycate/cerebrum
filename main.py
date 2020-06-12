#!/usr/bin/env python3
import discord
import os
import sys 

from util import Storage

TOKEN_ENV_VAR_NAME = 'NEWTON_BOT_TOKEN'

discord = discord.Client()
db = Storage()

@discord.event
async def on_ready():
    print("Logged in as {0.user}".format(discord))

@discord.event
async def on_message(message):
    # Ignore messages from self, otherwise we'll infinite loop.
    if message.author == discord.user:
        return

    if message.content.startswith('!record'):
        strs = message.content.split(' ')
        if len(strs) < 3:
            # TODO if len == 2 write empty string to storage.
            # This will be our means of "deleting" commands
            return
        command = strs[1]
        content = ' '.join(strs[2:])
        db.save(message.author.name, command, content)
        await message.channel.send("Got it! Will respond to ?{} with '{}'".format(command, content))
        return

    if message.content.startswith('?'):
        # Command is the first word, not including "?".
        command = message.content.split(' ')[0][1:]
        content = db.get(command)
        if content != '':
            await message.channel.send(content)
        return 
   
def _err(str):
    sys.exit(str)
            
def _main():
    # Log in to Discord.
    if TOKEN_ENV_VAR_NAME not in os.environ:
        _err("{0} not found in system environment. Try running again, prefixing '{0}=<insert discord bot token here>'".format(TOKEN_ENV_VAR_NAME))
    auth = os.environ[TOKEN_ENV_VAR_NAME]
    discord.run(auth)


_main()