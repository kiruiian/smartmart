from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem
)


customer_bp = Blueprint("customer", __name__)


# =========================================================
# ADD PRODUCT TO CART
# =========================================================

@customer_bp.route("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    if not cart:

        cart = Cart(
            user_id=current_user.id
        )

        db.session.add(cart)
        db.session.commit()

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

    flash(
        f"{product.name} added to cart!",
        "success"
    )

    return redirect(
        url_for("main.products")
    )


# =========================================================
# VIEW CART
# =========================================================

@customer_bp.route("/cart")
@login_required
def view_cart():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

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


# =========================================================
# INCREASE QUANTITY
# =========================================================

@customer_bp.route("/cart/increase/<int:item_id>")
@login_required
def increase_quantity(item_id):

    item = CartItem.query.get_or_404(item_id)

    if item.cart.user_id != current_user.id:

        flash(
            "Unauthorized action.",
            "danger"
        )

        return redirect(
            url_for("customer.view_cart")
        )

    item.quantity += 1

    db.session.commit()

    return redirect(
        url_for("customer.view_cart")
    )


# =========================================================
# DECREASE QUANTITY
# =========================================================

@customer_bp.route("/cart/decrease/<int:item_id>")
@login_required
def decrease_quantity(item_id):

    item = CartItem.query.get_or_404(item_id)

    if item.cart.user_id != current_user.id:

        flash(
            "Unauthorized action.",
            "danger"
        )

        return redirect(
            url_for("customer.view_cart")
        )

    if item.quantity > 1:

        item.quantity -= 1

    else:

        db.session.delete(item)

    db.session.commit()

    return redirect(
        url_for("customer.view_cart")
    )


# =========================================================
# REMOVE ITEM FROM CART
# =========================================================

@customer_bp.route("/cart/remove/<int:item_id>")
@login_required
def remove_from_cart(item_id):

    item = CartItem.query.get_or_404(item_id)

    if item.cart.user_id != current_user.id:

        flash(
            "Unauthorized action.",
            "danger"
        )

        return redirect(
            url_for("customer.view_cart")
        )

    db.session.delete(item)

    db.session.commit()

    flash(
        "Item removed from cart.",
        "info"
    )

    return redirect(
        url_for("customer.view_cart")
    )


# =========================================================
# CHECKOUT
# =========================================================

@customer_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    # Check whether cart exists
    if not cart or not cart.items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("customer.view_cart")
        )

    cart_items = cart.items

    # Calculate total
    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    # =====================================================
    # POST - PLACE ORDER
    # =====================================================

    if request.method == "POST":

        delivery_address = request.form.get(
            "delivery_address"
        )

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )

        payment_method = request.form.get(
            "payment_method"
        )

        # ---------------------------------------------
        # Validate delivery address
        # ---------------------------------------------

        if not delivery_address:

            flash(
                "Please select your delivery location.",
                "danger"
            )

            return redirect(
                url_for("customer.checkout")
            )

        # ---------------------------------------------
        # Validate payment method
        # ---------------------------------------------

        if not payment_method:

            flash(
                "Please select a payment method.",
                "danger"
            )

            return redirect(
                url_for("customer.checkout")
            )

        # ---------------------------------------------
        # Convert coordinates
        # ---------------------------------------------

        try:

            latitude = (
                float(latitude)
                if latitude
                else None
            )

            longitude = (
                float(longitude)
                if longitude
                else None
            )

        except ValueError:

            latitude = None
            longitude = None

        # =================================================
        # CREATE ORDER
        # =================================================

        order = Order(
            user_id=current_user.id,
            total_amount=total,
            delivery_address=delivery_address,
            latitude=latitude,
            longitude=longitude,
            payment_method=payment_method,
            status="Pending"
        )

        db.session.add(order)

        # Get order ID before creating items
        db.session.flush()

        # =================================================
        # CREATE ORDER ITEMS
        # =================================================

        for cart_item in cart_items:

            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            db.session.add(order_item)

        # =================================================
        # CLEAR CART
        # =================================================

        for cart_item in cart_items:

            db.session.delete(cart_item)

        # =================================================
        # SAVE ORDER
        # =================================================

        db.session.commit()

        flash(
            f"Order #{order.id} placed successfully!",
            "success"
        )

        return redirect(
            url_for(
                "customer.order_success",
                order_id=order.id
            )
        )

    # =====================================================
    # DISPLAY CHECKOUT
    # =====================================================

    return render_template(
        "customer/checkout.html",
        cart_items=cart_items,
        total=total
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@customer_bp.route("/order/<int:order_id>/success")
@login_required
def order_success(order_id):

    order = Order.query.get_or_404(order_id)

    # Security check
    if order.user_id != current_user.id:

        flash(
            "You are not authorized to view this order.",
            "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "customer/order_success.html",
        order=order
    )
# =========================================================
# MY ORDERS
# =========================================================

@customer_bp.route("/orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "customer/orders.html",
        orders=orders
    )