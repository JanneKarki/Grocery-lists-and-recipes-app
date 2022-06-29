from db import db
from app import app
from flask import  render_template, session, request, redirect, abort
from werkzeug.security import check_password_hash, generate_password_hash
import products
import users
import recipes
import basket
import lists

@app.route("/")
def index():

    random_recipe = recipes.random_recipe()
    weekend_menu = recipes.random_weekend_menu()
    recipes_count = recipes.count_recipes()
    return render_template("index.html", today=random_recipe, weekend=weekend_menu ,count=recipes_count) 


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            if not users.login(username, password):
                return redirect("/login")
        except:
            if not users.login(username, password):
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

    users.logout()
    return redirect("/")


@app.route("/recipes", methods=["GET", "POST"])
def show_recipes():
    recipes.random_recipe()
    

    if request.method == "GET":
        recipes_list = recipes.get_recipes()
        print(recipes_list)
        return render_template("recipes.html", recipes=recipes_list)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        delete = request.form["delete"]
        recipe_id = request.form["recipe_id"]
        print(delete)
        print(recipe_id)
        if delete == "yes":
            recipes.delete_recipe(recipe_id)

        recipes_list = recipes.get_recipes()
        return render_template("recipes.html", recipes=recipes_list)


@app.route("/grocery",  methods=["GET","POST"])
def show_grocery_lists():

    
    if request.method == "GET":
        grocery_lists = lists.get_all_grocery_lists()
   
        return render_template("grocery.html",lists=grocery_lists)
    
    if request.method == "POST":

        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        delete = request.form["delete"]
        list_id = request.form["list_id"]
        print(delete)
        print(list_id)
        if delete == "yes":
            lists.delete_list(list_id)
        grocery_lists = lists.get_all_grocery_lists()
        return render_template("grocery.html",lists=grocery_lists)


@app.route("/products",  methods=["GET", "POST"])
def show_products():
    user_id = users.get_user_id()
    products_list = products.get_products()

    if request.method == "GET":
        return render_template("products.html",products=products_list)
    
    if request.method == "POST":
        print(session["csrf_token"])
        print(request.form["csrf_token"])
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        name = request.form["product_name"]
        checked_products = request.form["checked_products"]

        if checked_products != "":
            basket.format_and_send_to_basket(user_id, checked_products)

        products.add_product(name)

        return redirect("/products")


@app.route("/recipes/create_recipe", methods=["GET", "POST"])
def create_recipe():

    user_id = users.get_user_id()

    if request.method == "GET":
        name = ""
        instructions = ""
        ingredients = ("",)
 
        return render_template("create_recipe.html", name=name, instructions=instructions, ingredients=ingredients)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        name = request.form["name"]
        instructions = request.form["instructions"]
        ingredients = request.form["lines"]

        valid_inputs = recipes.validate_inputs()

        if valid_inputs:

            recipes_id = recipes.add_recipe(name, instructions, ingredients, user_id)
            ingredients_data = recipes.get_recipe_ingredients(recipes_id)
            instructions_data = recipes.get_recipe_instructions(recipes_id)
            maker = recipes.get_recipe_maker(recipes_id)

            return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data, user=maker)
        
        else:
            if ingredients != "":
                formatted_list = recipes.handle_incomplete_inputs(ingredients)   
            else:
                formatted_list = ("",)
                
            return render_template("create_recipe.html", name=name, instructions=instructions, ingredients=formatted_list)


@app.route("/user", methods=["GET", "POST"])
def user_page():
    
    username = session['username']
    user_id = users.get_user_id()
    user_recipes = recipes.get_user_recipes(user_id)
    user_lists = lists.get_user_lists(user_id)

    if request.method == "GET":

        return render_template("user_page.html", user=username, user_recipes=user_recipes, user_lists=user_lists)

    if request.method == "POST":

        return redirect("/user")
    

@app.route("/basket", methods=["GET", "POST"])
def show_basket():

    user_id = users.get_user_id()
    user_basket = basket.get_basket(user_id)

    if not user_basket:
        empty_tuple = ()
        empty_list = []

        for i in range(3):
            empty_list.append("")
        
        empty_tuple = tuple(empty_list)
        user_basket.append(empty_tuple)

    if request.method == "GET":    
        return render_template("basket.html", basket=user_basket)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        empty = request.form["empty"]
        if empty == "1":
            basket.empty_basket(user_id)
            return redirect("/basket")
        else:
            missing_input = request.form["missingInput"]
            shop_list = request.form["lines"]
            name = request.form["name"]
            if not missing_input:

                list_id = lists.create_grocery_list(name, user_id)
                lists.add_to_grocery_list(list_id, shop_list)
                basket.empty_basket(user_id)

            return redirect("/basket")

