DROP DATABASE IF EXISTS `example`;

CREATE DATABASE `example` DEFAULT CHARACTER SET utf8mb4;
USE `example`;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Имя юзера',
  UNIQUE unique_name(name(10))
) COMMENT = 'Сотрудники';