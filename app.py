from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os

app = Flask(__name__, static_folder='.', static_url_path='')

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "reporte_aulas_db"

app.config['JWT_SECRET_KEY'] = 'tu-clave-secreta-para-jwt-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

mysql = MySQL(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        if not correo or not password:
            return jsonify({"mensaje": "Correo y contraseña requeridos"}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_usuario, nombre, correo, rol, password FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        
        if not usuario:
            return jsonify({"mensaje": "Credenciales inválidas"}), 401
        
        if usuario[4] != password:
            return jsonify({"mensaje": "Credenciales inválidas"}), 401

        token = create_access_token(identity=usuario[0])
        
        return jsonify({
            "token": token,
            "id_usuario": usuario[0],
            "nombre": usuario[1],
            "correo": usuario[2],
            "rol": usuario[3]
        })
    except Exception as e:
        return jsonify({"mensaje": f"Error en login: {str(e)}"}), 500
    

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_usuario, nombre, correo, rol FROM usuarios")
    datos = cursor.fetchall()
    cursor.close()
    
    usuarios = [{"id_usuario": row[0], "nombre": row[1], "correo": row[2], "rol": row[3]} for row in datos]
    return jsonify(usuarios) if usuarios else jsonify({"mensaje": "NO EXISTEN USUARIOS"})

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_usuario, nombre, correo, rol FROM usuarios WHERE id_usuario = %s", (id,))
    dato = cursor.fetchone()
    cursor.close()
    
    if not dato:
        return jsonify({"mensaje": "USUARIO NO EXISTE"}), 404
    return jsonify({"id_usuario": dato[0], "nombre": dato[1], "correo": dato[2], "rol": dato[3]})

@app.route('/api/usuarios', methods=['POST'])
@jwt_required()
def crear_usuario():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios(nombre, correo, rol, password) VALUES (%s, %s, %s, %s)",
                   (data['nombre'], data['correo'], data['rol'], data.get('password', '123456')))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Usuario insertado con éxito!!!"}), 201

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_usuario(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s, rol = %s WHERE id_usuario = %s",
                   (data['nombre'], data['correo'], data['rol'], id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Usuario modificado"}), 200

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombre FROM usuarios WHERE id_usuario = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        return jsonify({"mensaje": "EL USUARIO NO EXISTE!!!"}), 404
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Usuario eliminado"}), 200

@app.route('/api/aulas', methods=['GET'])
def listar_aulas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_aula, nombre, piso, capacidad FROM aulas")
    datos = cursor.fetchall()
    cursor.close()
    
    aulas = [{"id_aula": row[0], "nombre": row[1], "piso": row[2], "capacidad": row[3]} for row in datos]
    return jsonify(aulas) if aulas else jsonify({"mensaje": "NO EXISTEN AULAS"})

@app.route('/api/aulas/<int:id>', methods=['GET'])
def obtener_aula(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_aula, nombre, piso, capacidad FROM aulas WHERE id_aula = %s", (id,))
    dato = cursor.fetchone()
    cursor.close()
    
    if not dato:
        return jsonify({"mensaje": "AULA NO EXISTE"}), 404
    return jsonify({"id_aula": dato[0], "nombre": dato[1], "piso": dato[2], "capacidad": dato[3]})

@app.route('/api/aulas', methods=['POST'])
@jwt_required()
def crear_aula():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO aulas(nombre, piso, capacidad) VALUES (%s, %s, %s)",
                   (data['nombre'], data['piso'], data['capacidad']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Aula insertada con éxito!!!"}), 201

@app.route('/api/aulas/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_aula(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE aulas SET nombre = %s, piso = %s, capacidad = %s WHERE id_aula = %s",
                   (data['nombre'], data['piso'], data['capacidad'], id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Aula modificada"}), 200

@app.route('/api/aulas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_aula(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombre FROM aulas WHERE id_aula = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        return jsonify({"mensaje": "EL AULA NO EXISTE!!!"}), 404
    cursor.execute("DELETE FROM aulas WHERE id_aula = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Aula eliminada"}), 200

@app.route('/api/incidencias', methods=['GET'])
def listar_incidencias():
    aula = request.args.get('aula', '')
    tipo = request.args.get('tipo', '')
    estado = request.args.get('estado', '')
    
    cursor = mysql.connection.cursor()
    
    sql = """
        SELECT i.id_incidencia, i.titulo, i.descripcion, i.tipo, 
               DATE_FORMAT(i.fecha_reporte, '%%Y-%%m-%%d') as fecha, 
               i.estado, i.id_usuario, i.id_aula, a.nombre as aula_nombre
        FROM incidencias i
        JOIN aulas a ON i.id_aula = a.id_aula
        WHERE 1=1
    """
    params = []
    
    if aula:
        sql += " AND a.nombre LIKE %s"
        params.append(f"%{aula}%")
    if tipo:
        sql += " AND i.tipo = %s"
        params.append(tipo)
    if estado:
        sql += " AND i.estado = %s"
        params.append(estado)
    
    sql += " ORDER BY i.fecha_reporte DESC"
    
    cursor.execute(sql, params)
    datos = cursor.fetchall()
    cursor.close()
    
    incidencias = []
    for row in datos:
        incidencias.append({
            "id": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "tipo": row[3],
            "fecha": row[4],
            "estado": row[5],
            "id_usuario": row[6],
            "id_aula": row[7],
            "aula": row[8]
        })
    return jsonify(incidencias) if incidencias else jsonify([])

@app.route('/api/incidencias/<int:id>', methods=['GET'])
def obtener_incidencia(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT i.id_incidencia, i.titulo, i.descripcion, i.tipo, 
               DATE_FORMAT(i.fecha_reporte, '%%Y-%%m-%%d') as fecha, 
               i.estado, i.id_usuario, i.id_aula, a.nombre as aula_nombre
        FROM incidencias i
        JOIN aulas a ON i.id_aula = a.id_aula
        WHERE i.id_incidencia = %s
    """, (id,))
    dato = cursor.fetchone()
    cursor.close()
    
    if not dato:
        return jsonify({"mensaje": "INCIDENCIA NO EXISTE"}), 404
    
    return jsonify({
        "id": dato[0], "titulo": dato[1], "descripcion": dato[2],
        "tipo": dato[3], "fecha": dato[4], "estado": dato[5],
        "id_usuario": dato[6], "id_aula": dato[7], "aula": dato[8]
    })

@app.route('/api/incidencias', methods=['POST'])
@jwt_required()
def crear_incidencia():
    data = request.get_json()
    user_id = get_jwt_identity()
    id_usuario = data.get('id_usuario', user_id)
    
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO incidencias(titulo, descripcion, tipo, fecha_reporte, estado, id_usuario, id_aula)
        VALUES (%s, %s, %s, CURDATE(), %s, %s, %s)
    """, (data['titulo'], data.get('descripcion', ''), data['tipo'], 
          data.get('estado', 'Pendiente'), id_usuario, data['id_aula']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Incidencia registrada con éxito!!!"}), 201

@app.route('/api/incidencias/<int:id>', methods=['PUT'])
@jwt_required()
def modificar_incidencia(id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"mensaje": "No se recibieron datos"}), 400
        
        cursor = mysql.connection.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT id_incidencia FROM incidencias WHERE id_incidencia = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"mensaje": "LA INCIDENCIA NO EXISTE"}), 404
        
        # Construir actualización dinámica
        campos = []
        valores = []
        
        campos_validos = ['titulo', 'descripcion', 'tipo', 'estado', 'id_aula']
        
        for campo in campos_validos:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos:
            cursor.close()
            return jsonify({"mensaje": "No hay datos válidos para actualizar"}), 400
        
        valores.append(id)
        sql = f"UPDATE incidencias SET {', '.join(campos)} WHERE id_incidencia = %s"
        
        cursor.execute(sql, valores)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"mensaje": "Incidencia modificada exitosamente"}), 200
        
    except Exception as e:
        return jsonify({"mensaje": f"Error interno: {str(e)}"}), 500

@app.route('/api/incidencias/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_incidencia(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titulo FROM incidencias WHERE id_incidencia = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        return jsonify({"mensaje": "LA INCIDENCIA NO EXISTE!!!"}), 404
    
    cursor.execute("DELETE FROM incidencias WHERE id_incidencia = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Incidencia eliminada"}), 200

@app.route('/api/consultas/incidencias-pendientes-por-aula', methods=['GET'])
@jwt_required()
def incidencias_pendientes_por_aula():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT a.nombre as aula, COUNT(i.id_incidencia) as pendientes
        FROM aulas a
        LEFT JOIN incidencias i ON a.id_aula = i.id_aula AND i.estado = 'Pendiente'
        GROUP BY a.id_aula
        ORDER BY pendientes DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    
    resultado = [{"aula": row[0], "pendientes": row[1]} for row in datos]
    return jsonify(resultado)

@app.route('/api/consultas/incidencias-ultima-semana', methods=['GET'])
@jwt_required()
def incidencias_ultima_semana():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT i.id_incidencia, i.titulo, i.tipo, i.estado, 
               a.nombre as aula, DATE_FORMAT(i.fecha_reporte, '%%Y-%%m-%%d') as fecha
        FROM incidencias i
        JOIN aulas a ON i.id_aula = a.id_aula
        WHERE i.fecha_reporte >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        ORDER BY i.fecha_reporte DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    
    resultado = []
    for row in datos:
        resultado.append({
            "id": row[0],
            "titulo": row[1],
            "tipo": row[2],
            "estado": row[3],
            "aula": row[4],
            "fecha": row[5]
        })
    return jsonify(resultado)

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)