from flask import jsonify, request, current_app as app
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from Scripts import consulta_data

user = 'pooe1997@hotmail.com'
pwd = 'hola_22'
users = {
    user: generate_password_hash(pwd)
}
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


# Se carga la instancia que se encarga de llevar a cabo la consulta
reader = consulta_data.Consultor()

@app.route('/query', methods=['GET'])
@auth.login_required
def query():
    tipo = request.args.get('tipo', default=None, type=str)
    if tipo is None:
        return json.dumps({'Error': 'Especifica el tipo de consulta a ejecutar'}), 300, {'ContentType': 'application/json'}
    else:
        if tipo == 'estado':
            estado = request.args.get('estado', default=None, type=str)
            if estado is None:
                return json.dumps({'Error': 'Debes de proveer informacion en "estado"'}), 300, {'ContentType': 'application/json'}
            resultado = reader.from_estado(estado)
            # return json.dumps(resultado), 200, {'ContentType': 'application/json'}
            return jsonify(json.loads(resultado))

        elif tipo == 'municipio':
            municipio = request.args.get('municipio', default=None, type=str)
            if municipio is None:
                return json.dumps({'Error': 'Debes de proveer informacion en "municipio"'}), 300, {'ContentType': 'application/json'}
            resultado = reader.from_municipio(municipio)
            # return json.dumps(resultado), 200, {'ContentType': 'application/json'}
            return jsonify(json.loads(resultado))

        elif tipo == 'colonia':
            colonia = request.args.get('colonia', default=None, type=str)
            if colonia is None:
                return json.dumps({'Error': 'Debes de proveer informacion en "colonia"'}), 300, {'ContentType': 'application/json'}
            resultado = reader.from_colonia(colonia)
            # return json.dumps(resultado), 200, {'ContentType': 'application/json'}
            return jsonify(json.loads(resultado))

        elif tipo == 'cp':
            cp = request.args.get('cp', default=None, type=str)
            if cp is None:
                return json.dumps({'Error': 'Debes de proveer informacion en "cp"'}), 300, {'ContentType': 'application/json'}
            resultado = reader.from_cp(cp)
            # return json.dumps(json.loads(resultado)), 200, {'ContentType': 'application/json'}
            return jsonify(json.loads(resultado))

        else:
            return json.dumps({'Error': 'Especifica el tipo de consulta a ejecutar'}), 300, {'ContentType': 'application/json'}


@app.errorhandler(404)
def recurso_invalido(e):
    return json.dumps({'Mensaje': str(e)}), 404, {'ContentType': 'application/json'}