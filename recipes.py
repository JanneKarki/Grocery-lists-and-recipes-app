from db import db
from products import add_product

def add_recipe(name, instructions, incredients, user_id):

    sql = """INSERT INTO recipes (name, instructions, user_id)
                            VALUES (:name, :instructions, :user_id) RETURNING id"""

    recipe_id = db.session.execute(sql, {"name":name, "instructions":instructions, "user_id":user_id}).fetchone()[0]
    print(recipe_id)
    db.session.commit()
    print(incredients)

    incredients_list = incredients.splitlines()

    print(incredients_list)
    for item in incredients_list:
        add_product(item)

        
'''
        sql = """INSERT INTO incredients (recipe_id, product_id)
                VALUES (:name, :instructions)"""

        db.session.execute(sql, {"recipe_id":recipe_id, "product_id":product_id})
        db.session.commit()
'''


def add_incredients_to_products_db(incredients):

    incredients_list = incredients.split('/n')

    for item in incredients_list():

        sql = """INSERT INTO products (name)
                VALUES (:name) RETURNING id"""

        product_id = db.session.excecute(sql, {"name":item})
        db.session.commit()
