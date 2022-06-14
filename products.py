from db import db
import basket

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
        product_id = db.session.execute(sql, {"name":name}).fetchone()
        db.session.commit()
        
        return product_id[0]
    
    return product[0]


def find_product(name):
    sql = """SELECT * FROM products WHERE name=:name"""

    product = db.session.execute(sql, {"name":name}).fetchone()
    return product

def send_to_basket(user_id, products):
    list = products.split()
    print(list, "lista")
    basket.add_to_basket(user_id, list)


    