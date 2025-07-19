BEGIN TRANSACTION;

-- Reset tables
DELETE FROM rent_payment;
DELETE FROM rental_agreement;
DELETE FROM tenant;
DELETE FROM apartment;
DELETE FROM user;
DELETE FROM sqlite_sequence;

-- Insert test user with ID = 1
INSERT INTO user (id, name, email, password, is_confirmed, reminder_day, reminder_enabled, use_telegram, use_email)
VALUES (
    1,
    'Demo User',
    'test@email.com',
    'scrypt:32768:8:1$jTQKCqFd62BVREsn$29af821cdd9ecdca98d3fa740ffd2755c42507fcca24dba4d45edde648b2e70479f2cd8b1c693c4a9745cb79cae896facc77ba7860fea731f039551cf7d9cf18',
    1,
    1,
    1,
    0,
    1
);

-- Apartments
INSERT INTO apartment (name, address, user_id) VALUES 
  ('Demo Loft', 'Demo Street 1', 1),
  ('City Flat', 'Central Avenue 99', 1),
  ('Suburb House', 'Quiet Lane 5', 1);

-- Tenants
INSERT INTO tenant (name, tel_num, IDNP, user_id) VALUES
  ('Testa Tenantova', 37376111222, 1111111111111, 1),
  ('Max Mustermann', 37378112233, 2222222222222, 1),
  ('Elena Example', 37370123456, 3333333333333, 1);

-- Rental Agreements
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, end_date, rent_amount, user_id) VALUES 
    (1, 1, '2025-04-01', NULL, 500.00, 1),   -- Ongoing
  (2, 2, '2025-05-01', NULL, 600.00, 1),   -- Ongoing
  (3, 3, '2024-01-01', '2024-12-31', 700.00, 1); -- Ended

-- Rent Payments

-- Testa (Demo Loft): Missed May, paid June & July
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  (1, '2025-06', '2025-06-02', 'Paid in cash', 1),
  (1, '2025-07', '2025-06-25', 'Paid early for July', 1);

-- Max (City Flat): Paid May & June, missed July
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  
  (2, '2025-05', '2025-05-05', 'Paid on time', 1),
  (2, '2025-06', '2025-06-10', 'Paid via transfer', 1);
-- Elena (Suburb House): Paid everything last year
INSERT INTO rent_payment (apartment_id, month, payment_date, comment, user_id) VALUES
  (3, '2024-10', '2024-10-05', 'Regular', 1),
  (3, '2024-11', '2024-11-06', 'Regular', 1),
  (3, '2024-12', '2024-12-01', 'Last rent before contract end', 1);

COMMIT;