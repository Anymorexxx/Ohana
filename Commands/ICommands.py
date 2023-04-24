from abc import ABC, abstractmethod

from discord.ext import commands


class ICommands(ABC):
    @abstractmethod
    async def clear(self, ctx: commands.Context, cls):
        pass

    @abstractmethod
    async def msg(self, ctx, index: int, text: str):
        pass

    @abstractmethod
    async def match(self, ctx):
        pass

    @abstractmethod
    def level(self, ctx, color):
        pass
