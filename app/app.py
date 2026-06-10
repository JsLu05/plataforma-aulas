from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "proyecto2026"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    usuario = data.get('usuario')
    password = data.get('password')

    if usuario == "admin" and password == "1234":
        token = jwt.encode(
            {
                'usuario': usuario,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'token': token
        })

    return jsonify({'mensaje': 'Credenciales incorrectas'}), 401


def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'mensaje': 'Token requerido'}), 401

        try:
            datos = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token expirado'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/incidencias', methods=['POST'])
@token_requerido
def crear_incidencia():
    return jsonify({
        'mensaje': 'Incidencia creada correctamente'
    }), 201


@app.route('/incidencias/<int:id>', methods=['PUT'])
@token_requerido
def actualizar(id):
    return jsonify({
        'mensaje': f'Incidencia {id} actualizada correctamente'
    })


@app.route('/incidencias/<int:id>', methods=['DELETE'])
@token_requerido
def eliminar(id):
    return jsonify({
        'mensaje': f'Incidencia {id} eliminada correctamente'
    })


if __name__ == '__main__':
    app.run(debug=True)