from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import settings, SettingsEnum as Settings_enum

Model = declarative_base()
Engine = create_engine(settings[Settings_enum.DATABASE_LINK.value])
session = sessionmaker(bind=Engine)
Session = session()
