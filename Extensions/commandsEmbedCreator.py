import discord

from Extensions.logEmbedCreator import add_date_to_embed


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
