from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product

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

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        "products.html",
        products=products
    )