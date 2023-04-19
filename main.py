import discord
from discord.ext import commands
from Displayers.DefaultDisplayer import DefaultDisplayer
from Displayers.IDisplayer import IDisplayer
from config import settings
from db import Session
import models
import databaseExtensions as de
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command('help')

chat = (settings['chat'])
server = (settings['server'])
moder = (settings['moder'])
log = (settings['log'])
color = settings['color']
displayer : IDisplayer = DefaultDisplayer(bot, chat, server, color, moder, log)

#логи
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if Session.query(models.Servers).filter(models.Servers.server_id == guild.id).one_or_none() is None:
            de.AddNewServer(guild)
        for role in guild.roles:
            if Session.query(models.Roles).filter(models.Roles.role_ID == role.id).one_or_none() is None:
                de.AddNewRole(role)
        for member in guild.members:
            if Session.query(models.Users).filter(models.Users.user_id == member.id).one_or_none() is None:
                de.AddNewMember(member)
            else:
                print(f"member {member} is exists")
   
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(settings['status'])))
    print("Работаю каменщиком 3 дня без зарплаты!")
    print(f'Бот: {bot.user}')

@bot.event
async def on_member_remove (member: discord.Member=None):
    print(member.name)

@bot.event
async def on_message_delete(message):
    await displayer.MessageDeleted(message)

@bot.event
async def on_message_edit(message_before, message_after):
    await displayer.MessageEdit(message_before, message_after)

@bot.event
async def on_guild_channel_create(channel):
    await displayer.ChanelCreated(channel)

@bot.event
async def on_guild_channel_delete(channel):
    await displayer.ChanelDeleted(channel)

@bot.event
async def on_guild_role_create(role):
    print(role, "was created")
    de.AddNewRole(role)
    await displayer.RoleCreate(role)


@bot.event
async def on_guild_role_delete(role):
    print(role, "was deleted")
    de.RemoveRole(role)
    await displayer.RoleDelete(role)

@bot.event
async def on_guild_role_update(before, after):
    print(before, "was changed to", after)
    await displayer.RoleEdit(before, after)

@bot.event
async def on_member_update(before : discord.Member, after : discord.Member):
    member = Session.query(models.Users).filter(models.Users.user_id == after.id).first()
    await TryUpdateRoles(before, after, member)
    await MemberNicknameUpdate(before, after)

async def MemberNicknameUpdate(before : discord.Member, after : discord.Member):
    if before.nick != after.nick:
        async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if entry.target.id == before.id and entry.after.nick == after.nick:
                await displayer.MemberNicknameUpdated(before, after, entry)

async def TryUpdateRoles(before, after, member):
    if before.roles != after.roles:
        added_roles = set(after.roles) - set(before.roles)
        removed_roles = set(before.roles) - set(after.roles)
        await UpdateMemberRoles(added_roles, removed_roles, member, after, before)
        Session.commit()

async def UpdateMemberRoles(added_roles : set[discord.Role], removed_roles : set[discord.Role], member : models.Users, after:discord.member, before):
        if(de.TryAddRoleToMember(member, added_roles)):
            added_roles_str = ', '.join(role.name for role in added_roles)
            print(f"{after.name} получил(а) роль(и): {added_roles_str}")
            if len(added_roles) > 0:
                await displayer.MemberAddedRole(added_roles, after, before)
        if(de.TryRemoveRoleToMember(member, removed_roles)):
            removed_roles_str = ', '.join(role.name for role in removed_roles)
            print(f"{after.name} потерял(а) роль(и): {removed_roles_str}")
            if len(removed_roles) > 0:
                await displayer.MemberRemovedRoles(removed_roles, after, before)


#команды
@bot.command(name = 'clear')
@commands.has_permissions(view_audit_log=True)
async def Clear(ctx, cls=100):
    await ctx.message.delete()
    await ctx.channel.purge(limit=cls)
    await displayer.Clear(ctx, cls)




bot.run(settings['token'])
