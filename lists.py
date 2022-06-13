from db import db
import products


def add_to_grocery_list(lists_id, shop_list):
    listed_items = shop_list.split()
    print(listed_items)

    sql = "INSERT INTO shopping_list (lists_id, product_id, amount, unit) values (:lists_id, :product_id, :amount, :unit)"

    for i in range (0,len(listed_items), 3):
        print(listed_items[i])

        product_id = products.find_product(listed_items[i])

        db.session.execute(sql, {"lists_id": lists_id, "product_id":product_id[0], "amount": listed_items[i+1], "unit": listed_items[i+2]})

    db.session.commit()

    return

def create_grocery_list(name, user_id):

    sql = "INSERT INTO lists (name, user_id) values (:name, :user_id) RETURNING ID "

    list_id = db.session.execute(sql, {"name": name, "user_id": user_id}).fetchone()

    db.session.commit()

    return list_id[0]



