CREATE TABLE apartment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    
);
CREATE TABLE tenant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    tel_num NUMBER,
    IDNP NUMBER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE rental_agreement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apartment_id INTEGER NOT NULL,
    tenant_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,  -- can be NULL if current
    rent_amount REAL NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES apartment (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenant (id) ON UPDATE CASCADE ON DELETE CASCADE
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    telegram_token TEXT,
    telegram_chat_id TEXT,
    reminder_day INTEGER,
    reminder_enabled BOOLEAN DEFAULT 0
);
CREATE TABLE rent_payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apartment_id INTEGER NOT NULL,
    month TEXT NOT NULL,                    -- Format: YYYY-MM
    payment_date TEXT DEFAULT CURRENT_DATE, -- Actual payment date
    comment TEXT,                           -- Optional comment
    user_id INTEGER NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES apartment(id) ON DELETE CASCADE
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE

);
