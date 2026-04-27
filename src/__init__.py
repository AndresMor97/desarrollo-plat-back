from flask import Flask
from flask_cors import CORS
from src.models.transaccion_model import db
from src.dtos.transaccion_dto import ma
from src.utils.response_helper import standard_response

from src.routes.transaccion_routes import transaccion_bp
from src.routes.usuario_routes import usuario_bp
from src.routes.categoria_routes import categoria_bp
from src.routes.auth_routes import auth_bp


def create_app():
    """Crea y configura la instancia de la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    ma.init_app(app)

    @app.errorhandler(404)
    def not_found(e):
        return standard_response("El recurso solicitado no existe", None, 404)

    @app.errorhandler(500)
    def server_error(e):
        return standard_response("Error interno del servidor", str(e), 500)

    app.register_blueprint(transaccion_bp, url_prefix='/api')
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(categoria_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app
