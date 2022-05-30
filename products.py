from db import db


def get_products():
    sql = "SELECT * FROM products"
    products_list = db.session.execute(sql).fetchall()
    return products_list

def add_product(name):
    sql = """INSERT INTO products (name)
                    VALUES (:name) RETURNING id"""
    product_id = db.session.execute(sql, {"name":name})
    db.session.commit()

    return product_id