from app import app, db
from models import User, Product, CartItem
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    print(inspector.get_table_names())
    print("=== USERS ===")
    users = User.query.all()
    for u in users:
        print(u.userID, u.username)

    print("\n=== PRODUCTS ===")
    products = Product.query.all()
    for p in products:
        print(p.productID, p.productName, p.productStock)