from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/products")
def products():
    sample_products = [
        {"name": "Brookside Milk 500ml", "price": 120, "emoji": "🥛"},
        {"name": "Bread", "price": 75, "emoji": "🍞"},
        {"name": "Apples (1kg)", "price": 250, "emoji": "🍎"},
        {"name": "Coca-Cola 2L", "price": 180, "emoji": "🥤"},
        {"name": "Omo Washing Powder", "price": 350, "emoji": "🧼"},
        {"name": "Rice 2kg", "price": 420, "emoji": "🍚"},
    ]

    return render_template("products.html", products=sample_products)