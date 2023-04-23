import discord

from Extensions.logEmbedCreator import create_message_deleted_embed, create_message_edited_embed, \
    show_moder_updated_role, create_chanel_created_embed, create_chanel_delete_embed, create_role_create_embed, \
    create_role_deleted_embed, create_role_updated_embed, create_member_deleted_roles_embed, \
    create_member_added_roles_embed, create_member_update_nickname_embed
from Loggers.ILogger import ILogger
from discord import Message
from discord.ext import commands
import datetime
from datetime import datetime


class DefaultLogger(ILogger):
    def __init__(self, bot: commands.Bot, chat: int, server: int, moder: int, log: int, color):
        self.bot = bot
        self.chat = chat
        self.moder = moder
        self.server = server
        self.color = color
        self.log = log

    async def message_deleted(self, message: Message):
        embed = create_message_deleted_embed(message, self.color)
        channel = self.bot.get_channel(self.chat)
        await channel.send(embed=embed)

    async def message_edited(self, message_before: Message, message_after: Message):
        embed = create_message_edited_embed(before_message=message_before, after_message=message_after,
                                            color=self.color)
        channel = self.bot.get_channel(self.chat)
        await channel.send(embed=embed)

    async def chanel_created(self, channel):
        embed = create_chanel_created_embed(channel, self.color)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def chanel_deleted(self, channel):
        embed = create_chanel_delete_embed(channel, self.color)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_created(self, role):
        embed = create_role_create_embed(role, self.color)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_deleted(self, role):
        embed = create_role_deleted_embed(role, self.color)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_edited(self, before, after):
        embed = create_role_updated_embed(before, after, self.color)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def member_added_roles(self, added_roles, member):
        added_role = next(role for role in added_roles)
        channel = self.bot.get_channel(self.log)
        embed = await create_member_added_roles_embed(member, added_role, self.color)
        await channel.send(embed=embed)

    async def member_removed_roles(self, removed_roles, member):
        removed_role = next(role for role in removed_roles)
        channel = self.bot.get_channel(self.log)
        embed = await create_member_deleted_roles_embed(member, removed_role, self.color)
        await channel.send(embed=embed)

    async def member_nickname_updated(self, before, after, entry):
        channel = self.bot.get_channel(self.log)
        embed = create_member_update_nickname_embed(before, after, entry)
        await channel.send(embed=embed)
