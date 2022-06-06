from db import db
import products

def add_to_basket(user_id, product):
    
    product_id = products.find_product(product)
    
    sql = "INSERT INTO basket (user_id, product_id) values (:user_id, :product_id)"

    db.session.execute(sql, {"user_id": user_id, "product_id":product_id})

    db.session.commit()

def empty_basket(user_id):

    sql = "DELETE FROM basket WHERE user_id=user_id"

    db.session.execute(sql, {"user_id":user_id})

    db.session.commit()

def get_basket(user_id):

    sql = "SELECT * FROM basket WHERE user_id=user_id" 

    basket_list = db.session.execute(sql, {"user_id":user_id}).fetchall()

    return basket_list
