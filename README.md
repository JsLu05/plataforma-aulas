Activar entorno virtual
env\Scripts\activate

pip install -r requirements.txt
pip install Flask
pip install Flask-JWT-Extended
pip install Flask-MySQLdb
pip install PyMySQL

python app.py
El servidor corre en: http://127.0.0.1:5000

Para el login:
POST http://localhost:5000/api/login
Content-Type: application/json
{
    "correo": "admin@fcpn.edu.bo",
    "password": "admin123"
}

Crear incidencia (con token)
POST http://localhost:5000/api/incidencias
Authorization: Bearer <token-de-cuenta-de-docente-o-estudiante>
Content-Type: application/json
Body json
{
    "titulo": "Proyector no enciende",
    "id_aula": 1,
    "tipo": "Proyector",
    "descripcion": "El proyector no responde al encenderse",
    "estado": "Pendiente"
}

Cambiar estado de una incidencia
PUT http://localhost:5000/api/incidencias/1/estado
Authorization: Bearer <token-de-admin@fcpn.edu.bo>
Content-Type: application/json
Body json
{
    "estado": "En proceso" o "Pendiente" o "Resuelto"
}
