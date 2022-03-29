from flask import Flask
from Scripts import carga_datos_sepomex


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'cura_deuda_test'
    app.config.from_object('config.Config')

    # Se inicializan las tablas
    carga_datos_sepomex.CargaDatos()

    # Se importan los archivos de rutas
    with app.app_context():
        from sepomex import rutas
        return app