from flask import jsonify, current_app as app
import json

@app.route('/hello', methods=['GET'])
def hello():
    return json.dumps({'test': 2022}), 200, {'ContentType': 'application/json'}

@app.errorhandler(404)
def recurso_invalido(e):
    return json.dumps({'Mensaje': str(e)}), 404, {'ContentType': 'application/json'}