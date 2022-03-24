# bot.py
import os
import random
from turtle import title
from unicodedata import name
import discord
from dotenv import load_dotenv
import json
from datetime import datetime
import hashlib as hs
from discord import Color as c
import pandas as pd

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

msg_after = None
msg_before = None
msg_deleted = []
attachments_deleted = []
msg_latest = None
log_channel = None
current_msg_id = None
guild_glbl = None
msg_ids = []

@client.event
async def on_ready():
    global log_channel
    
    guild = discord.utils.get(client.guilds, name=GUILD)
    guild_glbl = guild
    log_channel = discord.utils.get(guild.channels, name="log")
    print("All messages will be stored in {} Channel".format(log_channel))

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

def embed_card(event, msg, color=discord.Color.blue()):
    embed = discord.Embed(
        title=event,
        # description=msg,
        color=color,
    )
    if event == "Deleted Message":
        embed.add_field(
            name="Deleted Message ID",
            value=msg.id,
            inline=False
        )
        embed.add_field(
            name="deleted message",
            value="---" if msg.content == "" else msg.content,
            inline=False
        )
        if msg.attachments:
            embed.set_thumbnail(url="{}".format(msg.attachments[0].url))
            embed.add_field(
                name="deleted message attachments id",
                value=msg.attachments[0].id,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments url",
                value=msg.attachments[0].url,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments content type",
                value=msg.attachments[0].content_type,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments file name",
                value=msg.attachments[0].filename,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments height",
                value=msg.attachments[0].height,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments width",
                value=msg.attachments[0].width,
                inline=True
            )
            embed.add_field(
                name="deleted message attachments size",
                value=msg.attachments[0].size,
                inline=True
            )
        embed.add_field(
            name="Author",
            value="{}({})".format(msg.author.name, msg.author.id),
            inline=False
        )
        embed.add_field(
            name="Channel",
            value="{}({})".format(msg.channel.name, msg.channel.id),
            inline=True
        )
        embed.set_footer(
            text="Deleted Time: {}".format(datetime.now()),
        )
    elif event == "Edited Message":
        edited_at_format = None if msg[1].edited_at == None else msg[1].edited_at.strftime("%Y/%m/%d, %H:%M:%S")
        embed.add_field(
            name="Message ID",
            value=msg[0].id,
            inline=False
        )
        embed.add_field(
            name="Before Edited",
            value=msg[0].content,
            inline=True
        )
        embed.add_field(
            name="After Edited",
            value=msg[1].content,
            inline=True
        )
        embed.add_field(
            name="Author",
            value="{}({})".format(msg[0].author.name, msg[0].author.id),
            inline=False
        )
        embed.add_field(
            name="Channel",
            value="{}({})".format(msg[1].channel.name, msg[1].channel.id),
            inline=True
        )
        embed.set_footer(
            text="Edited Time: {}".format(edited_at_format),
        )
    else:
        created_at_format = None if msg.created_at == None else msg.created_at.strftime("%Y/%m/%d, %H:%M:%S")
        embed.add_field(
            name="Message ID",
            value=msg.id,
            inline=False
        )
        embed.add_field(
            name="Content",
            value="---" if msg.content == "" else msg.content,
            inline=False
        )
        if msg.attachments:
            print(msg.attachments[0].url)
            embed.set_thumbnail(url="{}".format(msg.attachments[0].url))
            embed.add_field(
                name="attachments id",
                value=msg.attachments[0].id,
                inline=True
            )
            embed.add_field(
                name="attachments url",
                value=msg.attachments[0].url,
                inline=True
            )
            embed.add_field(
                name="attachments content type",
                value=msg.attachments[0].content_type,
                inline=True
            )
            embed.add_field(
                name="attachments file name",
                value=msg.attachments[0].filename,
                inline=True
            )
            embed.add_field(
                name="attachments height",
                value=msg.attachments[0].height,
                inline=True
            )
            embed.add_field(
                name="attachments width",
                value=msg.attachments[0].width,
                inline=True
            )
            embed.add_field(
                name="attachments size",
                value=msg.attachments[0].size,
                inline=True
            )
        embed.add_field(
            name="Author",
            value="{}({})".format(msg.author.name, msg.author.id),
            inline=False
        )
        embed.add_field(
            name="Channel",
            value="{}({})".format(msg.channel.name, msg.channel.id),
            inline=False
        )
        embed.set_footer(
            text="Time: {}".format(created_at_format),
        )
    return embed

