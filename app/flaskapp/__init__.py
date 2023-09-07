from flask import Flask
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'

# API Config
headers = {'Content-Type': 'application/json'}
apiurl = 'http://10.0.1.19'

from flaskapp.dashboard.routes import dashboardObj
from flaskapp.add.routes import addObj
from flaskapp.update.routes import updateObj

app.register_blueprint(dashboard.routes.dashboardObj)
app.register_blueprint(add.routes.addObj)
app.register_blueprint(update.routes.updateObj)

