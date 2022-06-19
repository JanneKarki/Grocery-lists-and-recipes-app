from db import db
import products


def add_to_grocery_list(lists_id, shop_list):
    listed_items = shop_list.split()
    print(listed_items, "listed item")

    sql = "INSERT INTO shopping_list (lists_id, product_id, amount, unit) values (:lists_id, :product_id, :amount, :unit)"

    for i in range (0,len(listed_items), 3):
        print(listed_items[i])

        product_id = products.add_product(listed_items[i])
        print(product_id, "product_id")
        db.session.execute(sql, {"lists_id": lists_id, "product_id":product_id, "amount": listed_items[i+1], "unit": listed_items[i+2]})

    db.session.commit()

    return

def create_grocery_list(name, user_id):

    sql = "INSERT INTO lists (name, user_id) values (:name, :user_id) RETURNING ID "

    list_id = db.session.execute(sql, {"name": name, "user_id": user_id}).fetchone()

    db.session.commit()

    return list_id[0]

def get_all_grocery_lists():

    sql = "SELECT * FROM lists"

    result = db.session.execute(sql).fetchall()

    db.session.commit()

    return result

def get_list_id(name):

    sql = "SELECT id FROM lists WHERE name=:name"

    result = db.session.execute(sql, {"name":name}).fetchone()

    return result[0]

def get_grocery_list(id):

    sql = """SELECT products.name,
            shopping_list.amount,
            shopping_list.unit
            FROM
            products,
            shopping_list 
            WHERE 
            products.id=shopping_list.product_id
            AND
            lists_id=:id
            """
            
    result = db.session.execute(sql, {"id":id}).fetchall()
    return result

def update_grocery_list(list_id, shop_list):
    
    sql = "DELETE FROM shopping_list WHERE lists_id=:list_id"

    db.session.execute(sql, {"list_id": list_id})

    add_to_grocery_list(list_id, shop_list)

    return




    return