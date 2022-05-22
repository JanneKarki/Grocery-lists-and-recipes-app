from flask import Flask, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html") 


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # TODO: check username and password

        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return redirect("/login")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                return redirect("/login")

       
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)


        sql = """INSERT INTO users (username, password)
                    VALUES (:username, :password)"""
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        


        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/recipes", methods=["POST"])
def show_recipes():
    return render_template("recipes.html")


@app.route("/grocery",  methods=["POST"])
def show_grocery_lists():
    return render_template("grocery.html")


@app.route("/products",  methods=["GET", "POST"])
def show_products():

    sql = "SELECT * FROM products "

    products_list = db.session.execute(sql).fetchall()

    if request.method == "GET":
        return render_template("products.html",products=products_list)
    
    if request.method == "POST":
        name = request.form["name"]
        

        sql = """INSERT INTO products (name)
                    VALUES (:name)"""
        db.session.execute(sql, {"name":name})
        db.session.commit()

        return redirect("/products")
