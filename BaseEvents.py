import discord

import botAnswer
import databaseExtensions
import databaseExtensions as Extension
import models
from Reputation.reputation import add_reputation_by_word, add_reputation
from config import settings, SettingsEnum as Settings_enum
from database import Session
from reputation import User

new = (settings[Settings_enum.NEW.value])
color = settings[Settings_enum.COLOR.value]
default_role = settings[Settings_enum.ROLE.value]
creator = settings[Settings_enum.CREATOR.value]
points_by_second = settings[Settings_enum.POINTS_BY_SECOND.value]


class BaseEvents:
    users = {}

    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    async def on_ready(self):
        for guild in self.bot.guilds:
            if Session.query(models.Servers).filter(models.Servers.server_id == guild.id).one_or_none() is None:
                Extension.add_new_server(guild)
            for role in guild.roles:
                if Session.query(models.Roles).filter(models.Roles.role_id == role.id).one_or_none() is None:
                    Extension.add_new_role(role)
            for member in guild.members:
                if Session.query(models.Users).filter(models.Users.user_id == member.id).one_or_none() is None:
                    Extension.add_new_member(member)

        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=(settings[Settings_enum.STATUS.value])))
        print("Работаю каменщиком 3 дня без зарплаты!")
        print(f'Бот: {self.bot.user}')

    async def on_message_delete(self, message):
        await self.logger.message_deleted(message)

    async def on_message_edit(self, message_before, message_after):
        await self.logger.message_edited(message_before, message_after)

    async def on_guild_channel_create(self, channel):
        await self.logger.chanel_created(channel)

    async def on_guild_channel_delete(self, channel):
        await self.logger.chanel_deleted(channel)

    async def on_guild_role_create(self, role):
        print(role, "was created")
        Extension.add_new_role(role)
        await self.logger.role_created(role)

    async def on_guild_role_delete(self, role):
        print(role, "was deleted")
        Extension.remove_server_role(role)
        await self.logger.role_deleted(role)

    async def on_guild_role_update(self, before, after):
        print(before, "was changed to", after)
        await self.logger.role_edited(before, after)

    async def on_member_join(self, member: discord.Member = None):
        print('Пчел присоединяется к серверу.')
        channel = self.bot.get_channel(new)
        guild = member.guild
        invites = await guild.invites()
        invite = invites[len(invites) - 1]
        from Extensions.messageEmbedCreator import create_member_join_embed
        embed = create_member_join_embed(member, invite, color)
        await channel.send(embed=embed)
        role = member.guild.get_role(default_role)
        databaseExtensions.try_add_member_to_server(member)
        await member.add_roles(role)

    async def on_member_remove(self, member: discord.Member = None):
        channel = self.bot.get_channel(new)
        from Extensions.messageEmbedCreator import create_member_remove_embed
        embed = create_member_remove_embed(member, color)
        databaseExtensions.try_remove_member_from_server(member)
        await channel.send(embed=embed)

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        member = Session.query(models.Users).filter(models.Users.user_id == after.id).first()
        await self.try_update_roles(before, after, member)
        await self.member_nickname_update(before, after)

    async def on_message(self, message: discord.Message):
        if message.author is not self.bot.user and message.author.id != creator:
            if message.guild is None:
                await botAnswer.on_message(message, self.bot, creator, color)
            else:
                add_reputation_by_word(message.author, message.content)

        await self.bot.process_commands(message)

    async def member_nickname_update(self, before: discord.Member, after: discord.Member):
        if before.nick != after.nick:
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if entry.target.id == before.id and entry.after.nick == after.nick:
                    await self.logger.member_nickname_updated(before, after, entry)

    async def update_member_roles(self, added_roles: set[discord.Role], removed_roles: set[discord.Role],
                                  member_model: models.Users, after: discord.member):
        if Extension.try_add_roles_to_user_model(member_model, added_roles):
            if len(added_roles) > 0:
                await self.logger.member_added_roles(added_roles, after)
        if Extension.try_remove_roles_from_member(member_model, removed_roles):
            if len(removed_roles) > 0:
                await self.logger.member_removed_roles(removed_roles, after)

    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        if before.channel is None and after.channel is not None:  # пользователь подключился к голосовому каналу
            if member.id not in self.users:
                self.users[member.id] = User(member)
        elif before.channel is not None and after.channel is None:  # пользователь отключился от голосового канала
            if member.id in self.users:
                add_reputation(member, self.users[member.id].get_total_time() * points_by_second)
                del self.users[member.id]
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:  # пользователь переключился на другой голосовой канал
            if member.id in self.users:
                print(f"{member} провел {self.users[member.id].get_total_time()} на канале")

    async def try_update_roles(self, before, after, member):
        if before.roles != after.roles:
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            await self.update_member_roles(added_roles, removed_roles, member, after)
            Session.commit()
