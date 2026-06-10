CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('docente','estudiante','admin') NOT NULL
);

CREATE TABLE aulas (
    id_aula INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    piso INT NOT NULL,
    capacidad INT
);

CREATE TABLE incidencias (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    tipo VARCHAR(50),
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente','En proceso','Resuelto') DEFAULT 'Pendiente',

    id_usuario INT NOT NULL,
    id_aula INT NOT NULL,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_aula) REFERENCES aulas(id_aula)
);

INSERT INTO usuarios(nombre, correo, password, rol) VALUES
('Juan Perez', 'juan@umsa.bo', '123456', 'docente'),
('Maria Gomez', 'maria@umsa.bo', '123456', 'estudiante'),
('Carlos Rojas', 'carlos@umsa.bo', '123456', 'docente'),
('Ana Flores', 'ana@umsa.bo', '123456', 'estudiante'),
('Luis Quispe', 'luis@umsa.bo', '123456', 'docente'),
('Fernanda Choque', 'fernanda@fcpn.edu.bo', '123456', 'estudiante'),
('Diego Mamani', 'diego@fcpn.edu.bo', '123456', 'estudiante'),
('Sofia Vargas', 'sofia@fcpn.edu.bo', '123456', 'docente'),
('Pedro Salazar', 'pedro@fcpn.edu.bo', '123456', 'estudiante'),
('Administrador', 'admin@fcpn.edu.bo', 'admin123', 'admin');

INSERT INTO aulas(nombre, piso, capacidad) VALUES
('Aula 101', 1, 35),
('Aula 102', 1, 40),
('Aula 201', 2, 45),
('Aula 202', 2, 40),
('Aula 203', 2, 50),
('Aula 301', 3, 45),
('Aula 302', 3, 40),
('Laboratorio Redes', 3, 25),
('Laboratorio Web', 4, 30),
('Auditorio Principal', 1, 120);

INSERT INTO incidencias(titulo, descripcion, tipo, estado, id_usuario, id_aula) VALUES
('Proyector no enciende', 'El proyector no responde al encenderse', 'Proyector', 'Pendiente',1, 3),
('Internet inestable', 'La conexion se pierde constantemente', 'Conectividad', 'En proceso', 2, 8),
('Computadora dañada', 'Equipo sin imagen en pantalla', 'Computadora', 'Pendiente', 3, 9),
('Sillas rotas', 'Existen varias sillas en mal estado', 'Mobiliario', 'Resuelto', 4, 4),
('Focos quemados', 'La iluminacion es insuficiente', 'Iluminacion', 'Pendiente', 5, 6),
('Cable de red desconectado', 'No existe acceso a internet', 'Conectividad', 'En proceso', 6, 8),
('Pantalla del proyector rota', 'La imagen presenta manchas', 'Proyector', 'Pendiente', 7, 3),
('Mesa docente dañada', 'La mesa presenta una pata rota', 'Mobiliario', 'Resuelto', 8, 2),
('PC no inicia', 'Muestra error al arrancar', 'Computadora', 'Pendiente', 9, 9),
('Problema de iluminación', 'Sector izquierdo sin luz', 'Iluminacion', 'Pendiente', 1, 1),
('Proyector sin señal', 'No recibe señal HDMI', 'Proyector', 'En proceso', 2, 4),
('Router reiniciándose', 'Se reinicia cada pocos minutos', 'Conectividad', 'Pendiente', 3, 8),
('Monitor averiado', 'Pantalla completamente negra', 'Computadora', 'Resuelto', 4, 9),
('Puerta dañada', 'La puerta no cierra correctamente', 'Mobiliario', 'Pendiente', 5, 5),
('Lámpara parpadea', 'Genera molestia durante clases', 'Iluminacion', 'En proceso', 6, 7),
('Mouse defectuoso', 'No responde correctamente', 'Computadora', 'Pendiente', 7, 9),
('Proyector con baja resolución', 'Imagen borrosa durante exposición', 'Proyector', 'Resuelto', 8, 6),
('Sin acceso a WiFi', 'No aparecen las redes disponibles', 'Conectividad', 'Pendiente', 9, 10),
('Escritorio roto', 'Superficie deteriorada', 'Mobiliario', 'Pendiente', 2, 2),
('Foco apagado permanentemente', 'Requiere reemplazo', 'Iluminacion', 'Resuelto', 3, 1);