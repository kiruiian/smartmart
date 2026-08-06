from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Product, Cart, CartItem

customer_bp = Blueprint("customer", __name__)


# ==========================================
# Add Product to Cart
# ==========================================
@customer_bp.route("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    # Get user's cart
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    # Create cart if it doesn't exist
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # Check if product already exists in cart
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()

    flash(f"{product.name} added to cart!", "success")

    return redirect(url_for("main.products"))


# ==========================================
# View Shopping Cart
# ==========================================
@customer_bp.route("/cart")
@login_required
def view_cart():

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if not cart:
        return render_template(
            "customer/cart.html",
            cart_items=[],
            total=0
        )

    cart_items = cart.items

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render_template(
        "customer/cart.html",
        cart_items=cart_items,
        total=total
    )