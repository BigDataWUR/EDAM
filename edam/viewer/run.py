from edam.viewer.app.views import app
from edam import SERVER

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])
