from database import Session
from discord import Member, Role, Guild

from models import Users, Roles, Servers, UserReputation


def add_new_server(guild: Guild) -> Servers:
    newServer = Servers(server_id=guild.id)
    Session.add(newServer)
    Session.commit()
    for role in guild.roles:
        databaseRole = Session.query(Roles).filter_by(role_id=role.id).one_or_none()
        if databaseRole is None:
            add_new_role(role)
    for member in guild.members:
        databaseMember = Session.query(Users).filter_by(user_id=member.id).one_or_none()
        if databaseMember is None:
            add_new_member(member)

    return newServer


def add_new_role(role: Role) -> Roles:
    role_model = add_role_to_data_base(role)
    add_role_model_to_server(role_model, role.guild.id)
    create_role_relation_ship(role, role_model)
    return role_model


def add_new_member(member: Member) -> Users:
    member_model = add_member_to_data_base(member)
    add_member_model_to_server(member_model, member.guild.id)
    create_member_relation_ship(member, member_model)
    return member_model


def add_role_to_data_base(role: Role) -> Roles:
    newRole = Roles(name=role.name, role_id=role.id)
    Session.add(newRole)
    Session.commit()
    return newRole


def add_member_to_data_base(member: Member) -> Users:
    new_user = Users(name=member.name, user_id=member.id, cash=0)
    Session.add(new_user)
    Session.commit()
    return new_user


def add_reputation_to_member(member: Member, points: int, threshold: int):
    reputation = try_get_reputation(member)
    reputation.reputation += points
    if reputation.reputation >= threshold * reputation.level + 1:
        reputation.level += 1
        reputation.reputation = 0

    Session.commit()


def subtract_reputation_from_member(member: Member, points: int, threshold: int):
    reputation = try_get_reputation(member)
    reputation.reputation -= points
    if reputation.reputation < threshold * reputation.level:
        reputation.level -= 1
        reputation.reputation = 0

    Session.commit()


def try_get_reputation(member: Member) -> UserReputation:
    user = Session.query(Users).filter_by(user_id=member.id).first()
    server = Session.query(Servers).filter_by(server_id=member.guild.id).first()
    reputation = Session.query(UserReputation).filter_by(user_ID=user.ID, server_ID=server.ID).one_or_none()
    if reputation is None:
        reputation = UserReputation(user_ID=user.ID, server_ID=server.ID, reputation=0, level=0)
        user.reputation.append(reputation)
        Session.add(reputation)
    return reputation


def remove_server_role(role: Role):
    role_to_delete = Session.query(Roles).filter_by(role_id=role.id).first()
    for member in role_to_delete.users:
        member.roles.remove(role_to_delete)
    for server in role_to_delete.servers:
        server.roles.remove(role_to_delete)
    Session.delete(role_to_delete)
    Session.commit()


def create_role_relation_ship(role: Role, role_model):
    add_role_model_to_server(role_model, role.guild.id)
    for member in role.members:
        member_model = Session.query(Users).filter_by(user_id=member.id).one_or_none()
        if member_model is None:
            member_model = add_new_member(member)
        member_model.roles.append(role_model)

    Session.commit()


def create_member_relation_ship(member: Member, member_model):
    add_member_model_to_server(member_model, member.guild.id)
    for role in member.roles:
        role_model = Session.query(Roles).filter_by(role_id=role.id).one_or_none()
        if role_model is None:
            role_model = add_new_role(role)

        if role_model not in member_model.roles:
            member_model.roles.append(role_model)

    Session.commit()


def add_member_model_to_server(user_model: Users, server_id):
    server = Session.query(Servers).filter_by(server_id=server_id).one_or_none()
    if server is not None:
        if user_model not in server.users:
            server.users.append(user_model)


def try_add_member_to_server(member: Member):
    server = Session.query(Servers).filter_by(server_id=member.guild.id).one_or_none()
    if server is not None:
        user = Session.query(Users).filter_by(user_id=member.id).one_or_none()
        if user is None:
            user = add_new_member(member)
        server.users.append(user)


def try_remove_member_from_server(member: Member):
    server = Session.query(Servers).filter_by(server_id=member.guild.id).one_or_none()
    if server is not None:
        user = Session.query(Users).filter_by(user_id=member.id).one_or_none()
        if user is not None:
            server.users.remove(user)
            for role in server.roles:
                if role in user.roles:
                    user.roles.remove(role)


def add_role_model_to_server(role_model: Roles, server_id):
    server = Session.query(Servers).filter_by(server_id=server_id).one_or_none()
    if server is not None:
        if role_model not in server.users:
            server.roles.append(role_model)


def try_add_roles_to_member(member: Member, roles: set[Role]):
    user_model = Session.query(Users).filter_by(user_id=member.id).one_or_none()
    if user_model is None:
        user_model = add_new_member(member)
    try_add_roles_to_user_model(user_model, roles)


def try_add_roles_to_user_model(user_model: Users, roles: set[Role]) -> bool:
    if roles:
        for role in roles:
            added_role = Session.query(Roles).filter_by(role_id=role.id).one_or_none()
            if added_role is not None:
                user_model.roles.append(added_role)
        return True
    return False


def try_remove_roles_from_member(user_model: Users, roles: set[Role]) -> bool:
    if roles:
        for role in roles:
            removed_role = Session.query(Roles).filter_by(role_id=role.id).one_or_none()
            if removed_role is not None:
                user_model.roles.remove(removed_role)
        return True
    return False
