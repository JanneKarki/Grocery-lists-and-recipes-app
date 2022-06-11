from db import db
import products


def add_to_grocery_list():
    return

def create_grocery_list(name, user_id):

    sql = "INSERT INTO lists (name, user_id) values (:name, :user_id) RETURNING ID "

    list_id = db.session.execute(sql, {"name": name, "user_id": user_id})

    db.session.commit()

    return list_id