@app.route("/recipes/<string:name>", methods=["GET", "POST"])
def recipe(name):

    user_id = users.get_user_id()
    recipe_id = recipes.get_recipe_id(name)
    maker = recipes.get_recipe_maker(recipe_id)
    
    ingredients_data = recipes.get_recipe_ingredients(recipe_id)
    instructions_data = recipes.get_recipe_instructions(recipe_id)

    if request.method == "GET":
        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data, user=maker)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        basket.add_recipe_to_basket(user_id, recipe_id)
        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data, user=maker)


@app.route("/grocery/<string:name>", methods=["GET", "POST"])
def list(name):

    user_id = users.get_user_id()
    list_id = lists.get_list_id(name)
    maker = lists.get_list_maker(list_id)
    grocery_list = lists.get_grocery_list(list_id)

    if request.method == "GET":

        return render_template("list.html", list_name=name, items=grocery_list, user=maker)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        basket.add_list_to_basket(user_id, list_id)

    return render_template("list.html", list_name=name, items=grocery_list, user=maker)


@app.route("/grocery/<string:name>/edit", methods=["GET", "POST"])
def edit_list(name):

    user_id = users.get_user_id()
    list_id = lists.get_list_id(name)
    grocery_list = lists.get_grocery_list(list_id)
    maker = lists.get_list_maker(list_id)
    allow = lists.allow_to_edit(user_id, list_id)
    
    
    if not allow:
        return render_template("error.html", message="Oops, no rights to enter this page!")
    else:
        if request.method == "GET":
            
            return render_template("edit_list.html", list_name=name, items=grocery_list )

        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                return abort(403)

            missing_input = request.form["missingInput"]
            shop_list = request.form["lines"]
            
            if missing_input == "":
                lists.update_grocery_list(list_id, shop_list)
                grocery_list = lists.get_grocery_list(list_id)
                

                return render_template("list.html", list_name=name, items=grocery_list, user=maker)
            else:
                return render_template("list.html", list_name=name, items=grocery_list, user=maker)
                

@app.route("/recipes/<string:name>/edit", methods=["GET", "POST"])
def edit_recipe(name):

    user_id = users.get_user_id()
    recipe_id = recipes.get_recipe_id(name)
    maker = recipes.get_recipe_maker(recipe_id)
    allow = recipes.allow_to_edit(user_id, recipe_id)

    if not allow:
        return render_template("error.html", message="Oops, no rights to enter this page!")

    else:
        if request.method == "GET":

            recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
            recipe_instructions = recipes.get_recipe_instructions(recipe_id)

            return render_template("edit_recipe.html", recipe_name=name, ingredients=recipe_ingredients, instructions=recipe_instructions)

        if request.method == "POST":
            
            if session["csrf_token"] != request.form["csrf_token"]:
                return abort(403)

            instructions = request.form["instructions"]
            ingredients = request.form["lines"]

            
            valid_inputs = recipes.validate_inputs()

            if valid_inputs:

                recipes.update_recipe(recipe_id, instructions, ingredients)

                ingredients_data = recipes.get_recipe_ingredients(recipe_id)
                instructions_data = recipes.get_recipe_instructions(recipe_id)

                return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data, user=maker)
            
            else:
                if ingredients != "":
                    formatted_list = recipes.handle_incomplete_inputs(ingredients)   
                else:
                    formatted_list = ("",)
                return render_template("edit_recipe.html", recipe_name=name, ingredients=formatted_list, instructions=instructions)

@app.route("/recipes/<string:name>/delete", methods=["GET", "POST"])
def delete_recipe(name):
    print(name)

    user_id = users.get_user_id()
    recipe_id = recipes.get_recipe_id(name)
    allow = recipes.allow_to_edit(user_id, recipe_id)
    recipe = ["recipe"]

    if not allow:
        return render_template("error.html", message="Oops, no rights to delete this recipe!")

    else:
        if request.method == "GET":
            return render_template("delete.html", deleting=recipe, recipe_name=name, recipe_id=recipe_id)


@app.route("/lists/<string:name>/delete", methods=["GET", "POST"])
def delete_list(name):
    print(name)

    user_id = users.get_user_id()
    list_id = lists.get_list_id(name)
    allow = lists.allow_to_edit(user_id, list_id)
    list = ["list"]
    
    if not allow:
        return render_template("error.html", message="Oops, no rights to delete this list!")
    else:
        if request.method == "GET":
            return render_template("delete.html", deleting=list, list_name=name, list_id=list_id)
