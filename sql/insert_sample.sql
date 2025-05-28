BEGIN TRANSACTION;

-- Clear old data
DELETE FROM rental_agreement;
DELETE FROM tenant;
DELETE FROM apartment;
DELETE FROM sqlite_sequence;

-- Insert apartments
INSERT INTO apartment (name, address) VALUES 
  ("Central Loft", "Str. Stefan cel Mare 10"),
  ("Park View", "Bulevardul Dacia 5"),
  ("Green Residence", "Str. Alba Iulia 15");

-- Insert tenants
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Ion Popescu", 37376123456, 1234567890123);
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Maria Ivanova", 37378112233, 2345678901234);
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Alexei Moraru", 37379223344, 3456789012345);

-- Insert rental agreements (links tenant to apartment)
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, end_date, rent_amount) VALUES 
  (1, 1, '2025-01-01', '2025-06-30', 550.00),
  (1, 2, '2025-07-01', NULL, 600.00),  -- same apartment, new tenant
  (2, 3, '2025-03-01', NULL, 700.00);

INSERT INTO rent_payment (apartment_id, month, payment_date, comment) VALUES
  (1, '2025-04', '2025-04-05', 'Paid in cash by Ion'),
  (1, '2025-05', '2025-05-01', 'Paid via bank transfer'),
  (2, '2025-05', '2025-05-02', 'Paid early'),
  (1, '2025-07', '2025-07-03', 'Anna moved in');

COMMIT;
