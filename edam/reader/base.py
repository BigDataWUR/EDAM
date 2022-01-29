from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from edam.settings import database_url

engine = create_engine(database_url, connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine,
                                         expire_on_commit=False))
Base = declarative_base(bind=engine)

Base.query = db_session.query_property()
