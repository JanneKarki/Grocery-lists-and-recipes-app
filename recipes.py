from db import db
from products import add_product, find_product

def add_recipe(name, instructions, ingredients, user_id):

    sql = """INSERT INTO recipes (name, instructions, user_id)
                            VALUES (:name, :instructions, :user_id) RETURNING id"""

    recipes_id = db.session.execute(sql, {"name":name, "instructions":instructions, "user_id":user_id}).fetchone()[0]

    print(recipes_id)

    db.session.commit()
   
    ingredients_list = ingredients.split()

    add_ingredients_to_products_db(ingredients_list, recipes_id)
   


    return recipes_id

        
'''
        sql = """INSERT INTO incredients (recipe_id, product_id)
                VALUES (:name, :instructions)"""

        db.session.execute(sql, {"recipe_id":recipe_id, "product_id":product_id})
        db.session.commit()
'''


def add_ingredients_to_products_db(ingredients_list, recipes_id):

    for i in range(0, len(ingredients_list), 3):
        print(ingredients_list[i])
        product_id = add_product(ingredients_list[i])
        amount = ingredients_list[i+1]
        unit = ingredients_list[i+2]
        add_to_ingredients(recipes_id, product_id, amount, unit )


def add_to_ingredients(recipes_id, product_id, amount, unit):
   
        sql = """INSERT INTO ingredients (recipes_id, product_id, amount, unit)
                VALUES (:recipes_id, :product_id, :amount, :unit)"""

        db.session.execute(sql, {"recipes_id":recipes_id, "product_id":product_id, "amount":amount, "unit":unit })
        db.session.commit()
    


def get_recipes():

    sql = "SELECT * FROM recipes"
    recipes_list = db.session.execute(sql).fetchall()
    return recipes_list

def get_recipe_instructions(id):
    sql = "SELECT instructions FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result[0] 

def get_recipe_ingredients(id):
    print(id)
    sql = "SELECT product_id, amount, unit FROM ingredients WHERE recipes_id=:id"
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result

def get_recipe_id(name):
    sql = "SELECT id FROM recipes WHERE name=:name"
    result = db.session.execute(sql, {"name":name}).fetchone()
    return result[0]
