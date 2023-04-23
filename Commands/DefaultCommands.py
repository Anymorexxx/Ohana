import discord

from Commands.ICommands import ICommands
from discord.ext import commands

from Extensions.commandsEmbedCreator import create_clear_command_embed


class DefaultCommands(ICommands):

    def __init__(self, bot: commands.Bot, moder: int, color):
        self.bot = bot
        self.moder = moder
        self.color = color

    async def clear(self, ctx, cls):
        await ctx.message.delete()
        await ctx.channel.purge(limit=cls)
        channel = self.bot.get_channel(self.moder)
        embed = create_clear_command_embed(ctx, cls, self.color)
        await channel.send(embed=embed)
