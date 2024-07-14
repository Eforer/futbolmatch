CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL
);
CREATE TABLE Match (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) NOT NULL,
    organizer_id INT NOT NULL,
    FOREIGN KEY (organizer_id) REFERENCES User(id)
);
CREATE TABLE user_match (
    user_id INT NOT NULL,
    match_id INT NOT NULL,
    PRIMARY KEY (user_id, match_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (match_id) REFERENCES Match(id)
);
