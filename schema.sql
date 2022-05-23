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
    instructions TEXT
);

CREATE TABLE incredients (
    recipes_id INTEGER REFERENCES recipes,
    incredients_id INTEGER REFERENCES products
);