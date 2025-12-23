from flask import Flask, jsonify
from marshmallow import ValidationError
from .config import Config
from .extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # errores bonitos
    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return jsonify({"error": "Validación", "details": err.messages}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(err):
        return jsonify({"error": str(err)}), 400

    # rutas
    from .routes.auth import bp as auth_bp
    from .routes.users import bp as users_bp
    from .routes.clients import bp as clients_bp
    from .routes.rooms import bp as rooms_bp
    from .routes.reservations import bp as reservations_bp
    from .routes.payments import bp as payments_bp
    from .routes.expenses import bp as expenses_bp
    from .routes.invoices import bp as invoices_bp
    from .routes.reports import bp as reports_bp
    from .routes.ui import bp as ui_bp

    app.register_blueprint(ui_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(reports_bp)

    @app.get("/")
    def health():
        return {"ok": True, "service": "hotel_api"}, 200

    return app
