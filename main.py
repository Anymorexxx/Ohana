import discord
from discord.ext import commands
from Displayers.DefaultDisplayer import DefaultDisplayer
from Displayers.IDisplayer import IDisplayer
from config import settings, SettingsEnum as Settings_enum
from database import Session
import models
import databaseExtensions as Extension

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command('help')

chat = (settings[Settings_enum.CHAT.value])
server = (settings[Settings_enum.SERVER.value])
moder = (settings[Settings_enum.MODER.value])
log = (settings[Settings_enum.LOG.value])
color = settings[Settings_enum.COLOR.value]
displayer: IDisplayer = DefaultDisplayer(bot, chat, server, color, moder, log)


def add_reputation(member: discord.Member, amount: int):
    Extension.add_reputation_to_member(member, amount, settings[Settings_enum.THRESHOLD.value])


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
async def on_member_remove(member: discord.Member = None):
    print(member.name)


@bot.event
async def on_message_delete(message):
    await displayer.message_deleted(message)


@bot.event
async def on_message_edit(message_before, message_after):
    await displayer.message_edited(message_before, message_after)


@bot.event
async def on_guild_channel_create(channel):
    await displayer.chanel_created(channel)


@bot.event
async def on_guild_channel_delete(channel):
    await displayer.chanel_deleted(channel)


@bot.event
async def on_guild_role_create(role):
    print(role, "was created")
    Extension.add_new_role(role)
    await displayer.role_created(role)


@bot.event
async def on_guild_role_delete(role):
    print(role, "was deleted")
    Extension.remove_server_role(role)
    await displayer.role_deleted(role)


@bot.event
async def on_guild_role_update(before, after):
    print(before, "was changed to", after)
    await displayer.role_edited(before, after)


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    member = Session.query(models.Users).filter(models.Users.user_id == after.id).first()
    await try_update_roles(before, after, member)
    await member_nickname_update(before, after)


async def member_nickname_update(before: discord.Member, after: discord.Member):
    if before.nick != after.nick:
        async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if entry.target.id == before.id and entry.after.nick == after.nick:
                await displayer.member_nickname_updated(before, after, entry)


async def try_update_roles(before, after, member):
    if before.roles != after.roles:
        added_roles = set(after.roles) - set(before.roles)
        removed_roles = set(before.roles) - set(after.roles)
        await update_member_roles(added_roles, removed_roles, member, after)
        Session.commit()


async def update_member_roles(added_roles: set[discord.Role], removed_roles: set[discord.Role],
                              member_model: models.Users, after: discord.member):
    if Extension.try_add_roles_to_member(member_model, added_roles):
        added_roles_str = ', '.join(role.name for role in added_roles)
        print(f"{after.name} получил(а) роль(и): {added_roles_str}")
        if len(added_roles) > 0:
            await displayer.member_added_roles(added_roles, after)
    if Extension.try_remove_roles_to_member(member_model, removed_roles):
        removed_roles_str = ', '.join(role.name for role in removed_roles)
        print(f"{after.name} потерял(а) роль(и): {removed_roles_str}")
        if len(removed_roles) > 0:
            await displayer.member_removed_roles(removed_roles, after)


# команды
@bot.command(name='clear')
@commands.has_permissions(view_audit_log=True)
async def clear(ctx, cls=100):
    await ctx.message.delete()
    await ctx.channel.purge(limit=cls)
    await displayer.clear(ctx, cls)


bot.run(settings[Settings_enum.TOKEN.value])
