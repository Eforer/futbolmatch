from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configurar la barra de herramientas de depuración
app.debug = False
toolbar = DebugToolbarExtension(app)

from routes import *



if __name__ == '__main__':
    app.run(debug=True)
