# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN2')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

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

@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return

    # brooklyn_99_quotes = [
    #     'I\'m the human form of the 💯 emoji.',
    #     'Bingpot!',
    #     (
    #         'Cool. Cool cool cool cool cool cool cool, '
    #         'no doubt no doubt no doubt no doubt.'
    #     ),
    # ]
    # print("{0}: {1}".format(message.author, message.content))
    # if len(message.attachments) > 0:
    #     print(message.attachments[0].url)

    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.content == "save":
        messages = await message.channel.history(limit=200).flatten()
        print(messages[0].created_at)
        list_msg = []
        for msg in messages:
            created_at_format = None if msg.created_at == None else msg.created_at.strftime("%Y/%m/%d, %H:%M:%S")
            edited_at_format = None if msg.edited_at == None else msg.edited_at.strftime("%Y/%m/%d, %H:%M:%S")
            tmp = dict(
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
        json_msg = json.dumps(channel_message)
        with open('channel_messages2.json', 'w') as fp:
            json.dump(channel_message, fp)
        print("saved!")
        await message.channel.send(content="saved!")
        # print("test: ",test)
        # print(channel_message["messages"][0])

@client.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",
                    inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",
                    inline=True)
    # channel = client.get_channel(channelid)
    # await channel.send(channel, embed=embed)
    print("before: ", message_before.content)
    print("after: ", message_after.content)

# @client.event
# async def on_message_delete(message):
#     embed = discord.Embed(title="{} deleted a message".format(message.author.name),
#                           description="", color=0xFF0000)
#     embed.add_field(name=message.content, value="This is the message that he has deleted",
#                     inline=True)
#     if len(message.attachments) > 0:
#         if message.content == "":
#             print("deleted: ", message.attachments[0].url)
#         else:
#             print("deleted: ", message.content)
#             print("deleted: ", message.attachments[0].url)
#     else:
#         print("deleted: ", message.content)

client.run(TOKEN)