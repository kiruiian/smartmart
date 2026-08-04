from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


# Landing Page
@main_bp.route("/")
def home():

    # If user is already logged in,
    # send them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    # Otherwise show the landing page
    return render_template("landing.html")


# Dashboard
@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user=current_user
    )


# Products
@main_bp.route("/products")
@login_required
def products():

    sample_products = [
        {
            "name": "Brookside Milk 500ml",
            "price": 120,
            "emoji": "🥛"
        },
        {
            "name": "Bread",
            "price": 75,
            "emoji": "🍞"
        },
        {
            "name": "Apples (1kg)",
            "price": 250,
            "emoji": "🍎"
        },
        {
            "name": "Rice 2kg",
            "price": 420,
            "emoji": "🍚"
        },
        {
            "name": "Coca-Cola 2L",
            "price": 180,
            "emoji": "🥤"
        },
        {
            "name": "Omo Washing Powder",
            "price": 350,
            "emoji": "🧼"
        },
    ]

    return render_template(
        "products.html",
        products=sample_products
    )