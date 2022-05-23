from db import db


def get_products():
    sql = "SELECT * FROM products"
    products_list = db.session.execute(sql).fetchall()
    return products_list

def add_product(name):
    sql = """INSERT INTO products (name)
                    VALUES (:name)"""
    db.session.execute(sql, {"name":name})
    db.session.commit() 