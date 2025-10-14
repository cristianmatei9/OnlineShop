from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from extensions import db
from models import Product, User, CartItem
from repository import CartRepository
from service import CartService
from flask_migrate import Migrate
from validators import CartValidator

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

repository = CartRepository()
validator = CartValidator()
service = CartService(repository, validator)


with app.app_context():
    if not Product.query.first():
        db.session.add(Product(productName="Laptop", productPrice=3000, productStock=5))
        db.session.add(Product(productName="Mouse", productPrice=100, productStock=20))
        db.session.add(Product(productName="Keyboard", productPrice=200, productStock=15))
        db.session.commit()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Login succesful", "userID": user.userID}), 200
    if user.password == data["password"]:
        return jsonify({"message": "Login succesful", "userID": user.userID}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.json
        hashed_pw = generate_password_hash(data.get('password'))
        user = User(username=data.get('username'), password=hashed_pw)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User created", "userID": user.userID}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Registration failed"}), 500
    else:
        return render_template("register.html")

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = [
        {
            "id": p.productID,         # compatibil cu shop.js
            "name": p.productName,
            "price": p.productPrice,
            "stock": p.productStock
        }
        for p in products
    ]
    return jsonify(result)

@app.route("/api/cart/<int:userID>", methods=["GET"])
def get_cart(userID):
    try:
        items = service.getAllCart(userID)
        total = sum(item.quantity * item.product.productPrice for item in items)
        result = {
            "items": [
                {
                    "itemID": i.itemID,
                    "prodID": i.prodID,  # foreign key
                    "productName": i.product.productName,
                    "quantity": i.quantity,
                    "price": i.product.productPrice
                }
                for i in items
            ],
            "total": total
        }
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Internal server error"}), 500

@app.route("/api/cart/<int:userID>/add", methods=["POST"])
def add_to_cart(userID):
    data = request.get_json()
    prod_id = data.get("prodID")
    quantity = data.get("quantity", 1)

    try:
        print(f"Adding to cart: userID={userID}, prodID={prod_id}, quantity={quantity}")
        cart_item = service.add_to_cart(userID, prod_id, quantity)
        db.session.commit()
        print(f"Added item with ID {cart_item.itemID}")
        return jsonify({"message": "Item added", "cart_item_id": cart_item.itemID}), 200
    except ValueError as e:
        db.session.rollback()
        print("ValueError:", e)
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print("Exception:", e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/api/cart/<int:userID>/decrease", methods=["POST"])
def decrease_from_cart(userID):
    data = request.get_json()
    try:
        service.decrease_from_cart(userID, data.get("prodID"))
        db.session.commit()
        return jsonify({"message": "Quantity updated"}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route("/api/cart/<int:cartItemID>/remove", methods=["DELETE"])
def remove_from_cart(cartItemID):
    try:
        service.delete_from_cart(cartItemID)
        db.session.commit()
        return jsonify({"message": "Item removed"}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route("/api/cart/<int:userID>/checkout", methods=["POST"])
def checkout(userID):
    try:
        total = service.checkoutCart(userID)
        db.session.commit()
        return jsonify({"message": "Checkout successful", "total": total}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/after_register/<int:userID>")
def after_register(userID):
    return redirect(f"/shop?userID={userID}")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")


if __name__ == "__main__":
    app.run(debug=True)