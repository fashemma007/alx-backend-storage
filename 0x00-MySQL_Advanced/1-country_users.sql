-- This SQL script creates the 'users' table with 'id', 'email' and 'name' columns, where 'id' is the primary key and auto-increment,
-- drop table to ensure schema is correct
DROP TABLE IF EXISTS users;
-- create the users table
CREATE TABLE users (
    -- with autogen int id column
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- unique emails for each entry
    email VARCHAR(255) NOT NULL UNIQUE,
    -- name of max-length 255
    name VARCHAR(255),
    -- enum column with first element as default value
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);