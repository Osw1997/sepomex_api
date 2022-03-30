from flask import Flask
from Scripts import carga_datos_sepomex

from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'cura_deuda_test'
    app.config.from_object('config.Config')


    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'SEPOMEX_API'
        }
    )
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    # Se inicializan las tablas
    carga_datos_sepomex.CargaDatos()

    # Se importan los archivos de rutas
    with app.app_context():
        from sepomex import rutas
        return app