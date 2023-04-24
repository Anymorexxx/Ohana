import discord
from discord.ext.commands import Context

from Extensions.logEmbedCreator import add_date_to_embed
from config import settings, SettingsEnum as Settings_enum
from database import Session
from models import Users, Servers, UserReputation


def add_sender_info_to_embed(embed, ctx) -> discord.Embed:
    embed.add_field(name='Модератор:', value=f'```{ctx.author}```', inline=True)
    embed.add_field(name='ID:', value=f'```fix\n{ctx.author.id}\n```', inline=True)
    return embed


def create_clear_command_embed(cls, ctx, color) -> discord.Embed:
    embed = discord.Embed(description=f'Удалено сообщений: **{cls}**\nВ канале: <#{ctx.channel.id}>',
                          color=color)
    add_date_to_embed(embed)
    add_sender_info_to_embed(embed, ctx)
    return embed


def create_level_command_embed(ctx: Context, color) -> discord.Embed:
    if ctx.guild:
        threshold = settings[Settings_enum.THRESHOLD.value]
        user = Session.query(Users).filter_by(user_id=ctx.author.id).one_or_none()
        server = Session.query(Servers).filter_by(server_id=ctx.guild.id).one_or_none()
        embed = discord.Embed(description=f'Пользователь: {ctx.author}', color=color)
        embed.add_field(name='ID', value=f'```{ctx.author.id}```', inline=True)
        if user and server:
            rep = Session.query(UserReputation).filter_by(user_ID=user.ID,
                                                          server_ID=server.ID).one_or_none()
            if rep:
                embed.add_field(name='Уровень', value=f'```{rep.level}```', inline=True)
                embed.add_field(name='Опыт',
                                value=f'```{threshold * rep.level + rep.reputation} \\ {threshold * (rep.level + 1)}```'
                                , inline=True)

        return embed
