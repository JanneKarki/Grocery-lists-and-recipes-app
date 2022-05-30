from db import db


def get_products():
    sql = "SELECT * FROM products"
    products_list = db.session.execute(sql).fetchall()
    return products_list

def add_product(name):

    product = find_product(name)

    if not product:
        print("not product in the list")
        sql = """INSERT INTO products (name)
                        VALUES (:name) RETURNING id"""
        product_id = db.session.execute(sql, {"name":name})
        db.session.commit()

        return product_id
        
    return product[0]   


def find_product(name):
    sql = """SELECT * FROM products WHERE name=:name"""

    product = db.session.execute(sql, {"name":name}).fetchone()
    print(product)
    return product

