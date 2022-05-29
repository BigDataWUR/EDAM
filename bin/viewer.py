from edam.reader.models.database import recreate_database

from edam import SERVER
from edam.viewer.app.views import app
from edam import database_url
import os


def run():
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])


def verify_database():
    if database_url.drivername == 'sqlite':
        if not os.path.isfile(database_url.database):
            recreate_database()


if __name__ == "__main__":
    verify_database()
    run()
