import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from edam.settings import database_url

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(database_url)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base(bind=engine)
Base.query = db_session.query_property()


def recreate_database(engine_to_be_created=engine):
    Base.metadata.drop_all(engine_to_be_created)
    Base.metadata.create_all(bind=engine_to_be_created)
