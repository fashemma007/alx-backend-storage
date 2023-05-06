-- This SQL script creates a trigger named 'item_sold' that runs after an insert on the 'orders' table.
DROP TRIGGER IF EXISTS item_sold;
-- DELIMITER $$ indeicates delim change from ; to $$
DELIMITER $$ CREATE TRIGGER item_sold
AFTER -- shld run after
INSERT ON orders FOR EACH ROW BEGIN -- an insert statement on orders table
UPDATE items -- update items table
SET quantity = quantity - NEW.number -- subtract number of orders from qtty
WHERE name = NEW.item_name;
-- from the newly added order name
END $$
DELIMITER;
-- disable newly set delimiter
