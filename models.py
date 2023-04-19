from sqlalchemy import Column,  Integer, String, ForeignKey, Table
from db import Model
from sqlalchemy.orm import relationship

class UsersRoles(Model):
    __tablename__ = "users_roles"

    ID = Column(Integer,primary_key = True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey('users.ID'))
    role_ID = Column(Integer, ForeignKey('roles.ID'))

class UsersServers(Model):
    __tablename__ = "users_servers"

    ID = Column(Integer, primary_key = True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey('users.ID'))
    server_ID = Column(Integer, ForeignKey('servers.ID'))

class RolesServers(Model):
    __tablename__ = "roles_servers"

    ID = Column(Integer, primary_key = True, autoincrement=True)
    role_ID = Column(Integer, ForeignKey('roles.ID'))
    server_ID = Column(Integer, ForeignKey('servers.ID'))

class Servers(Model):
    __tablename__ = "servers"

    ID = Column(Integer, primary_key = True, autoincrement=True)
    server_id = Column(Integer)
    users = relationship('Users', secondary='users_servers', back_populates="servers")
    roles = relationship("Roles", secondary='roles_servers', back_populates="servers")

class Users(Model):
    __tablename__ = "users"

    ID = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer)
    cash = Column(Integer)
    rep = Column(Integer)
    lvl = Column(Integer)
    servers = relationship('Servers', secondary='users_servers', back_populates="users")
    roles = relationship("Roles", secondary='users_roles', back_populates="users")
    

class Roles(Model):
    __tablename__ = "roles"
    
    ID = Column(Integer,primary_key = True, autoincrement=True)
    role_ID = Column(Integer)
    name = Column(String)
    servers = relationship('Servers', secondary='roles_servers', back_populates="roles")
    users = relationship('Users', secondary='users_roles', back_populates="roles")

# user_roles = Table('users_roles', 
#     Column(Integer, primary_key = True, autoincrement=True),                
#     Column('user_id', Integer, ForeignKey('Users.ID')),
#     Column('role_id', Integer, ForeignKey('oles.ID')))