# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

msg_after = None
msg_before = None
msg_deleted = []
attachments_deleted = []

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

def to_dictionary(msg):
    created_at_format = None if msg.created_at == None else msg.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    edited_at_format = None if msg.edited_at == None else msg.edited_at.strftime("%Y/%m/%d, %H:%M:%S")

    temp = dict(
        activity= msg.activity,
        application= msg.application,
        attachments= [a.url for a in msg.attachments],
        author= dict(
            id=msg.author.id,
            name=msg.author.name,
            discriminator=msg.author.discriminator
        ),
        call= msg.call,
        # channel= msg.channel,
        # channel_mentions= msg.channel,
        clean_content= msg.clean_content,
        content= msg.content,
        created_at= created_at_format,
        content_before_edited = None if msg_before == None else msg_before,
        edited_at= edited_at_format,
        embeds= msg.embeds,
        # flags= msg.flags,
        # guild= msg.guild,
        id= msg.id,
        jump_url= msg.jump_url,
        mention_everyone= msg.mention_everyone,
        mentions= msg.mentions,
        nonce= msg.nonce,
        pinned= msg.pinned,
        raw_channel_mentions= msg.raw_channel_mentions,
        raw_mentions= msg.raw_mentions,
        raw_role_mentions= msg.raw_role_mentions,
        reactions= msg.reactions,
        reference= msg.reference,
        role_mentions= msg.role_mentions,
        stickers= msg.stickers,
        system_content= msg.system_content,
        tts= msg.tts,
        # type= msg.type,
        webhook_id= msg.webhook_id
    )
    return temp

@client.event
async def on_message(message):
    global msg_before
    global msg_deleted

    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.content == "save":
        print(msg_before)
        messages = await message.channel.history(limit=200).flatten()
        print(messages[0].created_at)
        list_msg = []
        for msg in messages:
            tmp = to_dictionary(msg)
            list_msg.append(tmp)
        
        channel_message = {
            "id": message.channel.id,
            "category": {
                "id": message.channel.category.id,
                "name": message.channel.category.name
            },
            "guild": message.channel.guild.name,
            "name": message.channel.name,
            "created_at": message.channel.created_at.strftime("%Y/%m/%d, %H:%M:%S"),
            "messages": [i for i in list_msg]
        }

        deleted_messages = {
            "id": message.channel.id,
            "category": {
                "id": message.channel.category.id,
                "name": message.channel.category.name
            },
            "guild": message.channel.guild.name,
            "name": message.channel.name,
            "created_at": message.channel.created_at.strftime("%Y/%m/%d, %H:%M:%S"),
            "messages": [i for i in msg_deleted]
        }

        json_msg = json.dumps(deleted_messages)
        with open('deleted_messages.json', 'w') as fp:
            json.dump(deleted_messages, fp)
        print("deleted saved!")

        json_msg = json.dumps(channel_message)
        with open('hasil.json', 'w') as fp:
            json.dump(channel_message, fp)
        print("saved!")
        await message.channel.send(content="saved!")
        
        # print(channel_message["messages"][0]["attachments"])
    # print(message.attachments)

@client.event
async def on_message_edit(message_before, message_after):
    global msg_before
    global msg_after
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",
                    inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",
                    inline=True)
    # channel = client.get_channel(channelid)
    # await channel.send(channel, embed=embed)
    msg_after = message_after.content
    msg_before = message_before.content
    print("before: ", message_before.content)
    print("after: ", message_after.content)

@client.event
async def on_message_delete(message):
    global msg_deleted
    global attachments_deleted
    embed = discord.Embed(title="{} deleted a message".format(message.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",
                    inline=True)
    # if len(message.attachments) > 0:
    #     if message.content == "":
    #         attachments_deleted = [a.url for a in message.attachments]
    #         print("deleted: ", message.attachments[0].url)
    #     else:
    #         msg_deleted = message.content
    #         attachments_deleted = [a.url for a in message.attachments]
    #         print("deleted: ", message.content)
    #         print("deleted: ", message.attachments[0].url)
    # else:
    #     msg_deleted = message.content
    #     print("deleted: ", message.content)
    temp = to_dictionary(message)
    print(type(msg_deleted))
    msg_deleted.append(temp)
    print(temp)


client.run(TOKEN)