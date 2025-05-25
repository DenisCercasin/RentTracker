BEGIN TRANSACTION;

-- Clear old data
DELETE FROM rental_agreement;
DELETE FROM tenant;
DELETE FROM apartment;
DELETE FROM sqlite_sequence;

-- Insert apartments
INSERT INTO apartment (name, address) VALUES ("Apartment 1", "Strada Alba Iulia 23");
INSERT INTO apartment (name, address) VALUES ("Apartment 2", "Bulevardul Dacia 10/1");
INSERT INTO apartment (name, address) VALUES ("Apartment 3", "Calea Orheiului 145");

-- Insert tenants
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Ion Popescu", 37376123456, 1234567890123);
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Maria Ivanova", 37378112233, 2345678901234);
INSERT INTO tenant (name, tel_num, IDNP) VALUES ("Alexei Moraru", 37379223344, 3456789012345);

-- Insert rental agreements (links tenant to apartment)
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, rent_amount) VALUES (1, 1, "2025-05-01", 400);
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, rent_amount) VALUES (2, 2, "2025-06-01", 500);
INSERT INTO rental_agreement (apartment_id, tenant_id, start_date, rent_amount) VALUES (3, 3, "2025-07-01", 600);

COMMIT;
