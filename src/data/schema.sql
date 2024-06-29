-- CREAR OTRAS TABLAS

CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    enrollment_number VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    cuatri VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    club_id INT,

    FOREIGN KEY (role_id) REFERENCES roles(id)
    -- FOREIGN KEY (club_id) REFERENCES clubs(id)
);

INSERT INTO roles (title) VALUES ('admin'), ('student');
