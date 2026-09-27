from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy knows them
    from models.user import User
    from models.bike import Bike
    from models.booking import Booking

    # Import routes
    from routes.auth import auth_bp
    from routes.bikes import bikes_bp
    from routes.booking import booking_bp
    from routes.admin import admin_bp

    # Register routes
    app.register_blueprint(auth_bp)

    app.register_blueprint(bikes_bp)

    app.register_blueprint(booking_bp)

    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )