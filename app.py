from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/recipes")
def show_recipes():
    return render_template("recipes.html")


@app.route("/grocery",  methods=["POST"])
def show_grocery_lists():
    return render_template("grocery.html")