def to_dictionary(msg):
    created_at_format = None if msg.created_at == None else msg.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    edited_at_format = None if msg.edited_at == None else msg.edited_at.strftime("%Y/%m/%d, %H:%M:%S")

    temp = dict(
        activity= msg.activity,
        application= msg.application,
        attachments= [{
            'id': a.id,
            'content_type': a.content_type,
            'filename': a.filename,
            'height': a.height,
            'url': a.url,
            'proxy_url': a.proxy_url,
            'size': a.size,
            'width': a.width
        } for a in msg.attachments],
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

def to_dataframe(msg):
    created_at_format = None if msg.created_at == None else msg.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    edited_at_format = None if msg.edited_at == None else msg.edited_at.strftime("%Y/%m/%d, %H:%M:%S")

    # columns = [
    #             "id", "activity", "application", "content", "created_at", "content_before_edited", "edited_at", "embeds",
    #             "author_id", "author_name", "author_discriminator", "call", "clean_content", "jump_url", "mention_everyone",
    #             "mentions", "nonce", "pinned", "raw_channel_mention", "reactions", "reference", "raw_role_mention", "stickers",
    #             "system_content", "tts", "webhook_id","attachment_id", "attachment_content_type", "attachment_filename",
    #             "attachment_height", "attachment_url", "attachment_proxy_url","attachment_size","attachment_width"
    #         ]

    temp = [
        msg.id,
        msg.activity,
        msg.application,
        msg.content,
        created_at_format,
        None if msg_before == None else msg_before,
        edited_at_format,
        msg.embeds,
        msg.author.id,
        msg.author.name,
        msg.author.discriminator,
        msg.call,
        msg.clean_content,
        msg.jump_url,
        msg.mention_everyone,
        msg.mentions,
        msg.nonce,
        msg.pinned,
        msg.raw_channel_mentions,
        msg.reactions,
        msg.reference,
        msg.raw_role_mentions,
        msg.role_mentions,
        msg.stickers,
        msg.system_content,
        msg.tts,
        msg.webhook_id
    ]

    if msg.attachments:
        a = msg.attachments[0]
        temp.append(a.id),
        temp.append(a.content_type),
        temp.append(a.filename),
        temp.append(a.height),
        temp.append(a.url),
        temp.append(a.proxy_url),
        temp.append(a.size),
        temp.append(a.width),
    else:
        temp.append(None),
        temp.append(None),
        temp.append(None),
        temp.append(None),
        temp.append(None),
        temp.append(None),
        temp.append(None),
        temp.append(None),
    
    return temp

@client.event
async def on_message(message):
    global msg_before
    global msg_deleted
    global msg_latest
    global current_msg_id
    global log_channel
    global msg_ids

    guild = discord.utils.get(client.guilds, name=GUILD)
    print()
    if log_channel == None:
        log_channel = discord.utils.get(guild.channels, name="log")

    if message.channel.name != "log":
    
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

        if message.content == "md5":
            if msg_latest != None:
                if msg_latest.content == "":
                    msg_clear = {
                        'id': msg_latest.attachments[0].id,
                        'content_type': msg_latest.attachments[0].content_type,
                        'filename': msg_latest.attachments[0].filename,
                        'height': msg_latest.attachments[0].height,
                        'url': msg_latest.attachments[0].url,
                        'proxy_url': msg_latest.attachments[0].proxy_url,
                        'size': msg_latest.attachments[0].size,
                        'width': msg_latest.attachments[0].width
                    }
                    msg_clear = json.dumps(msg_clear)
                    result = hs.md5(msg_clear.encode("utf-8")).hexdigest()
                    msg_hash = "MD5 hash of {} : {}".format(msg_latest.attachments[0].filename, result)
                    await message.channel.send(content=msg_hash)
                else:
                    msg_clear = msg_latest.content
                    result = hs.md5(msg_clear.encode("utf-8")).hexdigest()
                    msg_hash = "MD5 hash of {} : {}".format(msg_clear, result)
                    await message.channel.send(content=msg_hash)

        if message.content == "csv":
            print(msg_before)
            messages2 = await message.channel.history(limit=200).flatten()
            print(messages2[0].created_at)
            list_msg2 = []
            list_msg_del = []
            for msg in messages2:
                tmp2 = to_dataframe(msg)
                list_msg2.append(tmp2)
            
            for msg in msg_deleted:
                tmp3 = to_dataframe(msg)
                list_msg_del .append(tmp3)
            
            columns = [
                "id", "activity", "application", "content", "created_at", "content_before_edited", "edited_at", "embeds",
                "author_id", "author_name", "author_discriminator", "call", "clean_content", "jump_url", "mention_everyone",
                "mentions", "nonce", "pinned", "raw_channel_mention", "reactions", "reference", "raw_role_mention", "role_mention", "stickers",
                "system_content", "tts", "webhook_id","attachment_id", "attachment_content_type", "attachment_filename",
                "attachment_height", "attachment_url", "attachment_proxy_url","attachment_size","attachment_width"
            ]

            columns2 = [
                "channel_id", "channel_category_id", "channel_category_name", "channel_guild_name", "channel_name",
                "channel_created_at"
            ]
            
            channel_message2 = [[
                message.channel.id,
                message.channel.category.id,
                message.channel.category.name,
                message.channel.guild.name,
                message.channel.name,
                message.channel.created_at.strftime("%Y/%m/%d, %H:%M:%S"),
            ]]
            print(channel_message2)

            deleted_messages2 = [[
                message.channel.id,
                message.channel.category.id,
                message.channel.category.name,
                message.channel.guild.name,
                message.channel.name,
                message.channel.created_at.strftime("%Y/%m/%d, %H:%M:%S"),
            ]]

            df_hasil = pd.DataFrame(list_msg2, columns=columns)
            df_deleted = pd.DataFrame(list_msg_del, columns=columns)
            df_channel = pd.DataFrame(channel_message2, columns=columns2)
            df_channel_del = pd.DataFrame(deleted_messages2, columns=columns2)

            df_hasil.to_csv("messages.csv", index=False)
            df_deleted.to_csv("deleted_messages.csv", index=False)
            df_channel.to_csv("channel_info.csv", index=False)
            df_channel_del.to_csv("channel_info_messages_deleted.csv", index=False)

            await message.channel.send(content="saved to csv!")

        msg_latest = message

        if message.id not in msg_ids:
            msg_ids.append(message.id)
            log_channel = discord.utils.get(guild.channels, name="log")
            await log_channel.send(embed=embed_card(event="Normal Message",msg=message))

@client.event
async def on_message_edit(message_before, message_after):
    global msg_before
    global msg_after

    guild = discord.utils.get(client.guilds, name=GUILD)
    embed = discord.Embed(title="{} Edited A Message".format(message_before.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",
                    inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",
                    inline=True)

    msg_after = message_after.content
    msg_before = message_before.content
    log_channel = discord.utils.get(guild.channels, name="log")
    await log_channel.send(embed=embed_card(event="Edited Message",msg=[message_before, message_after], color=discord.Color.orange()))
    print("before: ", message_before.content)
    print("after: ", message_after.content)

@client.event
async def on_message_delete(message):
    global msg_deleted
    global attachments_deleted

    guild = discord.utils.get(client.guilds, name=GUILD)
    embed = discord.Embed(title="{} Deleted a message".format(message.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",
                    inline=True)
    
    temp = to_dictionary(message)
    print(type(msg_deleted))
    log_channel = discord.utils.get(guild.channels, name="log")
    await log_channel.send(embed=embed_card(event="Deleted Message",msg=message, color=discord.Color.red()))
    msg_deleted.append(temp)
    print(temp)


client.run(TOKEN)
