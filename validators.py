from itertools import product

from models import Product

class CartValidator:
    @staticmethod
    def validateAdd(product: Product, quantity: int):
        print("Validating add:", product, quantity)
        if not product:
            raise ValueError("Product not found")

        if product.productStock < quantity:
            raise ValueError("Not enough stock")

    @staticmethod
    def validateDecrease(item):
        print("Validating decrease:", item)
        if not item:
            raise ValueError("Item not found")

    @staticmethod
    def validateDelete(success: bool):
        if not success:
            raise ValueError("Item not found")

    @staticmethod
    def validateCheckout(items):
        if not items:
            raise ValueError("Cart is empty")
        for item in items:
            if item.product.productStock < item.quantity:
                raise ValueError(f"Not enough stock for {item.product.productName}")