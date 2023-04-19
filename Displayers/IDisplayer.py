from discord import Message, TextChannel, Role, Member
from discord.ext import commands

class IDisplayer:
    async def MessageDeleted(self, message : Message):
        pass
    
    async def MessageEdit(self, message_before : Message, message_after : Message):
        pass

    async def ChanelCreated(self, channel : TextChannel):
        pass

    async def ChanelDeleted(self, channel : TextChannel):
        pass

    async def RoleDelete(self, role : Role):
        pass

    async def RoleCreate(self, role : Role):
        pass

    async def RoleEdit(self, befor : Role, after : Role):
        pass

    async def MemberNicknameUpdated(self, befor : Member, after : Member, entry):
        pass

    async def MemberAddedRole(self, added_role: set[Role], member: Member):
        pass

    async def MemberRemovedRoles(self, removed_role: set[Role], member: Member):
        pass

    async def Clear(self, ctx, cls):
        pass