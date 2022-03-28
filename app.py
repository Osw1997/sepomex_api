from flask import Flask

# Se crea la app
app = Flask(__name__)

# Configuracion del runtime de la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)