from abc import ABC, abstractmethod


class ICommands(ABC):
    @abstractmethod
    async def clear(self, ctx, cls):
        pass
