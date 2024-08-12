-- TASK MANAGER DATABASE SET UP


CREATE DATABASE IF NOT EXISTS taskmanager_dev_db;
CREATE USER IF NOT EXISTS 'taskmanager_dev'@'localhost' IDENTIFIED BY 'taskmanager_dev_pwd';
GRANT ALL PRIVILEGES ON taskmanager_dev_db.* TO 'taskmanager_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'taskmanager_dev'@'localhost';