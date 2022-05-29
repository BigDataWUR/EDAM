import os

from edam import database_url
from edam.reader.models.database import recreate_database


def verify_database():
    if database_url.drivername == 'sqlite':
        if not os.path.isfile(database_url.database):
            recreate_database()
