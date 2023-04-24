from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Model


class UsersRoles(Model):
    __tablename__ = "users_roles"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey('users.ID', ondelete='CASCADE'))
    role_ID = Column(Integer, ForeignKey('roles.ID', ondelete='CASCADE'))


class UsersServers(Model):
    __tablename__ = "users_servers"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey('users.ID', ondelete='CASCADE'))
    server_ID = Column(Integer, ForeignKey('servers.ID', ondelete='CASCADE'))


# class RolesServers(Model):
#    __tablename__ = "roles_servers"
#
#    ID = Column(Integer, primary_key=True, autoincrement=True)
#    role_ID = Column(Integer, ForeignKey('roles.ID', ondelete='CASCADE'))
#    server_ID = Column(Integer, ForeignKey('servers.ID', ondelete='CASCADE'))


class UserReputation(Model):
    __tablename__ = "user_reputation"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey('users.ID', ondelete='CASCADE'))
    server_ID = Column(Integer, ForeignKey('servers.ID', ondelete='CASCADE'))
    reputation = Column(Integer)
    level = Column(Integer)


class Servers(Model):
    __tablename__ = "servers"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer)
    users = relationship('Users', secondary='users_servers', back_populates="servers")
    #roles = relationship("Roles", secondary='roles_servers', back_populates="servers")
    roles = relationship("Roles", backref="server")


class Users(Model):
    __tablename__ = "users"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer)
    cash = Column(Integer)
    servers = relationship('Servers', secondary='users_servers', back_populates="users")
    roles = relationship("Roles", secondary='users_roles', back_populates="users")
    reputation = relationship("UserReputation", backref="user")


class Roles(Model):
    __tablename__ = "roles"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer)
    name = Column(String)
    level_match = Column(Integer)
    # servers = relationship('Servers', secondary='roles_servers', back_populates="roles")
    server_ID = Column(Integer, ForeignKey('servers.ID', ondelete='CASCADE'))
    users = relationship('Users', secondary='users_roles', back_populates="roles")

# user_roles = Table('users_roles',
#     Column(Integer, primary_key = True, autoincrement=True),                
#     Column('user_id', Integer, ForeignKey('Users.ID')),
#     Column('role_id', Integer, ForeignKey('oles.ID')))
