-- CUISINE DATABASE SET UP
CREATE DATABASE IF NOT EXISTS TaskManager_dev_db;
CREATE USER IF NOT EXISTS 'TaskManager_dev'@'localhost' IDENTIFIED BY 'TaskManager_dev_pwd';
GRANT ALL PRIVILEGES ON TaskManager_dev_db.* TO 'TaskManager_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'TaskManager_dev'@'localhost';