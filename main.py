import asyncio

import discord
from discord.ext import commands

import databaseExtensions
from Commands.DefaultCommands import DefaultCommands
from Commands.ICommands import ICommands
from Loggers.DefaultLogger import DefaultLogger
from Loggers.ILogger import ILogger
from config import settings, SettingsEnum as Settings_enum
from database import Session
import models
import databaseExtensions as Extension
from reputation import User

users = {}

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command('help')

chat = (settings[Settings_enum.CHAT.value])
server = (settings[Settings_enum.SERVER.value])
moder = (settings[Settings_enum.MODER.value])
log = (settings[Settings_enum.LOG.value])
new = (settings[Settings_enum.NEW.value])
color = settings[Settings_enum.COLOR.value]
data = settings[Settings_enum.DATA.value]
default_role = settings[Settings_enum.ROLE.value]
creator = settings[Settings_enum.CREATOR.value]
points_by_word = settings[Settings_enum.POINTS_BY_WORD.value]
min_word_size = settings[Settings_enum.MIN_WORD_SIZE.value]
max_word_size = settings[Settings_enum.MAX_WORD_SIZE.value]
points_by_second = settings[Settings_enum.POINTS_BY_SECOND.value]
logger: ILogger = DefaultLogger(bot, chat, server, moder, log, color)
command: ICommands = DefaultCommands(bot, moder, color)


def add_reputation(member: discord.Member, amount: int):
    Extension.add_reputation_to_member(member, amount, settings[Settings_enum.THRESHOLD.value])


def subtract_reputation(member: discord.Member, amount: int):
    Extension.subtract_reputation_from_member(member, amount, settings[Settings_enum.THRESHOLD.value])


# logs
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if Session.query(models.Servers).filter(models.Servers.server_id == guild.id).one_or_none() is None:
            Extension.add_new_server(guild)
        for role in guild.roles:
            if Session.query(models.Roles).filter(models.Roles.role_id == role.id).one_or_none() is None:
                Extension.add_new_role(role)
        for member in guild.members:
            if Session.query(models.Users).filter(models.Users.user_id == member.id).one_or_none() is None:
                Extension.add_new_member(member)
            else:
                print(f"member {member} is exists")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=(settings[Settings_enum.STATUS.value])))
    print("Работаю каменщиком 3 дня без зарплаты!")
    print(f'Бот: {bot.user}')


@bot.event
async def on_message_delete(message):
    await logger.message_deleted(message)


@bot.event
async def on_message_edit(message_before, message_after):
    await logger.message_edited(message_before, message_after)


@bot.event
async def on_guild_channel_create(channel):
    await logger.chanel_created(channel)


@bot.event
async def on_guild_channel_delete(channel):
    await logger.chanel_deleted(channel)


@bot.event
async def on_guild_role_create(role):
    print(role, "was created")
    Extension.add_new_role(role)
    await logger.role_created(role)


@bot.event
async def on_guild_role_delete(role):
    print(role, "was deleted")
    Extension.remove_server_role(role)
    await logger.role_deleted(role)


@bot.event
async def on_guild_role_update(before, after):
    print(before, "was changed to", after)
    await logger.role_edited(before, after)


@bot.event
async def on_member_join(member: discord.Member = None):
    print('Пчел присоединяется к серверу.')
    channel = bot.get_channel(new)
    guild = member.guild
    invites = await guild.invites()
    invite = invites[len(invites) - 1]
    from Extensions.messageEmbedCreator import create_member_join_embed
    embed = create_member_join_embed(member, invite, color)
    await channel.send(embed=embed)
    role = member.guild.get_role(default_role)
    databaseExtensions.try_add_member_to_server(member)
    await member.add_roles(role)


@bot.event
async def on_member_remove(member: discord.Member = None):
    channel = bot.get_channel(new)
    from Extensions.messageEmbedCreator import create_member_remove_embed
    embed = create_member_remove_embed(member, color)
    databaseExtensions.try_remove_member_from_server(member)
    await channel.send(embed=embed)


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    member = Session.query(models.Users).filter(models.Users.user_id == after.id).first()
    await try_update_roles(before, after, member)
    await member_nickname_update(before, after)


async def member_nickname_update(before: discord.Member, after: discord.Member):
    if before.nick != after.nick:
        async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if entry.target.id == before.id and entry.after.nick == after.nick:
                await logger.member_nickname_updated(before, after, entry)


