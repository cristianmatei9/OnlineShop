from models import db, CartItem
from sqlalchemy.exc import SQLAlchemyError

class CartRepository:
    def __init__(self):
        pass

    def addCartItem(self, userID, prodID, quantity=1):
        cartItem = CartItem(userID=userID, prodID=prodID, quantity=quantity)
        db.session.add(cartItem)
        return cartItem

    def removeCartItem(self, cartItemID):
        cartItem = CartItem.query.get(cartItemID)
        if cartItem:
            db.session.delete(cartItem)
            return True
        return False

    def getCartForUser(self, userID):
        return CartItem.query.filter_by(userID=userID).all()

    def clearCartForUser(self, userID):
        CartItem.query.filter_by(userID=userID).delete()
        return True