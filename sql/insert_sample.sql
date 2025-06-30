BEGIN TRANSACTION;

-- Reset tables
DELETE FROM rental_agreement;
DELETE FROM rent_payment;
DELETE FROM tenant;
DELETE FROM apartment;
DELETE FROM sqlite_sequence;


-- Apartments
INSERT INTO apartment (name, address, user_id) VALUES 
  ("Demo Loft", "Demo Street 1", 1),
  ("City Flat", "Central Avenue 99", 1);

-- Tenants
INSERT INTO tenant (name, tel_num, IDNP, user_id) VALUES
  ("Testa Tenantova", 37376111222, 1111111111111, 1),
  ("Max Mustermann", 37378112233, 2222222222222, 1);

-- Rental agreements
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, end_date, rent_amount, user_id) VALUES 
  (1, 1, '2025-04-01', NULL, 500.00, 1),
  (2, 2, '2025-05-01', NULL, 600.00, 1);

-- Rent payments
-- Testa (apartment 1): Missed May, paid June & July
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  (1, '2025-06', '2025-06-02', 'Paid in cash', 1),
  (1, '2025-07', '2025-06-25', 'Paid early for July', 1);

-- Max (apartment 2): Paid June, missed May
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  (2, '2025-06', '2025-06-10', 'Paid via transfer', 1);


COMMIT;