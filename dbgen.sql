DROP DATABASE IF EXISTS dirtree;
CREATE DATABASE dirtree;
USE dirtree;
CREATE TABLE dirs(
	directory_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	lft INT NOT NULL,
	rgt INT NOT NULL	
);

INSERT INTO dirs
VALUES(1, 'root',1,8),(2,'videos',2,3),(3,'pictures',4,5),(4,'music',6,7);
