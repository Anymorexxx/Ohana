from discord import Message, TextChannel, Role, Member
from discord.ext import commands


class IDisplayer:
    async def message_deleted(self, message: Message):
        pass

    async def message_edited(self, message_before: Message, message_after: Message):
        pass

    async def chanel_created(self, channel: TextChannel):
        pass

    async def chanel_deleted(self, channel: TextChannel):
        pass

    async def role_deleted(self, role: Role):
        pass

    async def role_created(self, role: Role):
        pass

    async def role_edited(self, before: Role, after: Role):
        pass

    async def member_nickname_updated(self, before: Member, after: Member, entry):
        pass

    async def member_added_roles(self, added_roles: set[Role], member: Member):
        pass

    async def member_removed_roles(self, removed_roles: set[Role], member: Member):
        pass

    async def clear(self, ctx, cls):
        pass
