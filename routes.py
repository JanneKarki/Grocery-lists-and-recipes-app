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

        return redirect("/recipes/create_recipe")


@app.route("/user", methods=["GET", "POST"])
def user_page():
    
    username = session['username']
    user_id = users.get_user_id()
    user_recipes = recipes.get_user_recipes(user_id)
    print(user_recipes)
    user_lists = lists.get_user_lists(user_id)
    print(user_lists)


    if request.method == "GET":

        return render_template("user_page.html", user=username, user_recipes=user_recipes, user_lists=user_lists)

    if request.method == "POST":
       
        hidden = request.form["myField"]
        print(hidden)
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

        basket.add_recipe_to_basket(user_id, recipe_id)
        
        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data, user=maker)




@app.route("/grocery/<string:name>", methods=["GET", "POST"])
def list(name):

    id = lists.get_list_id(name)
    print(id)

    grocery_list = lists.get_grocery_list(id)

    #ingredients_data = recipes.get_recipe_ingredients(id)
    
    #instructions_data = recipes.get_recipe_instructions(id)

    return render_template("list.html", list_name=name, items=grocery_list )


@app.route("/grocery/<string:name>/edit", methods=["GET", "POST"])
def edit_list(name):

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
                

@app.route("/recipes/<string:name>/edit", methods=["GET", "POST"])
def edit_recipe(name):

    print(request.method)

    recipe_id = recipes.get_recipe_id(name)

    if request.method == "GET":

        recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)

        recipe_instructions = recipes.get_recipe_instructions(recipe_id)

        return render_template("edit_recipe.html", recipe_name=name, ingredients=recipe_ingredients, instructions=recipe_instructions)


    if request.method == "POST":

        instructions = request.form["instructions"]
        ingredients = request.form["ingredients"]

        recipes.update_recipe(recipe_id, instructions, ingredients)

        ingredients_data = recipes.get_recipe_ingredients(recipe_id)
        
        instructions_data = recipes.get_recipe_instructions(recipe_id)

        print(instructions_data, "instructions data")


        return render_template("recipe.html", recipe_name=name, ingredients=ingredients_data, instructions=instructions_data)
