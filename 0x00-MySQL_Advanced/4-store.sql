-- This SQL script creates a trigger named 'item_sold' that runs after an insert on the 'orders' table.
DROP TRIGGER IF EXISTS item_sold;

-- DELIMITER $$ indeicates delim change from ; to $$
DELIMITER $$

CREATE TRIGGER item_sold
	AFTER INSERT
	ON orders FOR EACH ROW -- run after an insert statement on orders table
BEGIN
	UPDATE items -- update items table
	SET quantity = quantity - NEW.number -- subtract number of orders from qtty
	-- from the newly added order name
	WHERE name = NEW.item_name;
END $$
DELIMITER ; -- disable newly set delimiter