from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# USER MODEL

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    cart = db.relationship(
        "Cart",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):

        return f"<User {self.email}>"

# PRODUCT MODEL

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    image = db.Column(
        db.String(255),
        default="default.jpg"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Product → CartItems
    cart_items = db.relationship(
        "CartItem",
        back_populates="product",
        lazy=True
    )

    def __repr__(self):

        return f"<Product {self.name}>"


# CART MODEL
class Cart(db.Model):

    __tablename__ = "cart"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    items = db.relationship(
        "CartItem",
        backref="cart",
        lazy=True,
        cascade="all, delete-orphan"
    )

# CART ITEM MODEL

class CartItem(db.Model):

    __tablename__ = "cart_item"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("cart.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    # CartItem → Product
    product = db.relationship(
        "Product",
        back_populates="cart_items"
    )

# ORDER MODEL


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    delivery_address = db.Column(
        db.Text,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Order → User
    user = db.relationship(
        "User",
        backref="orders"
    )

    # Order → OrderItems
    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return f"<Order {self.id}>"

# ORDER ITEM MODEL

class OrderItem(db.Model):

    __tablename__ = "order_item"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    # OrderItem → Product
    product = db.relationship(
        "Product"
    )

    def __repr__(self):

        return f"<OrderItem {self.id}>"