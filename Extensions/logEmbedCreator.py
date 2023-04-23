from datetime import datetime
import discord

def create_message_title_embed(title: str, author, author_id, chanel_id, color) -> discord.Embed:
    embed = discord.Embed(title=title.format(author),
                          description=f"ID пользователя: {author_id}\nВ канале <#{chanel_id}>",
                          color=color)
    return embed


def create_message_title_embed_from_message(title: str, message, color) -> discord.Embed:
    embed = create_message_title_embed(title, message.author, message.author.id, message.channel.id,
                                       color)
    return embed


def create_message_container_field(embed: discord.Embed, content: str) -> discord.Embed:
    embed.add_field(name="Содержимое сообщения.", value=f'```diff\n- {content}\n```', inline=True)
    return embed


def create_message_edited_embed(before_message: discord.Message, after_message: discord.Message, color) \
        -> discord.Embed:
    embed = create_message_title_embed_from_message("Пользователь {} отредактировал сообщение.", after_message, color)
    create_message_container_field(embed, before_message.content)
    embed.add_field(name='Отредактированное сообщение:', value=f'> ```{after_message.content}```', inline=True)
    add_date_to_embed(embed)
    return embed


def create_message_deleted_embed(message: discord.Message, color) -> discord.Embed:
    embed = create_message_title_embed_from_message("Удалено сообщение от пользователя {}", message, color)
    create_message_container_field(embed, message.content)
    add_date_to_embed(embed)
    return embed


def create_channel_role_title_embed(title: str, description, color) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    return embed


def add_channel_info_to_embed(embed, channel) -> discord.Embed:
    embed.add_field(name='Название:', value=f'> ```{channel.name}```', inline=True)
    embed.add_field(name='Категория:', value=f'> ```{channel.category}```', inline=True)
    embed.add_field(name='ID:', value=f'>>> ```fix\n{channel.id}\n```', inline=True)
    return embed


def create_chanel_created_embed(channel, color) -> discord.Embed:
    embed = create_channel_role_title_embed(f"Создан канал. Тип: {channel.type}",
                                            f'Канал создан: {channel.created_at.strftime("%d.%m.%Y %H:%M:%S")}', color)
    add_channel_info_to_embed(embed, channel)
    return embed


def create_chanel_delete_embed(channel, color) -> discord.Embed:
    embed = create_channel_role_title_embed(f"Удалён канал. Тип: {channel.type}",
                                            f'', color)
    add_channel_info_to_embed(embed, channel)
    add_date_to_embed(embed)
    return embed


def create_role_create_embed(role, color) -> discord.Embed:
    embed = create_channel_role_title_embed(f"Создана роль",
                                            description=f'', color=color)
    add_role_info_to_embed(embed, role)
    add_date_to_embed(embed)
    return embed


def create_role_deleted_embed(role, color) -> discord.Embed:
    embed = create_channel_role_title_embed(f"Удалена роль",
                                            description=f'', color=color)
    add_role_info_to_embed(embed, role)
    add_date_to_embed(embed)
    return embed


def add_date_to_embed(embed) -> discord.Embed:
    return embed.add_field(name='Дата:ᅠ ᅠ ᅠ Время:',
                           value=f'```fix\n{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n```',
                           inline=False)


def create_role_updated_embed(before, after, color) -> discord.Embed:
    embed = create_channel_role_title_embed(title=f'Изменена роль',
                                            description=f'', color=color)
    if before.name != after.name:
        embed.add_field(name='Название до:', value=f'> ```{before.name}```', inline=True)
        embed.add_field(name='Название после:', value=f'> ```{after.name}```', inline=True)
    else:
        embed.add_field(name='Название:', value=f'> ```{before.name}```', inline=True)
    embed.add_field(name='ID:', value=f'>>> ```fix\n{before.id}\n```', inline=False)
    embed.add_field(name='', value=f'', inline=False)
    if before.permissions != after.permissions:
        embed.add_field(name='Новые разрешения:', value=f'>>> ```fix\n{after.permissions}\n```', inline=False)
    else:
        embed.add_field(name='Разрешения:', value=f'> ```{after.permissions}```', inline=True)
    add_date_to_embed(embed)
    return embed


def add_role_info_to_embed(embed, role) -> discord.Embed:
    embed.add_field(name='Название:', value=f'> <@&{role.name}>', inline=True)
    embed.add_field(name='Цвет:', value=f'> ```{role.color}```', inline=True)
    embed.add_field(name='ID:', value=f'>>> ```fix\n{role.id}\n```', inline=True)
    embed.add_field(name='Разрешения:', value=f'> ```{role.permissions}```', inline=True)
    return embed


async def show_moder_updated_role(changed_role: discord.Role, embed: discord.Embed, before: discord.Member):
    async for entry in changed_role.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
        if entry.target == before:
            embed.add_field(name='Роль:', value=f'```{changed_role}```', inline=True)
            embed.add_field(name='ID:', value=f'```fix\n{changed_role.id}\n```', inline=True)
            embed.add_field(name='Модератор:', value=f'```{entry.user.name}```', inline=False)


async def create_member_deleted_roles_embed(member, roles, color) -> discord.Embed:
    embed = create_channel_role_title_embed(description=f'В профиле `{member.name}` удалена роль.', color=color,
                                            title=f'')
    await show_moder_updated_role(roles, embed, member)
    add_date_to_embed(embed)
    return embed


async def create_member_added_roles_embed(member, roles, color) -> discord.Embed:
    embed = create_channel_role_title_embed(description=f'В профиле `{member.name}` добавлена роль.', color=color,
                                            title=f'')
    await show_moder_updated_role(roles, embed, member)
    add_date_to_embed(embed)
    return embed


def create_member_update_nickname_embed(before, after, entry, color) -> discord.Embed:
    embed = create_channel_role_title_embed(title=f'', description=f'**Изменён ник.**', color=color)
    discord.Embed(description=f'**Изменён ник.**', color=color)
    embed.add_field(name='ᅠ ᅠ ᅠ', value=f'`{before.nick}` `-->` `{after.nick}`', inline=False)
    embed.add_field(name='Модератор/пользователь', value=f'```{entry.user.name}```', inline=False)
    embed.add_field(name='ID пользователя:', value=f'```fix\n{before.id}\n```', inline=True)
    add_date_to_embed(embed)
    return embed
