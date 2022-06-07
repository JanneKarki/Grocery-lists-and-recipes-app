from db import db
from app import app
from flask import  render_template, session, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import products
import users
import recipes
import basket

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
        user_role = None
        try:
            user_role = request.form["administrator"]
            if not users.login(username, password, user_role):
                return redirect("/login")
            print(user_role)
        except:
            if not users.login(username, password, user_role):
                return redirect("/login")
               
            
        return redirect("/")
            

       
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash_value = generate_password_hash(password)

        users.register_user(username, password_hash_value)
        


        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/recipes", methods=["GET", "POST"])
def show_recipes():
    return render_template("recipes.html")


@app.route("/grocery",  methods=["GET","POST"])
def show_grocery_lists():

    products_list = products.get_products()
   
    if request.method == "GET":
        return render_template("grocery.html",products=products_list)
    
    if request.method == "POST":


        return redirect("/grocery")


@app.route("/products",  methods=["GET", "POST"])
def show_products():
    print(users.get_user_id())
    products_list = products.get_products()

    if request.method == "GET":
        return render_template("products.html",products=products_list)
    
    if request.method == "POST":
        name = request.form["name"]

        checked_products = request.form["checked_products"]
        if checked_products != "":
            print("checked none")
            print(checked_products)

        
        products.add_product(name)

        return redirect("/products")


@app.route("/recipes/create_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "GET":
        return render_template("create_recipe.html")

    if request.method == "POST":
       
        name = request.form["name"]
        instructions = request.form["instructions"]
        incredients = request.form["incredients"]
        user_id = users.get_user_id()
    
        recipes.add_recipe(name, instructions, incredients, user_id)
        
      #  sql = """INSERT INTO recipes (name, instructions)
       #                 VALUES (:name, :instructions) RETURNING id"""

      #  id = db.session.execute(sql, {"name":name, "instructions":instructions}).fetchone()[0]
      #  print(id)
      #  db.session.commit()

      #  sql = """INSERT INTO incredients (name, instructions)
       #                 VALUES (:name, :instructions) RETURNING id"""

        return redirect("/recipes/create_recipe")

@app.route("/testpage", methods=["GET", "POST"])
def test():
    if request.method == "GET":

        return render_template("testpage.html")

    if request.method == "POST":
       
        hidden = request.form["myField"]
        print(hidden)
        return redirect("/testpage")


@app.route("/basket")
def show_basket():
    user_id = users.get_user_id()
    user_basket = basket.get_basket(user_id)
    return render_template("basket.html", basket=user_basket)