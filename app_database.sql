
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO users (id, username, password) VALUES
    (10001, 'admin', 'securepassword'),
    (10002, 'user1', 'password123'),
    (10003, 'user2', 'mypassword');
