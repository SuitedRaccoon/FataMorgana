CREATE SCHEMA IF NOT EXISTS `libris` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `libris` ;

DROP TABLE IF EXISTS user_books;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    genre VARCHAR(100),
    year_published INT
);

CREATE TABLE user_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    status ENUM('planned', 'reading', 'completed', 'skipped'),
    queue_position INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE IF NOT EXISTS saved_lists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS saved_list_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    list_id INT,
    book_id INT,
    FOREIGN KEY (list_id) REFERENCES saved_lists(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);