import discord
from discord.ext import commands

from BaseEvents import BaseEvents
from Commands.DefaultCommands import DefaultCommands
from Commands.ICommands import ICommands
from Loggers.DefaultLogger import DefaultLogger
from Loggers.ILogger import ILogger
from config import settings, SettingsEnum as Settings_enum

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

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
points_by_second = settings[Settings_enum.POINTS_BY_SECOND.value]
reputation_cooldown = settings[Settings_enum.REPUTATION_COOLDOWN.value]
logger: ILogger = DefaultLogger(bot, chat, server, moder, log, color)
command: ICommands = DefaultCommands(bot, moder, creator, color)

base_events = BaseEvents(bot, logger)


# команды - логи

@bot.event
async def on_ready():
    await base_events.on_ready()


@bot.event
async def on_message_delete(message):
    await base_events.on_message_delete(message)


@bot.event
async def on_message_edit(message_before, message_after):
    await base_events.on_message_edit(message_before, message_after)


@bot.event
async def on_guild_channel_create(channel):
    await base_events.on_guild_channel_create(channel)


@bot.event
async def on_guild_channel_delete(channel):
    await base_events.on_guild_channel_delete(channel)


@bot.event
async def on_guild_role_create(role):
    await base_events.on_guild_role_create(role)


@bot.event
async def on_guild_role_delete(role):
    await base_events.on_guild_role_delete(role)


@bot.event
async def on_guild_role_update(before, after):
    await base_events.on_guild_role_update(before, after)


@bot.event
async def on_member_join(member: discord.Member = None):
    await base_events.on_member_join(member)


@bot.event
async def on_member_remove(member: discord.Member = None):
    await base_events.on_member_remove(member)


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    await base_events.on_member_update(before, after)


@bot.event
async def on_message(message: discord.Message):
    await base_events.on_message(message)


@bot.event
async def on_voice_state_update(member, before, after):
    await base_events.on_voice_state_update(member, before, after)


@bot.command(name='clear')
@commands.has_permissions(view_audit_log=True)
async def clear(ctx, cls=100):
    await command.clear(ctx, cls)


@bot.command(name='msg')
async def msg(ctx, index: int, *, text: str):
    await command.msg(ctx, index, text)


@bot.command(name='match')
async def match(ctx: discord.ext.commands.Context):
    await command.match(ctx)


@bot.command(name='level')
async def level(ctx: discord.ext.commands.Context):
    await command.level(ctx, color)


bot.run(settings[Settings_enum.TOKEN.value])
