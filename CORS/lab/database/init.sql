CREATE DATABASE IF NOT EXISTS cors_null_lab;

USE cors_null_lab;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) NOT NULL
);

INSERT INTO users
    (username, password, email, api_key)
VALUES
    (
        'attack',
        'attack123',
        'attack@example.com',
        'ATTACK-KEY-12345'
    ),
    (
        'victim',
        'victim123',
        'victim@example.com',
        'VICTIM-SECRET-98765'
    );