async def try_update_roles(before, after, member):
    if before.roles != after.roles:
        added_roles = set(after.roles) - set(before.roles)
        removed_roles = set(before.roles) - set(after.roles)
        await update_member_roles(added_roles, removed_roles, member, after)
        Session.commit()


async def update_member_roles(added_roles: set[discord.Role], removed_roles: set[discord.Role],
                              member_model: models.Users, after: discord.member):
    if Extension.try_add_roles_to_user_model(member_model, added_roles):
        added_roles_str = ', '.join(role.name for role in added_roles)
        print(f"{after.name} получил(а) роль(и): {added_roles_str}")
        if len(added_roles) > 0:
            await logger.member_added_roles(added_roles, after)
    if Extension.try_remove_roles_from_member(member_model, removed_roles):
        removed_roles_str = ', '.join(role.name for role in removed_roles)
        print(f"{after.name} потерял(а) роль(и): {removed_roles_str}")
        if len(removed_roles) > 0:
            await logger.member_removed_roles(removed_roles, after)


# команды - логи
@bot.command(name='clear')
@commands.has_permissions(view_audit_log=True)
async def clear(ctx, cls=100):
    await command.clear(ctx, cls)


@bot.command(name='msg')
async def msg(ctx, index: int, *, text: str):
    if isinstance(ctx.channel, discord.DMChannel) and ctx.message.author.id == creator:
        user = bot.get_user(index)
        if user:
            embed = discord.Embed(description=f'**Сообщение от <@{ctx.message.author.id}>**', color=color)
            embed.add_field(name='', value=f'```fix\n{text}\n```', inline=False)
            await user.send(embed=embed)
            await ctx.message.author.send(f'**Отправлено {user}**')


@bot.event
async def on_message(message: discord.Message):
    if message.author is not bot.user and message.author.id != creator:
        if message.guild is None:
            if isinstance(message.channel, discord.DMChannel):
                qt = bot.get_user(creator)
                chunks = [message.content[i:i + 1000] for i in range(0, len(message.content), 1000)]
                embed = discord.Embed(description=f'**Сообщение от {message.author.mention}**', color=color)
                for chunk in chunks:
                    embed.add_field(name='', value=f'```fix\n{chunk}\n```', inline=False)
                embed.add_field(name='ID пользователя:', value=f'```fix\n{message.author.id}\n```', inline=True)
                await asyncio.sleep(3)
                await qt.send(embed=embed)

                bot_message = await message.channel.send('Loading…. █[][][][][][][][][] 10%')
                await asyncio.sleep(1)
                await bot_message.edit(content="Loading…. █████[][][][][] 50%")
                await asyncio.sleep(1)
                await bot_message.edit(content="Loading…. ████████[][] 80%")
                await asyncio.sleep(1)
                await bot_message.edit(content="Loading… ██████████████] 99%")
                await asyncio.sleep(1)
                await bot_message.edit(content="*•.¸♡ meow! ♡¸.•*")
                embed = discord.Embed(
                    description=f'```fix\n Ваше сообщение отправлено, ожидайте, скоро на него ответит модератор\n```',
                    color=color)
                await bot_message.edit(embed=embed)

        else:
            await counting_reputation_by_message(message.author, message.content)

    await bot.process_commands(message)


@bot.event
async def counting_reputation_by_message(member, content):
    if member.bot:
        return
    words = content.split(' ')
    points = 0
    for word in words:
        len_word = len(word)
        if min_word_size <= len_word <= max_word_size:
            points += settings[Settings_enum.POINTS_BY_WORD.value]
    if points > 0:
        add_reputation(member, points)


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    if before.channel is None and after.channel is not None:
        # пользователь подключился к голосовому каналу
        if member.id not in users:
            users[member.id] = User(member)
    elif before.channel is not None and after.channel is None:
        # пользователь отключился от голосового канала
        if member.id in users:
            print(f"{member} провел {users[member.id].get_total_time()} на канале")
            add_reputation(member, users[member.id].get_total_time() * points_by_second)
            del users[member.id]
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        # пользователь переключился на другой голосовой канал
        if member.id in users:
            print(f"{member} провел {users[member.id].get_total_time()} на канале")


bot.run(settings[Settings_enum.TOKEN.value])
