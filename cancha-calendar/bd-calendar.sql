CREATE TABLE cancha (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    cancha_id INT,
    FOREIGN KEY (cancha_id) REFERENCES cancha(id)
);
