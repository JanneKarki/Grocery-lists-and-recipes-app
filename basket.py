from db import db
import products
import recipes

def add_to_basket(user_id, product_list):

    sql = "INSERT INTO basket (user_id, product_id, amount, unit) values (:user_id, :product_id, :amount, :unit )"

    print(product_list, "product list")
    
    for i in range(len(product_list)):
        print(product_list[i], "onko tämä se just")
        product_id = products.add_product(product_list[i][0])
        amount = product_list[i][1]
        unit = product_list[i][2]

        if not find_from_basket(product_id):

            db.session.execute(sql, {"user_id": user_id, "product_id":product_id, "amount":amount, "unit": unit})

            db.session.commit()


def empty_basket(user_id):

    sql = "DELETE FROM basket WHERE user_id=user_id"

    db.session.execute(sql, {"user_id":user_id})

    db.session.commit()

def get_basket(user_id):

    sql = "SELECT products.name, basket.amount, basket.unit FROM products, basket WHERE products.id = basket.product_id AND basket.user_id=user_id" 

    basket_list = db.session.execute(sql, {"user_id":user_id}).fetchall()

    return basket_list

def add_recipe_to_basket(user_id, recipe_id):

    ingredients = recipes.get_recipe_ingredients(recipe_id)

    add_to_basket(user_id, ingredients)
    

def format_and_send_to_basket(user_id, products_string):
    print(products_string)
    product_list = products_string.split()
    formatted_list = []

    for i in range(len(product_list)):
        product = product_list[i]
        amount = 0.0
        unit = "-"
        
        formatted_list.append((product, amount, unit))

    add_to_basket(user_id, formatted_list)

    
def find_from_basket(id):

    sql = "SELECT * FROM basket WHERE product_id =:id"

    result = db.session.execute(sql, {"id":id}).fetchone()

    print(result)

    if not result:
        return False
    
    return True

