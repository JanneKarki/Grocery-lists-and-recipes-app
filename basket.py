from db import db
import products

def add_to_basket(user_id, product):

    print(user_id, "user id")
    print(product, "productlist")

    sql = "INSERT INTO basket (user_id, product_id) values (:user_id, :product_id)"
    
    for i in range(0, len(product)):
        
        product_id = products.add_product(product[i])
        print(product_id)
        db.session.execute(sql, {"user_id": user_id, "product_id":product_id})

    db.session.commit()

def empty_basket(user_id):

    sql = "DELETE FROM basket WHERE user_id=user_id"

    db.session.execute(sql, {"user_id":user_id})

    db.session.commit()

def get_basket(user_id):

    sql = "SELECT products.name FROM products, basket WHERE products.id = basket.product_id AND basket.user_id=user_id" 

    basket_list = db.session.execute(sql, {"user_id":user_id}).fetchall()

    return basket_list
