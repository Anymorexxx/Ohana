import discord
from Displayers.IDisplayer import IDisplayer
from discord import Message, TextChannel
from discord.ext import commands
import datetime
from datetime import datetime


async def show_moder_updated_role(changed_role: discord.Role, embed: discord.Embed, before: discord.Role):
    async for entry in changed_role.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
        if entry.target == before:
            embed.add_field(name='Роль:', value=f'```{changed_role}```', inline=True)
            embed.add_field(name='ID:', value=f'```fix\n{changed_role.id}\n```', inline=True)
            embed.add_field(name='Модератор:', value=f'```{entry.user.name}```', inline=False)


class DefaultDisplayer(IDisplayer):
    def __init__(self, bot: commands.Bot, chat: int, server: int, color, moder: int, log: int):
        self.bot = bot
        self.chat = chat
        self.moder = moder
        self.server = server
        self.color = color
        self.log = log

    async def message_deleted(self, message: Message):
        embed = discord.Embed(title="Удалено сообщение от пользователя {}".format(message.author),
                              description=f"ID пользователя: {message.author.id}\nВ канале <#{message.channel.id}>",
                              color=self.color)
        embed.add_field(name="Содержимое сообщения.", value=f'```diff\n- {message.content}\n```', inline=True)
        channel = self.bot.get_channel(self.chat)
        await channel.send(embed=embed)

    async def message_edited(self, message_before: Message, message_after: Message):
        embed = discord.Embed(title="Пользователь {} отредактировал сообщение.".format(message_before.author),
                              description=f"ID пользователя: {message_before.author.id}\nВ канале <#{message_before.channel.id}>",
                              color=self.color)
        embed.add_field(name='Сообщение:', value=f'>>> ```diff\n- {message_before.content}\n```', inline=True)
        embed.add_field(name='Отредактированное сообщение:', value=f'> ```{message_after.content}```', inline=True)
        channel = self.bot.get_channel(self.chat)
        await channel.send(embed=embed)

    async def chanel_created(self, channel: TextChannel):
        embed = discord.Embed(title=f"Создан канал. Тип: {channel.type}",
                              description=f'Канал создан: {channel.created_at.strftime("%d.%m.%Y %H:%M:%S")}',
                              color=self.color)
        embed.add_field(name='Название:', value=f'> ```{channel.name}```', inline=True)
        embed.add_field(name='Категория:', value=f'> ```{channel.category}```', inline=True)
        embed.add_field(name='ID:', value=f'>>> ```fix\n{channel.id}\n```', inline=True)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def chanel_deleted(self, channel: TextChannel):
        embed = discord.Embed(title=f"Удалён канал. Тип: {channel.type}",
                              description=f'', color=self.color)
        embed.add_field(name='Название:', value=f'> ```{channel.name}```', inline=True)
        embed.add_field(name='Категория:', value=f'> ```{channel.category}```', inline=True)
        embed.add_field(name='ID:', value=f'>>> ```fix\n{channel.id}\n```', inline=True)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_created(self, role):
        embed = discord.Embed(title=f"Создана роль",
                              description=f'', color=self.color)
        embed.add_field(name='Название:', value=f'> <@&{role.id}>', inline=True)
        # embed.add_field(name='Цвет:',value=f'> ```{role.color}```', inline=True)
        embed.add_field(name='ID:', value=f'>>> ```fix\n{role.id}\n```', inline=True)
        # embed.add_field(name='Разрешения:',value=f'> ```{role.permissions}```', inline=True)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_deleted(self, role):
        embed = discord.Embed(title=f"Удалена роль",
                              description=f'', color=self.color)
        embed.add_field(name='Название:', value=f'> ```{role.name}```', inline=True)
        embed.add_field(name='Цвет:', value=f'> ```{role.color}```', inline=True)
        embed.add_field(name='ID:', value=f'>>> ```fix\n{role.id}\n```', inline=True)
        embed.add_field(name='Разрешения:', value=f'> ```{role.permissions}```', inline=True)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def role_edited(self, before, after):
        embed = discord.Embed(title=f'Изменена роль',
                              description=f'', color=self.color)
        embed.add_field(name='Название до:', value=f'> ```{before.name}```', inline=True)
        embed.add_field(name='Название после:', value=f'> ```{after.name}```', inline=True)
        embed.add_field(name='ID:', value=f'>>> ```fix\n{before.id}\n```', inline=False)
        embed.add_field(name='', value=f'', inline=False)
        embed.add_field(name='Новые разрешения:', value=f'>>> ```fix\n{after.permissions}\n```', inline=False)
        channel = self.bot.get_channel(self.server)
        await channel.send(embed=embed)

    async def clear(self, ctx, cls):
        channel = self.bot.get_channel(self.moder)
        embed = discord.Embed(description=f'Удалено сообщений: **{cls}**\nВ канале: <#{ctx.channel.id}>',
                              color=self.color)
        embed.add_field(name='Дата:ᅠ ᅠ ᅠ Время:', value=f'```fix\n{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n```',
                        inline=False)
        embed.add_field(name='Модератор:', value=f'```{ctx.author}```', inline=True)
        embed.add_field(name='ID:', value=f'```fix\n{ctx.author.id}\n```', inline=True)
        await channel.send(embed=embed)

    async def member_added_roles(self, added_roles, member):
        added_role = next(role for role in added_roles)
        channel = self.bot.get_channel(self.log)
        embed = discord.Embed(description=f'В профиль `{member.name}` добавлена роль.', color=self.color)
        await show_moder_updated_role(added_role, embed, member)
        embed.add_field(name='Дата:ᅠ ᅠ ᅠ Время:', value=f'```fix\n{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n```',
                        inline=False)
        await channel.send(embed=embed)

    async def member_removed_roles(self, removed_roles, member):
        removed_role = next(role for role in removed_roles)
        channel = self.bot.get_channel(self.log)
        embed = discord.Embed(description=f'В профиле `{member.name}` удалена роль.', color=self.color)
        await show_moder_updated_role(removed_role, embed, member)
        embed.add_field(name='Дата:ᅠ ᅠ ᅠ Время:', value=f'```fix\n{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n```',
                        inline=False)
        await channel.send(embed=embed)

    async def member_nickname_updated(self, before, after, entry):
        channel = self.bot.get_channel(self.log)
        embed = discord.Embed(description=f'**Изменён ник.**', color=self.color)
        embed.add_field(name='ᅠ ᅠ ᅠ', value=f'`{before.nick}` `-->` `{after.nick}`', inline=False)
        embed.add_field(name='Модератор/пользователь', value=f'```{entry.user.name}```', inline=False)
        embed.add_field(name='ID пользователя:', value=f'```fix\n{before.id}\n```', inline=True)
        embed.add_field(name='Дата:ᅠ ᅠ ᅠᅠ Время:', value=f'```fix\n{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n```',
                        inline=False)
        await channel.send(embed=embed)
