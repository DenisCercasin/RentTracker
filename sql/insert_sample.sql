BEGIN TRANSACTION;

-- Reset tables
DELETE FROM rental_agreement;
DELETE FROM rent_payment;
DELETE FROM tenant;
DELETE FROM apartment;
DELETE FROM user;
DELETE FROM sqlite_sequence;


-- For testing
INSERT INTO user (id, name, email, password) VALUES 
  (1, 'Alice Admin', 'alice@example.com', 'Hello12345!'),
  (2, 'Bob Owner', 'bob@example.com', 'hashed_pw2'),
  (3, 'Charlie Checker', 'charlie@example.com', 'hashed_pw3');


-- Apartments per user
INSERT INTO apartment (name, address, user_id) VALUES 
  ("Central Loft", "Str. Stefan cel Mare 10", 1),
  ("Park View", "Bulevardul Dacia 5", 1),
  ("Urban Nest", "Str. Veronica Micle 22", 2),
  ("Green Residence", "Str. Alba Iulia 15", 2),
  ("Sunset Villa", "Str. Independentei 8", 3);

-- Tenants per user
INSERT INTO tenant (name, tel_num, IDNP, user_id) VALUES
  ("Ion Popescu", 37376123456, 1234567890123, 1),
  ("Maria Ivanova", 37378112233, 2345678901234, 1),
  ("Alexei Moraru", 37379223344, 3456789012345, 2),
  ("Elena Ceban", 37376222222, 4567890123456, 2),
  ("Victor Lungu", 37376333333, 5678901234567, 3);


-- Rental agreements per user
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, end_date, rent_amount, user_id) VALUES 
  (1, 1, '2025-01-01', '2025-06-30', 550.00, 1),
  (1, 2, '2025-07-01', NULL, 600.00, 1),
  (3, 3, '2025-03-01', NULL, 700.00, 2),
  (4, 4, '2025-05-01', NULL, 720.00, 2),
  (5, 5, '2025-06-01', NULL, 800.00, 3);

-- Rent payments per user
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  (1, '2025-04', '2025-04-05', 'Paid in cash by Ion', 1),
  (1, '2025-05', '2025-05-01', 'Paid via bank transfer', 1),
  (3, '2025-05', '2025-05-02', 'Paid early', 2),
  (4, '2025-06', '2025-06-03', 'Paid late', 2),
  (5, '2025-06', '2025-06-03', 'Victor started contract', 3);

COMMIT;
