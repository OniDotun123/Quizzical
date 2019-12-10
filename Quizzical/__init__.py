from flask import Flask

from .commands import create_tables
from .extensions import db, login_manager
from .routes.auth import auth
from .routes.main import main

def create_app(config_file='settings.py'):
  app = Flask(__name__)

  app.config.from_pyfile(config_file)

  db.init_app(app)
  
  login_manager.init_app(app)
  
  app.cli.add_command(create_tables)

  app.register_blueprint(main)
  app.register_blueprint(auth)

  #login_manager.login_view=''

  #@login_manager.user.loader
  ##return User.query.get(user_id)

  

  return app