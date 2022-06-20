from db import db
from products import add_product, find_product

def add_recipe(name, instructions, ingredients, user_id):

    sql = """INSERT INTO recipes (name, instructions, user_id)
                            VALUES (:name, :instructions, :user_id) RETURNING id"""

    recipes_id = db.session.execute(sql, {"name":name, "instructions":instructions, "user_id":user_id}).fetchone()[0]

    print(recipes_id)

    db.session.commit()
   
    ingredients_list = ingredients.split()

    add_ingredients(ingredients_list, recipes_id)
   


    return recipes_id


def add_ingredients(ingredients_list, recipes_id):

    sql = """INSERT INTO ingredients (recipes_id, product_id, amount, unit)
                VALUES (:recipes_id, :product_id, :amount, :unit)"""    

    for i in range(0, len(ingredients_list), 3):
        
        product_id = add_product(ingredients_list[i])
        amount = ingredients_list[i+1]
        unit = ingredients_list[i+2]

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
    sql = "SELECT products.name, ingredients.amount, ingredients.unit FROM ingredients, products WHERE ingredients.recipes_id=:id AND ingredients.product_id=products.id "
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result

def get_recipe_id(name):
    sql = "SELECT id FROM recipes WHERE name=:name"
    result = db.session.execute(sql, {"name":name}).fetchone()
    return result[0]

def get_user_recipes(user_id):

    sql = "SELECT name FROM recipes WHERE  user_id=:user_id"

    result = db.session.execute(sql, {"user_id":user_id}).fetchall()

    return result

def update_recipe(recipe_id, instructions, ingredients):

    ingredients = ingredients.split()

    sql = "UPDATE recipes SET instructions=:instructions WHERE recipes.id=:recipe_id"

    db.session.execute(sql, {"instructions":instructions, "recipe_id":recipe_id})

    db.session.commit()

    _update_recipe_ingredients(recipe_id, ingredients)

    return

def _update_recipe_ingredients(recipe_id, ingredients):

    sql = "DELETE FROM ingredients WHERE recipes_id=:recipe_id"

    db.session.execute(sql, {"recipe_id": recipe_id})

    add_ingredients(ingredients, recipe_id)
    
    return

def get_recipe_maker(recipe_id):

    sql = "SELECT users.username FROM users, recipes WHERE users.id=recipes.user_id AND recipes.id=:recipe_id"

    result =db.session.execute(sql, {"recipe_id":recipe_id}).fetchone()

    return result


