CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    instructions TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE ingredients (
    recipes_id INTEGER REFERENCES recipes,
    product_id INTEGER REFERENCES products,
    amount FLOAT,
    unit TEXT

);

CREATE TABLE basket (
    user_id INTEGER REFERENCES users,
    product_id INTEGER REFERENCES products

);

CREATE TABLE shopping_list (
    lists_id INTEGER REFERENCES lists,
    product_id INTEGER REFERENCES products,
    amount FLOAT,
    unit TEXT
);

CREATE TABLE lists (
    id SERIAL PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users
);