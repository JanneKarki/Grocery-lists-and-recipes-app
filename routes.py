from db import db
from app import app
from flask import  render_template, session, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import products
import users
import recipes
import basket
import lists

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
    user_id = users.get_user_id()
    del session["username"]
    basket.empty_basket(user_id)
    return redirect("/")


@app.route("/recipes", methods=["GET", "POST"])
def show_recipes():

    recipes_list = recipes.get_recipes()

    return render_template("recipes.html", recipes=recipes_list)
        

@app.route("/grocery",  methods=["GET","POST"])
def show_grocery_lists():

    grocery_lists = lists.get_all_grocery_lists()
   
    if request.method == "GET":
        return render_template("grocery.html",lists=grocery_lists)
    
    if request.method == "POST":

        return redirect("/grocery")


@app.route("/products",  methods=["GET", "POST"])
def show_products():
    user_id = users.get_user_id()
    products_list = products.get_products()

    if request.method == "GET":
        return render_template("products.html",products=products_list)
    
    if request.method == "POST":
        name = request.form["name"]

        checked_products = request.form["checked_products"]

        print(checked_products, "asödlfkaskdf")

        if checked_products != "":
            print(checked_products, "checekd products")
            basket.format_and_send_to_basket(user_id, checked_products)

           

        
        products.add_product(name)

        return redirect("/products")


@app.route("/recipes/create_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "GET":
        return render_template("create_recipe.html")

    if request.method == "POST":
       
        name = request.form["name"]
        instructions = request.form["instructions"]
        ingredients = request.form["ingredients"]

       
        user_id = users.get_user_id()
   
        recipes.add_recipe(name, instructions, ingredients, user_id)


        
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


@app.route("/basket", methods=["GET", "POST"])
def show_basket():
    user_id = users.get_user_id()
    user_basket = basket.get_basket(user_id)

    if request.method == "GET":    
        return render_template("basket.html", basket=user_basket)

    if request.method == "POST":
        missing_input = request.form["missingInput"]
        shop_list = request.form["lines"]
        name = request.form["name"]
        if not missing_input:

            list_id = lists.create_grocery_list(name, user_id)
            lists.add_to_grocery_list(list_id, shop_list)
            basket.empty_basket()

        return redirect("/basket")

@app.route("/recipes/<string:name>", methods=["GET", "POST"])
def recipe(name):
    user_id = users.get_user_id()
    recipe_id = recipes.get_recipe_id(name)
    
    ingredients_data = recipes.get_recipe_ingredients(recipe_id)
        
    instructions_data = recipes.get_recipe_instructions(recipe_id)

    if request.method == "GET":
       
        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data)

    if request.method == "POST":

        basket.add_recipe_to_basket(user_id, recipe_id)
        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data)




@app.route("/grocery/<string:name>", methods=["GET", "POST"])
def list(name):

    id = lists.get_list_id(name)
    print(id)

    grocery_list = lists.get_grocery_list(id)

    #ingredients_data = recipes.get_recipe_ingredients(id)
    
    #instructions_data = recipes.get_recipe_instructions(id)

    return render_template("list.html", list_name=name, items=grocery_list )


@app.route("/grocery/<string:name>/edit", methods=["GET", "POST"])
def edit(name):

    list_id = lists.get_list_id(name)
    print(list_id)

    grocery_list = lists.get_grocery_list(list_id)

    if request.method == "GET":
        
        return render_template("edit_list.html", list_name=name, items=grocery_list )

    if request.method == "POST":
        missing_input = request.form["missingInput"]
        shop_list = request.form["lines"]
        
        if missing_input == "":
            lists.update_grocery_list(list_id, shop_list)
            grocery_list = lists.get_grocery_list(list_id)
            

            return render_template("list.html", list_name=name, items=grocery_list)
        else:
            return render_template("list.html", list_name=name, items=grocery_list)
                

        