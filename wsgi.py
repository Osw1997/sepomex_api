from sepomex import create_app

# Se crea la instancia de la APP
app = create_app()

# Se ajustan los parametros de la APP
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0', port=2222)


# Ejecutar la aplicación: sepomex_ven\Scripts\python.exe wsgi.py
# Activar entorno virtual: .\sepomex_ven\Scripts\activate