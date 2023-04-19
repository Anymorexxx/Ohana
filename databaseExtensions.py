from db import Session
from discord import Member, Role, Guild
import models

def AddNewServer(guild : Guild) -> models.Servers:
    newServer = models.Servers(server_id = guild.id)
    Session.add(newServer)
    Session.commit()
    for role in guild.roles:
        databaseRole = Session.query(models.Roles).filter(models.Roles.role_ID == role.id).one_or_none()
        if databaseRole is None:
            databaseRole = AddNewRole(role)
    for member in guild.members:
        databaseMember = Session.query(models.Users).filter(models.Users.user_id == member.id).one_or_none()
        if databaseMember is None:
            databaseMember = AddNewMember(member)

    return newServer

def AddNewRole(role : Role) -> models.Roles:
    dbrole = AddRoleToDataBase(role)
    AddRoleToServer(dbrole, role.guild.id)
    CreateRoleRelationShip(role, dbrole)
    return dbrole

def AddNewMember(member : Member) -> models.Users:
    dbmember = AddMemberToDataBase(member)
    AddMemberToServer(dbmember, member.guild.id)
    CreateMemberRelationShip(member, dbmember)
    return dbmember

def AddRoleToDataBase(role : Role) -> models.Roles:
    newRole = models.Roles(name = role.name, role_ID = role.id)
    Session.add(newRole)
    Session.commit()
    return newRole

def AddMemberToDataBase(member : Member) -> models.Users:
    newUser = models.Users(name = member.name, user_id = member.id, cash = 0, lvl = 0, rep = 0)
    Session.add(newUser)
    Session.commit()
    return newUser

def RemoveServerRole(role : Role):
    roleToDelete = Session.query(models.Roles).filter(models.Roles.role_ID == role.id).first()
    for member in roleToDelete.users:
        member.roles.remove(roleToDelete)
    for server in roleToDelete.servers:
        server.roles.remove(roleToDelete)
    Session.delete(roleToDelete)
    Session.commit()
    
def CreateRoleRelationShip(role : Role, dbrole):
    AddRoleToServer(dbrole, role.guild.id)
    for member in role.members:
        memberid = Session.query(models.Users).filter(models.Users.user_id == member.id).one_or_none()
        if memberid is None:
            memberid = AddNewMember(member)
        memberid.roles.append(dbrole)

    Session.commit()   

def CreateMemberRelationShip(member : Member, dbmember):
    AddMemberToServer(dbmember, member.guild.id)
    for role in member.roles:
        dbrole = Session.query(models.Roles).filter(models.Roles.role_ID == role.id).one_or_none()
        if dbrole is None:
            dbrole = AddNewRole(role)
        dbmember.roles.append(dbrole)

    Session.commit()

def AddMemberToServer(model : models.Users, serverid):
    server = Session.query(models.Servers).filter(models.Servers.server_id == serverid).one_or_none()
    if server is not None:
        server.users.append(model)

def AddRoleToServer(model : models.Roles, serverid):
    server = Session.query(models.Servers).filter(models.Servers.server_id == serverid).one_or_none()
    if server is not None:
        server.roles.append(model)

def TryAddRoleToMember(member : models.Users, roles : set[Role]) -> bool: 
    if roles:
            for role in roles:
                addedRole = Session.query(models.Roles).filter(models.Roles.role_ID == role.id).one_or_none()
                if addedRole is not None:
                    member.roles.append(addedRole)
            return True
    return False

def TryRemoveRoleToMember(member : models.Users, roles : set[Role]) -> bool:
    if roles:
        for role in roles:
            removedRole = Session.query(models.Roles).filter(models.Roles.role_ID == role.id).one_or_none()
            if removedRole is not None:
                member.roles.remove(removedRole)
        return True 
    return False