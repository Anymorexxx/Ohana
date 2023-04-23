import discord
from Extensions.logEmbedCreator import add_date_to_embed


def create_member_join_embed(member, invite, color):
    embed = discord.Embed(color=color,
                          description=f"""**{member.mention} || `{member}`\nприсоединяется к серверу.**""")
    embed.add_field(name='> <:linkk:1099388948893151363> Ссылка:',
                    value=f'```{invite.url}```', inline=False)
    embed.add_field(name='> <:linkcreater:1099389532673151087> Создатель:',
                    value=f'```{invite.inviter}```', inline=False)
    embed.add_field(name='> <:freeiconprofiles:1099390379549278328> Кол-во использований:',
                    value=f'```{invite.uses}```', inline=False)
    embed.set_image(url='https://cdn.discordapp.com/attachments/1099403215985979472/1099403612947492985/2GxE5Kn.gif')
    # TODO: поменять стикер на айдишник!
    embed.add_field(name='> <:card:1099711611385692191> ID:',
                    value=f'```{member.id}```', inline=True)
    add_date_to_embed(embed)
    embed.set_thumbnail(url=member.avatar)
    return embed


def create_member_remove_embed(member, color):
    embed = discord.Embed(
        color=color,
        description=f"""**{member.mention} || `{member}` покидает сервер.**""")
    embed.set_image(url='https://cdn.discordapp.com/attachments/1099403215985979472/1099403612947492985/2GxE5Kn.gif')
    # TODO: поменять стикер на айдишник!
    embed.add_field(name='> <:card:1099711611385692191> ID:',
                    value=f'```{member.id}```', inline=True)
    add_date_to_embed(embed)
    embed.set_thumbnail(url=member.avatar)
    return embed
