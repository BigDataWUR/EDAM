from edam.viewer.app.views import app
from edam.settings import SERVER


def run():
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])

if __name__ == "__main__":
    run()
