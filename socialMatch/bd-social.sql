CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Friendships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    friend_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE
);


INSERT INTO users (nombre, apellido, email, password, fecha_nacimiento) VALUES
('Claudio', 'Bravo', 'claudio.bravo@example.com', 'password123', '1983-04-13'),
('Gary', 'Medel', 'gary.medel@example.com', 'password123', '1987-08-03'),
('Arturo', 'Vidal', 'arturo.vidal@example.com', 'password123', '1987-05-22'),
('Alexis', 'Sánchez', 'alexis.sanchez@example.com', 'password123', '1988-12-19'),
('Charles', 'Aránguiz', 'charles.aranguiz@example.com', 'password123', '1989-04-17'),
('Eduardo', 'Vargas', 'eduardo.vargas@example.com', 'password123', '1989-11-20'),
('Mauricio', 'Isla', 'mauricio.isla@example.com', 'password123', '1988-06-12'),
('Eugenio', 'Mena', 'eugenio.mena@example.com', 'password123', '1988-07-18'),
('Jean', 'Beausejour', 'jean.beausejour@example.com', 'password123', '1984-06-01');