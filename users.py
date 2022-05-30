
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def register_user(username, password_hash_value):

    sql = """INSERT INTO users (username, password)
                        VALUES (:username, :password)"""
    db.session.execute(sql, {"username":username, "password":password_hash_value})
    db.session.commit()

def login(username, password):

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False

    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
            
        else:
            return False
    
def get_user_id():
    return session.get("user_id", 0)