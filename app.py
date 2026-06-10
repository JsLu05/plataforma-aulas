from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
#pip install flask_mysqldb

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "reporte_aulas_db"

#==================================================================================GET
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    cursor = mysql.connection.cursor()
    sql = "SELECT id_usuario, nombre, correo, rol FROM usuarios"
    cursor.execute(sql)
    datos = cursor.fetchall()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN USUARIOS"})
    usuarios = []
    for fila in datos:
        usuarios.append({
            "id_usuario": fila[0],
            "nombre": fila[1],
            "correo": fila[2],
            "rol": fila[3]
        })
    cursor.close()
    return jsonify(usuarios)

@app.route('/aulas', methods=['GET'])
def listar_aulas():
    cursor = mysql.connection.cursor()
    sql = "SELECT id_aula, nombre, piso, capacidad FROM aulas"
    cursor.execute(sql)
    datos = cursor.fetchall()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN AULAS"})
    aulas = []
    for fila in datos:
        aulas.append({
            "id_aula": fila[0],
            "nombre": fila[1],
            "piso": fila[2],
            "capacidad": fila[3]
        })
    cursor.close()
    return jsonify(aulas)

@app.route('/incidencias', methods=['GET'])
def listar_incidencias():
    cursor = mysql.connection.cursor()
    sql = "SELECT id_incidencia, titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula FROM incidencias"
    cursor.execute(sql)
    datos = cursor.fetchall()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN INCIDENCIAS"})
    incidencias = []
    for fila in datos:
        incidencias.append({
            "id_incidencia": fila[0],
            "titulo": fila[1],
            "descripcion": fila[2],
            "tipo": fila[3],
            "fecha_reporte": fila[4],
            "estado": fila[5],
            "id_usuario": fila[6],
            "id_aula": fila[7]
        })
    cursor.close()
    return jsonify(incidencias)

#==================================================================================GET POR ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT id_usuario, nombre, correo, rol FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN USUARIOS"})
    usuarios = []
    for fila in datos:
        usuarios.append({
            "id_usuario": fila[0],
            "nombre": fila[1],
            "correo": fila[2],
            "rol": fila[3]
        })
    cursor.close()
    return jsonify(usuarios)

@app.route('/aulas/<int:id>', methods=['GET'])
def obtener_aula(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT id_aula, nombre, piso, capacidad FROM aulas WHERE id_aula = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN AULAS"})
    aulas = []
    for fila in datos:
        aulas.append({
            "id_aula": fila[0],
            "nombre": fila[1],
            "piso": fila[2],
            "capacidad": fila[3]
        })
    cursor.close()
    return jsonify(aulas)

@app.route('/incidencias/<int:id>', methods=['GET'])
def obtener_incidencia(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT id_incidencia, titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula FROM incidencias WHERE id_incidencia = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if not datos:
        return jsonify({"mensaje": "NO EXISTEN INCIDENCIAS"})
    incidencias = []
    for fila in datos:
        incidencias.append({
            "id_incidencia": fila[0],
            "titulo": fila[1],
            "descripcion": fila[2],
            "tipo": fila[3],
            "fecha_reporte": fila[4],
            "estado": fila[5],
            "id_usuario": fila[6],
            "id_aula": fila[7]
        })
    cursor.close()
    return jsonify(incidencias)

#==================================================================================POST
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    rol = data['rol']

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO usuarios(nombre, correo, rol)
            VALUES (%s, %s, %s)"""
    cursor.execute(sql, (nombre, correo, rol))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Usuario insertado con exito!!!"}),201

@app.route('/aulas', methods=['POST'])
def crear_aula():
    data = request.get_json()
    nombre = data['nombre']
    piso = data['piso']
    capacidad = data['capacidad']

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO aulas(nombre, piso, capacidad)
            VALUES (%s, %s, %s)"""
    cursor.execute(sql, (nombre, piso, capacidad))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Aula insertada con exito!!!"}),201

@app.route('/incidencias', methods=['POST'])
def crear_incidencia():
    data = request.get_json()
    titulo = data['titulo']
    descripcion = data['descripcion']
    tipo = data['tipo']
    fecha_reporte = data['fecha_reporte']
    estado = data['estado']
    id_usuario = data['id_usuario']
    id_aula = data['id_aula']

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO incidencias(titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Incidencia registrada con exito!!!"}),201

#==================================================================================PUT
@app.route('/usuarios/<int:id>', methods=['PUT'])
def modificar_usuario(id):
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    rol = data['rol']

    cursor = mysql.connection.cursor()
    sql = """UPDATE usuarios 
            SET nombre = %s, correo = %s, rol = %s
            WHERE id = %s"""
    cursor.execute(sql, (nombre, correo, rol, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Usuario modificado"}),200

@app.route('/aulas/<int:id>', methods=['PUT'])
def modificar_aula(id):
    data = request.get_json()
    nombre = data['nombre']
    piso = data['piso']
    capacidad = data['capacidad']

    cursor = mysql.connection.cursor()
    sql = """UPDATE aulas 
            SET nombre = %s, piso = %s, capacidad = %s
            WHERE id = %s"""
    cursor.execute(sql, (nombre, piso, capacidad, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Aula modificada"}),200

@app.route('/incidencias/<int:id>', methods=['PUT'])
def modificar_incidencia(id):
    data = request.get_json()
    titulo = data['titulo']
    descripcion = data['descripcion']
    tipo = data['tipo']
    fecha_reporte = data['fecha_reporte']
    estado = data['estado']
    id_usuario = data['id_usuario']
    id_aula = data['id_aula']

    cursor = mysql.connection.cursor()
    sql = """UPDATE incidencias 
            SET titulo = %s, descripcion = %s, tipo = %s, fecha_reporte = %s, estado = %s, id_usuario = %s, id_aula = %s
            WHERE id = %s"""
    cursor.execute(sql, (titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Incidencia modificada"}),200

#==================================================================================DELETE
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    #BUSCAR USUARIO
    cursor = mysql.connection.cursor()
    sql = "SELECT nombre FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if datos == None:
        cursor.close()
        return jsonify({"mensaje": "EL USUARIO NO EXISTE!!!"}), 404
    #ELIMINAR USUARIO
    sql = """DELETE FROM usuarios 
            WHERE id = %s"""
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Usuario eliminado"}),200

@app.route('/aulas/<int:id>', methods=['DELETE'])
def eliminar_aula(id):
    #BUSCAR AULA
    cursor = mysql.connection.cursor()
    sql = "SELECT nombre FROM aulas WHERE id_aula = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if datos == None:
        cursor.close()
        return jsonify({"mensaje": "EL AULA NO EXISTE!!!"}), 404
    #ELIMINAR AULA
    sql = """DELETE FROM aulas 
            WHERE id = %s"""
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Aula eliminada"}),200

@app.route('/incidencias/<int:id>', methods=['DELETE'])
def eliminar_incidencia(id):
    #BUSCAR INCIDENCIA
    cursor = mysql.connection.cursor()
    sql = "SELECT titulo FROM incidencias WHERE id_incidencia = %s"
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()
    if datos == None:
        cursor.close()
        return jsonify({"mensaje": "LA INCIDENCIA NO EXISTE!!!"}), 404
    #ELIMINAR INCIDENCIA
    sql = """DELETE FROM incidencias 
            WHERE id = %s"""
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"Incidencia eliminada"}),200

if __name__ == "__main__":
    app.run(debug=True)