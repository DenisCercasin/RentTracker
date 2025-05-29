CREATE TABLE apartment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL 
    
);
CREATE TABLE tenant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    tel_num NUMBER,
    IDNP NUMBER
);
CREATE TABLE rental_agreement (
    apartment_id INTEGER,
    tenant_id INTEGER,
    PRIMARY KEY (apartment_id, tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartment (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenant (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);