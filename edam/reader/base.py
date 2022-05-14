from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from edam import database_url

engine = create_engine(database_url, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False,
                       expire_on_commit=True)
session = Session(future=True)
Base = declarative_base(bind=engine)
Base.query = scoped_session(Session).query_property()
