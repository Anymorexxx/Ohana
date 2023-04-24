import discord
from discord import SelectOption
from discord.ext import commands
from discord.ui import Select

import botAnswer
from Commands.ICommands import ICommands
from Extensions.commandsEmbedCreator import create_clear_command_embed
from config import settings, SettingsEnum as Settings_enum

min_level = settings[Settings_enum.MIN_LEVEL.value]
max_level = settings[Settings_enum.MAX_LEVEL.value] + 1


class FavouriteGameSelect(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Выберите роль")

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)


class MatchView(discord.ui.View):
    roleSelected = None
    level_selected = None

    @discord.ui.select(placeholder="Выберете уровень",
                       options=[SelectOption(label=str(i), value=str(i)) for i in
                                range(min_level, max_level)])
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
        view = MatchView()
        message = await ctx.send(view=view)

        await view.wait()

        results = {
            "a1": view.level_selected,
            "a2": view.roleSelected,
        }
        print(type(results['a2'][0]))
        await ctx.send(f"{results}")
        await message.delete(delay=5)
