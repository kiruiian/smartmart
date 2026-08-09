from flask import Flask
from flask_login import current_user

from .extensions import db, migrate, login_manager
from .models import User, Cart


def create_app():

    app = Flask(__name__)

    # ==========================================
    # LOAD CONFIGURATION
    # ==========================================

    app.config.from_object("config.Config")


    # ==========================================
    # INITIALIZE EXTENSIONS
    # ==========================================

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    # ==========================================
    # LOGIN CONFIGURATION
    # ==========================================

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"


    # ==========================================
    # USER LOADER
    # ==========================================

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )


    # ==========================================
    # CART COUNT
    # ==========================================

    @app.context_processor
    def inject_cart_count():

        cart_count = 0

        # Only calculate the cart count
        # when a user is logged in

        if current_user.is_authenticated:

            cart = Cart.query.filter_by(
                user_id=current_user.id
            ).first()

            if cart:

                cart_count = sum(
                    item.quantity
                    for item in cart.items
                )

        return {
            "cart_count": cart_count
        }


    # ==========================================
    # IMPORT BLUEPRINTS
    # ==========================================

    from .routes import main_bp
    from .auth import auth_bp
    from .admin import admin_bp
    from .customer import customer_bp


    # ==========================================
    # REGISTER BLUEPRINTS
    # ==========================================

    app.register_blueprint(
        main_bp
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        admin_bp
    )

    app.register_blueprint(
        customer_bp
    )


    # ==========================================
    # RETURN APPLICATION
    # ==========================================

    return app