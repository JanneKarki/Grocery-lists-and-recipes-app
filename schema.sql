CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    quantity INTEGER,
    unit TEXT,
    gategory TEXT
);