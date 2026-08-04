from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models import Product

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@admin_bp.route("/products")
@login_required
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin/products.html", products=products)


@admin_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        product = Product(
            name=request.form.get("name"),
            description=request.form.get("description"),
            category=request.form.get("category"),
            price=float(request.form.get("price")),
            stock=int(request.form.get("stock"))
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")

        return redirect(url_for("admin.products"))

    return render_template("admin/add_product.html")