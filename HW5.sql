USE sakila;

# Problem 1
CREATE PROCEDURE listCity (IN country_in VARCHAR(20))
BEGIN
    SELECT city, SUM(amount) FROM country co
        JOIN sakila.city c on co.country_id = c.country_id
        JOIN sakila.address a on c.city_id = a.city_id
        JOIN sakila.customer cu on a.address_id = cu.address_id
        JOIN sakila.payment p on cu.customer_id = p.customer_id
        WHERE country LIKE country_in
        GROUP BY city;
END;

# Problem 1 Test
CALL listCity("UNITED STATES");


# Problem 2
CREATE FUNCTION customerRewardLevel (c_id INT, gold_threshold INT, silver_threshold INT, bronze_threshold INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE reward_level VARCHAR(20);
    DECLARE customer_spend INT;
    SELECT SUM(amount) INTO customer_spend FROM payment
        JOIN customer ON payment.customer_id = customer.customer_id
    WHERE  payment.customer_id = c_id;
    IF customer_spend >= gold_threshold THEN
        SET reward_level = 'GOLD';
    ELSEIF (customer_spend < gold_threshold AND customer_spend >= silver_threshold) THEN
        SET reward_level = 'SILVER';
    ELSEIF (customer_spend < silver_threshold AND customer_spend >= bronze_threshold) THEN
        SET reward_level = 'BRONZE';
    ELSE
        SET reward_level = 'NOTHING';
    END IF;
    RETURN reward_level;
END;

# Problem 2 Test
SELECT customerRewardLevel(10, 180, 100 ,50)


# Problem 3
DROP TABLE customer_log;
CREATE TABLE customer_log (
    log_id INT UNSIGNED AUTO_INCREMENT,
    customer_id SMALLINT UNSIGNED,
    field_name VARCHAR(40),
    old_value VARCHAR(40),
    new_value VARCHAR(40),
    date_change DATETIME,
    PRIMARY KEY (log_id),
    CONSTRAINT FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

CREATE TRIGGER logCustomerChange
    AFTER UPDATE ON customer
    FOR EACH ROW
    IF NEW.first_name != OLD.first_name THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "first_name", OLD.first_name, NEW.first_name, CURRENT_TIMESTAMP);
    ELSEIF NEW.last_name != OLD.last_name THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "last_name", OLD.last_name, NEW.last_name, CURRENT_TIMESTAMP);
    ELSEIF NEW.email != OLD.email THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "email", OLD.email, NEW.email, CURRENT_TIMESTAMP);
    ELSEIF NEW.active != OLD.active THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "active", OLD.active, NEW.active, CURRENT_TIMESTAMP);
    ELSEIF NEW.store_id != OLD.store_id THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "store_id", OLD.store_id, NEW.store_id, CURRENT_TIMESTAMP);
    ELSEIF NEW.address_id != OLD.address_id THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "address_id", OLD.address_id, NEW.address_id, CURRENT_TIMESTAMP);
    ELSEIF NEW.create_date != OLD.create_date THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "create_date", OLD.create_date, NEW.create_date, CURRENT_TIMESTAMP);
    ELSEIF NEW.last_update != OLD.last_update THEN
        INSERT INTO customer_log(customer_id, field_name, old_value, new_value, date_change)
            VALUES (OLD.customer_id, "last_update", OLD.last_update, NEW.last_update, CURRENT_TIMESTAMP);
    END IF;


# Problem 3 Test
UPDATE customer
SET first_name = "Updated"
WHERE customer_id = 599;

SELECT *
FROM customer_log;


# Problem 4
ALTER TABLE customer
ADD mtd_spent DECIMAL(10,2);

CREATE EVENT calculateRevenue
ON SCHEDULE
    EVERY 1 MONTH
    STARTS CURRENT_TIMESTAMP
    ENDS CURRENT_TIMESTAMP + INTERVAL 1 YEAR
DO
    UPDATE customer c
    JOIN (
        SELECT p.customer_id AS customer_id, SUM(amount) AS mtd_spent FROM payment p
            JOIN customer c ON p.customer_id = c.customer_id
            WHERE payment_date = YEAR(payment_date) = YEAR(NOW())
            AND MONTH(payment_date) = MONTH(NOW())
            GROUP BY c.customer_id
        ) cp ON c.customer_id = cp.customer_id
    SET c.mtd_spent = cp.mtd_spent;



