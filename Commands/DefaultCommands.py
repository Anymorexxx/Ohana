import discord
from discord import SelectOption
from discord.ext import commands
from discord.ui import Select

import botAnswer
from Commands.ICommands import ICommands
from Extensions.commandsEmbedCreator import create_clear_command_embed, create_level_command_embed
from config import settings, SettingsEnum as Settings_enum
from database import Session
from models import Servers, Roles

min_level: int = settings[Settings_enum.MIN_LEVEL.value]
max_level: int = settings[Settings_enum.MAX_LEVEL.value] + 1


class FavouriteGameSelect(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Выберите роль")

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)


class MatchView(discord.ui.View):
    roleSelected = None
    level_selected = None
    levels: set[int] = {0}

    def __init__(self):
        super().__init__()

    @discord.ui.select(placeholder="Выберете уровень",
                       options=[SelectOption(label=str(i), value=str(i)) for i in range(min_level, max_level)])
    async def level_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.level_selected = select.values[0]
        level_selector: Select = self.children[0]
        level_selector.disabled = True
        level_selector.placeholder = self.level_selected
        game_select = FavouriteGameSelect()
        self.add_item(game_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        self.roleSelected = choices
        self.children[1].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        self.stop()


class DefaultCommands(ICommands):

    def __init__(self, bot: commands.Bot, moder: int, creator, color):
        self.bot = bot
        self.moder = moder
        self.color = color
        self.creator = creator

    async def level(self, ctx, color):
        embed = create_level_command_embed(ctx, color)
        channel = self.bot.get_channel(ctx.channel.id)
        await channel.send(embed=embed)

    async def msg(self, ctx, index: int, text: str):
        if isinstance(ctx.channel, discord.DMChannel) and ctx.message.author.id == self.creator:
            user = self.bot.get_user(index)
            await botAnswer.msg(user, ctx, text, self.color)

    async def clear(self, ctx: commands.Context, cls):
        await ctx.message.delete()
        await ctx.channel.purge(limit=cls)
        channel = self.bot.get_channel(self.moder)
        embed = create_clear_command_embed(ctx, cls, self.color)
        await channel.send(embed=embed)

    async def match(self, ctx: commands.Context):
        if ctx.guild is None:
            return
        levels = {str(i) for i in range(min_level, max_level)}

        server = Session.query(Servers).filter_by(server_id=ctx.guild.id).one_or_none()
        if server is None:
            await ctx.send(f"error no server in DB", delete_after=5)
            return
        for role in server.roles:
            if role.level_match is not None:
                if str(role.level_match) in levels:
                    levels.remove(str(role.level_match))
                    levels.add(str(role.level_match) + "|" + role.name)
        levels.add("None")
        # levels.difference_update(using_levels)
        view = MatchView()
        view.children[0].options = [SelectOption(label=i, value=i) for i in sorted(levels)]
        message = await ctx.send(view=view)

        await view.wait()

        results = {
            1: view.level_selected,
            2: view.roleSelected,
        }
        role = Session.query(Roles).filter_by(role_id=results[2][0].id, server_ID=server.ID).one_or_none()
        level = results[1].split('|')[0]
        level_using_rile = Session.query(Roles).filter_by(server_ID=server.ID, level_match=level).one_or_none()
        if role:
            if level != "None":
                if level_using_rile:
                    await message.edit(content="Уровень используется, у прошлой роли удален уровень", view=None)
                    level_using_rile.level_match = None
                role.level_match = results[1].split('|')[0]
                Session.commit()
            else:
                role.level_match = None
                Session.commit()
        await ctx.send(f"{results}")
        await message.delete(delay=5)
