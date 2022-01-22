from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from utility.utility import get_db_path
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = f'sqlite:///{get_db_path()}'

dbConnection = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
dbSession = sessionmaker(bind=dbConnection)
session = scoped_session(dbSession)
Base = declarative_base()
