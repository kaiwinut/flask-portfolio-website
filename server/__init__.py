import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # Web app configuration
    app = Flask(__name__)
    app.config.from_object('server.config')
    db.init_app(app)

    from server.homepage import homepage
    from server.blogpage import blogpage
    from server.auth import auth
    app.register_blueprint(homepage, url_prefix='/')
    app.register_blueprint(blogpage, url_prefix='/blog')
    app.register_blueprint(auth, url_prefix='/blog')

    # Generate database
    from server.models import User, Comment, Post, Like
    from server.config import DB_NAME
    if not os.path.exists(os.path.join('server', DB_NAME)):
        db.create_all(app=app)
        print('Created database.')

    # Login manager configuration
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

app = create_app()