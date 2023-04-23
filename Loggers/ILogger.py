from discord import Message, Role, Member
from discord.abc import GuildChannel
from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    async def message_deleted(self, message: Message):
        pass

    @abstractmethod
    async def message_edited(self, message_before: Message, message_after: Message):
        pass

    @abstractmethod
    async def chanel_created(self, channel: GuildChannel):
        pass

    @abstractmethod
    async def chanel_deleted(self, channel: GuildChannel):
        pass

    @abstractmethod
    async def role_deleted(self, role: Role):
        pass

    @abstractmethod
    async def role_created(self, role: Role):
        pass

    @abstractmethod
    async def role_edited(self, before: Role, after: Role):
        pass

    @abstractmethod
    async def member_nickname_updated(self, before: Member, after: Member, entry):
        pass

    @abstractmethod
    async def member_added_roles(self, added_roles: set[Role], member: Member):
        pass

    @abstractmethod
    async def member_removed_roles(self, removed_roles: set[Role], member: Member):
        pass
