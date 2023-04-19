from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import settings

Model = declarative_base()
Engine = create_engine(settings['db'])
session = sessionmaker(bind=Engine)
Session = session()
