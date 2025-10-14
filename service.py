from models import Product, CartItem, db
from repository import CartRepository
from validators import CartValidator

class CartService:
    def __init__(self, repo: CartRepository, validator: CartValidator):
        self.cartRepo = repo
        self.validator = validator

    def add_to_cart(self, user_id, prod_id, quantity=1):
        product = Product.query.get(prod_id)
        self.validator.validateAdd(product, quantity)
        return self.cartRepo.addCartItem(user_id, prod_id, quantity)

    def delete_from_cart(self, cart_item_id):
        success = self.cartRepo.removeCartItem(cart_item_id)
        self.validator.validateDelete(success)
        return True

    def decrease_from_cart(self, user_id, prod_id):
        item = CartItem.query.filter_by(userID=user_id, prodID=prod_id).first()
        self.validator.validateDecrease(item)
        product = item.product
        product.productStock += 1
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
        return True


    def checkoutCart(self, user_id):
        items = self.cartRepo.getCartForUser(user_id)
        self.validator.validateCheckout(items)
        total = 0
        for item in items:
            product = item.product
            total += item.quantity * product.productPrice
            product.productStock -= item.quantity
            db.session.delete(item)
        return total


    def getAllCart(self, user_id):
        return self.cartRepo.getCartForUser(user_id)

    def sortByPrice(self, user_id):
        sortedProducts = self.cartRepo.getCartForUser(user_id)
        return sorted(sortedProducts, key=lambda p: p.price)